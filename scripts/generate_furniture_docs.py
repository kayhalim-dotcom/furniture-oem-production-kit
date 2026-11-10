"""Generate basic, human-reviewable OEM furniture release documents from catalog JSON.

This tool is intentionally dependency-free. The SVG views communicate the overall
product envelope only; they are not machine-ready drawings or a substitute for CAD.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "catalog.json"
OUT_DIR = ROOT / "generated"
CODE_RE = re.compile(r"^[A-Z0-9][A-Z0-9_-]*$")


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_product(product: dict[str, Any], catalog_code: str) -> list[str]:
    errors: list[str] = []
    for key in ("product_code", "product_name", "revision", "overall_dimensions_mm", "components", "hardware", "assembly_steps", "quality_checks", "packaging"):
        if key not in product:
            errors.append(f"{catalog_code}: missing required field '{key}'")
    if product.get("product_code") != catalog_code:
        errors.append(f"{catalog_code}: product_code does not match catalog entry")
    dimensions = product.get("overall_dimensions_mm", {})
    for key in ("width", "depth", "height"):
        value = dimensions.get(key)
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"{catalog_code}: overall_dimensions_mm.{key} must be a positive number")
    components = product.get("components", [])
    if not isinstance(components, list) or not components:
        errors.append(f"{catalog_code}: components must be a non-empty list")
        components = []
    seen_parts: set[str] = set()
    for index, part in enumerate(components):
        part_no = part.get("part_no", f"index {index}")
        if part_no in seen_parts:
            errors.append(f"{catalog_code}: duplicate part_no '{part_no}'")
        seen_parts.add(part_no)
        for key in ("name", "material_code", "finished_size_mm", "quantity", "operations"):
            if key not in part:
                errors.append(f"{catalog_code}/{part_no}: missing '{key}'")
        size = part.get("finished_size_mm", {})
        for key in ("width", "height", "thickness"):
            value = size.get(key)
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"{catalog_code}/{part_no}: finished_size_mm.{key} must be positive")
        if not isinstance(part.get("quantity"), int) or part.get("quantity", 0) < 1:
            errors.append(f"{catalog_code}/{part_no}: quantity must be a positive integer")
    for key in ("hardware", "assembly_steps", "quality_checks"):
        if not isinstance(product.get(key), list):
            errors.append(f"{catalog_code}: '{key}' must be a list")
    return errors


def load_catalog(selected_code: str | None = None) -> list[tuple[dict[str, Any], str]]:
    catalog = read_json(CATALOG)
    results: list[tuple[dict[str, Any], str]] = []
    seen: set[str] = set()
    for entry in catalog.get("products", []):
        code = entry.get("code", "")
        if not CODE_RE.fullmatch(code):
            raise ValueError(f"Invalid product code in catalog: {code!r}")
        if code in seen:
            raise ValueError(f"Duplicate product code in catalog: {code}")
        seen.add(code)
        if selected_code and code != selected_code:
            continue
        product_path = (ROOT / "data" / entry["file"]).resolve()
        if ROOT not in product_path.parents:
            raise ValueError(f"Catalog path escapes repository: {entry['file']}")
        product = read_json(product_path)
        errors = validate_product(product, code)
        if errors:
            raise ValueError("\n".join(errors))
        results.append((product, entry.get("status", "unspecified")))
    if selected_code and not results:
        raise ValueError(f"No product with code {selected_code!r} in catalog")
    if not results:
        raise ValueError("Catalog contains no products")
    return results


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def bom_rows(product: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for part in product["components"]:
        size = part["finished_size_mm"]
        rows.append([product["product_code"], product["revision"], part["part_no"], part["name"], part["material_code"], size["thickness"], part["quantity"], "panel/part", ""])
    for item in product["hardware"]:
        rows.append([product["product_code"], product["revision"], item["code"], item["description"], "", "", item["quantity"], item.get("unit", "ea"), item.get("supplier", "TBD")])
    return rows


def cutlist_rows(product: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for part in product["components"]:
        size = part["finished_size_mm"]
        rows.append([product["product_code"], product["revision"], part["part_no"], part["name"], part["material_code"], size["width"], size["height"], size["thickness"], part["quantity"], part.get("grain_direction", "unspecified"), "; ".join(part.get("edge_banding", [])), "Finished dimensions; saw allowance/nesting not calculated"])
    return rows


def operation_rows(product: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for part in product["components"]:
        for index, operation in enumerate(part.get("operations", []), start=1):
            rows.append([part["part_no"], part["name"], index, operation.get("op", "TBD"), operation.get("datum", "TBD"), operation.get("details", "")])
    return rows


def assembly_rows(product: dict[str, Any]) -> list[list[Any]]:
    return [[step.get("step", ""), step.get("task", "")] for step in sorted(product["assembly_steps"], key=lambda item: item.get("step", 0))]


def qc_rows(product: dict[str, Any]) -> list[list[Any]]:
    return [[item.get("check", ""), item.get("method", ""), item.get("acceptance", "")] for item in product["quality_checks"]]


def product_markdown(product: dict[str, Any], status: str) -> str:
    dims = product["overall_dimensions_mm"]
    lines = [f"# {product['product_name']}", "", f"**Code:** {product['product_code']}  |  **Revision:** {product['revision']}  |  **Status:** {status}", "", "> Example data only. Do not release for production until all open specifications and controlled drawings are approved.", "", "## Product envelope", "", f"{dims['width']} W × {dims['depth']} D × {dims['height']} H mm; units: {product.get('units', 'mm')}.", "", "## Materials and finish", "", "| Code | Description | Thickness | Specification |", "|---|---|---:|---|"]
    for material in product.get("materials", []):
        lines.append(f"| {material['code']} | {material['name']} | {material.get('thickness_mm') if material.get('thickness_mm') is not None else 'varies'} | {material.get('standard', '')} |")
    finish = product.get("finish", {})
    lines.extend(["", "## Finish", ""])
    lines.extend(f"- **{key.replace('_', ' ').title()}:** {value}" for key, value in finish.items())
    lines.extend(["", "## Components", "", "See `cut-list.csv` for quantities and finished sizes, and `operations.csv` for the supplied operation notes.", "", "| Part | Description | Material | Qty | Finished W × H × T (mm) |", "|---|---|---|---:|---|"])
    for part in product["components"]:
        size = part["finished_size_mm"]
        lines.append(f"| {part['part_no']} | {part['name']} | {part['material_code']} | {part['quantity']} | {size['width']} × {size['height']} × {size['thickness']} |")
    lines.extend(["", "## Hardware", "", "| Code | Description | Qty | Unit | Supplier |", "|---|---|---:|---|---|"])
    for item in product["hardware"]:
        lines.append(f"| {item['code']} | {item['description']} | {item['quantity']} | {item.get('unit', 'ea')} | {item.get('supplier', 'TBD')} |")
    lines.extend(["", "## Assembly", "", "See `assembly.csv` for the ordered assembly sequence.", "", "## Inspection", "", "See `qc-plan.csv`; acceptance criteria remain subject to approved drawings, samples, engineering, and customer/market requirements.", "", "## Packaging", "", f"- Pack type: {product['packaging'].get('pack_type', 'TBD')}", f"- Cartons per unit: {product['packaging'].get('cartons_per_unit', 'TBD')}"])
    carton = product["packaging"].get("carton_internal_dimensions_mm")
    if carton:
        lines.append(f"- Carton internal dimensions (W × D × H): {carton['width']} × {carton['depth']} × {carton['height']} mm")
    for key in ("estimated_net_weight_kg", "estimated_gross_weight_kg"):
        if product["packaging"].get(key) is not None:
            lines.append(f"- {key.replace('_', ' ').title()}: {product['packaging'][key]} kg")
    lines.extend(["", f"- Protection: {product['packaging'].get('protection', 'TBD')}", "", "## Release documents / open items", ""])
    lines.extend(f"- [ ] {item}" for item in product.get("release_documents", []))
    lines.extend(["", "## Revision and approval", "", "| Role | Name | Date | Approval/reference |", "|---|---|---|---|", "| Design | | | |", "| Engineering | | | |", "| Quality | | | |", "| Customer | | | |", "", "**Release status:** NOT APPROVED FOR PRODUCTION (example record).", ""])
    return "\n".join(lines)


def drawing_svg(product: dict[str, Any]) -> str:
    """Create clearly marked overall-envelope elevations, not detailed part geometry."""
    code = html.escape(product["product_code"])
    name = html.escape(product["product_name"])
    rev = html.escape(product["revision"])
    d = product["overall_dimensions_mm"]
    width, depth, height = (float(d[k]) for k in ("width", "depth", "height"))
    svg_w, svg_h = 1200, 850
    panels = [(70, 150, 500, 500, width, height, "FRONT ELEVATION", f"W {width:g} × H {height:g} mm"), (650, 150, 220, 500, depth, height, "SIDE ELEVATION", f"D {depth:g} × H {height:g} mm"), (930, 300, 220, 150, width, depth, "TOP ENVELOPE", f"W {width:g} × D {depth:g} mm")]
    shapes = []
    for x, y, box_w, box_h, real_w, real_h, label, dimension in panels:
        scale = min((box_w - 50) / real_w, (box_h - 50) / real_h)
        rw, rh = real_w * scale, real_h * scale
        rx, ry = x + (box_w - rw) / 2, y + (box_h - rh) / 2
        shapes.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#f7f8fa" stroke="#172b4d" stroke-width="2"/>')
        shapes.append(f'<text x="{x + box_w/2:.1f}" y="{y + box_h + 28}" text-anchor="middle" class="label">{label}</text>')
        shapes.append(f'<text x="{x + box_w/2:.1f}" y="{y + box_h + 50}" text-anchor="middle" class="dim">{dimension}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
  <style>text{{font-family:Arial,sans-serif;fill:#172b4d}}.title{{font-size:27px;font-weight:bold}}.label{{font-size:15px;font-weight:bold}}.dim{{font-size:13px}}.note{{font-size:13px;fill:#9b1c1c}}.small{{font-size:12px}}</style>
  <rect width="100%" height="100%" fill="white"/><text x="55" y="55" class="title">{name} — OVERALL ENVELOPE</text>
  <text x="55" y="85" class="small">Product {code} | Revision {rev} | Units: mm | Status: EXAMPLE / NOT RELEASED</text>
  {''.join(shapes)}
  <rect x="55" y="690" width="1090" height="105" fill="#fff7e6" stroke="#b7791f"/>
  <text x="75" y="720" class="note">REFERENCE SHEET ONLY — NOT A PRODUCTION, MACHINING, OR CAD/CAM DRAWING.</text>
  <text x="75" y="745" class="small">Only the overall envelope is represented. Part geometry, joints, datums, hole coordinates, sections, and tolerances require controlled approved drawings.</text>
  <text x="75" y="770" class="small">Generated from product JSON. Verify all data and obtain design/engineering/customer approval before manufacture.</text>
</svg>'''


def generate(product: dict[str, Any], status: str) -> Path:
    folder = OUT_DIR / product["product_code"]
    folder.mkdir(parents=True, exist_ok=True)
    write_csv(folder / "bom.csv", ["product_code", "revision", "item_code", "description", "material_code", "thickness_mm", "quantity", "item_type", "supplier"], bom_rows(product))
    write_csv(folder / "cut-list.csv", ["product_code", "revision", "part_no", "part_name", "material_code", "finished_width_mm", "finished_height_mm", "thickness_mm", "quantity", "grain_direction", "edge_banding", "notes"], cutlist_rows(product))
    write_csv(folder / "operations.csv", ["part_no", "part_name", "sequence", "operation", "datum", "details"], operation_rows(product))
    write_csv(folder / "assembly.csv", ["step", "task"], assembly_rows(product))
    write_csv(folder / "qc-plan.csv", ["check", "method", "acceptance"], qc_rows(product))
    (folder / "product-pack.md").write_text(product_markdown(product, status), encoding="utf-8")
    (folder / "drawing.svg").write_text(drawing_svg(product), encoding="utf-8")
    return folder


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", help="Generate only this product code")
    args = parser.parse_args()
    try:
        products = load_catalog(args.product)
        for product, status in products:
            print(f"Generated {product['product_code']} -> {generate(product, status).relative_to(ROOT)}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

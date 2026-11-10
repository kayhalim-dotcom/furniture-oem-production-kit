import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "generated"
OUT_DIR.mkdir(exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_markdown(product, materials, hardware):
    lines = []
    lines.append(f"# {product['product_name']}")
    lines.append("")
    lines.append("## Product Information")
    lines.append("")
    lines.append(f"- Product code: {product['product_code']}")
    lines.append(f"- Category: {product['category']}")
    lines.append(f"- Revision: {product['revision']}")
    lines.append(f"- Target market: {product['target_market']}")
    lines.append("")
    lines.append("## Overall Dimensions")
    lines.append("")
    for key, value in product["overall_dimensions_mm"].items():
        lines.append(f"- {key.title()}: {value} mm")
    lines.append("")
    lines.append("## Materials")
    lines.append("")
    lines.append("| Component | Material | Thickness | Quantity |")
    lines.append("|-----------|----------|-----------|----------|")
    for item in product["materials"]:
        lines.append(f"| {item['component']} | {item['material_code']} | {item['thickness_mm']} mm | {item['quantity']} |")
    lines.append("")
    lines.append("## Hardware")
    lines.append("")
    lines.append("| Component | Code | Quantity |")
    lines.append("|-----------|------|----------|")
    for item in product["hardware"]:
        lines.append(f"| {item['component']} | {item['hardware_code']} | {item['quantity']} |")
    lines.append("")
    lines.append("## Finish")
    lines.append("")
    for key, value in product["finish"].items():
        lines.append(f"- {key.title()}: {value}")
    lines.append("")
    lines.append("## Assembly Notes")
    lines.append("")
    for note in product["assembly_notes"]:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## Quality Checks")
    lines.append("")
    for check in product["quality_checks"]:
        lines.append(f"- {check}")
    lines.append("")
    lines.append("## Packaging")
    lines.append("")
    pack = product["packaging"]
    lines.append(f"- Method: {pack['method']}")
    lines.append(f"- Carton size: {pack['carton_size_mm']['width']} x {pack['carton_size_mm']['depth']} x {pack['carton_size_mm']['height']} mm")
    lines.append(f"- Weight: {pack['weight_kg']} kg")
    lines.append("- Labels: " + ", ".join(pack["labels"]))
    return "\n".join(lines) + "\n"


def main():
    materials = load_json(DATA_DIR / "materials.json")
    hardware = load_json(DATA_DIR / "materials.json")
    product = load_json(DATA_DIR / "sample-product.json")

    generated = build_markdown(product, materials, hardware)
    (OUT_DIR / "product-spec.md").write_text(generated, encoding="utf-8")
    (OUT_DIR / "manufacturer-ready-summary.txt").write_text(
        f"{product['product_name']} ({product['product_code']})\n"
        f"Dimensions: {product['overall_dimensions_mm']['width']} x {product['overall_dimensions_mm']['depth']} x {product['overall_dimensions_mm']['height']} mm\n"
        f"Materials: {len(product['materials'])} item references\n"
        f"Hardware: {len(product['hardware'])} item references\n",
        encoding="utf-8",
    )
    print("Generated product documentation in generated/")


if __name__ == "__main__":
    main()

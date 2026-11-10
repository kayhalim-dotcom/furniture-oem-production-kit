# Furniture OEM Production Kit

A data-driven starter system for organizing OEM furniture product definitions and generating a consistent manufacturing document pack. It includes a small example catalog, structured product specifications, drawing-sheet generation, BOM/cut-list exports, operation and assembly schedules, and release-control guidance.

> **Important:** Generated drawings are dimensioned product-level reference sheets, not validated CAD/CAM, structural engineering, or compliance documents. Confirm every dimension, joint, load, material, tolerance, safety requirement, and applicable market standard with the responsible designer, engineer, customer, and factory before production.

## Included capabilities

- Three example products: a storage cabinet, writing desk, and dining chair.
- JSON product records with revision, finished dimensions, components, materials, edge treatment, machining notes, hardware, assembly, inspection, and packaging fields.
- Python standard-library generator that creates an individual product release pack: SVG drawing sheet, product specification, BOM, cut list, machining-operation schedule, assembly sequence, and QC plan.
- CSV templates, a release checklist, schema guidance, and a sample factory handoff process.

## Quick start

Requires Python 3.9+; no third-party packages are needed.

```bash
python3 scripts/generate_furniture_docs.py
python3 -m unittest discover -s tests -v
```

Generated files are written to `generated/<product-code>/`. Use `--product CODE` to generate one catalog item, for example:

```bash
python3 scripts/generate_furniture_docs.py --product DESK-01
```

The generator validates catalog paths and essential production fields. It does not certify design safety, calculate structural capacity, optimize nesting, or create machine-ready toolpaths.

## Catalog and product data

- `data/catalog.json` is the source of truth for active catalog entries.
- `data/products/*.json` contains one version-controlled product record per item.
- `data/materials.json` and `data/hardware.json` hold shared reference data; product records should identify the actual supplier/grade/finish approved for each order.
- `docs/product-data-schema.md` documents the current data contract and conventions.

Start a new SKU by copying `templates/product-template.json`, assigning a unique product code and revision, filling every required value, adding it to the catalog, and running the generator and tests. Do not copy sample dimensions or tolerances into a real product without engineering approval.

## Repository map

```text
 data/       Shared references, catalog, and product records
 docs/       Data schema, release workflow, and manufacturing guidance
 generated/  Example/generated release packs (rebuild with the script)
 scripts/    Standard-library document generator
 templates/  Product, BOM, cut-list, and release-check templates
 tests/      Generator and data validation tests
```

## Production release workflow

1. Capture the customer brief, market, intended use, and approval owner.
2. Define product geometry, datums, joints, materials, finishes, hardware, and tolerances.
3. Review the generated views, BOM, cut list, machining and assembly operations with design and factory teams.
4. Add detailed, controlled CAD drawings and approved supplier specifications where required; record their document IDs and revision in the release record.
5. Prototype and verify fit, function, stability, finish, packaging, and any required regulatory or market-specific testing.
6. Close the release checklist, approve the revision, and distribute a read-only release package to suppliers.
7. Record deviations and changes through a new revision; never silently overwrite an approved production definition.

See `docs/release-workflow.md` before using any output for manufacturing.

## License

MIT. Example product data is illustrative and must be validated for the intended application and market.

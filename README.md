# Furniture OEM Production Kit

A complete starter repository for OEM furniture manufacturers to manage production drawings, material data, BOMs, cut lists, packaging specs, and quality control documentation in one place.

## What this repo includes

- Standardized production drawing sheet template
- Material and hardware data reference
- Sample OEM furniture product specification
- BOM and cut-list templates for manufacturing
- Production notes and assembly instructions
- QC checklist for final inspection
- Packaging and dispatch documentation
- Python generator to turn product data into manufacturing docs

## Repository structure

- `data/` — material, hardware, and sample product JSON specifications
- `docs/` — production and manufacturer standards
- `templates/` — CSV, SVG, markdown starter templates
- `scripts/` — generation utilities
- `generated/` — example output docs from sample data

## Quick start

1. Review the sample product data in `data/sample-product.json`.
2. Customize materials and hardware values in `data/materials.json` and `data/hardware.json`.
3. Use the templates in `templates/` as the baseline for production calculations.
4. Run:

```bash
python3 scripts/generate_furniture_docs.py
```

5. Open the generated package in `generated/` for a manufacturer-ready specification.

## Typical workflow for OEM production

1. Product brief and design intent
2. Final dimensions and tolerance definition
3. Material selection and finish specification
4. BOM, cut list, and machining notes
5. Production drawing approval
6. QC and inspection documentation
7. Packaging, dispatch, and customer paperwork

## Sample product model

This repo includes a sample product: `Linen Storage Cabinet`.
It contains:
- dimensions and tolerances
- material set
- component list
- hardware list
- assembly steps
- packaging plan
- QC checks

## Why this repository is useful

It is built to help small and midsize furniture makers and OEM factories reduce confusion by consolidating the information required to produce furniture consistently. Instead of scattered drawings and spreadsheets, teams can work from one clear and structured data package.

## License

MIT

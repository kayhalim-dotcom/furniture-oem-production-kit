# Product data schema and conventions

Catalog records are JSON. The generator currently requires the fields shown in `templates/product-template.json`, with the full examples in `data/products/` as practical references.

## Catalog

`data/catalog.json` contains `schema_version` and `products`. Every catalog entry has a unique uppercase `code`, a path relative to `data/`, and a lifecycle `status` such as `development`, `sample`, `approved`, or `obsolete`. Keep file paths within the repository and keep product code consistent between catalog and record.

## Product record

- `product_code`, `product_name`, `category`, `revision`, `status`, `units`, `market`: product identity and lifecycle. Use controlled revision rules; distinguish development/example data from production-approved data.
- `overall_dimensions_mm`: finished envelope width, depth, and height.
- `tolerances_mm`: explicit tolerance values and scope. Values in samples are illustrative; engineering must assign fit-for-purpose tolerances.
- `materials`: code, description, supplier grade/specification, and nominal thickness (null where not applicable).
- `finish`: approved finish, decor/color reference, and edge treatment.
- `components`: one record per part number, with finished size (width × height × thickness in the part's defined orientation), quantity per sellable unit, grain direction, edge treatment, and operations.
- `operations`: process code, datum, and a clear instruction or a reference to a controlled drawing. Text notes are not a substitute for coordinates, feature sizes, depths, fixtures, or machine programs.
- `hardware`: unique item code, description/model, quantity, unit, supplier, and installation reference.
- `assembly_steps`: ordered, actionable steps with approved joint and process references.
- `quality_checks`: check, method, and measurable approved acceptance criteria.
- `packaging`: pack configuration, internal dimensions, verified weights, protection, and label fields. Unknown weights should remain null, not be guessed.
- `release_documents`: controlled drawing, supplier, test, finish, and packaging references required for release.

## Conventions and safeguards

1. Millimeters are the default. Dimensions are nominal finished dimensions; define machining allowance and panel/edge construction separately.
2. Part number and revision together identify a released definition. Do not reuse a part number for changed geometry without controlled change review.
3. Keep supplier, grade, color/decor, thickness, and hardware model explicit. A generic material family is not a purchase specification.
4. Use named datums and controlled drawings for machining geometry. This starter generator does not calculate hole coordinates or validate joints.
5. Specify measurement method and acceptance value for each QC characteristic before production. “Check quality” is not measurable.
6. Keep unverified values null or explicitly TBD. Never treat illustrative sample values as engineering approval.
7. Relevant product safety, chemical, emissions, fire, durability, and labeling requirements vary by product and destination market; identify and document the applicable requirements with qualified responsible parties.

# OEM release and factory handoff workflow

This repository organizes product information; it does not establish that a design is safe, compliant, structurally adequate, or ready to manufacture. The examples intentionally remain marked as not released.

## Release gates

### Gate 1 — Brief and design inputs

Record customer/SKU, intended use, destination markets, target quantity, packaging and logistics constraints, appearance references, and the accountable design owner. Identify applicable product standards and market requirements with the responsible compliance/engineering team.

### Gate 2 — Engineering definition

Approve product envelope, part geometry, datums, joint sections, hole locations and depths, edge/finish callouts, material grades, hardware models, tolerances, and revision history. Controlled CAD/drawing files should have document IDs and revisions recorded in the product release pack. Confirm the BOM and cut list against the drawings.

### Gate 3 — Supplier and process readiness

Approve supplier specifications and samples for panels/timber, finishes, upholstery, hardware, adhesives, and packaging. Define manufacturing process parameters and inspection methods. Confirm tooling, fixtures, work instructions, traceability, and special-process controls with the factory.

### Gate 4 — Prototype and validation

Build representative prototypes. Verify fit, assembly, function, stability, finish, and packaging. Complete engineering-defined load, durability, safety, and market-specific tests where applicable. Record results, deviations, corrective actions, and approval references. Do not infer test pass from a drawing or template.

### Gate 5 — Production release

Complete `templates/release-checklist.md`; resolve open items; obtain design, engineering, quality, customer, and compliance approvals as applicable. Freeze the release package and distribute the same revision to every supplier. Mark obsolete copies and retain the change history.

### Gate 6 — Change control and production feedback

Request changes with reason, affected SKUs/parts, risk, effective date/lot, and disposition of existing inventory. Review fit, tooling, cost, quality, compliance, and packaging impacts; issue a new revision and update every affected controlled document. Capture production deviations and corrective actions.

## Supplier handoff package

At minimum, issue the approved product specification, dimensioned assembly and part drawings, machining/feature drawings, BOM, cut list, material and finish specifications, hardware supplier data, assembly work instruction, inspection/control plan, packaging specification, label artwork, and revision/change record. Add order-specific quantity, ship-to, approved substitutions, and required certificates/test reports.

## Responsibility and limitations

The product owner and qualified design/engineering team are responsible for correctness and approval. Factories are responsible for confirming process feasibility and reporting discrepancies before production. The generator produces a convenience pack from entered data; it does not replace CAD, engineering review, regulatory advice, supplier approval, or physical validation.

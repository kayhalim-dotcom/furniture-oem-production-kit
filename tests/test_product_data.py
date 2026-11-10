import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_furniture_docs as generator


class ProductDataTests(unittest.TestCase):
    def test_all_catalog_products_validate_and_generate(self):
        products = generator.load_catalog()
        self.assertEqual({p["product_code"] for p, _ in products}, {"LSC-01", "DESK-01", "CHAIR-01"})
        for product, status in products:
            errors = generator.validate_product(product, product["product_code"])
            self.assertEqual(errors, [])
            self.assertIn("OVERALL ENVELOPE", generator.drawing_svg(product))
            self.assertEqual(len(generator.cutlist_rows(product)), len(product["components"]))
            self.assertEqual(len(generator.bom_rows(product)), len(product["components"]) + len(product["hardware"]))

    def test_invalid_component_dimension_is_reported(self):
        product = {
            "product_code": "TEST-01",
            "product_name": "test",
            "revision": "A0",
            "overall_dimensions_mm": {"width": 1, "depth": 1, "height": 1},
            "components": [{"part_no": "P01", "name": "part", "material_code": "M", "finished_size_mm": {"width": -1, "height": 1, "thickness": 1}, "quantity": 1, "operations": []}],
            "hardware": [], "assembly_steps": [], "quality_checks": [], "packaging": {}
        }
        errors = generator.validate_product(product, "TEST-01")
        self.assertTrue(any("finished_size_mm.width" in error for error in errors))

    def test_catalog_product_file_is_valid_json(self):
        catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        for entry in catalog["products"]:
            product_path = ROOT / "data" / entry["file"]
            self.assertTrue(product_path.is_file())
            json.loads(product_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

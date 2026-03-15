import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from brackets import create_app, generate_full_bracket_html, generate_seed_order


class BracketsTests(unittest.TestCase):
    def test_create_app(self):
        app = create_app({"TESTING": True})
        self.assertEqual(app.name, "brackets.app")

    def test_generate_seed_order(self):
        self.assertEqual(generate_seed_order(4), [1, 4, 2, 3])
        self.assertEqual(generate_seed_order(8), [1, 8, 4, 5, 2, 7, 3, 6])
        self.assertEqual(
            generate_seed_order(16),
            [1, 16, 8, 9, 4, 13, 5, 12, 2, 15, 7, 10, 3, 14, 6, 11],
        )

    def test_generate_full_bracket_html(self):
        people = [{"Seed": i, "Name": f"Person {i}"} for i in range(1, 65)]
        regions = [
            {
                "Name": "Region 1",
                "Sites": ["Site 1", "Site 2", "Site 3", "Site 4"],
                "Final": "Final 1",
            }
        ]
        html = generate_full_bracket_html(people, regions)
        self.assertIn('<div class="bracket-left">', html)
        self.assertIn("Region 1", html)
        self.assertIn("Final 1", html)
        self.assertIn("Person 1", html)
        self.assertIn("Person 64", html)


if __name__ == "__main__":
    unittest.main()


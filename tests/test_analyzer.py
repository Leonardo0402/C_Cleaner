import unittest

from core import analyzer


class AnalyzerTests(unittest.TestCase):
    def test_generate_insights_applies_thresholds(self) -> None:
        flat = {
            r"C:\\Users\\User\\Downloads": 6 * 1024 ** 3,
            r"C:\\Windows\\SoftwareDistribution": 2 * 1024 ** 3,
            r"C:\\Temp": 800 * 1024 ** 2,
        }
        insights = analyzer.generate_insights(flat)
        paths = {item["path"] for item in insights}
        self.assertIn(r"C:\\Users\\User\\Downloads", paths)
        self.assertNotIn(r"C:\\Windows\\SoftwareDistribution", paths)
        self.assertNotIn(r"C:\\Temp", paths)

    def test_generate_insights_returns_suggestions(self) -> None:
        flat = {r"C:\\Windows\\SoftwareDistribution": 5 * 1024 ** 3}
        insights = analyzer.generate_insights(flat)
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0]["suggestion"], "清理")
        self.assertTrue(insights[0]["size"].endswith("GB"))


if __name__ == "__main__":
    unittest.main()

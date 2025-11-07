import os
import tempfile
import unittest
from pathlib import Path

from core import scanner


class ScannerTests(unittest.TestCase):
    def test_scan_drive_default_root_exists(self) -> None:
        data = scanner.scan_drive(depth=0)
        expected_root = Path("C:/") if os.name == "nt" else Path(os.sep)
        self.assertEqual(Path(data["root"]["path"]), expected_root)
        self.assertIn("total", data)
        self.assertGreater(data["total"], 0)

    def test_scan_directory_counts_nested_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "file1.bin").write_bytes(b"a" * 1024)
            sub = tmp_path / "sub"
            sub.mkdir()
            (sub / "file2.bin").write_bytes(b"b" * 2048)

            stat = scanner.scan_directory(tmp_path, depth=2)
            self.assertEqual(stat.size, 1024 + 2048)
            self.assertEqual(len(stat.children), 1)
            self.assertEqual(stat.children[0].path, sub)
            self.assertEqual(stat.children[0].size, 2048)


if __name__ == "__main__":
    unittest.main()

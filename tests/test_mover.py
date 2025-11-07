import tempfile
import unittest
from pathlib import Path

from core import mover


class MoverTests(unittest.TestCase):
    def test_migrate_directory_dry_run_returns_destination(self) -> None:
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dst_dir:
            src_path = Path(src_dir)
            dst_root = Path(dst_dir)
            (src_path / "file.txt").write_text("content")

            projected = mover.migrate_directory(src_path, dst_root, dry_run=True)
            self.assertEqual(projected, (dst_root / src_path.name).resolve())
            self.assertTrue(src_path.exists())

    def test_migrate_directory_moves_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_root:
            root = Path(tmp_root)
            src = root / "source"
            dst_root = root / "dest"
            src.mkdir()
            dst_root.mkdir()
            payload = src / "payload.txt"
            payload.write_text("hello")

            result = mover.migrate_directory(src, dst_root, dry_run=False)
            self.assertEqual(result, (dst_root / "source").resolve())
            self.assertFalse(src.exists())
            self.assertTrue((dst_root / "source" / "payload.txt").exists())


if __name__ == "__main__":
    unittest.main()

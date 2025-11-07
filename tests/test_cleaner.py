import tempfile
import unittest
from pathlib import Path

from core import cleaner


class CleanerTests(unittest.TestCase):
    def test_clean_directory_dry_run_and_execute(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            nested = tmp_path / "nested"
            nested.mkdir()
            file_one = nested / "one.bin"
            file_two = tmp_path / "two.bin"
            file_one.write_bytes(b"a" * 128)
            file_two.write_bytes(b"b" * 256)

            dry_removed = cleaner.clean_directory(tmp_path, dry_run=True)
            self.assertEqual(dry_removed, 128 + 256)
            self.assertTrue(file_one.exists())
            self.assertTrue(file_two.exists())

            removed = cleaner.clean_directory(tmp_path, dry_run=False)
            self.assertEqual(removed, 128 + 256)
            self.assertFalse(file_one.exists())
            self.assertFalse(file_two.exists())

    def test_summarize_targets_with_custom_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "data.bin").write_bytes(b"x" * 64)
            summary = cleaner.summarize_targets({"Custom": tmp_path})
            self.assertEqual(summary["Custom"], 64)

    def test_clean_target_with_injected_directory(self) -> None:
        original_targets = dict(cleaner.CLEAN_TARGETS)
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                (tmp_path / "payload.dat").write_bytes(b"z" * 32)
                cleaner.CLEAN_TARGETS["Injected"] = tmp_path
                removed = cleaner.clean_target("Injected", dry_run=True)
                self.assertEqual(removed, 32)
        finally:
            cleaner.CLEAN_TARGETS = original_targets


if __name__ == "__main__":
    unittest.main()

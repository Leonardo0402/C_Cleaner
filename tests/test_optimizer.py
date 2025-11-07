import unittest

from core import optimizer


class OptimizerTests(unittest.TestCase):
    def test_run_command_dry_run(self) -> None:
        for name in optimizer.list_commands():
            self.assertEqual(optimizer.run_command(name, dry_run=True), 0)


if __name__ == "__main__":
    unittest.main()

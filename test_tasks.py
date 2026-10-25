"""Run with python3 -m unittest -v. Tests use temporary task databases."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('tasks.py')


class TaskTrackerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.database = Path(self.directory.name) / 'tasks.json'

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), '--file', str(self.database), *arguments],
            text=True, capture_output=True,
        )

    def test_tasks_persist_across_processes(self):
        for title in ['Write documentation', 'Test Unicode: café']:
            self.assertEqual(self.run_cli('add', title).returncode, 0)
        self.assertEqual(self.run_cli('done', '1').returncode, 0)
        listing = self.run_cli('list')
        self.assertEqual(listing.returncode, 0)
        self.assertIn('1: [x] Write documentation', listing.stdout)
        self.assertIn('2: [ ] Test Unicode: café', listing.stdout)
        self.assertEqual(len(json.loads(self.database.read_text())), 2)

    def test_invalid_commands_preserve_existing_data(self):
        self.assertEqual(self.run_cli('add', 'Keep this task').returncode, 0)
        original = self.database.read_bytes()
        for arguments in [('add', '   '), ('done', '999'), ('done', 'invalid')]:
            with self.subTest(arguments=arguments):
                result = self.run_cli(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.database.read_bytes(), original)

    def test_corrupt_database_is_not_overwritten(self):
        for content in ['{broken', '{}', '[{"id": 1}]']:
            with self.subTest(content=content):
                self.database.write_text(content)
                result = self.run_cli('add', 'New task')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Error:', result.stderr)
                self.assertEqual(self.database.read_text(), content)

    def test_listing_empty_database_does_not_create_file(self):
        self.assertEqual(self.run_cli('list').returncode, 0)
        self.assertFalse(self.database.exists())


if __name__ == '__main__':
    unittest.main()

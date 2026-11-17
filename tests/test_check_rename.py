import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/grasp/scripts/check_rename.py"


class CheckRenameTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q", "--initial-branch=main")
        self.git("config", "user.name", "Rename Test")
        self.git("config", "user.email", "rename-test@example.invalid")
        self.write("src/a.js", "function get() { return Old; }\n")
        self.write("other.js", "const value = 1;\n")
        self.base = self.save("base")

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *args], cwd=self.root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def save(self, message):
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def run_check(self, head="HEAD", paths=(".",), base=None, old="Old", new="New"):
        return subprocess.run(
            [sys.executable, str(SCRIPT), f"{base or self.base}...{head}", old, new, "--", *paths],
            cwd=self.root, capture_output=True, text=True,
        )

    def assert_pass(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS:", result.stdout)

    def assert_fail(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("FAIL:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_true_rename(self):
        self.write("src/a.js", "function get() { return New; }\n")
        self.save("rename")
        self.assert_pass(self.run_check())

    def test_unpaired_identifier_deletion(self):
        self.write("src/a.js", "function get() { return; }\n")
        self.save("delete identifier")
        self.assert_fail(self.run_check())

    def test_reordering_is_rejected(self):
        self.write("src/a.js", "const a = Old;\nconst b = 2;\n")
        self.base = self.save("two statements")
        self.write("src/a.js", "const b = 2;\nconst a = New;\n")
        self.save("rename and reorder")
        self.assert_fail(self.run_check())

    def test_addition_deletion_and_move_are_rejected(self):
        for change in ("add", "delete", "move"):
            with self.subTest(change=change):
                self.git("reset", "--hard", self.base)
                self.write("src/a.js", "function get() { return New; }\n")
                if change == "add":
                    self.write("added.js", "const value = New;\n")
                elif change == "delete":
                    (self.root / "other.js").unlink()
                else:
                    (self.root / "other.js").rename(self.root / "moved.js")
                self.save(change)
                self.assert_fail(self.run_check())

    def test_mode_change_is_rejected(self):
        self.write("src/a.js", "function get() { return New; }\n")
        os.chmod(self.root / "src/a.js", 0o755)
        self.save("rename and mode")
        self.assert_fail(self.run_check())

    def test_file_type_change_is_rejected(self):
        target = self.root / "src/a.js"
        target.unlink()
        target.symlink_to("../other.js")
        self.save("replace source with symlink")
        self.assert_fail(self.run_check())

    def test_path_scope(self):
        self.write("src/a.js", "function get() { return New; }\n")
        self.write("other.js", "const value = 2;\n")
        self.save("rename and unrelated change")
        self.assert_pass(self.run_check(paths=("src",)))
        self.assert_fail(self.run_check())

    def test_git_failure(self):
        self.assert_fail(self.run_check(head="does-not-exist"))

    def test_no_changes_are_rejected(self):
        self.assert_fail(self.run_check(head=self.base))

    def test_three_dot_uses_merge_base(self):
        self.git("checkout", "-qb", "feature")
        self.write("src/a.js", "function get() { return New; }\n")
        self.save("feature rename")
        self.git("checkout", "-q", "main")
        self.write("other.js", "const value = 2;\n")
        self.save("main advanced")
        self.assert_pass(self.run_check(head="feature", base="main"))

    def test_whitespace_change_is_rejected(self):
        self.write("src/a.js", "function get() {  return New; }\n")
        self.save("rename and whitespace")
        self.assert_fail(self.run_check())

    def test_identifier_boundaries_include_unicode_and_dollar(self):
        self.write("src/a.js", "Old; $Old; Old$; éOld; Oldé; Old_x;\n")
        self.base = self.save("identifier boundaries")
        self.write("src/a.js", "New; $Old; Old$; éOld; Oldé; Old_x;\n")
        self.save("standalone rename")
        self.assert_pass(self.run_check())

    def test_dollar_identifier(self):
        self.write("src/a.js", "const $old = value; use($old);\n")
        self.base = self.save("dollar identifier")
        self.write("src/a.js", "const $new = value; use($new);\n")
        self.save("rename dollar identifier")
        self.assert_pass(self.run_check(old="$old", new="$new"))

    def test_invalid_identifier_and_range(self):
        self.assert_fail(self.run_check(old="not-an-identifier"))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "HEAD..HEAD", "Old", "New", "--", "."],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assert_fail(result)

    def test_missing_path_is_rejected(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "HEAD...HEAD", "Old", "New", "--"],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assert_fail(result)

    def test_non_utf8_and_binary_content_are_rejected(self):
        for data in (b"Old\xff\n", b"Old\x00\n"):
            with self.subTest(data=data):
                self.git("reset", "--hard", self.base)
                (self.root / "src/a.js").write_bytes(data)
                self.save("non-text source")
                self.assert_fail(self.run_check())


if __name__ == "__main__":
    unittest.main()

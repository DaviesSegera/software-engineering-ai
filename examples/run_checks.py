"""Local quality gate. A failing compile or test yields a nonzero status."""
from pathlib import Path
import sys
import unittest


def main():
    directory = Path(__file__).resolve().parent
    for path in sorted(directory.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print("All example Python files compile.", flush=True)
    suite = unittest.defaultTestLoader.discover(str(directory), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())

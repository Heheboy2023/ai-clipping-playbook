"""Create an isolated, deliberately broken clock-parser exercise once."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "work/clock-repair"


def prepare(target: Path = TARGET) -> Path:
    if target.exists():
        raise ValueError("Practice folder exists. Keep it; choose a new folder for another attempt.")
    source = (HERE / "clip_plan.py").read_text()
    start = source.index("def seconds(")
    end = source.index("\n\ndef decimal_text", start)
    broken = ('def seconds(value: str) -> Decimal:\n'
              '    """Exercise bug: accepts decimal text but not clock notation."""\n'
              '    return Decimal(value.strip())\n')
    target.mkdir(parents=True)
    (target / "clip_plan.py").write_text(source[:start] + broken + source[end:])
    shutil.copy2(HERE / "repair_checks.py", target / "test_clock.py")
    (target / "README.md").write_text(
        "# Clock-input repair exercise\n\n"
        "This copy intentionally contains a broken seconds() function.\n"
        "Run: python -m pytest work/clock-repair/test_clock.py -q\n\n"
        "Fix implementation behavior, not expected test answers.\n"
        "The tested answer remains in examples/agent-clip-plan/clip_plan.py.\n"
    )
    return target


if __name__ == "__main__":
    print(prepare())

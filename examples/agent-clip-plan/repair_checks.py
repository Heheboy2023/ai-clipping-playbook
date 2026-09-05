"""Copied beside the exercise module as test_clock.py; not an installed test."""
from decimal import Decimal
import importlib.util
from pathlib import Path
import pytest

SPEC = importlib.util.spec_from_file_location("clock_exercise", Path(__file__).with_name("clip_plan.py"))
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)


@pytest.mark.parametrize("text,expected", [
    ("2.5", "2.5"), ("00:00:02.500", "2.5"),
    ("00:01:02.250", "62.25"), ("01:00:00", "3600"),
])
def test_valid_time(text, expected):
    assert planner.seconds(text) == Decimal(expected)


@pytest.mark.parametrize("text", ["-1", "NaN", "Infinity", "00:60:00", "00:00:60", "00:00:01:15"])
def test_reject_bad_time(text):
    with pytest.raises(ValueError):
        planner.seconds(text)

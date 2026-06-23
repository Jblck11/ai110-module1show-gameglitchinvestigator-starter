"""Tests for the guessing-game logic in logic_utils.py.

Run with:  pytest test/test_game_logic.py
"""

import os
import sys

import pytest

# Allow importing logic_utils.py from the project root when running pytest
# from inside the test/ directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic_utils import (  # noqa: E402
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "difficulty, expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 50)),
        ("Unknown", (1, 100)),  # defaults to Normal range
    ],
)
def test_get_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_float_string_truncates():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_check_guess_win():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_check_guess_too_high():
    outcome, _ = check_guess(75, 50)
    assert outcome == "Too High"


def test_check_guess_too_low():
    outcome, _ = check_guess(25, 50)
    assert outcome == "Too Low"


def test_check_guess_low_value_is_too_low_not_too_high():
    # Regression test for the original "guess 1 -> Go LOWER" glitch.
    # A guess of 1 against a secret of 50 must be "Too Low".
    outcome, _ = check_guess(1, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_update_score_win_awards_points():
    assert update_score(0, "Win", attempt_number=1) > 0


def test_update_score_win_has_minimum_floor():
    # Many attempts should never drop a win below the 10-point floor.
    assert update_score(0, "Win", attempt_number=20) == 10


def test_update_score_wrong_guess_loses_points():
    assert update_score(50, "Too Low", attempt_number=3) == 45
    assert update_score(50, "Too High", attempt_number=3) == 45


def test_update_score_unknown_outcome_unchanged():
    assert update_score(50, "Whatever", attempt_number=3) == 50

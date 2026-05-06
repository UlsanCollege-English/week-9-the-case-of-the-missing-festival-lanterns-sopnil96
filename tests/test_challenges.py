"""Tests for Week 9: The Case of the Missing Festival Lanterns."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from challenges import analyze_lanterns


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

EXPECTED = {
    "river-dragon",
    "blue-crane",
    "moon-rabbit",
    "gold-tiger",
    "white-lotus",
    "red-kite",
}

CORRECT = {
    "river-dragon": "North Gate",
    "blue-crane": "River Walk",
    "moon-rabbit": "River Walk",
    "gold-tiger": "Market Street",
    "white-lotus": "Temple Road",
    "red-kite": "Temple Road",
}


# ---------------------------------------------------------------------------
# Starter tests (provided)
# ---------------------------------------------------------------------------

def test_seen_lanterns():
    log = [
        ("river-dragon", "North Gate"),
        ("blue-crane", "River Walk"),
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert report["seen_lanterns"] == {"river-dragon", "blue-crane"}


def test_missing_lanterns():
    log = [
        ("river-dragon", "North Gate"),
        ("blue-crane", "River Walk"),
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert "moon-rabbit" in report["missing_lanterns"]
    assert "gold-tiger" in report["missing_lanterns"]
    assert "white-lotus" in report["missing_lanterns"]
    assert "red-kite" in report["missing_lanterns"]


def test_unexpected_lanterns():
    log = [
        ("river-dragon", "North Gate"),
        ("silver-fox", "Market Street"),   # not in EXPECTED
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert "silver-fox" in report["unexpected_lanterns"]
    assert "river-dragon" not in report["unexpected_lanterns"]


def test_duplicate_lanterns():
    log = [
        ("river-dragon", "North Gate"),
        ("river-dragon", "North Gate"),   # duplicate
        ("blue-crane", "River Walk"),
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert "river-dragon" in report["duplicate_lanterns"]
    assert "blue-crane" not in report["duplicate_lanterns"]


def test_count_by_section():
    log = [
        ("river-dragon", "North Gate"),
        ("blue-crane", "River Walk"),
        ("moon-rabbit", "River Walk"),
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert report["count_by_section"]["North Gate"] == 1
    assert report["count_by_section"]["River Walk"] == 2


def test_wrong_section_lanterns():
    log = [
        ("red-kite", "South Bridge"),   # correct is "Temple Road"
        ("blue-crane", "River Walk"),   # correct section — should NOT appear
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert "red-kite" in report["wrong_section_lanterns"]
    assert report["wrong_section_lanterns"]["red-kite"]["expected"] == "Temple Road"
    assert report["wrong_section_lanterns"]["red-kite"]["actual"] == "South Bridge"
    assert "blue-crane" not in report["wrong_section_lanterns"]


def test_unexpected_lanterns_not_in_wrong_section():
    """Unexpected lanterns must never appear in wrong_section_lanterns."""
    log = [
        ("silver-fox", "Market Street"),  # unexpected — not in EXPECTED
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert "silver-fox" not in report["wrong_section_lanterns"]


def test_first_wrong_section_recorded():
    """When an expected lantern appears in two wrong sections, only the first is kept."""
    log = [
        ("red-kite", "South Bridge"),   # first wrong section
        ("red-kite", "North Gate"),     # second wrong section — should be ignored
    ]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert report["wrong_section_lanterns"]["red-kite"]["actual"] == "South Bridge"


# ---------------------------------------------------------------------------
# Empty-input edge cases
# ---------------------------------------------------------------------------

def test_empty_log():
    report = analyze_lanterns(EXPECTED, [], CORRECT)
    assert report["seen_lanterns"] == set()
    assert report["missing_lanterns"] == EXPECTED
    assert report["unexpected_lanterns"] == set()
    assert report["duplicate_lanterns"] == set()
    assert report["count_by_section"] == {}
    assert report["wrong_section_lanterns"] == {}


def test_empty_expected():
    log = [("river-dragon", "North Gate")]
    report = analyze_lanterns(set(), log, CORRECT)
    assert report["missing_lanterns"] == set()
    assert "river-dragon" in report["unexpected_lanterns"]


def test_no_missing_lanterns():
    log = [(name, CORRECT[name]) for name in EXPECTED]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert report["missing_lanterns"] == set()


def test_no_unexpected_lanterns():
    log = [(name, CORRECT[name]) for name in EXPECTED]
    report = analyze_lanterns(EXPECTED, log, CORRECT)
    assert report["unexpected_lanterns"] == set()


# ---------------------------------------------------------------------------
# Custom test (student-added)
# ---------------------------------------------------------------------------

def test_all_lanterns_in_wrong_sections():
    """
    Test name: test_all_lanterns_in_wrong_sections
    What it checks:
        Every expected lantern appears, but every single one is in the wrong
        section. Verifies that wrong_section_lanterns captures all of them,
        missing_lanterns is empty, and unexpected_lanterns is also empty.
    Why it matters:
        This stress-tests the wrong-section logic across the full set of
        expected lanterns at once, confirming there are no off-by-one errors
        or early exits that would cause some lanterns to be skipped.
    """
    # Swap every lantern into a section that is NOT its correct one
    wrong_log = [
        ("river-dragon", "Temple Road"),    # correct: North Gate
        ("blue-crane", "North Gate"),       # correct: River Walk
        ("moon-rabbit", "Market Street"),   # correct: River Walk
        ("gold-tiger", "River Walk"),       # correct: Market Street
        ("white-lotus", "South Bridge"),    # correct: Temple Road
        ("red-kite", "North Gate"),         # correct: Temple Road
    ]
    report = analyze_lanterns(EXPECTED, wrong_log, CORRECT)

    # All lanterns were seen — none missing, none unexpected
    assert report["missing_lanterns"] == set()
    assert report["unexpected_lanterns"] == set()

    # Every expected lantern should be flagged as in the wrong section
    for name in EXPECTED:
        assert name in report["wrong_section_lanterns"], (
            f"{name} should be in wrong_section_lanterns"
        )
        assert report["wrong_section_lanterns"][name]["expected"] == CORRECT[name]
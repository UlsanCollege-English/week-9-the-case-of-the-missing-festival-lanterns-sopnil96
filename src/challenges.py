"""Week 9 Homework: The Case of the Missing Festival Lanterns.

Read HOMEWORK_BRIEF.md for the full assignment instructions.

Run tests with:
    pytest -q

Do not solve this by only printing output.
The function must return a report dictionary.
"""

EXPECTED_LANTERNS = {
    "river-dragon",
    "blue-crane",
    "moon-rabbit",
    "gold-tiger",
    "white-lotus",
    "red-kite",
}

LANTERN_LOG = [
    ("river-dragon", "North Gate"),
    ("blue-crane", "River Walk"),
    ("moon-rabbit", "River Walk"),
    ("river-dragon", "North Gate"),
    ("gold-tiger", "Market Street"),
    ("silver-fox", "Market Street"),
    ("red-kite", "South Bridge"),
]

CORRECT_SECTIONS = {
    "river-dragon": "North Gate",
    "blue-crane": "River Walk",
    "moon-rabbit": "River Walk",
    "gold-tiger": "Market Street",
    "white-lotus": "Temple Road",
    "red-kite": "Temple Road",
}


def analyze_lanterns(
    expected_lanterns: set[str],
    lantern_log: list[tuple[str, str]],
    correct_sections: dict[str, str],
) -> dict[str, object]:
    """Analyze festival lantern records and return a report.

    Args:
        expected_lanterns:
            A set of lantern names that should appear at the festival.
        lantern_log:
            A list of records. Each record is a tuple:
            (lantern_name, actual_section).
        correct_sections:
            A dictionary where each key is an expected lantern name and each
            value is the section where that lantern should appear.

    Returns:
        A dictionary with these keys:
            - "seen_lanterns": set[str]
            - "missing_lanterns": set[str]
            - "unexpected_lanterns": set[str]
            - "duplicate_lanterns": set[str]
            - "count_by_section": dict[str, int]
            - "wrong_section_lanterns": dict[str, dict[str, str]]

    Important rules:
        - Return the dictionary. Do not only print it.
        - Only expected lanterns should be checked for wrong sections.
        - Unexpected lanterns should not appear in wrong_section_lanterns.
        - If an expected lantern appears in more than one wrong section, record
          the first wrong section found in the log.
    """
    # TODO 1: Create the collections you need.
    seen_lanterns = set()
    seen_once = set()
    duplicate_lanterns = set()
    count_by_section = {}
    wrong_section_lanterns = {}

    # TODO 2 & 3: Loop through lantern_log.
    for lantern_name, actual_section in lantern_log:
        # Track all seen lantern names
        seen_lanterns.add(lantern_name)

        # Detect duplicates: if we've seen it before, it's a duplicate
        if lantern_name in seen_once:
            duplicate_lanterns.add(lantern_name)
        else:
            seen_once.add(lantern_name)

        # Count how many records appear in each section
        if actual_section in count_by_section:
            count_by_section[actual_section] += 1
        else:
            count_by_section[actual_section] = 1

        # Check wrong sections for expected lanterns only (not unexpected ones)
        # Only record the FIRST wrong section found
        if lantern_name in expected_lanterns:
            expected_section = correct_sections.get(lantern_name)
            if expected_section is not None and actual_section != expected_section:
                if lantern_name not in wrong_section_lanterns:
                    wrong_section_lanterns[lantern_name] = {
                        "expected": expected_section,
                        "actual": actual_section,
                    }

    # TODO 4: After the loop, use set operations
    missing_lanterns = expected_lanterns - seen_lanterns
    unexpected_lanterns = seen_lanterns - expected_lanterns

    # TODO 5: Return the full report dictionary with all required keys.
    return {
        "seen_lanterns": seen_lanterns,
        "missing_lanterns": missing_lanterns,
        "unexpected_lanterns": unexpected_lanterns,
        "duplicate_lanterns": duplicate_lanterns,
        "count_by_section": count_by_section,
        "wrong_section_lanterns": wrong_section_lanterns,
    }


if __name__ == "__main__":
    report = analyze_lanterns(EXPECTED_LANTERNS, LANTERN_LOG, CORRECT_SECTIONS)
    print(report)
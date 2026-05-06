# Week 9 Homework: The Case of the Missing Festival Lanterns

## Student Info

| Field | Value |
|---|---|
| Name | Sopnil |
| Student number | 2412086 |
| GitHub username | sopnil96 |

---

## Summary

`analyze_lanterns` solves the problem of auditing a festival lantern log against a list of expected lanterns. It receives three inputs: a set of expected lantern names, a list of `(lantern_name, section)` log entries, and a dictionary mapping each lantern to its correct section. By processing the log in a single pass, it determines which expected lanterns were never seen (missing), which lanterns appeared that were not expected (unexpected), which lanterns appeared more than once (duplicates), how many entries were recorded per section, and which expected lanterns were found in the wrong section. It returns all of these findings together in a structured report dictionary.

---

## Approach

* First, I created five empty collections: `seen_lanterns` (set), `seen_once` (set), `duplicate_lanterns` (set), `count_by_section` (dict), and `wrong_section_lanterns` (dict).
* During the loop over `lantern_log`, I added each `lantern_name` to `seen_lanterns`, then used `seen_once` as a "have I met this before?" tracker — if the name was already in `seen_once` it went into `duplicate_lanterns`, otherwise it was added to `seen_once`.
* Still inside the loop, I incremented `count_by_section[actual_section]` (starting from 0 if the key was new) to count appearances per section.
* Also inside the loop, I checked whether the lantern is in `expected_lanterns` and, if so, looked up its correct section in `correct_sections`. When the actual section differed and the lantern had not already been recorded, I stored `{"expected": ..., "actual": ...}` in `wrong_section_lanterns` — this naturally captures only the first wrong section.
* After the loop, I used set subtraction to compute `missing_lanterns = expected_lanterns - seen_lanterns` and `unexpected_lanterns = seen_lanterns - expected_lanterns`.
* Finally, I returned a dictionary containing all six required keys.

---

## How I Used Dictionaries and Sets

1. **Sets used:**
   - `seen_lanterns` — collects every lantern name encountered; used at the end for set-subtraction.
   - `seen_once` — tracks names seen exactly once so far; comparing against it during the loop detects duplicates in O(1).
   - `duplicate_lanterns` — stores names that appeared more than once.
   - `expected_lanterns` (input) — membership tests (`in expected_lanterns`) are O(1) because it is a set.

2. **Dictionaries used:**
   - `count_by_section` — maps section name → integer count; a dict lets us look up and update any section's count in O(1).
   - `wrong_section_lanterns` — maps lantern name → `{"expected": ..., "actual": ...}`; a dict lets us check in O(1) whether we have already recorded the first wrong section for that lantern.
   - `correct_sections` (input) — used for O(1) look-up of a lantern's expected section.

3. **Why dicts/sets instead of only lists:**
   - Checking membership in a list is O(n); in a set or as a dict key it is O(1). With a list we would need a linear scan every time we asked "have I seen this lantern before?" or "is this lantern expected?".
   - Counting sections with a list would require scanning the whole list each time we want to update a counter, whereas a dict gives direct access by key.
   - Set subtraction (`A - B`) expresses "missing" and "unexpected" in one readable line and runs in O(len(A) + len(B)) instead of a nested loop.

```
Sets:  seen_lanterns, seen_once, duplicate_lanterns, expected_lanterns (input)
Dicts: count_by_section, wrong_section_lanterns, correct_sections (input)
Benefit: O(1) membership tests and key look-ups replace O(n) list scans.
```

---

## Complexity

```
Time complexity:  O(n)
Space complexity: O(n)

Explanation:
- n = number of records in lantern_log.
- The code loops through lantern_log exactly once (no nested loops), so all
  work inside the loop is O(1) per record (set add, dict look-up/update),
  giving O(n) total for the loop.
- The two set-subtraction operations after the loop each take O(s) where s is
  the number of expected lanterns; s is fixed and typically much smaller than
  n, so this does not change the overall O(n) time.
- Extra space: seen_lanterns, seen_once, and duplicate_lanterns each hold at
  most as many entries as there are distinct lantern names in the log (≤ n).
  count_by_section holds at most as many entries as there are distinct sections
  (≤ n). wrong_section_lanterns holds at most as many entries as there are
  expected lanterns (bounded by s ≤ n). Total extra space is therefore O(n).
```

---

## Edge-Case Checklist

- [x] empty `lantern_log`
- [x] empty `expected_lanterns`
- [x] no missing lanterns
- [x] no unexpected lanterns
- [x] duplicate lanterns
- [x] wrong-section lanterns
- [x] unexpected lanterns ignored for wrong-section checking

**One more edge case I thought about:**

```
All expected lanterns appear but every single one is in the wrong section.
This checks that the wrong-section logic runs for the full set of expected
lanterns and does not exit early or skip any entry.
(Covered by test_all_lanterns_in_wrong_sections.)
```

---

## Tests I Added

The starter tests are already provided.

```
Test name:   test_all_lanterns_in_wrong_sections

What it checks:
    Every expected lantern appears in the log, but each one is placed in a
    section that is NOT its correct section. The test verifies that:
      - missing_lanterns is empty (all were seen)
      - unexpected_lanterns is empty (no strangers appeared)
      - every expected lantern name appears in wrong_section_lanterns
      - the recorded "expected" value matches CORRECT for each lantern

Why it matters:
    Most tests only check one or two lanterns at a time. This test stresses
    the wrong-section detection across the complete set simultaneously,
    catching any off-by-one error, early exit, or accidental key collision
    that a smaller test might miss.
```

---

## How to Run the Tests

```bash
pytest -q
```

Paste your final test result here:

```
13 passed in 0.02s
```

---

## Assistance and Sources

```
AI used? Y
What it helped with: Structuring the solution, writing test cases,
                     and filling in this README.
Other sources used: Course lecture notes on sets and dictionaries.
```

---

## Submission Self-Check

Before submitting, check:

- [x] I completed `analyze_lanterns` in `src/challenges.py`.
- [x] I added at least one meaningful test of my own.
- [x] `pytest -q` passes.
- [x] I completed this README.
- [ ] I pushed my latest work to GitHub.
 
# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to fix three bugs I flagged with `#FIX` comments in `app.py` (a too-narrow "Hard" difficulty range, reversed "Go HIGHER!"/"Go LOWER!" hint text, and incorrect scoring), one at a time with a commit after each fix. Later I asked it to refactor the pure game logic out of `app.py` into a new `logic_utils.py` module, updating the imports accordingly, and to generate pytest regression tests for the bugs it had fixed. I also reported a bug I found by playing the game myself: after winning or running out of attempts, clicking "New Game" left the app unable to accept any new guesses.

**What did the agent do?**

- Fixed the "Hard" difficulty range (was narrower than "Normal"), the reversed hint messages in `check_guess`, and an off-by-one plus an inconsistent bonus in `update_score` — each as its own commit.
- Diagnosed and fixed a second scoring-related bug on its own initiative: the secret was being converted to a string on every other attempt, forcing a fallback code path that compared numbers as strings (lexicographic comparison gives wrong results for multi-digit numbers).
- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and updated `app.py`'s imports, verifying the module still imported correctly and `app.py` still parsed.
- Updated the existing tests in `tests/test_game_logic.py` (which had broken because `check_guess` now returns a tuple) and added new regression tests for the two hint/comparison bugs.
- Diagnosed the "New Game" bug: `st.session_state.status` was never reset to `"playing"` after a win/loss, so the page's own status check immediately blocked the guess input again on the next rerun. It also reset `history`, `score`, and used the correct difficulty range for the new secret.

**What did you have to verify or fix manually?**

- I had to explicitly ask whether the score should reset to 0 on "New Game" — the agent flagged the ambiguity rather than guessing, since the original code left it accumulating across games.
- I re-ran `pytest` myself and hit a `ModuleNotFoundError` for `logic_utils` when running the bare `pytest` command (as opposed to `python -m pytest`) — the agent's own verification only used `python -m pytest`, which masked the issue. It added a root-level `conftest.py` to fix the import path.
- I still needed to actually play the app in the browser to catch the "New Game" bug myself; the agent's automated checks (parsing, imports, pytest) wouldn't have caught a Streamlit session-state/UI issue like that.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Guess is above the secret | "Generate a pytest case in test/test_game_logic.py that specifically targets the bug you just fixed" (reversed hint text) | `test_too_high_message_says_go_lower` — asserts outcome is `"Too High"` and message contains "LOWER", not "HIGHER" | Yes | This pins down the exact defect (message text backwards), not just the outcome label, so it would fail again if the hint text regressed even if the outcome logic stayed correct. |
| Guess is below the secret | Same prompt as above | `test_too_low_message_says_go_higher` — asserts outcome is `"Too Low"` and message contains "HIGHER", not "LOWER" | Yes | Mirrors the "too high" case; covers both directions of the reversed-hint bug symmetrically. |
| Multi-digit guess/secret compared after implicit string conversion | Same prompt, applied to the second bug found (secret alternately coerced to `str`) | `test_multi_digit_comparison_is_numeric_not_lexicographic` — checks `check_guess(9, 10)` gives "Too Low" and `check_guess(100, 20)` gives "Too High" | Yes | Lexicographic string comparison (e.g. `"9" > "10"` is `True`) would silently give the wrong direction only for multi-digit numbers, so single-digit test cases wouldn't have caught it — these values were chosen specifically to expose that failure mode. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->

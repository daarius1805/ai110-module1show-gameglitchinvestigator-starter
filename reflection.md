# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked like a normal Streamlit number guesser (pick a difficulty, guess a number, get higher/lower hints), but several things were subtly wrong once I actually played it. The hints told me to go the opposite direction of what I actually needed, "Hard" difficulty was easier than "Normal" instead of harder, and the score sometimes moved in ways that didn't match whether my guess was actually good. There was also a bug where the app would get completely stuck after a win or loss — clicking "New Game" didn't let me enter another guess.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess higher than the secret (e.g. secret=50, guess=60) | Hint says "Go LOWER!" | Hint said "Go HIGHER!" | No error — wrong hint text returned by `check_guess` |
| Select "Hard" difficulty | Range should be wider than "Normal" (e.g. 1–200) | Range was 1–50, narrower than "Normal"'s 1–100 | No error — `get_range_for_difficulty` returned the wrong bounds |
| Guess is too high on an even-numbered attempt, with a multi-digit secret (e.g. guess=9, secret=10) | "Too Low" (9 < 10) | Sometimes "Too High" | No crash visible in the UI, but `check_guess` was comparing `"9" > "10"` as strings (lexicographic), which is `True` |
| Win or lose the game, then click "New Game" | New secret picked, attempts/score/status reset, guess input works again | Guess input stayed hidden; app showed "Game over" / "You already won" forever | No error — `st.session_state.status` was never reset to `"playing"` in the New Game handler |

---

## 2. How did you use AI as a teammate?

I used Claude (via Claude Code) as my main AI tool for this project — I pointed it at the specific `#FIX` comments and bugs I found, and asked it to fix them one at a time, refactor the logic, and write tests.

One example of a correct AI suggestion: I asked it to fix the reversed hint messages in `check_guess`. It correctly identified that `guess > secret` should say "Go LOWER!" (not "Go HIGHER!") and swapped both branches, including the matching fallback branch further down in the same function. I verified this by re-reading the fixed function and later by writing a pytest test (`test_too_high_message_says_go_lower`) that asserts the message text explicitly.

One example I didn't accept as written: to fix a `ModuleNotFoundError` when running the bare `pytest` command (as opposed to `python -m pytest`), the AI added an empty `conftest.py` at the project root. It looked like a useless empty file to me, so I deleted it. The AI explained that pytest specifically uses a conftest.py's location to decide what to add to its import path, so the file being empty was the point — it just needed to exist there, not contain anything. I verified this by running the bare `pytest` command with the file deleted, which reproduced the exact same `ModuleNotFoundError: No module named 'logic_utils'`; re-adding the empty file made all 6 tests pass again, confirming the AI's explanation was correct.

---

## 3. Debugging and testing your fixes

I considered a bug really fixed once I could both read through the corrected logic and confirm it by actually triggering the scenario — either manually in the running app or with a pytest test that reproduces the exact input that used to break. For most of the logic bugs (hints, scoring, range), reading the diff plus a passing pytest test was enough; for the "New Game" state bug, I only caught it by actually clicking through the app in the browser after a win, since none of the automated checks (import checks, `ast.parse`, pytest) would exercise a Streamlit session-state/UI flow like that.

One test I ran: `test_multi_digit_comparison_is_numeric_not_lexicographic` in `tests/test_game_logic.py` calls `check_guess(9, 10)` and asserts it returns "Too Low". This showed me that the old bug (comparing numbers as strings on alternating attempts) wasn't just a cosmetic issue — it could flip the actual outcome for two-digit numbers, since `"9" > "10"` is `True` as a string comparison even though `9 < 10` numerically.

AI helped me design these tests directly — I asked it to generate pytest cases targeting specific bugs it had just fixed, and it picked input values (like 9 vs. 10) specifically chosen to expose the failure mode rather than generic/random numbers, which made the tests much more meaningful than if I'd just picked arbitrary guesses myself.

---

## 4. What did you learn about Streamlit and state?

I'd explain it like this: every time you interact with a Streamlit app — click a button, type into a box, check a checkbox — Streamlit doesn't just update that one widget, it reruns your *entire* Python script from top to bottom. Any plain Python variable you set (like `secret = random.randint(...)`) gets wiped out and recreated from scratch on every single rerun, which is why the original game's secret number kept changing on every guess. `st.session_state` is the one thing that survives between reruns — it's like a dictionary that Streamlit keeps alive for you across that reset, so anything that needs to persist (the secret number, score, attempt count, game status) has to live there instead of in a normal variable. The bug I found with "New Game" was a perfect example of this: the button set some session_state values but forgot to reset `status`, so even after a full rerun, that one stale leftover value kept blocking the rest of the page.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is fixing and committing bugs one at a time instead of batching everything into one big commit — it made each change easy to review on its own, and if something had gone wrong I could point to exactly which commit introduced the problem. I also want to keep the habit of asking for a regression test tied to the specific bug just fixed, rather than generic tests, since that's what caught that the hint-direction bug and the string-comparison bug were actually two separate issues.

One thing I'd do differently next time is verify AI-reported fixes under more than one way of running things before trusting them — the AI's own verification of the `conftest.py` fix only used `python -m pytest`, which hid the fact that the bare `pytest` command still failed, and I only caught that because I happened to run it differently myself.

This project changed how I think about AI-generated code because it showed me that AI code can look completely reasonable and still be subtly, confidently wrong — the bugs weren't crashes or syntax errors, they were logic that *ran fine* but did the opposite of what it claimed to do, which means I can't just trust that working code is correct code.

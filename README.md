# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

The game is a Streamlit number-guessing game: pick a difficulty, the app secretly picks a number in that difficulty's range, and you have a limited number of attempts to guess it with "higher/lower" hints along the way. As shipped, it was broken in several ways (see `reflection.md` for the full bug log):

- The "Hard" difficulty range (1–50) was narrower than "Normal" (1–100), making Hard easier instead of harder.
- The "Go HIGHER!"/"Go LOWER!" hint text was reversed relative to the actual guess direction.
- `update_score` had an off-by-one in the win-points formula and inconsistently awarded (instead of deducted) points for a "Too High" guess on even-numbered attempts.
- The secret number was silently converted to a string on every other attempt, which forced guess comparisons through a buggy string-comparison fallback that gives wrong answers for multi-digit numbers.
- Clicking "New Game" after a win or loss never reset the game's status flag, so the app stayed stuck on the end-of-game screen and wouldn't accept new guesses.

Each bug was fixed in its own commit, and the core game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) was refactored out of `app.py` into `logic_utils.py` so it can be tested without the Streamlit UI.

## 📸 Demo Walkthrough

1. Run the app and the sidebar shows the selected difficulty's actual range (e.g. "Hard" now shows 1–200, wider than "Normal").
2. Enter a guess that's higher than the secret number — the hint now correctly says "Go LOWER!".
3. Enter a guess that's lower than the secret number — the hint now correctly says "Go HIGHER!".
4. Keep guessing until you find the secret number — you get the "🎉 Correct!" win message, balloons, and a final score that reflects the number of attempts taken.
5. Click "New Game 🔁" — the game immediately resets (new secret, attempts, score, and history) and accepts guesses right away, instead of staying stuck on the old win/loss screen.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
pytest tests/
============================= test session starts =============================
platform win32 -- Python 3.10.9, pytest-9.1.1, pluggy-1.6.0
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 50%]
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED     [ 66%]
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED     [ 83%]
tests/test_game_logic.py::test_multi_digit_comparison_is_numeric_not_lexicographic PASSED [100%]

========================== 6 passed in 0.06s ==========================
```

## 🚀 Stretch Features

- [ ] Challenge 4 (Enhanced UI) was not attempted.

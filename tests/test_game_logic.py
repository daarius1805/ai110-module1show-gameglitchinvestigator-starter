from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_message_says_go_lower():
    # Regression test: check_guess used to say "Go HIGHER!" when the
    # guess was above the secret, which is backwards. A guess above
    # the secret should tell the player to go lower.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_message_says_go_higher():
    # Regression test: check_guess used to say "Go LOWER!" when the
    # guess was below the secret, which is backwards. A guess below
    # the secret should tell the player to go higher.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_multi_digit_comparison_is_numeric_not_lexicographic():
    # Regression test: app.py used to convert the secret to a string
    # on alternating attempts, forcing check_guess through a
    # string-comparison fallback. Lexicographic string comparison
    # gives the wrong answer for multi-digit numbers (e.g. "9" > "10"
    # is True as strings, even though 9 < 10 numerically). Both
    # guess and secret must always be compared as numbers.
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low"
    assert "HIGHER" in message

    outcome, message = check_guess(100, 20)
    assert outcome == "Too High"
    assert "LOWER" in message

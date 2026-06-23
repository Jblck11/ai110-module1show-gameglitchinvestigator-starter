# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

-The game looked ok but the functionality was off. the number guesses seemed inconsistant. when i selected the number 1 it still responded with "lower". When i tried 0, i expected invalid but it still said lower. Also when i tried a high number, even if the answer was lower the hint still stated higher


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input      | Expected Behavior         | Actual Behavior | Console Output / Error |
|------------|---------------------------|-----------------|------------------------|
 guess of 1  |unless answer is 1         |response: "Lower"| "None"
               response should be "higher"|                                          
 guess of 0  | "invalid"; instructions state| response: "Lower" | "None"
             | guess from 1 - 100           |
 Selecting "New game"| Game Reset | No response; game over banner remains | "None"
 button              |       
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

I used Claude Code (in agent mode) as my main AI teammate for this project. I used it to help me check the bugs, refactor the game logic, and write tests, while I made the choices about what to actually keep.

A correct suggestion: when I described the backwards hint behavior, Claude figured out that `check_guess` was returning "Go HIGHER!" for a too-high guess and vice versa, and swapped the messages. I verified the fix by writing a pytest test that checks a guess of 1 against a secret of 50 returns "Too Low" — it passed, along with the other 16 tests.

An incorrect/misleading suggestion: the AI first told me to run the app with `py -m streamlit run app.py`, but that kept giving me "No module named streamlit." I verified the problem by checking which Python `py` was actually using, and found I had two virtual environments and was activating an empty one inside the project folder instead of the real shared one. So the AI's command looked reasonable but was wrong for my setup until we tracked down the environment problem together.

## 3. Debugging and testing your fixes

Determined bug was  fixed when I could both reproduce the old behavior and then show it was gone — for the logic bugs that meant a pytest test. For the "New Game" bug it meant clicking the button in the browser and watching the game-over banner actually disappear. I ran `python -m pytest test/test_game_logic.py` and all 17 tests passed, including a regression test for the backwards-hint glitch and tests confirming a wrong guess always loses 5 points. That showed me my `check_guess` and `update_score` functions behaved correctly across the cases, not just the one I happened to try by hand.

AI helped me design the tests. Claude wrote the parametrized pytest suite (covering difficulty ranges, parsing, guess checking, and scoring) and explained why a regression test for the "guess 1 → Go LOWER" bug was worth keeping so the glitch can't quietly come back.

---

## 4. What did you learn about Streamlit and state?

I'd tell a friend that Streamlit re-runs your whole script from top to bottom every single time you interact with the page — every button click or checkbox toggle starts the script over from line 1. Because of that, any normal variable gets wiped and recreated on each run, so if you want to remember something (like the secret number, the score, or whether the game is over) you have to store it in `st.session_state`, which survives between reruns. Two of our bugs were really state bugs: the secret number was getting changed on some reruns, and the "New Game" button reset the score and secret but forgot to reset the `status`, so the game-over banner kept coming back on the next rerun. Once I thought about it as "the script restarts, but session_state remembers," those bugs made a lot more sense.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing a quick pytest test to confirm a bug is fixed instead of just eyeballing it once — pulling the game logic out of `app.py` into `logic_utils.py` made that easy and I want to keep separating logic from the UI so it stays testable. One thing I'd do differently next time is to check my environment first (which Python and which virtual environment I'm actually using) before assuming an AI's run command is wrong, because I lost time on the "No module named streamlit" error that turned out to be the wrong venv, not the code.

This project changed how I think about AI-generated code: it can produce correct fixes and useful tests fast, but it can also confidently give me commands or code that don't fit my actual setup, so I learned to treat its output as a strong suggestion I still have to verify myself.

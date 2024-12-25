from flask import Flask, render_template, request, redirect, url_for, session

# Questions and answers
QUESTIONS = [
    {
        "question": "Which country has the highest population in the world?",
        "options": ["a. China", "b. India", "c. United States", "d. Russia"],
        "answer": "a",
        "prize": 100
    },
    {
        "question": "What is the capital city of Australia?",
        "options": ["a. Sydney", "b. Canberra", "c. Melbourne", "d. Perth"],
        "answer": "b",
        "prize": 200
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["a. Yaun", "b. Dollar", "c. Yen", "d. Pounds"],
        "answer": "c",
        "prize": 200
    },
    {
        "question": "Which country has the highest population in the world?",
        "options": ["a. China", "b. India", "c. United States", "d. Russia"],
        "answer": "a",
        "prize": 100
    },
    {
        "question": "What is the capital city of Australia?",
        "options": ["a. Sydney", "b. Canberra", "c. Melbourne", "d. Perth"],
        "answer": "b",
        "prize": 200
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["a. Yaun", "b. Dollar", "c. Yen", "d. Pounds"],
        "answer": "c",
        "prize": 200
    },
    # Add more questions here...
]

app = Flask(__name__)
app.secret_key = "kbc_secret_key"  # For session management


@app.route("/")
def home():
    session.clear()  # Clear session data for a new game
    return render_template("index.html")


@app.route("/start_game", methods=["POST"])
def start_game():
    session["current_question"] = 0
    session["prize"] = 0
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    current_question_index = session.get("current_question", 0)
    prize = session.get("prize", 0)

    # Check if we've reached the end of the game
    if current_question_index >= len(QUESTIONS):
        return redirect(url_for("result", prize=prize))

    current_question = QUESTIONS[current_question_index]

    if request.method == "POST":
        selected_option = request.form.get("option")
        correct_option = current_question["answer"]

        if selected_option == correct_option:
            # Correct answer, move to the next question
            session["prize"] += current_question["prize"]
            session["current_question"] += 1
            return redirect(url_for("game"))
        else:
            # Incorrect answer, end the game
            return redirect(url_for("result", prize=prize, lost=True))

    return render_template("game.html", question=current_question, prize=prize)


@app.route("/result")
def result():
    prize = request.args.get("prize", 0)
    lost = request.args.get("lost", False)
    return render_template("result.html", prize=prize, lost=lost)


if __name__ == "__main__":
    app.run(debug=True)

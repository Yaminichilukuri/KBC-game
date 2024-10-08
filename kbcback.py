from flask import Flask, request, render_template, jsonify
import qrcode
import io
import base64

app = Flask(__name__)

# Sample Questions
questions = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Paris", "Madrid", "Rome"], "answer": "Paris"},
    {"question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Leo Tolstoy"], "answer": "William Shakespeare"},
    {"question": "What is the largest planet in our solar system?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter"},
    {"question": "What is the chemical symbol for gold?", "options": ["Ag", "Au", "Pb", "Fe"], "answer": "Au"},
    {"question": "In which year did the Titanic sink?", "options": ["1905", "1912", "1915", "1920"], "answer": "1912"}
]

current_question_index = 0

@app.route('/')
def index():
    global current_question_index

    if current_question_index >= len(questions):
        current_question_index = 0  # Reset to first question when all are answered

    question = questions[current_question_index]
    
    # Generate QR code for the current question
    qr_data = f"http://localhost:5000/question/{current_question_index}"
    qr = qrcode.make(qr_data)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_code = base64.b64encode(buffered.getvalue()).decode()

    # Render the template with the current question, options, and QR code
    return render_template('index.html', question=question['question'], options=question['options'], qr_code=qr_code, current_question_index=current_question_index)

@app.route('/question/<int:question_index>', methods=['POST'])
def question_response(question_index):
    global current_question_index
    player_name = request.form['name']
    answer = request.form['answer']
    correct_answer = questions[question_index]['answer']

    if answer == correct_answer:
        current_question_index += 1  # Move to the next question if the answer is correct
        return jsonify({"status": "correct", "name": player_name})
    else:
        return jsonify({"status": "wrong"})

if __name__ == '__main__':
    app.run(debug=True)

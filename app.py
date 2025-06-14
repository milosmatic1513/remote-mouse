import pyautogui
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/mouse/move', methods=['POST'])
def move_mouse():
    data = request.get_json()
    direction = data.get('direction')
    distance = data.get('distance', 10)

    x, y = pyautogui.position()

    if direction == 'up':
        y -= distance
    elif direction == 'down':
        y += distance
    elif direction == 'left':
        x -= distance
    elif direction == 'right':
        x += distance
    else:
        return jsonify({'status': 'error', 'message': 'Invalid direction'}), 400

    pyautogui.moveTo(x, y)
    return jsonify({'status': 'success', 'new_position': {'x': x, 'y': y}})


@app.route('/mouse/click', methods=['POST'])
def click_mouse():
    data = request.get_json()
    button = data.get('button', 'left')
    clicks = data.get('clicks', 1)
    interval = data.get('interval', 0.0)

    if button not in ['left', 'right', 'middle']:
        return jsonify({'status': 'error', 'message': 'Invalid button'}), 400

    pyautogui.click(button=button, clicks=clicks, interval=interval)
    return jsonify({'status': 'success', 'action': 'click', 'button': button})


@app.route('/mouse/scroll', methods=['POST'])
def scroll_mouse():
    data = request.get_json()
    amount = data.get('amount', 1)
    pyautogui.scroll(amount)
    return jsonify({'status': 'success', 'action': 'scroll', 'amount': amount})


@app.route('/mouse/position', methods=['GET'])
def get_position():
    x, y = pyautogui.position()
    return jsonify({'status': 'success', 'position': {'x': x, 'y': y}})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

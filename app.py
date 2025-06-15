import pyautogui
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <- this allows CORS for all routes by default


@app.route('/mouse/move', methods=['POST'])
def move_mouse():
    data = request.get_json()
    move_x = data.get('moveX', 0)
    move_y = data.get('moveY', 0)
    x, y = pyautogui.position()
    pyautogui.moveTo(x+move_x, y+move_y)

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
    app.run(host='0.0.0.0', port=5000, debug=True)

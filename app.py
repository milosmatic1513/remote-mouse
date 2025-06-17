#import pyautogui
import socket

from io import BytesIO

import qrcode
from flask import Flask, request, jsonify, render_template, abort, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, send
import platform

system = platform.system()

if system == "Windows":
    from windows import volume_change
else:
    def volume_change(amount): print("Unsupported OS.")
    def set_volume(level): print("Unsupported OS.")
    def toggle_mute(): print("Unsupported OS.")


def get_local_ip():
    # Grab local IP address (works on most LANs)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

app = Flask(__name__)
CORS(app)  # <- this allows CORS for all routes by default
socketio = SocketIO(app, cors_allowed_origins="*")
ALLOWED_IPS = []

with open('whitelist.txt', 'r') as file:
    ALLOWED_IPS = [line.strip() for line in file if line.strip()]

local_ip = get_local_ip()
ALLOWED_IPS.append(local_ip)

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        print(
            f"User with ip: {request.remote_addr} is trying to access remote! If you want to allow this user to access the remote, add to whitelist and restart")
        abort(403)  # Forbidden


@app.route('/mouse/move', methods=['POST'])
def move_mouse():
    data = request.get_json()
    move_x = int(data.get('moveX', 0))
    move_y = int(data.get('moveY', 0))
    speed_modifier = int(data.get('speedModifier', 50)) / 100
    x, y = pyautogui.position()
    pyautogui.moveTo(x + move_x * speed_modifier, y - move_y * speed_modifier)

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


@app.route('/', methods=['GET'])
def whitelist():
    img = qrcode.make('http://'+local_ip+':5000/remote')
    type(img)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/media/volume', methods=['POST'])
def volume():
    data = request.get_json()
    amount = float(data.get('amount', 1.0))
    volume_change(amount)
    return jsonify({'status': 'success', 'action': 'volume', 'amount': amount})

@app.route('/remote')
def index():
    return render_template('index.html')

@socketio.on('mouse_move')
def mouse_move_socket(data):
    move_x = int(data['x'])
    move_y = int(data['y'])
    print(move_x,move_y)
    speed_modifier = int(data['mod']) / 100
    x, y = pyautogui.position()
    pyautogui.moveTo(x + move_x * speed_modifier, y - move_y * speed_modifier)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

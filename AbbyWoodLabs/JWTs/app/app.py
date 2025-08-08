from flask import Flask, request, render_template, jsonify, redirect, make_response
import jwt
import datetime
import json
from base64 import b64decode

app = Flask(__name__)
SECRET_KEY = 'supersecretsecret'  # <- Intentionally weak for challenge

MAX_CLICKS = 1000000

def create_token(clicks):
    payload = {
        'clicks': clicks,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        # Split JWT manually
        parts = token.split('.')
        if len(parts) != 2 and len(parts) != 3:
            raise ValueError("Expected unsigned JWT with 2 parts (header.payload)")

        header_b64 = parts[0]
        payload_b64 = parts[1]
        header = json.loads(b64decode(header_b64 + '==').decode())
        payload = json.loads(b64decode(payload_b64 + '==').decode())

        # Ensure alg is 'none'
        if header.get('alg') != 'none':
            raise ValueError("Only 'alg: none' tokens are accepted")

        # Optional: enforce expiration if needed

        return payload
    except Exception as e:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    

@app.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        token = create_token(0)
        resp = make_response(render_template('index.html', clicks=0))
        resp.set_cookie('token', token)
        return resp

    try:
        data = decode_token(token)
        clicks = data['clicks']
        return render_template('index.html', clicks=clicks)
    except jwt.ExpiredSignatureError:
        return "Session expired. Refresh to restart."
    except jwt.InvalidTokenError:
        return "Invalid token."

@app.route('/click', methods=['POST'])
def click():
    token = request.cookies.get('token')
    try:
        data = decode_token(token)
        clicks = data.get('clicks', 0) + 1

        if clicks >= MAX_CLICKS:
            flag = "Congrats! It worked!"
            return jsonify({'flag': flag})

        new_token = create_token(clicks)
        resp = make_response(jsonify({'clicks': clicks}))
        resp.set_cookie('token', new_token)
        return resp

    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)



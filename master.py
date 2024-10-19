
from flask import Flask, request, jsonify

app = Flask(__name__)

master_log = []

secondaries = ["http://secondary1:3001", "http://secondary2:3002"]

@app.route('/log', methods=['POST'])
def append_log():
    message = request.json.get('message')
    if not message:
        return "No message", 400

    master_log.append(message)


    for secondary in secondaries:
        try:
            res = request.post(f"{secondary}/log", json={'message':message})
            if response.status_code != 200:
                return f"Failed ti replicate to {secondary}", 500



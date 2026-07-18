from flask import Flask, request, jsonify
import json, time, os

app = Flask(__name__)
STATE_FILE = "/tmp/state.json"

def read_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"cmd": "stop", "mode": 1, "intensity": 0, "updated_at": 0}

def write_state(s):
    s["updated_at"] = time.time()
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)

@app.route("/")
def home():
    return "Toy Bridge Running"

@app.route("/state")
def state():
    return jsonify(read_state())

@app.route("/set")
def set_cmd():
    mode = int(request.args.get("mode", 1))
    intensity = int(request.args.get("intensity", 0))
    write_state({"cmd": "set", "mode": mode, "intensity": intensity})
    return "OK"

@app.route("/stop")
def stop():
    write_state({"cmd": "stop", "mode": 0, "intensity": 0})
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

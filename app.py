from flask import Flask, request, jsonify
from fastmcp import FastMCP
import json, time

app = Flask(__name__)
mcp = FastMCP("toy")

STATE_FILE = "/tmp/state.json"

def read_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"cmd":"stop","mode":1,"intensity":0,"updated_at":0}

def write_state(s):
    s["updated_at"] = time.time()
    with open(STATE_FILE,"w") as f:
        json.dump(s,f)

@mcp.tool()
def toy_set(mode:int=1, intensity:int=3) -> str:
    """控制toy，mode模式1-8，intensity强度1-5"""
    write_state({"cmd":"set","mode":mode,"intensity":intensity})
    return f"OK mode={mode} intensity={intensity}"

@mcp.tool()
def toy_stop() -> str:
    """停止toy"""
    write_state({"cmd":"stop","mode":0,"intensity":0})
    return "stopped"

@mcp.tool()
def toy_status() -> dict:
    """查看toy当前状态"""
    return read_state()

@app.route("/")
def home():
    return "Toy Bridge Running"

@app.route("/state")
def state():
    return jsonify(read_state())

@app.route("/set")
def set_cmd():
    mode=int(request.args.get("mode",1))
    intensity=int(request.args.get("intensity",0))
    write_state({"cmd":"set","mode":mode,"intensity":intensity})
    return "OK"

@app.route("/stop")
def stop():
    write_state({"cmd":"stop","mode":0,"intensity":0})
    return "OK"

if __name__=="__main__":
    import threading
    threading.Thread(target=lambda: mcp.run(transport="streamable-http",host="0.0.0.0",port=8001),daemon=True).start()
    app.run(host="0.0.0.0",port=8000)

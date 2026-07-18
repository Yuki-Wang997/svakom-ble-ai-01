from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
import json
import time


STATE_FILE = "/tmp/state.json"


def read_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {
            "cmd": "stop",
            "mode": 0,
            "intensity": 0,
            "updated_at": 0
        }


def write_state(s):
    s["updated_at"] = time.time()
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)


mcp = FastMCP("toy")


@mcp.tool()
def toy_set(mode: int = 1, intensity: int = 3) -> str:
    """
    控制toy，mode模式1-8，intensity强度1-5
    """
    write_state({
        "cmd": "set",
        "mode": mode,
        "intensity": intensity
    })
    return f"OK mode={mode} intensity={intensity}"


@mcp.tool()
def toy_stop() -> str:
    """
    停止toy
    """
    write_state({
        "cmd": "stop",
        "mode": 0,
        "intensity": 0
    })
    return "stopped"


@mcp.tool()
def toy_status() -> dict:
    """
    查看toy当前状态
    """
    return read_state()


# 给 bridge.py 使用的接口
@mcp.custom_route("/toy-next", methods=["GET"])
async def toy_next(request: Request):
    return JSONResponse(read_state())


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )

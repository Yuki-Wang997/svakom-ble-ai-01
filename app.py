from flask import Flask, request
import asyncio
from bleak import BleakClient
import os

app = Flask(__name__)

TOY_ADDR = os.environ.get("BLEDEVICE", "FF:26:01:5D:F9:5F")
WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

def build_cmd(intensity):
    return bytes([0x55, 0x04, 0x00, 0x00, 0x01, intensity, 0xAA])

@app.route('/set')
def set_intensity():
    try:
        intensity = int(request.args.get('intensity', 0))
        asyncio.run(send_cmd(intensity))
        return f"OK {intensity}"
    except Exception as e:
        return f"Error: {e}"

async def send_cmd(intensity):
    try:
        async with BleakClient(TOY_ADDR) as client:
            await client.write_gatt_char(WRITE_UUID, build_cmd(intensity))
    except Exception as e:
        print(f"Connection error: {e}")

@app.route('/')
def home():
    return "Toy Control Running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

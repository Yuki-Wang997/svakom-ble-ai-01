"""
测试各种控制命令，确认设备响应。
用法：python test.py
"""
import asyncio
from bleak import BleakScanner, BleakClient

WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
H = 0x55

def cmd_scale(v):
    return bytes([H, 4, 0, 0, 1, max(0, min(255, v)), 0xAA])

def cmd_vibrate(mode, level):
    return bytes([H, 3, 0, 0, max(1,min(8,mode)), max(1,min(5,level)), 0])

def cmd_stop():
    return bytes([H, 4, 0, 0, 0, 0, 0xAA])

async def main():
    print("🔍 扫描 SL278H ...")
    devs = await BleakScanner.discover(timeout=6.0)
    dev = next((d for d in devs if d.name and "SL278" in d.name), None)
    if not dev:
        print("⚠️ 没找到设备"); return
    print(f"✅ 连接 {dev.name} ...\n")

    async with BleakClient(dev) as c:
        tests = [
            ("强度 30%",  cmd_scale(77)),
            ("强度 60%",  cmd_scale(153)),
            ("强度 100%", cmd_scale(255)),
            ("花样1 弱",  cmd_vibrate(1, 2)),
            ("花样3 中",  cmd_vibrate(3, 3)),
            ("花样5 强",  cmd_vibrate(5, 5)),
            ("花样8 强",  cmd_vibrate(8, 5)),
            ("停止",      cmd_stop()),
        ]
        for name, buf in tests:
            print(f"▶ {name}  {buf.hex()}")
            await c.write_gatt_char(WRITE_UUID, buf, response=False)
            await asyncio.sleep(3)

        print("\n⏹ 测试完毕")

asyncio.run(main())

from Devices.thorlabs_rotation_mount import RotationMount
from Devices.camera_automation import CameraAutomation
from Devices.LED_control import LEDController

import asyncio
import time
import os
from pathlib import Path
import tomllib



config_path = Path(__file__).parent / "config" / "rotation_mounts_SN.toml"
with open(config_path, "rb") as f:
    config = tomllib.load(f)


for key, value in config.items():
    print(key, value)

analyzer = RotationMount(config["analyzer_SN"])
qwp1 = RotationMount(config["qwp1_SN"])
qwp2 = RotationMount(config["qwp2_SN"])
polarizer = RotationMount(config["polarizer_SN"])

rotation_mounts = [analyzer, qwp1, qwp2, polarizer]
for mount in rotation_mounts:
    mount.open_device()
    mount.setup_conversion()


async def move_mount(mount, position):
    await asyncio.get_event_loop().run_in_executor(None, mount.move_to_position, position)

angles = [90, 90, 180, 180]

async def move_all_mounts():
    tasks = [
        move_mount(polarizer, angles[0]),
        move_mount(qwp1, angles[1]),
        move_mount(qwp2, angles[2]),
        move_mount(analyzer, angles[3]),
    ]
    await asyncio.gather(*tasks)

asyncio.run(move_all_mounts())








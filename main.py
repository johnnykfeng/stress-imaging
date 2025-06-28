from Devices.thorlabs_rotation_mount import RotationMount
from Devices.camera_automation import CameraAutomation
from Devices.LED_control import LEDController

import asyncio
from pathlib import Path
import tomllib
from utils import rad_to_deg, deg_to_rad
import numpy as np
import time

config_path = Path(__file__).parent / "config.toml"
with open(config_path, "rb") as f:
    config = tomllib.load(f)

polarizer = RotationMount(config["polarizer_SN"], label="Polarizer", mirror=False)
qwp1 = RotationMount(config["qwp1_SN"], label="QWP1", mirror=True)
qwp2 = RotationMount(config["qwp2_SN"], label="QWP2", mirror=False)
analyzer = RotationMount(config["analyzer_SN"], label="Analyzer", mirror=True)

rotation_mounts = [analyzer, qwp1, qwp2, polarizer]
for mount in rotation_mounts:
    mount.open_device()
    mount.setup_conversion()

angles_Tsinghua = {
    "I1": [5*np.pi/8, None, None, np.pi/8], 
    "I2": [np.pi/2, None, None, 0], 
    "I3": [7*np.pi/8, None, None, 3*np.pi/8], 
    "I4": [3*np.pi/4, None, None, np.pi/4],
    "I5": [np.pi/2, 3*np.pi/2, 0, np.pi/4],
    "I6": [np.pi/2, 3*np.pi/2, 0, 3*np.pi/4],
    "I7": [np.pi/2, 3*np.pi/2, 0, 0],
    "I8": [np.pi/2, 3*np.pi/2, np.pi/4, np.pi/4],
    "I9": [np.pi/2, 3*np.pi/2, np.pi/2, np.pi/2],
   "I10": [np.pi/2, 3*np.pi/2, 3*np.pi/4, 3*np.pi/4],
    }

angles_Ramesh = {
    "I1": [0, None, None, np.pi/2], 
    "I2": [np.pi/4, None, None, np.pi/2], 
    "I3": [0, None, None, np.pi/4], 
    "I4": [np.pi/4, None, None, 3*np.pi/4],
    "I5": [np.pi/2, 3*np.pi/2, np.pi/4, np.pi/2],
    "I6": [np.pi/2, 3*np.pi/2, np.pi/4, 0],
    "I7": [np.pi/2, 3*np.pi/2, 0, 0],
    "I8": [np.pi/2, 3*np.pi/2, np.pi/4, np.pi/4],
    "I9": [np.pi/2, np.pi/4, 0, 0],
   "I10": [np.pi/2, np.pi/4, 3*np.pi/4, np.pi/4],
    }

async def move_mount(mount, position):
    await asyncio.get_event_loop().run_in_executor(None, mount.move_to_position, position)


async def move_all_mounts(step="I1"):
    tasks = [
        move_mount(polarizer, rad_to_deg(angles_Ramesh[step][0])),
        move_mount(qwp1, rad_to_deg(angles_Ramesh[step][1])),
        move_mount(qwp2, rad_to_deg(angles_Ramesh[step][2])),
        move_mount(analyzer, rad_to_deg(angles_Ramesh[step][3])),
    ]
    await asyncio.gather(*tasks)

steps = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"]

for step in steps:
    asyncio.run(move_all_mounts(step=step))
    time.sleep(1)


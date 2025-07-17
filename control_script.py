from Devices.thorlabs_rotation_mount import RotationMount
from Devices.camera_automation import CameraAutomation
from Devices.LED_control import LEDController

import asyncio
from pathlib import Path
import tomllib
# from utils import rad_to_deg, deg_to_rad
# import numpy as np
import time
from loguru import logger

# ------------------------------------------------------------------
# Configure a file sink
# ------------------------------------------------------------------
log_dir = Path(__file__).with_suffix("").parent / "logs"
log_dir.mkdir(exist_ok=True)                           # create folder if it doesn't exist
logger.add(
    log_dir / "control_script_{time}.log",             # one file per run
    level="DEBUG",                                     # capture everything
    rotation="10 MB",                                  # start a new file when it reaches 10 MB
    retention="14 days",                               # keep logs for two weeks
    compression="zip",                                 # older logs are zipped
    enqueue=True,                                      # thread-/process-safe
    backtrace=True, diagnose=True                      # nicer tracebacks
)

config_path = Path(__file__).parent / "config.toml"
with open(config_path, "rb") as f:
    config = tomllib.load(f)

image_save_path = Path("R:/Pockels_data/STRESS IMAGING/Polariscope-Test")
image_save_path.mkdir(parents=True, exist_ok=True) # create folder if it doesn't exist
cam = CameraAutomation()
led = LEDController()
led.set_current(800)
led.turn_on()

polarizer = RotationMount(config["polarizer_SN"], label="Polarizer", mirror=False)
qwp1 = RotationMount(config["qwp1_SN"], label="QWP1", mirror=True)
qwp2 = RotationMount(config["qwp2_SN"], label="QWP2", mirror=False)
analyzer = RotationMount(config["analyzer_SN"], label="Analyzer", mirror=True)

rotation_mounts = [polarizer, qwp1, qwp2, analyzer]
for mount in rotation_mounts:
    mount.open_device()
    mount.setup_conversion()


angles_Ramesh = config["angles_Ramesh"]

async def move_mount(mount, position):
    await asyncio.get_event_loop().run_in_executor(None, mount.move_to_position, position)


async def move_all_mounts(step, phase_offset=90.0):
    if step in ["I1", "I2", "I3", "I4"]:
        tasks = [
            move_mount(polarizer, angles_Ramesh[step][0]+phase_offset),
            move_mount(analyzer, angles_Ramesh[step][3]+phase_offset),
        ]
    else:
        tasks = [
            move_mount(polarizer, angles_Ramesh[step][0]+phase_offset),
            move_mount(qwp1, angles_Ramesh[step][1]+phase_offset),
            move_mount(qwp2, angles_Ramesh[step][2]+phase_offset),
            move_mount(analyzer, angles_Ramesh[step][3]+phase_offset),
        ]
    await asyncio.gather(*tasks)

steps = ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"]

for i, step in enumerate(steps):
    response = input(f"Move to {step}? ('n' to skip, Enter to continue)")
    if response.lower() != "n":
        if step == "I5":
            response2 = input("Mount the QWPs before continuing. Press Enter to continue.")
        asyncio.run(move_all_mounts(step=step))
        time.sleep(1)
        if i == 0: # only type save path in the first image
            cam.save_image_png_typewrite(f"{step}_CZT.png", 
                                         save_path=str(image_save_path))
        else:
            cam.save_image_png_typewrite(f"{step}_CZT.png")

### SHUTDOWN ###
led.turn_off()
for mount in rotation_mounts:
    mount.close_device()
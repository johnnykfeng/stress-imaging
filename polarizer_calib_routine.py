from Devices.thorlabs_rotation_mount import RotationMount
from Devices.camera_automation import CameraAutomation
from Devices.LED_control import LEDController

# import asyncio
from pathlib import Path
import tomllib

config_path = Path(__file__).parent / "config.toml"
with open(config_path, "rb") as f:
    config = tomllib.load(f)

image_save_path = Path("C:/Code/Stress-Imaging/SAMPLE_DATA/polarizer_calib_w_CZT/")
cam = CameraAutomation()
led = LEDController()
led.set_current(800)
led.turn_on()

polarizer = RotationMount(config["polarizer_SN"], label="Polarizer", mirror=False)
analyzer = RotationMount(config["analyzer_SN"], label="Analyzer", mirror=True)

rotation_mounts = [polarizer, analyzer]
for mount in rotation_mounts:
    mount.open_device()
    mount.setup_conversion()

polarizer_angles = [0, 45, 90]
for alpha in polarizer_angles:
    polarizer.move_to_position(alpha)
    for beta in range(0, 360, 10):
        analyzer.move_to_position(beta)
        if beta == 0:
            cam.save_image_png_typewrite(f"polarizer_{alpha}_analyzer_{beta}_CZT.png", 
                                        save_path=str(image_save_path))
        else:
            cam.save_image_png_typewrite(f"polarizer_{alpha}_analyzer_{beta}_CZT.png")

### SHUTDOWN ###
led.turn_off()
for mount in rotation_mounts:
    mount.close_device()
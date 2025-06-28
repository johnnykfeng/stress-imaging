from loguru import logger
import pyautogui
import time
import numpy as np


def dont_sleep():
    pyautogui.press("win")
    pyautogui.typewrite("Don't Sleep!", interval=0.05)
    pyautogui.press("esc")


def countdown_timer(seconds, action_interval=300):
    """Countdown timer for specified seconds"""
    logger.warning("Countdown Timer: " + str(seconds) + " seconds")
    while seconds > 0:
        print(seconds, end=" ")
        print("\b" * 5, end="", flush=True)
        time.sleep(1)
        seconds -= 1
        if seconds % action_interval == 0 and seconds != 0:
            minutes = seconds // 60
            # seconds_remaining = seconds % 60
            print(f"{minutes} minutes remaining")
            pyautogui.press("win")
            pyautogui.typewrite("Don't Sleep!", interval=0.05)
            pyautogui.press("esc")


def rad_to_deg(rad):
    if rad is None:
        return None
    return rad * 180.0 / np.pi

def deg_to_rad(deg):
    if deg is None:
        return None
    return deg * np.pi / 180.0

def mirror_deg(deg):
    if deg is None:
        return None
    return 360 - deg

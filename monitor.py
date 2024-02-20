import os
import shutil
import socket
import psutil

from datetime import datetime
from time import sleep
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.emulator.device import capture
from luma.oled.device import sh1106


def ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 1))
    except OSError:
        return "N.a."

    return s.getsockname()[0]


def time() -> str:
    return datetime.now().strftime("%H:%M")


def disk_usage() -> str:
    path = '/'
    percent = shutil.disk_usage(path).free / shutil.disk_usage(path).total

    return f"{percent:.0%}"


def load_avg() -> str:
    values = os.getloadavg()

    return f"{values[0]:.2f}"


def temperature() -> str:
    sensors = psutil.sensors_temperatures()
    sensor = 'coretemp'
    if sensor not in sensors:
        sensor = 'cpu_thermal'

    coretemp = sensors[sensor][0].current

    return f"{coretemp:.0f}°C"


class Monitor:
    def __init__(self, emulator=False):
        self._font = ImageFont.truetype('DejaVuSansMono.ttf', 10)
        self._device = capture(scale=1, file_template='preview.png')

        if not emulator:
            self._device = sh1106(serial_interface=i2c(port=1, address=0x3c))

    def render(self) -> None:
        with canvas(self._device) as draw:
            text_lines = [
                f"{time()}  {ip()}",
                f"Disk free : {disk_usage()}",
                f"Load avg. : {load_avg()}",
                f"Temp.     : {temperature()}",
            ]
            draw.text((0, 0), "\n".join(text_lines), font=self._font, fill="white")

    def watch(self, interval=10) -> None:
        while True:
            self.render()
            sleep(interval)

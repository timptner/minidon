#!/usr/bin/env python3

# noinspection PyPackageRequirements
import board
import digitalio
import logging
import subprocess

from adafruit_rgb_display.st7789 import ST7789
from gpiozero import Button, CPUTemperature, OutputDevice
from PIL import Image, ImageDraw, ImageFont
from signal import pause
from threading import Thread
from time import sleep


class Screen:
    def __init__(self):
        self.backlight = OutputDevice(22)

        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None
        baudrate = 64000000
        display = ST7789(board.SPI(), cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=baudrate,
                         width=135, height=240, x_offset=53, y_offset=40)

        self._display = display

        height = display.width
        width = display.height

        self.image = Image.new('RGB', (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

        self.clear()

    def update(self):
        self._display.image(self.image, rotation=90)

    def clear(self):
        self.draw.rectangle((0, 0, self.image.width, self.image.height), fill=(0, 0, 0), outline=(0, 0, 0))
        self.update()

    def write(self, text: str, x: int = 0, y: int = 0):
        self.draw.text((x, y), text, (255, 255, 255), self.font)


class Job:
    def __init__(self):
        self.active = False
        self.thread = None

        self.screen = Screen()

        self.ip = subprocess.check_output(['hostname', '-I'], encoding='utf-8').split()[0]
        self.cpu = CPUTemperature()

    def refresh_display(self) -> None:
        while self.active:
            temp = self.cpu.temperature

            self.screen.draw.rectangle((0, 0, self.screen.image.width, self.screen.image.height), fill=(0, 0, 0), outline=(0, 0, 0))

            self.screen.write(f"IP: {self.ip}")
            self.screen.write(f"Temp.: {temp:.3f} °C", y=24)

            self.screen.update()

            sleep(1)

    def toggle_display(self):
        if self.thread is None:
            logging.info("Display activated")

            self.screen.backlight.on()

            self.active = True

            self.thread = Thread(target=self.refresh_display)
            self.thread.start()
        else:
            logging.info("Display deactivated")

            self.active = False

            self.thread.join()
            self.thread = None

            self.screen.backlight.off()


def main() -> None:
    job = Job()

    button1 = Button(23)
    button1.when_pressed = job.toggle_display

    button2 = Button(24)
    button2.when_pressed = job.toggle_display

    try:
        pause()
    except KeyboardInterrupt:
        print("\nDoing some cleanup...")
    finally:
        job.screen.clear()
        job.screen.backlight.off()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s\t%(levelname)s\t%(message)s",
        datefmt='%d-%m-%y %H:%M:%S',
    )

    main()

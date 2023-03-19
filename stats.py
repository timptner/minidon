#!/usr/bin/env python3

import subprocess
import time

from adafruit_rgb_display import st7789
from adafruit_rgb_display.rgb import color565
# noinspection PyPackageRequirements
import board
import digitalio
# noinspection PyUnresolvedReferences
# noinspection PyPackageRequirements
from gpiozero import CPUTemperature
from PIL import Image, ImageDraw, ImageFont


def main():
    # Configuration for CS and DC pins for Raspberry Pi
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)

    reset_pin = None

    baudrate = 64000000  # The pi can be very fast!

    # Create the ST7789 display:
    display = st7789.ST7789(
        board.SPI(),
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=baudrate,
        width=135,
        height=240,
        x_offset=53,
        y_offset=40,
    )

    # Swap dimensions to rotate to landscape
    height = display.width
    width = display.height

    image = Image.new('RGB', (width, height))

    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=(0, 0, 0), outline=0)

    display.image(image, rotation=90)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    cpu = CPUTemperature()

    button24 = digitalio.DigitalInOut(board.D24)
    button24.switch_to_input()

    while True:
        draw.rectangle((0, 0, width, height), fill=(0, 0, 0), outline=0)

        cmd = "hostname -I | cut -d\' \' -f1"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8')
        ip = f"IP: {result}"

        temp = f"CPU: {cpu.temperature:.3f} °C"

        x = 5
        y = 5
        draw.text((x, y), ip, (255, 255, 0), font)
        y += sum(font.getmetrics())
        draw.text((x, y), temp, (255, 0, 0), font)

        display.image(image, rotation=90)

        time.sleep(1)


if __name__ == '__main__':
    main()

import time
import board
import busio
import adafruit_ina260
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize INA260
ina260 = adafruit_ina260.INA260(i2c)

# Initialize SSD1306 OLED display
disp = adafruit_ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# Clear display
disp.fill(0)
disp.show()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Initialize drawing object
draw = ImageDraw.Draw(image)
draw.font = ImageFont.load_default()

while True:
    # Clear display
    disp.fill(0)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read sensor data
    current_mA = ina260.current
    voltage_V = ina260.voltage
    power_mW = ina260.power

    # Display data on OLED
    draw.text((0, 0), f"Current: {current_mA:.2f} mA", font=draw.font, fill=255)
    draw.text((0, 10), f"Voltage: {voltage_V:.2f} V", font=draw.font, fill=255)
    draw.text((0, 20), f"Power: {power_mW:.2f} mW", font=draw.font, fill=255)

    # Display image
    disp.image(image)
    disp.show()

    # Delay before refreshing
    time.sleep(0.5)

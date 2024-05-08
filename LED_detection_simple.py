import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

start_time = time.time()
led_detected_count = 0
try: 
    while time.time() - start_time < 10:
        camera.capture(rawCapture, format="rgb")
        image = rawCapture.array
        image = Image.fromarray(image)
        brightness = image.convert("L")
        max_brightness = brightness.getextrema()[1]
        print(max_brightness)
        if max_brightness > 256:
            print("LED detected")
            led_detected_count += 1
            if led_detected_count == 5:
                break
        else:
            print("LED not detected")
        time.sleep(0.5)
        rawCapture.truncate(0)
finally:
    rawCapture.truncate(0)
    print("Programmet har avslutats.")

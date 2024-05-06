import time
import picamera
import numpy as np
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO

def detect_led():

    # Initialisera kameran
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        rawCapture = PiRGBArray(camera, size=(640, 480))

        # Vänta på att kameran ska starta
        time.sleep(0.1)

        # Starta tidtagning
        start_time = time.time()

        # Räkna antal gånger LED har detekterats
        led_detected_count = 0

        # Loopa över bilderna från kameran
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # Hämta bildmatrisen från bildbufferten
            image = frame.array

            # Beräkna medelvärdet av röd, grönt och blått i bilden
            mean_color = np.mean(image, axis=(0, 1))

            # Om medelvärdet av röd och grönt är högre än 100, antas det att LED är tänd
            if mean_color[0] > 100 and mean_color[1] > 100:
                print("LED detekterad")
                led_detected_count += 1
            else:
                print("LED ej detekterad")

            # Rensa bildbufferten för nästa bild
            rawCapture.truncate(0)

            # Avsluta om 10 sekunder har gått eller om LED har detekterats 5 gånger i rad
            if time.time() - start_time > 10 or led_detected_count >= 5:
                break

            # Vänta en sekund
            time.sleep(1)

    # Återställ GPIO-inställningar
    GPIO.cleanup()

# Testa funktionen
detect_led()

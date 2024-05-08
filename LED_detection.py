#import cv2
import time
import numpy as np

# Ladda in Pi Camera modulen
from picamera.array import PiRGBArray
from picamera import PiCamera

# Skapa en instans av PiCamera och PiRGBArray
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Vänta på att kameran ska initialiseras
time.sleep(0.1)

try:
    while True:
        # Ta en bild
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array

        # Här kan du lägga till din LED-detekteringskod
        # Om en LED detekteras, skriv ut "LED detected"
        # Annars, skriv ut "LED not detected"
        # Vi antar att en LED kommer att vara mycket ljusare än bakgrunden.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            print("LED detected")
        else:
            print("LED not detected")

        # Visa bilden
        cv2.imshow("Image", image)

        # Vänta i 5 sekunder
        time.sleep(5)

        # Om 'q' trycks, avsluta loopen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Rensa strömmen för nästa bild
        rawCapture.truncate(0)

finally:
    # Stäng alla OpenCV-fönster
    cv2.destroyAllWindows()

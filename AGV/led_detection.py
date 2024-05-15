import time
import numpy as np
import cv2
import os
from picamera2 import Picamera2
import RPi.GPIO as GPIO

os.environ["LIBCAMERA_LOG_LEVELS"] = "3"  # Ställer in loggningsnivån för libcamera till ERROR


# ------------------------- LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT) # LED lyslampa
# Sätt av och på LED lampan 
def LED_light(light): 
        if light: 
            GPIO.output(8, GPIO.HIGH) 
        else: 
            GPIO.output(8, GPIO.LOW)


def LED_detect():
    led_detected_count = 0

    start_time = time.time()
    done = False
    try:
        with Picamera2() as camera:
            camera_config = camera.create_still_configuration({"size":(640*2, 480*2)})
            camera.configure(camera_config)
            camera.start()
            LED_light(True)
            time.sleep(1)
            LED_light(False)
            while time.time() - start_time < 10 and not done:
                frame = camera.capture_array()  # Fångar en bild från kameran
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Konverterar bilden till gråskala
                _, threshold = cv2.threshold(gray, 253, 270, cv2.THRESH_BINARY)  # Applicerar en tröskel på den gråskalade bilden
                contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Hittar konturer i den trösklade bilden
                for cnt in contours:
                    area = cv2.contourArea(cnt)  # Beräknar arean av konturen
                    if area > 350:  # Om arean är större än 350
                        x, y, w, h = cv2.boundingRect(cnt)  # Beräknar en bounding box runt konturen
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Ritar bounding boxen på bilden
                        if w/h > 0.95 and w/h < 1.05:  # Om förhållandet mellan bredden och höjden på bounding boxen är nära 1
                            led_detected_count += 1  # Ökar räknaren för detekterade LED-lampor
                            if led_detected_count == 2:  # Om två LED-lampor har detekterats
                                print("Two LEDs detected")
                                done = True
                                LED_light(False)
                                return "LED detected"
                                break
                            elif led_detected_count == 1:  # Om två LED-lampor har detekterats
                                print("One LEDs detected")
                                done = True
                                LED_light(False)
                                return "LED detected"
                                break
                                #raise LedDetectedException  # Kastar ett undantag för att avsluta programmet
                #cv2.imshow('Camera View', frame)  # Visar bilden med bounding boxarna
                #if cv2.waitKey(1) & 0xFF == ord('q'):  # Om 'q' trycks ner
                    #break  # Avbryter loopen
                time.sleep(0.1)  # Väntar i 0.1 sekunder
    except:
        print("Two LEDs detected, exiting program.")
    finally:
        LED_light(False)
        return "Time out"
        #cv2.destroyAllWindows()  # Stänger alla öppna fönster
        print("Programmet har avslutats.")
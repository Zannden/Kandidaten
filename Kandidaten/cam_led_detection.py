import time
from PIL import Image
from picamera import PiCamera

def count_pixels_above_threshold(image, threshold):
    # Konvertera bilden till gråskala
    grayscale_image = image.convert('L')

    # Räkna antalet pixlar över tröskelvärdet
    above_threshold_count = 0
    for pixel_value in grayscale_image.getdata():
        if pixel_value > threshold:
            above_threshold_count += 1

    return above_threshold_count

def detect_leds(image, threshold):
    # Räkna antalet pixlar över tröskelvärdet för varje LED
    # Här kan du anpassa pixeltröskelvärdet för att passa dina LED-lampor
    pixel_count_led1 = count_pixels_above_threshold(image, threshold)
    pixel_count_led2 = count_pixels_above_threshold(image, threshold)

    # Returnera True om antalet pixlar över tröskelvärdet är signifikant för båda LED-lamporna
    return pixel_count_led1 > 100 and pixel_count_led2 > 100

def capture_and_detect():
    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)  

        while True:
            # Ta en bild
            image_path = 'temp.jpg'
            camera.capture(image_path)

            # Öppna bilden
            image = Image.open(image_path)

            # Detektera LED-lampor i bilden
            if detect_leds(image, threshold=200):
                print("Båda LED-lamporna har detekterats!")

            # Kort väntetid mellan bilderna
            time.sleep(0.1)

# Anropa funktionen för att starta detektionen
capture_and_detect()

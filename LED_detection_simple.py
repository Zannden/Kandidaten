import time
# Importerar time-modulen som tillhandahåller funktioner för att arbeta med tid

from picamera.array import PiRGBArray
# PiRGBArray används för att lagra bilderna som tas av kameran i RGB-format

from picamera import PiCamera
# PiCamera används för att interagera med kameran på Raspberry Pi

from PIL import Image
# Importerar Image från PIL (Python Imaging Library), ett bibliotek för att hantera bilder

camera = PiCamera()
rawCapture = PiRGBArray(camera)
# Skapar en instans av PiCamera och PiRGBArray. PiRGBArray tar camera som argument,
# vilket innebär att den kommer att lagra bilderna som tas av camera

time.sleep(0.1)
# Pausar programmet i 0.1 sekunder. Detta ger kameran tid att starta och justera ljusnivåerna

try: 
    while True:
# Startar en oändlig loop. try-blocket används för att hantera eventuella fel som kan uppstå under programmets körning
      
        camera.capture(rawCapture, format="rgb")
        image = rawCapture.array
        # Tar en bild med kameran i RGB-format och lagrar den i rawCapture.
        # Bilden konverteras sedan till en numpy-array och lagras i image
      
        image = Image.fromarray(image)
        # Konverterar numpy-arrayen till en PIL Image-objekt
    
        brightness = image.convert("L")
        max_brightness = brightness.getextrema()[1]
        print(max_brightness)
        if max_brightness > 256:
            print("LED detected")
        else:
            print("LED not detected")
        # Konverterar bilden till gråskala (L) och beräknar den maximala ljusstyrkan i bilden.
        # Om den maximala ljusstyrkan är större än 250, antas det att en LED har detekterats
    
        time.sleep(5)
        # Pausar programmet i 5 sekunder innan nästa bild tas
    
        rawCapture.truncate(0)
        # Rensar rawCapture för att förbereda för nästa bild
finally:
    print("Programmet har avslutats.")
# När loopen avbryts (till exempel genom ett tangentbordsavbrott),
# skrivs “Programmet har avslutats.” ut. finally-blocket körs oavsett om ett undantag uppstår eller inte
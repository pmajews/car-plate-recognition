import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import requests

reader = SimpleMFRC522()

try:
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)
    id = reader.read()
    GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(16, GPIO.HIGH)

    a = input("Choose photo from 1 to 10: ")

    if a == '1':
        img = cv2.imread('img1.jpg',cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '2':
        img = cv2.imread('img2.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '3':
        img = cv2.imread('img3.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '4':
        img = cv2.imread('img4.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '5':
        img = cv2.imread('img5.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '6':
        img = cv2.imread('img6.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '7':
        img = cv2.imread('img7.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '8':
        img = cv2.imread('img8.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '9':
        img = cv2.imread('img9.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))
    elif a == '10':
        img = cv2.imread('img10.jpg', cv2.IMREAD_COLOR)
        img = cv2.resize(img, (620, 480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in cnts:
     peri = cv2.arcLength(c, True)
     approx = cv2.approxPolyDP(c, 0.018 * peri, True)


     if len(approx) == 4:
      screenCnt = approx
      break




    if screenCnt is None:
     detected = 0
     print("No contour detected")

    else:
     detected = 1

    if detected == 1:
     cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv2.bitwise_and(img,img,mask=mask)


    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]


    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    print("Detected Number is:",text)
    requests.post('https://plateproject.azurewebsites.net/api/create', json={"plate": text})
    cv2.imshow('image',img)
    cv2.imshow('Cropped',Cropped)
    GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(37, GPIO.HIGH)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

finally:
    GPIO.cleanup()






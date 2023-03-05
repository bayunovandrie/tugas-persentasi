from HandTrackingModule import HandDetector
import cv2 
import os
import pyttsx3
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

folder_path = "File"
widthCam, heightCam = int(213*1), int(150*1)

cam = cv2.VideoCapture(0)
cam.set(3, widthCam)
cam.set(4, heightCam)
detector = HandDetector(maxHands=1, detectionCon=0.5)

gambar = os.listdir(folder_path)
gambar_number = 0

button_pressed = False
button_Counter = 0 
button_delay = 10

# engine.say("hello everyone, my name is alice.")
engine.say("Open slide!")
engine.runAndWait()
while True:
    # untuk kamera
    success, frame = cam.read()
    frame = cv2.flip(frame, 1)
    
    # untuk gambar
    full_img = os.path.join(folder_path, gambar[gambar_number])
    img_current = cv2.imread(full_img)

    scale_percent = 70
    width = int(img_current.shape[1] * scale_percent / 100)
    height = int(img_current.shape[0] * scale_percent / 100)
    dim = (width, height)

    # deteksi tangan
    hands, frame = detector.findHands(frame, flipType=False)


    if hands and button_pressed is False:
        hand = hands[0]
        jari = detector.fingersUp(hand)
        lmList = hand['lmList']

        if jari == [0,1,0,0,0]:
            if gambar_number > 0:
                button_pressed = True
                gambar_number -= 1

        if jari == [0,0,0,0,1]:

            if gambar_number < len(gambar)-1:
                button_pressed = True
                gambar_number += 1

    if button_pressed:
        button_Counter += 1

        if button_Counter > button_delay:
            button_Counter = 0
            button_pressed = False

    
    small_gambar = cv2.resize(frame, (widthCam, heightCam))
    h, w, _ = img_current.shape
    img_current[0:heightCam, w-widthCam:w] = small_gambar

    img_current = cv2.resize(img_current, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow('web', frame)
    cv2.imshow('slide', img_current)

    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:
        break

engine.say("persentation is done,, thanks for your attention!!!, close slide. bye")
engine.runAndWait()
# Import required packages
import sys
import glob
import numpy as np 
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\3479226\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Read image
path = glob.glob("./media/*.png")
for imgPath in path:

    img = cv2.imread(imgPath)

    # (Single-screen Screenshot)
    # Resize
    rw=1920
    rh=1030
    # Crop 
    cx=1500
    cy=950
    cw=300 
    ch=100
    # (Dual-screen Screenshot)
    
    if (len(img[0])/len(img))>2.5:
        # Resize
        rw=3520
        rh=1080
        # Crop 
        cx=1400
        cy=950
        cw=400 
        ch=100

    # Print Image Name
    # Get String after substring occurrence
    splitString = imgPath.split("\\")
    imgName = splitString[-1]
    print(imgName)

    # Preprocessing
    img = cv2.resize(img, (rw,rh))
    img = img[cy:cy+ch, cx:cx+cw]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilate = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, 
                                                    cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()
    
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        if cv2.contourArea(cnt)>2000:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = im2[y:y + h, x:x + w]
            
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped)
            
            # Print Result Text
            print(text)

    # cv2.imshow('norm',rect)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()    
import time
import cv2
import numpy as np
import imutils
import easyocr

captura = cv2.VideoCapture(0)
reader = easyocr.Reader(['en'])
# lastExecution = time.time();

def getCroppedFrame(frame, gray, location):
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(frame, frame, mask=mask)

        # Crop new image
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    return cropped_image

while(1):
    ret, frame = captura.read()
    # cv2.imshow("Video", frame)

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    cv2.imshow("Video", edged)

    # if time.time() - lastExecution < 5:
    #   continue
    
    # lastExecution = time.time()

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
      location = cv2.approxPolyDP(contour, 10, True)

      if len(location) == 4: # License plate has 4 corners
        cropped_frame = getCroppedFrame(frame, gray, location)

        result = reader.readtext(cropped_frame)

        if len(result) == 0 or len(result[0]) < 2:
          continue

        text = ''
        if len(result) > 0:
            text = result[0][-2]

        print(text)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
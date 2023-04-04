import os
import cv2
import imutils
import numpy as np


# importing, identifying and editing the image
def find_marker(image):
    # convert image to grayscale, blur it and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)

    # identifying the image (the largest contour)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # compute the bounding box of the paper region and return it
    return  cv2.mainAreaReact(c)


# the end goal of computing distance to camera
def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth


KNOWN_DISTANCE = 24
KNOWN_WIDTH = 8.3
folder = 'photos'
lst = []


# reading all images in a directory and calculating focal length
for images in os.listdir(folder):
    img = cv2.imread(images)  # image read
    marker = find_marker(img)  # detect the object
    temp_focal_length = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH  # calculate focal lenght from that one image
    lst.append(temp_focal_length)  # put it an empty list to average it
focalLength = sum(lst) / len(lst)  # computing the average

# now loop over all images
for pictures in os.listdir(folder):
    image = cv2.imread(pictures)
    marker = find_marker(pictures)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[0][1])

    # draw a bounding box around the image and display it
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    cv2.putText(image, "%.2fft" % (inches / 12),
                (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
    cv2.imshow("image", image)
    cv2.waitKey(0)




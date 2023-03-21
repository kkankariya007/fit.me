import cv2
import numpy as np

img = cv2.imread('manu.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 200)
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_contour = max(contours, key=cv2.contourArea)

ellipse = cv2.fitEllipse(max_contour)

img= cv2.ellipse(img, ellipse, (0, 255, 0), 2)

waist_circumference = np.pi * (ellipse[1][0] + ellipse[1][1]) / 2

cv2.imshow('image', cv2.resize(img,(1300,720)))
print('Waist size:', waist_circumference)

cv2.waitKey(0)
cv2.destroyAllWindows()

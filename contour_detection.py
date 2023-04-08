#Code has been compiled on google colab, it might cause issues while running on jupyter or pycharm

#import libraries
import cv2
from google.colab.patches import cv2_imshow
image = cv2.imread("/content/drive/MyDrive/Colab Notebooks/Fashion/Clothes_images/white_shirt.jpg")

#Convert the image into a binary image. We can use thresholding or edge detection. We will be using the Canny edge detector.
#Find the contours using the cv2.findContours function.
#Draw the contours on the image using the cv2.drawContours function.

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blurred, 10, 100)

cv2_imshow(image)
cv2_imshow(edged)
cv2.waitKey(0)

# find the contours in the edged image
#The first argument is the name of the binary image
#The second argument is the contour retrieval mode. By using cv2.RETR_EXTERNAL we only retrieve the outer contours of the objects on the image. See RetrievalModes for other possible options.
#The third argument to this function is the contour approximation method. In our case we used cv2.CHAIN_APPROX_SIMPLE, which will compress horizontal, vertical, and diagonal segments to keep only their end points. 
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# draw the contours on a copy of the original image
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
print(len(contours), "objects were found in this image.")

cv2_imshow(edged)
cv2_imshow(image_copy)
cv2.waitKey(0)

# define a (3, 3) structuring element
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# apply the dilation operation to the edged image
dilate = cv2.dilate(edged, kernel, iterations=1)

# find the contours in the dilated image
contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# draw the contours on a copy of the original image
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
print(len(contours), "objects were found in this image.")

cv2_imshow( dilate)
cv2_imshow(image_copy)
cv2.waitKey(0)

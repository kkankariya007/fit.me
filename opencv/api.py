import cv2
print(cv2.__version__)

''' first detect the tshirt color 
    then type of clothing , shirt , tshirt , top etc etc'''\
    
img_grayscale = cv2.imread(r'.\opencv\test.jpg' , 0)

cv2.imshow('grayscale image', img_grayscale)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('grayscale.jpg' , img_grayscale)
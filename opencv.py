import cv2.cv2 as cv2
import numpy as np

base_image_color = cv2.imread('image-items/base_image.png', 1)
base_image = cv2.imread('image-items/base_image.png', 0)
template_image = cv2.imread('image-items/athanor', 0)
h, w = template_image.shape


tmp_image = base_image.copy()
np_image = np.array(tmp_image)
# result = cv2.matchTemplate(np_image, template_image, cv2.TM_CCOEFF)
result = cv2.matchTemplate(tmp_image, template_image, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
location = max_loc
bottom_right = (location[0] + w, location[1] + h)
cv2.rectangle(base_image_color, location, bottom_right, 255, 2)
cv2.imshow('Match', base_image_color)
cv2.waitKey(0)
cv2.destroyAllWindows()

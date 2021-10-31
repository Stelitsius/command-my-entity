import pyautogui
import time
from cv2 import cv2

time.sleep(1)
image = cv2.imread("test.png", cv2.IMREAD_UNCHANGED)  # 1920x1080
new_image = None
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_color = (0, 255, 255)
line_type = 3
thickness = 2


for i in range(5):

    i = i + 1
    bottom_left = (i * 200 - 10, i * 200 - 10)
    new_image = cv2.putText(image, str(i),
                            bottom_left,
                            font,
                            font_scale,
                            font_color,
                            thickness,
                            line_type,
                            False)

cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("image", cv2.WND_PROP_TOPMOST, 1)
cv2.imshow("image", new_image)
pyautogui.click()
cv2.waitKey(0)

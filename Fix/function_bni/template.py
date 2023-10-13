import cv2 as cv

threshold_binary = 128

# Templat pertama
template_path = "image\data_bni\data_540x1200.jpeg"
template_rgb_1 = cv.imread(template_path)
template_gray_1 = cv.cvtColor(template_rgb_1, cv.COLOR_RGB2GRAY)
_, binary_template_1 = cv.threshold(template_gray_1, threshold_binary, 255, cv.THRESH_BINARY)

# Templat kedua
template_path_2 = "image\data_bni\data_720x1600.jpg"
template_rgb_2 = cv.imread(template_path_2)
template_gray_2 = cv.cvtColor(template_rgb_2, cv.COLOR_RGB2GRAY)
_, binary_template_2 = cv.threshold(template_gray_2, threshold_binary, 255, cv.THRESH_BINARY)

import cv2 as cv

threshold_binary = 128

# Templat pertama
template_path = "image\data_btn\data_540x371.jpg"
template_rgb_1 = cv.imread(template_path)
template_gray_1 = cv.cvtColor(template_rgb_1, cv.COLOR_RGB2GRAY)
_, binary_template_1 = cv.threshold(template_gray_1, threshold_binary, 255, cv.THRESH_BINARY)

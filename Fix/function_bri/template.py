import cv2 as cv

threshold_binary = 128

# Templat pertama
template_path = "image\data_bri\data_720x1600.jpg"
template_rgb_1 = cv.imread(template_path)
template_gray_1 = cv.cvtColor(template_rgb_1, cv.COLOR_RGB2GRAY)
_, binary_template_1 = cv.threshold(template_gray_1, threshold_binary, 255, cv.THRESH_BINARY)

# Templat kedua
template_path_2 = "image\data_bni\data_720x1600.jpg"
template_rgb_2 = cv.imread(template_path_2)
template_gray_2 = cv.cvtColor(template_rgb_2, cv.COLOR_RGB2GRAY)
_, binary_template_2 = cv.threshold(template_gray_2, threshold_binary, 255, cv.THRESH_BINARY)

# Templat ketiga
template_path_3 = "image\data_bni\data_738x1600.jpeg"
template_rgb_3 = cv.imread(template_path_3)
template_gray_3 = cv.cvtColor(template_rgb_3, cv.COLOR_RGB2GRAY)
_, binary_template_3 = cv.threshold(template_gray_3, threshold_binary, 255, cv.THRESH_BINARY)

# Templat keempat
template_path_4 = "image\data_bni\data_900x1600.jpg"
template_rgb_4 = cv.imread(template_path_4)
template_gray_4 = cv.cvtColor(template_rgb_4, cv.COLOR_RGB2GRAY)
_, binary_template_4 = cv.threshold(template_gray_4, threshold_binary, 255, cv.THRESH_BINARY)

# Templat kelima
template_path_5 = "image\data_bni\data_606x1280.jpg"
template_rgb_5 = cv.imread(template_path_5)
template_gray_5 = cv.cvtColor(template_rgb_5, cv.COLOR_RGB2GRAY)
_, binary_template_5 = cv.threshold(template_gray_5, threshold_binary, 255, cv.THRESH_BINARY)

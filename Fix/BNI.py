import cv2 as cv
import numpy as np
import streamlit as st
import Fix.function_bni.template as tp  
from Fix.function_bni.print import print
from Fix.function_bni.ocr import perform_ocr
from Fix.function_bni.nms import non_max_suppression

# POI (Point Of Interest)
def crop_image(image, start_x, start_y, end_x, end_y):
    # Memotong citra berdasarkan koordinat yang diberikan
    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image

def run_app():
    st.title("BNI Project")
    # Mengunggah citra dan template
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    threshold = 0.8
    threshold_luminosity = 128
    threshold_nms = 0.8

    button_ok = st.button("Run")

    if button_ok and uploaded_image is not None :

        # Membaca citra yang diunggah
        image_rgb = cv.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
        # Mendapatkan dimensi citra
        height, width, _ = image_rgb.shape
        # Inisialisasi citra grayscale
        image_gray = np.zeros((height, width), dtype=np.uint8)
        # Mengonversi citra RGB ke grayscale dengan rumus yang diberikan
        for y in range(height):
            for x in range(width):
                r, g, b = image_rgb[y, x]
                gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
                image_gray[y, x] = gray_value
        _, image_gray = cv.threshold(image_gray, threshold_luminosity, 255, cv.THRESH_BINARY)

        table_df = None
    
        if height == 1200 and width == 540:
            result = cv.matchTemplate(image_gray, tp.binary_template_1, cv.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            boxes = np.column_stack((loc[1], loc[0], loc[1] + tp.template_gray_1.shape[1], loc[0] + tp.template_gray_1.shape[0]))
            selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)
    
            if len(selected_boxes) == 0:
                st.write("Gambar bukan mutasi M-banking BNI")
            else:
                x1, y1, x2, y2 = selected_boxes[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)
    
        elif height == 1600 and width == 720:
            result = cv.matchTemplate(image_gray, tp.binary_template_2, cv.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            boxes = np.column_stack((loc[1], loc[0], loc[1] + tp.template_gray_2.shape[1], loc[0] + tp.template_gray_2.shape[0]))
            selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)
    
            if len(selected_boxes) == 0:
                st.write("Gambar bukan mutasi M-banking BNI")
            else:
                x1, y1, x2, y2 = selected_boxes[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)
        
        elif height == 1600 and 740 >= width >= 738:
            result = cv.matchTemplate(image_gray, tp.binary_template_3, cv.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            boxes = np.column_stack((loc[1], loc[0], loc[1] + tp.template_gray_3.shape[1], loc[0] + tp.template_gray_3.shape[0]))
            selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)
    
            if len(selected_boxes) == 0:
                st.write("Gambar bukan mutasi M-banking BNI")
            else:
                x1, y1, x2, y2 = selected_boxes[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)
        
        elif height == 1600 and width == 900:
            result = cv.matchTemplate(image_gray, tp.binary_template_4, cv.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            boxes = np.column_stack((loc[1], loc[0], loc[1] + tp.template_gray_4.shape[1], loc[0] + tp.template_gray_4.shape[0]))
            selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)
    
            if len(selected_boxes) == 0:
                st.write("Gambar bukan mutasi M-banking BNI")
            else:
                x1, y1, x2, y2 = selected_boxes[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)
        
        elif height == 1280 and width == 606:
            result = cv.matchTemplate(image_gray, tp.binary_template_5, cv.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            boxes = np.column_stack((loc[1], loc[0], loc[1] + tp.template_gray_5.shape[1], loc[0] + tp.template_gray_5.shape[0]))
            selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)
    
            if len(selected_boxes) == 0:
                st.write("Gambar bukan mutasi M-banking BNI")
            else:
                x1, y1, x2, y2 = selected_boxes[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)

        else:
            st.write("Resolusi tidak terdeteksi dengan template")

        if table_df is not None and not table_df.empty:
            print(table_df)
        else :
            return False
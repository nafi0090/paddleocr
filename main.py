import time
import cv2 as cv
import numpy as np
import streamlit as st

import Fix.function_bni.template as bni_tp
from Fix.function_bni.print import print as bni_print
from Fix.function_bni.ocr import perform_ocr as bni_perform_ocr
from Fix.function_bni.nms import non_max_suppression as bni_non_max_suppression

import Fix.function_bri.template as bri_tp
from Fix.function_bri.print import print as bri_print
from Fix.function_bri.ocr import perform_ocr as bri_perform_ocr
from Fix.function_bri.nms import non_max_suppression as bri_non_max_suppression

import Fix.function_btn.template as btn_tp
from Fix.function_btn.print import print as btn_print
from Fix.function_btn.ocr import perform_ocr as btn_perform_ocr
from Fix.function_btn.nms import non_max_suppression as btn_non_max_suppression

start_time_1 = time.time()
start_time_2 = time.time()

def process_image_bank(image_rgb, bank=None):
    image_rgb = cv.imdecode(np.frombuffer(image_rgb.read(), np.uint8), 1)

    threshold = 0.8
    threshold_luminosity = 128
    threshold_nms = 0.8

    height, width, _ = image_rgb.shape
    image_gray = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r, g, b = image_rgb[y, x]
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            image_gray[y, x] = gray_value

    _, image_gray = cv.threshold(image_gray, threshold_luminosity, 255, cv.THRESH_BINARY)

    table_df = None
    bni_found = False
    bri_found = False
    btn_found = False

    #  ================================================================= BNI templates ================================================================= 
    if height == 1200 and width == 540 and not bni_found:
        result = cv.matchTemplate(image_gray, bni_tp.binary_template_1, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bni_tp.template_gray_1.shape[1], loc[0] + bni_tp.template_gray_1.shape[0]))
        selected_boxes = bni_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            table_df= bni_perform_ocr(image_rgb)
            
            st.table(table_df)
            # st.write(total_nominal)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bni_print(table_df)

        bni_found = True
    
    elif height == 1600 and width == 720 and not bni_found:
        result = cv.matchTemplate(image_gray, bni_tp.binary_template_2, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bni_tp.template_gray_2.shape[1], loc[0] + bni_tp.template_gray_2.shape[0]))
        selected_boxes = bni_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            table_df = bni_perform_ocr(image_rgb)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bni_print(table_df)

        bni_found = True
    
    elif height == 1600 and 740 >= width >= 738:
        result = cv.matchTemplate(image_gray, bni_tp.binary_template_3, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bni_tp.template_gray_3.shape[1], loc[0] + bni_tp.template_gray_3.shape[0]))
        selected_boxes = bni_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("Gambar bukan mutasi M-banking BNI")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
            
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            table_df = bni_perform_ocr(image_rgb)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bni_print(table_df)

        bni_found = True

    elif height == 1600 and width == 900:
        result = cv.matchTemplate(image_gray, bni_tp.binary_template_4, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bni_tp.template_gray_4.shape[1], loc[0] + bni_tp.template_gray_4.shape[0]))
        selected_boxes = bni_non_max_suppression(boxes, result[loc], threshold_nms)
    
        if len(selected_boxes) == 0:
            st.write("Gambar bukan mutasi M-banking BNI")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))

            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            table_df = bni_perform_ocr(image_rgb)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))
            
            bni_print(table_df)
        
        bni_found = True

    elif height == 1280 and width == 606:
        result = cv.matchTemplate(image_gray, bni_tp.binary_template_5, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bni_tp.template_gray_5.shape[1], loc[0] + bni_tp.template_gray_5.shape[0]))
        selected_boxes = bni_non_max_suppression(boxes, result[loc], threshold_nms)
    
        if len(selected_boxes) == 0:
            st.write("Gambar bukan mutasi M-banking BNI")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            table_df = bni_perform_ocr(image_rgb)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bni_print(table_df)

        bni_found = True

    #  ================================================================= BRI Template ================================================================= 
    if height == 1600 and width == 720 and not bri_found:
        result = cv.matchTemplate(image_gray, bri_tp.binary_template_1, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bri_tp.template_gray_1.shape[1], loc[0] + bri_tp.template_gray_1.shape[0]))
        selected_boxes = bri_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb_crop = image_rgb[y1:, x1:]
            table_df = bri_perform_ocr(image_rgb_crop)

            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bri_print(table_df)

        bri_found = True

    elif height == 1480 and width == 720 and not bri_found:
        result = cv.matchTemplate(image_gray, bri_tp.binary_template_2, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + bri_tp.template_gray_2.shape[1], loc[0] + bri_tp.template_gray_2.shape[0]))
        selected_boxes = bri_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb_crop = image_rgb[y1:, x1:]
            table_df = bri_perform_ocr(image_rgb_crop)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            bri_print(table_df)

        bri_found = True

    # ================================================================= BTN Template =================================================================
    if height == 471 and width == 530 and not btn_found:
        result = cv.matchTemplate(image_gray, btn_tp.binary_template_1, cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + btn_tp.template_gray_1.shape[1], loc[0] + btn_tp.template_gray_1.shape[0]))
        selected_boxes = btn_non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("")
        else:
            # end_time_1 = time.time()
            # processing_time_1 = end_time_1 - start_time_1
            # st.write(str(processing_time_1))
        
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb_crop = image_rgb[y1:, x1:]
            table_df = btn_perform_ocr(image_rgb_crop)
            
            st.table(table_df)
            # end_time = time.time()
            # processing_time_2 = end_time - start_time_2
            # st.write(str(processing_time_2))

            btn_print(table_df)
            

        btn_found = True
    
    # ================================================================= UnDetected Image Files ================================================================= 
    if not (bni_found or bri_found or btn_found):
        st.write("Tidak terdeteksi template bank yang sesuai")

st.title("Banking Projects")

uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
button_ok = st.button("Run")

if button_ok and uploaded_image is not None:
    process_image_bank(uploaded_image)
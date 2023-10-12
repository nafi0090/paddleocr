import io
import pandas as pd
import cv2 as cv
import numpy as np
import streamlit as st
from Fix.function_bni.ocr import perform_ocr
from Fix.function_bni.nms import non_max_suppression

def crop_image(image, start_x, start_y, end_x, end_y):
    # Memotong citra berdasarkan koordinat yang diberikan
    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image

def run_app():
    st.title("BNI App")
    # Mengunggah citra dan template
    uploaded_image = st.file_uploader("Unggah citra", type=["jpg", "jpeg", "png"])
    template_path = "image\data_bni\data_540x1200.jpeg"
    template_path_2 = "image\data_bni\data_720x1600.jpg"

    threshold = 0.1
    threshold_luminosity = 128
    threshold_binary = 128
    threshold_nms = 0.8

    button_ok = st.button("Run")

    if button_ok and uploaded_image is not None :
        # Membaca citra dan template yang diunggah
        image_rgb = cv.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
        template_rgb = cv.imread(template_path)
        template_rgb_2 = cv.imread(template_path_2)

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
        template_gray = cv.cvtColor(template_rgb, cv.COLOR_RGB2GRAY)
        template_gray_2 = cv.cvtColor(template_rgb_2, cv.COLOR_RGB2GRAY)
        
        _, binary_image = cv.threshold(image_gray, threshold_binary, 255, cv.THRESH_BINARY)
        _, binary_template = cv.threshold(template_gray, threshold_binary, 255, cv.THRESH_BINARY)
        _, binary_template_2 = cv.threshold(template_gray_2, threshold_binary, 255, cv.THRESH_BINARY)

        # Periksa ukuran gambar dan templat
        image_height, image_width = binary_image.shape
        template_height, template_width = binary_template.shape
        template_height_2, template_width_2 = binary_template_2.shape

        # Resize gambar jika ukuran lebih kecil daripada templat
        if image_height < template_height or image_width < template_width:
            binary_template = cv.resize(image_gray, (template_width, template_height))
        
        if image_height < template_height_2 or image_width < template_width_2:
            binary_template_2 = cv.resize(image_gray, (template_width_2, template_height_2))

        # result = match_template(image_gray, template_gray)
        result = cv.matchTemplate(binary_image, binary_template ,cv.TM_CCOEFF_NORMED)
        result_2 = cv.matchTemplate(binary_image, binary_template_2 ,cv.TM_CCOEFF_NORMED)

        loc_1 = np.where(result >= threshold)
        loc_2 = np.where(result_2 >= threshold)

        boxes_1 = np.column_stack((loc_1[1], loc_1[0], loc_1[1] + template_gray.shape[1], loc_1[0] + template_gray.shape[0]))
        boxes_2 = np.column_stack((loc_2[1], loc_2[0], loc_2[1] + template_gray_2.shape[1], loc_2[0] + template_gray_2.shape[0]))

        selected_boxes_1 = non_max_suppression(boxes_1, result[loc_1], threshold_nms)
        selected_boxes_2 = non_max_suppression(boxes_2, result_2[loc_2], threshold_nms)

        # loc = np.where(result >= threshold)
        # boxes = np.column_stack((loc[1], loc[0], loc[1] + template_gray.shape[1], loc[0] + template_gray.shape[0]))

        # selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes_1) == 0 and len(selected_boxes_2) == 0:
            st.write("Gambar tidak sesuai dengan template yang disediakan")
        else:
            if len(selected_boxes_1) > 0:
                st.write("ini gambar template 540 x 1200")
                x1, y1, x2, y2 = selected_boxes_1[0]
                image_rgb = image_rgb[y1:, x1:]

                table_df = perform_ocr(image_rgb)

                st.table(table_df)
            if len (selected_boxes_2) > 0:
                st.write("ini gambar template 729 x 100")
                x1, y1, x2, y2 = selected_boxes_1[0]
                image_rgb = image_rgb[y1:, x1:]
                table_df = perform_ocr(image_rgb)
                st.table(table_df)
            
            st.markdown('### Unduh Tabel dalam Format Excel')

            # Buat objek BytesIO untuk menyimpan file Excel
            excel_buffer = io.BytesIO()

            # Tulis DataFrame ke dalam objek BytesIO sebagai file Excel
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter', mode='xlsx', options={'remove_timezone': True}) as writer:
                table_df.to_excel(writer, sheet_name='Sheet1', index=False)

            # Unduh data Excel
            excel_buffer.seek(0)
            st.download_button(
                label="Unduh Data dalam Format Excel",
                data=excel_buffer,
                file_name='data.xlsx',  # Nama file yang akan diunduh
                key='excel-download'
            )
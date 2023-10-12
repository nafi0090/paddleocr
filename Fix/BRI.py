import io
import cv2 as cv
import numpy as np
import pandas as pd
import streamlit as st
from Fix.function_bri.nms import non_max_suppression
from Fix.function_bri.ocr import perform_ocr

def crop_image(image, start_x, start_y, end_x, end_y):
    # Memotong citra berdasarkan koordinat yang diberikan
    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image

def run_app():
    st.title("BRI Project")
    # Mengunggah citra dan template
    uploaded_image = st.file_uploader("Unggah citra", type=["jpg", "jpeg", "png"])
    uploaded_template = "image\data_bri\data_720x1600.jpg"

    threshold = 0.1
    threshold_luminosity = 128
    threshold_binary = 128
    threshold_nms = 0.8

    button_ok = st.button("Run")

    if button_ok and uploaded_image is not None and uploaded_template is not None:
        image_rgb = cv.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
        template_rgb = cv.imread(uploaded_template)

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
        
        _, binary_image = cv.threshold(image_gray, threshold_binary, 255, cv.THRESH_BINARY)
        _, binary_template = cv.threshold(template_gray, threshold_binary, 255, cv.THRESH_BINARY)

        # Periksa ukuran gambar dan templat
        # image_height, image_width = image_gray.shape
        # template_height, template_width = template_gray.shape

        # Resize gambar jika ukuran lebih kecil daripada templat
        # if image_height < template_height or image_width < template_width:
        #     image_gray = cv.resize(image_gray, (template_width, template_height))

        # result = match_template(image_gray, template_gray)
        result = cv.matchTemplate(binary_image, binary_template ,cv.TM_CCOEFF_NORMED)

        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + template_gray.shape[1], loc[0] + template_gray.shape[0]))

        selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("Gambar tidak sesuai dengan template yang disediakan")
        else:
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]

            table  = perform_ocr(image_rgb)

            st.table(table)

            st.markdown('### Unduh Tabel dalam Format Excel')

            # Buat objek BytesIO untuk menyimpan file Excel
            excel_buffer = io.BytesIO()

            # Tulis DataFrame ke dalam objek BytesIO sebagai file Excel
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter', mode='xlsx', options={'remove_timezone': True}) as writer:
                table.to_excel(writer, sheet_name='Sheet1', index=False)

            # Unduh data Excel
            excel_buffer.seek(0)
            st.download_button(
                label="Unduh Data dalam Format Excel",
                data=excel_buffer,
                file_name='data.xlsx',  # Nama file yang akan diunduh
                key='excel-download'
            )




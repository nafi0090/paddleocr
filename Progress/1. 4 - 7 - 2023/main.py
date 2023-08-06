import cv2
import streamlit as st
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import cv2
import pandas as pd
from datetime import datetime

def non_max_suppression(boxes, scores, threshold):
    # Mengurutkan kotak dan skor berdasarkan skor secara menurun
    sorted_indices = np.argsort(scores)[::-1]
    boxes = boxes[sorted_indices]
    scores = scores[sorted_indices]

    # Menginisialisasi daftar kotak yang dipilih
    selected_boxes = []

    while len(boxes) > 0:
        # Mengambil kotak dengan skor tertinggi
        current_box = boxes[0]
        selected_boxes.append(current_box)

        # Menghitung IoU (Intersection over Union) antara kotak saat ini dan kotak yang tersisa
        ious = calculate_iou(current_box, boxes[1:])

        # Mengambil kotak yang memiliki IoU kurang dari threshold
        selected_indices = np.where(ious < threshold)[0]

        # Menghapus kotak yang dipilih dari daftar kotak
        boxes = boxes[selected_indices + 1]
        scores = scores[selected_indices + 1]

    return selected_boxes

def calculate_iou(box, boxes):
    # Menghitung luas kotak saat ini
    x1 = box[0]
    y1 = box[1]
    x2 = box[2]
    y2 = box[3]
    area = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Menghitung luas kotak-kotak yang tersisa
    x1s = boxes[:, 0]
    y1s = boxes[:, 1]
    x2s = boxes[:, 2]
    y2s = boxes[:, 3]
    areas = (x2s - x1s + 1) * (y2s - y1s + 1)

    # Menghitung koordinat persekutuan antara kotak saat ini dan kotak-kotak yang tersisa
    xx1s = np.maximum(x1, x1s)
    yy1s = np.maximum(y1, y1s)
    xx2s = np.minimum(x2, x2s)
    yy2s = np.minimum(y2, y2s)

    # Menghitung luas persekutuan
    intersection = np.maximum(0, xx2s - xx1s + 1) * \
        np.maximum(0, yy2s - yy1s + 1)

    # Menghitung IoU (Intersection over Union)
    ious = intersection / (area + areas - intersection)

    return ious


def template_match_multi_scale(image, template, threshold):
    # Mengubah citra dan template menjadi grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Inisialisasi daftar koordinat hasil
    coordinates = []

    # Mendapatkan ukuran citra dan template
    image_height, image_width = gray_image.shape[:2]
    template_height, template_width = gray_template.shape[:2]

    # Loop melalui berbagai skala citra
    for scale in np.linspace(0.1, 3.0, 30)[::-1]:
        # Mengubah ukuran template sesuai dengan skala saat ini
        resized_template = cv2.resize(
            gray_template, (int(template_width * scale), int(template_height * scale)))

        # Jika ukuran template setelah diresize lebih kecil dari ukuran citra, lanjutkan pencarian
        if resized_template.shape[0] > image_height or resized_template.shape[1] > image_width:
            continue

        # Melakukan template matching pada skala saat ini
        result = cv2.matchTemplate(
            gray_image, resized_template, cv2.TM_CCOEFF_NORMED)

        # Mengambil lokasi koordinat dengan nilai kemiripan di atas threshold
        loc = np.where(result >= threshold)
        coordinates.extend(list(zip(*loc[::-1])))

    return coordinates


def crop_image(image, start_x, start_y, end_x, end_y):
    # Memotong citra berdasarkan koordinat yang diberikan
    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image

# Mengunggah citra dan template
uploaded_image = st.file_uploader("Unggah citra", type=["jpg", "jpeg", "png"])
uploaded_template = st.file_uploader(
    "Unggah template", type=["jpg", "jpeg", "png"])

threshold = 0.56
threshold_nms = 0.5192

if uploaded_image is not None and uploaded_template is not None:
    # Membaca citra dan template yang diunggah
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
    template = cv2.imdecode(np.frombuffer(
        uploaded_template.read(), np.uint8), 1)

    # # # Menampilkan citra dan template
    # st.image(image, caption='Citra Asli', use_column_width=True)
    # st.image(template, caption='Template', use_column_width=True)

    # Melakukan template matching multi-skala
    coordinates = template_match_multi_scale(image, template, threshold)

    arr_desc=[]
    arr_type=[]
    arr_date=[]
    arr_time=[]
    arr_cash=[]
    arr_cash_1=[]

    if len(coordinates) == 0:
        st.write("Tidak ditemukan kecocokan template dalam citra")
    else:
        # Mengubah koordinat menjadi format kotak [x1, y1, x2, y2]
        boxes = np.array([(x, y, x + template.shape[1], y + template.shape[0]) for x, y in coordinates])

        # Menerapkan non-max suppression
        selected_boxes = non_max_suppression(boxes, np.ones(len(boxes)), threshold_nms)


        for i, box in enumerate(selected_boxes):
            start_x, start_y, end_x, end_y = box
            # Memotong citra berdasarkan koordinat
            cropped_image = crop_image(image, start_x, start_y, end_x, end_y)
            # Menampilkan gambar di Streamlit
            

            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            img_path = np.array(cropped_image)

            array_time = []
            array_date = []
            array_word = []
            array_code = []
            array_nominal = []

            def is_date(txt):
                if len(txt) != 10:
                    return False
                for i in range(10):
                    if i == 4 or i == 7:
                        if txt[i] != '-':
                            return False
                        elif not txt[i].isdigit():
                            return False
                    return True
                    
            result = ocr.ocr(img_path, cls=True)
            for idx in range(len(result)):
                res = result[idx]
                txts = [line[1][0] for line in res]
                for txt in txts:
                    if len(txt) == 1 and "K" in txt:
                        array_code.append(txt)
                    elif len(txt) == 1 and "D" in txt:
                        array_code.append(txt)
                    elif "." in txt or "," in txt or ",00" in txt or ".00" in txt:
                        array_nominal.append(txt)
                    elif len(txt)==8 and ":":
                        array_time.append(txt)
                    elif is_date(txt):
                        array_date.append(txt)
                    else:
                        array_word.append(txt)

            word = ' '.join(array_word)
            # code = ' '.join(array_code)
            # date = ' '.join(array_date)
            # time = ' '.join(array_time)

            # st.write(array_word)
            # st.write(array_code)
            # st.write(array_date)
            # st.write(array_nominal)
            # st.write(array_time)
            arr_desc.append(word)
            arr_type.append(array_code[0])
            arr_date.append(array_date[0])
            arr_time.append(array_time[0])
            arr_cash.append(array_nominal[0])
            arr_cash_1.append(array_nominal[1])

    Table = {
        'Keterangan': arr_desc,
        'Tipe': arr_type,
        'Date': arr_date,
        'Time': arr_time,
        'Nominal': arr_cash,
        'Saldo Akhir': arr_cash_1
    }
    
    table = pd.DataFrame(Table)
    st.table(table)
    # st.write(arr_desc)
    # st.write(arr_type)
    # st.write(arr_date)
    # st.write(arr_time)
    # st.write(arr_cash)
    # st.write(arr_cash_1)



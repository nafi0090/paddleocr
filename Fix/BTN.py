import re
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from paddleocr import PaddleOCR
from skimage.feature import match_template

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

def crop_image(image, start_x, start_y, end_x, end_y):
    # Memotong citra berdasarkan koordinat yang diberikan
    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image

def is_date(txt):
    pattern = r"\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Agu|Sep|Oct|Nov|Dec)\s*\d{4}" 
    # dengan pattern tanggal bulan tahun dengan spasi maupun tidak
    tanggal = re.findall(pattern, txt)
    if tanggal:
        return True
    return False

def is_time(txt):
    pattern = r"\b\d{2}:\d{2}:\d{2}\b"
    waktu = re.findall(pattern, txt)
    if waktu:
        return True
    return False

def is_number(txt):
    pattern = r"Rp\d{1,3}(?:\.\d{3})*(?:,\d{2})?"
    angka = re.findall(pattern, txt)
    if angka:
        return True
    return False

def is_number_credit(txt):
    pattern = r"\d{4}\s\d{4}\s\d{4}\s\d{3}"
    matches = re.findall(pattern, txt)
    if matches:
        return True
    return False

def run_app():
    st.title("BTN Project")
    # Mengunggah citra dan template
    uploaded_image = st.file_uploader("Unggah citra", type=["jpg", "jpeg", "png"])
    uploaded_template = st.file_uploader("Unggah template", type=["jpg", "jpeg", "png"])

    threshold = 0.1
    threshold_nms = 0.8
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    button_ok = st.button("Run")

    if button_ok and uploaded_image is not None and uploaded_template is not None:
        # Membaca citra dan template yang diunggah
        image_rgb = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
        template_rgb = cv2.imdecode(np.frombuffer(uploaded_template.read(), np.uint8), 1)

        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2GRAY)
        
        # Periksa ukuran gambar dan templat
        image_height, image_width = image_gray.shape
        template_height, template_width = template_gray.shape

        # Resize gambar jika ukuran lebih kecil daripada templat
        if image_height < template_height or image_width < template_width:
            image_gray = cv2.resize(image_gray, (template_width, template_height))

        result = match_template(image_gray, template_gray)

        loc = np.where(result >= threshold)
        boxes = np.column_stack((loc[1], loc[0], loc[1] + template_gray.shape[1], loc[0] + template_gray.shape[0]))

        selected_boxes = non_max_suppression(boxes, result[loc], threshold_nms)

        if len(selected_boxes) == 0:
            st.write("Tidak ditemukan kecocokan template dalam citra")
        else:
            x1, y1, x2, y2 = selected_boxes[0]
            image_rgb = image_rgb[y1:, x1:]
            array = ocr.ocr(image_rgb, cls=True)[0]
            array = [line[1][0] for line in array]
            data = []
            start = 0
            end = 0
            for i, result in enumerate(array):
                if is_time(result):
                    end = i+1
                    data.append(
                        array[start:end]
                    )
                    start = i+1

                arr_desc=[]
                arr_date=[]
                arr_time=[]
                arr_cash=[]

                for i, data_i in enumerate(data):
                    array_time = []
                    array_date = []
                    array_word = []
                    array_nominal = []
                    for data_j in data_i:
                        print(data_j)
                        if is_number(data_j):
                            array_nominal.append(data_j)
                        elif is_number_credit(data_j):
                            print(data_j)
                        elif is_time(data_j):
                            array_time.append(data_j)
                        elif is_date(data_j):
                            array_date.append(data_j)
                        else:
                            array_word.append(data_j)

                    word = ' '.join(array_word)
                    if "Rentang Waktu" in word:
                        word_index = word.index("Rentang Waktu")
                        word = word[word_index:]
                        word = word.replace("Rentang Waktu", "")

                    arr_desc.append(word)
                    arr_date.append(array_date[0] if len(array_date) > 0 else "Data Tidak Terdeteksi")
                    arr_time.append(array_time[0] if len(array_time) > 0 else "Data Tidak Terdeteksi")
                    arr_cash.append(array_nominal[0] if len(array_nominal) > 0 else "Data Tidak Terdeteksi")

            table = {
                'Keterangan': arr_desc,
                'Date': arr_date,
                'Time': arr_time,
                'Nominal': arr_cash,
            }

            table = pd.DataFrame(table)
            st.table(table)




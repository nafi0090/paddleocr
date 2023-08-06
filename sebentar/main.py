import cv2
import streamlit as st
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import cv2
import pandas as pd
from datetime import datetime

# Mengunggah gambar menggunakan komponen Streamlit "file_uploader"
uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

# Mengecek apakah file gambar telah diunggah
if uploaded_file is not None:
    # Membaca gambar menggunakan PIL (Python Imaging Library)
    img = Image.open(uploaded_file)

    # Mengubah gambar menjadi array numpy menggunakan OpenCV
    gambar = img.convert('RGB')
    gray_rumus = Image.new('L', gambar.size)
    for x in range(gambar.width):
        for y in range(gambar.height):
            r, g, b = gambar.getpixel((x, y))
            gray_pixel = int((0.299 * r) + (0.587 * g) + (0.114 * b))
            gray_rumus.putpixel((x, y), gray_pixel)

    img_array = np.array(gray_rumus)

    # Mengubah gambar menjadi gambar biner menggunakan thresholding
    threshold = 200
    _, binary_image = cv2.threshold(
        img_array, threshold, 255, cv2.THRESH_BINARY)

    # Melakukan resize pada gambar biner
    resized_image = cv2.resize(binary_image, (0, 0), fx=0.8, fy=0.8)

    # Menampilkan gambar di Streamlit
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

    def is_time(txt):
        if len(txt) != 8:
            return False
        for i in range(8):
            if i == 2 or i == 5:
                if txt[i] != ':':
                    return False
            elif not txt[i].isdigit():
                return False
        return True

    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    img_path = np.array(gambar)

    array_time = []
    array_date = []
    array_word = []
    array_code = []
    array_nominal = []

    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        txts = [line[1][0] for line in res]
        for txt in txts:
            if len(txt) == 1 and "K" in txt:
                array_code.append(txt)
            elif len(txt) == 1 and "D" in txt:
                array_code.append(txt)
            elif "." and "," and ",00" in txt:
                array_nominal.append(txt)
            elif is_time(txt):
                array_time.append(txt)
            elif is_date(txt):
                array_date.append(txt)
            else:
                array_word.append(txt)

    datetime_str = array_word[1]

    datetime_parts = datetime_str.split("|")
    if len(datetime_parts) == 2:
        date_time_part = datetime_parts[1].strip()
        date_part, time_part = date_time_part.split(" ")
        time_parts = time_part.split(":")
        if len(time_parts) == 3:
            time = []
            for part in time_parts:
                time.append(int(part))

        date_parts = date_part.split("/")
        if len(date_parts) == 3:
            date = []
            for part in date_parts:
                if part.isdigit():
                    date.append(int(part))

    word = ' '.join(array_word)
    code = ' '.join(array_code)
    date = ' '.join(array_date)
    time = ' '.join(array_time)

    # array u/ menghitung jumlah array yang terbaca
    total_word = len(array_word)
    total_code = len(array_code)
    total_time = len(array_time)
    total_date = len(array_date)
    total_nominal = len(array_nominal)

    # Total Array yang terbaca
    data = {
        'Keterangan': total_word,
        'Code': total_code,
        'Date': total_date,
        'Time': total_time,
        'Pengeluaran': total_nominal
    }

    data = pd.DataFrame([data])

    # Table = {
    #     'Keterangan': word,
    #     'Tipe': code,
    #     'Date': date,
    #     'Time': time,
    #     'Nominal': array_nominal[0],
    #     'Saldo Akhir': array_nominal[1]
    # }

    # table = pd.DataFrame([Table])

    # Menampilkan tabel menggunakan st.table()
    st.image(gambar)
    st.table(data)
    # st.table(table)
    st.write(array_word)
    st.write(array_code)
    st.write(array_date)
    st.write(array_nominal)
    st.write(array_time)

else:
    st.write("Mohon unggah file gambar")

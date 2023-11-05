import re
import pandas as pd
from paddleocr import PaddleOCR

def is_date(txt):
    pattern = r'\d{1,2}\s?/\s?\d{1,2}'
    date = re.findall(pattern, txt)
    if date:
        return True
    return False

def is_time(txt):
    pattern = r"\b\d{2}:\d{2}:\d{2}\b"
    waktu = re.findall(pattern, txt)
    if waktu:
        return True
    return False

def is_number(txt):
    pattern = r'^[1-9]\d{0,2}(?:[.,]\d{3})*(?:[.,]\d{2})?$'
    if re.match(pattern, txt):
        return True
    return False

def perform_ocr(image_rgb_crop):
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    array = ocr.ocr(image_rgb_crop, cls=True)[0]
    array = [line[1][0] for line in array]
    print (array)
    data = []
    start = 0
    end = 0
    for i, result in enumerate(array):
        if result == "SALDO AWAL":
            start = i + 2  # Mulai dari indeks i, bukan i + 2
        elif result == "TOTAL":
            end = i
            data.append(array[start:end ])  # Tambahkan 1 untuk menyertakan indeks 'end'
            start = i   # Mulai dari indeks setelah 'TOTAL' untuk grup berikutnya
        elif is_date(result):
            end = i
            data.append(array[start:end])  # Tambahkan 1 untuk menyertakan indeks 'end'
            start = i  # Mulai dari indeks tanggal untuk grup berikutnya
        
        arr_desc=[]
        arr_date=[]
        arr_time=[]
        arr_cash=[]
        arr_cash=[]
        arr_saldo_akhir=[]

    if data:
        data.pop(0)
        
        for i, data_i in enumerate(data):
            print(data_i)

            array_time = []
            array_date = []
            array_word = []
            array_nominal = []

            for data_j in data_i:
                # print(data_j)
                if is_number(data_j):
                    array_nominal.append(data_j)
                elif is_time(data_j):
                    array_time.append(data_j)
                elif is_date(data_j):
                    array_date.append(data_j)
                else:
                    array_word.append(data_j)

            word = ' '.join(array_word)
            if "SALDO AWAL" in word:
                word_index = word.index("SALDO AWAL")
                word = word[word_index:]
                word = word.replace("SALDO AWAL", "")
            
            arr_desc.append(word if len(word) > 0 else "Data Tidak Terdeteksi")
            arr_date.append(array_date[0] if len(array_date) > 0 else "Data Tidak Terdeteksi")
            arr_time.append(array_time[0] if len(array_time) > 0 else "Data Tidak Terdeteksi")
            arr_cash.append(array_nominal[0] if len(array_nominal) > 0 else "Data Tidak Terdeteksi")
            arr_saldo_akhir.append(array_nominal[1] if len(array_nominal) > 1 else "Data Tidak Terdeteksi")

    table = {
        'Keterangan': arr_desc,
        'Date': arr_date,
        'Time': arr_time,
        'Nominal': arr_cash,
        'Saldo Akhir': arr_saldo_akhir,
    }

    table = pd.DataFrame(table)

    return table
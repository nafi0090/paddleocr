import re
import pandas as pd
from paddleocr import PaddleOCR

def is_date(txt):
    pattern = r"\b\d{4}-\d{2}-\d{2}\b"
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
    pattern = r'^[1-9]\d{0,2}(?:[.,]\d{3})*(?:[.,]\d{2})?$'
    if re.match(pattern, txt):
        return True
    return False

def perform_ocr(image_rgb):
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

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
        arr_type=[]
        arr_date=[]
        arr_time=[]
        arr_cash=[]
        arr_saldo_akhir=[]
        for i, data_i in enumerate(data):
            array_time = []
            array_date = []
            array_word = []
            array_code = []
            array_nominal = []
            for data_j in data_i:
                print(data_j)
                if len(data_j) == 1 and "K" in data_j:
                    array_code.append(data_j)
                elif len(data_j) == 1 and "D" in data_j:
                    array_code.append(data_j)
                elif is_number(data_j):
                    array_nominal.append(data_j)
                elif is_time(data_j):
                    array_time.append(data_j)
                elif is_date(data_j):
                    array_date.append(data_j)
                else:
                    array_word.append(data_j)
            word = ' '.join(array_word)
            if "Saldo Akhir" in word:
                word_index = word.index("Saldo Akhir")
                word = word[word_index:]
                word = word.replace("Saldo Akhir", "")
            arr_desc.append(word)
            arr_type.append(array_code[0] if len(array_code) > 0 else "Data Tidak Terdeteksi")
            arr_date.append(array_date[0] if len(array_date) > 0 else "Data Tidak Terdeteksi")
            arr_time.append(array_time[0] if len(array_time) > 0 else "Data Tidak Terdeteksi")
            arr_cash.append(array_nominal[0] if len(array_nominal) > 0 else "Data Tidak Terdeteksi")
            arr_saldo_akhir.append(array_nominal[1] if len(array_nominal) > 1 else "Data Tidak Terdeteksi")

    table = {
        'Keterangan': arr_desc,
        'Tipe': arr_type,
        'Date': arr_date,
        'Time': arr_time,
        'Nominal': arr_cash,
        'Saldo Akhir': arr_saldo_akhir
    }

    table = pd.DataFrame(table)

    return table
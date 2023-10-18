import re
import pandas as pd
from paddleocr import PaddleOCR

def is_date(txt):
    pattern = r'\d{1,2}\s?\D{3}\s?\d{4}'
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
    pattern = r"Rp\d{1,3}(?:\.\d{3})*(?:,\d{2})?"
    angka = re.findall(pattern, txt)
    if angka:
        return True
    return False

def is_credit_card_number(txt):
    pattern = r"\d{4}\s\d{4}\s\d{4}\s\d{3}"
    credit_card_number = re.findall(pattern, txt)
    if credit_card_number:
        return True
    return False

def perform_ocr(image_rgb_crop):
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    array = ocr.ocr(image_rgb_crop, cls=True)[0]
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
        arr_credit_card=[]

        for i, data_i in enumerate(data):

            array_time = []
            array_date = []
            array_word = []
            array_nominal = []
            array_credit_card = []

            for data_j in data_i:
                print(data_j)
                if is_number(data_j):
                    array_nominal.append(data_j)
                elif is_credit_card_number(data_j):
                    array_credit_card.append(data_j)
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
            arr_date.append(array_date[0] if len(array_date) > 0 else arr_date[-1])
            arr_time.append(array_time[0] if len(array_time) > 0 else "Data Tidak Terdeteksi")
            arr_cash.append(array_nominal[0] if len(array_nominal) > 0 else "Data Tidak Terdeteksi")
            arr_credit_card.append(array_credit_card[0] if len(array_credit_card) > 0 else "Data Tidak Terdeteksi")

    table = {
        'Keterangan': arr_desc,
        'Date': arr_date,
        'Time': arr_time,
        'Nominal': arr_cash,
    }

    table = pd.DataFrame(table)

    return table
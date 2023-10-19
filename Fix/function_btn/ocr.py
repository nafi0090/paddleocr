import re
import pandas as pd
from paddleocr import PaddleOCR

def is_date(txt):
    pattern = r'\d{1,2}\s?/\s?\d{1,2}'
    date = re.findall(pattern, txt)
    if date:
        return True
    return False

def process_data(data):
    # Process the data here
    print("Processing Data:")
    for text in data:
        print(text)
    print()

def perform_ocr(image_rgb_crop):
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    # Perform OCR on the image
    ocr_results = ocr.ocr(image_rgb_crop, cls=True)[0]
    ocr_text = [line[1][0] for line in ocr_results]

    # Initialize variables to track start and end indices
    start_index = None
    end_index = None

    # Iterate through the OCR text
    for i, text in enumerate(ocr_text):
        if is_date(text):
            # If the text is a date, set it as the start index
            start_index = i
            if end_index is not None:
                # If there's already an end index, process the data
                process_data(ocr_text[start_index:end_index])
                start_index = None
                end_index = None
        elif text == "AFIDA KHOLIFATU":
            # If the text is "AFIDA KHOLIFATU," set it as the end index and break the loop
            end_index = i
            break

    # If there's a start index without an end index (e.g., last date in the text), process the data
    if start_index is not None:
        process_data(ocr_text[start_index:])

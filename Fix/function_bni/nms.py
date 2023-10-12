import numpy as np

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
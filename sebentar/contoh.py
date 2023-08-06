import cv2
import numpy as np
import streamlit as st


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

threshold = 0.5192

if uploaded_image is not None and uploaded_template is not None:
    # Membaca citra dan template yang diunggah
    image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), 1)
    template = cv2.imdecode(np.frombuffer(
        uploaded_template.read(), np.uint8), 1)

    # Menampilkan citra dan template
    st.image(image, caption='Citra Asli', use_column_width=True)
    st.image(template, caption='Template', use_column_width=True)

    # Melakukan template matching multi-skala
    coordinates = template_match_multi_scale(image, template, threshold)

    if len(coordinates) == 0:
        st.write("Tidak ditemukan kecocokan template dalam citra")
    else:
        st.write(
            f"Ditemukan {len(coordinates)} kecocokan template dalam citra")

        for i, (start_x, start_y) in enumerate(coordinates):
            end_x = start_x + template.shape[1]
            end_y = start_y + template.shape[0]

            # Memotong citra berdasarkan koordinat
            cropped_image = crop_image(image, start_x, start_y, end_x, end_y)
            st.image(cropped_image,
                     caption=f'Hasil Pemotongan {i+1}', use_column_width=True)

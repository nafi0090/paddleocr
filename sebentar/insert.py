from PIL import Image
import numpy as np

def convert_to_binary(image_path, threshold, output_path):
    # Buka gambar dengan PIL
    image = Image.open(image_path)
    
    # Konversi gambar ke grayscale menggunakan rumus yang diberikan
    gray_image = image.convert('RGB')
    gray_rumus = Image.new('L', gray_image.size)
    for x in range(gray_image.width):
        for y in range(gray_image.height):
            r, g, b = gray_image.getpixel((x, y))
            gray_pixel = int((0.299 * r) + (0.587 * g) + (0.114 * b))
            gray_rumus.putpixel((x, y), gray_pixel)
    
    # Buat citra biner dengan ambang batas
    binary_image = gray_rumus.point(lambda pixel: 0 if pixel < threshold else 255, mode='1')
    
    # Simpan citra biner ke file
    binary_image.save(output_path)
    print("Citra biner telah disimpan di", output_path)

# Path ke gambar yang ingin diubah menjadi citra biner
image_path = "BNI/lane_2/crop.png"

# Ambang batas untuk konversi (dalam hal ini, 200)
threshold = 200

# Path untuk menyimpan citra biner
output_path = "BNI/lane_2/crop1.png"

# Panggil fungsi untuk mengonversi dan menyimpan gambar menjadi citra biner
convert_to_binary(image_path, threshold, output_path)

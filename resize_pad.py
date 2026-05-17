import cv2
import numpy as np
import sys
import os

def resize_with_padding(image_path, output_path, size=128):
    # Đọc ảnh
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Không đọc được ảnh!")

    h, w = img.shape[:2]

    # Tính scale để giữ tỉ lệ
    scale = size / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Tạo ảnh nền (đen)
    canvas = np.zeros((size, size, 3), dtype=np.uint8)

    # Tính vị trí để đặt ảnh vào giữa
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2

    # Gán vào canvas
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    # Lưu ảnh
    cv2.imwrite(output_path, canvas)
    print(f"Đã lưu ảnh: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cách dùng: python resize_pad.py input.jpg")
        sys.exit(1)

    input_path = sys.argv[1]
    name, ext = os.path.splitext(input_path)
    output_path = name + "_128x128.jpg"

    resize_with_padding(input_path, output_path)
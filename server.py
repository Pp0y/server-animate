import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

UPLOAD_FOLDER = './upload'  # โฟลเดอร์สำหรับเก็บไฟล์
PROCESSED_FOLDER = './processed'  # โฟลเดอร์สำหรับเก็บไฟล์ที่ประมวลผลแล้ว
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_image(file_path):
    # อ่านภาพ
    img = cv2.imread(file_path)
    img_original = img.copy()

    # แปลงภาพเป็น Grayscale และใช้ Bilateral Filter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 20, 30, 30)
    edged = cv2.Canny(gray, 10, 20)

    # ค้นหา Contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest = biggest_contour(contours)

    if biggest.size != 0:
        cv2.drawContours(img, [biggest], -1, (0, 255, 0), 3)

        points = biggest.reshape(4, 2)
        input_points = np.zeros((4, 2), dtype="float32")

        # จัดเรียงจุด
        points_sum = points.sum(axis=1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]

        points_diff = np.diff(points, axis=1)
        input_points[1] = points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]

        # แปลง Perspective
        converted_points = np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]])
        matrix = cv2.getPerspectiveTransform(input_points, converted_points)
        img_output = cv2.warpPerspective(img_original, matrix, (1920, 1080))

        # บันทึกผลลัพธ์
        processed_file_path = os.path.join(PROCESSED_FOLDER, "processed_image.jpg")
        cv2.imwrite(processed_file_path, img_output)
        return processed_file_path

    # ถ้าไม่พบ Contours
    return None

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # บันทึกไฟล์ในโฟลเดอร์ upload
    original_filename = file.filename
    original_file_path = os.path.join(UPLOAD_FOLDER, original_filename)
    file.save(original_file_path)

    # ประมวลผลรูปภาพ
    processed_file_path = process_image(original_file_path)
    if processed_file_path:
        # ส่งไฟล์ที่ประมวลผลกลับไปยัง Unity
        return send_file(processed_file_path, mimetype='image/jpeg')
    else:
        return jsonify({"error": "Failed to process the image"}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

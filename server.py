import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = './upload'  # โฟลเดอร์สำหรับเก็บไฟล์
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี

@app.route("/")
def home():
    return "Welcome to the upload service!"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # บันทึกไฟล์ในโฟลเดอร์ upload
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File saved successfully!", "file_path": file_path}), 200

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

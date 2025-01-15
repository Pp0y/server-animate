import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = './upload'  # โฟลเดอร์สำหรับเก็บไฟล์
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี

@app.route('/ss' , methods=['GET'])
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
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = './upload'  # โฟลเดอร์สำหรับเก็บไฟล์
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # สร้างโฟลเดอร์หากยังไม่มี

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

        # เปลี่ยนชื่อหรือประมวลผลไฟล์
    renamed_filename = f"processed_{original_filename}"
    renamed_file_path = os.path.join(UPLOAD_FOLDER, renamed_filename)
    os.rename(original_file_path, renamed_file_path)

    # ส่งไฟล์กลับไปยัง Unity
    return send_file(renamed_file_path, mimetype='image/jpeg')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
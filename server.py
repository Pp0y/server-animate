import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # บันทึกไฟล์ในโฟลเดอร์ upload
    original_filename = secure_filename(file.filename)
    original_file_path = os.path.join(UPLOAD_FOLDER, original_filename)
    file.save(original_file_path)

    # เปลี่ยนชื่อไฟล์
    new_filename = f"renamed_{original_filename}"
    new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)
    os.rename(original_file_path, new_file_path)

    # ส่งไฟล์กลับไปยัง Unity
    return send_file(new_file_path, mimetype='image/jpeg')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

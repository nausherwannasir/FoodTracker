from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from utils import save_file, image_ocr, extract_date, parse_dates

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET" ,"POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            return "No File Selected"

        file = request.files["file"]
        filepath, filename = save_file(file, app.config['UPLOAD_FOLDER'])
        text = image_ocr(filepath)
        date_strings = extract_date(text)
        expiry_dates = parse_dates(date_strings)

       
        expiry_date = expiry_dates[0] if expiry_dates else "No expiry date found"

        return render_template("result.html", filename=filename, text=text, expiry_date=expiry_date)

    return redirect(url_for("home"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)

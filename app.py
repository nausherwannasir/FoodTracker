import os
import re
from flask import send_from_directory
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import dateparser



app = Flask(__name__)
UPLOAD_FOLDER = '/Users/nash/Documents/Github/FoodTracker/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


   

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET" ,"POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No File Part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        text = pytesseract.image_to_string(Image.open(filepath))
        
        date_patterns = [
        r"\b\d{2}[/-]\d{2}[/-]\d{2,4}\b",   # 22/09/2025
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}",
        r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}",
        r"(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[a-z]*\s+\d{1,2},?\s+\d{2,4}",
        r"\d{1,2}\s+(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[a-z]*\s+\d{2,4}"
    ]

        expiry_date = "No expiry date found"      
        for pattern in date_patterns:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
            
                parsed = dateparser.parse(matches[0], languages=["en", "fr"])
                if parsed:
                    expiry_date = parsed.strftime("%Y-%m-%d")  # Normalize
                    break
        
        return render_template("result.html", filename=filename, text=text, expiry_date=expiry_date)
    
    
    return redirect(url_for("home"))
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)

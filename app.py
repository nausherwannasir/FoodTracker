import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/nash/Documents/Github/FoodTracker/static/uploads'
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
        return render_template("result.html", filename=filename)
    return redirect(url_for("home"))

@app.route("/show/<filename>")
def show_file(filename):
    return f"<img src = '/static/uploads/{filename}' alt = 'uploaded image'>"
    
if __name__ == "__main__":
    app.run(debug=True)

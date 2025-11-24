# ---------------------------------------------------------
#  FLASK WEB APP FOR OCR DOCUMENT PROCESSING + DATABASE
# ---------------------------------------------------------

import sys
import os
from flask import Flask, render_template, request

# ---------------------------------------------------------
#  FIX IMPORT PATH TO main.py (one folder up)
# ---------------------------------------------------------

BASE_DIR = r"D:\PYTHON\3N mini hackathon"
sys.path.append(BASE_DIR)

from main import ocr_file, classify_document, extract_fields

# ---------------------------------------------------------
#  DATABASE IMPORT
# ---------------------------------------------------------

from database import init_db, save_to_db


# ---------------------------------------------------------
#  FLASK SETUP
# ---------------------------------------------------------

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the SQLite database
init_db()


# ---------------------------------------------------------
#  ROUTES
# ---------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():

    if "file" not in request.files:
        return "Error: No file field found."

    file = request.files["file"]

    if file.filename == "":
        return "Error: No file selected."

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Run your existing pipeline
    text = ocr_file(file_path)
    doc_type = classify_document(text)
    fields = extract_fields(doc_type, text)

    # SAVE INTO DATABASE
    save_to_db(file.filename, doc_type, fields)

    # Show results on webpage
    return render_template(
        "result.html",
        filename=file.filename,
        doc_type=doc_type,
        fields=fields
    )


# ---------------------------------------------------------
#  MAIN ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

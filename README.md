# 3N OCR Pipeline

An end-to-end **document OCR and structured data extraction pipeline** built with Python.

The system accepts document images and PDFs, extracts text using **Tesseract OCR**, identifies the document type using a **keyword-based scoring mechanism**, and then applies document-specific **regular-expression extraction rules** to convert unstructured OCR text into structured fields.

The project also includes both a **Streamlit interface** for interactive document processing and a **Flask + SQLite web application** for document processing with persistent storage.

---

## Features

* OCR for images and PDF documents
* Automatic document classification
* Document-specific structured field extraction
* Support for multiple document categories
* Interactive Streamlit interface
* Flask web application
* SQLite persistence for extracted results
* JSON export of extracted fields
* OCR text inspection
* Recent processing history in the Streamlit interface

---

## Supported Documents

The current pipeline is configured to recognize the following document types:

| Document Type     | Example Extracted Fields                             |
| ----------------- | ---------------------------------------------------- |
| Driving License   | DL Number, Name, DOB                                 |
| Passport          | Passport Number, Name, Country                       |
| W-2               | EIN, Year, Employee Name                             |
| Paystub           | Net Pay, Employee Name, Employer Name                |
| Flood Certificate | Borrower Name, Customer Number, Expiration Date      |
| Others            | Returned when no supported document type is detected |

The classifier assigns scores to each supported document type based on characteristic keywords found in the OCR output and selects the highest-scoring category.

---

## How It Works

The complete processing flow is:

```text
              ┌──────────────────┐
              │  PDF / Image     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Tesseract OCR  │
              │  Text Extraction │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Document         │
              │ Classification   │
              │ (Keyword Scoring)│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Document-Specific│
              │ Field Extraction │
              │ (Regex / Rules)  │
              └────────┬─────────┘
                       │
              ┌────────┴─────────┐
              ▼                  ▼
       ┌──────────────┐   ┌──────────────┐
       │ Structured   │   │ OCR Text     │
       │ JSON Fields  │   │ Output       │
       └──────────────┘   └──────────────┘
```

For PDFs, the current OCR implementation converts **only the first page** to an image before sending it to Tesseract.

---

## Architecture

### 1. OCR Layer

The OCR layer is implemented in `main.py`.

Supported input formats include:

* PNG
* JPG / JPEG
* BMP
* TIFF
* PDF

Images are processed directly with Pillow and Tesseract. PDFs are converted to an image using `pdf2image` before OCR processing.

Core function:

```python
ocr_file(path)
```

returns the raw OCR text extracted from the document.

---

### 2. Document Classification

After OCR, the extracted text is normalized and passed to:

```python
classify_document(text)
```

The classifier maintains a score for each supported document category and increments the score whenever a matching keyword is found.

For example:

```text
Passport
    ↓
"passport"
"passport number"
"surname"
"given name"
"nationality"
...
```

The document type with the highest score is selected.

If no supported category receives a score, the document is classified as:

```text
Others
```

This logic is intentionally lightweight and does not require a machine-learning classification model.

---

### 3. Structured Field Extraction

Once the document type is determined, the pipeline dispatches the OCR text to a document-specific extraction function.

```python
extract_fields(doc_type, text)
```

The dispatcher routes the document to functions such as:

```text
extract_driving_license()
extract_passport()
extract_w2()
extract_paystub()
extract_flood()
```

These functions use regular expressions, normalization, and document-specific heuristics to extract relevant fields.

Examples include:

### Driving License

```text
DL number
Name
DOB
```

### Passport

```text
Passport number
Country
Name
```

Passport name extraction can use the MRZ when available, with additional fallback strategies for printed passport fields.

### W-2

```text
EIN
Year
Employee Name
```

### Paystub

```text
Net Pay
Employee Name
Employer Name
```

### Flood Certificate

```text
Borrower name
Customer No
Expire date
```

---

# Web Interfaces

The repository contains two interfaces for using the OCR pipeline.

## Streamlit Application

The Streamlit application provides an interactive **Document Intelligence Workspace**.

Users can:

1. Upload a PDF or image
2. Run OCR automatically
3. Detect the document type
4. View extracted fields
5. View the complete OCR text
6. Download the extracted fields as JSON
7. Review recent processing runs

The Streamlit application directly reuses the processing functions from `main.py`.
The `webApp/` folder is a separate Flask interface and is **not required** to run the Streamlit app.

### Run Streamlit

```bash
streamlit run streamlit_app.py
```

The application accepts:

```text
PNG
JPG
JPEG
BMP
TIFF
TIF
PDF
```

---

## Flask Web Application

The repository also contains a Flask-based web interface under:

```text
webApp/
```

The Flask application exposes:

```text
/
```

for the main page and:

```text
/process
```

for document processing.

Uploaded documents are passed through the same OCR → classification → extraction pipeline used by the rest of the project.

### Run Flask

From the project directory:

```bash
python webApp/app.py
```

The application starts Flask in debug mode using:

```python
app.run(debug=True)
```

---

# SQLite Database

The Flask application includes persistent storage using SQLite.

The database is stored as:

```text
extracted_data.db
```

The `documents` table contains:

```text
id
filename
doc_type
fields_json
created_at
```

Extracted structured fields are serialized to JSON before being stored in the database.

---

# Project Structure

```text
3N-OCR-pipeline/
│
├── main.py
├── streamlit_app.py
├── extracted_data.db
│
├── documents-used/
│   ├── Doc1.jpg
│   ├── Doc2.jpg
│   ├── Doc3.png
│   ├── Doc4.pdf
│   └── Doc5.pdf
│
├── webApp/
│   ├── app.py
│   ├── database.py
│   ├── static/
│   └── templates/
│
└── smaple image.png
```

The repository includes five sample documents representing the supported document categories.

---

# Requirements

## Python

Use a recent Python 3 installation.

Install the Python dependencies used by the project:

```bash
pip install -r requirements.txt
```

---

## Tesseract OCR

This project requires **Tesseract OCR** to be installed separately on the system.
Python package installation alone is not enough; the `tesseract` system binary must also be installed.

Configuration options:

- Recommended: make `tesseract` available on your system `PATH`.
- Optional: set `TESSERACT_CMD` to the absolute path of the `tesseract` executable.
- Windows users can still use the default install location (`C:\Program Files\Tesseract-OCR\tesseract.exe`).

On Streamlit Cloud, configure the system dependency in your deployment (for example through apt packages) and, if needed, set `TESSERACT_CMD` in app secrets/environment.

---

## PDF Support

PDF processing uses:

```python
from pdf2image import convert_from_path
```

The current implementation converts the **first page** of a PDF into an image and then sends that image to Tesseract.

`pdf2image` also requires **Poppler** system utilities (`pdftoppm`) on the host machine. Ensure Poppler is installed and available on PATH (including Linux/Streamlit Cloud environments).

---

# Installation

Clone the repository:

```bash
git clone https://github.com/ShekhawaTTiku/3N-OCR-pipeline.git
```

Move into the project:

```bash
cd 3N-OCR-pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```
Install and configure Tesseract OCR on the host machine. If it is not on PATH, set `TESSERACT_CMD` to its absolute binary path.

---

# Usage

## Process the sample documents with Python

The command-line pipeline can process the documents configured in `DOCS_FOLDER`.

```bash
python main.py
```

The script processes each file, performs OCR, determines the document type, and prints the extracted fields.

---

## Launch the Streamlit UI

```bash
streamlit run streamlit_app.py
```

Then upload a supported document through the browser interface.

The application displays:

```text
Detected Document Type
        +
Extracted Fields
        +
Raw OCR Text
        +
JSON Download
```

---

## Launch the Flask UI

```bash
python webApp/app.py
```

The Flask application saves uploaded documents, runs the OCR pipeline, stores the extracted results in SQLite, and renders the processed result in the web interface.

---

# Example Output

A processed document is converted into a structure similar to:

```json
{
  "Name": "John Doe",
  "DOB": "01/01/1990",
  "DL number": "D123456789"
}
```

The exact fields depend on the detected document type.

The Streamlit application also provides a button to download the extracted fields as a JSON file.

---

# Design Decisions

## Why Tesseract?

Tesseract provides a lightweight local OCR engine without requiring a cloud OCR API.

This makes the pipeline suitable for:

* Local development
* Offline processing
* Prototyping
* Privacy-sensitive document workflows

## Why keyword-based classification?

The classification stage is intentionally simple and transparent.

Instead of relying on a trained document-classification model, the pipeline uses document-specific keywords and scoring rules. This makes the behavior easy to inspect and modify for new document categories.

## Why regex-based extraction?

Each supported document type has a known structure and a relatively small set of fields that need to be extracted.

Regular expressions and document-specific heuristics provide a lightweight way to transform OCR text into structured data without introducing a separate NLP model.

---

# Limitations

The current version is primarily a prototype / task-oriented document extraction pipeline.

### PDF processing

Only the first page of a PDF is currently processed.

```python
convert_from_path(path, first_page=1, last_page=1)
```

### Document classification

Classification is based on predefined keywords rather than a trained machine-learning model.

Documents with poor OCR quality or unusual layouts may therefore be misclassified.

### Field extraction

The extraction rules are document-specific and rely heavily on expected text patterns.

OCR errors, layout changes, or different document templates can cause individual fields to be returned as `None` or extracted incorrectly.

### Configuration

Some paths in the current code are hard-coded for the original Windows development environment, including the Tesseract executable path and document directory.

---

# Future Improvements

Potential improvements include:

* Multi-page PDF processing
* OCR preprocessing for noisy or rotated documents
* Confidence scoring for OCR and extracted fields
* Better document classification using ML / transformer models
* Layout-aware document understanding
* Support for additional document types
* Configurable extraction schemas
* Environment-variable based configuration
* API endpoints for programmatic document processing
* Improved validation of extracted identifiers
* Dockerized deployment
* Authentication and access control
* Production-grade database support

---

# Technologies Used

| Technology          | Purpose                            |
| ------------------- | ---------------------------------- |
| Python              | Core implementation                |
| Tesseract OCR       | Text recognition                   |
| pytesseract         | Python interface for Tesseract     |
| Pillow              | Image loading and processing       |
| pdf2image           | PDF-to-image conversion            |
| Streamlit           | Interactive document-processing UI |
| Flask               | Web application                    |
| SQLite              | Persistent result storage          |
| Regular Expressions | Structured field extraction        |

---

# Sample Documents

The repository contains a `documents-used` directory with sample documents for testing the pipeline:

```text
Doc1.jpg
Doc2.jpg
Doc3.png
Doc4.pdf
Doc5.pdf
```

---

# Pipeline Summary

```text
Input Document
      │
      ▼
┌───────────────┐
│ OCR           │
│ Tesseract     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Classification│
│ Keyword Score │
└───────┬───────┘
        │
        ▼
┌────────────────┐
│ Field Extractor│
│ Regex + Rules  │
└───────┬────────┘
        │
        ▼
┌─────────────────────┐
│ Structured Document │
│ Data / JSON         │
└─────────────────────┘
        │
        ├──────────────► Streamlit UI
        │
        └──────────────► Flask + SQLite
```

---

# Author

**Digvijay Singh Shekhawat**

GitHub: [@ShekhawaTTiku](https://github.com/ShekhawaTTiku)

---

## License

No license is currently specified in the repository.

Add a `LICENSE` file if you intend to distribute the project under an open-source license.

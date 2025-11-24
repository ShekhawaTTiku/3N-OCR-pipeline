# 3N-OCR-pipeline

## Overview

The 3N-OCR-pipeline is an intelligent document processing system that automatically extracts, classifies, and analyzes information from various document types. It uses Optical Character Recognition (OCR) to convert document images and PDFs into structured data.

## Features

- **Multi-format Support**: Processes images (PNG, JPG, JPEG, BMP, TIFF) and PDF documents
- **Automatic Classification**: Identifies document types using keyword-based scoring
- **Field Extraction**: Extracts relevant fields specific to each document type
- **Dual Interface**: 
  - Streamlit web application for interactive document processing
  - Flask web application with SQLite database for persistent storage
- **Supported Document Types**:
  - Driving License
  - Passport
  - W2 Tax Forms
  - Paystubs
  - Flood Certificates

## Project Structure

```
3N-OCR-pipeline/
├── main.py                 # Core OCR and extraction pipeline
├── streamlit_app.py        # Streamlit web interface
├── webApp/                 # Flask web application
│   ├── app.py             # Flask routes and handlers
│   ├── database.py        # SQLite database operations
│   ├── templates/         # HTML templates
│   └── static/            # CSS and static files
├── documents-used/         # Sample documents for testing
└── extracted_data.db       # SQLite database (created at runtime)
```

## Prerequisites

- Python 3.7+
- Tesseract OCR installed on your system
  - **Windows**: Download from [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - **Linux**: `sudo apt-get install tesseract-ocr`
  - **macOS**: `brew install tesseract`

## Required Python Packages

```
pillow
pytesseract
pdf2image
streamlit
flask
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ShekhawaTTiku/3N-OCR-pipeline.git
cd 3N-OCR-pipeline
```

2. Install required packages:
```bash
pip install pillow pytesseract pdf2image streamlit flask
```

3. Update the Tesseract path in `main.py` (line 9) to match your installation:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Usage

### Command Line Processing

To process all documents in a folder:

1. Update the `DOCS_FOLDER` path in `main.py` (line 12)
2. Run:
```bash
python main.py
```

### Streamlit Web Application

Launch the interactive Streamlit interface:
```bash
streamlit run streamlit_app.py
```

Features:
- Upload documents via drag-and-drop
- View OCR text and extracted fields
- Download results as JSON
- View processing history

### Flask Web Application

Run the Flask server with database storage:

1. Navigate to the webApp directory
2. Run:
```bash
python app.py
```
3. Open your browser to `http://localhost:5000`

Features:
- Upload and process documents
- Stores results in SQLite database
- View extracted information in HTML tables

## How It Works

### 1. OCR (Optical Character Recognition)
- Converts images directly to text using Tesseract
- Converts PDF first page to image, then extracts text

### 2. Document Classification
- Uses keyword-based scoring system
- Matches document content against predefined keywords for each type
- Assigns the document type with the highest score

### 3. Field Extraction
- Applies document-specific regex patterns
- Extracts relevant information based on document type:
  - **Driving License**: DL Number, DOB, Name
  - **Passport**: Passport Number, Country, Name
  - **W2**: EIN, Year, Employee Name
  - **Paystub**: Net Pay, Employee Name, Employer Name
  - **Flood Certificate**: Borrower Name, Customer Number, Expiry Date

## Configuration

### Tesseract Path
Update in `main.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"/path/to/tesseract"
```

### Document Folder
Update in `main.py`:
```python
DOCS_FOLDER = r"/path/to/your/documents"
```

### Upload Directory (Streamlit)
Automatically created in the project directory as `uploads/`

## Database Schema

The SQLite database stores processed documents with the following structure:

```sql
documents (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    doc_type TEXT,
    fields_json TEXT,
    created_at TIMESTAMP
)
```

## Sample Documents

The `documents-used/` folder contains sample documents for testing:
- Doc1.jpg - W2 Form
- Doc2.jpg - Passport
- Doc3.png - Driving License
- Doc4.pdf - Paystub
- Doc5.pdf - Flood Certificate

## Limitations

- Only processes the first page of PDF documents
- Accuracy depends on image/document quality
- Tesseract path must be configured correctly
- Classification is based on keyword matching (not ML-based)

## Future Enhancements

- Multi-page PDF support
- Machine learning-based classification
- Additional document types
- Improved field extraction accuracy
- User authentication for Flask app
- Document management dashboard

## Contributing

Feel free to fork this repository and submit pull requests for improvements.

## License

This project is available for educational and personal use.

## Support

For issues or questions, please open an issue on the GitHub repository.
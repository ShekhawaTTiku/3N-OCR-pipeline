# webApp - Flask Web Application

## Overview

This folder contains a Flask-based web application that provides a user-friendly interface for the OCR document processing pipeline. It includes database storage capabilities using SQLite to persist processed document information.

## Components

### app.py
The main Flask application file that handles:
- Web server configuration
- Route definitions
- File upload handling
- Integration with the main OCR pipeline
- Database operations coordination

**Key Routes:**
- `/` - Home page with file upload form
- `/process` (POST) - Processes uploaded documents and stores results

**Features:**
- File upload with validation
- Integration with main.py OCR pipeline
- Automatic database storage of results
- HTML template rendering for results display

### database.py
Database management module that handles:
- SQLite database initialization
- Table schema creation
- Data insertion operations

**Database Schema:**
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    doc_type TEXT,
    fields_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Functions:**
- `init_db()` - Creates the database and tables if they don't exist
- `save_to_db(filename, doc_type, fields)` - Saves document processing results

## Folder Structure

```
webApp/
├── app.py              # Main Flask application
├── database.py         # Database operations
├── templates/          # HTML templates
│   ├── index.html     # Upload form page
│   └── result.html    # Results display page
└── static/            # Static files (CSS, JS, images)
    └── style.css      # Stylesheet (currently empty)
```

## Installation & Setup

1. Ensure you have Flask installed:
```bash
pip install flask
```

2. Update the `BASE_DIR` path in `app.py` (line 13) to match your project location:
```python
BASE_DIR = r"D:\PYTHON\3N mini hackathon"
```

3. The application will automatically:
   - Create an `uploads/` directory for temporary file storage
   - Initialize the SQLite database (`extracted_data.db`) in the parent directory

## Running the Application

1. Navigate to the webApp directory:
```bash
cd webApp
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Flow

1. **Upload**: Visit the home page and select a document (image or PDF)
2. **Process**: Click "Extract" to process the document
3. **View Results**: See the extracted information displayed in a table
4. **Database Storage**: Results are automatically saved to the database

## API Endpoints

### GET /
- **Description**: Displays the file upload form
- **Returns**: HTML page with upload interface

### POST /process
- **Description**: Processes uploaded document
- **Parameters**: 
  - `file` (multipart/form-data): Document file to process
- **Returns**: HTML page with extracted results
- **Side Effects**: Saves results to database

## Database Location

The SQLite database file `extracted_data.db` is created in the parent directory:
```
3N-OCR-pipeline/
├── extracted_data.db    # SQLite database
└── webApp/
    └── app.py
```

## Configuration

### Upload Folder
Files are temporarily stored in:
```python
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
```

### Database Path
Configured in `database.py`:
```python
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "extracted_data.db")
```

## Error Handling

The application includes basic error handling for:
- Missing file in upload
- Empty filename
- Processing failures (try-except in main pipeline)

## Dependencies

- **Flask**: Web framework
- **main.py**: Core OCR and extraction pipeline
- **sqlite3**: Database operations (Python standard library)

## Features

- ✅ Simple, clean web interface
- ✅ File upload with drag-and-drop support
- ✅ Automatic document classification
- ✅ Field extraction based on document type
- ✅ Persistent storage in SQLite database
- ✅ Results displayed in formatted HTML tables
- ✅ Navigation between upload and results pages

## Limitations

- No user authentication
- No file size limits enforced
- No file type validation on the server side
- Database grows indefinitely (no cleanup mechanism)
- No pagination for viewing stored documents
- No search or filter capabilities

## Future Enhancements

- Add user authentication and authorization
- Implement document management dashboard
- Add search and filter functionality
- Implement pagination for results viewing
- Add file size and type validation
- Include image preview before processing
- Add batch processing capability
- Implement document deletion from database
- Add export functionality (CSV, Excel)
- Improve error messages and user feedback

## Troubleshooting

### Import Error for main.py
Ensure the `BASE_DIR` path is correct and points to the directory containing `main.py`.

### Database Not Created
Check file permissions in the parent directory where `extracted_data.db` should be created.

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Tesseract Not Found
Update the Tesseract path in the parent `main.py` file to match your system installation.

## Security Notes

⚠️ **Important**: This application is designed for development/testing purposes:
- Debug mode is enabled (`debug=True`)
- No input sanitization for filenames
- No file size limits
- No CSRF protection
- Uploaded files are stored without encryption

For production use, implement proper security measures including:
- Disable debug mode
- Add CSRF protection
- Implement file validation and sanitization
- Add rate limiting
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization
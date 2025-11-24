# Templates - HTML Templates for Flask App

## Overview

This folder contains HTML templates used by the Flask web application to render the user interface. The templates use Jinja2 templating engine, which is Flask's default template system.

## Files

### index.html
The main landing page and file upload interface.

**Purpose:**
- Displays the document upload form
- Entry point for users to submit documents for processing

**Features:**
- Simple HTML form with file input
- Accepts document uploads via file selection
- POST request to `/process` endpoint
- Basic inline styling (white background, black text, Arial font)

**Form Elements:**
- File input field (required)
- Submit button labeled "Extract"
- Uses `multipart/form-data` encoding for file uploads

**Design:**
- Minimal, functional design
- Inline CSS styling
- 40px padding for comfortable spacing
- 16px font size for readability

### result.html
The results display page showing extracted information.

**Purpose:**
- Displays processed document information
- Shows extracted fields in a structured format

**Features:**
- Dynamic content rendering using Jinja2 templates
- Displays filename and detected document type
- Table format for extracted fields
- Link to return to upload page

**Template Variables:**
- `{{ filename }}` - Name of the processed document
- `{{ doc_type }}` - Classified document type
- `{{ fields }}` - Dictionary of extracted field-value pairs

**Display Format:**
```
File: [filename]
Document Type: [doc_type]

+------------------+------------------+
| Field            | Value            |
+------------------+------------------+
| [key]            | [value]          |
| ...              | ...              |
+------------------+------------------+
```

**Navigation:**
- "Upload another document" link returns to home page

## Jinja2 Template Syntax Used

### Variable Rendering
```html
{{ variable_name }}
```
Renders the value of a variable passed from Flask.

### Loop Iteration
```html
{% for key, value in fields.items() %}
    <tr>
        <td>{{ key }}</td>
        <td>{{ value }}</td>
    </tr>
{% endfor %}
```
Iterates through the fields dictionary to display all extracted data.

## Styling

Both templates use inline CSS with consistent styling:
- **Background**: White (`#fff`)
- **Text Color**: Black (`#000`)
- **Font**: Arial, sans-serif
- **Padding**: 40px around content
- **Font Size**: 16px for form elements

## Usage in Flask

### Rendering index.html
```python
@app.route("/")
def index():
    return render_template("index.html")
```

### Rendering result.html with data
```python
@app.route("/process", methods=["POST"])
def process():
    # ... processing logic ...
    return render_template(
        "result.html",
        filename=file.filename,
        doc_type=doc_type,
        fields=fields
    )
```

## Customization Guide

### Adding Custom Styling

#### Option 1: Link External CSS
Add to the `<head>` section:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

#### Option 2: Add Internal Styles
Replace inline styles with a `<style>` block:
```html
<head>
    <style>
        body {
            background: #fff;
            color: #000;
            font-family: Arial, sans-serif;
            padding: 40px;
        }
    </style>
</head>
```

### Adding JavaScript

Add before closing `</body>` tag:
```html
<script src="{{ url_for('static', filename='script.js') }}"></script>
```

Or inline:
```html
<script>
    // Your JavaScript code
</script>
```

### Improving the Upload Form

Add file type restrictions:
```html
<input type="file" name="file" accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff" required>
```

Add drag-and-drop functionality:
```html
<div id="drop-zone">
    Drop files here or click to select
    <input type="file" name="file" id="file-input" required>
</div>
```

### Enhancing the Results Display

Add conditional rendering:
```html
{% if fields %}
    <table>
        {% for key, value in fields.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ value if value else 'N/A' }}</td>
            </tr>
        {% endfor %}
    </table>
{% else %}
    <p>No fields extracted.</p>
{% endif %}
```

Add download button:
```html
<button onclick="downloadResults()">Download JSON</button>
```

## Recommended Enhancements

### For index.html:
1. Add Bootstrap or Tailwind CSS for better styling
2. Include file preview before upload
3. Add file type icons
4. Implement drag-and-drop upload zone
5. Show loading spinner during upload
6. Add file size validation
7. Display upload progress bar

### For result.html:
1. Add copy-to-clipboard functionality
2. Implement JSON download button
3. Show confidence scores for classifications
4. Add edit functionality for extracted fields
5. Include document thumbnail preview
6. Add sharing options (email, export)
7. Show processing timestamp
8. Add button to save to database explicitly

## Template Inheritance (Future Enhancement)

Create a base template (`base.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}OCR Document Extractor{% endblock %}</title>
    {% block styles %}{% endblock %}
</head>
<body>
    <nav>
        <!-- Navigation bar -->
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <!-- Footer content -->
    </footer>
</body>
</html>
```

Then extend it in other templates:
```html
{% extends "base.html" %}

{% block title %}Upload Document{% endblock %}

{% block content %}
    <!-- Page-specific content -->
{% endblock %}
```

## Accessibility Improvements

1. Add proper labels:
```html
<label for="file-input">Select Document:</label>
<input type="file" id="file-input" name="file" required>
```

2. Add ARIA attributes:
```html
<button type="submit" aria-label="Extract document information">Extract</button>
```

3. Add semantic HTML:
```html
<main role="main">
    <section aria-labelledby="upload-heading">
        <h2 id="upload-heading">Upload Document</h2>
        <!-- Form content -->
    </section>
</main>
```

## Browser Compatibility

Both templates use standard HTML5 and should work in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Opera (latest)
- ✅ Internet Explorer 11+ (with polyfills)

## Testing

### Manual Testing Checklist:
- [ ] Upload form displays correctly
- [ ] File selection works
- [ ] Submit button triggers processing
- [ ] Results page displays all extracted fields
- [ ] Return link navigates back to upload page
- [ ] Table formatting is correct
- [ ] Special characters in fields display properly
- [ ] Empty/null values are handled gracefully

## Security Considerations

⚠️ **Current Limitations:**
- No CSRF token in forms
- No input sanitization for display
- Inline JavaScript should be avoided (XSS risk)

**Recommendations:**
```html
<!-- Add CSRF protection -->
<form method="POST" action="/process">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <!-- other fields -->
</form>
```

```html
<!-- Escape output (Jinja2 does this by default) -->
{{ filename | e }}
```

## File Locations

These templates should be placed in:
```
webApp/templates/
├── index.html
└── result.html
```

Flask automatically looks for templates in the `templates/` folder relative to the Flask app location.
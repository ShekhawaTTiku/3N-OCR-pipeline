# Static - Static Files for Flask Web Application

## Overview

This folder contains static assets (CSS, JavaScript, images, fonts) used by the Flask web application. Static files are served directly by Flask and don't require server-side processing.

## Current Contents

### style.css
Currently an empty stylesheet file. This is where custom CSS styles for the web application should be added.

**Purpose:**
- Centralized styling for the Flask web interface
- Separates presentation from HTML structure
- Allows for consistent theming across all pages

**Current Status:** Empty - ready for customization

## Folder Structure

```
webApp/static/
├── style.css          # Main stylesheet (currently empty)
└── readme             # Placeholder file
```

## Using Static Files in Flask

### In Templates

To reference static files in your HTML templates, use Flask's `url_for()` function:

#### CSS Files
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

#### JavaScript Files
```html
<script src="{{ url_for('static', filename='script.js') }}"></script>
```

#### Images
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

### Recommended Folder Organization

```
webApp/static/
├── css/
│   ├── style.css
│   ├── theme.css
│   └── responsive.css
├── js/
│   ├── main.js
│   ├── upload.js
│   └── validation.js
├── images/
│   ├── logo.png
│   ├── favicon.ico
│   └── icons/
├── fonts/
│   └── custom-fonts/
└── vendor/
    ├── bootstrap/
    └── jquery/
```

## Recommended CSS Additions

### style.css Template

Here's a recommended structure for `style.css`:

```css
/* ===== CSS VARIABLES ===== */
:root {
    --primary-color: #4A90E2;
    --secondary-color: #50E3C2;
    --background-color: #F5F7FA;
    --text-color: #333333;
    --border-color: #E1E8ED;
    --success-color: #4CAF50;
    --error-color: #F44336;
    --font-main: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ===== GLOBAL STYLES ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-main);
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    padding: 20px;
}

/* ===== CONTAINERS ===== */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* ===== HEADER ===== */
h1, h2, h3 {
    color: var(--primary-color);
    margin-bottom: 20px;
}

/* ===== FORMS ===== */
form {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

input[type="file"] {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 2px dashed var(--border-color);
    border-radius: 4px;
    cursor: pointer;
}

button[type="submit"] {
    background-color: var(--primary-color);
    color: white;
    padding: 12px 30px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

button[type="submit"]:hover {
    background-color: #357ABD;
}

/* ===== TABLES ===== */
table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}

th, td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

th {
    background-color: var(--primary-color);
    color: white;
    font-weight: 600;
}

tr:hover {
    background-color: #F9F9F9;
}

/* ===== LINKS ===== */
a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.3s;
}

a:hover {
    color: var(--secondary-color);
    text-decoration: underline;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    form {
        padding: 20px;
    }
    
    table {
        font-size: 14px;
    }
}
```

## JavaScript Recommendations

### upload.js - File Upload Enhancement

```javascript
// Drag and Drop functionality
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    fileInput.files = files;
    
    displayFileName(files[0].name);
});

// File validation
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        if (validateFile(file)) {
            displayFileName(file.name);
        } else {
            alert('Please select a valid file type (PDF, PNG, JPG, etc.)');
            fileInput.value = '';
        }
    }
});

function validateFile(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff', 'application/pdf'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    return validTypes.includes(file.type) && file.size <= maxSize;
}

function displayFileName(name) {
    console.log('Selected file:', name);
    // Update UI to show selected file
}
```

### results.js - Results Page Enhancement

```javascript
// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
    });
}

// Download results as JSON
function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
```

## Image Assets

### Recommended Images to Add:

1. **Logo**: `images/logo.png`
   - Application branding
   - Displayed in header

2. **Favicon**: `images/favicon.ico`
   - Browser tab icon
   - 16x16 or 32x32 pixels

3. **Document Icons**: `images/icons/`
   - `pdf-icon.png`
   - `image-icon.png`
   - `success-icon.png`
   - `error-icon.png`

4. **Loading Animations**: `images/loading/`
   - `spinner.gif`
   - `loading-dots.gif`

### Using Favicon

Add to your HTML template `<head>`:
```html
<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='images/favicon.ico') }}">
```

## Third-Party Libraries

### Recommended Libraries to Add:

#### 1. Bootstrap (CSS Framework)
Download and place in `static/vendor/bootstrap/`
```html
<link rel="stylesheet" href="{{ url_for('static', filename='vendor/bootstrap/css/bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js') }}"></script>
```

Or use CDN:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

#### 2. Font Awesome (Icons)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

#### 3. jQuery (JavaScript Library)
```html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

## Flask Configuration

To serve static files, Flask uses this default configuration:

```python
app = Flask(__name__)
# Static folder is 'static' by default
# Static URL path is '/static' by default
```

### Custom Static Folder
```python
app = Flask(__name__, static_folder='assets', static_url_path='/assets')
```

### Caching Static Files

For production, enable caching in Flask:
```python
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year
```

## Best Practices

### 1. File Organization
- Group related files together (CSS in css/, JS in js/)
- Use descriptive filenames
- Version your files (e.g., `style-v1.2.css`)

### 2. Performance
- Minify CSS and JavaScript files
- Compress images
- Use CSS sprites for icons
- Implement lazy loading for images

### 3. Versioning
Add version query strings to bust cache:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}?v=1.2">
```

### 4. Security
- Don't store sensitive data in static files
- Validate all uploaded files before storing
- Use HTTPS in production

## File Size Guidelines

- **CSS**: Keep under 100KB per file
- **JavaScript**: Keep under 200KB per file
- **Images**: 
  - Logos: Under 50KB
  - Icons: Under 20KB each
  - Photos: Under 500KB

## Common Static File Types

```
Static Files
├── Stylesheets (.css)
├── JavaScript (.js)
├── Images
│   ├── .png
│   ├── .jpg
│   ├── .gif
│   ├── .svg
│   └── .ico
├── Fonts
│   ├── .woff
│   ├── .woff2
│   └── .ttf
├── Documents
│   └── .pdf
└── Data
    ├── .json
    └── .xml
```

## Development vs Production

### Development
- Use unminified files for easier debugging
- Include source maps
- Disable caching

### Production
- Minify all CSS and JavaScript
- Enable caching with proper expiration headers
- Use a CDN for common libraries
- Compress images
- Consider using a static file server (nginx)

## Testing Static Files

### Manual Testing
1. Check if files load in browser
2. Verify correct MIME types
3. Test on different browsers
4. Check mobile responsiveness

### Automated Testing
```python
def test_static_file_exists():
    response = client.get('/static/style.css')
    assert response.status_code == 200
```

## Troubleshooting

### Static Files Not Loading
1. Check file path is correct
2. Verify static folder configuration
3. Clear browser cache
4. Check Flask logs for 404 errors

### CSS Not Applying
1. Check link tag in HTML
2. Verify CSS syntax
3. Check browser console for errors
4. Ensure correct specificity in CSS selectors

### Images Not Displaying
1. Verify image path
2. Check image file exists
3. Verify image format is supported
4. Check file permissions

## Future Enhancements

- [ ] Add custom theme switcher (light/dark mode)
- [ ] Implement responsive navigation
- [ ] Add loading animations
- [ ] Create custom icon set
- [ ] Add print-friendly styles
- [ ] Implement PWA assets (manifest, service worker)
- [ ] Add accessibility features (high contrast mode)
- [ ] Create style guide documentation
# documents-used - Sample Documents for Testing

## Overview

This folder contains sample documents used for testing and demonstrating the OCR pipeline's capabilities. These documents represent the five different document types that the system can process and classify.

## Sample Documents

### Doc1.jpg - W2 Tax Form
**Document Type:** W2 Tax Form (Wage and Tax Statement)

**Description:**
- IRS Form W-2 showing employee wages and tax withholdings
- Contains employer and employee information
- Displays various tax-related fields

**Extracted Fields:**
- `EIN` - Employer Identification Number (format: XX-XXXXXXX)
- `Year` - Tax year (e.g., 2022)
- `Employee Name` - Full name of the employee

**Sample Use Case:**
- Tax filing verification
- Employment income verification
- Loan applications
- Financial record keeping

**Format:** JPG image file

---

### Doc2.jpg - Passport
**Document Type:** United States Passport

**Description:**
- US passport identification document
- Contains personal identification information
- Includes Machine Readable Zone (MRZ) at the bottom

**Extracted Fields:**
- `Passport number` - 9-digit passport number
- `Country` - United States of America or USA
- `Name` - Full name (First Last) extracted from surname and given names

**Sample Use Case:**
- Identity verification
- International travel documentation
- Age verification
- Citizenship verification

**Format:** JPG image file

---

### Doc3.png - Driving License
**Document Type:** Arizona Driver License

**Description:**
- State-issued driver's license
- Contains driver identification and licensing information
- Includes physical characteristics and class designation

**Extracted Fields:**
- `DL number` - Driver License Number (format: D followed by 8-9 digits)
- `DOB` - Date of Birth (format: MM/DD/YYYY)
- `Name` - Driver's full name

**Sample Use Case:**
- Identity verification
- Age verification
- Address verification
- Driving privileges confirmation

**Format:** PNG image file

---

### Doc4.pdf - Paystub
**Document Type:** Employee Paystub

**Description:**
- Payroll document showing earnings and deductions
- From Avalon Accounting Inc
- Contains current and year-to-date information

**Extracted Fields:**
- `Net Pay` - Take-home pay amount
- `Employee Name` - Name of the employee
- `Employer Name` - Name of the employer (e.g., Avalon Accounting Inc)

**Sample Use Case:**
- Income verification
- Loan applications
- Rental applications
- Employment verification

**Format:** PDF document

---

### Doc5.pdf - Flood Certificate
**Document Type:** Standard Flood Hazard Determination Form

**Description:**
- FEMA flood zone determination document
- Property flood risk assessment
- Required for mortgage and insurance purposes

**Extracted Fields:**
- `Borrower name` - Name of the property owner/borrower
- `Customer No` - Customer identification number
- `Expire date` - Certificate expiration date (format: MM-DD-YYYY)

**Sample Use Case:**
- Property insurance
- Mortgage applications
- Real estate transactions
- Flood risk assessment

**Format:** PDF document

---

## Document Classification

The OCR pipeline uses keyword-based scoring to classify documents:

### Classification Keywords

| Document Type | Key Identifying Terms |
|---------------|----------------------|
| **Driving License** | driver license, DLN, class d, veteran, donor |
| **Passport** | passport, surname, given names, nationality, place of birth |
| **W2** | w-2, wage and tax statement, employer identification number, federal income tax withheld |
| **Paystub** | paystub, gross pay, net pay, year-to-date, deductions, income |
| **Flood Certificate** | flood, FEMA, national flood insurance, flood hazard determination |

## Using These Documents

### With main.py
1. Update the `DOCS_FOLDER` path in `main.py`:
```python
DOCS_FOLDER = r"/path/to/documents-used"
```

2. Run the script:
```bash
python main.py
```

### With Streamlit App
1. Launch the app:
```bash
streamlit run streamlit_app.py
```

2. Upload any of these sample documents through the web interface

### With Flask App
1. Start the Flask server:
```bash
cd webApp
python app.py
```

2. Navigate to `http://localhost:5000` and upload a document

## Expected Results

### Doc1.jpg (W2)
```json
{
  "EIN": "12-3456789",
  "Year": "2022",
  "Employee Name": "John Doe"
}
```

### Doc2.jpg (Passport)
```json
{
  "Passport number": "123456789",
  "Country": "United States of America",
  "Name": "John Smith"
}
```

### Doc3.png (Driving License)
```json
{
  "DL number": "D12345678",
  "DOB": "01/15/1985",
  "Name": "Jane Doe"
}
```

### Doc4.pdf (Paystub)
```json
{
  "Net Pay": "3,456.78",
  "Employee Name": "John Smith",
  "Employer Name": "Avalon Accounting Inc"
}
```

### Doc5.pdf (Flood Certificate)
```json
{
  "Borrower name": "John Doe",
  "Customer No": "12345",
  "Expire date": "12-31-2024"
}
```

*Note: Actual values will vary based on the content of the sample documents.*

## Document Quality Guidelines

For best OCR results, documents should:
- ✅ Have clear, legible text
- ✅ Be properly oriented (not rotated)
- ✅ Have good contrast between text and background
- ✅ Be at least 300 DPI resolution for scanned images
- ✅ Be free from excessive shadows or glare
- ✅ Have minimal background noise or artifacts

## Adding New Sample Documents

When adding new sample documents to this folder:

1. **Name Convention**: Use descriptive names (e.g., `Doc6-BankStatement.pdf`)
2. **Supported Formats**: PNG, JPG, JPEG, BMP, TIFF, PDF
3. **Privacy**: Ensure all personal information is either:
   - Fictional/synthetic data
   - Properly anonymized
   - Used with permission
4. **Documentation**: Update this README with document details

## File Information

| File | Type | Format | Size |
|------|------|--------|------|
| Doc1.jpg | W2 | JPG | Varies |
| Doc2.jpg | Passport | JPG | Varies |
| Doc3.png | Driving License | PNG | Varies |
| Doc4.pdf | Paystub | PDF | Varies |
| Doc5.pdf | Flood Certificate | PDF | Varies |

## Testing Coverage

These documents provide comprehensive testing for:
- ✅ Multiple image formats (JPG, PNG)
- ✅ PDF document processing
- ✅ Different document layouts and structures
- ✅ Various field extraction patterns
- ✅ Text recognition in different fonts and sizes
- ✅ Classification accuracy across all supported types

## Limitations

### OCR Accuracy
- Results depend on document quality
- Handwritten text may not be recognized
- Complex layouts may cause extraction errors
- Multi-column formats may be challenging

### PDF Processing
- Only the first page is processed
- Multi-page PDFs require modification to the code
- Some PDF formats may not convert properly

## Privacy and Security

⚠️ **Important Notes:**
- These are sample documents for demonstration purposes only
- Do not use real personal documents without proper authorization
- Ensure compliance with privacy regulations (GDPR, CCPA, etc.)
- Securely dispose of processed documents containing real information
- Do not commit real personal documents to version control

## Troubleshooting

### OCR Not Working
- **Issue**: No text extracted
- **Solution**: Check Tesseract installation and path configuration

### Wrong Classification
- **Issue**: Document classified incorrectly
- **Solution**: Document may not match expected patterns; review keyword lists in `main.py`

### Missing Fields
- **Issue**: Some fields not extracted
- **Solution**: Field extraction uses regex patterns; document format may vary from expected pattern

### PDF Conversion Errors
- **Issue**: PDF cannot be processed
- **Solution**: Ensure pdf2image and poppler are properly installed

## Support and Enhancement

### Reporting Issues
If sample documents are not being processed correctly:
1. Check document quality and format
2. Verify Tesseract installation
3. Review classification keywords in `main.py`
4. Update regex patterns for field extraction if needed

### Adding Support for New Document Types
To add support for additional document types:
1. Add sample document(s) to this folder
2. Add classification keywords in `classify_document()` function
3. Create extraction function for new document type
4. Update `extract_fields()` dispatcher
5. Document the new type in this README

## References

- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract
- **pdf2image**: https://github.com/Belval/pdf2image
- **pytesseract**: https://github.com/madmaze/pytesseract

## Version History

- **v1.0**: Initial set of 5 sample documents
  - W2 Tax Form
  - Passport
  - Driving License
  - Paystub
  - Flood Certificate
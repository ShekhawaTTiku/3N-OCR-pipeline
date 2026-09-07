import os
import shutil
from typing import Dict, Any

from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError
from pdf2image import convert_from_path

DEFAULT_WINDOWS_TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_CMD_ENV = "TESSERACT_CMD"
DOCS_FOLDER = os.getenv(
    "DOCS_FOLDER",
    os.path.join(os.path.dirname(__file__), "documents-used"),
)


def _configure_tesseract() -> None:
    env_cmd = os.getenv(TESSERACT_CMD_ENV)
    if env_cmd:
        pytesseract.pytesseract.tesseract_cmd = env_cmd
        return
    if os.path.exists(DEFAULT_WINDOWS_TESSERACT):
        pytesseract.pytesseract.tesseract_cmd = DEFAULT_WINDOWS_TESSERACT


def _raise_tesseract_runtime_error() -> None:
    configured_cmd = os.getenv(TESSERACT_CMD_ENV) or shutil.which("tesseract")
    details = (
        f" Current command/path: {configured_cmd}."
        if configured_cmd
        else " No Tesseract binary was detected on PATH."
    )
    raise RuntimeError(
        "Tesseract OCR binary is required but was not found. "
        "Install Tesseract on your system and ensure it is available on PATH, "
        f"or set the {TESSERACT_CMD_ENV} environment variable to the executable path."
        f"{details}"
    )


_configure_tesseract()


# ---------- STEP 1: LOAD FILE + OCR ----------

def ocr_file(path: str) -> str:
    """
    Take an image or PDF file and return extracted text.
    """
    ext = os.path.splitext(path)[1].lower()

    # For images
    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        image = Image.open(path)
        try:
            return pytesseract.image_to_string(image)
        except TesseractNotFoundError:
            _raise_tesseract_runtime_error()

    # For PDFs → convert first page to image
    elif ext == ".pdf":
        pages = convert_from_path(path, first_page=1, last_page=1)  # only page 1
        image = pages[0]
        try:
            return pytesseract.image_to_string(image)
        except TesseractNotFoundError:
            _raise_tesseract_runtime_error()

    else:
        raise ValueError(f"Unsupported file type: {ext}")


# ---------- STEP 2: CLASSIFY DOC TYPE (SCORING VERSION) ----------

def classify_document(text: str) -> str:
    t = text.lower()

    scores = {
        "Driving License": 0,
        "Passport": 0,
        "W2": 0,
        "Paystub": 0,
        "Flood Certificate": 0,
    }

    # ---- Driving License (Doc3) ----
    dl_keywords = [
        "driver license",
        "driver licence",
        "dln",
        "arizona",
        "veteran",
        "donor",
        "class d",
        "dl number",
    ]
    for kw in dl_keywords:
        if kw in t:
            scores["Driving License"] += 1

    # ---- Passport (Doc2) ----
    passport_keywords = [
        "passport",
        "passport number",
        "surname",
        "given name",
        "given names",
        "place of birth",
        "date of birth",
        "nationality",
        "see page 27",
        "usa",  # often appears on the passport
    ]
    for kw in passport_keywords:
        if kw in t:
            scores["Passport"] += 1

    # ---- W2 (Doc1) ----
    w2_keywords = [
        "w-2",
        "form w-2",
        "form w 2",
        "w2 ",
        "wage and tax statement",
        "wages, tips, other compensation",
        "wage and tax",
        "federal income tax withheld",
        "social security wages",
        "employer identification number",
    ]
    for kw in w2_keywords:
        if kw in t:
            scores["W2"] += 1

    # ---- Paystub (Doc4) ----
    paystub_keywords = [
        "pay stub",
        "paystub",
        "gross pay",
        "net pay",
        "year-to-date",
        "year to date",
        "current amount",
        "deductions",
        "avalon",
        "pay date",
        "income",
    ]
    for kw in paystub_keywords:
        if kw in t:
            scores["Paystub"] += 1

    # ---- Flood Certificate (Doc5) ----
    flood_keywords = [
        "flood",
        "fema",
        "standard flood hazard determination form",
        "flood hazard determination",
        "national flood insurance",
        "nfip",
        "flood insurance",
        "loan information",
        "apn/tax id",
    ]
    for kw in flood_keywords:
        if kw in t:
            scores["Flood Certificate"] += 1

    # Decide best type
    best_type = max(scores, key=scores.get)
    if scores[best_type] == 0:
        return "Others"
    return best_type


# ---------- STEP 3: EXTRACT FIELDS (PLACEHOLDERS FOR NOW) ----------

import re
from typing import Dict, Any


# ---------------------------------------------------------
#   1. DRIVING LICENSE  (you already have this working)
# ---------------------------------------------------------
def extract_driving_license(text: str) -> Dict[str, Any]:
    data = {}
    normalized = text.replace("O", "0")

    # DL Number
    dl_match = re.search(r"\bD\s*[0-9]{8,9}\b", normalized)
    if dl_match:
        data["DL number"] = dl_match.group(0).replace(" ", "")
    else:
        dl2 = re.search(r"DLN[:\s]*([D0-9\s]{9,12})", normalized, re.IGNORECASE)
        data["DL number"] = dl2.group(1).replace(" ", "") if dl2 else None

    # DOB
    dob = re.search(r"DOB[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})", normalized)
    if dob:
        data["DOB"] = dob.group(1)
    else:
        dob2 = re.search(r"\b([0-9]{2}/[0-9]{2}/[0-9]{4})\b", normalized)
        data["DOB"] = dob2.group(1) if dob2 else None

    # NAME — auto-cleaning strategies
    blacklist = {
        "ARIZONA", "USA", "DRIVER", "LICENSE", "DONOR", "VETERAN",
        "CLASS", "END", "NONE", "REST", "EXP", "ISS", "SEX", "EYES",
        "HGT", "WGT", "HAIR", "BRO", "PHOENIX", "MAIN", "VERDE",
        "STREET", "NAG", "DEP", "VER"
    }

    name_candidates = []

    region = re.search(r"DRIVER\s*LICENSE(.*?)(?:DLN|D\s*[0-9]{8})",
                       normalized, re.S | re.IGNORECASE)
    if region:
        block = region.group(1)
        words = re.findall(r"\b[A-Z]{4,}\b", block)
        for w in words:
            if w not in blacklist:
                name_candidates.append(w)

    if not name_candidates:
        all_words = re.findall(r"\b[A-Z]{4,}\b", normalized)
        for w in all_words:
            if w not in blacklist:
                name_candidates.append(w)

    if len(name_candidates) >= 2:
        data["Name"] = f"{name_candidates[0].title()} {name_candidates[1].title()}"
    elif len(name_candidates) == 1:
        data["Name"] = name_candidates[0].title()
    else:
        data["Name"] = None

    return data



# ---------------------------------------------------------
#   2. PASSPORT (Doc2.jpg)
# ---------------------------------------------------------
def extract_passport(text: str) -> Dict[str, Any]:
    """
    Extract Name, Passport number, Country from US Passport.
    """
    data = {}
    t = text.replace("O", "0").replace("«", "").replace("»", "")

    # Passport Number — always 9 digits
    pp = re.search(r"\b([0-9]{9})\b", t)
    data["Passport number"] = pp.group(1) if pp else None

    # Country — usually 'United States of America' or 'USA'
    country = None
    if "united states" in t.lower():
        country = "United States of America"
    elif "usa" in t.lower():
        country = "USA"
    data["Country"] = country

    # Name extraction from MRZ (optional)
    # MRZ format: P<USA<LASTNAME<FIRSTNAME<<
    mrz = re.search(r"P<...<([A-Z<]+)<<([A-Z<]+)", t)
    if mrz:
        last = mrz.group(1).replace("<", " ").title()
        first = mrz.group(2).replace("<", " ").title()
        data["Name"] = f"{first} {last}"
        return data

    # Otherwise: extract printed name (Surname+Given Names)
    name = re.search(r"Surname[:\s]*([A-Za-z ]+)", t)
    given = re.search(r"Given Names?[:\s]*([A-Za-z ]+)", t)

    if name and given:
        data["Name"] = f"{given.group(1).title()} {name.group(1).title()}"
    else:
        # fallback: detect 2 long all-caps words
        words = re.findall(r"\b[A-Z]{3,}\b", t)
        if len(words) >= 2:
            data["Name"] = f"{words[0].title()} {words[1].title()}"
        else:
            data["Name"] = None

    return data



# ---------------------------------------------------------
#   3. W2 (Doc1.jpg)
# ---------------------------------------------------------
def extract_w2(text: str) -> Dict[str, Any]:
    data = {}

    # EIN
    ein = re.search(r"\b(\d{2}-\d{7})\b", text)
    data["EIN"] = ein.group(1) if ein else None

    # Year (W-2 2022)
    year = re.search(r"\b(20\d{2})\b", text)
    data["Year"] = year.group(1) if year else None

    # Employee Name (two words near "Employee's first name")
    name_block = re.search(r"Employee[’']?s first name.*?\n(.+?)\nLast name\s+([A-Za-z]+)", 
                           text, re.S | re.IGNORECASE)
    if name_block:
        data["Employee Name"] = (
            f"{name_block.group(1).strip()} {name_block.group(2).strip()}"
        )
    else:
        # fallback: first two Title Case words
        fallback = re.findall(r"\b[A-Z][a-z]+\b", text)
        data["Employee Name"] = f"{fallback[0]} {fallback[1]}" if len(fallback) >= 2 else None

    return data



# ---------------------------------------------------------
#   4. PAYSTUB (Doc4.pdf)
# ---------------------------------------------------------
def extract_paystub(text: str) -> Dict[str, Any]:
    data = {}

    # Net Pay
    net = re.search(r"Net Pay[:\s]*\$?([0-9,.]+)", text, re.IGNORECASE)
    data["Net Pay"] = net.group(1) if net else None

    # Employee Name — usually top-left, two words
    emp = re.findall(r"\b[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+\b", text)
    data["Employee Name"] = emp[0] if emp else None

    # Employer Name — from header (Avalon Accounting Inc)
    employer = re.search(r"(Avalon[ A-Za-z]*)", text)
    data["Employer Name"] = employer.group(1) if employer else None

    return data



# ---------------------------------------------------------
#   5. FLOOD CERTIFICATE (Doc5.pdf)
# ---------------------------------------------------------
def extract_flood(text: str) -> Dict[str, Any]:
    data = {}

    # Borrower name
    br = re.search(r"Borrower[:\s]*([A-Za-z ,]+)", text)
    data["Borrower name"] = br.group(1).strip() if br else None

    # Customer Number
    cust = re.search(r"Customer Number[:\s]*([0-9]+)", text)
    data["Customer No"] = cust.group(1) if cust else None

    # Expire Date
    exp = re.search(r"Expires[:\s]*([0-9]{2}-[0-9]{2}-[0-9]{4})", text)
    data["Expire date"] = exp.group(1) if exp else None

    return data



# ---------------------------------------------------------
#   MAIN DISPATCHER
# ---------------------------------------------------------
def extract_fields(doc_type: str, text: str) -> Dict[str, Any]:

    if doc_type == "Driving License":
        return extract_driving_license(text)

    if doc_type == "Passport":
        return extract_passport(text)

    if doc_type == "W2":
        return extract_w2(text)

    if doc_type == "Paystub":
        return extract_paystub(text)

    if doc_type == "Flood Certificate":
        return extract_flood(text)

    return {}


# ---------- MAIN PIPELINE ----------

def process_all_documents(docs_folder: str = DOCS_FOLDER):
    print("\n=== Starting Document Processing Pipeline ===")
    print(f"Looking inside: {docs_folder}\n")

    results = []

    if not os.path.isdir(docs_folder):
        print(
            f"Document folder not found: {docs_folder}. "
            "Set DOCS_FOLDER env var or pass a valid folder path."
        )
        return results

    for filename in os.listdir(docs_folder):
        path = os.path.join(docs_folder, filename)

        # Skip folders, just process actual files
        if not os.path.isfile(path):
            continue

        print(f"Processing: {filename}")

        # OCR
        try:
            text = ocr_file(path)
        except Exception as e:
            print(f"  OCR failed for {filename}: {e}")
            continue

        # Classification
        doc_type = classify_document(text)
        print(f"  Detected Type: {doc_type}")

        # Extract fields (currently placeholders)
        fields = extract_fields(doc_type, text)
        print(f"  Extracted Fields: {fields}")

        results.append({
            "file_name": filename,
            "doc_type": doc_type,
            "fields": fields,
        })

        print("--------------------------------------------------")

    return results


if __name__ == "__main__":
    final_data = process_all_documents()

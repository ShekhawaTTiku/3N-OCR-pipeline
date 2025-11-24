import json
import os
from pathlib import Path
from typing import Dict, Any

import streamlit as st

import main  # reuse OCR + extraction pipeline


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "bmp", "tiff", "tif", "pdf"]


def run_pipeline(file_path: Path) -> Dict[str, Any]:
    """Run OCR → classify → extract pipeline on the given file."""
    text = main.ocr_file(str(file_path))
    doc_type = main.classify_document(text)
    fields = main.extract_fields(doc_type, text)
    return {"text": text, "doc_type": doc_type, "fields": fields}


def save_uploaded_file(uploaded_file) -> Path:
    target_path = UPLOAD_DIR / uploaded_file.name
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return target_path


def render_result(filename: str, doc_type: str, fields: Dict[str, Any], text: str):
    st.subheader("Result")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Detected Type", value=doc_type)
        st.caption(filename)
        st.download_button(
            label="Download extracted JSON",
            data=json.dumps(fields, indent=2),
            file_name=f"{Path(filename).stem}_fields.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.markdown("**Extracted Fields**")
        if fields:
            field_rows = [{"Field": k, "Value": v or "—"} for k, v in fields.items()]
            st.dataframe(field_rows, hide_index=True, use_container_width=True)
        else:
            st.info("No structured fields were extracted for this document.")

    with st.expander("View OCR Text"):
        st.text(text.strip() or "(No text detected)")


def render_history():
    history = st.session_state.get("runs", [])
    if not history:
        return

    st.markdown("### Recent Runs")
    for run in history[:5]:
        with st.expander(f"{run['filename']} · {run['doc_type']}"):
            st.json(run["fields"])


def main_page():
    st.set_page_config(
        page_title="Document Intelligence",
        page_icon="📄",
        layout="wide",
    )

    st.title("📄 Document Intelligence Workspace")
    st.write(
        "Upload a document to automatically OCR, classify, and capture key fields."
    )

    with st.sidebar:
        st.header("How it works")
        st.markdown(
            """
1. **Upload** a PDF or image  
2. We **OCR** the first page (Tesseract)  
3. Text is **classified** into a known document type  
4. Type-specific **fields** are extracted and displayed  
            """
        )
        st.caption("Supported types: Driving License, Passport, W2, Paystub, Flood Certificate.")

    uploaded_file = st.file_uploader(
        "Drop a file or click to browse",
        type=ALLOWED_EXTENSIONS,
        accept_multiple_files=False,
        help="PNG, JPG, TIFF, BMP, or PDF",
    )

    if uploaded_file is None:
        render_history()
        return

    with st.spinner("Processing document..."):
        saved_path = save_uploaded_file(uploaded_file)
        try:
            result = run_pipeline(saved_path)
        except Exception as exc:
            st.error(f"Processing failed: {exc}")
            return

    run_record = {
        "filename": uploaded_file.name,
        "doc_type": result["doc_type"],
        "fields": result["fields"],
    }
    st.session_state.setdefault("runs", []).insert(0, run_record)

    render_result(
        filename=uploaded_file.name,
        doc_type=result["doc_type"],
        fields=result["fields"],
        text=result["text"],
    )

    render_history()


if __name__ == "__main__":
    main_page()


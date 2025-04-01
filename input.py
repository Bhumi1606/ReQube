import os
import subprocess
import logging
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for DOCX files
import pytesseract  # OCR for images
from PIL import Image  # Image processing
from langdetect import detect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Tesseract path manually (if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Define a constant for OCR languages
OCR_LANGUAGES = "eng+mar+hin+tam+tel+guj+kan+ben+ori+pan+fra+spa+deu+chi_sim+jpn+rus+ara"


def extract_text_from_pdf(pdf_path, lang=OCR_LANGUAGES):
    """Extracts text from a PDF file using built-in extraction first, then OCR if needed."""
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document[page_num]
            page_text = page.get_text("text")
            if page_text.strip():
                text += page_text + "\n"
            else:
                # Increase DPI for better OCR
                img = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                image = Image.frombytes("RGB", [img.width, img.height], img.samples)
                text += pytesseract.image_to_string(image, lang=lang) + "\n"
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
        return None


def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join(para.text for para in doc.paragraphs)
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {docx_path}: {e}")
        return None


def extract_text_from_doc(doc_path):
    """Extracts text from a DOC (Word 97-2003) file using catdoc."""
    try:
        result = subprocess.run(["catdoc", doc_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        logging.error(f"Error extracting text from {doc_path}: {e}")
        return None


def extract_text_from_txt(txt_path):
    """Extracts text from a TXT file."""
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error extracting text from {txt_path}: {e}")
        return None


def extract_text_from_image(image_path, lang=OCR_LANGUAGES):
    """Extracts text from an image file using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        logging.error(f"Error extracting text from {image_path}: {e}")
        return None


def detect_language(text):
    """Detects the language of the extracted text."""
    try:
        clean_text = " ".join(text.split())  # Remove extra whitespace
        return detect(clean_text) if len(clean_text) > 10 else "unknown"
    except Exception as e:
        logging.error(f"Error detecting language: {e}")
        return "unknown"


def extract_text(file_path):
    """Determines file type and extracts text accordingly."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    text = None
    if file_extension == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        text = extract_text_from_docx(file_path)
    elif file_extension == ".doc":
        text = extract_text_from_doc(file_path)
    elif file_extension == ".txt":
        text = extract_text_from_txt(file_path)
    elif file_extension in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = extract_text_from_image(file_path)
    else:
        logging.error("Unsupported file format.")
        return None

    if text and file_extension not in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        detected_lang = detect_language(text)
        logging.info(f"Detected Language: {detected_lang}")

    return text


# Example Usage
if __name__ == "__main__":
    file_path = "C:/Projects/Null_Pointers/ReQube/input_file.png"  # Update file path as needed
    text_output = extract_text(file_path)
    if text_output:
        print(text_output)  # Or further process the extracted text

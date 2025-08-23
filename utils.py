import re
import dateparser
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename

def save_file(file, upload_folder):
    filename = secure_filename(file.filename)
    filepath = f"{upload_folder}/{filename}"
    file.save(filepath)
    return filepath, filename

def image_ocr(filepath):
    return pytesseract.image_to_string(Image.open(filepath))

def extract_date(text):
    date_patterns =[
        "\b\d{2}[/-]\d{2}[/-]\d{2,4}\b",
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}",
        r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}",
        r"(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[a-z]*\s+\d{1,2},?\s+\d{2,4}",
        r"\d{1,2}\s+(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[a-z]*\s+\d{2,4}"

    ]

    matches = []
    for pattern in date_patterns:
        found = re.findall(pattern, text, flags=re.IGNORECASE)
        matches.extend(found)
    return matches

def parse_dates(date_strings):
    parsed_dates = []
    for ds in date_strings:
        parsed = dateparser.parse(ds, languages=["en", "fr"], settings={"DATE_ORDER": "DMY"})
        if parsed:
            parsed_dates.append(parsed.strftime("%m-%d-%-Y"))
    return list(set(parsed_dates))  
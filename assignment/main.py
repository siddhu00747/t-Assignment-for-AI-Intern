# run.py
from src.extract import extract_raw_pages
from src.parse import extract_to_schema
from src.utils import write_output

PDF = "Data Input.pdf"
OUT_XLSX = "output/Output1.xlsx"

def main():
    print("Extracting text from PDF...")
    pages = extract_raw_pages(PDF, use_ocr_if_empty=True)
    print(f"Pages extracted: {len(pages)}")

    print("Parsing content to schema...")
    rows = extract_to_schema(pages)

    print("Writing Excel...")
    write_output(rows, OUT_XLSX)

    print("Done. Output saved to:", OUT_XLSX)

if __name__ == "__main__":
    main()

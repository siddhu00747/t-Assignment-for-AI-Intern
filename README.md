# 📄 PDF to Structured Excel Extractor

This project automatically extracts structured information from a candidate’s descriptive PDF profile and converts it into a clean **37-row standardized Excel output** following a fixed schema.

The solution uses:
- **Custom NLP parsing logic** (regex + rule-based extraction)
- **Streamlit UI** for PDF upload & preview
- **PyPDF2** for PDF reading
- **Pandas + OpenPyXL** for generating Excel output

---

## 🚀 Features

### ✔ 1. Upload PDF  
Upload any candidate profile written in paragraph or free-text format.

### ✔ 2. Automatic Extraction  
The system auto-extracts key fields including:
- Personal details  
- Education  
- Employment history  
- Certifications  
- Technical skills  

Matches exactly **37 fields** in the expected HR schema.

### ✔ 3. Excel Export  
After extraction, user can download:
- `output.xlsx` — clean, structured dataset ready for processing.

### ✔ 4. Streamlit Web Interface  
Easy UI for:
- Uploading PDF  
- Previewing extracted table  
- Downloading Excel  

---

## 📁 Project Structure


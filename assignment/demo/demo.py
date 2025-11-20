import streamlit as st
import pandas as pd
from src.parse import extract_to_schema
from PyPDF2 import PdfReader
import io

st.set_page_config(page_title="PDF → Excel Extractor", layout="wide")

st.title("📄 PDF to Structured Excel Extractor")
st.write("Upload a profile PDF and get a clean 37-row structured Excel output.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully!")

    reader = PdfReader(uploaded_file)
    pages = []

    # Extract text page-wise (same as your main script)
    for page in reader.pages:
        pages.append({"text": page.extract_text()})

    # Use your extraction function
    rows = extract_to_schema(pages)

    # Convert to DataFrame
    df = pd.DataFrame(rows)

    st.subheader("📊 Extracted Data Preview")
    st.dataframe(df, use_container_width=True)

    # Convert to Excel bytes
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Extracted Data")
    excel_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Excel (output.xlsx)",
        data=excel_data,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.info("✔ Extraction complete! Download the Excel file above.")

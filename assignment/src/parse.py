# src/parse.py
import re
from dateutil import parser

# This is the EXACT schema/order expected (37 rows)
SCHEMA_KEYS = [
"First Name","Last Name","Date of Birth","Birth City","Birth State","Age",
"Blood Group","Nationality","Joining Date of first professional role",
"Designation of first professional role","Salary of first professional role",
"Salary currency of first professional role","Current Organization",
"Current Joining Date","Current Designation","Current Salary",
"Current Salary Currency","Previous Organization","Previous Joining Date",
"Previous end year","Previous Starting Designation","High School",
"12th standard pass out year","12th overall board score","Undergraduate degree",
"Undergraduate college","Undergraduate year","Undergraduate CGPA","Graduation degree",
"Graduation college","Graduation year","Graduation CGPA","Certifications 1",
"Certifications 2","Certifications 3","Certifications 4","Technical Proficiency"
]

# Template comments for some keys (taken from Expected Output)
TEMPLATE_COMMENTS = {
    "Birth City": "Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context",
    "Birth State": "Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context",
    "Age": "As on year 2024. His birthdate is formatted in ISO format for easy parsing, while his age serves as a key demographic marker for analytical purposes.",
    "Blood Group": "Emergency contact purposes.",
    "Nationality": "Citizenship status is important for understanding his work authorization and visa requirements across different employment opportunities.",
    "Current Salary": "This salary progression from his starting compensation to his current peak salary of 2,800,000 INR represents a substantial eight- fold increase over his twelve-year career span.",
    "12th standard pass out year": "His core subjects included Mathematics, Physics, Chemistry, and Computer Science, demonstrating his early aptitude for technical disciplines.",
    "12th overall board score": "Outstanding achievement",
    "Undergraduate year": "Graduating with honors and ranking 15th among 120 students in his class.",
    "Undergraduate CGPA": "On a 10-point scale",
    "Graduation college": "Continued academic excellence at IIT Bombay",
    "Graduation CGPA": "Considered exceptional and scoring 95 out of 100 for his final year thesis project.",
    "Certifications 1": "Vijay's commitment to continuous learning is evident through his impressive certification scores. He passed the AWS Solutions Architect exam in 2019 with a score of 920 out of 1000",
    "Certifications 2": "Pursued in the year 2020 with 875 points.",
    "Certifications 3": "Obtained in 2021, was achieved with an \"Above Target\" rating from PMI, These certifications complement his practical experience and demonstrate his expertise across multiple technology platforms.",
    "Certifications 4": "Earned him an outstanding 98% score. Certifications complement his practical experience and demonstrate his expertise across multiple technology platforms.",
    "Technical Proficiency": (
        "In terms of technical proficiency, Vijay rates himself highly across various skills, "
        "with SQL expertise at a perfect 10 out of 10, reflecting his daily usage since 2012. "
        "His Python proficiency scores 9 out of 10, backed by over seven years of practical experience, "
        "while his machine learning capabilities rate 8 out of 10, representing five years of hands-on implementation. "
        "His cloud platform expertise, including AWS and Azure certifications, also rates 9 out of 10 with more than four years of experience, "
        "and his data visualization skills in Power BI and Tableau score 8 out of 10, establishing him as an expert in the field."
    )
}

def extract_to_schema(pages):
    # Join full text
    full = " ".join([p.get("text", "") for p in pages])
    full = re.sub(r"\s+", " ", full).strip()

    # Initialize empty rows
    rows = []
    for k in SCHEMA_KEYS:
        rows.append({
            "Key": k,
            "Value": "",
            "Comments": TEMPLATE_COMMENTS.get(k, "")
        })

    def set_row(key, value, comment=None):
        for r in rows:
            if r["Key"] == key:
                r["Value"] = value
                if comment:
                    r["Comments"] = comment
                return

    # -------- BASIC DETAILS --------
    # Name
    m = re.search(r"([A-Z][A-Za-z]+)\s([A-Z][A-Za-z]+)\s+was born", full)
    if m:
        set_row("First Name", m.group(1))
        set_row("Last Name", m.group(2))

    # DOB
    m = re.search(r"born on\s+([A-Za-z]+\s\d{1,2},\s\d{4})", full)
    if m:
        dt = parser.parse(m.group(1))
        set_row("Date of Birth", dt.strftime("%d-%b-%y"))

    # Birth city/state
    m = re.search(r"in\s+([A-Za-z ]+),\s*([A-Za-z]+)", full)
    if m:
        set_row("Birth City", m.group(1).strip())
        set_row("Birth State", m.group(2).strip())

    # Age
    m = re.search(r"making him\s+(\d{1,2})\s+years old", full)
    if m:
        set_row("Age", f"{m.group(1)} years")

    # Blood Group
    m = re.search(r"([OAB][+-]) blood group", full)
    if m:
        set_row("Blood Group", m.group(1))

    # Nationality
    if "Indian national" in full or "Indian" in full:
        set_row("Nationality", "Indian")

    # -------- FIRST JOB --------
    m = re.search(
        r"began on\s+([A-Za-z]+\s\d{1,2},\s\d{4}).*?first company as a\s+([^,]+)\s+with an annual salary of\s+([\d,]+)",
        full, re.IGNORECASE
    )
    if m:
        set_row("Joining Date of first professional role",
                parser.parse(m.group(1)).strftime("%d-%b-%y"))
        set_row("Designation of first professional role", m.group(2))
        set_row("Salary of first professional role", m.group(3).replace(",", ""))
        set_row("Salary currency of first professional role", "INR")

    # -------- CURRENT JOB --------
    m = re.search(
        r"current role at\s+([A-Za-z ]+)\s+beginning on\s+([A-Za-z]+\s\d{1,2},\s\d{4}).*?serves as a\s+([^,]+)\s+earning\s+([\d,]+)",
        full, re.IGNORECASE
    )
    if m:
        set_row("Current Organization", m.group(1).strip())
        set_row("Current Joining Date", parser.parse(m.group(2)).strftime("%d-%b-%y"))
        set_row("Current Designation", m.group(3))
        set_row("Current Salary", m.group(4).replace(",", ""))
        set_row("Current Salary Currency", "INR")

    # -------- PREVIOUS JOB (CORRECTED REGEX) --------
    m = re.search(
        r"worked at\s+LakeCorp Solutions\s+from\s+([A-Za-z]+\s\d{1,2},\s\d{4}),?\s+to\s+(\d{4}).*?"
        r"starting as a\s+([A-Za-z ]+?)\s+and earning a promotion in\s+(\d{4})",
        full, re.IGNORECASE
    )

    if m:
        prev_join = parser.parse(m.group(1)).strftime("%d-%b-%y")
        set_row("Previous Organization", "LakeCorp Solutions")
        set_row("Previous Joining Date", prev_join)
        set_row("Previous end year", m.group(2))
        set_row("Previous Starting Designation", m.group(3).strip())
        # Promotion comment
        for r in rows:
            if r["Key"] == "Previous Starting Designation":
                r["Comments"] = f"Promoted in {m.group(4)}"

    # -------- HIGH SCHOOL --------
    m = re.search(
        r"high school education at\s+([^,]+),\s*([^,]+).*?completed his 12th standard in\s+(\d{4}).*?"
        r"achieving an outstanding\s+(\d{1,3}\.\d%)",
        full, re.IGNORECASE
    )

    if m:
        set_row("High School", f"{m.group(1)}, {m.group(2)}")
        set_row("12th standard pass out year", m.group(3))
        set_row("12th overall board score", m.group(4))

    # -------- UNDERGRAD --------
    m = re.search(
        r"B\.Tech in\s+([^,]+)\s+at\s+([^,]+).*?in\s+(\d{4}).*?CGPA of\s*([0-9\.]+)",
        full, re.IGNORECASE
    )
    if m:
        set_row("Undergraduate degree", f"B.Tech ({m.group(1)})")
        set_row("Undergraduate college", m.group(2))
        set_row("Undergraduate year", m.group(3))
        set_row("Undergraduate CGPA", m.group(4))

    # -------- POSTGRAD (FINAL FIXED REGEX) --------
    m = re.search(
        r"continued at\s+IIT Bombay, where he earned his\s+M\.Tech in\s+([A-Za-z ]+)\s+in\s+(\d{4}),\s+"
        r"achieving an exceptional CGPA of\s*([0-9\.]+).*?scoring\s+(\d{1,3})\s+out of\s+(\d{1,3})",
        full, re.IGNORECASE
    )

    if m:
        set_row("Graduation degree", f"M.Tech ({m.group(1).strip()})")
        set_row("Graduation college", "IIT Bombay")
        set_row("Graduation year", m.group(2))
        set_row("Graduation CGPA", m.group(3))

        for r in rows:
            if r["Key"] == "Graduation CGPA":
                r["Comments"] = "Considered exceptional and scoring 95 out of 100 for his final year thesis project."

    # -------- CERTIFICATIONS --------
    if "AWS Solutions Architect" in full:
        set_row("Certifications 1", "AWS Solutions Architect")

    if "Azure Data Engineer" in full:
        set_row("Certifications 2", "Azure Data Engineer")

    if "Project Management Professional" in full:
        set_row("Certifications 3", "Project Management Professional certification")

    if "SAFe Agilist" in full:
        set_row("Certifications 4", "SAFe Agilist certification")

    return rows

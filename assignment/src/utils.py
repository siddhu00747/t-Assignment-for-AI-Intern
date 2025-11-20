# src/utils.py
import pandas as pd
import os

def write_output(rows, out_path):
    # rows: list of dicts {"Key", "Value", "Comments"}
    df = pd.DataFrame(rows)
    # Add serial number column named '#'
    df.insert(0, "#", range(1, len(df)+1))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_excel(out_path, index=False)

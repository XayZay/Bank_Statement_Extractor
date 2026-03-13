import pdfplumber
import pandas as pd
import re
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Pattern for dates like 01/03/2025
date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")

def extract_transactions(pdf_file, password):
    rows = []

    with pdfplumber.open(pdf_file, password=password) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        rows.append(row)

    transactions = []
    current_row = None

    for row in rows:
        first_cell = str(row[0]).strip() if row[0] else ""

        if date_pattern.match(first_cell):
            if current_row:
                transactions.append(current_row)
            current_row = row
        else:
            if current_row:
                current_row[2] = (str(current_row[2]) + " " + (row[2] or "")).strip()

    if current_row:
        transactions.append(current_row)

    transactions = [r for r in transactions if len(r) == 7]

    return transactions


def process_all_statements(folder=".", password=""):
    columns = ["Post Date", "Value Date", "Narration", "Reference", "Debit", "Credit", "Balance"]

    pdf_files = list(Path(folder).glob("Consolidated_*_Statement.pdf"))

    if not pdf_files:
        print("No matching PDF files found.")
        return

    csv_folder = Path(folder) / "csvs"
    csv_folder.mkdir(exist_ok=True)

    for pdf_path in sorted(pdf_files):
        match = re.search(r"Consolidated_(\w+)_Statement", pdf_path.name)
        period = match.group(1) if match else "Unknown"

        print(f"Processing {pdf_path.name}...")

        try:
            transactions = extract_transactions(pdf_path, password)
            df = pd.DataFrame(transactions, columns=columns)

            for col in ["Debit", "Credit", "Balance"]:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(",", "")
                    .str.replace("₦", "")
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df[df["Post Date"] != "Post Date"]
            df["Narration"] = df["Narration"].str.replace(r"\d{6,}", "REDACTED", regex=True)

            # Drop Reference column
            df = df.drop(columns=["Reference"])

            df.insert(0, "Period", period)

            output_name = f"Consolidated_{period}_Statement.csv"
            df.to_csv(csv_folder / output_name, index=False)
            print(f"  → Saved csvs/{output_name}")
            print(f"  → {len(df)} transactions found")

        except Exception as e:
            print(f"  → ERROR: {e}")

    print(f"\nDone! CSVs saved to {csv_folder}")


pdf_password = os.getenv("PDF_PASSWORD")

process_all_statements(
    folder=r"C:\Users\User\Desktop\Personal\Personal Studies\Projects\Bank_Statement_Extractor",
    password=pdf_password
)
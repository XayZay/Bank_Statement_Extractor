# 🏦 Bank Statement Extractor

A Python script that automatically extracts transactions from password-protected bank statement PDFs and saves them as clean, structured CSV files.

## What It Does

- Scans a folder for all bank statement PDFs matching the naming convention `Consolidated_[Period]_Statement.pdf`
- Extracts transaction tables from each PDF (handles multi-line narrations)
- Cleans and formats numeric columns (debits, credits, balances)
- Anonymizes sensitive account numbers in narrations
- Saves each month's transactions as an individual CSV
- Outputs everything into a `csvs/` subfolder

## Folder Structure

```
Bank_Statement_Extractor/
│
├── Consolidated_Jan2025_Statement.pdf
├── Consolidated_Feb2025_Statement.pdf
├── Consolidated_Mar2025_Statement.pdf
├── csv_extractor.py
├── .env
│
└── csvs/
    ├── Consolidated_Jan2025_Statement.csv
    ├── Consolidated_Feb2025_Statement.csv
    └── Consolidated_Mar2025_Statement.csv
```

## Requirements

Install dependencies with:

```bash
pip install pdfplumber pandas python-dotenv
```

## Setup

**1. Clone or download the repo**

**2. Create a `.env` file** in the same folder as the script:

```
PDF_PASSWORD=yourpasswordhere
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

**3. Update the folder path** at the bottom of `csv_extractor.py`:

```python
process_all_statements(
    folder=r"C:\Path\To\Your\Statements",
    password=pdf_password
)
```

## Usage

```bash
python csv_extractor.py
```

**Example output:**

```
Processing Consolidated_Jan2025_Statement.pdf...
  → Saved csvs/Consolidated_Jan2025_Statement.csv
  → 87 transactions found

Processing Consolidated_Feb2025_Statement.pdf...
  → Saved csvs/Consolidated_Feb2025_Statement.csv
  → 91 transactions found

Done! CSVs saved to csvs/
```

## Output CSV Columns

| Column | Description |
|--------|-------------|
| Period | Month/year extracted from filename e.g. `Jan2025` |
| Post Date | Date transaction was posted |
| Value Date | Value date of the transaction |
| Narration | Transaction description (account numbers redacted) |
| Debit | Amount debited (numeric) |
| Credit | Amount credited (numeric) |
| Balance | Running balance (numeric) |

## Notes

- PDFs must follow the naming convention `Consolidated_[Period]_Statement.pdf`
- All PDFs in the folder must share the same password
- The `csvs/` output folder is created automatically if it doesn't exist
- Rows with mismatched column counts are automatically skipped
- Long digit sequences (6+ digits) in narrations are replaced with `REDACTED`

## .gitignore

Make sure your `.gitignore` includes:

```
.env
csvs/
```
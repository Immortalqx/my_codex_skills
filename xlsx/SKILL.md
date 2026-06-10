---
name: xlsx
description: Spreadsheet workflow for `.xlsx`, `.xlsm`, `.csv`, and `.tsv` files. Use when Codex needs to create, inspect, repair, clean, reformat, or extend a spreadsheet; preserve workbook structure while editing an existing file; add formulas, charts, or sheets; or convert messy tabular data into a deliverable spreadsheet file.
---

# Spreadsheet Files

## Overview

Use this skill whenever the primary deliverable is a spreadsheet file or the user explicitly wants work done on spreadsheet data in place. Prefer `openpyxl` when workbook structure, formulas, styling, or multiple sheets must be preserved. Use `pandas` for analysis and reshaping, then write the final workbook carefully instead of treating the spreadsheet as a disposable export.

## Non-Negotiable Rules

- Use formulas in the workbook instead of calculating values in Python and hardcoding the result.
- Preserve existing workbook structure unless the user asked for destructive cleanup.
- Recalculate and verify formulas after edits with `scripts/recalc.py`.
- Keep formatting readable: sensible column widths, aligned headers, and explicit number formats.
- If editing a financial model, keep assumptions visually distinct from formulas and outputs.

## Choose the Workflow

### Existing workbook

Use `openpyxl` when the file already exists and you must preserve:

- formulas,
- formatting,
- named sheets,
- comments,
- workbook-level structure.

### New workbook or pure analysis

Use `pandas` for:

- data cleaning,
- joins,
- aggregation,
- reshaping.

Then write the final spreadsheet with either:

- `pandas` if a simple flat export is enough, or
- `openpyxl` if formulas, formatting, or multiple sheets matter.

## Core Workflow

1. Inspect the workbook or source data.
2. Decide whether the task is analysis-only, structure-preserving edit, or workbook creation.
3. Make the edits.
4. Recalculate formulas with `python scripts/recalc.py <excel_file>`.
5. Fix any reported workbook errors before handoff.

## Reading and Analyzing Data

### Pandas quick read

```python
import pandas as pd

df = pd.read_excel("file.xlsx")
all_sheets = pd.read_excel("file.xlsx", sheet_name=None)

print(df.head())
print(df.info())
print(df.describe(include="all"))
```

### Openpyxl structure-preserving read

```python
from openpyxl import load_workbook

wb = load_workbook("existing.xlsx")
print(wb.sheetnames)

ws = wb["Sheet1"]
print(ws["A1"].value)
```

## Use Formulas, Not Hardcoded Values

### Wrong

```python
total = df["Sales"].sum()
sheet["B10"] = total
```

### Correct

```python
sheet["B10"] = "=SUM(B2:B9)"
sheet["C5"] = "=(C4-C2)/C2"
sheet["D20"] = "=AVERAGE(D2:D19)"
```

This rule applies to totals, percentages, growth rates, averages, ratios, and derived metrics in general.

## Creating a New Workbook

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "Summary"

ws["A1"] = "Metric"
ws["B1"] = "Value"
ws["A2"] = "Revenue"
ws["B2"] = 125000
ws["A3"] = "Cost"
ws["B3"] = 83000
ws["A4"] = "Profit"
ws["B4"] = "=B2-B3"

header_fill = PatternFill("solid", start_color="D9EAF7")
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center")

ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 14

wb.save("output.xlsx")
```

## Editing an Existing Workbook

```python
from openpyxl import load_workbook

wb = load_workbook("existing.xlsx")
ws = wb["Sheet1"]

ws["A1"] = "New Value"
ws.insert_rows(2)
ws.delete_cols(3)

new_sheet = wb.create_sheet("NewSheet")
new_sheet["A1"] = "Data"

wb.save("modified.xlsx")
```

## Recalculate and Verify

After editing any workbook with formulas, run:

```bash
python scripts/recalc.py output.xlsx
```

Optional timeout override:

```bash
python scripts/recalc.py output.xlsx 30
```

The script:

- sets up LibreOffice automation when needed,
- recalculates formulas,
- scans all sheets for Excel errors,
- returns JSON with counts and cell locations.

### Example output

```json
{
  "status": "success",
  "total_errors": 0,
  "total_formulas": 42
}
```

### If errors are reported

Typical fixes:

- `#REF!`: invalid references after row or column edits.
- `#DIV/0!`: denominator can be zero.
- `#VALUE!`: wrong data type in a formula input.
- `#NAME?`: misspelled function or unsupported name.

Do not hand off the workbook until recalculation is clean or the user explicitly accepts the remaining issues.

## Financial Model Conventions

When the workbook behaves like a model rather than a data dump:

- keep assumptions in dedicated cells or sheets,
- label units and time periods explicitly,
- apply consistent number formats,
- visually separate inputs, formulas, and outputs,
- add comments for non-obvious hardcoded assumptions.

## Verification Checklist

- Workbook opens successfully.
- Expected sheets are present.
- Key formulas still point at the right ranges.
- Number formats and percentages are readable.
- No accidental hardcoded replacements were introduced.
- `scripts/recalc.py` reports success or the remaining issues are documented.

## Notes

- Use `openpyxl` for workbook fidelity.
- Use `pandas` for tabular transformation.
- Use local scripts in `scripts/` instead of rebuilding recalculation helpers ad hoc.

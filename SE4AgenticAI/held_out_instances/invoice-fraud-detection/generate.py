#!/usr/bin/env python3
"""Generate a held-out invoice-fraud-detection instance: different vendors,
amounts, and fraud cases than the original SkillsBench instance, same schema
and same fraud-rule contract from task.md."""
import json
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

OUT = "/Users/rudranshrathore/.claude/jobs/9cd511d2/tmp/heldout/invoice-fraud-detection"

vendors = [
    {"id": "V101", "name": "Meridian Steel Co", "iban": "IBANH0001"},
    {"id": "V102", "name": "Bluewater Logistics", "iban": "IBANH0002"},
    {"id": "V103", "name": "Granite Peak Supplies", "iban": "IBANH0003"},
    {"id": "V104", "name": "Solstice Office Group", "iban": "IBANH0004"},
    {"id": "V105", "name": "Ironclad Fasteners", "iban": "IBANH0005"},
    {"id": "V106", "name": "Coastal Freight Partners", "iban": "IBANH0006"},
    {"id": "V107", "name": "Amberlight Consulting", "iban": "IBANH0007"},
    {"id": "V108", "name": "Vireo Data Systems", "iban": "IBANH0008"},
    {"id": "V109", "name": "Northgate Industrial", "iban": "IBANH0009"},
    {"id": "V110", "name": "Fernbrook Analytics", "iban": "IBANH0010"},
]

pos = [
    {"po_number": "PO-2001", "vendor_id": "V101", "amount": 4210.50},
    {"po_number": "PO-2002", "vendor_id": "V102", "amount": 1875.20},
    {"po_number": "PO-2003", "vendor_id": "V103", "amount": 9320.00},
    {"po_number": "PO-2004", "vendor_id": "V104", "amount": 3055.75},
    {"po_number": "PO-2005", "vendor_id": "V105", "amount": 6640.10},
    {"po_number": "PO-2006", "vendor_id": "V106", "amount": 2199.99},
    {"po_number": "PO-2007", "vendor_id": "V107", "amount": 5430.00},
    {"po_number": "PO-2008", "vendor_id": "V108", "amount": 7788.88},
    {"po_number": "PO-2009", "vendor_id": "V109", "amount": 1200.00},
    {"po_number": "PO-2010", "vendor_id": "V110", "amount": 4999.99},
]

# Each invoice: (vendor_name_on_invoice, amount, po_number, iban, intended_reason_or_None)
invoices = [
    # 1: clean, exact vendor match
    ("Meridian Steel Co", 4210.50, "PO-2001", "IBANH0001", None),
    # 2: clean but with a minor spelling variation -> must still fuzzy-match >80
    ("Bluewater Logistics Ltd", 1875.20, "PO-2002", "IBANH0002", None),
    # 3: IBAN Mismatch (known vendor, wrong IBAN)
    ("Granite Peak Supplies", 9320.00, "PO-2003", "IBANWRONG9", "IBAN Mismatch"),
    # 4: Invalid PO (known vendor, correct IBAN, PO not in purchase_orders.csv)
    ("Solstice Office Group", 3055.75, "PO-2099", "IBANH0004", "Invalid PO"),
    # 5: Amount Mismatch (known vendor, correct IBAN, valid PO, wrong amount)
    ("Ironclad Fasteners", 6699.00, "PO-2005", "IBANH0005", "Amount Mismatch"),
    # 6: Vendor Mismatch (PO-2007 actually belongs to V107, invoice claims V106)
    ("Coastal Freight Partners", 5430.00, "PO-2007", "IBANH0006", "Vendor Mismatch"),
    # 7: Unknown Vendor (name not in vendor list at all, low fuzzy score)
    ("Zephyr Trading LLC", 999.00, "PO-2050", "IBANZZZZZZ", "Unknown Vendor"),
    # 8: clean, exact vendor match
    ("Vireo Data Systems", 7788.88, "PO-2008", "IBANH0008", None),
    # 9: clean, exact vendor match
    ("Northgate Industrial", 1200.00, "PO-2009", "IBANH0009", None),
    # 10: priority test - Unknown Vendor should win even though IBAN and PO are also bad
    ("Umbra Consolidated Traders", 4321.00, "PO-2098", "IBANQQQQQQ", "Unknown Vendor"),
    # 11: priority test - known vendor, IBAN wrong AND PO invalid -> IBAN Mismatch wins (listed before Invalid PO)
    ("Fernbrook Analytics", 4999.99, "PO-2097", "IBANWRONGX", "IBAN Mismatch"),
    # 12: clean, exact vendor match
    ("Amberlight Consulting", 5430.00, "PO-2007".replace("2007", "2007"), "IBANH0007", None),
]
# fix invoice 12 PO to correct one for Amberlight (PO-2007 belongs to V107 = Amberlight)

def write_vendors():
    df = pd.DataFrame(vendors)
    df.to_excel(f"{OUT}/vendors.xlsx", index=False)

def write_pos():
    df = pd.DataFrame(pos)
    df.to_csv(f"{OUT}/purchase_orders.csv", index=False)

def write_pdf():
    c = canvas.Canvas(f"{OUT}/invoices.pdf", pagesize=letter)
    width, height = letter
    for i, (vname, amount, po, iban, _reason) in enumerate(invoices, start=1):
        y = height - 100
        c.setFont("Helvetica", 12)
        c.drawString(72, y, f"INVOICE #{1000+i}")
        y -= 30
        c.drawString(72, y, f"From: {vname}")
        y -= 20
        c.drawString(72, y, f"Total ${amount:.2f}")
        y -= 20
        c.drawString(72, y, f"PO Number: {po}")
        y -= 20
        c.drawString(72, y, f"Payment IBAN: {iban}")
        c.showPage()
    c.save()

def write_expected_ground_truth():
    gt = []
    po_db = {p["po_number"]: p for p in pos}
    vendor_by_name = {v["name"]: v for v in vendors}
    for i, (vname, amount, po, iban, reason) in enumerate(invoices, start=1):
        if reason is None:
            continue
        gt.append({
            "invoice_page_number": i,
            "vendor_name": vname,
            "invoice_amount": amount,
            "iban": iban,
            "po_number": po,
            "reason": reason,
        })
    with open(f"{OUT}/expected_ground_truth.json", "w") as f:
        json.dump(gt, f, indent=2)
    return gt

if __name__ == "__main__":
    write_vendors()
    write_pos()
    write_pdf()
    gt = write_expected_ground_truth()
    print(f"Generated {len(invoices)} invoices, {len(gt)} intended-fraud cases:")
    for g in gt:
        print(f"  page {g['invoice_page_number']}: {g['reason']}")

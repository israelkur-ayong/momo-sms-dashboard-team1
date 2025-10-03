<<<<<<< HEAD
# dsa/parse_xml.py
import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime
from pathlib import Path

# Auto-detect project root (script’s parent folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Look for XML in project root first
XML_PATH = PROJECT_ROOT / "modified_sms_v2.xml"

# Output JSON inside /data folder
OUT_JSON = PROJECT_ROOT / "data" / "transactions.json"
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

# Regex patterns
=======
import xml.etree.ElementTree as ET
import re
import json
from pathlib import Path

XML_PATH = Path("data/modified_sms_v2.xml")  # adjust path if needed
OUT_JSON = Path("data/transactions.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

>>>>>>> 9d2f6ecd9541c8289d667f10df470a66c9fd18c0
txid_re = re.compile(r'(?:TxId:|Financial Transaction Id:)\s*([A-Za-z0-9\-]+)', re.I)
amount_re = re.compile(r'([0-9,]+)\s*RWF', re.I)
fee_re = re.compile(r'Fee was\s*([0-9,]+)\s*RWF', re.I)
balance_re = re.compile(r'new balance[:\s]*([0-9,]+)\s*RWF', re.I)
<<<<<<< HEAD
to_name_re = re.compile(r'(?:to|from)\s+([A-Za-z\s]+)\s*(?:\(|[0-9])', re.I)

def safe_float(val):
    """Convert string to float safely."""
    try:
        return float(val.replace(',', ''))
    except Exception:
        return None

def parse_sms_elem(e):
    """Parse a single <sms> element into a transaction dict."""
    body = e.get('body') or ""
    clean_body = body.replace(',', '')

    txid_m = txid_re.search(body)
    amount_m = amount_re.search(clean_body)
    fee_m = fee_re.search(clean_body)
    balance_m = balance_re.search(clean_body)
    to_m = to_name_re.search(body)

    tx = {
        "txn_external_id": txid_m.group(1) if txid_m else None,
        "body": body.strip(),
=======

def parse_sms_elem(e):
    body = e.get('body') or ""
    txid_m = txid_re.search(body)
    amount_m = amount_re.search(body.replace(',', ''))
    fee_m = fee_re.search(body.replace(',', ''))
    balance_m = balance_re.search(body.replace(',', ''))
    tx = {
        "txn_external_id": txid_m.group(1) if txid_m else f"LOCAL-{e.get('date')}",
        "body": body,
>>>>>>> 9d2f6ecd9541c8289d667f10df470a66c9fd18c0
        "provider": e.get('address'),
        "raw_date": e.get('date'),
        "date_sent": e.get('date_sent'),
        "readable_date": e.get('readable_date'),
        "contact_name": e.get('contact_name'),
<<<<<<< HEAD
        "amount": safe_float(amount_m.group(1)) if amount_m else None,
        "fee": safe_float(fee_m.group(1)) if fee_m else 0.0,
        "balance_after": safe_float(balance_m.group(1)) if balance_m else None,
        "counterparty": to_m.group(1).strip() if to_m else None,
    }

    # Convert raw_date to ISO datetime if possible
    if tx["raw_date"]:
        try:
            tx["iso_date"] = datetime.fromtimestamp(int(tx["raw_date"]) / 1000).isoformat()
        except Exception:
            tx["iso_date"] = None

    return tx

def parse_xml(infile=XML_PATH):
    """Parse the entire XML and return a list of transactions."""
    if not infile.exists():
        raise FileNotFoundError(
            f"❌ XML file not found at {infile}. "
            f"Please place 'modified_sms_v2.xml' in {PROJECT_ROOT}"
        )

    tree = ET.parse(infile)
    root = tree.getroot()
    txs = []
    for sms in root.findall('sms'):
        tx = parse_sms_elem(sms)
        if not tx["txn_external_id"]:
            tx["txn_external_id"] = f"LOCAL-{len(txs)+1}"
        txs.append(tx)
    return txs

def write_json(txs, outpath=OUT_JSON):
    """Write list of transactions to JSON file."""
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(txs, f, indent=2, ensure_ascii=False)
    print(f"✅ Wrote {len(txs)} transactions to {outpath}")

if __name__ == "__main__":
    txs = parse_xml()
    write_json(txs)
=======
        "amount": float(amount_m.group(1).replace(',', '')) if amount_m else None,
        "fee": float(fee_m.group(1).replace(',', '')) if fee_m else 0.0,
        "balance_after": float(balance_m.group(1).replace(',', '')) if balance_m else None,
    }
    return tx

def parse_xml(infile=XML_PATH):
    tree = ET.parse(infile)
    root = tree.getroot()
    txs = [parse_sms_elem(sms) for sms in root.findall('sms')]
    return txs

def write_json(txs, outpath=OUT_JSON):
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(txs, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(txs)} transactions to {outpath}")

if __name__ == "__main__":
    txs = parse_xml()
    write_json(txs)
>>>>>>> 9d2f6ecd9541c8289d667f10df470a66c9fd18c0

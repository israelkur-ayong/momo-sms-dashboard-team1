# dsa/parse_xml.py
import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime
from pathlib import Path

XML_PATH = Path("modified_sms_v2.xml")   # place file at repo root or adjust path
OUT_JSON = Path("data/transactions.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

txid_re = re.compile(r'(?:TxId:|Financial Transaction Id:)\s*([A-Za-z0-9\-]+)', re.I)
amount_re = re.compile(r'([0-9,]+)\s*RWF', re.I)
fee_re = re.compile(r'Fee was\s*([0-9,]+)\s*RWF', re.I)
balance_re = re.compile(r'new balance[:\s]*([0-9,]+)\s*RWF', re.I)
to_name_re = re.compile(r'(?:to|from)\s+([A-Za-z\s]+)\s*(?:\(|[0-9])', re.I)

def parse_sms_elem(e):
    body = e.get('body') or ""
    txid_m = txid_re.search(body)
    amount_m = amount_re.search(body.replace(',', ''))
    fee_m = fee_re.search(body.replace(',', ''))
    balance_m = balance_re.search(body.replace(',', ''))
    tx = {
        "txn_external_id": txid_m.group(1) if txid_m else None,
        "body": body,
        "provider": e.get('address'),
        "raw_date": e.get('date'),
        "date_sent": e.get('date_sent'),
        "readable_date": e.get('readable_date'),
        "contact_name": e.get('contact_name'),
        "amount": float(amount_m.group(1).replace(',', '')) if amount_m else None,
        "fee": float(fee_m.group(1).replace(',', '')) if fee_m else 0.0,
        "balance_after": float(balance_m.group(1).replace(',', '')) if balance_m else None,
    }
    return tx

def parse_xml(infile=XML_PATH):
    tree = ET.parse(infile)
    root = tree.getroot()
    txs = []
    for sms in root.findall('sms'):
        tx = parse_sms_elem(sms)
        # generate simple ID if external id missing
        if not tx["txn_external_id"]:
            tx["txn_external_id"] = f"LOCAL-{len(txs)+1}"
        txs.append(tx)
    return txs

def write_json(txs, outpath=OUT_JSON):
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(txs, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(txs)} transactions to {outpath}")

if __name__ == "__main__":
    txs = parse_xml()
    write_json(txs)
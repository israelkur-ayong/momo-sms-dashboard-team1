from pathlib import Path
import xml.etree.ElementTree as ET
import json
import sys

# Absolute path based on this script's location
XML_PATH = Path(__file__).resolve().parent.parent / "data" / "modified_sms_v2.xml"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "transactions.json"

def parse_xml():
    if not XML_PATH.exists():
        print(f"XML file not found at {XML_PATH}")
        sys.exit(1)

    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    transactions = []
    for txn in root.findall("transaction"):
        try:
            record = {
                "txn_external_id": txn.findtext("txn_external_id"),
                "amount": float(txn.findtext("amount", 0)),
                "sender": txn.findtext("sender"),
                "receiver": txn.findtext("receiver"),
                "timestamp": txn.findtext("timestamp"),
                "provider": txn.findtext("provider")
            }
            transactions.append(record)
        except Exception as e:
            print(f"Skipped a transaction due to error: {e}")
    return transactions

if __name__ == "__main__":
    txs = parse_xml()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(txs, f, indent=2)
    print(f"Parsed {len(txs)} transactions → {OUT_PATH}")
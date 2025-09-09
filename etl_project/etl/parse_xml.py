#!/usr/bin/env python3
"""
ETL: Parse XML files from data/raw/ and output processed data to data/processed/.
Uses lxml for XML parsing and python-dateutil for date handling.
"""
import os
from datetime import datetime
from dateutil import parser as date_parser
from lxml import etree
import json  # For outputting processed data as JSON (easy to load later)

def parse_xml_file(file_path):
    """
    Parse an XML file and extract key data (customize based on your XML schema).
    Example: Assumes XML like <root><item><name>Item1</name><date>2023-01-01</date></item></root>
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    tree = etree.parse(file_path)
    root = tree.getroot()
    processed_data = []

    for item in root.findall('item'):  # Adjust XPath based on your XML
        name = item.find('name').text if item.find('name') is not None else 'Unknown'
        date_str = item.find('date').text if item.find('date') is not None else None
        if date_str:
            parsed_date = date_parser.parse(date_str)  # Handles various date formats
        else:
            parsed_date = datetime.now()

        processed_data.append({
            'name': name,
            'parsed_date': parsed_date.isoformat(),
            'timestamp': datetime.now().isoformat()
        })

    return processed_data

def main():
    raw_dir = 'data/raw'
    processed_dir = 'data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    # Example: Process all .xml files in raw/
    for filename in os.listdir(raw_dir):
        if filename.endswith('.xml'):
            file_path = os.path.join(raw_dir, filename)
            data = parse_xml_file(file_path)
            if data:
                output_file = os.path.join(processed_dir, f"{filename}.json")
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"Processed {filename} -> {output_file}")

if __name__ == '__main__':
    main()

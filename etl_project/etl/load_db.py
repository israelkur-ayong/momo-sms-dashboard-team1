#!/usr/bin/env python3
"""
ETL: Load processed data from data/processed/ into SQLite DB.
Uses SQLAlchemy for ORM and python-dotenv for .env loading.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

load_dotenv()  # Loads .env or .env.example

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/db.sqlite3')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Item(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True)
    name = Column(String)
    parsed_date = Column(DateTime)
    timestamp = Column(DateTime, default=datetime.now)

def load_to_db(processed_file_path):
    """
    Load JSON from processed file into DB.
    """
    Base.metadata.create_all(engine)  # Create table if not exists

    session = Session()
    with open(processed_file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        db_item = Item(
            id=item['name'],  # Use name as ID; adjust as needed
            name=item['name'],
            parsed_date=datetime.fromisoformat(item['parsed_date'])
        )
        session.merge(db_item)  # Avoid duplicates

    session.commit()
    session.close()
    print(f"Loaded {len(data)} items from {processed_file_path}")

def main():
    processed_dir = 'data/processed'
    for filename in os.listdir(processed_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(processed_dir, filename)
            load_to_db(file_path)

if __name__ == '__main__':
    main()

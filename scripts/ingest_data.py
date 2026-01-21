import os
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATASET_URL = os.getenv("DATASET_URL", "https://static.krevera.com/dataset.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the data model based on the JSON structure
class ProductInspection(Base):
    __tablename__ = "product_inspections"

    id = Column(Integer, primary_key=True, index=True)
    molding_machine_id = Column(String)
    timestamp = Column(DateTime)
    version = Column(String)

    # Example fields from object_detection - this will need to be expanded
    burn_mark_defect_reject = Column(Boolean)
    burn_mark_defect_pixel_severity = Column(Float)


def ingest_data():
    # Fetch data from the URL
    response = requests.get(DATASET_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Ingest data
    for entry in data:
        ts_datetime = datetime.fromtimestamp(entry["timestamp"])
        # This is a simplified example. A more robust implementation
        # would map the nested JSON to a proper relational schema.
        inspection = ProductInspection(
            molding_machine_id=entry["molding_machine_id"],
            timestamp=ts_datetime,
            version=entry["version"],
            burn_mark_defect_reject=entry["object_detection"]["burn_mark_defect"]["reject"],
            burn_mark_defect_pixel_severity=entry["object_detection"]["burn_mark_defect"]["pixel_severity"]["value"],
        )
        db.add(inspection)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    ingest_data()
    print("Data ingestion complete.")

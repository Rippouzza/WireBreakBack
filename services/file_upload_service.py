import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from models.wire_break_detail import WireBreakDetail
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from dateutil import parser
from sqlalchemy.sql import text
import numpy as np  # ✅ Import NumPy for NaN handling

# Configure logger
logger = logging.getLogger(__name__)

# Database connection setup
DB_SERVER = 'PC-GHILEB'
DB_NAME = 'WireBreak'
DB_USER = ''
DB_PASSWORD = ''

# SQLAlchemy connection string
conn_str = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def handle_file_upload(file):
    """Service to handle file processing logic."""

    df = pd.read_excel(file, engine='openpyxl')

    # ✅ Rename columns correctly
    df.rename(columns={
        'WireBreak': 'Plant',
        'Unnamed: 1': 'Supplier',
        'Unnamed: 2': 'Week_Number',
        'Unnamed: 3': 'Wire_Break_Type',
        'Unnamed: 4': 'num_of_break',
        'Unnamed: 5': 'Break_date',
        'Unnamed: 6': 'Batch_Number',
        'Unnamed: 7': 'Machine_Number',
        'Unnamed: 8': 'Break_Diameter',
        'Unnamed: 9': 'Range_',
        'Unnamed: 10': 'Finished_Wire_Diameter'
    }, inplace=True)

    # ✅ Remove completely empty rows
    df.dropna(how='all', inplace=True)

    # ✅ Drop any rows where the first column is not a valid Plant name (header rows)
    df = df[df["Plant"].apply(lambda x: isinstance(x, str) and x.strip().lower() != "plant")]

    records = df.to_dict(orient="records")

    success_count = 0
    failure_count = 0
    db = SessionLocal()

    for record in records:
        try:
            # ✅ Convert 'Break_date' correctly or set to None if invalid
            if pd.notna(record["Break_date"]) and str(record["Break_date"]).lower() != "nan":
                record["Break_date"] = parser.parse(str(record["Break_date"])).date()
            else:
                record["Break_date"] = None  # ✅ Handle NaN dates

            # ✅ Replace NaN values with None
            for key, value in record.items():
                if isinstance(value, float) and np.isnan(value):
                    record[key] = None

            # ✅ Ensure 'num_of_break' is numeric
            if not isinstance(record["num_of_break"], (int, float)):
                record["num_of_break"] = None

            # ✅ Validate Machine_Number exists in the database
            machine_exists = db.execute(
                text("SELECT COUNT(*) FROM machine WHERE codeMachine = :machine"),
                {"machine": record["Machine_Number"]}
            ).scalar()

            if not machine_exists:
                logger.error(f"Machine_Number {record['Machine_Number']} does not exist in 'machine' table.")
                failure_count += 1
                continue

            # ✅ Check if the record already exists
            existing_record = db.query(WireBreakDetail).filter_by(
                Plant=record["Plant"],
                Supplier=record["Supplier"],
                Week_Number=record["Week_Number"],
                Wire_Break_Type=record["Wire_Break_Type"],
                Break_date=record["Break_date"],
                num_of_break=record["num_of_break"],
                Machine_Number=record["Machine_Number"]
            ).first()

            if existing_record:
                for key, value in record.items():
                    setattr(existing_record, key, value)
            else:
                new_record = WireBreakDetail(**record)
                db.add(new_record)

            db.commit()
            success_count += 1
        except Exception as e:
            logger.error(f"Error processing record: {record}. Error: {str(e)}")
            db.rollback()
            failure_count += 1

    db.close()
    return success_count, failure_count

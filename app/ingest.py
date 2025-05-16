import pandas as pd
from .models import Sales, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

REQUIRED_COLUMNS = [
    'sale_id', 'product_id', 'product_name', 'quantity', 'price', 'date', 'customer_id', 'region'
]

def validate_record(record):
    # Row validation logic
    if not isinstance(record['sale_id'], int):
        return False, "sale_id must be an integer"
    if not isinstance(record['product_id'], int):
        return False, "product_id must be an integer"
    if not isinstance(record['product_name'], str):
        return False, "product_name must be a string"
    if not isinstance(record['quantity'], int):
        return False, "quantity must be an integer"
    if not isinstance(record['price'], (int, float)):
        return False, "price must be a number"
    if not isinstance(record['date'], datetime):
        return False, "date must be a datetime object"
    if not isinstance(record['customer_id'], int):
        return False, "customer_id must be an integer"
    if not isinstance(record['region'], str):
        return False, "region must be a string"
    return True, ""


def ingest_csv(file_path):
    chunksize = 10000  # Number of rows per chunk
    first_chunk = True
    try:
        # Read the CSV file in chunks
        for chunk in pd.read_csv(file_path, parse_dates=['date'], chunksize=chunksize):
            # Check if all required columns are present
            if first_chunk:
                missing_columns = set(REQUIRED_COLUMNS) - set(chunk.columns)
                if missing_columns:
                    raise ValueError(f"Missing columns in CSV: {missing_columns}")
                first_chunk = False

            # Drop rows with NaN values
            chunk.dropna(subset=REQUIRED_COLUMNS, inplace=True)  # Drop rows with NaN values
            records = chunk.to_dict(orient='records')
            #show the dtypes of the chunk
            #print( chunk.dtypes)
            sales_records = []
            for rec in records:
                #Validate required columns
                valid, msg = validate_record(rec)
                if valid:
                    sales_records.append(Sales(**rec))
                else:
                    raise ValueError(f"Invalid record: {msg}")
            
            if sales_records:
                try:
                    db.session.bulk_save_objects(sales_records)
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()
                    print(f"Ingestion failed while trying to save records in db: {e}") 

        
        
            # Validate required columns
            for record in records:
                for col in REQUIRED_COLUMNS:
                    if col not in record:
                        raise ValueError(f"Missing column '{col}' in record: {record}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    
    
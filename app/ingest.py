import pandas as pd
from .models import Sales, db
from sqlalchemy.exc import SQLAlchemyError

def ingest_csv(file_path):
    chunksize = 10000  # Number of rows per chunk
    for chunk in pd.read_csv(file_path, parse_dates= ['date'],chunksize=chunksize):
        chunk.dropna(inplace=True)  # Drop rows with NaN values
        records= chunk.to_dict(orient='records')
        sales_records = [Sales(**rec) for rec in records]

        try:
            db.session.bulk_save_objects(sales_records)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Ingestion failed: {e}")
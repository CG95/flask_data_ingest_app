from app import create_app, db
from app.models import Sales
from app.ingest import ingest_csv
import os

DATA_PATH = os.path.join('data', 'sales_data.csv')  # Adjust filename

app = create_app()

with app.app_context():
    # Create the database tables
    #db.create_all()

    # Check if any data exists
    if db.session.query(Sales).count() == 0:
        print("No data found in 'sales' table. Ingesting CSV...")
        ingest_csv(DATA_PATH)
    else:
        print("Sales data already ingested. Skipping ingestion.")

if __name__ == "__main__":
    app.run(debug=True)
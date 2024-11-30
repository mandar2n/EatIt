import asyncio
import csv
from fastapi import Depends
from geoalchemy2 import functions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from models import Store, Base
from database import engine, SessionLocal, get_db

# Function to insert CSV data into the store table
async def insert_data_from_csv(csv_file_path: str, db: AsyncSession = Depends(get_db)):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            # Create a POINT geometry from latitude and longitude
            location = f"POINT({longitude} {latitude})"

            # Create a new Store object and add to the session
            store = Store(
                store_name=row['store_name'],
                address=row['address'],
                location=location  # Directly insert as POINT geometry
            )
            db.add(store)
        await db.commit()

# Main function to trigger the data import
async def import_csv(csv_file_path: str):
    async with SessionLocal() as db:
        await insert_data_from_csv(csv_file_path, db)
        print("Data inserted successfully.")

# Main function to trigger the data import
async def main():
    await import_csv("C:/Users/lovel/Downloads/converted_dataset.csv")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

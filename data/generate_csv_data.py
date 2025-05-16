import pandas as pd
from faker import Faker
import random
from datetime import date
from tqdm import tqdm

# Configuration
OUTPUT_FILE_TEST = "tests\data\sales_data.csv"
OUTPUT_FILE = "data\sales_data.csv"
NUM_SALES = 900_000        # Number of distinct sales (Sale_id)
NUM_SALES_TEST = 70_000        # Number of distinct sales (Sale_id)
MAX_PRODUCTS_PER_SALE = 5  # Sale may have 1 to 5 products



fake = Faker()
Faker.seed(0)
random.seed(0)

PRODUCT_NAMES = [
    "Smartphone", "Laptop", "Headphones", "Monitor", "Keyboard", "Mouse", "Tablet", "Smartwatch", "Charger", "USB Cable",
    "TV", "Speaker", "Camera", "Microphone", "Webcam", "Projector", "Drone", "VR Headset", "Game Console", "Graphics Card",
    "Motherboard", "Processor", "RAM Stick", "Power Supply", "Cooling Fan", "SSD Drive", "Hard Drive", "Router", "Modem", "Switch",
    "Desk Lamp", "Office Chair", "Standing Desk", "Notebook", "Pen", "Backpack", "Briefcase", "Mouse Pad", "Desk Organizer", "Paper Shredder",
    "Coffee Maker", "Toaster", "Blender", "Air Fryer", "Rice Cooker", "Microwave", "Dishwasher", "Washing Machine", "Refrigerator", "Air Conditioner",
    "Sofa", "Bookshelf", "TV Stand", "Dining Table", "Bed Frame", "Mattress", "Nightstand", "Wardrobe", "Curtains", "Floor Lamp",
    "T-shirt", "Jeans", "Sneakers", "Jacket", "Hat", "Sunglasses", "Watch", "Belt", "Scarf", "Gloves",
    "Shampoo", "Toothpaste", "Hair Dryer", "Electric Shaver", "Deodorant", "Face Cream", "Hand Sanitizer", "Perfume", "Lip Balm", "Makeup Kit",
    "Basketball", "Soccer Ball", "Yoga Mat", "Dumbbells", "Tennis Racket", "Bicycle", "Treadmill", "Jump Rope", "Helmet", "Sports Bag",
    "Book", "Notebook", "E-reader", "Subscription Card", "Board Game", "Puzzle", "Toy Car", "Action Figure", "Doll", "Building Blocks"
]

PRODUCT_ID_MAP = {i + 1: name + fake.color_name() for i, name in enumerate(PRODUCT_NAMES)}



def generate_sales_data(num_sales):
    rows = []
    for sale_id in tqdm(range(1, num_sales + 1)):
        customer_id = random.randint(1000, 1999)
        sale_date = fake.date_between(start_date=date(2023, 1, 1), end_date=date(2024, 12, 31))
        num_products = random.randint(1, MAX_PRODUCTS_PER_SALE)
        region = fake.country()

        for _ in range(num_products):
            product_id = random.randint(1, len(PRODUCT_NAMES))
            product_name = PRODUCT_ID_MAP[product_id]
            quantity = random.randint(1, 10)
            price = round(random.uniform(5, 500), 2)

            rows.append({
                "sale_id": sale_id,
                "product_id": product_id,
                "product_name": product_name,
                "quantity": quantity,
                "price": price,
                "date": sale_date,
                "customer_id": customer_id,
                "region": region
            })

    return pd.DataFrame(rows)
    

def main():
    df = generate_sales_data(NUM_SALES)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ File saved to {OUTPUT_FILE}")
    df2 = generate_sales_data(NUM_SALES_TEST)
    df2.to_csv(OUTPUT_FILE_TEST, index=False)
    print(f"✅ File saved to {OUTPUT_FILE_TEST}")

if __name__ == "__main__":
    main()

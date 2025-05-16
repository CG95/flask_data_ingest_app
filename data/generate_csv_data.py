import pandas as pd
from faker import Faker
import random
from datetime import date
from tqdm import tqdm

# Configuration
#OUTPUT_FILE = "tests\data\sales_data.csv"
OUTPUT_FILE = "data\sales_data.csv"
NUM_SALES = 200_000        # Number of distinct sales (Sale_id)
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

PRODUCT_ID_MAP = {i + 1: name for i, name in enumerate(PRODUCT_NAMES)}



def generate_sales_data():
    rows = []
    for sale_id in tqdm(range(1, NUM_SALES + 1)):
        customer_id = random.randint(1000, 1999)
        sale_date = fake.date_between(start_date=date(2023, 1, 1), end_date=date(2024, 12, 31))
        num_products = random.randint(1, MAX_PRODUCTS_PER_SALE)
        region = fake.country()

        for _ in range(num_products):
            product_id = random.randint(1, len(PRODUCT_NAMES))
            product_name = PRODUCT_ID_MAP[product_id] + " " + fake.color_name()
            quantity = random.randint(1, 10)
            price = round(random.uniform(5, 500), 2)

            rows.append({
                "Sale_id": sale_id,
                "Product_id": product_id,
                "Product_name": product_name,
                "quantity": quantity,
                "price": price,
                "sale_date": sale_date,
                "customer_id": customer_id,
                "region": region
            })

    return pd.DataFrame(rows)
    

def main():
    df = generate_sales_data()
    df.to_csv(OUTPUT_FILE, index=False)
    print("✅ File saved as: sales_data_multi_product.csv")

if __name__ == "__main__":
    main()

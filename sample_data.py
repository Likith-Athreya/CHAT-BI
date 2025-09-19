"""
Sample data generator for testing the BI Agent.
Creates a sample database with realistic business data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any
from sqlalchemy import create_engine, text

class SampleDataGenerator:
    """Generate sample business data for testing the BI Agent."""
    
    def __init__(self, db_url: str = "postgresql+psycopg2://user:password@localhost:5432/bi_db"):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        
    def generate_customers(self, num_customers: int = 1000) -> pd.DataFrame:
        """Generate customer data."""
        np.random.seed(42)
        
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily", 
                      "William", "Jessica", "James", "Ashley", "Christopher", "Amanda", "Daniel"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                     "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
        
        customers = []
        for i in range(num_customers):
            customer = {
                "customer_id": i + 1,
                "first_name": random.choice(first_names),
                "last_name": random.choice(last_names),
                "email": f"customer{i+1}@example.com",
                "phone": f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "registration_date": datetime.now() - timedelta(days=random.randint(1, 365*3)),
                "customer_segment": random.choice(["Premium", "Standard", "Basic"]),
                "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                                     "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]),
                "state": random.choice(["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]),
                "country": "USA"
            }
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_products(self, num_products: int = 100) -> pd.DataFrame:
        """Generate product data."""
        np.random.seed(42)
        
        categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Beauty", "Toys"]
        brands = ["TechCorp", "FashionBrand", "BookWorld", "HomeStyle", "SportMax", "BeautyPlus", "ToyLand"]
        
        products = []
        for i in range(num_products):
            category = random.choice(categories)
            brand = random.choice(brands)
            
            product = {
                "product_id": i + 1,
                "product_name": f"{brand} {category} Item {i+1}",
                "category": category,
                "brand": brand,
                "price": round(random.uniform(10, 500), 2),
                "cost": round(random.uniform(5, 250), 2),
                "stock_quantity": random.randint(0, 1000),
                "supplier": f"Supplier {random.randint(1, 20)}",
                "created_date": datetime.now() - timedelta(days=random.randint(1, 365*2))
            }
            products.append(product)
        
        return pd.DataFrame(products)
    
    def generate_orders(self, num_orders: int = 5000, num_customers: int = 1000, num_products: int = 100) -> pd.DataFrame:
        """Generate order data."""
        np.random.seed(42)
        
        orders = []
        for i in range(num_orders):
            order_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            order = {
                "order_id": i + 1,
                "customer_id": random.randint(1, num_customers),
                "order_date": order_date,
                "total_amount": round(random.uniform(20, 2000), 2),
                "status": random.choice(["Completed", "Pending", "Cancelled", "Shipped"]),
                "payment_method": random.choice(["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]),
                "shipping_address": f"{random.randint(100, 9999)} Main St",
                "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]),
                "state": random.choice(["NY", "CA", "IL", "TX", "AZ"]),
                "zip_code": f"{random.randint(10000, 99999)}"
            }
            orders.append(order)
        
        return pd.DataFrame(orders)
    
    def generate_order_items(self, num_items: int = 15000, num_orders: int = 5000, num_products: int = 100) -> pd.DataFrame:
        """Generate order items data."""
        np.random.seed(42)
        
        order_items = []
        for i in range(num_items):
            order_item = {
                "order_item_id": i + 1,
                "order_id": random.randint(1, num_orders),
                "product_id": random.randint(1, num_products),
                "quantity": random.randint(1, 10),
                "unit_price": round(random.uniform(5, 200), 2),
                "discount": round(random.uniform(0, 0.3), 2)
            }
            order_items.append(order_item)
        
        return pd.DataFrame(order_items)
    
    def generate_sales_data(self, num_records: int = 10000) -> pd.DataFrame:
        """Generate sales data."""
        np.random.seed(42)
        
        sales = []
        for i in range(num_records):
            sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            sale = {
                "sale_id": i + 1,
                "product_id": random.randint(1, 100),
                "customer_id": random.randint(1, 1000),
                "sale_date": sale_date,
                "quantity": random.randint(1, 20),
                "unit_price": round(random.uniform(10, 500), 2),
                "total_amount": 0,  # Will be calculated
                "sales_rep": f"Rep {random.randint(1, 20)}",
                "region": random.choice(["North", "South", "East", "West", "Central"]),
                "channel": random.choice(["Online", "Store", "Phone", "Email"])
            }
            sale["total_amount"] = sale["quantity"] * sale["unit_price"]
            sales.append(sale)
        
        return pd.DataFrame(sales)
    
    def create_sample_database(self):
        """Create the complete sample database."""
        print("Creating sample database...")
        
        # Generate data
        print("Generating customers...")
        customers_df = self.generate_customers(1000)
        
        print("Generating products...")
        products_df = self.generate_products(100)
        
        print("Generating orders...")
        orders_df = self.generate_orders(5000, 1000, 100)
        
        print("Generating order items...")
        order_items_df = self.generate_order_items(15000, 5000, 100)
        
        print("Generating sales data...")
        sales_df = self.generate_sales_data(10000)
        
        # Create tables
        print("Creating database tables...")
        customers_df.to_sql("customers", self.engine, if_exists="replace", index=False)
        products_df.to_sql("products", self.engine, if_exists="replace", index=False)
        orders_df.to_sql("orders", self.engine, if_exists="replace", index=False)
        order_items_df.to_sql("order_items", self.engine, if_exists="replace", index=False)
        sales_df.to_sql("sales", self.engine, if_exists="replace", index=False)
        
        # Create indexes for better performance
        print("Creating indexes...")
        with self.engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_customers_id ON customers(customer_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_id ON products(product_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id)"))
            conn.commit()
        
        print(f"Sample database created successfully at {self.db_url}")
        
        # Print summary
        print("\nDatabase Summary:")
        tables = ["customers", "products", "orders", "order_items", "sales"]
        for table in tables:
            count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", self.engine).iloc[0]["count"]
            print(f"  {table}: {count} records")
    
    def close(self):
        """Close database connection."""
        self.engine.dispose()

def main():
    """Main function to create sample database."""
    generator = SampleDataGenerator()
    try:
        generator.create_sample_database()
    finally:
        generator.close()

if __name__ == "__main__":
    main()

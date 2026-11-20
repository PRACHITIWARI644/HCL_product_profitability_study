"""
=============================================================================
Product Category Profitability Study
Script: generate_raw_dataset.py
Epic: D04-E01 - Problem Understanding and Dataset Creation
Author: Student Research Team
Description: Generates realistic multi-category retail transaction data
             spanning 2023-2024 with realistic cost structures, seasonal
             trends, and intentional real-world data quality artifacts
             (missing values, formatting inconsistencies, anomalies) for
             subsequent data cleaning and validation pipelines.
=============================================================================
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_raw_data(num_records=8500):
    print(f"Generating {num_records} raw sales transactions...")

    # Define Categories and realistic product catalogs
    catalog = {
        'Electronics': {
            'products': [
                ('ELEC_101', 'Smartphone Pro Max', 850.0, 680.0),
                ('ELEC_102', 'Wireless Noise-Cancelling Headphones', 180.0, 110.0),
                ('ELEC_103', '4K Smart LED TV 55"', 650.0, 530.0),
                ('ELEC_104', 'Ultra-Slim Gaming Laptop', 1200.0, 980.0),
                ('ELEC_105', 'Smartwatch Series 5', 220.0, 150.0),
                ('ELEC_106', 'Bluetooth Portable Speaker', 65.0, 40.0),
                ('ELEC_107', 'Tablet 10-inch 128GB', 380.0, 290.0)
            ],
            'base_discount_range': (0.00, 0.25),
            'quantity_weights': [0.55, 0.30, 0.10, 0.04, 0.01]  # mostly 1-2 items
        },
        'Apparel & Footwear': {
            'products': [
                ('APP_201', 'Men\'s Slim Fit Denim Jeans', 48.0, 22.0),
                ('APP_202', 'Women\'s Running Shoes', 75.0, 34.0),
                ('APP_203', 'Cotton Casual Crewneck T-Shirt', 22.0, 8.5),
                ('APP_204', 'Waterproof Winter Jacket', 135.0, 62.0),
                ('APP_205', 'Formal Leather Oxford Shoes', 95.0, 45.0),
                ('APP_206', 'Women\'s Floral Summer Dress', 55.0, 24.0)
            ],
            'base_discount_range': (0.05, 0.35),
            'quantity_weights': [0.40, 0.35, 0.15, 0.07, 0.03]
        },
        'Home & Kitchen': {
            'products': [
                ('HOME_301', 'Air Fryer Touchscreen 5.8Qt', 110.0, 68.0),
                ('HOME_302', 'Stainless Steel Cookware 10-Piece', 160.0, 95.0),
                ('HOME_303', 'Microfiber Bedding Sheet Set', 45.0, 20.0),
                ('HOME_304', 'Robotic Vacuum Cleaner', 260.0, 175.0),
                ('HOME_305', 'Single-Serve Espresso Machine', 130.0, 78.0),
                ('HOME_306', 'Ceramic Tabletop Lamp Set', 60.0, 32.0)
            ],
            'base_discount_range': (0.00, 0.20),
            'quantity_weights': [0.50, 0.30, 0.12, 0.06, 0.02]
        },
        'Office Supplies': {
            'products': [
                ('OFF_401', 'Ergonomic Mesh Desk Chair', 190.0, 125.0),
                ('OFF_402', 'Multipurpose Copy Paper (Case)', 38.0, 26.0),
                ('OFF_403', 'Wireless Laser Printer', 170.0, 120.0),
                ('OFF_404', 'Heavy-Duty Shredder', 85.0, 52.0),
                ('OFF_405', 'Desk Organizer & Pen Set', 25.0, 11.0),
                ('OFF_406', 'Dry Erase Magnetic Whiteboard', 45.0, 25.0)
            ],
            'base_discount_range': (0.00, 0.15),
            'quantity_weights': [0.35, 0.30, 0.20, 0.10, 0.05]
        },
        'Beauty & Personal Care': {
            'products': [
                ('BEAU_501', 'Anti-Aging Hyaluronic Acid Serum', 42.0, 12.0),
                ('BEAU_502', 'Hydrating Facial Moisturizer', 28.0, 8.5),
                ('BEAU_503', 'Organic Argan Oil Hair Mask', 32.0, 10.0),
                ('BEAU_504', 'Sonic Electric Toothbrush', 68.0, 28.0),
                ('BEAU_505', 'Matte Long-Lasting Lipstick Trio', 24.0, 6.0),
                ('BEAU_506', 'Sunscreen SPF 50 Broad Spectrum', 22.0, 6.5)
            ],
            'base_discount_range': (0.00, 0.15),
            'quantity_weights': [0.45, 0.35, 0.12, 0.06, 0.02]
        },
        'Furniture': {
            'products': [
                ('FURN_601', '3-Seater Fabric Recliner Sofa', 720.0, 590.0),
                ('FURN_602', 'Solid Oak Dining Table Set', 640.0, 520.0),
                ('FURN_603', 'King Size Memory Foam Mattress', 550.0, 420.0),
                ('FURN_604', 'Minimalist Bookshelf 5-Tier', 140.0, 105.0),
                ('FURN_605', 'Accent Armchair Velvet', 280.0, 220.0)
            ],
            'base_discount_range': (0.05, 0.30),
            'quantity_weights': [0.75, 0.20, 0.04, 0.01, 0.00]
        },
        'Sports & Fitness': {
            'products': [
                ('SPO_701', 'Adjustable Cast Iron Dumbbells Set', 120.0, 72.0),
                ('SPO_702', 'Non-Slip Thick Yoga Mat', 35.0, 14.0),
                ('SPO_703', 'Foldable Indoor Treadmill', 480.0, 340.0),
                ('SPO_704', 'Smart Fitness Tracker Band', 50.0, 26.0),
                ('SPO_705', 'Insulated Stainless Steel Bottle 32oz', 25.0, 9.0)
            ],
            'base_discount_range': (0.00, 0.20),
            'quantity_weights': [0.50, 0.32, 0.12, 0.05, 0.01]
        }
    }

    regions = ['North', 'South', 'East', 'West', 'Central']
    region_weights = [0.28, 0.24, 0.18, 0.20, 0.10]

    stores = [f'STR_{i:03d}' for i in range(101, 126)]  # 25 stores
    store_region_map = {s: np.random.choice(regions, p=region_weights) for s in stores}

    payment_modes = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash on Delivery']
    payment_weights = [0.38, 0.18, 0.25, 0.11, 0.08]

    # Generate dates across 2023-01-01 to 2024-12-31 (730 days)
    start_date = datetime(2023, 1, 1)

    records = []
    category_names = list(catalog.keys())
    cat_distribution = [0.24, 0.20, 0.16, 0.12, 0.11, 0.08, 0.09]

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2023 + (i % 2):04d}-{10000 + i}"
        
        # Pick category
        cat = np.random.choice(category_names, p=cat_distribution)
        cat_info = catalog[cat]
        
        # Pick product
        prod_tuple = random.choice(cat_info['products'])
        product_id, prod_name, unit_price, unit_cost = prod_tuple
        
        # Add slight natural pricing jitter (+- 5%)
        unit_price = round(unit_price * np.random.uniform(0.95, 1.05), 2)
        unit_cost = round(unit_cost * np.random.uniform(0.96, 1.04), 2)
        
        # Quantity
        qty = np.random.choice([1, 2, 3, 4, 5], p=cat_info['quantity_weights'])
        
        # Discount
        d_min, d_max = cat_info['base_discount_range']
        discount_pct = round(np.random.uniform(d_min, d_max), 2)
        
        # High discount promotion event occasionally (holiday seasons)
        day_offset = np.random.randint(0, 730)
        order_dt = start_date + timedelta(days=day_offset)
        
        # Black Friday / Festive season boost (Nov/Dec)
        if order_dt.month in [11, 12]:
            discount_pct = min(0.50, round(discount_pct + np.random.uniform(0.05, 0.15), 2))
            
        gross_rev = round(unit_price * qty, 2)
        discount_amount = round(gross_rev * discount_pct, 2)
        net_revenue = round(gross_rev - discount_amount, 2)
        total_cost = round(unit_cost * qty, 2)
        
        store_id = random.choice(stores)
        region = store_region_map[store_id]
        customer_id = f"CUST_{np.random.randint(1001, 2801):04d}"
        payment_mode = np.random.choice(payment_modes, p=payment_weights)
        
        # Formatting variation for order date (simulating raw multi-source ingestion)
        rand_fmt = np.random.random()
        if rand_fmt < 0.85:
            date_str = order_dt.strftime('%Y-%m-%d')
        elif rand_fmt < 0.95:
            date_str = order_dt.strftime('%d/%m/%Y')
        else:
            date_str = order_dt.strftime('%m-%d-%Y')
            
        # Intentional Casing / Whitespace variations in category for data cleaning demonstration
        rand_cat = np.random.random()
        if rand_cat < 0.03:
            raw_category = cat.upper()
        elif rand_cat < 0.06:
            raw_category = f" {cat} "
        elif rand_cat < 0.08:
            raw_category = cat.lower()
        else:
            raw_category = cat
            
        records.append({
            'order_id': order_id,
            'order_date': date_str,
            'store_id': store_id,
            'region': region,
            'customer_id': customer_id,
            'product_id': product_id,
            'product_name': prod_name,
            'product_category': raw_category,
            'quantity': qty,
            'unit_price': unit_price,
            'unit_cost': unit_cost,
            'discount_pct': discount_pct,
            'revenue': net_revenue,
            'cost': total_cost,
            'payment_mode': payment_mode
        })

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # Inject Realistic Messiness / Data Quality Artifacts
    # -------------------------------------------------------------
    # 1. Duplicate records (e.g. 120 duplicate rows simulating API retries)
    duplicate_indices = np.random.choice(df.index, size=120, replace=False)
    df_dupes = df.loc[duplicate_indices].copy()
    df = pd.concat([df, df_dupes], ignore_index=True)

    # 2. Missing values (simulating dropped packets or optional fields)
    # Missing customer_id (~1.5%)
    cust_null_idx = np.random.choice(df.index, size=int(0.015 * len(df)), replace=False)
    df.loc[cust_null_idx, 'customer_id'] = np.nan

    # Missing payment_mode (~1.8%)
    pay_null_idx = np.random.choice(df.index, size=int(0.018 * len(df)), replace=False)
    df.loc[pay_null_idx, 'payment_mode'] = np.nan

    # Missing discount_pct (~1.2%)
    disc_null_idx = np.random.choice(df.index, size=int(0.012 * len(df)), replace=False)
    df.loc[disc_null_idx, 'discount_pct'] = np.nan

    # Missing unit_cost (~0.8%)
    cost_null_idx = np.random.choice(df.index, size=int(0.008 * len(df)), replace=False)
    df.loc[cost_null_idx, 'unit_cost'] = np.nan

    # 3. Erroneous values (simulating manual entry typos or sign bugs)
    # Negative quantity in 15 rows (return / cancelled orders recorded wrongly)
    neg_qty_idx = np.random.choice(df.index, size=15, replace=False)
    df.loc[neg_qty_idx, 'quantity'] = -1 * df.loc[neg_qty_idx, 'quantity']

    # Erroneous unit price zero or negative in 10 rows
    err_price_idx = np.random.choice(df.index, size=10, replace=False)
    df.loc[err_price_idx, 'unit_price'] = -10.0

    # Discount entered as integer percentage instead of decimal in 25 rows (e.g. 20.0 instead of 0.20)
    err_disc_idx = np.random.choice(df.index, size=25, replace=False)
    df.loc[err_disc_idx, 'discount_pct'] = df.loc[err_disc_idx, 'discount_pct'] * 100.0

    # Shuffle rows to simulate raw logs
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)

    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    raw_csv_path = os.path.join(output_dir, 'raw_product_sales.csv')
    df.to_csv(raw_csv_path, index=False)
    print(f"Successfully generated raw dataset: {raw_csv_path} with {len(df)} records.")
    return df

if __name__ == '__main__':
    generate_raw_data(8500)

"""
=============================================================================
Product Category Profitability Study
Script: clean_data.py
Epic: D04-E02 - Data Cleaning and Preparation
Author: Student Research Team
Description: Comprehensive data cleaning pipeline for raw sales transactions.
             Handles deduplication, missing value imputation, type casting,
             date parsing, outlier correction, financial reconciliation,
             and feature engineering.
=============================================================================
"""

import os
import pandas as pd
import numpy as np

def clean_sales_data(raw_csv_path=None, output_csv_path=None, output_excel_path=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if raw_csv_path is None:
        raw_csv_path = os.path.join(base_dir, 'data', 'raw', 'raw_product_sales.csv')
    if output_csv_path is None:
        output_csv_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_product_sales.csv')
    if output_excel_path is None:
        output_excel_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_product_sales.xlsx')

    print("=" * 70)
    print("EPIC D04-E02: COMMENCING DATA CLEANING & RECONCILIATION PIPELINE")
    print("=" * 70)
    
    # Load raw dataset
    df_raw = pd.read_csv(raw_csv_path)
    initial_rows = len(df_raw)
    print(f"[*] Initial records loaded: {initial_rows:,}")
    print(f"[*] Raw columns: {list(df_raw.columns)}")

    # 1. Deduplication
    # Check duplicate rows or duplicate order_ids
    dupes_count = df_raw.duplicated(subset=['order_id']).sum()
    print(f"[*] Duplicate order IDs detected: {dupes_count:,}")
    df_clean = df_raw.drop_duplicates(subset=['order_id'], keep='first').copy()
    print(f"[*] Records remaining after deduplication: {len(df_clean):,}")

    # 2. Standardize Categorical Strings
    print("[*] Standardizing categorical fields (casing, whitespace trimming)...")
    # Category normalization mapping
    category_map = {
        'electronics': 'Electronics',
        'apparel & footwear': 'Apparel & Footwear',
        'home & kitchen': 'Home & Kitchen',
        'office supplies': 'Office Supplies',
        'beauty & personal care': 'Beauty & Personal Care',
        'furniture': 'Furniture',
        'sports & fitness': 'Sports & Fitness'
    }
    df_clean['product_category'] = (
        df_clean['product_category']
        .astype(str)
        .str.strip()
        .apply(lambda x: category_map.get(x.lower(), x.title()))
    )
    df_clean['region'] = df_clean['region'].astype(str).str.strip().str.title()
    df_clean['store_id'] = df_clean['store_id'].astype(str).str.strip().str.upper()
    df_clean['product_id'] = df_clean['product_id'].astype(str).str.strip().str.upper()

    # 3. Robust Date Parsing
    print("[*] Normalizing heterogeneous date formats to ISO-8601 (YYYY-MM-DD)...")
    # Use format='mixed' to handle various date strings
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], format='mixed', errors='coerce')
    invalid_dates = df_clean['order_date'].isna().sum()
    if invalid_dates > 0:
        print(f"    - Warning: {invalid_dates} unparseable dates dropped.")
        df_clean = df_clean.dropna(subset=['order_date']).copy()

    # 4. Handle Missing Values (Documented Assumptions)
    print("[*] Resolving missing values with documented business assumptions:")
    # A) customer_id: replace NaN with 'GUEST_CHECKOUT' (common in retail for unregistered buyers)
    null_cust = df_clean['customer_id'].isna().sum()
    df_clean['customer_id'] = df_clean['customer_id'].fillna('GUEST_CHECKOUT')
    print(f"    - Imputed {null_cust} missing customer_id values with 'GUEST_CHECKOUT'")

    # B) payment_mode: replace NaN with 'Other / Unspecified'
    null_pay = df_clean['payment_mode'].isna().sum()
    df_clean['payment_mode'] = df_clean['payment_mode'].fillna('Other / Unspecified')
    print(f"    - Imputed {null_pay} missing payment_mode values with 'Other / Unspecified'")

    # C) unit_cost: impute missing unit_cost using median unit_cost for that product_id
    null_cost = df_clean['unit_cost'].isna().sum()
    cost_medians = df_clean.groupby('product_id')['unit_cost'].transform('median')
    df_clean['unit_cost'] = df_clean['unit_cost'].fillna(cost_medians)
    # If still any null, fill with category median
    cat_cost_medians = df_clean.groupby('product_category')['unit_cost'].transform('median')
    df_clean['unit_cost'] = df_clean['unit_cost'].fillna(cat_cost_medians)
    print(f"    - Imputed {null_cost} missing unit_cost values using SKU-level median cost")

    # D) discount_pct: impute missing discount_pct as 0.00 (standard list price)
    null_disc = df_clean['discount_pct'].isna().sum()
    df_clean['discount_pct'] = df_clean['discount_pct'].fillna(0.0)
    print(f"    - Imputed {null_disc} missing discount_pct values with 0.00 (no promotional discount)")

    # 5. Fix Outliers, Scaling & Data Entry Bugs
    print("[*] Validating and correcting numeric constraints...")
    # Fix percentage scaling: if discount_pct > 1.0 (e.g. 25 instead of 0.25), scale down by 100
    disc_rescaled = (df_clean['discount_pct'] > 1.0).sum()
    df_clean.loc[df_clean['discount_pct'] > 1.0, 'discount_pct'] /= 100.0
    # Clamp discount between 0.0 and 0.80
    df_clean['discount_pct'] = df_clean['discount_pct'].clip(0.0, 0.80).round(4)
    print(f"    - Rescaled {disc_rescaled} discount rates entered as percentages (> 1.0)")

    # Filter out non-positive quantities (cancelled / erroneous returns)
    neg_qty = (df_clean['quantity'] <= 0).sum()
    df_clean = df_clean[df_clean['quantity'] > 0].copy()
    print(f"    - Filtered out {neg_qty} records with quantity <= 0")

    # Filter out negative or zero unit prices (pricing entry error)
    neg_price = (df_clean['unit_price'] <= 0).sum()
    df_clean = df_clean[df_clean['unit_price'] > 0].copy()
    print(f"    - Filtered out {neg_price} records with unit_price <= 0")

    # 6. Financial Reconciliation & Feature Engineering
    print("[*] Recomputing unified financial ledger and engineering analytical features...")
    df_clean['quantity'] = df_clean['quantity'].astype(int)
    df_clean['unit_price'] = df_clean['unit_price'].round(2)
    df_clean['unit_cost'] = df_clean['unit_cost'].round(2)
    
    # Financial metrics re-derivation (enforcing mathematical integrity)
    df_clean['gross_revenue'] = (df_clean['quantity'] * df_clean['unit_price']).round(2)
    df_clean['discount_amount'] = (df_clean['gross_revenue'] * df_clean['discount_pct']).round(2)
    df_clean['net_revenue'] = (df_clean['gross_revenue'] - df_clean['discount_amount']).round(2)
    df_clean['total_cost'] = (df_clean['quantity'] * df_clean['unit_cost']).round(2)
    
    # Standardize column 'revenue' and 'cost' to match prompt suggested fields
    df_clean['revenue'] = df_clean['net_revenue']
    df_clean['cost'] = df_clean['total_cost']
    
    # Profit and margins
    df_clean['profit'] = (df_clean['revenue'] - df_clean['cost']).round(2)
    df_clean['profit_margin_pct'] = ((df_clean['profit'] / df_clean['revenue']) * 100).round(2)
    df_clean['cost_to_revenue_ratio'] = (df_clean['cost'] / df_clean['revenue']).round(4)
    df_clean['is_profitable'] = df_clean['profit'] > 0

    # Temporal features
    df_clean['order_year'] = df_clean['order_date'].dt.year
    df_clean['order_month'] = df_clean['order_date'].dt.strftime('%Y-%m')
    df_clean['order_quarter'] = df_clean['order_date'].dt.to_period('Q').astype(str)
    df_clean['day_of_week'] = df_clean['order_date'].dt.day_name()

    # Reorder columns logically
    ordered_cols = [
        'order_id', 'order_date', 'order_year', 'order_quarter', 'order_month', 'day_of_week',
        'store_id', 'region', 'customer_id', 'payment_mode',
        'product_id', 'product_name', 'product_category',
        'quantity', 'unit_price', 'unit_cost', 'discount_pct',
        'gross_revenue', 'discount_amount', 'revenue', 'cost',
        'profit', 'profit_margin_pct', 'cost_to_revenue_ratio', 'is_profitable'
    ]
    df_clean = df_clean[ordered_cols].sort_values('order_date').reset_index(drop=True)

    # 7. Export Processed Datasets
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df_clean.to_csv(output_csv_path, index=False)
    print(f"[✓] Saved cleaned CSV: {output_csv_path} ({len(df_clean):,} records)")

    # Also save to Excel for Power BI / Tableau direct import
    df_clean.to_excel(output_excel_path, index=False, engine='openpyxl')
    print(f"[✓] Saved cleaned Excel: {output_excel_path}")

    # Summary Statistics
    final_rows = len(df_clean)
    retention_rate = (final_rows / initial_rows) * 100
    print("-" * 70)
    print(f"Data Cleaning Audit Summary:")
    print(f"  • Initial Raw Records:     {initial_rows:,}")
    print(f"  • Final Cleaned Records:   {final_rows:,} ({retention_rate:.2f}% data retention)")
    print(f"  • Total Net Revenue:       ${df_clean['revenue'].sum():,.2f}")
    print(f"  • Total Cost of Goods:     ${df_clean['cost'].sum():,.2f}")
    print(f"  • Total Gross Profit:      ${df_clean['profit'].sum():,.2f}")
    print(f"  • Overall Margin:          {(df_clean['profit'].sum() / df_clean['revenue'].sum()) * 100:.2f}%")
    print(f"  • Date Horizon:            {df_clean['order_date'].min().strftime('%Y-%m-%d')} to {df_clean['order_date'].max().strftime('%Y-%m-%d')}")
    print("=" * 70)

    return df_clean

if __name__ == '__main__':
    clean_sales_data()

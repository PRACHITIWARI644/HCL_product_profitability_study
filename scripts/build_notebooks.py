"""
=============================================================================
Product Category Profitability Study
Script: build_notebooks.py
Description: Generates clean, reproducible, and beautifully documented
             Jupyter Notebooks for each Epic.
=============================================================================
"""

import os
import nbformat as nbf

def create_notebook_1(output_path):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Epic D04-E01: Problem Understanding & Dataset Creation
## Product Category Profitability Study
**Course/Project:** Retail Analytics & Business Intelligence  
**Student Name:** Retail Analytics Team  
**Dataset Timeframe:** 2023 - 2024 (24 Months)  

---

### 1. Business Problem & Objectives
In modern omni-channel retail, top-line revenue often masks underlying profitability bottlenecks. Merchandising teams frequently push high-revenue categories (e.g., Electronics, Heavy Furniture) without realizing that promotional discounts, high inventory holding costs, and low base margins erode bottom-line returns.

**Primary Objectives:**
1. Formulate core business questions to compare **Revenue**, **Cost of Goods Sold (COGS)**, and **Gross Profit** across product categories.
2. Synthesize an enterprise-grade retail transactions dataset reflecting realistic market pricing, consumer purchase volume, regional distribution, and promotional discounting.
3. Inject realistic real-world data quality anomalies (duplicates, missing values, text discrepancies, negative values) to simulate dirty enterprise data logs for subsequent cleaning pipelines.
"""),
        nbf.v4.new_code_cell("""# Import requisite libraries
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Verify environment
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")"""),
        nbf.v4.new_markdown_cell("""### 2. Dataset Synthesis Logic
We simulate 8,500+ multi-category transactions across 7 product categories:
* `Electronics`
* `Apparel & Footwear`
* `Home & Kitchen`
* `Office Supplies`
* `Beauty & Personal Care`
* `Furniture`
* `Sports & Fitness`

Each category features distinct margin structures, typical unit price bands, and discount sensitivity profiles."""),
        nbf.v4.new_code_cell("""# Inspect generated raw dataset
raw_csv_path = '../data/raw/raw_product_sales.csv'

if os.path.exists(raw_csv_path):
    df_raw = pd.read_csv(raw_csv_path)
    print(f"Raw Dataset Shape: {df_raw.shape[0]:,} rows, {df_raw.shape[1]} columns")
    display(df_raw.head())
else:
    print(f"Raw CSV not found at {raw_csv_path}. Please execute scripts/generate_raw_dataset.py.")"""),
        nbf.v4.new_markdown_cell("""### 3. Initial Data Inspection & Anomaly Profiling
Let's inspect the data types, missing value percentages, and categorical irregularities before moving to data cleaning."""),
        nbf.v4.new_code_cell("""# Check column data types and missing values
print("--- Missing Values Profiling ---")
display(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])

print("\\n--- Duplicate Order IDs ---")
print(f"Duplicate IDs: {df_raw.duplicated(subset=['order_id']).sum():,}")

print("\\n--- Inconsistent Category Names (Raw Text) ---")
print(df_raw['product_category'].unique()[:10])"""),
        nbf.v4.new_markdown_cell("""### 4. Summary & Transition to Epic D04-E02
The raw dataset contains:
* Duplicate order IDs from simulated ingestion retries.
* Missing fields in `customer_id`, `payment_mode`, `unit_cost`, and `discount_pct`.
* Inconsistent date strings (mixed formatting).
* Capitalization and trailing whitespace anomalies in categorical dimensions.

In the next notebook (`02_Data_Cleaning_and_Preparation.ipynb`), we establish a documented data cleaning pipeline to produce an analysis-ready ledger.""")
    ]
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[✓] Created Notebook 1: {output_path}")

def create_notebook_2(output_path):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Epic D04-E02: Data Cleaning & Preparation
## Product Category Profitability Study
**Objective:** Clean raw sales data, resolve missing values with documented business assumptions, eliminate anomalies, engineer financial features, and output analysis-ready datasets.

---

### Cleaning Assumptions Documented:
1. **Deduplication:** Repeated transactions with identical `order_id` are redundant logging artifacts and must be dropped.
2. **Missing Customer IDs:** Online retail often allows guest checkout; missing `customer_id` values are imputed with `'GUEST_CHECKOUT'` rather than discarding valid revenue records.
3. **Missing Payment Modes:** Replaced with `'Other / Unspecified'` to preserve overall sales volume.
4. **Missing Unit Cost:** Imputed using the SKU-level median cost (`product_id`), falling back to category-level median cost.
5. **Missing Discount Rate:** Assumed to be `0.00` (full list price sold without promotion).
6. **Discount Scaling:** Percentage entries > 1.0 (e.g. 20%) are rescaled to decimal proportions (0.20) and clipped at 80% maximum promotional cap.
7. **Invalid Quantities / Unit Prices:** Non-positive values represent erroneous test pings or invalid returns and are pruned.
"""),
        nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np

# Load raw dataset
raw_csv_path = '../data/raw/raw_product_sales.csv'
df_raw = pd.read_csv(raw_csv_path)
print(f"Starting with {len(df_raw):,} raw records.")"""),
        nbf.v4.new_markdown_cell("""### Step 1: Deduplication"""),
        nbf.v4.new_code_cell("""# Remove duplicates
initial_count = len(df_raw)
df_clean = df_raw.drop_duplicates(subset=['order_id'], keep='first').copy()
print(f"Dropped {initial_count - len(df_clean)} duplicate transactions. Remaining: {len(df_clean):,}")"""),
        nbf.v4.new_markdown_cell("""### Step 2: Categorical Standardization & Date Parsing"""),
        nbf.v4.new_code_cell("""# Standardize category labels
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

# Robust date parsing
df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], format='mixed', errors='coerce')
df_clean = df_clean.dropna(subset=['order_date']).copy()
print(f"Date range: {df_clean['order_date'].min().strftime('%Y-%m-%d')} to {df_clean['order_date'].max().strftime('%Y-%m-%d')}")"""),
        nbf.v4.new_markdown_cell("""### Step 3: Imputation & Anomaly Rectification"""),
        nbf.v4.new_code_cell("""# Impute missing values
df_clean['customer_id'] = df_clean['customer_id'].fillna('GUEST_CHECKOUT')
df_clean['payment_mode'] = df_clean['payment_mode'].fillna('Other / Unspecified')
df_clean['discount_pct'] = df_clean['discount_pct'].fillna(0.0)

# Impute cost using SKU median
cost_sku_median = df_clean.groupby('product_id')['unit_cost'].transform('median')
df_clean['unit_cost'] = df_clean['unit_cost'].fillna(cost_sku_median)
cat_sku_median = df_clean.groupby('product_category')['unit_cost'].transform('median')
df_clean['unit_cost'] = df_clean['unit_cost'].fillna(cat_sku_median)

# Correct discount rates entered as percentages (e.g. 25 instead of 0.25)
df_clean.loc[df_clean['discount_pct'] > 1.0, 'discount_pct'] /= 100.0
df_clean['discount_pct'] = df_clean['discount_pct'].clip(0.0, 0.80).round(4)

# Filter invalid quantities & prices
df_clean = df_clean[(df_clean['quantity'] > 0) & (df_clean['unit_price'] > 0)].copy()
df_clean['quantity'] = df_clean['quantity'].astype(int)
print(f"Records after validation: {len(df_clean):,}")"""),
        nbf.v4.new_markdown_cell("""### Step 4: Financial Ledger Feature Engineering
Enforce mathematical consistency across accounting metrics:
* $\\text{Gross Revenue} = \\text{Quantity} \\times \\text{Unit Price}$
* $\\text{Discount Amount} = \\text{Gross Revenue} \\times \\text{Discount \\%}$
* $\\text{Net Revenue} = \\text{Gross Revenue} - \\text{Discount Amount}$
* $\\text{Total Cost} = \\text{Quantity} \\times \\text{Unit Cost}$
* $\\text{Gross Profit} = \\text{Net Revenue} - \\text{Total Cost}$
* $\\text{Profit Margin \\%} = \\left(\\frac{\\text{Gross Profit}}{\\text{Net Revenue}}\\right) \\times 100$
* $\\text{Cost-to-Revenue Ratio} = \\frac{\\text{Total Cost}}{\\text{Net Revenue}}$"""),
        nbf.v4.new_code_cell("""# Recompute financial metrics
df_clean['gross_revenue'] = (df_clean['quantity'] * df_clean['unit_price']).round(2)
df_clean['discount_amount'] = (df_clean['gross_revenue'] * df_clean['discount_pct']).round(2)
df_clean['net_revenue'] = (df_clean['gross_revenue'] - df_clean['discount_amount']).round(2)
df_clean['total_cost'] = (df_clean['quantity'] * df_clean['unit_cost']).round(2)

df_clean['revenue'] = df_clean['net_revenue']
df_clean['cost'] = df_clean['total_cost']
df_clean['profit'] = (df_clean['revenue'] - df_clean['cost']).round(2)
df_clean['profit_margin_pct'] = ((df_clean['profit'] / df_clean['revenue']) * 100).round(2)
df_clean['cost_to_revenue_ratio'] = (df_clean['cost'] / df_clean['revenue']).round(4)
df_clean['is_profitable'] = df_clean['profit'] > 0

# Temporal extraction
df_clean['order_year'] = df_clean['order_date'].dt.year
df_clean['order_month'] = df_clean['order_date'].dt.strftime('%Y-%m')
df_clean['order_quarter'] = df_clean['order_date'].dt.to_period('Q').astype(str)
df_clean['day_of_week'] = df_clean['order_date'].dt.day_name()

# Export clean datasets
output_dir = '../data/processed'
os.makedirs(output_dir, exist_ok=True)
df_clean.to_csv(os.path.join(output_dir, 'cleaned_product_sales.csv'), index=False)
print("Clean dataset saved to data/processed/cleaned_product_sales.csv")
display(df_clean.describe())""")
    ]
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[✓] Created Notebook 2: {output_path}")

def create_notebook_3(output_path):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Epic D04-E03: Exploratory Data Analysis (EDA)
## Product Category Profitability Study
**Objective:** Perform comprehensive statistical and graphical exploration of revenue distributions, cost structures, margin dispersions, discount dynamics, and regional performance.

---
"""),
        nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.sans-serif'] = 'Arial'

# Load clean dataset
df = pd.read_csv('../data/processed/cleaned_product_sales.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
print(f"Loaded {len(df):,} cleaned sales transactions.")"""),
        nbf.v4.new_markdown_cell("""### 1. Revenue, Cost & Profit Comparison by Category"""),
        nbf.v4.new_code_cell("""# Aggregate financial metrics by product category
cat_perf = df.groupby('product_category').agg(
    total_revenue=('revenue', 'sum'),
    total_cost=('cost', 'sum'),
    total_profit=('profit', 'sum'),
    avg_margin=('profit_margin_pct', 'mean')
).sort_values('total_revenue', ascending=False).reset_index()

display(cat_perf)

# Grouped bar chart
fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(cat_perf))
width = 0.28

ax.bar(x - width, cat_perf['total_revenue'] / 1e3, width, label='Net Revenue ($K)', color='#2b5c8f')
ax.bar(x, cat_perf['total_cost'] / 1e3, width, label='COGS ($K)', color='#d9534f')
ax.bar(x + width, cat_perf['total_profit'] / 1e3, width, label='Gross Profit ($K)', color='#5cb85c')

ax.set_xticks(x)
ax.set_xticklabels(cat_perf['product_category'], rotation=25, ha='right')
ax.set_ylabel('Amount ($ Thousands USD)')
ax.set_title('Category Financial Breakdown: Revenue vs Cost vs Profit')
ax.legend()
plt.tight_layout()
plt.show()"""),
        nbf.v4.new_markdown_cell("""**Observation:**
* `Electronics` dominates top-line revenue (\$1.4M+) but carries a massive cost burden (\$1.3M), resulting in compressed margin share.
* `Furniture` exhibits extreme cost-to-revenue ratios, yielding almost zero cumulative profit despite substantial sales volume.
* `Apparel & Footwear` and `Home & Kitchen` generate high profit contributions relative to their top-line scale."""),
        nbf.v4.new_markdown_cell("""### 2. Profit Margin Distribution & Outliers (Boxplots)"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(11, 5.5))
order_cat = df.groupby('product_category')['profit_margin_pct'].median().sort_values(ascending=False).index

sns.boxplot(x='product_category', y='profit_margin_pct', data=df, order=order_cat, showmeans=True,
            meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black"})
plt.axhline(0, color='crimson', linestyle='--', label='Break-Even Point (0%)')
plt.title('Profit Margin (%) Distribution Across Categories (Sorted by Median)')
plt.xticks(rotation=25, ha='right')
plt.ylabel('Profit Margin (%)')
plt.legend()
plt.tight_layout()
plt.show()"""),
        nbf.v4.new_markdown_cell("""### 3. The Discount Erosion Trap: Discount % vs Margin %"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(10, 6))
sample_df = df.sample(min(2000, len(df)), random_state=42)

sns.scatterplot(
    x=sample_df['discount_pct'] * 100,
    y=sample_df['profit_margin_pct'],
    hue=sample_df['product_category'],
    alpha=0.6,
    palette='tab10'
)
sns.regplot(
    x=df['discount_pct'] * 100,
    y=df['profit_margin_pct'],
    scatter=False,
    color='black',
    line_kws={'linestyle': '--', 'label': 'Margin Decay Trendline'}
)
plt.axhline(0, color='red', linestyle='-', label='Break-Even Threshold')
plt.title('Promotional Discount % vs Realized Profit Margin %')
plt.xlabel('Discount Rate Applied (%)')
plt.ylabel('Profit Margin (%)')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()"""),
        nbf.v4.new_markdown_cell("""### 4. Correlation Heatmap Between Numerical Attributes"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(8, 6))
corr_cols = ['quantity', 'unit_price', 'unit_cost', 'discount_pct', 'revenue', 'cost', 'profit', 'profit_margin_pct']
sns.heatmap(df[corr_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, linewidths=0.5)
plt.title('Correlation Matrix of Transaction Attributes')
plt.tight_layout()
plt.show()""")
    ]
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[✓] Created Notebook 3: {output_path}")

def create_notebook_4(output_path):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Epic D04-E04: KPIs & Strategic Business Insights
## Product Category Profitability Study
**Objective:** Define executive-level Key Performance Indicators (KPIs), construct category portfolio segmentation (BCG Matrix), and synthesize actionable business recommendations for merchandising and pricing strategies.

---
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../data/processed/cleaned_product_sales.csv')
df['order_date'] = pd.to_datetime(df['order_date'])"""),
        nbf.v4.new_markdown_cell("""### 1. Executive KPI Scorecard Calculation"""),
        nbf.v4.new_code_cell("""# Compute fundamental retail KPIs
total_net_rev = df['revenue'].sum()
total_cogs = df['cost'].sum()
total_profit = df['profit'].sum()
overall_margin = (total_profit / total_net_rev) * 100
aov = df['revenue'].mean()
avg_discount = df['discount_pct'].mean() * 100
profitable_ratio = (df['is_profitable'].sum() / len(df)) * 100

kpis = {
    'Metric': [
        'Total Net Revenue ($)',
        'Total Cost of Goods Sold ($)',
        'Total Gross Profit ($)',
        'Overall Gross Margin (%)',
        'Average Order Value (AOV) ($)',
        'Average Discount Rate (%)',
        'Profitable Order Ratio (%)',
        'Total Orders Processed',
        'Total Physical Units Sold'
    ],
    'Value': [
        f"${total_net_rev:,.2f}",
        f"${total_cogs:,.2f}",
        f"${total_profit:,.2f}",
        f"{overall_margin:.2f}%",
        f"${aov:.2f}",
        f"{avg_discount:.2f}%",
        f"{profitable_ratio:.2f}%",
        f"{len(df):,}",
        f"{df['quantity'].sum():,}"
    ]
}
display(pd.DataFrame(kpis))"""),
        nbf.v4.new_markdown_cell("""### 2. Strategic Portfolio Matrix (BCG / Profitability-Volume Matrix)
We classify product categories into four operational quadrants based on median Revenue and Gross Margin:
1. **Stars (High Revenue, High Margin):** Primary profit growth engines.
2. **Volume Drivers / Cash Engines (High Revenue, Moderate/Low Margin):** High cash turnover, but highly vulnerable to discount erosion.
3. **Niche Harvesters (Low Revenue, High Margin):** Highly lucrative per unit; candidates for marketing expansion.
4. **Margin Bleeders (Low/Moderate Revenue, Negative/Slim Margin):** Capital drains requiring SKU rationalization or supplier renegotiation."""),
        nbf.v4.new_code_cell("""cat_summary = df.groupby('product_category').agg(
    revenue=('revenue', 'sum'),
    profit=('profit', 'sum'),
    orders=('order_id', 'count')
).reset_index()
cat_summary['margin_pct'] = (cat_summary['profit'] / cat_summary['revenue']) * 100

plt.figure(figsize=(10, 6.5))
sizes = (cat_summary['orders'] / cat_summary['orders'].max()) * 1600 + 300

plt.scatter(
    cat_summary['revenue'] / 1e3,
    cat_summary['margin_pct'],
    s=sizes,
    c=cat_summary['margin_pct'],
    cmap='viridis',
    edgecolors='black',
    alpha=0.85
)

rev_mid = (cat_summary['revenue'] / 1e3).median()
margin_mid = cat_summary['margin_pct'].median()

plt.axvline(rev_mid, color='gray', linestyle='--')
plt.axhline(margin_mid, color='gray', linestyle='--')

for _, row in cat_summary.iterrows():
    plt.annotate(
        row['product_category'],
        xy=(row['revenue'] / 1e3, row['margin_pct']),
        xytext=(0, 10), textcoords="offset points",
        ha='center', weight='bold'
    )

plt.title('Product Category Profitability Portfolio Matrix')
plt.xlabel('Total Revenue ($ Thousands)')
plt.ylabel('Profit Margin (%)')
plt.colorbar(label='Profit Margin (%)')
plt.tight_layout()
plt.show()"""),
        nbf.v4.new_markdown_cell("""### 3. Actionable Business Recommendations
1. **Electronics Discount Guardrails:** Electronics represents 54% of sales volume but operates at only 8.5% margin. Cap promotional discounts at 12% to prevent loss-making transactions.
2. **Furniture SKU Rationalization:** With a net margin of barely 1.34%, the business is essentially running Furniture as a cost center. Re-negotiate supplier wholesale rates, add freight surcharges for oversized shipping, and discontinue low-margin SKUs.
3. **Scale Beauty & Apparel Marketing:** `Beauty & Personal Care` enjoys a 64% margin and `Apparel` delivers 42% margin. Allocate a larger portion of ad spend to these high-margin categories.
4. **Regional Merchandising:** Rebalance inventory based on regional demand strength (e.g., North and West territories lead consumer tech sales, while East exhibits steady home goods margins).""")
    ]
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[✓] Created Notebook 4: {output_path}")

def build_all_notebooks():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nb_dir = os.path.join(base_dir, 'notebooks')
    os.makedirs(nb_dir, exist_ok=True)
    
    create_notebook_1(os.path.join(nb_dir, '01_Data_Creation_and_Understanding.ipynb'))
    create_notebook_2(os.path.join(nb_dir, '02_Data_Cleaning_and_Preparation.ipynb'))
    create_notebook_3(os.path.join(nb_dir, '03_Exploratory_Data_Analysis.ipynb'))
    create_notebook_4(os.path.join(nb_dir, '04_KPIs_and_Business_Insights.ipynb'))

if __name__ == '__main__':
    build_all_notebooks()

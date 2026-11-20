# Data Dictionary — Product Category Profitability Study (D04)

## Overview
This document specifies the schema, definitions, expected data types, and business rules for the raw and processed transactions dataset used in the **Product Category Profitability Study**.

The dataset represents multi-channel retail operations spanning a 24-month horizon (January 1, 2023 to December 31, 2024), covering 7 distinct product categories, 25 retail stores across 5 geographic regions, and multiple digital/in-person payment channels.

---

## Schema & Field Specifications

| Column Name | Raw Data Type | Cleaned Data Type | Description | Allowed Values / Range | Example Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `VARCHAR` / `str` | `String (Categorical)` | Unique transaction identifier | Format: `ORD-YYYY-XXXXX` | `ORD-2023-10482` |
| `order_date` | `VARCHAR` / `str` | `Datetime (YYYY-MM-DD)` | Date of customer purchase transaction | 2023-01-01 to 2024-12-31 | `2023-11-14` |
| `store_id` | `VARCHAR` / `str` | `String (Categorical)` | Origin store / fulfillment center identifier | `STR_101` to `STR_125` | `STR_108` |
| `region` | `VARCHAR` / `str` | `Category` | Geographic retail territory | `North`, `South`, `East`, `West`, `Central` | `North` |
| `customer_id` | `VARCHAR` / `str` | `String` | Unique customer account identifier | `CUST_1001` to `CUST_2800` (or `GUEST_CHECKOUT`) | `CUST_1492` |
| `product_id` | `VARCHAR` / `str` | `String (Categorical)` | Unique SKU / product catalog code | E.g., `ELEC_101`, `APP_201` | `ELEC_104` |
| `product_name` | `VARCHAR` / `str` | `String` | Human-readable merchandise title | Descriptive product title | `Ultra-Slim Gaming Laptop` |
| `product_category` | `VARCHAR` / `str` | `Category` | High-level merchandise category | 7 Standard Categories | `Electronics` |
| `quantity` | `INT` / `float` | `Integer` | Number of merchandise units purchased | Strictly $\ge 1$ (Cleaned: $1$ to $5$) | `2` |
| `unit_price` | `FLOAT` | `Float` | Listed selling price per unit before discount (USD) | Strictly $> 0$ (\$10.00 to \$1,400.00) | `1180.50` |
| `unit_cost` | `FLOAT` | `Float` | Cost of Goods Sold (COGS) per unit (USD) | Strictly $> 0$ (\$5.00 to \$1,100.00) | `960.20` |
| `discount_pct` | `FLOAT` | `Float` | Discount rate applied to the line item | $0.00$ to $0.60$ ($0\%$ to $60\%$) | `0.15` |
| `revenue` | `FLOAT` | `Float` | Net sales realized after discount ($Net = Gross - Discount$) | Strictly $> 0$ (USD) | `2006.85` |
| `cost` | `FLOAT` | `Float` | Total Cost of Goods Sold ($Cost = Unit Cost \times Quantity$) | Strictly $> 0$ (USD) | `1920.40` |
| `payment_mode` | `VARCHAR` / `str` | `Category` | Tender type / settlement method used | `Credit Card`, `Debit Card`, `UPI`, `Net Banking`, `Cash on Delivery` | `Credit Card` |

---

## Derived / Engineered Financial Features (Added in Cleaning Phase)

| Feature Name | Formula / Derivation | Business Purpose & Interpretation |
| :--- | :--- | :--- |
| `gross_revenue` | `quantity * unit_price` | Top-line nominal billing value before applying promotions |
| `discount_amount` | `gross_revenue * discount_pct` | Dollar value sacrificed to promotional discounting |
| `net_revenue` | `gross_revenue - discount_amount` | Actual top-line money collected from the customer |
| `profit` (Gross Margin \$) | `net_revenue - cost` | Dollar contribution margin towards operating expenses |
| `profit_margin_pct` | `(profit / net_revenue) * 100` | Percentage of net revenue retained as gross profit |
| `cost_to_revenue_ratio` | `cost / net_revenue` | Efficiency indicator: fraction of revenue consumed by inventory cost |
| `is_profitable` | `profit > 0` (Boolean flag) | Flags transactions that eroded capital or generated positive margin |
| `order_year` | `order_date.dt.year` | Calendar year for annual comparative analysis |
| `order_quarter` | `order_date.dt.to_period('Q')` | Fiscal / seasonal quarterly grouping (Q1 to Q4) |
| `order_month` | `order_date.dt.strftime('%Y-%m')` | Monthly aggregation identifier |
| `day_of_week` | `order_date.dt.day_name()` | Weekly shopping pattern analysis |

---

## Business Questions Answered by this Dataset
1. **Category Profit Contribution**: Which product categories drive the highest gross dollar profit versus highest top-line revenue?
2. **Margin Health**: What are the average and median profit margins by category, and which categories suffer from compressed margins?
3. **The Discount Erosion Trap**: How does discounting impact margin percentages? At what discount threshold do categories become loss-making?
4. **Geographic Heterogeneity**: Are certain product categories significantly more profitable in specific geographic territories (North vs South vs East vs West vs Central)?
5. **Cost vs Revenue Dynamics**: What is the cost-to-revenue ratio across categories, and which categories represent high capital exposure?
6. **Temporal & Seasonal Patterns**: How do festive seasons (e.g. Q4 Black Friday / Holiday promotions) impact net margins compared to steady-state months?
7. **Payment Mode Economics**: Do order basket sizes and profit margins differ across payment channels (e.g. Digital UPI/Cards vs Cash on Delivery)?

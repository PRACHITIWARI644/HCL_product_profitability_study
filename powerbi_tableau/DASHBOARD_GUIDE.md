# Power BI & Tableau Implementation Guide: Product Category Profitability Study (D04)

This comprehensive guide enables students and evaluators to import the cleaned transactions dataset (`data/processed/cleaned_product_sales.xlsx` or `.csv`) into **Power BI Desktop** or **Tableau Desktop / Tableau Public** to reproduce the enterprise executive dashboard.

---

## 1. Quick Data Ingestion

### Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Excel workbook** (or **Text/CSV**).
3. Select `data/processed/cleaned_product_sales.xlsx`.
4. Check the `Sheet1` table preview and click **Transform Data** (Power Query).
5. Verify column data types:
   - `order_date`: `Date`
   - `quantity`: `Whole Number`
   - `unit_price`, `unit_cost`, `revenue`, `cost`, `profit`: `Fixed decimal number` ($ Currency)
   - `discount_pct`, `profit_margin_pct`: `Percentage` / `Decimal`
6. Click **Close & Apply**.

### Tableau Desktop / Public
1. Open **Tableau** $\rightarrow$ Under **Connect** $\rightarrow$ **Microsoft Excel**.
2. Select `data/processed/cleaned_product_sales.xlsx`.
3. Ensure `Order Date` is recognized as a **Date** dimension, and `Product Category`, `Region`, and `Payment Mode` are recognized as **Dimensions**.

---

## 2. Power BI DAX Formulas (Measures Library)

Create a dedicated table named `_Measures` in Power BI and paste the following verified DAX expressions:

```dax
// 1. Total Net Revenue
Total Revenue = SUM(cleaned_product_sales[revenue])

// 2. Total Cost of Goods Sold (COGS)
Total Cost = SUM(cleaned_product_sales[cost])

// 3. Gross Profit
Total Gross Profit = [Total Revenue] - [Total Cost]

// 4. Gross Profit Margin %
Gross Profit Margin % = 
DIVIDE(
    [Total Gross Profit],
    [Total Revenue],
    0
)

// 5. Total Order Count
Total Orders = DISTINCTCOUNT(cleaned_product_sales[order_id])

// 6. Average Order Value (AOV)
Average Order Value = 
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)

// 7. Average Promotional Discount Rate
Avg Discount % = AVERAGE(cleaned_product_sales[discount_pct])

// 8. Cost-to-Revenue Ratio
Cost to Revenue Ratio = 
DIVIDE(
    [Total Cost],
    [Total Revenue],
    0
)

// 9. Profitable Orders Ratio
Profitable Orders Count = 
CALCULATE(
    COUNTROWS(cleaned_product_sales),
    cleaned_product_sales[profit] > 0
)

Profitable Orders Ratio % = 
DIVIDE(
    [Profitable Orders Count],
    COUNTROWS(cleaned_product_sales),
    0
)

// 10. Prior Year Revenue (YoY Analysis)
Revenue PY = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(cleaned_product_sales[order_date])
)

// 11. Year-over-Year Growth %
YoY Revenue Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue PY],
    [Revenue PY],
    0
)
```

---

## 3. Tableau Calculated Fields Library

In Tableau, right-click on the data pane $\rightarrow$ **Create Calculated Field**:

```tableau
// 1. Total Gross Profit
[Gross Profit] = SUM([Revenue]) - SUM([Cost])

// 2. Gross Margin Percentage
[Gross Margin %] = ([Gross Profit]) / SUM([Revenue])

// 3. Cost to Revenue Ratio
[Cost Ratio] = SUM([Cost]) / SUM([Revenue])

// 4. Profitability Status Flag
[Profit Status] = IF [Profit] > 0 THEN "Profitable" ELSE "Unprofitable" END

// 5. BCG Category Quadrant
[BCG Classification] = 
IF SUM([Revenue]) >= 200000 AND [Gross Margin %] >= 0.25 THEN "Star"
ELSEIF SUM([Revenue]) >= 200000 AND [Gross Margin %] < 0.25 THEN "Volume Driver"
ELSEIF SUM([Revenue]) < 200000 AND [Gross Margin %] >= 0.25 THEN "Niche Harvester"
ELSE "Margin Bleeder"
END
```

---

## 4. Visual Layout Specifications

### Canvas Grid Layout (16:9 1920x1080 or 1280x720)

```
+---------------------------------------------------------------------------------------------------+
|  [LOGO]  PRODUCT CATEGORY PROFITABILITY STUDY — EXECUTIVE BI DASHBOARD                           |
|  Filters: Date Range | Product Category | Territory / Region | Payment Mode                       |
+---------------------------------------------------------------------------------------------------+
|  [KPI CARD 1]      | [KPI CARD 2]      | [KPI CARD 3]      | [KPI CARD 4]     | [KPI CARD 5]      |
|  Net Revenue       | Total COGS        | Gross Profit      | Gross Margin %   | Avg Order Value   |
|  $2,627,396        | $2,196,101        | $431,295          | 16.42%           | $310.02           |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 1: Clustered Column & Line Chart           |  VISUAL 2: Donut Chart                       |
|  X-Axis: Product Category                          |  Values: Total Profit by Category            |
|  Columns: Net Revenue ($), Total Cost ($)          |  Color: Rainbow / Discrete Palette           |
|  Line: Gross Margin %                              |  Legend: Top-right                           |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 3: Monthly Trajectory Area Chart           |  VISUAL 4: Category Portfolio BCG Matrix     |
|  X-Axis: Order Month (2023-01 to 2024-12)          |  X-Axis: Total Net Revenue                   |
|  Y-Axis: Monthly Revenue & Gross Profit            |  Y-Axis: Gross Margin %                      |
|  Secondary Y-Axis: Monthly Margin %                |  Size: Total Orders                          |
+---------------------------------------------------------------------------------------------------+
|  VISUAL 5: Regional Heatmap Matrix                 |  VISUAL 6: Tender / Payment Mode Bar Chart   |
|  Rows: Product Category, Columns: Region           |  Bars: Net Revenue by Payment Mode           |
|  Values: Mean Margin % (Conditional Formatting)    |  Tooltip: AOV, Transaction Count             |
+---------------------------------------------------------------------------------------------------+
```

---

## 5. Visual Formatting & Color Standards

- **Primary Brand / Revenue Color:** Deep Corporate Blue (`#1E3A8A` or `#2563EB`)
- **Cost / Expense Color:** Crimson Red (`#DC2626` or `#EF4444`)
- **Gross Profit / Positive Margin:** Forest Emerald (`#16A34A` or `#10B981`)
- **Warning / Neutral Trend:** Amber Gold (`#D97706` or `#F59E0B`)
- **Canvas Background:** Modern Off-White (`#F8FAFC`)
- **Card Background:** Pure White (`#FFFFFF`) with 1px border (`#E2E8F0`)

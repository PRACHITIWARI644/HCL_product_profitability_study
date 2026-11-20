# Product Category Profitability Study (Project D04)

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Dashboard-Streamlit%20%7C%20Plotly-red?logo=streamlit)](https://streamlit.io/)
[![BI Compatibility](https://img.shields.io/badge/BI-Power%20BI%20%7C%20Tableau-yellow?logo=powerbi)](powerbi_tableau/DASHBOARD_GUIDE.md)
[![Release](https://img.shields.io/badge/Release-v1.0.0-blueviolet?logo=git)](https://github.com/)

An enterprise-grade **Retail Analytics & Business Intelligence** capstone project comparing **Revenue**, **Cost of Goods Sold (COGS)**, and **Gross Profit** across 7 product categories over a 24-month operating horizon (8,475 validated transactions). 

Designed to uncover the hidden discrepancy between top-line sales volume and bottom-line margin realization, and to identify operational remedies for margin erosion.

---

## 📑 Table of Contents
- [Project Overview & Business Problem](#project-overview--business-problem)
- [Technology Stack](#technology-stack)
- [Agile Epics & Deliverables](#agile-epics--deliverables)
- [Repository Structure](#repository-structure)
- [Executive KPI Summary](#executive-kpi-summary)
- [Key Business Insights](#key-business-insights)
- [Interactive Dashboards](#interactive-dashboards)
- [Power BI & Tableau Guide](#power-bi--tableau-guide)
- [Quickstart & Reproduction Guide](#quickstart--reproduction-guide)
- [Release Notes (v1.0.0)](#release-notes-v100)

---

## 🎯 Project Overview & Business Problem

In high-growth omnichannel retail, management often focuses exclusively on top-line **Gross Merchandise Value (GMV)** and revenue expansion. This frequently creates a dangerous phenomenon known as the **"Scale Illusion"**—where departments like Consumer Electronics generate massive transaction volume while surrendering margins to promotional discounts, high inventory holding costs, and supplier markups.

### Core Objectives:
1. **Compare Financial Ledgers:** Dissect Revenue vs COGS vs Gross Profit across 7 departments.
2. **Examine Promotional Margin Decay:** Quantify the impact of promotional discounts on net category profitability.
3. **Audit Data Quality:** Build an enterprise cleaning pipeline handling missing fields, duplicates, and pricing anomalies with documented assumptions.
4. **Portfolio Classification:** Segment categories into **Stars**, **Volume Drivers**, **Niche Harvesters**, and **Margin Bleeders**.
5. **Multi-Platform Deployment:** Deliver interactive analysis across reproducible Jupyter Notebooks, a live Streamlit web application, a standalone offline HTML dashboard, and Power BI / Tableau blueprints.

---

## 🛠️ Technology Stack

| Layer | Tools & Libraries |
| :--- | :--- |
| **Data Processing & Manipulation** | Python 3.12+, `pandas`, `numpy`, `openpyxl` |
| **Statistical & Visual EDA** | `matplotlib`, `seaborn`, `plotly` |
| **Interactive Application** | `streamlit`, `plotly-express` |
| **Notebook Environments** | Jupyter Notebook, Google Colab (`.ipynb`) |
| **Enterprise Business Intelligence** | Microsoft Power BI Desktop, Tableau Desktop / Public |
| **Version Control & Agile Tracking** | Git, GitHub / GitLab workflow, SemVer `v1.0.0` |

---

## 🏆 Agile Epics & Deliverables

This capstone project is structured around the 6 core project Epics:

| Epic ID | Epic Title | Description & Scope | Deliverable Assets | Status |
| :---: | :--- | :--- | :--- | :---: |
| **D04-E01** | **Problem Understanding & Dataset Creation** | Define core business questions, design transaction schema, and synthesize 8,500+ records with realistic data quality anomalies. | `scripts/generate_raw_dataset.py`<br>`data/raw/raw_product_sales.csv`<br>`data/raw/data_dictionary.md`<br>`notebooks/01_Data_Creation_and_Understanding.ipynb` | **Completed** |
| **D04-E02** | **Data Cleaning & Preparation** | Deduplicate records, standardize categories, parse dates, impute missing values with documented rules, and engineer accounting features. | `scripts/clean_data.py`<br>`data/processed/cleaned_product_sales.csv`<br>`data/processed/cleaned_product_sales.xlsx`<br>`notebooks/02_Data_Cleaning_and_Preparation.ipynb` | **Completed** |
| **D04-E03** | **Exploratory Data Analysis (EDA)** | Explore distributions, margin spreads, time-series trends, discount decay, and territorial performance. | `scripts/run_analysis.py`<br>`figures/*.png` (7 High-Res Charts)<br>`notebooks/03_Exploratory_Data_Analysis.ipynb` | **Completed** |
| **D04-E04** | **KPIs & Business Insights** | Calculate executive KPIs, construct the Category Portfolio Matrix (BCG Matrix), and derive actionable merchandising strategies. | `notebooks/04_KPIs_and_Business_Insights.ipynb`<br>`figures/06_bcg_profitability_matrix.png` | **Completed** |
| **D04-E05** | **Dashboard & Visualization** | Build multi-tab interactive Streamlit web dashboard, zero-dependency offline HTML dashboard, and Power BI DAX specs. | `dashboard/app.py`<br>`dashboard/generate_html_dashboard.py`<br>`dashboard/standalone_dashboard.html`<br>`powerbi_tableau/DASHBOARD_GUIDE.md` | **Completed** |
| **D04-E06** | **Reporting & Git Release** | Compile comprehensive formal academic project report, 10-slide executive presentation deck, and tag Git `v1.0.0` release. | `reports/Final_Project_Report.md`<br>`reports/Executive_Presentation.md`<br>`README.md`<br>Git Tag `v1.0.0` | **Completed** |

---

## 📁 Repository Structure

```
product-category-profitability-study/
├── .gitignore                           # Git ignore configurations
├── requirements.txt                     # Production Python dependencies
├── README.md                            # Comprehensive project documentation
│
├── data/
│   ├── raw/
│   │   ├── raw_product_sales.csv        # Raw transaction log (8,620 rows)
│   │   └── data_dictionary.md           # Schema definitions and data rules
│   └── processed/
│       ├── cleaned_product_sales.csv    # Analysis-ready clean ledger (8,475 rows)
│       └── cleaned_product_sales.xlsx   # Excel workbook for Power BI / Tableau
│
├── scripts/
│   ├── generate_raw_dataset.py          # Data synthesis engine (Epic E01)
│   ├── clean_data.py                    # Cleaning & feature pipeline (Epic E02)
│   ├── run_analysis.py                  # Statistical EDA & figure generation (Epic E03-E04)
│   └── build_notebooks.py               # Generates reproducible Jupyter notebooks
│
├── notebooks/
│   ├── 01_Data_Creation_and_Understanding.ipynb
│   ├── 02_Data_Cleaning_and_Preparation.ipynb
│   ├── 03_Exploratory_Data_Analysis.ipynb
│   └── 04_KPIs_and_Business_Insights.ipynb
│
├── dashboard/
│   ├── app.py                           # Multi-tab Streamlit web application
│   ├── generate_html_dashboard.py       # Compiles standalone HTML dashboard
│   └── standalone_dashboard.html        # Zero-server offline Plotly dashboard
│
├── powerbi_tableau/
│   ├── DASHBOARD_GUIDE.md               # Step-by-step DAX formulas & visual wireframes
│   └── dataset_schema.json              # Data types and measures metadata
│
├── reports/
│   ├── Final_Project_Report.md          # Comprehensive formal academic report
│   └── Executive_Presentation.md        # 10-slide executive presentation deck
│
└── figures/                             # Exported high-resolution publication charts
    ├── 01_revenue_cost_profit_by_category.png
    ├── 02_profit_margin_distribution.png
    ├── 03_discount_vs_profit_margin_scatter.png
    ├── 04_monthly_financial_trends.png
    ├── 05_regional_category_profitability_heatmap.png
    ├── 06_bcg_profitability_matrix.png
    └── 07_payment_mode_analysis.png
```

---

## 📊 Executive KPI Summary

Across the 24-month horizon (January 2023 - December 2024):

* **Gross Top-Line Revenue:** \$3,073,988.07
* **Promotional Discounts Surrendered:** \$446,592.09 (14.53% concession)
* **Net Realized Revenue:** **\$2,627,395.98**
* **Cost of Goods Sold (COGS):** **\$2,196,101.34**
* **Gross Contribution Profit:** **\$431,294.64**
* **Composite Gross Margin:** **16.42%**
* **Average Order Value (AOV):** **\$310.02**
* **Average Discount Rate:** **14.10%**
* **Profitable Transaction Rate:** **93.05%**

---

## 💡 Key Business Insights

### Departmental Performance Ledger
| Product Category | Net Revenue | Total Cost | Gross Profit | Gross Margin % | Revenue Share | Profit Share |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Electronics** | \$1,423,452.75 | \$1,302,152.83 | \$121,299.92 | **8.52%** | **54.18%** | **28.12%** |
| **Furniture** | \$314,830.13 | \$310,601.47 | \$4,228.66 | **1.34%** | **11.98%** | **0.98%** |
| **Home & Kitchen** | \$274,709.63 | \$189,258.24 | \$85,451.39 | **31.11%** | **10.46%** | **19.81%** |
| **Apparel & Footwear** | \$194,946.68 | \$112,782.10 | \$82,164.58 | **42.15%** | **7.42%** | **19.05%** |
| **Office Supplies** | \$187,197.46 | \$131,979.54 | \$55,217.92 | **29.50%** | **7.12%** | **12.80%** |
| **Sports & Fitness** | \$173,435.73 | \$128,155.44 | \$45,280.29 | **26.11%** | **6.60%** | **10.50%** |
| **Beauty & Personal Care** | \$58,823.60 | \$21,171.72 | \$37,651.88 | **64.01%** | **2.24%** | **8.73%** |

### Critical Takeaways:
1. **The Electronics Illusion:** Electronics commands over 54% of sales, yet delivers only 28% of profit due to an 8.52% net margin.
2. **The Furniture Margin Crisis:** Furniture generated \$314.8K in sales but yielded only \$4,228 in gross profit (1.34% margin) due to heavy shipping/handling costs and aggressive promotions.
3. **High-Margin Growth Engines:** Beauty & Personal Care (64.01% margin) and Apparel & Footwear (42.15% margin) produce \$119.8K in profit on just \$253.8K in sales.
4. **The Discount Trap:** Every 5% increase in promotional discount rate reduces category margins by ~4.2 percentage points. At discounts $> 14\%$, Electronics and Furniture enter negative margin territory.

---

## 🖥️ Interactive Dashboards

### 1. Live Streamlit Web App (`dashboard/app.py`)
Features dynamic sidebar filters (Date Range, Categories, Regions, Payment Channels), interactive Plotly visualizations, KPI cards, and an interactive **Discount Sensitivity Simulator** that projects margin recovery when setting discount caps.

To run:
```bash
streamlit run dashboard/app.py
```

### 2. Standalone Offline HTML Dashboard (`dashboard/standalone_dashboard.html`)
A self-contained HTML file compiled with Plotly JS that opens in **Google Chrome, Microsoft Edge, or Safari** without requiring Python or server processes. Ideal for offline evaluators.

---

## 📊 Power BI & Tableau Guide

The directory `powerbi_tableau/` includes:
- `cleaned_product_sales.xlsx`: Cleaned data ready for direct import.
- `DASHBOARD_GUIDE.md`: Contains verified **DAX Measures** (`Total Revenue`, `Gross Profit Margin %`, `Cost to Revenue Ratio`, `YoY Growth %`), Tableau calculated fields, visual canvas layout wireframes, and color standards.

---

## 🚀 Quickstart & Reproduction Guide

### 1. Clone & Set Up Environment
```bash
git clone <repository_url>
cd product-category-profitability-study
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Execute Data & Analysis Pipeline
```bash
# 1. Synthesize raw transaction log (Epic E01)
python scripts/generate_raw_dataset.py

# 2. Run data cleaning & feature engineering (Epic E02)
python scripts/clean_data.py

# 3. Compute statistical EDA and render figures (Epic E03-E04)
python scripts/run_analysis.py

# 4. Generate standalone HTML dashboard (Epic E05)
python scripts/generate_html_dashboard.py

# 5. Build reproducible Jupyter Notebooks
python scripts/build_notebooks.py
```

### 3. Launch the Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 🏷️ Release Notes (v1.0.0)

- **Release Tag:** `v1.0.0`
- **Features:** Complete coverage of Agile Epics D04-E01 through D04-E06.
- **Verification:** All scripts, notebooks, figures, reports, and dashboards generated and validated.

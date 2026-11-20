"""
=============================================================================
Product Category Profitability Study
Script: run_analysis.py
Epics: D04-E03 (Exploratory Data Analysis) & D04-E04 (KPIs & Business Insights)
Author: Student Research Team
Description: Computes comprehensive statistical aggregations, KPI metrics,
             and generates publication-quality charts saved to figures/.
=============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

def perform_eda_and_kpis():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, 'data', 'processed', 'cleaned_product_sales.csv')
    fig_dir = os.path.join(base_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)

    print("=" * 70)
    print("EPIC D04-E03 & D04-E04: EXPLORATORY DATA ANALYSIS & KPI ENGINE")
    print("=" * 70)

    df = pd.read_csv(clean_csv)
    df['order_date'] = pd.to_datetime(df['order_date'])

    # -------------------------------------------------------------
    # 1. CORE EXECUTIVE KPIS
    # -------------------------------------------------------------
    total_revenue = df['revenue'].sum()
    total_cost = df['cost'].sum()
    total_gross_profit = df['profit'].sum()
    overall_margin_pct = (total_gross_profit / total_revenue) * 100
    total_orders = len(df)
    total_units_sold = df['quantity'].sum()
    avg_order_value = df['revenue'].mean()
    avg_discount_pct = df['discount_pct'].mean() * 100
    profitable_orders_pct = (df['is_profitable'].sum() / total_orders) * 100

    print(f"[*] Executive KPI Summary:")
    print(f"    - Gross Top-Line Revenue:    ${df['gross_revenue'].sum():,.2f}")
    print(f"    - Total Discounts Given:     ${df['discount_amount'].sum():,.2f}")
    print(f"    - Net Revenue:               ${total_revenue:,.2f}")
    print(f"    - Cost of Goods Sold (COGS): ${total_cost:,.2f}")
    print(f"    - Gross Profit:              ${total_gross_profit:,.2f}")
    print(f"    - Overall Gross Margin:      {overall_margin_pct:.2f}%")
    print(f"    - Total Transactions:        {total_orders:,}")
    print(f"    - Total Units Sold:          {total_units_sold:,}")
    print(f"    - Average Order Value (AOV): ${avg_order_value:.2f}")
    print(f"    - Average Discount Rate:     {avg_discount_pct:.2f}%")
    print(f"    - Profitable Orders Ratio:   {profitable_orders_pct:.2f}%")

    # -------------------------------------------------------------
    # 2. CATEGORY BREAKDOWN TABLE
    # -------------------------------------------------------------
    cat_summary = df.groupby('product_category').agg(
        orders=('order_id', 'count'),
        units_sold=('quantity', 'sum'),
        total_revenue=('revenue', 'sum'),
        total_cost=('cost', 'sum'),
        total_profit=('profit', 'sum'),
        avg_discount=('discount_pct', lambda x: x.mean() * 100),
        loss_making_orders=('is_profitable', lambda x: (~x).sum())
    ).reset_index()

    cat_summary['profit_margin_pct'] = (cat_summary['total_profit'] / cat_summary['total_revenue']) * 100
    cat_summary['cost_to_revenue_pct'] = (cat_summary['total_cost'] / cat_summary['total_revenue']) * 100
    cat_summary['revenue_share_pct'] = (cat_summary['total_revenue'] / total_revenue) * 100
    cat_summary['profit_share_pct'] = (cat_summary['total_profit'] / total_gross_profit) * 100
    cat_summary = cat_summary.sort_values('total_revenue', ascending=False).reset_index(drop=True)

    print("\n[*] Category Financial Performance Breakdown:")
    print(cat_summary[['product_category', 'total_revenue', 'total_profit', 'profit_margin_pct', 'revenue_share_pct', 'profit_share_pct']].to_string(index=False))

    # -------------------------------------------------------------
    # 3. FIGURE 1: Revenue, Cost & Profit by Category
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6.5))
    x = np.arange(len(cat_summary))
    width = 0.26

    rects1 = ax.bar(x - width, cat_summary['total_revenue'] / 1000, width, label='Net Revenue ($K)', color='#2b5c8f', edgecolor='black', alpha=0.9)
    rects2 = ax.bar(x, cat_summary['total_cost'] / 1000, width, label='Cost of Goods ($K)', color='#e06666', edgecolor='black', alpha=0.9)
    rects3 = ax.bar(x + width, cat_summary['total_profit'] / 1000, width, label='Gross Profit ($K)', color='#2e8540', edgecolor='black', alpha=0.9)

    ax.set_title('Comparative Financial Breakdown by Product Category (Revenue vs Cost vs Profit)', fontsize=14, weight='bold', pad=15)
    ax.set_xlabel('Product Category', fontsize=12, labelpad=10)
    ax.set_ylabel('Amount (Thousands USD $)', fontsize=12, labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_summary['product_category'], rotation=25, ha='right', fontsize=10)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Add margin annotations above profit bars
    for i, rect in enumerate(rects3):
        h = rect.get_height()
        margin = cat_summary.loc[i, 'profit_margin_pct']
        ax.annotate(f"{margin:.1f}%",
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, weight='bold', color='#1b4d24')

    plt.tight_layout()
    f1_path = os.path.join(fig_dir, '01_revenue_cost_profit_by_category.png')
    plt.savefig(f1_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 1: {f1_path}")

    # -------------------------------------------------------------
    # 4. FIGURE 2: Profit Margin Distribution by Category (Boxplot + Mean Markers)
    # -------------------------------------------------------------
    plt.figure(figsize=(12, 6))
    order_cat = df.groupby('product_category')['profit_margin_pct'].median().sort_values(ascending=False).index
    
    palette = sns.color_palette("mako", len(order_cat))
    ax = sns.boxplot(x='product_category', y='profit_margin_pct', data=df, order=order_cat, palette=palette, showmeans=True,
                     meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black", "markersize":"8"})
    
    plt.axhline(0, color='crimson', linestyle='--', linewidth=1.5, label='Break-Even Margin (0%)')
    plt.title('Profit Margin (%) Distribution Across Product Categories (Sorted by Median Margin)', fontsize=14, weight='bold', pad=15)
    plt.xlabel('Product Category', fontsize=12, labelpad=10)
    plt.ylabel('Profit Margin (%)', fontsize=12, labelpad=10)
    plt.xticks(rotation=25, ha='right', fontsize=10)
    plt.legend(loc='lower left', frameon=True)
    plt.tight_layout()
    f2_path = os.path.join(fig_dir, '02_profit_margin_distribution.png')
    plt.savefig(f2_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 2: {f2_path}")

    # -------------------------------------------------------------
    # 5. FIGURE 3: Discount vs Profit Margin (The Margin Erosion Trap)
    # -------------------------------------------------------------
    plt.figure(figsize=(12, 6.5))
    sample_df = df.sample(min(2500, len(df)), random_state=42)
    
    sns.scatterplot(
        x=sample_df['discount_pct'] * 100,
        y=sample_df['profit_margin_pct'],
        hue=sample_df['product_category'],
        alpha=0.6,
        s=35,
        palette='tab10'
    )
    
    # Regression line
    sns.regplot(
        x=df['discount_pct'] * 100,
        y=df['profit_margin_pct'],
        scatter=False,
        color='black',
        line_kws={'linestyle': '--', 'linewidth': 2, 'label': 'Linear Margin Decay Trendline'}
    )
    
    plt.axhline(0, color='red', linestyle='-', linewidth=1.5, label='Break-Even Threshold (0% Profit)')
    plt.title('The Discount Trap: Impact of Promotional Discount Rate on Profit Margin %', fontsize=14, weight='bold', pad=15)
    plt.xlabel('Promotional Discount Rate (%)', fontsize=12, labelpad=10)
    plt.ylabel('Profit Margin (%)', fontsize=12, labelpad=10)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=9)
    plt.tight_layout()
    f3_path = os.path.join(fig_dir, '03_discount_vs_profit_margin_scatter.png')
    plt.savefig(f3_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 3: {f3_path}")

    # -------------------------------------------------------------
    # 6. FIGURE 4: Monthly Financial Trends (Revenue, Profit, Margin %)
    # -------------------------------------------------------------
    monthly = df.groupby('order_month').agg(
        revenue=('revenue', 'sum'),
        cost=('cost', 'sum'),
        profit=('profit', 'sum')
    ).reset_index()
    monthly['margin_pct'] = (monthly['profit'] / monthly['revenue']) * 100

    fig, ax1 = plt.subplots(figsize=(14, 6))

    color1 = '#1f77b4'
    color2 = '#2ca02c'
    color3 = '#d62728'

    ax1.set_xlabel('Timeline (Month)', fontsize=12, labelpad=10)
    ax1.set_ylabel('Monthly Revenue & Profit ($)', color=color1, fontsize=12)
    p1 = ax1.plot(monthly['order_month'], monthly['revenue'], marker='o', linewidth=2.5, color=color1, label='Net Revenue ($)')
    p2 = ax1.plot(monthly['order_month'], monthly['profit'], marker='s', linewidth=2.5, color=color2, label='Gross Profit ($)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xticklabels(monthly['order_month'], rotation=45, ha='right', fontsize=9)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Profit Margin (%)', color=color3, fontsize=12)
    p3 = ax2.plot(monthly['order_month'], monthly['margin_pct'], marker='^', linewidth=2, linestyle=':', color=color3, label='Profit Margin (%)')
    ax2.tick_params(axis='y', labelcolor=color3)
    ax2.grid(False)

    lines = p1 + p2 + p3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, framealpha=0.9)

    plt.title('Monthly Sales Trajectory & Margin Stability (2023 - 2024)', fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    f4_path = os.path.join(fig_dir, '04_monthly_financial_trends.png')
    plt.savefig(f4_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 4: {f4_path}")

    # -------------------------------------------------------------
    # 7. FIGURE 5: Regional Category Profitability Heatmap
    # -------------------------------------------------------------
    region_cat = df.pivot_table(index='product_category', columns='region', values='profit_margin_pct', aggfunc='mean')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(region_cat, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Mean Profit Margin (%)'}, linewidths=.5)
    plt.title('Geographic Cross-Tabulation: Mean Profit Margin (%) by Category & Region', fontsize=13, weight='bold', pad=15)
    plt.xlabel('Territory / Region', fontsize=11, labelpad=10)
    plt.ylabel('Product Category', fontsize=11, labelpad=10)
    plt.tight_layout()
    f5_path = os.path.join(fig_dir, '05_regional_category_profitability_heatmap.png')
    plt.savefig(f5_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 5: {f5_path}")

    # -------------------------------------------------------------
    # 8. FIGURE 6: Strategic Category Portfolio Matrix (BCG / Profitability Matrix)
    # -------------------------------------------------------------
    plt.figure(figsize=(11, 7))
    
    # Bubble plot: X = Net Revenue, Y = Profit Margin %, Size = Order Volume
    sizes = (cat_summary['orders'] / cat_summary['orders'].max()) * 1800 + 300
    scatter = plt.scatter(
        cat_summary['total_revenue'] / 1000,
        cat_summary['profit_margin_pct'],
        s=sizes,
        c=cat_summary['profit_margin_pct'],
        cmap='viridis',
        edgecolors='black',
        alpha=0.85,
        linewidths=1.5
    )

    # Median benchmark lines
    rev_mid = (cat_summary['total_revenue'] / 1000).median()
    margin_mid = cat_summary['profit_margin_pct'].median()

    plt.axvline(rev_mid, color='grey', linestyle='--', alpha=0.7)
    plt.axhline(margin_mid, color='grey', linestyle='--', alpha=0.7)

    # Quadrant Labels
    plt.text(cat_summary['total_revenue'].max()/1000 * 0.92, cat_summary['profit_margin_pct'].max() * 0.95,
             '★ STARS\n(High Revenue, High Margin)', fontsize=10, weight='bold', color='#1e5631', ha='right')
    plt.text(cat_summary['total_revenue'].max()/1000 * 0.92, cat_summary['profit_margin_pct'].min() * 1.1,
             '⚡ VOLUME DRIVERS\n(High Revenue, Low Margin)', fontsize=10, weight='bold', color='#990000', ha='right')
    plt.text(cat_summary['total_revenue'].min()/1000 * 1.05, cat_summary['profit_margin_pct'].max() * 0.95,
             '◆ NICHE HARVESTERS\n(Low Revenue, High Margin)', fontsize=10, weight='bold', color='#2b5c8f', ha='left')
    plt.text(cat_summary['total_revenue'].min()/1000 * 1.05, cat_summary['profit_margin_pct'].min() * 1.1,
             '▲ MARGIN BLEEDERS\n(Low Revenue, Low Margin)', fontsize=10, weight='bold', color='#555555', ha='left')

    # Category name labels
    for _, row in cat_summary.iterrows():
        plt.annotate(
            row['product_category'],
            xy=(row['total_revenue'] / 1000, row['profit_margin_pct']),
            xytext=(0, 10), textcoords="offset points",
            ha='center', fontsize=10, weight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", alpha=0.7, lw=0.5)
        )

    plt.title('Strategic Category Portfolio Matrix: Revenue vs Profit Margin % (Bubble Size = Order Volume)', fontsize=13, weight='bold', pad=15)
    plt.xlabel('Total Net Revenue ($ Thousands)', fontsize=12, labelpad=10)
    plt.ylabel('Gross Profit Margin (%)', fontsize=12, labelpad=10)
    plt.colorbar(scatter, label='Gross Profit Margin (%)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    f6_path = os.path.join(fig_dir, '06_bcg_profitability_matrix.png')
    plt.savefig(f6_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 6: {f6_path}")

    # -------------------------------------------------------------
    # 9. FIGURE 7: Payment Mode Performance
    # -------------------------------------------------------------
    pay_summary = df.groupby('payment_mode').agg(
        revenue=('revenue', 'sum'),
        orders=('order_id', 'count'),
        aov=('revenue', 'mean'),
        margin=('profit_margin_pct', 'mean')
    ).reset_index().sort_values('revenue', ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 5))
    bars = ax1.bar(pay_summary['payment_mode'], pay_summary['revenue'] / 1000, color='#386cb0', width=0.5, label='Total Net Revenue ($K)')
    ax1.set_ylabel('Revenue ($K)', color='#386cb0', fontsize=11)
    ax1.set_xticklabels(pay_summary['payment_mode'], rotation=15, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(pay_summary['payment_mode'], pay_summary['aov'], color='#f0027f', marker='o', linewidth=2.5, label='Average Order Value ($)')
    ax2.set_ylabel('Average Order Value ($)', color='#f0027f', fontsize=11)
    ax2.grid(False)

    plt.title('Payment Mode Contribution to Net Sales & Average Order Value (AOV)', fontsize=13, weight='bold', pad=15)
    fig.tight_layout()
    f7_path = os.path.join(fig_dir, '07_payment_mode_analysis.png')
    plt.savefig(f7_path, dpi=300)
    plt.close()
    print(f"[✓] Generated Figure 7: {f7_path}")

    print("=" * 70)
    print("EPIC D04-E03 & D04-E04 ANALYSIS COMPLETE. All figures rendered.")
    print("=" * 70)

if __name__ == '__main__':
    perform_eda_and_kpis()

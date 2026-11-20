"""
=============================================================================
Product Category Profitability Study
Application: Streamlit Interactive Executive Dashboard
Epic: D04-E05 - Dashboard and Visualization
Author: Student Research Team
Description: Modern, responsive multi-tab analytics dashboard equipped with
             interactive Plotly charts, dynamic dimension filtering,
             KPI cards, and discount sensitivity simulator.
=============================================================================
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------
# Page Configuration & Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="Product Category Profitability Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.45rem !important;
        font-weight: 700;
        white-space: nowrap;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600;
        color: #64748B;
    }
    .badge-star { color: #15803d; font-weight: bold; }
    .badge-bleed { color: #b91c1c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Data Loading & Caching
# -------------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_product_sales.csv')
    df = pd.read_csv(file_path)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}. Please ensure scripts/clean_data.py has been executed.")
    st.stop()

# -------------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Navigation & Filters")
st.sidebar.markdown("Filter sales ledger dimensions:")

# Date Range Filter
min_date = df_raw['order_date'].min().date()
max_date = df_raw['order_date'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Category Filter
all_categories = sorted(df_raw['product_category'].unique())
selected_categories = st.sidebar.multiselect("Product Categories", all_categories, default=all_categories)

# Region Filter
all_regions = sorted(df_raw['region'].unique())
selected_regions = st.sidebar.multiselect("Geographic Regions", all_regions, default=all_regions)

# Payment Mode Filter
all_payments = sorted(df_raw['payment_mode'].unique())
selected_payments = st.sidebar.multiselect("Payment Channels", all_payments, default=all_payments)

# Apply Filter Mask
if len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

df = df_raw[
    (df_raw['order_date'].dt.date >= start_d) &
    (df_raw['order_date'].dt.date <= end_d) &
    (df_raw['product_category'].isin(selected_categories)) &
    (df_raw['region'].isin(selected_regions)) &
    (df_raw['payment_mode'].isin(selected_payments))
].copy()

# -------------------------------------------------------------
# Main Header
# -------------------------------------------------------------
st.markdown('<div class="main-header">📈 Product Category Profitability Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Strategic BI study examining top-line revenue vs bottom-line gross margins across retail merchandise lines (Course Project D04)</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# Executive KPI Metrics Row
# -------------------------------------------------------------
tot_revenue = df['revenue'].sum()
tot_cost = df['cost'].sum()
tot_profit = df['profit'].sum()
tot_margin = (tot_profit / tot_revenue * 100) if tot_revenue > 0 else 0
avg_order_val = df['revenue'].mean() if len(df) > 0 else 0
profit_order_rate = (df['is_profitable'].sum() / len(df) * 100) if len(df) > 0 else 0

kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5, kpi_c6 = st.columns(6)
kpi_c1.metric("Net Revenue", f"${tot_revenue:,.0f}", delta=f"{len(df):,} Orders")
kpi_c2.metric("Total COGS", f"${tot_cost:,.0f}", delta_color="inverse")
kpi_c3.metric("Gross Profit", f"${tot_profit:,.0f}", delta=f"${tot_profit/len(df):.1f}/order" if len(df) else None)
kpi_c4.metric("Gross Margin", f"{tot_margin:.2f}%", delta="Benchmark: 15%")
kpi_c5.metric("Avg Order Value", f"${avg_order_val:.2f}")
kpi_c6.metric("Profitable Orders", f"{profit_order_rate:.1f}%")

st.markdown("---")

# -------------------------------------------------------------
# Tabbed Analytical Layout
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Category Financials",
    "🎯 Portfolio BCG Matrix",
    "⚠️ Discount Sensitivity",
    "🌍 Geographic & Tender Analysis",
    "📋 Data Explorer"
])

# -------------------------------------------------------------
# TAB 1: Category Financial Breakdown
# -------------------------------------------------------------
with tab1:
    col_t1a, col_t1b = st.columns([1.2, 0.8])
    
    with col_t1a:
        st.subheader("Revenue vs Cost vs Profit by Category")
        cat_agg = df.groupby('product_category').agg(
            Revenue=('revenue', 'sum'),
            Cost=('cost', 'sum'),
            Profit=('profit', 'sum')
        ).reset_index().sort_values('Revenue', ascending=False)
        
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(name='Net Revenue', x=cat_agg['product_category'], y=cat_agg['Revenue'], marker_color='#2563EB'))
        fig_cat.add_trace(go.Bar(name='Cost of Goods', x=cat_agg['product_category'], y=cat_agg['Cost'], marker_color='#EF4444'))
        fig_cat.add_trace(go.Bar(name='Gross Profit', x=cat_agg['product_category'], y=cat_agg['Profit'], marker_color='#10B981'))
        fig_cat.update_layout(barmode='group', template='plotly_white', height=420, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col_t1b:
        st.subheader("Category Profit Share (%)")
        # Treemap or Donut
        fig_donut = px.pie(
            cat_agg,
            names='product_category',
            values='Profit',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_donut.update_layout(height=420, template='plotly_white')
        st.plotly_chart(fig_donut, use_container_width=True)

    # Monthly Trendline
    st.subheader("Monthly Revenue & Gross Margin (%) Trajectory")
    monthly_trend = df.groupby('order_month').agg(
        Revenue=('revenue', 'sum'),
        Profit=('profit', 'sum')
    ).reset_index()
    monthly_trend['Margin_Pct'] = (monthly_trend['Profit'] / monthly_trend['Revenue']) * 100

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=monthly_trend['order_month'], y=monthly_trend['Revenue'], name='Net Revenue ($)', mode='lines+markers', line=dict(color='#2563EB', width=2.5)))
    fig_trend.add_trace(go.Scatter(x=monthly_trend['order_month'], y=monthly_trend['Profit'], name='Gross Profit ($)', mode='lines+markers', line=dict(color='#10B981', width=2.5)))
    fig_trend.add_trace(go.Scatter(x=monthly_trend['order_month'], y=monthly_trend['Margin_Pct'], name='Margin %', yaxis='y2', mode='lines+markers', line=dict(color='#F59E0B', width=2, dash='dot')))
    
    fig_trend.update_layout(
        template='plotly_white',
        height=380,
        yaxis=dict(title='Dollar Amount ($)'),
        yaxis2=dict(title='Margin (%)', overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: Strategic Portfolio Matrix (BCG Matrix)
# -------------------------------------------------------------
with tab2:
    st.subheader("Category Strategic Positioning Matrix (Revenue vs Margin %)")
    st.markdown("""
    This matrix categorizes retail product lines by commercial scale (Net Revenue) vs bottom-line yield (Gross Margin %).
    * **Stars:** High Revenue, High Margin (Growth Engines)
    * **Volume Drivers:** High Revenue, Low Margin (Cash Flow / Basket Fillers)
    * **Niche Harvesters:** Low Revenue, High Margin (Expansion Opportunities)
    * **Margin Bleeders:** Low Revenue, Compressed Margin (Restructure or Prune)
    """)
    
    cat_mat = df.groupby('product_category').agg(
        Revenue=('revenue', 'sum'),
        Profit=('profit', 'sum'),
        Orders=('order_id', 'count')
    ).reset_index()
    cat_mat['Margin_Pct'] = (cat_mat['Profit'] / cat_mat['Revenue']) * 100

    fig_mat = px.scatter(
        cat_mat,
        x='Revenue',
        y='Margin_Pct',
        size='Orders',
        color='product_category',
        text='product_category',
        labels={'Revenue': 'Total Net Revenue ($)', 'Margin_Pct': 'Gross Profit Margin (%)'},
        template='plotly_white',
        height=520
    )
    fig_mat.update_traces(textposition='top center', marker=dict(opacity=0.85, line=dict(width=1.5, color='DarkSlateGrey')))
    
    # Add benchmark reference lines
    rev_median = cat_mat['Revenue'].median()
    margin_median = cat_mat['Margin_Pct'].median()
    fig_mat.add_vline(x=rev_median, line_dash="dash", line_color="gray", annotation_text="Median Revenue", annotation_position="top left")
    fig_mat.add_hline(y=margin_median, line_dash="dash", line_color="gray", annotation_text="Median Margin", annotation_position="bottom right")

    st.plotly_chart(fig_mat, use_container_width=True)

# -------------------------------------------------------------
# TAB 3: Discount Sensitivity & Profit Erosion
# -------------------------------------------------------------
with tab3:
    st.subheader("Promotional Discount Rate vs Profit Margin Decay")
    
    col_t3a, col_t3b = st.columns([1, 1])
    
    with col_t3a:
        sample_size = min(1500, len(df))
        if sample_size > 0:
            sample_df = df.sample(sample_size, random_state=42).copy()
            sample_df['discount_rate_pct'] = (sample_df['discount_pct'] * 100).round(2)
            
            fig_scatter = px.scatter(
                sample_df,
                x='discount_rate_pct',
                y='profit_margin_pct',
                color='product_category',
                opacity=0.65,
                trendline="ols",
                labels={'discount_rate_pct': 'Promotional Discount Applied (%)', 'profit_margin_pct': 'Profit Margin (%)'},
                title="Margin Decay Correlation (Sampled Transactions)",
                template='plotly_white',
                height=420
            )
            fig_scatter.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-Even (0%)", annotation_position="bottom right")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No data available for selected filter combination.")

    with col_t3b:
        st.markdown("#### 🎛️ Interactive Discount Simulation")
        st.write("Simulate the impact of applying a universal discount cap on high-volume categories:")
        sim_category = st.selectbox("Select Target Category", all_categories, index=0)
        sim_max_discount = st.slider("Simulated Maximum Allowed Discount (%)", 0, 40, 15)
        
        # Calculate simulation impact
        cat_subset = df[df['product_category'] == sim_category].copy()
        current_profit = cat_subset['profit'].sum()
        
        # Simulated revenue and profit
        sim_discount = cat_subset['discount_pct'].clip(upper=sim_max_discount / 100.0)
        sim_net_rev = cat_subset['gross_revenue'] * (1 - sim_discount)
        sim_profit = sim_net_rev - cat_subset['cost']
        new_profit = sim_profit.sum()
        profit_delta = new_profit - current_profit
        
        st.metric(f"Projected Profit Impact ({sim_category})", f"${new_profit:,.2f}", delta=f"{'+' if profit_delta >= 0 else ''}${profit_delta:,.2f}")
        st.info(f"Setting a hard promotional ceiling of {sim_max_discount}% on {sim_category} prevents underwater margin erosion during peak promotional cycles.")

# -------------------------------------------------------------
# TAB 4: Geographic & Tender Mode Economics
# -------------------------------------------------------------
with tab4:
    col_t4a, col_t4b = st.columns(2)
    
    with col_t4a:
        st.subheader("Regional Profit Margin Heatmap")
        pivot_geo = df.pivot_table(index='product_category', columns='region', values='profit_margin_pct', aggfunc='mean')
        fig_heat = px.imshow(
            pivot_geo,
            text_auto=".1f",
            color_continuous_scale="Viridis",
            labels=dict(x="Territory", y="Category", color="Avg Margin %"),
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_t4b:
        st.subheader("Tender Mode Distribution & AOV")
        pay_df = df.groupby('payment_mode').agg(
            Revenue=('revenue', 'sum'),
            AOV=('revenue', 'mean'),
            Margin=('profit_margin_pct', 'mean')
        ).reset_index().sort_values('Revenue', ascending=False)
        
        fig_pay = px.bar(
            pay_df,
            x='payment_mode',
            y='Revenue',
            color='Margin',
            text_auto='.2s',
            labels={'payment_mode': 'Payment Channel', 'Revenue': 'Net Revenue ($)'},
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig_pay, use_container_width=True)

# -------------------------------------------------------------
# TAB 5: Data Ledger Explorer
# -------------------------------------------------------------
with tab5:
    st.subheader("Transaction Ledger (Cleaned & Analysis-Ready)")
    st.write(f"Displaying {len(df):,} filtered transaction rows:")
    st.dataframe(df.head(200), use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_category_profitability.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.caption("College Capstone Project D04 — Product Category Profitability Study | Built with Python, Pandas, Streamlit, and Plotly.")

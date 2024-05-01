import streamlit as st
from connection import get_data

# Load data
data = get_data()

st.title('Table of Content')

cols = st.columns(12)  # Expand to 12 columns to accommodate the new filters

# Textual filters
with cols[0]:
    panel_type_filter = st.selectbox("Panel Type", options=[None] + list(data['PNL_TYP'].unique()), index=0)
with cols[1]:
    metric_type_filter = st.multiselect("Metric Type", options=list(data['MTRC_TYP'].unique()), default=None)

with cols[2]:
    sector_filter = st.selectbox("Sector", options=[None] + list(data['SCTR_NM'].unique()), index=0)
with cols[3]:
    sub_sector_filter = st.selectbox("Sub Sector", options=[None] + list(data['SUBSCTR_NM'].unique()), index=0)
with cols[4]:
    industry_filter = st.selectbox("Industry", options=[None] + list(data['INDSTRY_NM'].unique()), index=0)
with cols[5]:
    sub_industry_filter = st.selectbox("Sub-Industry", options=[None] + list(data['SUBINDSTRY_NM'].unique()), index=0)
with cols[6]:
    segment_type_filter = st.selectbox("Parent/Segment", options=[None] + list(data['SEG_TYP'].unique()), index=0)
with cols[7]:
    ownership_type_filter = st.selectbox("Ownership", options=[None] + list(data['OWNSHP_TYP'].unique()), index=0)

# Numerical filters
with cols[8]:
    if 'MARKETCAP' in data.columns:
        col1, col2 = st.columns(2)

        # Input for minimum market cap in the first column
        with col1:
            min_cap = st.number_input("Minimum Market Cap",
                                      min_value=int(data['MARKETCAP'].min()),
                                      value=int(data['MARKETCAP'].min()))

        # Input for maximum market cap in the second column
        with col2:
            max_cap = st.number_input("Maximum Market Cap",
                                      min_value=int(data['MARKETCAP'].min()),
                                      max_value=int(data['MARKETCAP'].max()),
                                      value=int(data['MARKETCAP'].max()))
with cols[9]:
    if 'QTD_PROGRESS' in data.columns:
        min_days, max_days = st.slider("Days Through Quarter", int(data['QTD_PROGRESS'].min()), int(data['QTD_PROGRESS'].max()), (int(data['QTD_PROGRESS'].min()), int(data['QTD_PROGRESS'].max())))
with cols[10]:
    if 'MTD_SPEND' in data.columns:
        min_spend, max_spend = st.slider("Min. Monthly Spend", int(data['MTD_SPEND'].min()), int(data['MTD_SPEND'].max()), (int(data['MTD_SPEND'].min()), int(data['MTD_SPEND'].max())))
with cols[11]:
    if 'CORRELATION' in data.columns:
        min_corr, max_corr = st.slider("Correlation", float(data['CORRELATION'].min()), float(data['CORRELATION'].max()), (float(data['CORRELATION'].min()), float(data['CORRELATION'].max())))

# Apply filters dynamically based on selection
filtered_data = data
if panel_type_filter:
    filtered_data = filtered_data[filtered_data['PNL_TYP'] == panel_type_filter]
if metric_type_filter:
    filtered_data = filtered_data[filtered_data['MTRC_TYP'].isin(metric_type_filter)]
if sector_filter:
    filtered_data = filtered_data[filtered_data['SCTR_NM'] == sector_filter]
if sub_sector_filter:
    filtered_data = filtered_data[filtered_data['SUBSCTR_NM'] == sub_sector_filter]
if industry_filter:
    filtered_data = filtered_data[filtered_data['INDSTRY_NM'] == industry_filter]
if sub_industry_filter:
    filtered_data = filtered_data[filtered_data['SUBINDSTRY_NM'] == sub_industry_filter]
if segment_type_filter:
    filtered_data = filtered_data[filtered_data['SEG_TYP'] == segment_type_filter]
if ownership_type_filter:
    filtered_data = filtered_data[filtered_data['OWNSHP_TYP'] == ownership_type_filter]
# Applying numerical filters
if 'MARKETCAP' in data.columns:
    filtered_data = filtered_data[filtered_data['MARKETCAP'].between(min_cap, max_cap)]
if 'QTD_PROGRESS' in data.columns:
    filtered_data = filtered_data[filtered_data['QTD_PROGRESS'].between(min_days, max_days)]
if 'MTD_SPEND' in data.columns:
    filtered_data = filtered_data[filtered_data['MTD_SPEND'].between(min_spend, max_spend)]
if 'CORRELATION' in data.columns:
    filtered_data = filtered_data[filtered_data['CORRELATION'].between(min_corr, max_corr)]


# Display the DataFrame on the page (filtered based on user input)
if not filtered_data.empty:
    # Exclude 'PNL_TYP' from display and apply heatmap to 'MTD_SPEND' column
    display_columns = [col for col in filtered_data.columns if col != 'PNL_TYP']
    display_data = filtered_data[display_columns].style.background_gradient(subset=['MARKETCAP'], cmap='coolwarm')
    st.write(display_data)  # Use st.write to render pandas Styler objects
else:
    st.write("No data matches your filters.")
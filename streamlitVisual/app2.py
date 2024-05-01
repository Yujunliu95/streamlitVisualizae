import streamlit as st
from connection import get_data


class DataApp:
    def __init__(self):
        self.data = get_data()
        self.initialize_filters()

    def initialize_filters(self):
        self.filters = {
            'panel_type': None,
            'metric_type': None,
            'sector': None,
            'sub_sector': None,
            'industry': None,
            'sub_industry': None,
            'segment_type': None,
            'ownership_type': None,
            'market_cap': None,
            'days_through_quarter': None,
            'min_monthly_spend': None,
            'correlation': None
        }

    def set_filters(self):
        cols = st.columns(12)
        with cols[0]:
            self.filters['panel_type'] = st.selectbox("Panel Type", options=[None] + list(self.data['PNL_TYP'].unique()), index=0)
        with cols[1]:
            self.filters['metric_type'] = st.selectbox("Metric Type", options=[None] + list(self.data['MTRC_TYP'].unique()), index=0)
        with cols[2]:
            self.filters['sector'] = st.selectbox("Sector", options=[None] + list(self.data['SCTR_NM'].unique()), index=0)
        with cols[3]:
            self.filters['sub_sector'] = st.selectbox("Sub Sector", options=[None] + list(self.data['SUBSCTR_NM'].unique()), index=0)
        with cols[4]:
            self.filters['industry'] = st.selectbox("Industry", options=[None] + list(self.data['INDSTRY_NM'].unique()), index=0)
        with cols[5]:
            self.filters['sub_industry'] = st.selectbox("Sub-Industry", options=[None] + list(self.data['SUBINDSTRY_NM'].unique()), index=0)
        with cols[6]:
            self.filters['segment_type'] = st.selectbox("Parent/Segment", options=[None] + list(self.data['SEG_TYP'].unique()), index=0)
        with cols[7]:
            self.filters['ownership_type'] = st.selectbox("Ownership", options=[None] + list(self.data['OWNSHP_TYP'].unique()), index=0)
        # Numerical filters
        with cols[8]:
            if 'MARKETCAP' in self.data.columns:
                self.filters['market_cap'] = st.slider("Market Cap", int(self.data['MARKETCAP'].min()), int(self.data['MARKETCAP'].max()), (int(self.data['MARKETCAP'].min()), int(self.data['MARKETCAP'].max())))
        with cols[9]:
            if 'QTD_PROGRESS' in self.data.columns:
                self.filters['days_through_quarter'] = st.slider("Days Through Quarter", int(self.data['QTD_PROGRESS'].min()), int(self.data['QTD_PROGRESS'].max()), (int(self.data['QTD_PROGRESS'].min()), int(self.data['QTD_PROGRESS'].max())))
        with cols[10]:
            if 'MTD_SPEND' in self.data.columns:
                self.filters['min_monthly_spend'] = st.slider("Min. Monthly Spend", int(self.data['MTD_SPEND'].min()), int(self.data['MTD_SPEND'].max()), (int(self.data['MTD_SPEND'].min()), int(self.data['MTD_SPEND'].max())))
        with cols[11]:
            if 'CORRELATION' in self.data.columns:
                self.filters['correlation'] = st.slider("Correlation", float(self.data['CORRELATION'].min()), float(self.data['CORRELATION'].max()), (float(self.data['CORRELATION'].min()), float(self.data['CORRELATION'].max())))

    def apply_filters(self):
        filtered_data = self.data
        for key, value in self.filters.items():
            if value and key in self.data.columns:
                if isinstance(value, tuple):  # For numerical range filters
                    filtered_data = filtered_data[filtered_data[key].between(value[0], value[1])]
                else:
                    filtered_data = filtered_data[filtered_data[key] == value]
        return filtered_data

    def run(self):
        st.title('Table of Content')
        self.set_filters()
        filtered_data = self.apply_filters()
        if not filtered_data.empty:
            st.dataframe(filtered_data, height=500)
        else:
            st.write("No data matches your filters.")

if __name__ == "__main__":
    app = DataApp()
    app.run()

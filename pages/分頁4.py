
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth # Import for consistency, though login might be handled in main.py

# --- Page Configuration ---
# Setting the page title for this specific page
st.set_page_config(page_title="BI Dashboard Demo", layout="wide")

# --- BI Functionality Demonstration ---
def bi_dashboard_page():
    st.title("BI Dashboard - Sample Data Demo")
    st.write("This page demonstrates basic BI features like KPIs and interactive charts using sample data.")

    # Sample Data using Pandas
    data = {
        'Category': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'],
        'Metric1': [10, 15, 12, 18, 16, 20, 11, 14, 19, 13, 17, 22],
        'Metric2': [5, 8, 6, 9, 7, 10, 5, 8, 9, 6, 8, 11],
        'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South', 'East', 'West']
    }
    df = pd.DataFrame(data)

    st.write("### Sample Data Preview")
    st.dataframe(df.head())

    st.write("---")

    # --- Key Performance Indicators (KPIs) ---
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_metric1 = df['Metric1'].sum()
        st.metric("Total Metric 1", f"{total_metric1}")

    with col2:
        avg_metric2 = df['Metric2'].mean()
        st.metric("Average Metric 2", f"{avg_value2:.2f}")

    with col3:
        unique_regions = df['Region'].nunique()
        st.metric("Number of Regions", f"{unique_regions}")

    st.write("---")

    # --- Interactive Charts using Plotly Express ---
    st.subheader("Interactive Charts")

    # Bar chart: Metric1 by Category
    st.write("#### Metric 1 by Category")
    fig_bar = px.bar(df, x='Category', y='Metric1', color='Category', 
                     title="Metric 1 Distribution by Category",
                     labels={'Metric1': 'Value of Metric 1', 'Category': 'Category'},
                     barmode='group') # Using group mode for better comparison if needed
    st.plotly_chart(fig_bar, use_container_width=True)

    st.write("---")

    # Scatter plot: Metric1 vs Metric2, colored by Region
    st.write("#### Metric 1 vs Metric 2 Scatter Plot")
    fig_scatter = px.scatter(df, x='Metric1', y='Metric2', color='Region', 
                             title="Relationship between Metric1 and Metric2",
                             labels={'Metric1': 'Metric 1 Value', 'Metric2': 'Metric 2 Value'},
                             hover_name='Category') # Hover over points to see category
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.write("---")
    st.write("This is a basic demonstration. For a full BI experience, you would integrate real data sources, implement more advanced analysis, and refine the UI.")

# To make this page runnable by Streamlit's multi-page feature, 
# we just need to define the function. Streamlit will discover and call it.
# The main app's authentication would typically handle the initial login.
# If you want this page to be selectable from the sidebar in main.py,
# you'll need to add '分頁4' (or its intended name) to the options in main.py's option_menu.

# This block is for standalone testing if needed, but Streamlit's runner handles page calls.
if __name__ == "__main__":
    # For demonstration, we'll assume a basic session state is available
    # In a real app, Streamlit manages session state automatically.
    # We might need to mock st.session_state for direct script execution testing if authentication is involved.
    
    # To ensure compatibility with existing pages, we'll mimic a basic structure.
    # The user name is assumed to be from config.yaml
    st.session_state["authentication_status"] = True # Assume logged in for demo
    st.session_state["name"] = "Anio Wang" # From config.yaml

    bi_dashboard_page()

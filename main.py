import pickle
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import yaml # Added import for yaml

# --- Authentication ---
# Load authentication configuration
try:
    # ****** MODIFICATION START ******
    # Try reading config.yaml with cp950 encoding as suggested by previous errors
    # Also changed pickle.load to yaml.safe_load as config.yaml is likely YAML
    with open("./config.yaml", "r", encoding="cp950") as file: 
        config = yaml.safe_load(file) 
except FileNotFoundError:
    st.error("Config file not found. Please ensure config.yaml exists.")
    st.stop()
except Exception as e: # Catches UnicodeDecodeError and other potential errors
    st.error(f"Error loading config file: {e}")
    st.stop()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# --- Navigation ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Home", "Dashboard", "Analytics", "Settings", "分頁4"],  # ****** MODIFICATION START ****** Add '分頁4'
        icons=["house", "graph-up", "bar-chart-line", "gear", "file-earmark-bar-graph"],  # Optional: Add an icon for the new page
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )

# --- Page Content ---
if selected == "Home":
    st.title("Welcome to the BI Dashboard!")
    st.write("This is the home page. Please select an option from the sidebar to continue.")
    # Display login status
    if st.session_state["authentication_status"]:
        st.write(f"Hello, {st.session_state['name']}!")
    else:
        authenticator.login()

elif selected == "Dashboard":
    st.title("Dashboard")
    st.write("This is the dashboard page.")
    # Placeholder for dashboard content

elif selected == "Analytics":
    st.title("Analytics")
    st.write("This is the analytics page.")
    # Placeholder for analytics content

elif selected == "Settings":
    st.title("Settings")
    st.write("This is the settings page.")
    # Placeholder for settings content

# ****** MODIFICATION START ****** Add handling for the new page
elif selected == "分頁4":
    # Dynamically import the page function. It's better practice to import at the top
    # but for demonstration within a single code block, this is acceptable.
    # For a real app, ensure 'pages/分頁4.py' is structured correctly with a page function.
    # Assuming the function is named 'bi_dashboard_page' in 'pages.分頁4'
    try:
        from pages.分頁4 import bi_dashboard_page
        bi_dashboard_page()
    except ImportError:
        st.error("Could not import 'bi_dashboard_page' from 'pages.分頁4'. Please check the file and function name.")
    except Exception as e:
        st.error(f"An error occurred while loading page 4: {e}")
# ****** MODIFICATION END ******

# --- Footer ---
st.markdown("---")
st.markdown("© 2024 BI Dashboard. All rights reserved.")

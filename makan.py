import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pandas as pd
import os
from selenium.webdriver.chrome.service import Service

# Web driver setup function
def web_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"  # Updated path
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1200")
    return webdriver.Chrome(options=options)

# Function to generate weekday dates
def generate_weekdays(start_date, end_date):
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    return dates.strftime('%m/%d/%Y').tolist()

# Custom CSS styling that adapts to both light and dark themes
st.markdown("""
    <style>
    /* General Font */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: var(--secondary-background-color) !important;
    }
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: var(--primary-background-color) !important;
    }
    
    /* Input fields */
    [data-testid="stTextInput"], [data-testid="stDateInput"] input {
        background: var(--secondary-background-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Text input focus state */
    [data-testid="stTextInput"]:focus-within,
    [data-testid="stDateInput"]:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 2px rgba(13, 110, 253, 0.25) !important;
    }
    
    /* Button styling */
    [data-testid="stButton"] button {
        background: var(--blue) !important;
        color: var(--primary-text-color) !important; /* Ensure text color is adaptable */
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stButton"] button:hover {
        background: var(--blue-dark) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(13, 110, 253, 0.25);
    }
    
    /* Container styling */
    [data-testid="stHorizontalBlock"] {
        background: var(--primary-background-color);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    /* Headers */
    h1 {
        color: var(--text-color) !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    h2, h3 {
        color: var(--text-color-muted) !important;
        font-weight: 600 !important;
    }
    
    /* Success/Error messages */
    [data-testid="stNotification"] {
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Progress bar */
    [data-testid="stProgress"] > div > div {
        background-color: var(--blue) !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0 !important;
        border-color: var(--border-color) !important;
    }
    
    /* Center Title and Description */
    .center-text {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Improved UI Layout with centered title and description
st.markdown('<h1 class="center-text">Automated Meal Form</h1>', unsafe_allow_html=True)
st.markdown('<p class="center-text">🍴 Automatically fill your daily meal forms!</p>', unsafe_allow_html=True)

# First section: Google Form URL
with st.container():
    st.subheader("🔗 Google Form URL")
    form_url = st.text_input("Enter the Google Form URL")

# Second section: Date Range
with st.container():
    st.subheader("📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

# Third section: Employee Information
with st.container():
    st.subheader("👤 Employee Information")
    emp_col1, emp_col2 = st.columns(2)
    with emp_col1:
        employee_id = st.text_input("Employee ID")
    with emp_col2:
        full_name = st.text_input("Full Name")

st.divider()

if start_date and end_date:
    weekdays = generate_weekdays(str(start_date), str(end_date))
    if len(weekdays) == 0:
        st.warning("No working days found in the selected date range!")

if st.button('🚀 Submit Forms'):
    if not employee_id or not full_name or not form_url:
        st.error("Please fill in all required fields!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0
        error_count = 0
        
        try:
            driver = web_driver()
            
            total_days = len(weekdays)
            for index, date in enumerate(weekdays):
                try:
                    # Update progress without success messages
                    progress = (index + 1) / total_days
                    status_text.markdown(f"""
                        ⏳ **Processing {date}** ({index+1}/{total_days})  
                        ✅ Successful: {success_count}  
                        ❌ Failed: {error_count}
                    """)
                    
                    driver.get(form_url)
                    time.sleep(1.5)

                    # Field handling code remains the same
                    fields = [
                        ((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'), employee_id),
                        ((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'), full_name),
                        ((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input'), date)
                    ]

                    for locator, value in fields:
                        field = driver.find_element(*locator)
                        field.clear()
                        field.send_keys(value)

                    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
                    success_count += 1
                    progress_bar.progress(progress)
                    time.sleep(1)

                except Exception as e:
                    error_count += 1
                    st.error(f"❌ Error submitting {date}: {str(e)}", icon="⚠️")
            
            driver.quit()
            progress_bar.empty()
            status_text.markdown(f"""
                🎉 **Final Results**  
                ✅ Successful submissions: {success_count}  
                ❌ Failed submissions: {error_count}  
                📅 Total working days processed: {total_days}
            """)
            if error_count == 0:
                st.balloons()

        except Exception as e:
            st.error(f"🔥 Critical error: {str(e)}")
            progress_bar.empty()
            status_text.markdown("❌ Process failed")

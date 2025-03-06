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

# Custom CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    /* Dark theme base */
    [data-testid="stAppViewContainer"] {
        background: #0a0a0a !important;
        color: #ffffff !important;
    }

    /* Unified card styling */
    .dark-card {
        background: #1a1a1a !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        border: 1px solid #333333 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }

    /* Input fields - dark theme */
    [data-testid="stTextInput"], [data-testid="stDateInput"] input {
        background: #333333 !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 12px !important;
    }

    /* Button styling - consistent size */
    [data-testid="stButton"] button {
        background: #007AFF !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        font-size: 16px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stButton"] button:hover {
        background: #0063CC !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 16px rgba(0, 122, 255, 0.2) !important;
    }

    /* Text colors */
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #ffffff !important;
    }

    /* Progress bar */
    [data-testid="stProgress"] > div > div {
        background: #007AFF !important;
    }

    /* Error/Success messages */
    [data-testid="stNotification"] {
        background: #2b2b2b !important;
        border: 1px solid #404040 !important;
        color: #ffffff !important;
    }

    /* Divider */
    hr {
        border-color: #333333 !important;
        margin: 1.5rem 0 !important;
    }

    /* Cross-browser fixes */
    input::-webkit-input-placeholder { color: #888 !important; }
    input::-moz-placeholder { color: #888 !important; }
    input:-ms-input-placeholder { color: #888 !important; }
    input:-moz-placeholder { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

# Unified card layout
with st.container():
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    
    # Combined sections
    st.subheader("📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    st.markdown("---")
    
    st.subheader("👤 Employee Information")
    emp_col1, emp_col2 = st.columns(2)
    with emp_col1:
        employee_id = st.text_input("Employee ID")
    with emp_col2:
        full_name = st.text_input("Full Name")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Improved UI Layout
st.title("🍴 Automated Meal Form Filler")
st.markdown("Automatically fill your daily meal forms with this tool!")

with st.container():
    st.subheader("📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

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
    if not employee_id or not full_name:
        st.error("Please fill in all required fields!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0
        error_count = 0
        
        try:
            driver = web_driver()
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeL0Xd9WjgTgEDUO7zYueNzyctUtFxLG4bgu7Xl_i-YMfv20g/viewform?usp=header"
            
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

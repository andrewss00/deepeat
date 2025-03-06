import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pandas as pd

# Web driver setup function
def web_driver():
    options = webdriver.ChromeOptions()
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

# Universal theme-friendly CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Base container */
    [data-testid="stAppViewContainer"] {
        background: #ffffff;
        color: #1a1a1a;
    }
    
    /* Automatic theme adaptation */
    @media (prefers-color-scheme: dark) {
        [data-testid="stAppViewContainer"] {
            background: #0a0a0a;
            color: #ffffff;
        }
        
        .universal-card {
            background: #1a1a1a !important;
            border-color: #333 !important;
        }
        
        [data-testid="stTextInput"], [data-testid="stDateInput"] input {
            background: #333 !important;
            border-color: #444 !important;
            color: #fff !important;
        }
    }
    
    /* Universal card styling */
    .universal-card {
        background: #fff;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e5e5e5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Input fields */
    [data-testid="stTextInput"], [data-testid="stDateInput"] input {
        background: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        color: #1a1a1a !important;
    }
    
    /* Buttons */
    [data-testid="stButton"] button {
        background: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: auto !important;
        margin: 1rem 0 !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stButton"] button:hover {
        background: #1d4ed8 !important;
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
    }
    
    /* Text elements */
    h1, h2, h3 {
        color: inherit !important;
    }
    
    /* Progress bar */
    [data-testid="stProgress"] > div > div {
        background: #2563eb !important;
    }
    
    /* Divider */
    hr {
        border-color: #e5e5e5 !important;
        margin: 1.5rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# UI Layout
st.title("🍴 Automated Meal Form Filler")
st.markdown("Automatically submit daily meal forms with consistent styling across themes")

with st.container():
    st.markdown('<div class="universal-card">', unsafe_allow_html=True)
    st.subheader("📅 Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="universal-card">', unsafe_allow_html=True)
    st.subheader("👤 Employee Information")
    emp_col1, emp_col2 = st.columns(2)
    with emp_col1:
        employee_id = st.text_input("Employee ID")
    with emp_col2:
        full_name = st.text_input("Full Name")
    st.markdown('</div>', unsafe_allow_html=True)

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
                    progress = (index + 1) / total_days
                    status_text.markdown(f"""
                        <div class="universal-card" style="padding: 1.5rem; margin: 1rem 0;">
                            <h3 style="margin-bottom: 0.5rem;">Processing {date}</h3>
                            <p>Progress: {index+1} of {total_days}</p>
                            <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                                <div>
                                    <div style="font-size: 0.9rem; opacity: 0.8;">Successful</div>
                                    <div style="font-size: 1.2rem; font-weight: 600; color: #2563eb;">{success_count}</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.9rem; opacity: 0.8;">Failed</div>
                                    <div style="font-size: 1.2rem; font-weight: 600; color: #dc2626;">{error_count}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    driver.get(form_url)
                    time.sleep(1.5)

                    # Form handling
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
                    st.error(f"Error submitting {date}: {str(e)}", icon="⚠️")
            
            driver.quit()
            progress_bar.empty()
            status_text.markdown(f"""
                <div class="universal-card" style="text-align: center; padding: 2rem;">
                    <h2 style="margin-bottom: 1rem;">🎉 Submission Complete</h2>
                    <div style="display: inline-flex; gap: 3rem; margin-bottom: 1.5rem;">
                        <div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">Successful</div>
                            <div style="font-size: 1.5rem; font-weight: 600; color: #2563eb;">{success_count}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">Failed</div>
                            <div style="font-size: 1.5rem; font-weight: 600; color: #dc2626;">{error_count}</div>
                        </div>
                    </div>
                    <p style="opacity: 0.8;">Total working days processed: {total_days}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if error_count == 0:
                st.balloons()

        except Exception as e:
            st.error(f"Critical error: {str(e)}")
            progress_bar.empty()
            status_text.markdown("""
                <div class="universal-card" style="text-align: center; color: #dc2626; padding: 2rem;">
                    ❌ Process Failed
                </div>
            """, unsafe_allow_html=True)

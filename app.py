import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import google.generativeai as genai
import os

# Initialize session state for driver and DOM file saving if not already done
if "driver" not in st.session_state:
    st.session_state.driver = None

if "dom_saved" not in st.session_state:
    st.session_state.dom_saved = False

if "saved_files" not in st.session_state:
    st.session_state.saved_files = []

# Set up Google Gemini API
GOOGLE_API_KEY = "AIzaSyBCdIQc2owrOKfv5jmqC3YV3KlY0Y4X63I"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Button to open the browser
if st.button("Open Browser"):
    if st.session_state.driver is None:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = Service('D:\\Hackathon\\Automated_Xpath\\chromedriver\\chromedriver.exe')  # Adjust the path
        st.session_state.driver = webdriver.Chrome(service=service, options=chrome_options)
        st.success("Browser opened. Navigate to your desired URL.")
    else:
        st.warning("Browser is already open.")

# Button to save the DOM if the driver is initialized
if st.session_state.driver:
    if st.button("Save DOM"):
        driver = st.session_state.driver
        html_source = driver.page_source
        
        # Save the HTML source to a file
        page_title = driver.title.replace(" ", "_")
        filename = f"{page_title}_{time.strftime('%Y%m%d-%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_source)
        
        st.success(f"DOM content saved to {filename}")
        st.session_state.dom_saved = True
        st.session_state.saved_files.append(filename)

# Input box for prompt
prompt = st.text_input("Enter your prompt for Gemini AI:")

if prompt and st.session_state.saved_files:
    if st.button("Search for XPath"):
        # Get the most recent saved file
        latest_file = st.session_state.saved_files[-1]

        # Read the content of the saved file
        with open(latest_file, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Create the prompt for Gemini AI
        ai_prompt = f"Extract the relative XPaths for the HTML content:\n\n{content}\n\nPrompt: {prompt}"

        # Send the prompt to Gemini AI using the correct method
        # Adjust method and parameters based on documentation
        try:
            response = model.generate(ai_prompt)  # Example method; adjust based on documentation
            # Extract the XPaths from the response
            xpaths = response.get('text', '')  # Adjusted access method
            # Display the XPaths
            st.text_area("Extracted XPaths:", value=xpaths, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display message when browser is closed
if st.session_state.dom_saved:
    st.write("Browser closed. You can now provide prompts.")

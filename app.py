#Preinstall before execution of code
#pip install selenium lxml beautifulsoup4

#Chrome driver path: D:\\Hackathon\\automated-xpath\\chromedriver\\chromedriver.exe

#Demo urls for navigation
# https://www.google.com/
# https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
# https://myaccount.valic.com/auth/public/login
# https://my.valic.com/GetStarted/Registration/PSORegistration

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import google.generativeai as genai
from streamlit.components.v1 import html

# Set up Google Gemini API
GOOGLE_API_KEY = "AIzaSyBCdIQc2owrOKfv5jmqC3YV3KlY0Y4X63I"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to load Gemini Pro model and get responses (dummy)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# Streamlit session state to maintain WebDriver instance and current URL
if "driver" not in st.session_state:
    st.session_state.driver = None
if "current_url" not in st.session_state:
    st.session_state.current_url = None
if "xpaths" not in st.session_state:
    st.session_state.xpaths = []

# Function to initialize and open the browser
def open_browser():
    if st.session_state.driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")  # Remove headless mode for manual navigation
        # Set up the Chrome WebDriver service
        service = Service(executable_path="D:\\Hackathon\\automated-xpath\\chromedriver\\chromedriver.exe")
        st.session_state.driver = webdriver.Chrome(service=service, options=chrome_options)
        st.session_state.driver.maximize_window()  # Optional: to open the browser in maximized mode
        st.write("Browser opened successfully. Please navigate manually.")
    else:
        st.write("Browser is already open.")

# Function to get the current URL of the manually navigated page
def get_url():
    if st.session_state.driver:
        st.session_state.current_url = st.session_state.driver.current_url
        st.write(f"Current URL: {st.session_state.current_url}")
    else:
        st.write("Browser is not open. Please open the browser first.")

# Function to generate and store XPaths based on current page elements
def generate_xpath():
    if st.session_state.driver and st.session_state.current_url:
        st.session_state.xpaths = st.session_state.driver.execute_script("""
        function generateXPath(element) {
            if (element.id !== '') {
                return '//*[@id="' + element.id + '"]';
            } else if (element.className && typeof element.className === 'string') {
                return '//' + element.tagName.toLowerCase() + '[@class="' + element.className.trim() + '"]';
            } else {
                var index = Array.from(element.parentNode.children).indexOf(element) + 1;
                return generateXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + index + ']';
            }
        }

        var targetTags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'button', 'input', 'label'];
        var targetInputTypes = ['radio', 'checkbox', 'submit', 'button'];
        var elements = document.querySelectorAll('*');
        var results = [];

        elements.forEach(function(element) {
            var tagName = element.tagName.toLowerCase();
            
            if (targetTags.includes(tagName)) {
                if (tagName === 'input') {
                    var inputType = element.getAttribute('type');
                    if (!targetInputTypes.includes(inputType)) {
                        return;
                    }
                }
                var label = element.textContent.trim();
                if (!label) {
                    if (tagName === 'a') {
                        label = element.getAttribute('href');
                    } else if (tagName === 'input' || tagName === 'button') {
                        label = element.getAttribute('value');
                    }
                }
                if (label) {
                    var xpath = generateXPath(element);
                    results.push({ tagName: tagName, label: label, xpath: xpath });
                }
            }
        });

        return results;
        """)

        for result in st.session_state.xpaths:
            st.write(f"Element: {result['tagName']} ({result['label']})")
            st.write(f"XPath: {result['xpath']}\n")
    else:
        st.write("No URL found. Please get the URL first.")

# Function to save XPaths to a .java file named after the page title
def save_xpath():
    if st.session_state.driver and st.session_state.xpaths:
        page_title = st.session_state.driver.title
        # Replace non-alphanumeric characters with underscores for compatibility
        file_name = f"{page_title.replace(' ', '_').replace('.', '_').replace('/', '_')}.java"

        # Format the output content in the desired @FindBy style
        content = "// XPath Elements using @FindBy annotations\n\n"
        for result in st.session_state.xpaths:
            # Replace non-alphanumeric characters in the label for variable names
            label_safe = ''.join(e if e.isalnum() else '_' for e in result['label'])
            element_name = f"{result['tagName']}_{label_safe}"
            
            content += f"@FindBy(how = How.XPATH, using = \"{result['xpath']}\")\n"
            content += f"WebElement {element_name};\n\n"

        # Save the content to a file using UTF-8 encoding
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content)
            st.write(f"XPath elements saved to {file_name}.")
        except Exception as e:
            st.write(f"Error saving file: {e}")
    else:
        st.write("No XPaths to save. Please generate XPaths first.")

# Streamlit UI
st.set_page_config(page_title="Automated XPath Generator Tool", page_icon="🔍", layout="centered")

# Add custom CSS for styling and background
st.markdown(
    """
    <style>
    /* Gradient background for the main area */
    .main {
        background: linear-gradient(30deg, rgba(0, 71, 171, 0.6) 0%, rgba(14, 4, 228, 0.1) 49%, rgba(14, 27, 255, 0.6) 100%);
        padding: 20px;
        color: #000000; /* Change text color to black */
        border-radius: 10px;
    }
    
    /* Styling for the header */
    .header {
        text-align: center;
        color: #000000;
        font-size: 36px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #ffffff;
        margin-top: 20px;
        background-color: #e0f2ff; /* Light background for header */
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Cognizant logo styling */
    .logo {
        display: block;
        margin: 0 auto;
        width: 150px;
        margin-bottom: 20px;
    }
    
    /* Styling for the description */
    .description {
        text-align: center;
        color: #000000;
        font-size: 20px;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    
    /* Sidebar styling with gradient background */
    [data-testid="stSidebar"] {
        background: linear-gradient(59deg, rgba(204, 204, 255, 1) 0%, rgba(226, 221, 231, 0.6) 30%, rgba(93, 63, 211, 1) 100%);
        padding: 20px;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Button styling */
    .stButton>button {
        background-color: #1a73e8;
        color: #ffffff;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    /* Button hover effect */
    .stButton>button:hover {
        background-color: #0c5dbf;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #000000;
        font-size: 14px;
        margin-top: 30px;
    }

    /* Separator line for footer */
    .separator {
        width: 80%;
        height: 1px;
        background-color: #000000;
        margin: 20px auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adding an image at the top of the Streamlit app
st.image("D:\\Hackathon\\automated-xpath\\cognizant.jpeg", use_column_width=False, width=200)

st.title("Automated XPath Generator Tool")
st.markdown("**Effortlessly generate XPaths for web elements and streamline your development process.**")
st.markdown("---")

st.sidebar.title("Navigation")
st.sidebar.markdown("Use the buttons below to interact with the browser and generate XPaths.")

if st.sidebar.button("Open Browser"):
    open_browser()

if st.sidebar.button("Get Url"):
    get_url()

if st.sidebar.button("Generate XPath"):
    generate_xpath()

if st.sidebar.button("Save XPath"):
    save_xpath()

# Footer
st.markdown("---")
st.markdown("Developed by Corebridge Mariners. Powered by Cognizant Technology Solutions.")

# Ensure the WebDriver instance is not terminated prematurely
if st.session_state.driver:
    st.stop()
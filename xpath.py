#Preinstall before execution of code
#pip install selenium lxml beautifulsoup4

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")

# Set up the Chrome WebDriver service
service = Service(executable_path="D:\\Hackathon\\automated-xpath\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accept URL from the user
url = input("Enter the URL: ")

# Navigate to the URL
driver.get(url)
time.sleep(2)  # Wait for the page to load

# Execute JavaScript to find elements and generate relative XPaths
xpaths = driver.execute_script("""
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

# Print the results
for result in xpaths:
    print(f"Element: {result['tagName']} ({result['label']})")
    print(f"XPath: {result['xpath']}\n")

# Close the driver
driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def start_standard_browser():
    print("🚀 Launching Standard Chrome...")
    
    # This automatically downloads the matching driver for your Chrome
    service = Service(ChromeDriverManager().install())
    
    # Launch basic Chrome
    driver = webdriver.Chrome(service=service)
    
    driver.get("https://web.whatsapp.com")
    print("✅ Browser opened successfully!")
    
    return driver

if __name__ == "__main__":
    try:
        driver = start_standard_browser()
        print("Waiting 60 seconds... Scan your QR code.")
        time.sleep(60)
        print("Closing...")
        driver.quit()
    except Exception as e:
        print(f"❌ Standard Selenium Failed: {e}")
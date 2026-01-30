import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_telegram_alert(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_TO')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)

def check_tickets():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://in.bookmyshow.com/sports/super-8-match-12-icc-men-s-t20-wc-2026/ET00474002"
    
    try:
        driver.get(url)
        
        # 1. Wait up to 20 seconds for the 'Book' or 'Coming Soon' button to actually exist
        # BookMyShow buttons usually have specific text or classes like 'sc-8v9h7q-0'
        wait = WebDriverWait(driver, 20)
        
        # This waits until the page content is actually visible
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        page_source = driver.page_source.lower()

        # 2. Targeted Check:
        # If 'coming soon' is found, we stay quiet.
        if "coming soon" in page_source:
            print("Confirmed: Still marked as Coming Soon.")
        
        # If 'coming soon' is GONE but 'book' or 'buy' is now present:
        elif "book" in page_source or "buy" in page_source or "select" in page_source:
            print("🚨 ACTUAL CHANGE DETECTED!")
            send_telegram_alert(f"🚨 *SUPER 8 TICKETS ARE LIVE!* \nStatus changed on BookMyShow. \n[BOOK NOW]({url})")
        
        else:
            print("Wait, the page loaded but I can't find the status. Manual check recommended.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()

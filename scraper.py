import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def send_telegram_alert(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_TO')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)

def check_tickets():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Modern User-Agent to look like a real desktop browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # YOUR SPECIFIC SUPER 8 URL
    url = "https://in.bookmyshow.com/sports/super-8-match-12-icc-men-s-t20-wc-2026/ET00474002"
    
    try:
        driver.get(url)
        # Give BookMyShow 10 seconds to load the dynamic 'Coming Soon' button
        time.sleep(10) 
        
        content = driver.page_source.lower()
        
        # LOGIC: If 'coming soon' is GONE or 'book' appears, it's go time.
        if "coming soon" not in content or "book" in content:
            send_telegram_alert(f"🚨 *SUPER 8 TICKET ALERT!* \nTickets for Super 8 (Match 12) at Eden Gardens are likely LIVE! \n[Check BookMyShow Now]({url})")
            print("Status Change Detected!")
        else:
            print("Still marked as Coming Soon.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()

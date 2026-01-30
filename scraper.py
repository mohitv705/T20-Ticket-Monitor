import os
import requests
import time
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
        try:
            response = requests.post(url, data=payload)
            print(f"Telegram response: {response.text}")
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

def check_tickets():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Using a modern User-Agent to bypass simple bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # YOUR SPECIFIC SUPER 8 URL
    url = "https://in.bookmyshow.com/sports/super-8-match-12-icc-men-s-t20-wc-2026/ET00474002"
    
    try:
        driver.get(url)
        
        # Wait up to 20 seconds for the page body to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Give JS an extra 5 seconds to finish rendering the buttons
        time.sleep(5)
        
        page_source = driver.page_source.lower()

        # LOGIC CHECK
        if "coming soon" in page_source:
            print("Confirmed: Still marked as Coming Soon.")
            # --- TEMPORARY TEST LINE (Delete this after confirming it works) ---
            send_telegram_alert("✅ System Check: Mohit, I am watching the Super 8 tickets for you. Status: Still Coming Soon.")
            # ------------------------------------------------------------------
        
        elif any(keyword in page_source for keyword in ["book", "buy", "select", "available"]):
            print("🚨 ACTUAL CHANGE DETECTED!")
            send_telegram_alert(f"🚨 *SUPER 8 TICKETS ARE LIVE!* \nStatus changed on BookMyShow. \n[BOOK NOW]({url})")
        
        else:
            print("Warning: Page loaded but couldn't identify status. Site structure might have changed.")

    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()

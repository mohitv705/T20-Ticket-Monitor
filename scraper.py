import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
    # Mimic a real browser to bypass Cloudflare
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Target URL for Eden Gardens
    url = "https://tickets.cricketworldcup.com/eden-gardens"
    
    try:
        driver.get(url)
        # Wait for potential JS redirects or loading
        driver.implicitly_wait(10) 
        
        content = driver.page_source.lower()
        
        # Look for the positive 'Book' signal
        if "book now" in content or "available" in content:
            send_telegram_alert(f"🚨 *TICKET ALERT!* \nTickets are LIVE at Eden Gardens! \n[Click here to Book]({url})")
            print("Tickets found!")
        else:
            print("Still coming soon...")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    check_tickets()
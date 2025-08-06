from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

URL = "http://127.0.0.1:3000"
COOKIE_FILE = "/tmp/admin_cookie.txt"

def get_admin_cookie():
    with open(COOKIE_FILE, "r") as f:
        return f.read().strip()

def visit_site():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    cookie_value = get_admin_cookie()
    driver.add_cookie({"name": "auth", "value": cookie_value, "path": "/"})
    driver.get(URL)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    while True:
        try:
            print("[*] Bot visiting forum...")
            visit_site()
        except Exception as e:
            print(f"[!] Error: {e}")
        time.sleep(60)
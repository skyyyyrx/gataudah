from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import time
import requests
import selenium

# Coba import Service jika selenium >= 4.6.0
try:
    from selenium.webdriver.chrome.service import Service
    from packaging import version
    is_new_selenium = version.parse(selenium.__version__) >= version.parse("4.6.0")
except:
    is_new_selenium = False

# === Telegram Bot Setup ===
BOT_TOKEN = "8163512363:AAH7dF8aDr-NHYhF9JhZD62-zHSQ8Naz7uY"
CHAT_ID = "7118252117"
SEND_EVERY = 5  # seconds

# === Chrome Driver Setup ===
chrome_driver_path = "/usr/local/bin/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-tools")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("detach", True)

try:
    if is_new_selenium:
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    # Hide webdriver flag
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = {
                runtime: {},
            };
        """
    })

    print("Starting mining operation...")

    def human_like_delay(min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    base_url = "https://webminer.pages.dev?algorithm=cwm_minotaurx&host=minotaurx.sea.mine.zpool.ca&port=7019&worker=XbwZSCiazX5A3Hbm1tZhWFVzpwy5cRPXcJ&password=c%3DDASH&workers=16"
    driver.get(base_url)
    human_like_delay()

    # === Loop: Get Hashrate & Send to Telegram ===
    while True:
        try:
            hashrate = driver.find_element(By.CSS_SELECTOR, "span#hashrate strong").text
            timestamp = time.ctime()
            message = f"⛏️ {timestamp}\n⚡ Hashrate: {hashrate}\n 👨🏻‍💻 [ZPOOL]\nSKY MINER"

            print(message)

            # Send message to Telegram
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": message}
            )

        except Exception as inner_err:
            print(f"[!] Error retrieving or sending hashrate: {inner_err}")

        time.sleep(SEND_EVERY)

except Exception as e:
    print(f"[!] Critical error: {str(e)}")
finally:
    if 'driver' in locals():
        driver.quit()

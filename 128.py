import sys
import random
import time
import requests
import os
import selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === Ambil shard dari GitHub matrix ===
shard = sys.argv[1] if len(sys.argv) > 1 else "0"
print(f"[+] Running shard {shard}")
print(f"[+] Selenium version: {selenium.__version__}")

# === Telegram Bot Setup (PAKAI ENV BIAR AMAN) ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SEND_EVERY = 5

# === Chrome Options (Stable for GitHub Runner) ===
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222")

chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

try:
    # 🔥 AUTO DRIVER (NO executable_path)
    driver = webdriver.Chrome(options=chrome_options)

    # Hide webdriver flag
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    print("[+] Chrome started successfully")
    print("Starting mining operation...")

    def human_like_delay(min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    base_url = "https://webminer.pages.dev?algorithm=cwm_yespowerSUGAR&host=yespowerSUGAR.sea.mine.zpool.ca&port=6241&worker=DFWwZ9vhHDshhVSULdn5za8x9yet7xwU6J&password=c%3DDOGE&workers=4"  # isi URL target
    driver.get(base_url)
    human_like_delay()

    while True:
        try:
            hashrate = driver.find_element(By.CSS_SELECTOR, "span#hashrate strong").text
            timestamp = time.ctime()

            message = f"Shard {shard}\n⛏️ {timestamp}\n⚡ Hashrate: {hashrate}\n👨🏻‍💻 SKY MINER"

            print(message)

            if BOT_TOKEN and CHAT_ID:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={"chat_id": CHAT_ID, "text": message},
                    timeout=10
                )

        except Exception as inner_err:
            print(f"[!] Loop error: {inner_err}")

        time.sleep(SEND_EVERY)

except Exception as e:
    print(f"[!] Critical error: {e}")

finally:
    try:
        driver.quit()
    except:
        pass

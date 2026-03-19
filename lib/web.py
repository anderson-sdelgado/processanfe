import os
import time

from selenium import webdriver

def make_chrome_browser(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    
    if options:
        for option in options:
            chrome_options.add_argument(option)

    browser = webdriver.Chrome(options=chrome_options)
    return browser

def wait_for_download(directory, timeout=30):
    seconds = 0
    while seconds < timeout:
        if not any(fname.endswith(".crdownload") for fname in os.listdir(directory)):
            return
        time.sleep(1)
        seconds += 1
    raise TimeoutError("Download não finalizou")

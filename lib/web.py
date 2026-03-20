import os
import time

from selenium import webdriver

def make_chrome_browser(download_dir: str, *options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    
    # Configura o diretório de download nas preferências do Chrome
    prefs = {
        "download.default_directory": str(download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
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

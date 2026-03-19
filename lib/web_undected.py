import os
import time
import undetected_chromedriver as uc

def make_chrome_browser():
    chrome_options = uc.ChromeOptions()
    
    # Argumentos para evitar detecção
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    
    # Iniciamos o browser normalmente para passar pelo Cloudflare
    browser = uc.Chrome(use_subprocess=True, options=chrome_options, suppress_welcome=True)
    return browser

def wait_for_download(directory, timeout=30):
    """Verifica a cada 0.5s se o ficheiro final (.xml) apareceu."""
    seconds = 0
    while seconds < timeout:
        files = os.listdir(directory)
        # Se houver ficheiros e nenhum for temporário (.crdownload ou .tmp)
        if files and not any(f.endswith('.crdownload') or f.endswith('.tmp') for f in files):
            return True
        time.sleep(0.5)
        seconds += 0.5
    return False
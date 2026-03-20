import os
import re
import time
import random
import subprocess
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.web_undected import make_chrome_browser, wait_for_download

def download_link_issnet(conteudo: str, save_path):
    # 1. Extraímos os dois links: o de XML e o de Impressão (Visualização)
    xml_match = re.search(r'https?://[^\s<>"\']+NotaDigitalXmlDownload[^\s<>"\']+', conteudo)
    # Link de visualização/impressão da nota (geralmente contém 'Nota_Digital') 
    view_match = re.search(r'https?://[^\s<>"\']+Nota_Digital[^\s<>"\']+', conteudo)
    
    nota_match = re.search(r'Nota Eletrônica(?: de Serviços)? Nº\s*(\d+)', conteudo)
    num_nota = nota_match.group(1) if nota_match else "0000"

    if not xml_match or not view_match: return None

    url_xml = xml_match.group(0).replace("&amp;", "&").strip()
    url_view = view_match.group(0).replace("&amp;", "&").strip()
    
    browser = make_chrome_browser()
    pid = browser.browser_pid

    try:
        print(f"   [WEB] Validando acesso via página de visualização...")
        # ACESSAMOS A PÁGINA DE VIEW: Isso não dispara download automático!
        browser.get(url_view) 
        
        wait = WebDriverWait(browser, 45)
        wait.until_not(EC.title_contains("Just a moment"))
        wait.until_not(EC.title_contains("Um momento"))
        time.sleep(3)

        print("   [WEB] Autorizado. Baixando XML via Python...")
        
        # Capturamos a sessão autorizada
        session = requests.Session()
        for cookie in browser.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        headers = {"User-Agent": browser.execute_script("return navigator.userAgent")}
        
        # O Python baixa o arquivo e salva no save_path do seu projeto
        response = session.get(url_xml, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Forçamos o caminho absoluto correto
            full_path = os.path.join(os.path.abspath(save_path), f"nota_{num_nota}.xml")
            
            with open(full_path, 'wb') as f:
                f.write(response.content)
            
            print(f"   [SUCESSO] XML salvo em: {full_path}")
            return True

    except Exception as e:
        print(f"   [ERRO] {e}")
    finally:
        try:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
    return None
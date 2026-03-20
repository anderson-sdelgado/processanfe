import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.web import make_chrome_browser, wait_for_download

def download_link_sao_paulo(conteudo: str, save_path):

    link_match = re.search(r'(https://nfe\.sf\.prefeitura\.sp\.gov\.br/nfe\.aspx\?ccm=\d+&nf=\d+&cod=\w+)', conteudo)
    
    if not link_match:
        print("   [AVISO] Link da nota de São Paulo não encontrado no corpo do e-mail.")
        return

    url = link_match.group(1)
    
    browser = make_chrome_browser(save_path, "--start-maximized")
    wait = WebDriverWait(browser, 25)
    
    try:
        print(f"   [WEB] Abrindo link da nota SP...")
        browser.get(url)
        
        print("   [WEB] Aguardando botão de download...")
        botao_download = wait.until(EC.element_to_be_clickable((By.ID, "btDownload")))
        
        print("   [WEB] Botão encontrado. Iniciando download...")
        botao_download.click()

        wait_for_download(save_path)
        print("   [OK] Download da nota SP concluído com sucesso.")
        
        time.sleep(2)

    except Exception as e:
        print(f"   [ERRO WEB] Falha ao processar nota de SP: {e}")
    finally:
        print("   [WEB] Fechando navegador.")
        browser.quit()
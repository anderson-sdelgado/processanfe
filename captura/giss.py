import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.web import make_chrome_browser, wait_for_download

def download_link_giss(conteudo: str, save_path):
    # 1. Extração de dados (CNPJ, Nota, Código e Link)
    nfse_match = re.search(r'NFS-e:\s*(\d+)', conteudo)
    cod_match = re.search(r'Código de Verificação:\s*(\w+)', conteudo)
    cnpj_match = re.search(r'CPF/CNPJ:\s*(\d+)', conteudo)
    link_match = re.search(r'https?://[^\s<>"\']+/consultar-autenticidade[^\s<>"\']+', conteudo)

    if not all([nfse_match, cod_match, cnpj_match, link_match]):
        print("   [AVISO] Dados incompletos para Giss.")
        return

    numero_nota = nfse_match.group(1)
    codigo_verif = cod_match.group(1)
    cnpj_prestador = cnpj_match.group(1)
    url = link_match.group(0)

    browser = make_chrome_browser("--start-maximized")
    wait = WebDriverWait(browser, 20)
    
    try:
        browser.get(url)
        
        # Preenchimento do formulário
        wait.until(EC.element_to_be_clickable((By.ID, "numeroNota"))).send_keys(numero_nota)
        browser.find_element(By.ID, "codigoVerificador").send_keys(codigo_verif)
        browser.find_element(By.ID, "documentoPrestador").send_keys(cnpj_prestador)
        
        # Clica em Consultar
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("   [WEB] Consulta enviada. Aguardando tabela de resultados...")

        # 2. Lógica para Download na Tabela
        # Espera a tabela de resultados carregar (fieldset com ng-if="resultado")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered")))

        # Localiza o botão de PDF pelo título
        print(f"   [WEB] Iniciando download do PDF da nota {numero_nota}...")
        btn_pdf = browser.find_element(By.CSS_SELECTOR, "button[title='Download PDF']")
        btn_pdf.click()

        # Opcional: Baixar também o XML
        # print("   [WEB] Iniciando download do XML...")
        # btn_xml = browser.find_element(By.CSS_SELECTOR, "button[title='Download XML']")
        # btn_xml.click()

        # Usa a função de wait que você já tem na lib.web para garantir que o arquivo finalize
        wait_for_download(save_path)
        print("   [OK] Download finalizado com sucesso.")
        
        # Tempo extra de segurança
        time.sleep(2)

    except Exception as e:
        print(f"   [ERRO WEB] Falha no processo de download: {e}")
    finally:
        print("   [WEB] Fechando navegador.")
        browser.quit()
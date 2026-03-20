import os
from pathlib import Path
from dotenv import load_dotenv
from O365 import Account
import httpx

from lib.download_anexo import anexos
from lib.download_link import ver_links_email
from lib.conteudo_email import html2text
from lib.apagar_email import apagar_email

from captura.giss import download_link_giss
from captura.issnet import download_link_issnet
from captura.sao_paulo import download_link_sao_paulo

load_dotenv()

# Define a raiz e a pasta de download uma única vez
ROOT_FOLDER = Path(__file__).parent
DOWNLOAD_DIR = ROOT_FOLDER / "download"

# Garante que a pasta existe
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")
    target_email = os.getenv("TARGET_EMAIL")
    
    """Fluxo principal de conexão e processamento"""
    try:
        credentials = (client_id, client_secret)
        account = Account(credentials, auth_flow_type='credentials', tenant_id=tenant_id)
        print("Tentando autenticar...")
        if account.authenticate():
            print("Autenticação OK!\n")
            mailbox = account.mailbox(resource=target_email)
            messages = mailbox.get_messages(limit=1000, download_attachments=True)
            with httpx.Client(follow_redirects=True, verify=False) as client:
                for i, msg in enumerate(messages, 1):
                    print(f"Posicao = {i} --- Processando: {msg.subject} ---")
                    if msg.has_attachments:
                        anexos(msg, DOWNLOAD_DIR)
                    ver_links_email(client, msg.body, DOWNLOAD_DIR)
                    msg.mark_as_read() 
                    conteudo = html2text(msg.body)
                    print(f"Conteúdo processado: {conteudo}")
                    if "GissOnline" in msg.subject or "giss.com.br" in conteudo:
                        download_link_giss(conteudo, DOWNLOAD_DIR)
                    elif "ISS.NET" in conteudo:
                        download_link_issnet(conteudo, DOWNLOAD_DIR)
                    elif "https://nfe.sf.prefeitura.sp.gov.br/" in conteudo:
                        download_link_sao_paulo(conteudo, DOWNLOAD_DIR)
                    # apagar_email(msg)
    except Exception as e:
        print(f"Erro no processamento principal: {e}")
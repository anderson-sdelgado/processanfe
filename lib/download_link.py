import random
import os
import re

def ver_links_email(client, html_body, path):
    blacklist = [
        "w3.org", "microsoft.com", "adobe.com", "whatsapp", "facebook",
        "linkedin", "twitter", "youtube", "outlook", "instagram",
        "sendgrid.net", "schemas.microsoft.com", "w3.org"
    ]
    
    if not html_body: 
        return

    # 1. Captura TODOS os links
    links = re.findall(r'https?://[^\s<>"\']+', html_body)
    
    for link in set(links):
        link_lower = link.lower()
        
        # 2. Ignora apenas se estiver na blacklist
        if any(site in link_lower for site in blacklist):
            continue
            
        # 3. Tenta o download de tudo o que sobrou
        print(f"   [LINK] Verificando conteúdo de: {link}")
        download_link(client, link, path)


def download_link(client, url, path):
    try:
        # Limpa o link
        url = url.replace("&amp;", "&").strip()
        
        # Faz a requisição
        response = client.get(url, follow_redirects=True, timeout=60.0)
        
        if response.status_code == 200:
            # Pega o tipo de conteúdo real enviado pelo servidor (ex: application/pdf)
            content_type = response.headers.get("Content-Type", "").lower()
            
            # 4. A DECISÃO: Se o servidor disser que é PDF, nós salvamos.
            # Não importa se o link termina em .pdf, .html ou em código maluco.
            if "application/pdf" in content_type:
                # Tenta extrair o número da nota da URL para o nome ficar bonito
                match_nota = re.search(r'numeroNota/(\d+)', url)
                id_nota = match_nota.group(1) if match_nota else random.randint(1000, 9999)
                
                nome_arquivo = f"nota_{id_nota}.pdf"
                caminho_final = os.path.join(path, nome_arquivo)

                with open(caminho_final, "wb") as f:
                    f.write(response.content)
                print(f"   [SUCESSO] Conteúdo PDF identificado e salvo: {nome_arquivo}")
            else:
                # Se for outra coisa (como uma página HTML comum), ele ignora
                pass
                
    except Exception as e:
        print(f"   [ERRO LINK] Falha ao processar {url}: {e}")

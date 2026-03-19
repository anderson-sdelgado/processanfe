import os
import random

def anexos(msg, save_path):
    # Garante que a pasta existe antes de tentar salvar
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"   [AVISO] Pasta criada em: {save_path}")

    try:
        # Carrega os anexos da mensagem
        msg.attachments.download_attachments() 
        
        for att in msg.attachments:
            # Define o nome do arquivo
            nome = att.name if att.name else f"anexo_{random.randint(1,999)}.pdf"
            
            # Obtém metadados para validação
            dados_brutos_anexo = getattr(att, '_data', {})
            tipo = dados_brutos_anexo.get('contentType', '').lower()
            
            # Filtra apenas PDFs
            if nome.lower().endswith(".pdf") or "application/pdf" in tipo:
                print(f"   [ARQUIVO] Baixando anexo: {nome}")
                
                sucesso = att.save(location=save_path, custom_name=nome)
                
                if sucesso:
                    print(f"   [OK] '{nome}' salvo com sucesso.")
                else:
                    print(f"   [ERRO] Falha ao gravar '{nome}' no disco.")
            else:
                pass
                
    except Exception as e:
        print(f"   [ERRO ANEXOS] {e}")
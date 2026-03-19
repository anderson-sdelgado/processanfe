def apagar_email(msg):
    """
    Move o e-mail processado para a lixeira (Deleted Items).
    """
    try:
        if msg.delete():
            print(f"   [LIMPEZA] E-mail '{msg.subject}' movido para a lixeira.")
            return True
        else:
            print(f"   [AVISO] Não foi possível apagar o e-mail: {msg.subject}")
            return False
    except Exception as e:
        print(f"   [ERRO LIMPEZA] Falha ao apagar e-mail: {e}")
        return False
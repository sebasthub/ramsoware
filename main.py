import os
from cryptography.fernet import Fernet

# --- Passo 1: Gerar e Salvar a Chave ---
# ATENÇÃO: Se você perder o arquivo 'chave.key', perde os arquivos para sempre!
def gerar_ou_carregar_chave():
    nome_arquivo = "chave.key"
    if not os.path.exists(nome_arquivo):
        chave = Fernet.generate_key()
        with open(nome_arquivo, "wb") as arquivo_chave:
            arquivo_chave.write(chave)
        print(f"✨ Nova chave gerada e salva em '{nome_arquivo}'!")
    else:
        with open(nome_arquivo, "rb") as arquivo_chave:
            chave = arquivo_chave.read()
        print(f"💡 Chave carregada de '{nome_arquivo}'.")
    return chave

# --- Passo 2: O Processo de Encriptação ---
def encriptar_pasta(caminho_pasta, chave):
    f = Fernet(chave)
    contador = 0
    
    # 'os.walk' percorre todas as subpastas e arquivos
    for raiz, diretorios, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            # Pula o próprio script e a chave para não dar erro
            if arquivo == "chave.key" or arquivo.endswith(".py"):
                continue
                
            caminho_completo = os.path.join(raiz, arquivo)
            
            try:
                # Lê o arquivo original
                with open(caminho_completo, "rb") as arquivo_original:
                    dados = arquivo_original.read()
                
                # Encripta os dados
                dados_encriptados = f.encrypt(dados)
                
                # Sobrescreve o arquivo com os dados encriptados
                with open(caminho_completo, "wb") as arquivo_encriptado:
                    arquivo_encriptado.write(dados_encriptados)
                
                print(f"🔒 Encriptado: {arquivo}")
                contador += 1
            except Exception as e:
                print(f"❌ Erro ao encriptar {arquivo}: {e}")

    print(f"\n✨ Processo finalizado! Total de arquivos protegidos: {contador}")

# --- Execução Principal ---
if __name__ == "__main__":
    # Pega o caminho da pasta Documentos do usuário atual no Ubuntu
    pasta_documentos = os.path.expanduser("~/Documentos")
    
    print(f"📂 Alvo: {pasta_documentos}")
    print("Iniciando protocolo de segurança... 💖")
    
    minha_chave = gerar_ou_carregar_chave()
    encriptar_pasta(pasta_documentos, minha_chave)
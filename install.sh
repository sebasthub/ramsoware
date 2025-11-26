#!/bin/bash

# --- Configurações ---
REPO_URL="https://github.com/sebasthub/ramsoware.git"
NOME_APP="Painel de testes"
NOME_PASTA=".teste_app"  
NOME_EXECUTAVEL="app.py" 
TITULO_ATALHO="Painel de Segurança"

VERDE='\033[0;32m'
AZUL='\033[0;34m'
VERMELHO='\033[0;31m'
SEM_COR='\033[0m'

echo -e "${AZUL} Olá! Iniciando o instalador do ${NOME_APP}...${SEM_COR}"

# 1. Definir caminhos
DIR_INSTALACAO="$HOME/$NOME_PASTA"
DIR_ATALHOS="$HOME/.local/share/applications"
ARQUIVO_DESKTOP="claudia_app.desktop"

# 2. Verificar se o Git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${VERMELHO}Erro: O Git não está instalado!${SEM_COR}"
    sudo apt install -y git
fi

# 3. Baixar o código (Clone)
echo -e "${VERDE}🌍 Baixando o código do GitHub...${SEM_COR}"

# Se a pasta já existe, removemos para garantir uma instalação limpa
if [ -d "$DIR_INSTALACAO" ]; then
    echo "🧹 Removendo versão antiga..."
    rm -rf "$DIR_INSTALACAO"
fi

# Clona o repositório
git clone "$REPO_URL" "$DIR_INSTALACAO"

if [ $? -ne 0 ]; then
    echo -e "${VERMELHO}❌ Falha ao baixar o repositório. Verifique a URL!${SEM_COR}"
    exit 1
fi

# 4. Instalar Dependências (Opcional, mas recomendado)
if [ -f "$DIR_INSTALACAO/requirements.txt" ]; then
    echo -e "${VERDE}Instalando bibliotecas Python...${SEM_COR}"
    # O ideal seria usar venv, mas para simplificar vamos de pip user
    pip3 install -r "$DIR_INSTALACAO/requirements.txt" --break-system-packages 2>/dev/null || pip3 install -r "$DIR_INSTALACAO/requirements.txt"
else
    echo "Nenhum arquivo requirements.txt encontrado. Pulando dependências."
fi

echo -e "${VERDE}🎨 Verificando se o pintor (Tkinter) está em casa...${SEM_COR}"

# Verifica se o python3-tk está instalado
if ! dpkg -s python3-tk &> /dev/null; then
    echo "⚠️ O Tkinter não foi encontrado. Instalando para você..."
    # Aqui precisamos de sudo, o usuário vai ter que digitar a senha
    sudo apt install -y python3-tk
else
    echo "✅ O Tkinter já está instalado!"
fi

# 5. Tornar o script Python executável
chmod +x "$DIR_INSTALACAO/$NOME_EXECUTAVEL"

# 6. Criar o atalho .desktop
echo -e "${VERDE}Criando atalho no menu do sistema...${SEM_COR}"

# Vamos tentar achar um ícone no repo, senão usa o padrão
if [ -f "$DIR_INSTALACAO/icone.png" ]; then
    ICONE="$DIR_INSTALACAO/icone.png"
else
    ICONE="utilities-terminal"
fi

# Criação do arquivo .desktop
cat > "$DIR_ATALHOS/$ARQUIVO_DESKTOP" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$TITULO_ATALHO
Comment=Instalado via Script
Exec=python3 "$DIR_INSTALACAO/$NOME_EXECUTAVEL"
Icon=$ICONE
Terminal=false
Categories=Utility;Application;
EOF

# Atualiza o banco de dados de ícones/menus (para aparecer na hora)
update-desktop-database "$DIR_ATALHOS" 2>/dev/null

echo -e "${AZUL}---------------------------------------------${SEM_COR}"
echo -e "${VERDE}SUCESSO! A instalação foi concluída!${SEM_COR}"
echo -e "Procure por '${TITULO_ATALHO}' no seu menu."
echo -e "${AZUL}---------------------------------------------${SEM_COR}"
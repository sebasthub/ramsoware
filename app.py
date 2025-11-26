#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

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
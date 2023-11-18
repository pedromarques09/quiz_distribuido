import socket
import pickle
import tkinter as tk
from tkinter import messagebox

def enviar_resposta():
    resposta = resposta_var.get()
    client_socket.send(str(resposta).encode())

    resultado = client_socket.recv(1024).decode()

    if resultado == 'acertou':
        messagebox.showinfo("Resposta Correta", "Parabéns! Você acertou :) !")
    elif resultado == 'errou':
        messagebox.showinfo("Resposta Incorreta", "Você perdeu o jogo :( !")
        client_socket.close()
        root.destroy()
        return

    atualizar_pergunta()

def atualizar_pergunta():
    pergunta, opcoes, fim_de_jogo = pickle.loads(client_socket.recv(1024))

    if fim_de_jogo:
        messagebox.showinfo("Parabéns!", "Você venceu o jogo :) !")
        client_socket.close()
        root.destroy()
        return

    pergunta_label.config(text=pergunta)
    for i, opcao in enumerate(opcoes):
        opcoes_radiobuttons[i].config(text=opcao)

HOST = '127.0.0.1'
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.title("Quiz Tech")
root.geometry("700x600")

pergunta_label = tk.Label(root, text="", font=("Arial", 14))
pergunta_label.pack(pady=20)

resposta_var = tk.StringVar()
opcoes_radiobuttons = []
for i in range(4):
    opcao_radiobutton = tk.Radiobutton(root, text="", variable=resposta_var, value=i+1, font=("Arial", 12))
    opcao_radiobutton.pack(pady=5)
    opcoes_radiobuttons.append(opcao_radiobutton)

enviar_button = tk.Button(root, text="Enviar Resposta", command=enviar_resposta, font=("Arial", 12), bg="lightblue")
enviar_button.pack(pady=20)

atualizar_pergunta()

root.mainloop()
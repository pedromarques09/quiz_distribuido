import socket
import pickle
import threading

HOST = '127.0.0.1'
PORT = 1234

connected_clients = []

def handle_client(client_socket, addr):
    try:
        perguntas = [
            ("Qual empresa lançou o primeiro processador?", ["1 - IBM", "2 - AMD", "3 - Intel", "4 - Motorola"], 3),
            ("Qual foi o primeiro sistema de correio eletrônico?", ["1 - ARPANET Mail", "2 - Gmail", "3 - Hotmail", "4 - Yahoo Mail"], 1),
            ("Qual é o nome da linguagem de programação desenvolvida pela Microsoft?", ["1 - Python", "2 - C++", "3 - Java", "4 - C#"], 4),
            ("Qual é o protocolo de internet utilizado para acessar páginas web?", ["1 - FTP", "2 - HTTP", "3 - TCP", "4 - IP"], 2),
            ("Qual é o nome da tecnologia que permite a conexão de dispositivos\n à internet por meio de ondas de rádio?", ["1 - Wi-Fi", "2 - Ethernet", "3 - Bluetooth", "4 - 3G/4G/5G"], 4),
            ("Que ano foi lançado o Macintosh?", ["1 - 1980", "2 - 1982", "3 - 1984", "4 - 1986"], 3)
        ]
        acertos = 0

        for pergunta, opcoes, resposta_correta in perguntas:
            client_socket.send(pickle.dumps((pergunta, opcoes, False)))

            resposta_cliente = int(client_socket.recv(1024).decode())

            if resposta_cliente == resposta_correta:
                acertos += 1
                client_socket.send('acertou'.encode())
            else:
                client_socket.send('errou'.encode())
                break

        if acertos == 5:
            client_socket.send(pickle.dumps(("Você acertou todas as perguntas!", [], True)))
        else:
            client_socket.send(pickle.dumps(("Fim de Jogo", [], True)))
    except ConnectionResetError:
        print('Cliente desconectado:', addr)
    finally:
        client_socket.close()
        connected_clients.remove((client_socket, addr))
        print('Clientes conectados:', len(connected_clients))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    print('Aguardando conexões dos clientes...')

    while True:
        client_socket, addr = server_socket.accept()
        print('Cliente conectado:', addr)
        connected_clients.append((client_socket, addr))
        print('Clientes conectados:', len(connected_clients))

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

start_server()
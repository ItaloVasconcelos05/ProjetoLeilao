from concurrent.futures import thread
import socket
import threading
from time import sleep

HOST = '127.0.0.1'
PORTA = 55555

def receive_message(client_socket):
    while True:
        try:
            server_response = client_socket.recv(1024).decode('utf-8')
            if server_response:
                print(f"{server_response}")
            else:
                print("[!] O servidor fechou a conexão.")
                break
        except Exception as e:
            print(f"[!] Ocorreu um erro: {e}")
            client_socket.close()
            break

def send_message(client_socket):
    while True:
        send_message = input("\n [#] Escreva sua mensagem: ")
        client_socket.send(send_message.encode('utf-8'))
        sleep(1)
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORTA))
        print(f"[*] Conectando ao servidor em {HOST}:{PORTA}")
    except ConnectionRefusedError:
        print("[!] Não foi possível conectar ao servidor. Verifique se ele está rodando.")
        return 

    thread_receive = threading.Thread (
        target = receive_message,
        args = (client_socket,)
    )
    thread_receive.start()

    send_message(client_socket)



if __name__ == "__main__":
    start_client()
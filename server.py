from concurrent.futures import thread
import socket
import threading
import os

HOST = '127.0.0.1'
PORTA = 55555

def client_management(client_connection, client_address):
    print(f"\n[NOVA CONEXÃO] {client_address} conectado")
    
    try:
        while True:
            data_received = client_connection.recv(1024).decode('utf-8')
            if not data_received:
                break
            
            print(f" \n[{client_address}]: {data_received} [*]")

            send_response = f"\nServidor recebeu: {data_received}"
            client_connection.send(send_response.encode('utf-8'))

    except Exception as e:
        print(f"\n[!] Erro com {client_address}: {e}")

    finally:
        client_connection.close()
        print(f"\n[CONEXÃO ENCERRADA] {client_address}.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORTA))
    server_socket.listen()
    print(f"--- Servidor escutando em {HOST}:{PORTA} ---")

    while True:
        client_connection, client_address =  server_socket.accept()
        
        thread_client = threading.Thread(
            target = client_management,
            args=(client_connection, client_address)
        )
        thread_client.start()

        print(f"\n[CONEXÕES ATIVAS] {threading.active_count() - 1}")



if __name__ == "__main__":
    start_server()
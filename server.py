import socket
import string
import threading

active_clients = []

client_lock = threading.Lock()

HOST = '127.0.0.1'
PORTA = 55555

def broadcast(message: str, connection_sender):
    with client_lock:
        offline_client = []
        for client_socket in active_clients:
            if client_socket != connection_sender:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    offline_client.append(client_socket)

        for client in offline_client:
            active_clients.remove(client)


def client_management(client_connection, client_address):
    print(f"\n[NOVA CONEXÃO] {client_address} conectado")
    
    with client_lock:
        active_clients.append(client_connection)

    try:
        while True:
            data_received = client_connection.recv(1024).decode('utf-8')
            if not data_received:
                break
            
            message = f"\n[{client_address}]: {data_received}\n"
            print(message)
            broadcast(message, client_connection)

    except Exception as e:
        print(f"\n[!] Erro com {client_address}: {e}")

    finally:
        with client_lock:
            active_clients.remove(client_connection)

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
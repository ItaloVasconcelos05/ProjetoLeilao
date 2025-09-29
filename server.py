import socket

HOST = '127.0.0.1'
PORTA = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORTA))
server_socket.listen()

print(f"--- Servidor escutando em {HOST}:{PORTA} ---")
print("[...] Aguardando uma conexão [...]")

client_connection, client_address =  server_socket.accept()

print(f"\n[+] Conexão aceita de {client_address} [+]")
data_received = client_connection.recv(1024).decode('utf-8')

print(f" \n[*] Mensagem recebida: {data_received} [*]")

send_response = "Recebido!"
client_connection.send(send_response.encode('utf-8'))
client_connection.close()

print(f"\n[-] Conexão com {client_address} encerrada. [-]")


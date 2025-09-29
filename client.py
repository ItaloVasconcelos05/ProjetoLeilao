import socket

HOST = '127.0.0.1'
PORTA = 55555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORTA))
print(f"[*] Conectando ao servidor em {HOST}:{PORTA}")

send_message = 'Olá, mundo!'
client_socket.send(send_message.encode('utf-8'))

server_response = client_socket.recv(1024).decode('utf-8')
print(f"\n[*] Resposta do servidor: {server_response}")

client_socket.close()
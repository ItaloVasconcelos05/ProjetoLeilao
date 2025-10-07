import socket
import threading

class Auction:
    def __init__(self, item_name, bid, broadcast_callback):

        self.item_name = item_name
        self.bid = bid
        self.bidder = "Ninguém"
        self.status = True
        self.timer = None
        self.time_limit = 30.0
        self.lock = threading.Lock()
        self.broadcast_callback = broadcast_callback

    def placeBid (self, bid_amount, new_bidder):
        with self.lock:
            if not self.status:
                return (False, "Leilão encerrado")

            if bid_amount > self.bid:
                self.bid = bid_amount
                self.bidder = new_bidder

                if self.timer:
                    self.timer.cancel()
                self.timer = threading.Timer(self.time_limit, self.close)
                self.timer.start()

                message = f"\n[NOVO LANCE] R${self.bid:.2f} por {self.bidder}"
                return (True, message)
            else:
                message = f"\nSeu lance de R${bid_amount} não é maior que o lance de R${self.bid} atual"
                return (False, message)

    def getStatus(self):
        with self.lock:
            return f"\nItem: {self.item_name}\nLance Atual: R${self.bid}\nArrematante: {self.bidder}"

    def close(self):
        with self.lock:
            if not self.status:
                return
            self.status = False
        final_message = f"\n[LEILÃO ENCERRADO] Vencedor: {self.bidder} com lance de R${self.bid}"
        print(final_message)
        self.broadcast_callback(final_message,None)

def broadcast(message: str, connection_sender):
    with client_lock:
        offline_client = []
        for client_socket in active_clients.keys():
            if client_socket != connection_sender:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    offline_client.append(client_socket)

        for client in offline_client:
            active_clients.remove(client)
# ========================================================== #

active_clients = {}
client_lock = threading.Lock()
HOST = '127.0.0.1' 
PORTA = 55555
house_auction = Auction("Casa", 100, broadcast_callback=broadcast)

# ========================================================== #


def client_management(client_connection, client_address):
    try:
        username = client_connection.recv(1024).decode('utf-8')
        print(f"\n[NOVA CONEXÃO] {client_address} se conectou como {username}")
    
        with client_lock:
            active_clients[client_connection] = username

        broadcast(f"\n --- {username} entrou no leilão ---", client_connection)
        client_connection.send(f"\n[LEILÃO ABERTO] {house_auction.getStatus()}".encode('utf-8'))

        while True:
            data_received = client_connection.recv(1024).decode('utf-8')
            if not data_received:
                break
            
            try:
                new_bid = float(data_received)
                bidder_id = active_clients[client_connection]

                status, message = house_auction.placeBid(new_bid, bidder_id)

                if status:
                    print(f"[LEILÃO] {message}")
                    client_connection.send(f"[LANCE ACEITO] Parabéns! Seu lance de {new_bid} foi aceito com sucesso".encode('utf-8'))
                    broadcast(message, client_connection) 
                else:
                    client_connection.send(message.encode('utf-8'))
            except ValueError:
                client_connection.send("[ERRO] Envie apenas números como lance".encode('utf-8'))

    except Exception as e:
        print(f"\n[!] Erro com {client_address}: {e}")

    finally:
        with client_lock:
            if client_connection in active_clients:
                username = active_clients[client_connection]
                del active_clients[client_connection]
                broadcast(f"\n --- {username} saiu do leilão ---")

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
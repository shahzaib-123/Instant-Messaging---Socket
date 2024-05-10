import socket
import threading

def client_thread(conn, addr, clients):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                message=addr[0]+" : "+message
                print(f"{addr}: {message}")
                for client in clients:
                    if client != conn:
                        client.sendall(message.encode())
        except:
            conn.close()
            clients.remove(conn)
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(2)
    
    clients = []
    print("Server is listening for connections...")
    
    while True:
        client_conn, client_addr = server_socket.accept()
        print(f"Connected to {client_addr}")
        clients.append(client_conn)
        threading.Thread(target=client_thread, args=(client_conn, client_addr, clients)).start()

if __name__ == "__main__":
    main()

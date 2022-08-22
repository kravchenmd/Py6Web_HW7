import socket

TCP_IP = '192.168.0.187'  # from `get_ip()` of server
TCP_PORT = 5000


def run_client(ip: str, port: int):
    with socket.socket() as sock:
        server = ip, port
        client_socket = socket.socket()
        client_socket.connect(server)
        print(f"Connection with server @ {server} was established")
        message = input('--> ')
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        while data != 'OK':
            data = client_socket.recv(1024).decode()
            if not data:
                print("ERROR: connection was closed, but `OK` wasn't received!")
                return
        print(data)
    print(f"Connection with server was closed")


if __name__ == '__main__':
    run_client(TCP_IP, TCP_PORT)

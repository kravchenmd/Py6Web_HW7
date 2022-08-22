import os
import socket
from concurrent import futures as cf

# From Stack Overflow (modernized)
# For Linux
if os.name != "nt":
    import fcntl
    import struct


    def get_interface_ip(if_name):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                                            struct.pack('256s', if_name[:15]))[20:24])


def get_ip():
    ip = socket.gethostbyname(socket.gethostname())

    # For Linux
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
        for if_name in interfaces:
            try:
                ip = get_interface_ip(if_name)
                break
            except IOError:
                pass
    return ip


def run_server(ip, port):
    def handle(sock: socket.socket, addr: str):
        print(f'Connection with {addr} created')
        while True:
            data = sock.recv(1024).decode()
            if not data:
                break

            print(f'Received message form {sock.getsockname()}: {data}')
            while not (message := input('--> ')):
                print("Enter not empty message!")
            sock.send(message.encode())

    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f'Start server @ {server_socket.getsockname()}')
    with cf.ThreadPoolExecutor(5) as client_pool:
        try:
            while True:
                new_sock, address = server_socket.accept()
                client_pool.submit(handle, new_sock, address)
        except KeyboardInterrupt:
            print(f"Server stopped")
        finally:
            server_socket.close()


if __name__ == '__main__':
    TCP_IP = get_ip()
    TCP_PORT = 5000
    run_server(TCP_IP, TCP_PORT)

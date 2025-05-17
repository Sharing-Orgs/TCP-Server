# 2 - Client initiates a connection
import socket

HOST, PORT = '127.0.0.1', 3392

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # 3 - Data is exchanged
    s.sendall(b"Hello, world")
    data = s.recv(1024)
    print(f"Received {data!r}")
    s.close()
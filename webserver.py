import socket 
import sys
from typing import Tuple

ENCODING: str = "ISO-8859-1"

def server(port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        address: Tuple[str, int] = ('', port)
        s.bind(address)
        print(f"Server started @port:{port}")
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn: 
                print(f"{addr} joined server.")
                request: bytes = b""
                buffer: bytes = b""
                while True:
                    byte = conn.recv(1)
                    if not byte: 
                        break # no more data incoming 
                    buffer += byte 
                    if buffer.endswith(b"\r\n"): # empty buffer
                        if buffer == b"\r\n": # means buffer was empty line
                            break
                        request += buffer
                        buffer = b""
                print(request)
                data: str = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 13\r\n"
                    "\r\n"
                    "Hello, world!\r\n"
                    "\r\n"
                )
                conn.sendall(data.encode())
                

if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) == 2:
        if len(sys.argv) == 1:
           port: int = 8000
        else:

           port: int = int(sys.argv[1])
        server(port)
    else: 
        print("Usage: python webclient.py <port>[optional]")
        sys.exit(1)
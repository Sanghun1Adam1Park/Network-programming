import socket 
import sys
from typing import Tuple, List

ENCODING: str = "ISO-8859-1"

def server(port: int) -> None:
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
                method: str = request.decode(ENCODING).split(" ")[0]
                print(f"HTTP Method: {method}")
                if method != "GET":
                    lines: List[str] = request.decode(ENCODING).split("\r\n")
                    length: int = 0
                    for line in lines:
                        if "content-length" in line.lower():
                            length = int(line.split(":")[1].strip())

                    payload: bytes = b""
                    while len(payload) < length:
                        chunk: bytes = conn.recv(length - len(payload))
                        if not chunk:
                            break
                        payload += chunk
                    print(payload.decode(ENCODING))

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
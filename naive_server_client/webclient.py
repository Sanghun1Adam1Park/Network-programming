import socket 
from typing import Tuple
import sys  
from dotenv import load_dotenv

ENCODING: str = "ISO-8859-1"

def get(address: str, port: int) -> str:
    ip: str = socket.gethostbyname(address)
    ip_addr: Tuple[str, int] = (ip, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect(ip_addr)
        request: str = (
            "GET / HTTP/1.1\r\n"
            f"Host: {address}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        s.sendall(request.encode(ENCODING))
        response: bytes = b""
        buffer: bytes = b""
        while True:
            byte = s.recv(1)
            if not byte:
                break # no more data incoming 
            buffer += byte
            if buffer.endswith(b"\r\n"): # empty buffer
                if buffer == b"\r\n": # means buffer was empty line
                    continue
                response += buffer
                buffer = b""
        
    return response.decode(ENCODING)

def post(address: str, port: int, payload: str, content_type: str="text/pain") -> None:
    ip: str = socket.gethostbyname(address)
    ip_addr: Tuple[str, int] = (ip, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect(ip_addr)
        request: str = (
            "POST / HTTP/1.1\r\n"
            f"Host: {address}\r\n"
            "Connection: close\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(payload.encode(ENCODING))}\r\n"
            "\r\n"
            f"{payload}\r\n"
            "\r\n"
        )
        s.sendall(request.encode(ENCODING))

if __name__ == "__main__":
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        address: str = sys.argv[1]
        if len(sys.argv) == 2:
            port: int = 80
        else:
            port: int = int(sys.argv[2]) 
        response = get(address, port)
        print(response)
        post(address, port, "Hello, Server")
    else: 
        print("Usage: python webclient.py <address> <port>[optional]")
        sys.exit(1)
    
import socket
import os
import mimetypes

ENCODING: str = "ISO-8859-1"
HOST = '127.0.0.1'
PORT: int = 8000

# TODO: extention and mime 
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started @{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            with conn:
                request: bytes = b""
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    request += data
                    if b"\r\n\r\n" in request:
                        break

                # Stringfy the request
                decoded_req: str = request.decode(ENCODING)
                print(f"Recieved request:\n{decoded_req}")

                # Get header
                header: str = decoded_req.split("\r\n")[0]

                # Get filename for security
                # Since allowing whole path can cause data leak
                filename: str = os.path.split(header.split(" ")[1])[-1]
                path: str = os.path.join("./better_server/files", filename)

                response_header: bytes = b""
                response_payload: bytes = b""
                mime_type: bytes = b""
                if not os.path.isfile(path):
                    response_header = b"HTTP/1.1 404 Not Found"
                    response_payload = b"404 not found"
                    mime_type = b"text/plain"
                else:
                    response_header = b"HTTP/1.1 200 OK"
                    mime_type = (
                        mimetypes.guess_type(path)[0].encode(ENCODING) or b"application/octet-stream"
                    )
                    with open(path, "rb") as f:
                        response_payload = f.read()
                length: bytes = str(len(response_payload)).encode(ENCODING)

                # Build response 
                response: bytes = (
                    response_header + b"\r\n" +
                    b"Content-Type: " + mime_type + b"\r\n" +
                    b"Content-Length: " + length + b"\r\n" +
                    b"Connection: close\r\n" +
                    b"\r\n" +
                    response_payload
                )

                # Send response 
                conn.sendall(response)
                print(f"Sent response:\n{response.decode(ENCODING)}")
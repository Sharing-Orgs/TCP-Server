import socket
import json
import os
HOST, PORT = '0.0.0.0', 3396

def send_http_response(connection_socket, status_code="200 OK", content_type="text/html", body=""):
    if isinstance(body, dict) and content_type == "application/json":
        body_bytes = json.dumps(body, indent=2).encode()
    elif isinstance(body, bytes):
        body_bytes = body
    else:
        body_bytes = str(body).encode()
    
    headers = f"HTTP/1.1 {status_code}\r\n"
    headers += f"Content-Type: {content_type}\r\n"
    headers += f"Content-Length: {len(body_bytes)}\r\n"
    headers += "Connection: close\r\n\r\n"
    connection_socket.sendall(headers.encode() + body_bytes)

def get_file_response(filepath):
    """
    Reads a file and returns its content and content type based on file extension.

    Returns:
        (content_type, content)
    Raises:
        FileNotFoundError if the file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError("File not found")

    extension = os.path.splitext(filepath)[1]
    if extension == ".html":
        with open(filepath, "r") as f:
            content = f.read()
        content_type = "text/html"

    elif extension == ".json":
        with open(filepath, "r") as f:
            json_data = json.load(f)
        content = json.dumps(json_data, indent=2)
        content_type = "application/json"

    elif extension in [".jpg", ".jpeg", ".png", ".gif", ".pdf"]:
        with open(filepath, "rb") as f:
            content = f.read()
        content_type = "application/octet-stream"

    else:
        with open(filepath, "r") as f:
            content = f.read()
        content_type = "text/plain"

    return content_type, content

listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listeningSocket.bind((HOST, PORT))
listeningSocket.listen(1)
print(f'Server is running on http://{HOST}:{PORT}')
while True:
    connection, clientAddress = listeningSocket.accept()  # Accept connection
    print(f"Connected by {clientAddress}")
    try:
        data = connection.recv(1024).decode()  #Receive HTTP request
        filename = data.split()[1].lstrip("/")
        if filename != "":
            content_type, content = get_file_response(filename)
            send_http_response(connection, "200 OK", content_type, body=content)
        else:
            send_http_response(connection, "200 OK", body="Accessed server successfully")
    
    except FileNotFoundError:
        send_http_response(connection, "404 Not Found",  body= "404 Not Found")

    except Exception as e:
        print("Server error: ", e)
        send_http_response(connection, "500 Internal Server Error", body={"message": e, "status":"internal server error"})

    finally:
        connection.close()

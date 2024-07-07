import socket, uuid, os, requests
from datetime import datetime
url = 'http://127.0.0.1:8000/update/'

def send_image():


    files = os.listdir('images')
    for file in files:
        path = os.path.join('images', file)
        # Abre el archivo en modo binario y asegúrate de cerrarlo después
        with open(path, "rb") as image_file:
            # Crea un diccionario para los archivos que se enviarán en la solicitud
            files = {"file": (path, image_file, "images/jpeg")}
            
            # Realiza la solicitud POST
            response = requests.post(url, files=files)
        os.remove(path)
        # Muestra la respuesta del servidor
        print(response.json())

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Server started at {ip_address}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'images/image_{timestamp}_{unique_id}.jpeg'
        with open(filename, 'wb') as f:
            while True:
                conn.settimeout(2)
                data = conn.recv(1024)
                if not data:
                    break
                
                f.write(data)
        
        conn.close()
        print(f"Image received and saved as {filename}")
        send_image()
        

if __name__ == "__main__":
    start_server()

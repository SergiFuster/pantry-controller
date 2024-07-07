import socket, uuid, os, requests
from datetime import datetime
server_url = 'http://127.0.0.1:8000/update/'
controller_url = 'http://127.0.0.1:6000/'

path = 'middle/images'
def send_image():


    files = os.listdir(path)
    for file in files:
        image_path = os.path.join(path, file)
        # Abre el archivo en modo binario y asegúrate de cerrarlo después
        with open(image_path, "rb") as image_file:
            # Crea un diccionario para los archivos que se enviarán en la solicitud
            files = {"file": (image_path, image_file, "images/jpeg")}
            
            # Realiza la solicitud POST
            requests.post(server_url, files=files)
        os.remove(image_path)

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    requests.post(controller_url, json={"message" : f"-- MIDDLEWARE : Started at {ip_address}:{port}"})

    while True:
        conn, addr = server_socket.accept()
        requests.post(controller_url, json={"message" : f"-- MIDDLEWARE : Connection from {addr}"})
        unique_id = uuid.uuid4()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{path}/image_{timestamp}_{unique_id}.jpeg'
        with open(filename, 'wb') as f:
            while True:
                conn.settimeout(2)
                data = conn.recv(1024)
                if not data:
                    break
                
                f.write(data)
        
        conn.close()
        requests.post(controller_url, json={"message" : "-- MIDDLEWARE : Sending image to server."})
        send_image()

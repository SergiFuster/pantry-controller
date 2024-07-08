import utime as time
import socket
import sys
import network
import urequests as requests
import ujson as json
from machine import Pin
from Wifi import Sta
import camera

HOST = '192.168.1.83'
PORT = 5000
WIFI_SSID = ''
WIFI_PASSWORD = ''
REQUEST_INTERVAL = 45

# Configura la red Wi-Fi
def connect_wifi(ssid, password):
    wifi = Sta(WIFI_SSID, WIFI_PASSWORD)
    wifi.connect()
    wifi.wait()


def capture_image():
    
    try:
        print('Capturing image...')
        return camera.capture()
    except Exception as e:
        raise e
 
def connect_socket(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'Trying to connect socket at {server_ip}:{server_port}...')
    sock.connect((server_ip, server_port))
    return sock
    
def send_image(image, sock):
    
    print('Sending image...')
    try:
        sock.sendall(image)
        print("Image sent successfully")
    except OSError as e:
        print("Failed to send image:", e)


def connect_camera():
    cam = False
    while not cam:
        cam = camera.init()
        print("Camera ready?: ", cam)

    return cam


def configure_camera():
    # set preffered camera setting
    camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
    camera.contrast(2)       # increase contrast
    camera.speffect(2)       # jpeg
    
    
def wait_for(seconds):
    start = time.time()
    elapsed = time.time() - start
    last = seconds
    while elapsed < seconds:
        elapsed = int(time.time() - start)
        if int(elapsed) != last:
            last = int(elapsed)
            print(f"Waiting for {seconds - last} seconds")
        
        
def main():
    
    cam = connect_camera()
    configure_camera()

    # Conectar a la red Wi-Fi
    connect_wifi(WIFI_SSID, WIFI_PASSWORD)
    
    # Bucle principal
    sock = None
    while True:
        try:
            image = capture_image()
            if not image: raise Exception("No image captured!")
            sock = connect_socket(HOST, PORT)
            send_image(image, sock)
        except Exception as e:
            print(e)
            
        if sock: sock.close()
        
        wait_for(REQUEST_INTERVAL)

# if __name__ == '__main__':
main()

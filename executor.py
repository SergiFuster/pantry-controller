import uvicorn, os
from middle.middle import start_server
import threading
from controller.app import app as controller
def run_server():
    uvicorn.run("server-iot.app.server:app", host="127.0.0.1", port=8000, reload=True, log_level="warning")

def run_controller():
    controller.run(host='127.0.0.1', port=6000)
if __name__ == "__main__":
    
    print("Starting flask server...")
    controller_thread = threading.Thread(target=run_controller)
    controller_thread.start()

    print("Starting middleware server...")
    middleware_thread = threading.Thread(target=start_server)
    middleware_thread.start()
    
    print("Starting fastapi server...")
    run_server()

    
    

    

from flask import Flask, request
import logging

# Crea una instancia de la aplicación Flask
app = Flask(__name__)
# Configurar el nivel de logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route('/', methods=['POST'])
def show_message():
    # Extrae el mensaje del cuerpo de la solicitud
    data = request.json
    message = data.get('message', '')

    # Imprime el mensaje en la consola
    print(f"-- CONTROLLER : {message}")

    # Devuelve una respuesta
    return "Mensaje recibido y registrado."

if __name__ == "__main__":
    app.run(port=5000, debug=True)

# Run
1. Create a venv with ```python -venv name-venv```
2. Activate the venv with ```./name-venv/Scripts/activate```
3. Install dependencies with ```pip install -r requeriments.txt ```
4. Download Ollama.
5. Install llava model.
6. Load xiao files to your IoT device.
7. Modify parameters on Wifi.py (ssid and pswd) with your data.
8. Be sure that your IoT device and you middleware connects on the same subnet.
9. Take de ip of you middleware and put it on constant "HOST" on myapp.py script.
10. Run executor.py
11. Run myapp.py script.

If all went well you should check the ingredients and recipes generated on https://127.0.0.1:8000/data/ on your browser.

# Executor.py
Automates the execution of 3 differents server:
1. Controller server with flask, its the merging point where all other running programs will send messages in order to centralize debug information all in one.
2. Middleware socket who receives an image and resend it to the 3. server.
3. Server with FastAPI which extracts ingredients in json format from the image and extract food recipes from ingredients json, all with Ollama model like Llava.


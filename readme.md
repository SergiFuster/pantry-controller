1. Create a venv with ```python -venv name-venv```
2. Activate the venv with ```./name-venv/Scripts/activate```
3. Install dependencies with ```pip install -r requeriments.txt ```
4. Run executor.py

# Executor.py
Automates the execution of 3 differents server:
1. Controller server with flask, its the merging point where all other running programs will send messages in order to centralize debug information all in one.
2. Middleware socket who receibes an image and resend it to the 3. sever.
3. Server with FastAPI which extracts ingredients in json format from the image and extract food recipes from ingredients json, all with Ollama model like Llava.


from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .model.model import Model
import os, json, requests
from datetime import datetime
app = FastAPI()

model = Model()
templates = Jinja2Templates(directory="server-iot/app/templates")
data = "server-iot/app/data"
controller_url = 'http://127.0.0.1:6000/'


@app.post("/update/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    try:
        # Lee el archivo de imagen
        contents = await file.read()
        requests.post(controller_url, json={"message" : f"-- SERVER : Image received."})
        data_directory = os.path.join(data, datetime.now().strftime('%Y%m%d%H%M%S'))
        file_path = os.path.join(data_directory, "image.jpg")
        # Crear el directorio si no existe
        os.makedirs(data_directory, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(contents)

        def update_info(file_path):
            
            requests.post(controller_url, json={"message" : f"-- SERVER : Processing ingredients..."})
            ingredients = model.identify_items(file_path)
            requests.post(controller_url, json={"message" : f"-- SERVER : Ingredients processed."})

            if ingredients == "": ingredients = '{"nothing" : "found"}'
            ingredients_path = os.path.join(data_directory, "ingredients.json")
            with open(ingredients_path, "w") as f:
                f.write(ingredients)
            requests.post(controller_url, json={"message" : f"-- SERVER : Processing recipes..."})

            recipes = model.food_recipes(ingredients)
            requests.post(controller_url, json={"message" : f"-- SERVER : Recipes processed."})
            recipes_path = os.path.join(data_directory, "recipes.json")
            with open(recipes_path, "w") as f:
                f.write(recipes)
            

        # Process the image in the background to avoid blocking the request
        background_tasks.add_task(update_info, file_path)
        
        return JSONResponse(content={"message": "Image upload started"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@app.get("/data/")
async def get_data(request : Request):

    # Obtener una lista de los nombres de los subdirectorios
    subdirectorios = [nombre for nombre in os.listdir(data) if os.path.isdir(os.path.join(data, nombre))]

    # Ordenar los nombres de los subdirectorios numéricamente de mayor a menor
    subdirectorios_ordenados = sorted(subdirectorios, key=lambda x: int(x), reverse=True)

    data_directory = os.path.join(data, subdirectorios_ordenados[0])

    print(data_directory)
    try:
        ingredients_path = os.path.join(data_directory, "ingredients.json")
        with open(ingredients_path, "r") as file:
            ingredients = json.load(file)
        recipes_path = os.path.join(data_directory, "recipes.json")
        with open(recipes_path, "r") as file:
            recipes = json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Renderiza la plantilla con los datos
    return templates.TemplateResponse("index.html", {"request": request, "ingredients": ingredients, "recipes" : recipes})
    
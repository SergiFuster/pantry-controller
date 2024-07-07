from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .model.model import Model
import os, json
app = FastAPI()

model = Model()
data_directory = "server-iot/app/static"
app.mount("/static", StaticFiles(directory="server-iot/app/static"), name="static")
templates = Jinja2Templates(directory="server-iot/app/templates")


@app.post("/update/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    try:
        # Lee el archivo de imagen
        contents = await file.read()
        file_path = os.path.join(data_directory, "image.jpg")
        
        with open(file_path, "wb") as f:
            f.write(contents)

        def update_info(file_path):
            ingredients = model.identify_items(file_path)
            if ingredients == "": ingredients = '{"nothing" : "found"}'
            ingredients_path = os.path.join(data_directory, "ingredients.json")
            with open(ingredients_path, "w") as f:
                f.write(ingredients)
            recipes = model.food_recipes(ingredients)
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
     # Datos que se pasarán a la plantilla
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
    return templates.TemplateResponse("index.html", {"request": request, "ingredients": ingredients, "recipes" : recipes, "image_url" : "/static/image.jpg"})
    
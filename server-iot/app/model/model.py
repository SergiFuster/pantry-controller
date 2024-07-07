from langchain_community.llms.ollama import Ollama
from . import utils as u
# import utils as u
from PIL import Image
from langchain_core.prompts.prompt import PromptTemplate
import json

class Model:
    def __init__(self):
        self.prompt_1 = PromptTemplate(
            template= "With the image binded you have you count all the elements in the image and tell me how many are there. \
            Format all responses as JSON objects with a key for every different element and the value as the count of that element."
        )
        self.prompt_2 = PromptTemplate(
            input_variables=["ingredients"],
            template="With this ingredients: {ingredients}, I want you to give me between 1 and 3 differents food recipes. \
                Format all responses as JSON objects as {{recipe name : description}}."
        )

    def identify_items(self, file_path) -> json:
        
        model = Ollama(model="llava", format="json", temperature=0)
        pil_image = Image.open(file_path)
        image_b64 = u.convert_to_base64(pil_image)
        llm_with_image_context = model.bind(images=[image_b64])
        response = llm_with_image_context.invoke(self.prompt_1.format())
        return response
    
    def food_recipes(self, data):
        model = Ollama(model="llama3", format="json", temperature=1)
        response = model.invoke(self.prompt_2.format(ingredients=data))
        return response
    
if __name__ == "__main__":
    cheff = Model()
    with open("app/static/info.json", "r") as f:
            data = f.read()
    print(cheff.food_recipes(data))
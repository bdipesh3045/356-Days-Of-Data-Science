from urllib import response
#Define the schema
from pydantic import BaseModel, Field
from flask import Flask,request
from google import genai
from google.genai import types

# Intializing the GenAI client with API key
api="AIzaSyAE0F2sKMlI2DU6qHcsZtmKoxVpK8EAG2I"

client = genai.Client(api_key=api)
app = Flask(__name__)



class Finder(BaseModel):
    recycle: bool = Field(
        description=(
            "Indicates whether the image contains a person placing or disposing items "
            "into a recycling bin or dustbin. Return True if someone is actively "
            "recycling or throwing waste into a bin; otherwise, return False."
        )
    )

prompt="""You are an AI agent that analyzes images to determine whether a person is 
disposing or recycling items into a bin. Carefully inspect the image and decide 
if someone is placing, throwing, or depositing any object into a dustbin or 
recycling bin. If such an action is clearly visible, return true. If the image 
does not show this activity, return false."""

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            
            image_bytes = file.read()

            response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
                ),
                prompt
            ],
            config={
            "response_mime_type": "application/json",
            "response_json_schema": Finder.model_json_schema(),
            },
            )
            print("Pass1")
            return response.text
    return "Image processing Error"




if __name__ == "__main__":
    app.run(debug=True)

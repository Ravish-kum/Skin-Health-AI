import base64

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import numpy as np
from PIL import Image
from io import BytesIO
import os

import tensorflow
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from fastapi.staticfiles import StaticFiles

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -------------------------------
# Build Model Architecture
# -------------------------------
def build_densenet():

    base_model = DenseNet121(
        weights=None,   # IMPORTANT → weights will be loaded from file
        include_top=False,
        input_shape=(240,240,3)
    )

    model = Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(9, activation='sigmoid')
    ])

    return model

# -------------------------------
# Load Weights
# -------------------------------
MODEL_PATH = os.path.join("model", "skin_disease_model.h5")

model = build_densenet()
model.load_weights(MODEL_PATH)

print("Model loaded successfully")

# -------------------------------
# Class Names
# -------------------------------
class_names = [
    "Actinic Keratosis",
    "Atopic Dermatitis",
    "Benign Keratosis",
    "Dermatofibroma",
    "Melanocytic Nevus",
    "Melanoma",
    "Squamous Cell Carcinoma",
    "Tinea Ringworm Candidiasis",
    "Vascular Lesion"
]

# -------------------------------
# Image Preprocessing
# -------------------------------
IMG_SIZE = 240

def read_image(file_bytes):
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img).astype("float32") / 255.0
    return np.expand_dims(img_array, axis=0)

# -------------------------------
# Treatments
# -------------------------------
common_treatments = [
    "Keep the affected skin clean and dry",
    "Avoid scratching or irritating the area",
    "Apply broad-spectrum sunscreen daily",
    "Consult a dermatologist for a professional biopsy or skin check"
]

specific_treatments = {
    "Actinic Keratosis": ["Cryotherapy", "Topical creams", "Photodynamic therapy"],
    "Atopic Dermatitis": ["Moisturization", "Topical steroids", "Avoid triggers"],
    "Benign Keratosis": ["No treatment usually needed", "Cryotherapy"],
    "Dermatofibroma": ["Observation", "Surgical removal if painful"],
    "Melanocytic Nevus": ["Monitoring", "Removal if suspicious"],
    "Melanoma": ["Immediate excision", "Oncology consult"],
    "Squamous Cell Carcinoma": ["Surgery", "Radiation"],
    "Tinea Ringworm Candidiasis": ["Antifungal creams"],
    "Vascular Lesion": ["Laser therapy", "Observation"]
}

# -------------------------------
# Routes
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/skincheckup", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):

    try:
        if not file or file.filename == "":
            return templates.TemplateResponse(
                "home.html",
                {
                    "request": request,
                    "error": "⚠️ Please upload an image"
                }
            )

        img_bytes = await file.read()
        img_array = read_image(img_bytes)
    
        encoded_image = base64.b64encode(img_bytes).decode("utf-8")
        file_extension = file.filename.split(".")[-1]
        image_data = f"data:image/{file_extension};base64,{encoded_image}"

        preds = model.predict(img_array)

        class_idx = int(np.argmax(preds))
        confidence = float(preds[0][class_idx])

        prediction = class_names[class_idx]

        return templates.TemplateResponse(
            "home.html",   
            {
                "request": request,
                "prediction": prediction,
                "probability": round(confidence * 100, 2),
                "common_treatments": common_treatments,
                "specific_treatments": specific_treatments.get(prediction, []),
                "image_data": image_data
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "error": str(e)}
        )
    
# -------------------------------
# Run server (for debugging)
# -------------------------------
def main():
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    main()
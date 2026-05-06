import os
import numpy as np
from PIL import Image
from io import BytesIO

import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

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

IMG_SIZE = 240

def read_image(file_bytes):
    img = Image.open(BytesIO(file_bytes)).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img).astype("float32") / 255.0
    return np.expand_dims(img_array, axis=0)

def build_densenet():
    base_model = DenseNet121(
        weights=None,
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

MODEL_PATH = os.path.join("model", "skin_disease_model.h5")
model = build_densenet()
model.load_weights(MODEL_PATH)
print("ML Model loaded successfully")

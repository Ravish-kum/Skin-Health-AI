import os
import uuid
import base64
import numpy as np
from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import database
import models
from utils.dependencies import templates
from utils.ml_model import model, class_names, read_image, common_treatments, specific_treatments

router = APIRouter()

@router.get("/skincheckup", response_class=HTMLResponse)
async def home(request: Request):
    user_name = request.session.get('user_name')
    return templates.TemplateResponse("home.html", {"request": request, "user_name": user_name})

@router.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    try:
        if not file or file.filename == "":
            return templates.TemplateResponse(
                "home.html",
                {"request": request, "error": "⚠️ Please upload an image"}
            )

        img_bytes = await file.read()
        img_array = read_image(img_bytes)
    
        encoded_image = base64.b64encode(img_bytes).decode("utf-8")
        file_extension = file.filename.split(".")[-1]
        image_data = f"data:image/{file_extension};base64,{encoded_image}"

        filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join("static", "uploads", filename)
        with open(filepath, "wb") as f:
            f.write(img_bytes)

        user_id = request.session.get('user_id')
        new_upload = models.ImageUpload(image_path=filepath, user_id=user_id)
        db.add(new_upload)
        db.commit()
        db.refresh(new_upload)

        preds = model.predict(img_array)
        class_idx = int(np.argmax(preds))
        confidence = float(preds[0][class_idx])
        prediction = class_names[class_idx]

        new_diagnosis = models.Diagnosis(
            disease_name=prediction,
            confidence_score=confidence,
            image_id=new_upload.image_id
        )
        db.add(new_diagnosis)
        db.commit()

        return templates.TemplateResponse(
            "home.html",   
            {
                "request": request,
                "prediction": prediction,
                "probability": round(confidence * 100, 2),
                "common_treatments": common_treatments,
                "specific_treatments": specific_treatments.get(prediction, []),
                "image_data": image_data,
                "diagnosis": new_diagnosis,
                "user_name": request.session.get('user_name')
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "error": str(e)}
        )

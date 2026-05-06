from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

import database
import models
from utils.dependencies import templates
from utils.llm_service import get_llm

router = APIRouter()

class ChatMessageReq(BaseModel):
    diagnosis_id: int
    message: str

@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, diagnosis_id: int = None, db: Session = Depends(database.get_db)):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    if not user_id:
        return RedirectResponse(url="/signup", status_code=303)
    
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    history = []
    if user and user.image_uploads:
        for upload in user.image_uploads:
            if upload.diagnosis:
                history.append({
                    "id": upload.diagnosis.diagnosis_id,
                    "date": upload.diagnosis.diagnosis_date.strftime("%b %d, %Y"),
                    "disease": upload.diagnosis.disease_name
                })
    history.sort(key=lambda x: x["id"], reverse=True)
    
    chat_history = []
    selected_diagnosis = None
    
    if diagnosis_id:
        selected_diagnosis = db.query(models.Diagnosis).filter(models.Diagnosis.diagnosis_id == diagnosis_id).first()
        if selected_diagnosis and selected_diagnosis.image_upload.user_id == user_id:
            chats = db.query(models.AIChat).filter(models.AIChat.diagnosis_id == diagnosis_id).order_by(models.AIChat.timestamp.asc()).all()
            
            if not chats:
                try:
                    model = get_llm()
                    prompt = f"You are an expert AI Dermatologist. The patient has been diagnosed with {selected_diagnosis.disease_name}. Provide a concise, numbered list of steps to help cure or manage it. Be professional and empathetic."
                    
                    response = model.generate_content(prompt)
                    try:
                        bot_text = response.text.strip()
                    except Exception as e:
                        print(f"Gemini error (possibly safety block): {e}")
                        bot_text = "I'm here to help, but I'm unable to generate a response for this specific query due to safety guidelines. Please try rephrasing or consult a medical professional."
                    
                    new_chat = models.AIChat(
                        diagnosis_id=diagnosis_id,
                        message="", 
                        response=bot_text
                    )
                    db.add(new_chat)
                    db.commit()
                    db.refresh(new_chat)
                    chats = [new_chat]
                except Exception as e:
                    print("LLM Error:", e)
                    chats = [models.AIChat(message="", response="Hello! I am your AI Dermatologist. How can I assist you with your diagnosis? (Error loading LLM: " + str(e) + ")")]
                    
            for c in chats:
                if c.message:
                    chat_history.append({"sender": "user", "text": c.message})
                if c.response:
                    chat_history.append({"sender": "bot", "text": c.response})

    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "user_name": user_name,
        "history": history,
        "chat_history": chat_history,
        "selected_diagnosis": selected_diagnosis
    })

@router.post("/chat/message")
async def send_chat_message(req: ChatMessageReq, request: Request, db: Session = Depends(database.get_db)):
    user_id = request.session.get('user_id')
    if not user_id:
        return {"error": "Unauthorized"}
        
    diag = db.query(models.Diagnosis).filter(models.Diagnosis.diagnosis_id == req.diagnosis_id).first()
    if not diag or diag.image_upload.user_id != user_id:
        return {"error": "Forbidden"}
        
    chats = db.query(models.AIChat).filter(models.AIChat.diagnosis_id == req.diagnosis_id).order_by(models.AIChat.timestamp.asc()).all()
    messages = [
        {"role": "system", "content": f"You are an expert AI Dermatologist assisting a patient diagnosed with {diag.disease_name}. Be helpful, concise, and professional."}
    ]
    for c in chats:
        if c.message:
            messages.append({"role": "user", "content": c.message})
        if c.response:
            messages.append({"role": "assistant", "content": c.response})
            
    messages.append({"role": "user", "content": req.message})
    
    try:
        model = get_llm()
        
        # Build a conversation context for Gemini
        context = f"System: You are an expert AI Dermatologist assisting a patient diagnosed with {diag.disease_name}. Be helpful, concise, and professional.\n\n"
        for c in chats:
            if c.message:
                context += f"User: {c.message}\n"
            if c.response:
                context += f"AI: {c.response}\n"
        
        context += f"User: {req.message}\nAI:"
        
        response = model.generate_content(context)
        try:
            bot_text = response.text.strip()
        except Exception as e:
            print(f"Gemini error (possibly safety block): {e}")
            bot_text = "I'm sorry, I cannot answer that question right now. It might be due to safety filters or a technical issue. Please try a different question."
        
        new_chat = models.AIChat(
            diagnosis_id=req.diagnosis_id,
            message=req.message,
            response=bot_text
        )
        db.add(new_chat)
        db.commit()
        
        return {"response": bot_text}
    except Exception as e:
        return {"error": str(e)}

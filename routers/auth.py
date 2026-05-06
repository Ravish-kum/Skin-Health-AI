from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import database
import models
from utils.dependencies import templates, oauth

router = APIRouter()

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(None),
    age: int = Form(None),
    gender: str = Form(None),
    db: Session = Depends(database.get_db)
):
    try:
        new_user = models.User(
            name=name,
            email=email,
            password=password,
            phone=phone,
            age=age,
            gender=gender
        )
        db.add(new_user)
        db.commit()
        return templates.TemplateResponse("signup.html", {"request": request, "success": "Account created successfully! You can now proceed."})
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("signup.html", {"request": request, "error": f"Error creating account: {str(e)}"})

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(database.get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            return templates.TemplateResponse("signup.html", {"request": request, "error": "Failed to get user info from Google."})
        
        email = user_info.get("email")
        name = user_info.get("name")
        
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            user = models.User(name=name, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            
        request.session['user_id'] = user.user_id
        request.session['user_name'] = user.name
        
        return RedirectResponse(url="/chat", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": f"Google Auth Error: {str(e)}"})

@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    return RedirectResponse(url="/signup", status_code=303)

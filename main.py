from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Database.database import User, get_db_session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

app = FastAPI()
templates = Jinja2Templates(directory="Auth")
pass_hash = PasswordHasher()

def hash_password(password: str) -> str:
    return pass_hash.hash(password)

def verify_password(stored_password: str, provided_password: str) -> bool:
    try:
        return pass_hash.verify(stored_password, provided_password)
    except VerifyMismatchError:
        return False

# Signup routes
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "message": "Username or email already exists!"})
    
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("signup.html", {"request": request, "message": "User registered successfully!"})

# Login routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(user.password, password):
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials!"})
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": f"Welcome {user.username}!"})

# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

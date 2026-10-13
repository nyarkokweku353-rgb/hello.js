from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Database.database import User, get_db_session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "user": None})

@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "message": "Username or email already exists!"})

    if (
        len(password) < 8
        or not re.search(r"\d", password)
        or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        raise HTTPException(
            status_code=400,
            detail="Password must have at least 8 characters, one digit, and one special character."
        )
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("signup.html", {"request": request, "message": "User registered successfully!"})

# Login routes
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(user.password, password):
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid credentials!"})
    return RedirectResponse(url="/dashboard", status_code=303)

# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

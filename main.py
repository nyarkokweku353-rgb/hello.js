from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from Database.database import User, get_db_session, Student
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
def get_student_data_on_dashboard(request:Request,  db: Session = Depends(get_db_session)):
    students = db.query(Student).all()
    return templates.TemplateResponse("dashboard.html", {"request":request, "students": students})

#Data route
@app.post("/data", response_class=HTMLResponse)
def create_student_data(request:Request, studentname : str = Form(...), studentage : str = Form(...), studentclass : str = Form(...), parentname : str = Form(...), parentcontact : str = Form(...), db: Session = Depends(get_db_session)):
    new_student_record = Student(studentname=studentname, studentage=studentage, studentclass=studentclass, parentname=parentname, parentcontact=parentcontact)
    db.add(new_student_record)
    db.commit()
    return templates.TemplateResponse("data.html", {"request":request, "msg":"Successfully created!"})

@app.delete("/data", response_class=HTMLResponse)
def remove_student_data(request:Request, studentname : str = Form(...), db: Session = Depends(get_db_session)):
    student = db.query(Student).filter(Student.studentname == studentname).first()
    if student:
        db.delete(student)
        db.commit()
        msg = "Removed successsfully!"
    else:
        msg = f"{studentname}does not exsist"
        return templates.TemplateResponse("data.html", {"request":request, "msg":msg})

@app.put("/data", response_class=HTMLResponse)
def update_student_data(request:Request, studentname : str = Form(...), studentage : str = Form(...), studentclass : str = Form(...), parentname : str = Form(...), parentcontact : str = Form(...), db: Session = Depends(get_db_session)):
    student = db.query(Student).filter(Student.studentname == studentname).first()
    if student:
        student.studentage = studentage
        student.studentclass = studentclass
        student.parentname = parentname
        student.parentcontact = parentcontact
        db.commit()
        msg = "Updated successfully!"
    else:
        msg = f"{studentname} not found"
        return templates.TemplateResponse("data.html", {"request":request})


#Messaging
@app.get("/messaging", response_class=HTMLResponse)
def student_data_on_message_view(request:Request, db : Session = Depends(get_db_session)):
    student = db.query(Student).all()
    return templates.TemplateResponse("messaging.html",{"request" : request, "student":student})
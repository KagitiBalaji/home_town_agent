from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import SessionLocal, engine
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Local Bus Agent API",
    description="API for bus timings and user registration",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/buses")
async def get_buses(q: str):
    """Search buses by route name (supports fuzzy matching)"""
    results = utils.search_buses(q)
    return results

@app.get("/register", response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=RedirectResponse)
async def handle_registration(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return RedirectResponse("/register?error=Email+already+registered", status_code=303)
    
    # Create new user
    new_user = models.User(name=name, email=email, phone=phone)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse("/success", status_code=303)

@app.get("/success", response_class=HTMLResponse)
async def registration_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

# Admin endpoint to view registrations (add authentication in production)
@app.get("/admin/registrations", response_class=HTMLResponse)
async def view_registrations(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users
    })

@app.get("/courses", response_class=HTMLResponse)
async def show_courses(request: Request):
    return templates.TemplateResponse("courses.html", {"request": request})

@app.get("/course-register", response_class=HTMLResponse)
async def course_registration_form(request: Request):
    return templates.TemplateResponse("course_register.html", {"request": request})

@app.post("/course-register", response_class=RedirectResponse)
async def handle_course_registration(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    db: Session = Depends(get_db)
):
    # Optional: Check if already registered
    new_reg = models.CourseRegistration(name=name, email=email, phone=phone, course=course)
    db.add(new_reg)
    db.commit()
    return RedirectResponse("/success-course", status_code=303)

@app.get("/success-course", response_class=HTMLResponse)
async def course_success(request: Request):
    return templates.TemplateResponse("success_course.html", {"request": request})

@app.get("/admin/course-registrations", response_class=HTMLResponse)
async def view_course_regs(request: Request, db: Session = Depends(get_db)):
    course_users = db.query(models.CourseRegistration).order_by(models.CourseRegistration.created_at.desc()).all()
    return templates.TemplateResponse("admin_course.html", {
        "request": request,
        "users": course_users
    })


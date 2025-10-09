from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db
import models, crud, schemas
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import httpx
from fastapi.responses import RedirectResponse

# NEW imports for Google ID token verification
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

load_dotenv()

# -------------------------------
# App init
# -------------------------------
app = FastAPI(
    title="Payroll & HR Management API",
    description="Flexible Payroll Management System",
    version="1.0.0",
)

# -------------------------------
# CORS config for React dev servers
# -------------------------------
origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Security settings
# -------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------
# Auth models
# -------------------------------
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

# -------------------------------
# Dependency: get current user
# -------------------------------
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

# -------------------------------
# Root
# -------------------------------
@app.get("/")
async def root():
    return {"message": "Payroll API is running!"}

# -------------------------------
# User authentication
# -------------------------------
@app.post("/login/")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    user = await crud.get_user_by_username(db, req.username)
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    created_user = await crud.create_user(db, user)
    return created_user

@app.get("/users/me/", response_model=schemas.UserRead)
async def read_users_me(current_user: schemas.UserRead = Depends(get_current_user)):
    return current_user

# -------------------------------
# Google OAuth
# -------------------------------
@app.get("/auth/google/login")
async def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(url=google_auth_url)

@app.get("/auth/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_async_db)):
    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data=data)
        token_resp.raise_for_status()
        tokens = token_resp.json()
        id_token_str = tokens.get("id_token")

        if not id_token_str:
            raise HTTPException(status_code=400, detail="No id_token returned by Google")

        # Verify ID token using google-auth (this fetches Google's public keys automatically)
        try:
            payload = google_id_token.verify_oauth2_token(
                id_token_str,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Google ID Token")

        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Google account has no email")

        # Check if user exists
        user = await crud.get_user_by_username(db, email)
        if not user:
            # Create user automatically with a random password (not used for Google users)
            user_in = schemas.UserCreate(username=email, email=email, password=os.urandom(12).hex())
            user = await crud.create_user(db, user_in)

        # Create JWT for our app
        access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Redirect to frontend callback route with token
    frontend_url = f"http://localhost:5173/auth/google/callback?token={access_token}"
    return RedirectResponse(url=frontend_url)

# -------------------------------
# Organisations
# -------------------------------
@app.post("/organisations/", response_model=schemas.OrganisationOut, status_code=status.HTTP_201_CREATED)
async def create_organisation(org: schemas.OrganisationCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_organisation(db, org)

@app.get("/organisations/{org_id}", response_model=schemas.OrganisationOut)
async def get_organisation(org_id: int, db: AsyncSession = Depends(get_async_db)):
    org = await crud.get_organisation(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org

# -------------------------------
# Employees
# -------------------------------
@app.post("/employees/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: schemas.EmployeeCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_employee(db, emp)

@app.get("/employees/{emp_id}", response_model=schemas.EmployeeOut)
async def get_employee(emp_id: int, db: AsyncSession = Depends(get_async_db)):
    emp = await crud.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# -------------------------------
# Departments
# -------------------------------
@app.post("/departments/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
async def create_department(dept: schemas.DepartmentCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_department(db, dept)

@app.get("/departments/{dept_id}", response_model=schemas.DepartmentOut)
async def get_department(dept_id: int, db: AsyncSession = Depends(get_async_db)):
    dept = await crud.get_department(db, dept_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

# -------------------------------
# Designations
# -------------------------------
@app.post("/designations/", response_model=schemas.DesignationOut, status_code=status.HTTP_201_CREATED)
async def create_designation(desig: schemas.DesignationCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_designation(db, desig)

@app.get("/designations/{desig_id}", response_model=schemas.DesignationOut)
async def get_designation(desig_id: int, db: AsyncSession = Depends(get_async_db)):
    desig = await crud.get_designation(db, desig_id)
    if not desig:
        raise HTTPException(status_code=404, detail="Designation not found")
    return desig

# -------------------------------
# Payroll
# -------------------------------
@app.post("/payroll/", response_model=schemas.PayrollOut, status_code=status.HTTP_201_CREATED)
async def create_payroll_record(payroll: schemas.PayrollCreate, db: AsyncSession = Depends(get_async_db)):
    return await crud.create_payroll_record(db, payroll)

@app.get("/payroll/{record_id}", response_model=schemas.PayrollOut)
async def get_payroll_record(record_id: int, db: AsyncSession = Depends(get_async_db)):
    record = await crud.get_payroll_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return record

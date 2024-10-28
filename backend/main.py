from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import users_collection, get_database
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

app = FastAPI(title="FencerLunge API")

# Use this to get the database connection in your route handlers
db = get_database()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key for JWT
SECRET_KEY = "your-secret-key"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to FencerLunge API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/register")
async def register_user(user: UserCreate):
    # Check if username already exists
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create new user document
    new_user = user.dict()
    new_user["password"] = hashed_password
    new_user["_id"] = ObjectId()  # Generate a new ObjectId
    
    # Insert the new user into the database
    result = users_collection.insert_one(new_user)
    
    # Check if insertion was successful
    if result.inserted_id:
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.post("/upload-video")
async def upload_video(
    video: UploadFile = File(...),
    experience: str = Form(...),
    notes: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Create user-specific directory
        user_upload_dir = os.path.join(UPLOAD_DIR, str(current_user["_id"]))
        os.makedirs(user_upload_dir, exist_ok=True)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{video.filename}"
        filepath = os.path.join(user_upload_dir, filename)

        # Save the video file
        with open(filepath, "wb") as buffer:
            content = await video.read()
            buffer.write(content)

        # Save video metadata to database
        video_metadata = {
            "user_id": current_user["_id"],
            "filename": filename,
            "original_filename": video.filename,
            "filepath": filepath,
            "experience_level": experience,
            "notes": notes,
            "upload_date": datetime.utcnow(),
            "status": "uploaded"  # You can update this status during processing
        }
        
        db.videos.insert_one(video_metadata)

        return {
            "message": "Video uploaded successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

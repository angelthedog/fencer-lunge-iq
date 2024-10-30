import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from database import users_collection, get_database
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel
from bson import ObjectId
import deepmotion_api

# Load environment variables
load_dotenv()

# Get SECRET_KEY from environment variable
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/upload-video")
async def upload_video(
    video: UploadFile = File(...),
    experience: str = Form(...),
    notes: str = Form(...)
):
    try:
        # Create user-specific directory
        user_upload_dir = os.path.join(UPLOAD_DIR, str(ObjectId()))
        os.makedirs(user_upload_dir, exist_ok=True)

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{video.filename}"
        filepath = os.path.join(user_upload_dir, filename)

        # Save the video file
        with open(filepath, "wb") as buffer:
            content = await video.read()
            buffer.write(content)

        # Initialize DeepMotion session
        session = deepmotion_api.get_session()

        # Upload video to DeepMotion
        gcs_url = deepmotion_api.upload_video(session, filepath)

        # Start new job
        rid = deepmotion_api.start_new_job(session, gcs_url)

        # Wait for job to complete
        job_status = deepmotion_api.check_job_status(session, rid)
        while job_status["status"] == "PROGRESS":
            time.sleep(5)
            job_status = deepmotion_api.check_job_status(session, rid)

        if job_status["status"] == "SUCCESS":
            bvh_url = next(
                (path for path in job_status['details']['out'] if path.endswith("male-young.bvh")), 
                None
            )
            
            # Download male-young.bvh file
            if bvh_url:
                deepmotion_api.download_job_by_rid(session, rid)
                # bvh_content = deepmotion_api.download_bvh(session, bvh_url)
                # print("bvh_content", bvh_content)

                # # Save BVH content to MongoDB
                # bvh_id = db.bvh_files.insert_one({"content": bvh_content}).inserted_id

                # # Save video metadata to database
                # video_metadata = {
                #     "user_id": ObjectId(),
                #     "filename": filename,
                #     "original_filename": video.filename,
                #     "filepath": filepath,
                #     "experience_level": experience,
                #     "notes": notes,
                #     "upload_date": datetime.utcnow(),
                #     "status": "processed",
                #     "deepmotion_rid": rid,
                #     "bvh_file_id": bvh_id
                # }
                # db.videos.insert_one(video_metadata)

                return {
                    "message": "Video uploaded and processed successfully",
                    "filename": filename,
                    "deepmotion_rid": rid,
                    "bvh_file_id": str(rid)
                }
            else:
                raise Exception("male-young.bvh file URL not found in job status response")
        else:
            raise Exception(f"Job failed with status: {job_status['status']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

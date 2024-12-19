from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os
from PIL import Image
from db_config import init_db
from db_operations import insert_image_pair, get_image_pair, get_recent_image_pairs

app = FastAPI()

# Initialize the database connection at application startup.
@app.on_event("startup")
async def startup_event():
    init_db()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173" # Allow requests from the specified origin (local development).
    ],
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST etc.) for cross-origin requests.
    allow_headers=["*"],
)

# Define the directory for uploaded files, creating it if it doesn't exist.
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

@app.post("/api/upload")
async def upload_images(
    original: UploadFile = File(...),
    mask: UploadFile = File(...)
):
    try:
        # Save original image
        original_filename = f"{os.urandom(8).hex()}_{original.filename}" # Generate a unique filename.
        original_path = os.path.join(UPLOAD_DIR, original_filename)
        with open(original_path, "wb") as buffer:
            content = await original.read()
            buffer.write(content)
            file_size = len(content)
        
        # Get image dimensions
        with Image.open(original_path) as img:
            width, height = img.size
        
        # Save mask image
        mask_filename = f"{os.urandom(8).hex()}_{mask.filename}" # Generate a unique filename.
        mask_path = os.path.join(UPLOAD_DIR, mask_filename)
        with open(mask_path, "wb") as buffer:
            content = await mask.read()
            buffer.write(content)
        
        # Prepare information for saving to database
        original_info = {
            'filename': original_filename,
            'path': original_path,
            'file_size': file_size,
            'width': width,
            'height': height
        }
        
        mask_info = {
            'filename': mask_filename,
            'path': mask_path
        }
        
        # Insert image pair information into the database and retrieve its ID
        pair_id = insert_image_pair(original_info, mask_info)
        
        if pair_id:
            return {
                "id": pair_id,
                "message": "Images uploaded successfully", 
                "original_path": f"http://localhost:8000/images/{original_filename}", # URL to access the original image.
                "mask_path": f"http://localhost:8000/images/{mask_filename}" # URL to access the masked image.
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save to database")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
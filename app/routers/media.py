from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid
from app.config import settings
from app.auth import check_role

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(check_role("editor"))
):
    if file.content_type not in settings.get_allowed_mime_types():
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    if file.size > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.media_upload_path, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(settings.media_upload_path, exist_ok=True)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"id": unique_filename, "url": f"/api/media/{unique_filename}"}

@router.get("/{file_id}")
async def get_file(file_id: str):
    file_path = os.path.join(settings.media_upload_path, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)
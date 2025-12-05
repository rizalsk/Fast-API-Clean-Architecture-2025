import logging
from fastapi import UploadFile, File
import uuid
import os
from app.dependencies.logger import log

UPLOAD_DIR = "app/assets/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileService:
    @staticmethod
    async def doUpload(file: UploadFile = File(None), prefix: str = "", sub_dir: str = ""):
        if file is not None:
            filename = f"{prefix}{uuid.uuid4()}_{file.filename}"
            base_path = f"{UPLOAD_DIR}{sub_dir}"
            file_path = os.path.join( base_path, filename)
            os.makedirs(base_path, exist_ok=True)

            # Save file to disk
            with open(file_path, "wb") as f:
                f.write(await file.read())
            # Return desired info
            return {
                "filename": file.filename,
                "file_path": file_path
            }
        return None
    
    @staticmethod
    async def deleteFile(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"Deleted file: {file_path}")
        
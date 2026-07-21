import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import get_settings

settings = get_settings()

UPLOAD_DIR = Path(settings.upload_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}


def save_upload_file(upload_file: UploadFile, subfolder: str = "users/avatar") -> str:
    """保存上传文件，返回可访问的URL路径"""
    # 检查文件大小
    upload_file.file.seek(0, 2)
    file_size = upload_file.file.tell()
    upload_file.file.seek(0)

    if file_size > settings.max_upload_size:
        raise ValueError(f"文件大小超过限制 {settings.max_upload_size / 1024 / 1024}MB")

    # 检查文件类型
    ext = Path(upload_file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {ext}")

    if upload_file.content_type and upload_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"不支持的文件类型: {upload_file.content_type}")

    # 创建子目录
    target_dir = UPLOAD_DIR / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    # 生成唯一文件名
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = target_dir / unique_name

    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())

    # 返回相对路径，用于URL
    return f"/static/{subfolder}/{unique_name}"

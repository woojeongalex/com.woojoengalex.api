"""이미지 업로드 → (파일명, 바이트) (무상태 파싱)."""

from fastapi import HTTPException, UploadFile


async def read_vision_upload(file: UploadFile) -> tuple[str, bytes]:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")
    return file.filename or "upload.jpg", data

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

import json

from app.controllers.pdf_controller import upload_pdf

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

@router.post("/upload")
async def upload(

    file: UploadFile = File(...),

    config: str = Form(...)
):

    try:

        parsed_config = json.loads(config)

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid config JSON"
        )

    return await upload_pdf(
        file=file,
        config=parsed_config
    )
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

import json

from app.controllers.excel_controller import upload_excel

router = APIRouter(
    prefix="/excel",
    tags=["Excel"]
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

    return await upload_excel(
        file=file,
        config=parsed_config
    )
from app.services.pdf_service import process_pdf


async def upload_pdf(
    file,
    config
):

    file_bytes = await file.read()

    result = process_pdf(

        file_bytes=file_bytes,

        expected_headers=config[
            "expected_headers"
        ],

        header_mapping=config[
            "header_mapping"
        ]
    )

    return {
        "success": True,
        "data": result
    }
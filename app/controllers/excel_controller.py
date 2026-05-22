from app.services.excel_service import process_excel


async def upload_excel(
    file,
    config
):

    file_bytes = await file.read()

    result = process_excel(

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
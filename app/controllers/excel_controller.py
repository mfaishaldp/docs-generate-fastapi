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
        ],

        sheet_name=config.get(
            "sheet_name"
        ),

        sheet_names=config.get(
            "sheet_names"
        ),

        footer_keywords=config.get(
            "footer_keywords"
        ),

        min_data_cells=config.get(
            "min_data_cells",
            2
        ),

        min_filled_ratio=config.get(
            "min_filled_ratio",
            0.6
        ),

        max_single_cell_chars=config.get(
            "max_single_cell_chars",
            60
        ),

        outlier_trim_enabled=config.get(
            "outlier_trim_enabled",
            True
        ),

        outlier_similarity_threshold=config.get(
            "outlier_similarity_threshold",
            40
        ),

        outlier_max_ratio=config.get(
            "outlier_max_ratio",
            0.6
        ),

        outlier_min_columns=config.get(
            "outlier_min_columns",
            2
        )
    )

    return {
        "success": True,
        "data": result
    }
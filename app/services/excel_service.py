import pandas as pd
from io import BytesIO
from openpyxl import load_workbook

from app.utils.header_detector import detect_header_row
from app.utils.header_mapper import normalize_headers
from app.utils.table_cleaner import clean_table


def process_excel(
    file_bytes,
    expected_headers,
    header_mapping
):

    workbook = load_workbook(
        filename=BytesIO(file_bytes),
        data_only=True
    )

    all_results = []

    # LOOP EACH SHEET
    for sheet_name in workbook.sheetnames:

        worksheet = workbook[sheet_name]

        raw_rows = []

        # READ ALL ROWS
        for row in worksheet.iter_rows(values_only=True):

            raw_rows.append(
                list(row)
            )

        # CLEAN TABLE
        cleaned_table = clean_table(
            raw_rows
        )

        if len(cleaned_table) == 0:
            continue

        # DETECT HEADER ROW
        header_index = detect_header_row(
            cleaned_table,
            expected_headers
        )

        if header_index is None:
            continue

        # GET RAW HEADERS
        raw_headers = cleaned_table[
            header_index
        ]

        # NORMALIZE HEADERS
        normalized_headers = normalize_headers(
            raw_headers,
            header_mapping
        )

        # GET DATA ROWS
        rows = cleaned_table[
            header_index + 1:
        ]

        valid_rows = []

        for row in rows:

            # skip fully empty row
            if all(
                str(cell).strip() == ""
                for cell in row
            ):
                continue

            valid_rows.append(row)

        if len(valid_rows) == 0:
            continue

        # ====================================
        # REMOVE INVALID / EMPTY HEADERS
        # ====================================

        filtered_headers = []
        filtered_indexes = []

        for idx, header in enumerate(
            normalized_headers
        ):

            # SKIP NONE HEADER
            if header is None:
                continue

            # SKIP EMPTY HEADER
            if str(header).strip() == "":
                continue

            filtered_headers.append(
                header
            )

            filtered_indexes.append(
                idx
            )

        # SKIP IF NO VALID HEADERS
        if len(filtered_headers) == 0:
            continue

        # ====================================
        # FILTER ROW VALUES
        # ====================================

        filtered_rows = []

        for row in valid_rows:

            cleaned_row = []

            for idx in filtered_indexes:

                if idx < len(row):

                    value = row[idx]

                    # HANDLE NONE
                    if value is None:
                        value = ""

                    cleaned_row.append(
                        str(value).strip()
                    )

                else:

                    cleaned_row.append("")

            filtered_rows.append(
                cleaned_row
            )

        # ====================================
        # CREATE DATAFRAME
        # ====================================

        df = pd.DataFrame(
            filtered_rows,
            columns=filtered_headers
        )

        # ====================================
        # REMOVE DUPLICATE COLUMNS
        # ====================================

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]

        # ====================================
        # REPLACE EMPTY STRING -> None
        # ====================================

        df = df.replace(
            r'^\s*$',
            None,
            regex=True
        )

        # ====================================
        # DROP ROWS WHERE
        # ALL VALUES ARE EMPTY
        # ====================================

        df = df.dropna(
            how="all"
        )

        # ====================================
        # OPTIONAL:
        # REMOVE KEYS WITH NONE VALUE
        # ====================================

        records = df.to_dict(
            orient="records"
        )

        cleaned_records = []

        for record in records:

            cleaned_record = {

                key: value

                for key, value in record.items()

                if value not in [None, ""]
            }

            # skip object if empty
            if len(cleaned_record) == 0:
                continue

            cleaned_records.append(
                cleaned_record
            )

        all_results.extend(
            cleaned_records
        )

    return all_results
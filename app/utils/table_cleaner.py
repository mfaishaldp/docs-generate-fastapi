def clean_table(table):

    cleaned = []

    for row in table:

        if row is None:
            continue

        filtered = []

        for cell in row:

            if cell is None:
                filtered.append("")
            else:
                filtered.append(
                    str(cell).strip()
                )

        # skip fully empty row
        if all(cell == "" for cell in filtered):
            continue

        cleaned.append(filtered)

    return cleaned
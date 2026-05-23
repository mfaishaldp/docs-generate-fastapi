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


def trim_table_rows(
    rows,
    footer_keywords=None,
    min_data_cells=2,
    expected_columns=None,
    min_filled_ratio=0.6,
    max_single_cell_chars=60
):

    if footer_keywords is None:
        footer_keywords = [
            "total",
            "subtotal",
            "grand total",
            "jumlah",
            "total harga",
            "total amount",
            "note",
            "notes",
            "catatan",
            "keterangan",
            "remark"
        ]

    def _norm_cell(cell):
        if cell is None:
            return ""
        return str(cell).strip().lower()

    def _non_empty_count(row):
        return sum(
            1
            for cell in row
            if str(cell).strip() != ""
        )

    def _row_text(row):
        return " ".join(
            _norm_cell(cell)
            for cell in row
            if str(cell).strip() != ""
        )

    end = len(rows)

    while end > 0:

        row = rows[end - 1]

        if row is None:
            end -= 1
            continue

        non_empty = _non_empty_count(row)

        if non_empty == 0:
            end -= 1
            continue

        row_text = _row_text(row)

        if any(
            keyword in row_text
            for keyword in footer_keywords
        ):
            end -= 1
            continue

        if non_empty < min_data_cells:
            end -= 1
            continue

        if expected_columns:
            filled_ratio = non_empty / expected_columns
            if filled_ratio < min_filled_ratio:
                end -= 1
                continue

        if non_empty == 1 and len(row_text) >= max_single_cell_chars:
            end -= 1
            continue

        break

    return rows[:end]


def filter_outlier_rows(
    rows,
    min_columns=2,
    similarity_threshold=40,
    max_outlier_ratio=0.6
):

    try:
        from rapidfuzz import fuzz
    except Exception:
        return rows

    def _norm(value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def _pattern(value):
        text = _norm(value)
        if text == "":
            return ""
        pattern = []
        for ch in text:
            if ch.isdigit():
                pattern.append("9")
            elif ch.isalpha():
                pattern.append("a")
            else:
                pattern.append(ch)
        return "".join(pattern)

    if not rows:
        return rows

    column_patterns = []

    column_count = max(len(row) for row in rows)

    for col in range(column_count):
        patterns = []
        for row in rows:
            if col >= len(row):
                continue
            pattern = _pattern(row[col])
            if pattern:
                patterns.append(pattern)
        if not patterns:
            column_patterns.append("")
            continue
        pattern_counts = {}
        for pattern in patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        dominant = max(pattern_counts.items(), key=lambda item: item[1])[0]
        column_patterns.append(dominant)

    filtered = []

    for row in rows:
        comparisons = 0
        outliers = 0
        for col, dominant_pattern in enumerate(column_patterns):
            if dominant_pattern == "":
                continue
            if col >= len(row):
                continue
            cell_pattern = _pattern(row[col])
            if cell_pattern == "":
                continue
            comparisons += 1
            similarity = fuzz.ratio(
                cell_pattern,
                dominant_pattern
            )
            if similarity < similarity_threshold:
                outliers += 1

        if comparisons < min_columns:
            filtered.append(row)
            continue

        if outliers / comparisons <= max_outlier_ratio:
            filtered.append(row)

    return filtered
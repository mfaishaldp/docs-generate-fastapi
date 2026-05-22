from rapidfuzz import fuzz

def detect_header_row(
    table,
    expected_headers
):

    best_row = None
    best_score = 0

    for idx, row in enumerate(table):

        score = 0

        for cell in row:

            if cell is None:
                continue

            cell = str(cell).lower()

            for expected in expected_headers:

                similarity = fuzz.partial_ratio(
                    cell,
                    expected.lower()
                )

                if similarity > 80:
                    score += 1

        if score > best_score:
            best_score = score
            best_row = idx

    return best_row
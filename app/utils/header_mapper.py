from rapidfuzz import fuzz

SIMILARITY_THRESHOLD = 80

def normalize_single_header(
    header,
    header_mapping
):

    best_match = header
    best_score = 0

    for standard_name, variations in header_mapping.items():

        for variation in variations:

            score = fuzz.partial_ratio(
                str(header).lower(),
                variation.lower()
            )

            if score > best_score:
                best_score = score
                best_match = standard_name

    if best_score < SIMILARITY_THRESHOLD:
        return None

    return best_match

def normalize_headers(
    headers,
    header_mapping
):

    return [
        normalize_single_header(
            header,
            header_mapping
        )
        for header in headers
    ]
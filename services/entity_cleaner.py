import re
from collections import Counter

BAD_TERMS = {
"house",
"news",
"sky news",
"bbc",
"cnn",
"reuters",
"pcr",
"live updates",
"breaking"
}

ALIASES = {
"donald trump": "Donald Trump",
"trump": "Donald Trump",
"labour": "Labour Party",
"the labour party": "Labour Party"
}

def clean_entity(text):
    if not text:
        return None


    text = text.strip()

    text = re.sub(r"\(.*", "", text)
    text = re.sub(r"[^A-Za-z0-9\s&\-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < 4:
        return None

    low = text.lower()

    if low in BAD_TERMS:
        return None

    if low in ALIASES:
        return ALIASES[low]

    return text


def top_entities(entities, limit=8):
    cleaned = []

    for e in entities:
        x = clean_entity(e)

        if x:
            cleaned.append(x)

    return [
        x[0]
        for x in Counter(cleaned).most_common(limit)
    ]
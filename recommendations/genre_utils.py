COMBINED_SCIFI_FANTASY = "Science-Fiction & Fantastique"

FANTASY_KEYWORDS = [
    "magie", "magique", "dragon", "sorcier", "sorciere", "elfe", "royaume",
    "prophetie", "epee", "sortilege", "reine", "trone", "guerrier", "demon",
    "creature", "legende", "quete",
]

SCIFI_KEYWORDS = [
    "espace", "extraterrestre", "robot", "futur", "vaisseau", "intelligence artificielle",
    "cyborg", "planete", "galaxie", "technologie", "clone", "androide", "spatial",
    "mutant", "laboratoire", "experience",
]


def strip_accents(text):
    replacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a",
        "î": "i", "ï": "i",
        "ô": "o",
        "û": "u", "ù": "u",
        "ç": "c",
    }
    for accented, plain in replacements.items():
        text = text.replace(accented, plain)
    return text


def split_scifi_fantasy(genres, synopsis):
    if COMBINED_SCIFI_FANTASY not in (genres or []):
        return genres or []

    text = strip_accents((synopsis or "").lower())
    has_fantasy = any(kw in text for kw in FANTASY_KEYWORDS)
    has_scifi = any(kw in text for kw in SCIFI_KEYWORDS)

    result = [g for g in genres if g != COMBINED_SCIFI_FANTASY]
    if has_fantasy:
        result.append("Fantastique")
    if has_scifi:
        result.append("Science-Fiction")
    if not has_fantasy and not has_scifi:
        result.append(COMBINED_SCIFI_FANTASY)
    return result

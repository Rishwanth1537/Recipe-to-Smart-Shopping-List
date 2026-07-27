def normalize(name):
    """
    Map known synonym spellings to one canonical key, purely for grouping
    duplicates. This NEVER changes what gets stored — it only decides
    which ingredients get merged together.
    """

    if name is None:
        return ""

    name = name.lower().strip()

    replacements = {

        "green chillies": "green chilli",
        "green chilies": "green chilli",

        "mint": "mint leaves",
        "mint leaf": "mint leaves",
        "mint leaves": "mint leaves",

        "coriander": "coriander leaves",
        "coriander leaf": "coriander leaves",
        "coriander leaves": "coriander leaves",

        "onions": "onion",
        "tomatoes": "tomato"

    }

    return replacements.get(name, name)


def merge_duplicates(ingredients):
    """
    Merge duplicate ingredients ONLY. Does not invent names, does not
    change units, does not scale quantities. If a later duplicate has a
    quantity/unit and the existing entry doesn't, the existing entry is
    filled in from it — otherwise the first-seen entry's original values
    are kept untouched.
    """

    merged = {}

    for ingredient in ingredients:

        key = normalize(
            ingredient["canonical_name"]
        )

        if key not in merged:

            merged[key] = ingredient

            continue

        old = merged[key]

        if old["quantity"] is None and ingredient["quantity"] is not None:

            old["quantity"] = ingredient["quantity"]

            old["unit"] = ingredient["unit"]

    return list(merged.values())

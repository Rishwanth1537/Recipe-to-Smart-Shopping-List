import json
import os
import re

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are a QUANTITY ESTIMATION ENGINE. Nothing more.

You are NOT an ingredient extraction engine.
You are NOT a shopping list generation engine.
You do NOT decide what ingredients belong in this recipe.

The ingredient list you are given is FINAL and ALREADY DECIDED. It was
produced by a separate extraction stage and is the single source of
truth for WHICH ingredients exist. Your only job is to decide realistic
shopping QUANTITY and UNIT values for each ingredient, scaled for the
number of people given.

You will receive a JSON array of objects, each with:
- canonical_name
- quantity (may be null)
- unit (may be null)

STRICT RULES — violating any of these makes your output unusable:

1. You MUST return exactly one output object for every canonical_name
   you were given. Same count. Same names. Same order.

2. You MUST NOT add any ingredient that was not in the input.

3. You MUST NOT remove, skip, or omit any ingredient that was in the
   input.

4. You MUST NOT rename, translate, merge, or reinterpret
   canonical_name in any way. Copy it back byte-for-byte identical to
   the input.

5. You MUST NOT invent an ingredient based on what "usually" goes into
   a dish like this. Do not infer. Do not use general cooking
   knowledge to expand the list.

6. You may ONLY decide two fields per ingredient: "quantity" and
   "unit". Nothing else.

7. Do NOT include "display_name" in your output. You were not given
   it and must not guess it.

Rounding guidance: pick realistic, purchasable shopping amounts.

Examples

Chicken, 937 grams -> 1 kg

Rice, 860 grams -> 1 kg

Curd, 430 ml -> 500 ml

Green Chillies, 11 -> 12

------------------------------------------------

Return ONLY JSON in this exact shape, one object per input
canonical_name, in the same order as given:

{
    "ingredients":[
        {
            "canonical_name":"",
            "quantity":0,
            "unit":""
        }
    ]
}

Do not return markdown.

Do not explain anything.

Return valid JSON only.
"""

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config={"temperature": 0}
)


def clean_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    text = text.strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group()

    return text


def generate_quantities(recipe_name, people, ingredients):
    """
    Update quantity/unit ONLY.

    The extraction stage is the single source of truth for WHICH
    ingredients exist and what they're called. This function never lets
    Gemini's response determine ingredient identity:

    - Gemini is only ever shown canonical_name/quantity/unit (never
      display_name), so it cannot echo back or invent a display_name.
    - The returned ingredient list is rebuilt by iterating the ORIGINAL
      `ingredients` argument. canonical_name and display_name in the
      final output always come from that original list, never from
      Gemini's response.
    - After Gemini responds, the set of canonical_names in its response
      is validated against the set of canonical_names in the input. ANY
      mismatch (missing, added, or renamed ingredient) raises an
      exception rather than silently continuing.
    """

    slim_ingredients = [
        {
            "canonical_name": ing["canonical_name"],
            "quantity": ing.get("quantity"),
            "unit": ing.get("unit"),
        }
        for ing in ingredients
    ]

    prompt = f"""
Recipe Title

{recipe_name}

People

{people}

Ingredients

{json.dumps(slim_ingredients, ensure_ascii=False, indent=2)}
"""

    response = model.generate_content(prompt)

    cleaned = clean_json(response.text)

    try:
        result = json.loads(cleaned)
    except Exception as e:
        print(response.text)
        raise ValueError(
            "Quantity generator returned invalid JSON and could not be parsed."
        ) from e

    returned_items = result.get("ingredients", [])

    scaled_by_name = {
        item.get("canonical_name"): item
        for item in returned_items
        if isinstance(item, dict)
    }

    input_names = {ing["canonical_name"] for ing in ingredients}
    output_names = set(scaled_by_name.keys())

    if input_names != output_names:
        missing = input_names - output_names
        added = output_names - input_names
        raise ValueError(
            "Quantity generator changed the ingredient set — this is not "
            "allowed. "
            f"Missing from output: {sorted(missing)}. "
            f"Unexpected in output: {sorted(added)}."
        )

    final_ingredients = []

    for ing in ingredients:

        scaled = scaled_by_name[ing["canonical_name"]]

        final_ingredients.append({
            "canonical_name": ing["canonical_name"],
            "display_name": ing["display_name"],
            "quantity": scaled["quantity"],
            "unit": scaled["unit"],
        })

    return {"ingredients": final_ingredients}

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
You are a professional cooking assistant.

You receive:

1. Recipe title
2. Recipe transcript

Your task is to create a CLEAN SHOPPING INGREDIENT LIST.

------------------------------------------------

RULES

Extract ONLY ingredients explicitly mentioned in the transcript.

Never invent ingredients.

Never infer ingredients.

Never use general cooking knowledge to add ingredients that "should"
be in a dish like this. The transcript is the ONLY source of truth.

If an ingredient is not spoken in the transcript, do not include it.

------------------------------------------------

NORMALIZE

Merge duplicates.

Examples

Chicken
చికెన్

↓

Chicken

----------------

Green Chilli
Green Chillies
పచ్చిమిరపకాయలు

↓

Green Chilli

----------------

Mint
Mint Leaves
పుదీనా ఆకులు

↓

Mint Leaves

----------------

Coriander
Coriander Leaves
కొత్తిమీర

↓

Coriander Leaves

------------------------------------------------

DO NOT INCLUDE

Fried Onion

Cooked Chicken

Marinated Chicken

Rice Water

Boiled Rice

Color Water

Masala Paste

Prepared Garnish

Anything already prepared.

------------------------------------------------

Return ONLY grocery items.

------------------------------------------------

This stage produces ONLY the ingredient list. Do not generate shopping
quantities, do not scale anything, do not reason about servings — only
report the quantity/unit exactly as mentioned in the transcript (or null
if not mentioned).

------------------------------------------------

Return ONLY JSON.

{
    "ingredients":[

        {

            "canonical_name":"",

            "display_name":"",

            "quantity":null,

            "unit":null

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


def extract_ingredients(recipe_title, transcript):

    # Only the recipe-specific content goes in the user turn now.
    # Instructions live in system_instruction, so transcript text can
    # never be mistaken for (or override) the extraction rules.
    prompt = f"""
Recipe Title:

{recipe_title}

Transcript:

{transcript}
"""

    response = model.generate_content(prompt)

    cleaned = clean_json(response.text)

    try:

        return json.loads(cleaned)

    except Exception:

        print(response.text)

        return {
            "ingredients": []
        }

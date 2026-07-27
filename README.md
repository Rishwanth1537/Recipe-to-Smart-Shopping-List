# 🛒 Recipe to Smart Shopping List

Transform any YouTube cooking recipe into a structured, editable grocery shopping list using AI.

This application automatically downloads a YouTube recipe, transcribes the audio, extracts ingredients using Large Language Models, scales quantities based on the number of servings, and presents an editable shopping list ready for future Swiggy MCP integration.

---

## 📌 Problem Statement

Cooking recipes on YouTube require users to:

- Watch the video multiple times
- Manually note ingredients
- Estimate quantities
- Adjust quantities for family size
- Search every ingredient individually on grocery platforms

This process is repetitive, time-consuming, and error-prone.

---

## 💡 Solution

Our system automates the complete workflow.

The user simply provides:

- YouTube Recipe URL
- Required Number of Servings

The application automatically:

- Downloads the recipe audio
- Converts speech into text
- Extracts ingredients using AI
- Standardizes ingredient names
- Calculates shopping quantities
- Allows the user to review and edit the shopping list
- Prepares the verified shopping list for Swiggy MCP integration

---

# ✨ Features

- 🎥 YouTube Recipe Processing
- 🎙️ Speech-to-Text using Sarvam AI
- 🤖 Ingredient Extraction using Google Gemini
- 📦 Ingredient Standardization
- 🍽️ Quantity Scaling based on servings
- ✏️ Editable Shopping List
- ✅ Ingredient Selection / Deselection
- 📊 Shopping Summary
- ⚡ Modern React Frontend
- 🚀 FastAPI Backend

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
        Enter YouTube URL
                  │
                  ▼
         React Frontend
                  │
                  ▼
            FastAPI API
                  │
                  ▼
      Download YouTube Audio
                  │
                  ▼
      Sarvam Speech-to-Text
                  │
                  ▼
      Google Gemini Extraction
                  │
                  ▼
     Ingredient Normalization
                  │
                  ▼
      Quantity Calculation
                  │
                  ▼
      Structured JSON Response
                  │
                  ▼
      Editable Shopping List
                  │
                  ▼
     Future Swiggy MCP Integration
```

---

# 🔄 Application Workflow

```
User

↓

Paste YouTube Recipe URL

↓

Select Number of Servings

↓

Generate Shopping List

↓

Download Recipe Audio

↓

Transcribe using Sarvam AI

↓

Extract Ingredients using Gemini

↓

Merge & Standardize Ingredients

↓

Generate Shopping Quantities

↓

Review Shopping List

↓

Edit Quantities

↓

Select / Deselect Ingredients

↓

Proceed to Swiggy (Future MCP Integration)
```

# 📦 JSON Response Format

```json
{
  "status": "success",
  "recipe_name": "...",
  "people": 4,
  "shopping_list": [
    {
      "canonical_name": "Oil",
      "display_name": "ఆయిల్",
      "quantity": 500,
      "unit": "ml"
    }
  ]
}
```

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- JavaScript

## Backend

- FastAPI
- Python

## AI Models

- Google Gemini
- Sarvam AI Speech-to-Text

## Utilities

- yt-dlp
- FFmpeg

---

# 📂 Project Structure

```
recipe-form/

│

├── frontend/

│   ├── src/

│   ├── public/

│   └── package.json

│

├── app.py

├── pipeline.py

├── ingredient_extractor.py

├── quantity_generator.py

├── transcribe.py

├── merge.py

├── utils.py

├── requirements.txt

└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Rishwanth1537/Recipe-to-Smart-Shopping-List.git
```

Backend

```bash
cd recipe-form

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app:app --reload
```

Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🎯 Future Scope

The current prototype ends after user verification.

Once Swiggy MCP access is provided, the verified shopping list will be sent directly to the Swiggy MCP server.

Future workflow:

```
Verified Shopping List

↓

Swiggy MCP

↓

Product Search

↓

Best Product Selection

↓

Cart Creation

↓

Checkout
```

This will eliminate the need for users to manually search and add grocery items.

---

# 👨‍💻 Author

**Rishwanth Sai**

AI & Data Science Undergraduate

Amrita Vishwa Vidyapeetham

LinkedIN:
https://www.linkedin.com/in/rishwanthsai/

Portfolio:
https://rishwanth1537.github.io/portfolio/


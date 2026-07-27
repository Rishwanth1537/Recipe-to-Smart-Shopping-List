const API_BASE = "http://127.0.0.1:8000";

export async function generateShoppingList(youtubeUrl, servings) {

    const response = await fetch(`${API_BASE}/process_recipe`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
        },

        body: JSON.stringify({

            youtube_url: youtubeUrl,

            servings,

        }),

    });

    if (!response.ok) {

        const err = await response.json();

        throw new Error(err.detail);

    }

    return await response.json();

}
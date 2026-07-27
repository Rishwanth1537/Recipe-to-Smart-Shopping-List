import { useState } from "react";

import Home from "./pages/Home";
import Review from "./pages/Review";
import LoadingScreen from "./components/loading/LoadingScreen";

import { generateShoppingList } from "./services/api";

export default function App() {

    const [screen, setScreen] = useState("home");

    const [recipeData, setRecipeData] = useState(null);

    const [isLoading, setIsLoading] = useState(false);

    const goToLoading = async (youtubeUrl, servings) => {

        try {

            setIsLoading(true);

            setScreen("loading");

            const result = await generateShoppingList(
                youtubeUrl,
                servings
            );

            console.log(result);

            setRecipeData(result);

            setScreen("review");

            setIsLoading(false);

        }

        catch (error) {

            console.error(error);

            alert(error.message || "Something went wrong.");

            setScreen("home");

            setIsLoading(false);

        }

    };

    if (screen === "home") {

        return (

            <Home
                onGenerate={goToLoading}
                isLoading={isLoading}
            />

        );

    }

    if (screen === "loading") {

        return (

            <LoadingScreen />

        );

    }

    return (

        <Review
            recipeData={recipeData}
        />

    );

}
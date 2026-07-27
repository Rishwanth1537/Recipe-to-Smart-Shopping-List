import { useState } from "react";
import ShoppingSummary from "../components/shopping/ShoppingSummary";
import RecipeHeader from "../components/shopping/RecipeHeader";
import IngredientCard from "../components/shopping/IngredientCard";

import mockData from "../data/mockIngredients";

export default function Review({
    recipeData
}) {

    const data = recipeData || mockData;
    

    const [ingredients, setIngredients] = useState(
        data.shopping_list.map(item => ({
            ...item,
            selected: true
        }))
    );
    const selectedCount = ingredients.filter(
    item => item.selected).length;

    const toggleIngredient = (name) => {

        setIngredients(prev =>
            prev.map(item =>
                item.canonical_name === name
                    ? {
                          ...item,
                          selected: !item.selected,
                      }
                    : item
            )
        );

    };

    const saveQuantity = (name, quantity) => {

        setIngredients(prev =>
            prev.map(item =>
                item.canonical_name === name
                    ? {
                          ...item,
                          quantity,
                      }
                    : item
            )
        );

    };

    return (

        <div className="min-h-screen bg-[#FFF8F2]">

            <div className="mx-auto max-w-5xl space-y-6 px-6 py-12 pb-48">

                <RecipeHeader
                    recipeName={data.recipe_name}
                    people={data.people}
                    ingredientCount={ingredients.length}
                />

                {ingredients.map(item => (

                    <IngredientCard
                        key={item.canonical_name}
                        ingredient={item}
                        onToggle={toggleIngredient}
                        onSaveQuantity={saveQuantity}
                    />

                ))}
                <ShoppingSummary
                selectedCount={selectedCount}
                totalCount={ingredients.length}
                onProceed={() => setShowProceedModal(true)}
                
                />

            </div>

        </div>

    );

}
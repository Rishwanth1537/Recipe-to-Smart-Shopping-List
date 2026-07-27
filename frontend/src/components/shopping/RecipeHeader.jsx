import { Users, ShoppingBasket } from "lucide-react";

export default function RecipeHeader({
    recipeName,
    duration,
    people,
    ingredientCount,
}) {
    return (
        <div className="rounded-3xl bg-white p-8 shadow-sm border border-gray-100">

            <h1 className="text-3xl font-bold text-gray-900">
                {recipeName}
            </h1>

            <div className="mt-6 flex flex-wrap gap-6">

                <div className="flex items-center gap-2 text-gray-600">
                    <Users size={20} />
                    <span>{people} Servings</span>
                </div>

                

                <div className="flex items-center gap-2 text-gray-600">
                    <ShoppingBasket size={20} />
                    <span>{ingredientCount} Ingredients</span>
                </div>

            </div>

        </div>
    );
}
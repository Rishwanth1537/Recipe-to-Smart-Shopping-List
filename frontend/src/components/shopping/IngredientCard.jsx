import { useState } from "react";
import { Check, Pencil, X, Save } from "lucide-react";

export default function IngredientCard({
    ingredient,
    onToggle,
    onSaveQuantity,
}) {
    const [editing, setEditing] = useState(false);

    const [quantity, setQuantity] = useState(ingredient.quantity);

    const handleSave = () => {
        onSaveQuantity(ingredient.canonical_name, quantity);
        setEditing(false);
    };

    return (
        <div
            className={`rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 ${
                ingredient.selected
                    ? "border-orange-200"
                    : "opacity-50 border-gray-200"
            }`}
        >
            <div className="flex items-start justify-between">

                <div className="flex gap-4">

                    <button
                        onClick={() =>
                            onToggle(ingredient.canonical_name)
                        }
                        className={`mt-1 flex h-6 w-6 items-center justify-center rounded-full border ${
                            ingredient.selected
                                ? "bg-orange-500 border-orange-500 text-white"
                                : "border-gray-300"
                        }`}
                    >
                        {ingredient.selected && <Check size={14} />}
                    </button>

                    <div>

                        <h3 className="text-lg font-semibold">
                            {ingredient.canonical_name}
                        </h3>

                        {!editing ? (
                            <>
                                <p className="mt-2 text-sm text-gray-500">
                                    Shopping Quantity
                                </p>

                                <p className="text-lg font-medium">
                                    {ingredient.quantity} {ingredient.unit}
                                </p>
                            </>
                        ) : (
                            <div className="mt-3 flex gap-3">

                                <input
                                    type="number"
                                    value={quantity}
                                    onChange={(e) =>
                                        setQuantity(Number(e.target.value))
                                    }
                                    className="w-28 rounded-lg border px-3 py-2"
                                />

                                <span className="self-center text-gray-500">
                                    {ingredient.unit}
                                </span>

                            </div>
                        )}

                    </div>

                </div>

                {!editing ? (
                    <button
                        onClick={() => setEditing(true)}
                        className="flex items-center gap-2 rounded-lg px-3 py-2 text-orange-600 hover:bg-orange-50"
                    >
                        <Pencil size={18} />
                        Edit
                    </button>
                ) : (
                    <div className="flex gap-2">

                        <button
                            onClick={() => setEditing(false)}
                            className="rounded-lg border p-2"
                        >
                            <X size={18} />
                        </button>

                        <button
                            onClick={handleSave}
                            className="rounded-lg bg-orange-500 p-2 text-white"
                        >
                            <Save size={18} />
                        </button>

                    </div>
                )}

            </div>
        </div>
    );
}
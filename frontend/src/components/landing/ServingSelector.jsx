export default function ServingSelector({
    servings,
    setServings,
}) {
    return (

        <div className="flex items-center justify-center gap-5">

            <button
                onClick={() =>
                    setServings(Math.max(1, servings - 1))
                }
                className="h-12 w-12 rounded-full bg-white shadow text-xl"
            >
                −
            </button>

            <div className="rounded-xl bg-white px-8 py-3 shadow">

                <span className="text-2xl font-bold">

                    {servings}

                </span>

                <p className="text-sm text-gray-500">

                    People

                </p>

            </div>

            <button
                onClick={() =>
                    setServings(servings + 1)
                }
                className="h-12 w-12 rounded-full bg-white shadow text-xl"
            >
                +

            </button>

        </div>

    );
}
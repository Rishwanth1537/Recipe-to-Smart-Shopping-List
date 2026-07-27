import { ShoppingBasket } from "lucide-react";

export default function ShoppingSummary({
    selectedCount,
    totalCount,
    onProceed,
}) {
    return (
        <div className="mt-8 rounded-3xl border border-orange-200 bg-white p-6 shadow-lg">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-xl font-semibold">
                        Shopping Summary
                    </h2>

                    <p className="mt-1 text-gray-500">
                        {selectedCount} of {totalCount} ingredients selected
                    </p>

                </div>

                <button
                    onClick={onProceed}
                    className="rounded-xl bg-orange-500 px-8 py-3 font-semibold text-white transition hover:bg-orange-600"
                >
                    Proceed to Swiggy →
                </button>

            </div>

        </div>
    );
}
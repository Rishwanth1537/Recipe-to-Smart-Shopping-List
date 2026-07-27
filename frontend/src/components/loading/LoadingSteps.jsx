import { useEffect, useState } from "react";
import { Check } from "lucide-react";
import { LOADING_STEPS } from "../../utils/constants";


export default function LoadingSteps() {

    const [active, setActive] = useState(0);

    const [dots, setDots] = useState(1);

    useEffect(() => {

        const timer = setInterval(() => {

            setActive(prev => {

                if (prev >= LOADING_STEPS.length - 1) {

                    clearInterval(timer);

                    return prev;

                }

                return prev + 1;

            });

        }, 1500);

        return () => clearInterval(timer);

    }, []);

    useEffect(() => {

        if (active !== LOADING_STEPS.length - 1) {

            return;

        }

        const dotTimer = setInterval(() => {

            setDots(prev => (prev < 3 ? prev + 1 : 1));

        }, 500);

        return () => clearInterval(dotTimer);

    }, [active]);

    return (

        <div className="mt-10 w-full max-w-md space-y-4">

            {LOADING_STEPS.map((step, index) => {

                const isCompleted = index < active;

                const isActive = index === active;

                const isLastActive =

                    isActive && index === LOADING_STEPS.length - 1;

                return (

                    <div
                        key={step}
                        className="flex items-center gap-4"
                    >

                        <div
                            className={`flex h-3 w-3 items-center justify-center rounded-full ${
                                isCompleted
                                    ? "bg-green-500"

                                    : isActive
                                    ? "animate-pulse bg-orange-500"

                                    : "bg-gray-300"
                            }`}
                        >

                            {isCompleted && (

                                <Check
                                    size={10}
                                    className="text-white"
                                    strokeWidth={3}
                                />

                            )}

                        </div>

                        <span
                            className={
                                isActive
                                ? "font-semibold text-orange-600"
                                : isCompleted
                                ? "text-gray-700"
                                : "text-gray-500"
                            }
                        >

                            {isLastActive
                                ? `${step}${".".repeat(dots)}`
                                : step}

                        </span>

                    </div>

                );

            })}

        </div>

    );

}
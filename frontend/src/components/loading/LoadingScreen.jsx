import { ChefHat } from "lucide-react";

import CookingAnimation from "./CookingAnimation";
import LoadingSteps from "./LoadingSteps";

export default function LoadingScreen() {

    return (

        <div className="flex min-h-screen flex-col items-center justify-center bg-[#FFF8F2]">

            <CookingAnimation />

            <h1 className="mt-8 text-3xl font-bold">

                Preparing your Shopping List

            </h1>

            <p className="mt-3 text-gray-500">

                Something's cooking...

            </p>

            <LoadingSteps />

        </div>

    );

}
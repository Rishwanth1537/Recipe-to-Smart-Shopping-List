import { useState } from "react";

import Hero from "../components/landing/Hero";
import UrlInput from "../components/landing/UrlInput";
import ServingSelector from "../components/landing/ServingSelector";

import Button from "../components/common/Button";

export default function Home({ 
    onGenerate,
    isLoading

 }) {

    const [url, setUrl] = useState("");

    const [servings, setServings] = useState(5);

    const handleGenerate = () => {

        if (!url.trim()) {

            alert("Please paste a YouTube URL.");

            return;

        }

        onGenerate(url, servings);

    };

    return (

        <div className="min-h-screen bg-[#FFF8F2]">

            <div className="mx-auto flex max-w-4xl flex-col gap-8 px-6 py-20">

                <Hero />

                <UrlInput
                    value={url}
                    onChange={setUrl}
                />

                <ServingSelector
                    servings={servings}
                    setServings={setServings}
                />

                <Button 
                disabled={isLoading}
                onClick={handleGenerate}
                >
                    {isLoading
                        ? "Generating..."
                        : "Generate Shopping List"}

                    Generate Shopping List

                </Button>

            </div>

        </div>

    );
}
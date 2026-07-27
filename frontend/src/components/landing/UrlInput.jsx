export default function UrlInput({
    value,
    onChange,
}) {
    return (

        <input

            type="text"

            value={value}

            onChange={(e) => onChange(e.target.value)}

            placeholder="Paste YouTube Recipe URL..."

            className="
                w-full
                rounded-2xl
                border
                border-gray-300
                bg-white
                px-5
                py-4
                text-lg
                outline-none
                transition
                focus:border-orange-500
                focus:ring-4
                focus:ring-orange-100
            "

        />

    );
}
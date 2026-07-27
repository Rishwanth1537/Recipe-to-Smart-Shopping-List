export default function Button({

    children,

    onClick,

    disabled

}) {

    return (

        <button

            onClick={onClick}

            disabled={disabled}

            className="rounded-xl bg-orange-500 px-8 py-4 font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-gray-300"

        >

            {children}

        </button>

    );

}
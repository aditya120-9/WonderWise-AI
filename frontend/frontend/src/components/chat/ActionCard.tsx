import type { LucideIcon } from "lucide-react";
import { motion } from "framer-motion";

interface Props{
    icon:LucideIcon;
    title:string;
    subtitle:string;
    onClick:()=>void;
}

export default function ActionCard({
    icon:Icon,
    title,
    subtitle,
    onClick
}:Props){

    return(

        <motion.button

            whileHover={{y:-3}}

            whileTap={{scale:.98}}

            onClick={onClick}

            className="
            bg-white
            rounded-3xl
            p-4
            text-left
            border
            border-gray-200
            shadow-sm
            hover:shadow-md
            hover:border-blue-500
            transition-all
            "

        >

            <div
                className="
                w-12
                h-12
                rounded-2xl
                bg-blue-100
                flex
                items-center
                justify-center
                "
            >

                <Icon
                    className="text-blue-600"
                    size={24}
                />

            </div>

            <h3
                className="mt-4 text-base font-semibold"
            >
                {title}
            </h3>

            <p
                className="mt-2 text-gray-500 text-sm"
            >
                {subtitle}
            </p>

        </motion.button>

    );

}
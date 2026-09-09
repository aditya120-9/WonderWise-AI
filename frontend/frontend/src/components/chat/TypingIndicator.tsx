import {

motion

} from "framer-motion";

export default function TypingIndicator(){

    return(

        <motion.div

        animate={{

            opacity:[0.4,1,0.4]

        }}

        transition={{

            repeat:Infinity,

            duration:1

        }}

        className="bg-gray-100 rounded-full px-4 py-3 w-fit"

        >

            ● ● ●

        </motion.div>

    )

}
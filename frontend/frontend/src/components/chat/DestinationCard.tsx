import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

interface Props{

image:string;

title:string;

price:string;

category:string;

}

export default function DestinationCard({

image,

title,

price,

category

}:Props){

return(

<motion.div

whileHover={{

y:-6,

scale:1.02

}}

className="

rounded-3xl

overflow-hidden

bg-white

shadow-lg

cursor-pointer

"

>

<img

src={image}

alt={title}

className="

h-60

w-full

object-cover

"

/>

<div className="p-5">

<div className="flex justify-between">

<div>

<h3
className="text-xl font-bold">

{title}

</h3>

<p
className="text-gray-500 mt-1">

{category}

</p>

</div>

<div>

<p
className="text-blue-600 font-bold">

{price}

</p>

</div>

</div>

<button

className="

mt-5

flex

items-center

gap-2

text-blue-600

font-medium

"

>

Explore

<ArrowRight size={18}/>

</button>

</div>

</motion.div>

);

}
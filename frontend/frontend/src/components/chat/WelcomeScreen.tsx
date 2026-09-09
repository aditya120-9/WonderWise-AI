import { motion } from "framer-motion";

export default function WelcomeScreen(){
  const hour = new Date().getHours();
  let greeting = "Good Evening";

  if (hour < 12) {
    greeting = "Good Morning";
  } else if (hour < 18) {
    greeting = "Good Afternoon";
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="rounded-lg bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 p-4 text-white shadow-lg"
    >
        <p className="text-xs uppercase tracking-[0.35em] text-sky-300">AI Travel Assistant</p>
        <div className="mt-3 flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-white/10 flex items-center justify-center text-lg">🌍</div>
          <div>
            <h1 className="text-2xl font-black tracking-tight">{greeting}, Aditya</h1>
            <p className="mt-1 text-slate-200 text-sm">Where would you like to go?</p>
          </div>
        </div>
        <p className="mt-4 max-w-2xl text-slate-300 leading-6 text-sm">
          Plan flights, hotels, trains, cabs and discover amazing destinations with WonderWise AI. Get travel suggestions, booking assistance and personalized recommendations—all powered by a local AI model.
        </p>
    </motion.section>
  );
}
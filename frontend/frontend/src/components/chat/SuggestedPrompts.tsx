import {
  Plane,
  Hotel,
  Train,
  Car,
  Compass,
  Wallet,
} from "lucide-react";

import ActionCard from "./ActionCard";

const actions = [
  {
    title: "Find Flights",
    subtitle: "Best prices today",
    icon: Plane,
    prompt: "Help me find the cheapest flights for my next trip",
  },
  {
    title: "Hotels",
    subtitle: "Curated stays",
    icon: Hotel,
    prompt: "Show me hotel options with great reviews and value",
  },
  {
    title: "Train Booking",
    subtitle: "Fastest routes",
    icon: Train,
    prompt: "Find the best train routes and schedules for my journey",
  },
  {
    title: "Cab Booking",
    subtitle: "Airport & city rides",
    icon: Car,
    prompt: "Recommend the best cab options for airport and city travel",
  },
  {
    title: "Explore Places",
    subtitle: "Hidden gems",
    icon: Compass,
    prompt: "Suggest interesting travel destinations I should explore",
  },
  {
    title: "Budget Planner",
    subtitle: "Smart itineraries",
    icon: Wallet,
    prompt: "Create a budget travel plan for my next vacation",
  },
];

interface Props {
  onSelect: (prompt: string) => void;
}

export default function SuggestedPrompts({ onSelect }: Props) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {actions.map((action) => (
        <ActionCard
          key={action.title}
          icon={action.icon}
          title={action.title}
          subtitle={action.subtitle}
          onClick={() => onSelect(action.prompt)}
        />
      ))}
    </div>
  );
}
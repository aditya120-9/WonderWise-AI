import MessageBubble from "./MessageBubble";

import type { Message } from "../../types/chat";

interface Props{

    messages:Message[];

}

export default function ChatWindow({messages}:Props){

    return(

        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </div>

    )

}
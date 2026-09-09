export interface ChunkMessage{

    type:"chunk";

    content:string;

    request_id?: string | null;

}

export interface EndMessage{

    type:"end";

    request_id?: string | null;

}

export interface ErrorMessage{

    type:"error";

    message:string;

}

export type SocketMessage=

ChunkMessage|

EndMessage|

ErrorMessage;
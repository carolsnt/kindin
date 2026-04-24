const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type EventHandlers = {
  [eventType: string]: (data: unknown) => void;
};

/**
 * Connect to a Server-Sent Events endpoint.
 * Returns a cleanup function that closes the EventSource.
 */
export function connectSSE(path: string, handlers: EventHandlers): () => void {
  const url = `${API_BASE_URL}${path}`;
  const es = new EventSource(url);

  for (const [eventType, handler] of Object.entries(handlers)) {
    es.addEventListener(eventType, (e: MessageEvent) => {
      try {
        handler(JSON.parse(e.data));
      } catch {
        handler(e.data);
      }
    });
  }

  es.onerror = () => {
    handlers["error"]?.({ message: "SSE connection error" });
    es.close();
  };

  return () => es.close();
}

import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const sendMessage = async (message, birthDetails, history) => {
  const response = await api.post("/chat", {
    message,
    birth_details: birthDetails,
    conversation_history: history,
  });
  return response.data;
};

export const streamMessage = async (message, birthDetails, history, onToken, onDone) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      birth_details: birthDetails,
      conversation_history: history,
    }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          if (data.type === "token") onToken(data.content);
          if (data.type === "done") onDone();
          if (data.type === "error") console.error(data.content);
        } catch {}
      }
    }
  }
};

export default api;
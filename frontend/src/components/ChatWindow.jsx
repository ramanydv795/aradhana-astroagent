import { useState, useEffect, useRef } from "react";
import Message from "./Message";
import ToolActivity from "./ToolActivity";
import { sendMessage } from "../lib/api";

export default function ChatWindow({ birthDetails, onReset }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: birthDetails?.name
        ? `Namaste, ${birthDetails.name} 🙏\n\nThe stars have been waiting for you. I have your birth details and I'm ready to explore your cosmic blueprint.\n\nWhat would you like to know? You can ask about your birth chart, today's planetary energy, relationships, career, or anything on your heart.`
        : `Namaste 🙏\n\nI am Aradhana, your spiritual companion. The cosmos holds infinite wisdom, and I'm here to help you navigate it.\n\nWhat would you like to explore today?`,
      intent: null,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTools, setActiveTools] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, activeTools]);

  const getHistory = () =>
    messages.map((m) => ({ role: m.role, content: m.content }));

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // Show thinking indicator
    setActiveTools(["thinking"]);

    try {
      const data = await sendMessage(
        userMessage.content,
        birthDetails,
        getHistory()
      );

      setActiveTools([]);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          intent: data.intent,
        },
      ]);
    } catch (err) {
      setActiveTools([]);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "I sense a disturbance in the cosmic connection. Please try again in a moment. 🌙",
          intent: null,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-purple-950 to-slate-950 flex flex-col">
      {/* Header */}
      <div className="border-b border-white/10 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-amber-200 text-lg">✦</span>
          <span className="text-amber-100 font-light">Aradhana</span>
          {birthDetails?.name && (
            <span className="text-purple-400 text-xs">
              · {birthDetails.name}
            </span>
          )}
        </div>
        <button
          onClick={onReset}
          className="text-purple-400 hover:text-purple-300 text-xs transition-colors"
        >
          New reading
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        <div className="max-w-2xl mx-auto">
          {messages.map((msg, i) => (
            <Message key={i} message={msg} />
          ))}

          {/* Tool activity */}
          {loading && (
            <ToolActivity
              tools={activeTools[0] === "thinking" ? [] : activeTools}
            />
          )}

          {/* Typing indicator */}
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="w-8 h-8 rounded-full bg-purple-800 flex items-center justify-center text-sm mr-2">
                ✦
              </div>
              <div className="bg-white/5 border border-white/10 rounded-2xl rounded-tl-sm px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Suggested questions */}
      {messages.length === 1 && (
        <div className="px-4 pb-2">
          <div className="max-w-2xl mx-auto flex flex-wrap gap-2">
            {[
              "What does my birth chart reveal?",
              "What's the energy for me today?",
              "Tell me about my career path",
              "What does Venus in my chart mean?",
            ].map((q) => (
              <button
                key={q}
                onClick={() => setInput(q)}
                className="bg-white/5 border border-white/10 text-purple-300 text-xs px-3 py-1.5 rounded-full hover:bg-white/10 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="border-t border-white/10 px-4 py-3">
        <div className="max-w-2xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask Aradhana anything..."
            disabled={loading}
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-amber-100 placeholder-purple-400 text-sm focus:outline-none focus:border-purple-400 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-purple-600 hover:bg-purple-500 disabled:bg-purple-800 disabled:opacity-50 text-white px-4 py-2.5 rounded-xl text-sm font-medium transition-colors"
          >
            ✦
          </button>
        </div>
        <p className="text-purple-600 text-xs text-center mt-2">
          For guidance and reflection only — not medical, legal, or financial advice
        </p>
      </div>
    </div>
  );
}
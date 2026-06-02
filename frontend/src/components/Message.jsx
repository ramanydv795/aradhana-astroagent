export default function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-purple-800 flex items-center justify-center text-sm mr-2 flex-shrink-0 mt-1">
          ✦
        </div>
      )}
      <div
        className={`max-w-xs md:max-w-md lg:max-w-lg rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-purple-600 text-white rounded-tr-sm"
            : "bg-white/5 border border-white/10 text-amber-100 rounded-tl-sm"
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
          {message.streaming && (
            <span className="inline-block w-1 h-4 bg-purple-400 ml-1 animate-pulse" />
          )}
        </p>
        {message.intent && (
          <p className="text-purple-400 text-xs mt-1 opacity-60">
            {message.intent === "chart_request" && "🔮 Chart reading"}
            {message.intent === "daily_horoscope" && "⭐ Daily horoscope"}
            {message.intent === "general_question" && "✨ Guidance"}
          </p>
        )}
      </div>
    </div>
  );
}
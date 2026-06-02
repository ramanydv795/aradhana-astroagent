export default function ToolActivity({ tools }) {
  if (!tools || tools.length === 0) return null;

  const toolLabels = {
    tool_geocode_place: "📍 Locating birth place...",
    tool_compute_birth_chart: "🔮 Computing birth chart...",
    tool_get_daily_transits: "⭐ Fetching planetary transits...",
    tool_knowledge_lookup: "📚 Consulting astrology knowledge...",
  };

  return (
    <div className="flex justify-start mb-2">
      <div className="w-8 h-8 rounded-full bg-purple-800 flex items-center justify-center text-sm mr-2 flex-shrink-0">
        ✦
      </div>
      <div className="bg-white/5 border border-white/10 rounded-2xl rounded-tl-sm px-4 py-2">
        {tools.map((tool, i) => (
          <div key={i} className="flex items-center gap-2 text-purple-300 text-xs py-0.5">
            <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-pulse" />
            {toolLabels[tool] || `Using ${tool}...`}
          </div>
        ))}
      </div>
    </div>
  );
}
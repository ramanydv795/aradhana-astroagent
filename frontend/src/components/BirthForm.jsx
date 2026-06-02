import { useState } from "react";

export default function BirthForm({ onSubmit, onSkip }) {
  const [form, setForm] = useState({
    name: "",
    date: "",
    time: "",
    place: "",
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!form.name.trim()) newErrors.name = "Name is required";
    if (!form.date) newErrors.date = "Birth date is required";
    if (!form.place.trim()) newErrors.place = "Birth place is required";
    
    // Validate date range
    if (form.date) {
      const year = new Date(form.date).getFullYear();
      if (year < 1900 || year > 2010) {
        newErrors.date = "Please enter a valid birth year (1900-2010)";
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      onSubmit({
        name: form.name,
        date: form.date,
        time: form.time || "12:00",
        place: form.place,
        latitude: null,
        longitude: null,
        timezone: null,
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-purple-950 to-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">✦</div>
          <h1 className="text-3xl font-light text-amber-100 mb-2">Aradhana</h1>
          <p className="text-purple-300 text-sm">Your daily spiritual companion</p>
        </div>

        {/* Form Card */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
          <h2 className="text-amber-100 font-medium mb-1">Begin your journey</h2>
          <p className="text-purple-300 text-xs mb-6">
            Share your birth details for a personalized reading
          </p>

          <div className="space-y-4">
            <div>
              <label className="block text-purple-200 text-xs mb-1">Your Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="e.g. Arjun"
                className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-amber-100 placeholder-purple-400 text-sm focus:outline-none focus:border-purple-400"
              />
              {errors.name && <p className="text-red-400 text-xs mt-1">{errors.name}</p>}
            </div>

            <div>
              <label className="block text-purple-200 text-xs mb-1">Date of Birth</label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-amber-100 text-sm focus:outline-none focus:border-purple-400"
              />
              {errors.date && <p className="text-red-400 text-xs mt-1">{errors.date}</p>}
            </div>

            <div>
              <label className="block text-purple-200 text-xs mb-1">
                Time of Birth
                <span className="text-purple-400 ml-1">(optional but improves accuracy)</span>
              </label>
              <input
                type="time"
                value={form.time}
                onChange={(e) => setForm({ ...form, time: e.target.value })}
                className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-amber-100 text-sm focus:outline-none focus:border-purple-400"
              />
            </div>

            <div>
              <label className="block text-purple-200 text-xs mb-1">Place of Birth</label>
              <input
                type="text"
                value={form.place}
                onChange={(e) => setForm({ ...form, place: e.target.value })}
                placeholder="e.g. Mumbai, India"
                className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-amber-100 placeholder-purple-400 text-sm focus:outline-none focus:border-purple-400"
              />
              {errors.place && <p className="text-red-400 text-xs mt-1">{errors.place}</p>}
            </div>
          </div>

          <button
            onClick={handleSubmit}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-medium py-3 rounded-xl mt-6 transition-colors text-sm"
          >
            Begin Reading ✦
          </button>

          <button
            onClick={onSkip}
            className="w-full text-purple-400 hover:text-purple-300 text-xs mt-3 transition-colors"
          >
            Continue without birth details
          </button>

          <p className="text-purple-500 text-xs text-center mt-4">
            Astrology is for guidance and reflection only — not medical, legal, or financial advice.
          </p>
        </div>
      </div>
    </div>
  );
}
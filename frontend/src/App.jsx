import { useState } from "react";
import BirthForm from "./components/BirthForm";
import ChatWindow from "./components/ChatWindow";

export default function App() {
  const [birthDetails, setBirthDetails] = useState(null);
  const [started, setStarted] = useState(false);

  const handleBirthSubmit = (details) => {
    setBirthDetails(details);
    setStarted(true);
  };

  const handleSkip = () => {
    setBirthDetails(null);
    setStarted(true);
  };

  const handleReset = () => {
    setBirthDetails(null);
    setStarted(false);
  };

  if (!started) {
    return (
      <BirthForm
        onSubmit={handleBirthSubmit}
        onSkip={handleSkip}
      />
    );
  }

  return (
    <ChatWindow
      birthDetails={birthDetails}
      onReset={handleReset}
    />
  );
}
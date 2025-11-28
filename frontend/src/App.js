import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import VoiceAssistant from "./components/VoiceAssistant";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<VoiceAssistant />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </div>
  );
}

export default App;

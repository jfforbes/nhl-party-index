import { HashRouter as Router, Routes, Route} from "react-router-dom"
import GameListAndPartyIndex from "./components/GameListAndPartyIndex";
import AboutPage from "./components/AboutPage";
import HeaderBar from "./components/HeaderBar";
import "./App.css";
import "./DatePickerOverrides.css"
import "./responsive.css"
import { useEffect } from "react";
import CalculatingThePartyIndex from "./components/CalculatingThePartyIndex";


function App() {
  useEffect(() => {
    document.title = "NHL Party Index"
  }, [])
  return (
    <Router>
      <div className="app-center">
        <HeaderBar />
        <Routes>
          <Route path="calculating" element={<CalculatingThePartyIndex />} />
          <Route path="nhl-party-index" element={<GameListAndPartyIndex />} />
          <Route path="about" element={<AboutPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
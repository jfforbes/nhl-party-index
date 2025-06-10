import { HashRouter as Router, Routes, Route} from "react-router-dom"
import GameListAndPartyIndex from "./components/GameListAndPartyIndex";
import AboutPage from "./components/AboutPage";
import HeaderBar from "./components/HeaderBar";
import PartyIndexByTeam from "./components/PartyIndexByTeam";
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
          <Route path="party-index-date" element={<GameListAndPartyIndex />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="party-index-team" element={<PartyIndexByTeam />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
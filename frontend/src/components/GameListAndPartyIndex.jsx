import { use, useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const API_BASE = "https://nhl-party-index.onrender.com"

function GameListAndPartyIndex() {
  const [date, setDate] = useState(new Date("2024-04-18"));
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [validDates, setValidDates] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/get-all-game-dates`)
    .then(res => res.json())
    .then(data => {
      setValidDates(data.map(d => new Date(d)));
    })
  }, []);

  const fetchGames = async () => {
    if (!date) return;
    setLoading(true);
    setError("")
    setGames([]);
    try{
      const isoDate = date.toISOString().slice(0, 10); // YYYY-MM-DD
      const res = await fetch(`${API_BASE}/get-party-index-for-games/${isoDate}`);
      if (!res.ok) throw new Error("Failed to fetch games")
      const data = await res.json();
      setGames(data);
    } catch (err) {
      setError("Could not fetch games for that date.")
    } finally {
      setLoading(false);
    }


  };

  return (
    <div>
      <div className="party-index-how-to">
        <h2 style={{ color: "#D1D7DB", fontSize: "1.3rem", marginBottom: "0.5em" }}>How to Use This</h2>
          <ul style={{ color: "#D1D7DB", maxWidth: 700, margin: "0 auto 1.5em auto", fontSize: "1.05rem" }}>
            <li>Select a date using the date picker above.</li>
            <li>Click <b>Get Games</b> to view all NHL games for that day.</li>
            <li>
              Each game will display its calculated <b>Party Index</b>. 
              <ul>
                <li>Games with a <b>high Party Index</b> and an away team loss are highlighted in green.</li>
                <li>Games with a <b>low Party Index</b> and an away team win are highlighted in yellow.</li>
              </ul>
            </li>
            <li>Right now, the Party Index only works for the 2017/2018 - 2023/2024 seasons</li>
          </ul>
      </div>
      <div className="datepicker-wrapper">
        <DatePicker
          selected={date}
          onChange={setDate}
          dateFormat="yyyy-MM-dd"
          placeholderText="Select a date"
          maxDate={new Date()}
          showMonthDropdown
          showYearDropdown
          dropdownMode="select"
          isClearable
          filterDate={date =>
            validDates.some(
              d =>
                d.getFullYear() === date.getFullYear() &&
                d.getMonth() === date.getMonth() &&
                d.getDate() === date.getDate()
            )
          }
          renderCustomHeader={({
            date,
            changeYear,
            changeMonth,
            decreaseMonth,
            increaseMonth,
            prevMonthButtonDisabled,
            nextMonthButtonDisabled
          }) => (
            <div className="react-datepicker__header-row" style={{ flexDirection: "column", alignItems: "center" }}>
              <div style={{ display: "flex", alignItems: "center", width: "100%", justifyContent: "center" }}>
                <button
                  onClick={decreaseMonth}
                  disabled={prevMonthButtonDisabled}
                  className="react-datepicker__navigation react-datepicker__navigation--previous"
                  aria-label="Previous Month"
                  type="button"
                >
                  {"<"}
                </button>
                <span className="react-datepicker__current-month" style={{ flex: 1, textAlign: "center" }}>
                  {date.toLocaleString("default", { month: "long" }).toUpperCase()} {date.getFullYear()}
                </span>
                <button
                  onClick={increaseMonth}
                  disabled={nextMonthButtonDisabled}
                  className="react-datepicker__navigation react-datepicker__navigation--next"
                  aria-label="Next Month"
                  type="button"
                >
                  {">"}
                </button>
              </div>
              <div style={{ display: "flex", justifyContent: "center", marginTop: "0.5em" }}>
                <select
                  value={date.getMonth()}
                  onChange={e => changeMonth(Number(e.target.value))}
                  className="react-datepicker__month-dropdown-container"
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <option key={i} value={i}>
                      {new Date(0, i).toLocaleString("default", { month: "long" })}
                    </option>
                  ))}
                </select>
                <select
                  value={date.getFullYear()}
                  onChange={e => changeYear(Number(e.target.value))}
                  className="react-datepicker__year-dropdown-container"
                >
                  {Array.from({ length: 8 }, (_, i) => {
                    const year = 2017 + i;
                    return (
                      <option key={year} value={year}>
                        {year}
                      </option>
                    );
                  })}
                </select>
              </div>
            </div>
          )}
        />
      <button className = "get-games-button" onClick={fetchGames} disabled={!date || loading}>
        {loading? "Loading..." : "Get Games"}
      </button>
      </div>
      <ul className="games-list">
        {games.map (({game, party_index, away_lost}) => {
          const isHighPI = party_index !== null && party_index >= 70;
          const isLowPI = party_index !== null && party_index <= 40;
          let itemClass = "games-list-item"
          if (isHighPI && away_lost) {
            itemClass += " high-pi-away-loss"
          }
          else if (isLowPI && away_lost == false) {
            itemClass += " low-pi-away-win"
          }
          return (
            <li
              className={itemClass}
              key={game.id}
            >
              <b>{game.awayTeam_abbrev} {game.awayTeam_score}</b> @ <b>{game.homeTeam_abbrev} {game.homeTeam_score}</b>
              {party_index !== null && (
                <span style={{ marginLeft: 8, fontWeight: 400, fontSize: "1rem"}}>
                  (Party Index: {party_index})
                </span>
              )}
          </li>
          );
        })}
      </ul>
    </div>
    
  );
}

export default GameListAndPartyIndex;
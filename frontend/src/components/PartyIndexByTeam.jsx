import { useEffect, useState } from "react"

const API_BASE = 
  process.env.NODE_ENV === "production"
  ? "https://nhl-party-index.onrender.com"
  : ""

  function PartyIndexByTeam() {
    const [teams, setTeams] = useState([]);
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedSeason, setSelectedSeason] = useState("20232024");
    const [results, setResults] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE}/get-teams`)
        .then(res => res.json())
        .then(data => {
            let teamList = Array.isArray(data) ? data: data.teams || [];
            teamList = [...teamList].sort((a, b) => a.localeCompare(b));
            setTeams(teamList);
        })
        .catch(() => setTeams([]));
    }, []);

    const seasons = [
        { label: "2017-2018", value: "20172018" },
        { label: "2018-2019", value: "20182019" },
        { label: "2019-2020", value: "20192020" },
        { label: "2020-2021", value: "20202021" },
        { label: "2021-2022", value: "20212022" },
        { label: "2022-2023", value: "20222023" },
        { label: "2023-2024", value: "20232024" }
    ];

    useEffect(() => {
        if (selectedTeam && selectedSeason) {
            // Fetch party index for the selected team and season here
            fetch(`${API_BASE}/get-party-index-for-team/${selectedTeam}/${selectedSeason}`)
            .then(res => res.json())
            .then(data => setResults(data))
            .catch(() => setResults([]));
        }
        }, [selectedTeam, selectedSeason]);

    return (
        <div className="page-container">
            <div style={{ margin: "1em 0" }}>
                <label>
                    Team:&nbsp;
                    <select
                        value={selectedTeam}
                        onChange={e => setSelectedTeam(e.target.value)}
                    >
                        <option value="">Select a team</option>
                        {teams.map(team => (
                        <option key={team} value={team}>
                            {team}
                        </option>
                        ))}
                    </select>
                </label>
            </div>
            <div style={{ margin: "1em 0" }}>
                <label>
                Season:&nbsp;
                <select
                    value={selectedSeason}
                    onChange={e => setSelectedSeason(e.target.value)}
                >
                    {seasons.map(season => (
                    <option key={season.value} value={season.value}>
                        {season.label}
                    </option>
                    ))}
                </select>
                </label>
            </div>
            <div className="party-index-results-box">
                <ul className="games-list two-columns">
                    {results.map (({game, party_index, away_lost}) => {
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
                        <b>{game.gameDate} </b><b>{game.awayTeam_abbrev} {game.awayTeam_score}</b> @ <b>{game.homeTeam_abbrev} {game.homeTeam_score}</b>
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
        </div>
    );
  }

  export default PartyIndexByTeam;
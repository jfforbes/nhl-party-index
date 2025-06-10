import React from "react";
import "../App.css";
import "../pages.css";

function CalculatingThePartyIndex() {
  return (
    <div className="page-container">
        <h1 className="page-title">What is the NHL Party Index?</h1>
        <p>
            Partially inspired by the Spittin Chiclets podcast, the <strong>NHL Party Index</strong> is a fun, data-driven metric designed to identify NHL road games where the visiting team might have a higher propensity for an "eventful" night out.
            It's not about predicting game outcomes, but rather quantifying a unique set of circumstances that could impact performance.
        </p>
        <ul>
            <li>
            <strong>Youthful Energy:</strong> Teams with more players under 28 may be more inclined to enjoy the nightlife on the road. Furthermore, AI research was done to determine the average age NHL players get married (as that data is not publicly available), which was 28.
            </li>
            <li>
            <strong>Host City Allure:</strong> Cities with vibrant nightlife (like Vegas or Nashville) are weighted more heavily. 
            </li>
            <li>
            <strong>Opportunity & Rest:</strong> A night off before a game increases the potential for off-ice activities.
            </li>
        </ul>
        <p>
            <strong>Formula:</strong> <br />
            <span style={{ fontFamily: "monospace", background: "#181c23", padding: "0.2em 0.5em", borderRadius: "4px" }}>
            Party Index = (YPR) × (City Score) × (Rest Modifier)
            </span>
        </p>
        <ul>
            <li>
            <strong>YPR (Young Player Ratio):</strong> The ratio of players below 28 to total players on a team. Above 1 if there are more players below 28, less than 1 if there are fewer.
            </li>
            <li>
            <strong>City Score:</strong> Subjective score for each NHL city's "party potential", 10.0 being highest (Vegas), 0.1 being the lowest (sorry Winnipeg)
            </li>
            <li>
            <strong>Rest Modifier:</strong> Adjusts for whether the team is rested or on a back-to-back. If there are more days between games in an exciting city, they're more likely to party, and therefore there is a higher modifier. Whereas if they are on the road at a boring city, and there are more days between games, they're likely to be rested.
            </li>
        </ul>
        <p>
            <strong>Disclaimer:</strong> The Party Index is for entertainment and discussion. It's not a definitive predictor of game outcomes, but a lens for exploring how off-ice factors might influence performance.
        </p>
    </div>
  );
}

export default CalculatingThePartyIndex;
import React from "react";
import "../App.css";

function CalculatingThePartyIndex() {
  return (
    <section className="calculating-section">
      <h2 className="calculating-header">About the NHL Party Index</h2>
      <p>
        The <strong>NHL Party Index</strong> is a fun, data-driven metric designed to identify NHL road games where the visiting team might have a higher propensity for an "eventful" night out.
        It’s not about predicting game outcomes, but rather quantifying a unique set of circumstances that could impact performance.
      </p>
      <ul>
        <li>
          <strong>Youthful Energy:</strong> Teams with more players under 28 may be more inclined to enjoy the nightlife on the road.
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
          Party Index = (YPM) × (City Score) × (Rest Modifier)
        </span>
      </p>
      <ul>
        <li>
          <strong>YPM (Young Player Metric):</strong> Number of visiting players under 28.
        </li>
        <li>
          <strong>City Score:</strong> Subjective score for each NHL city’s "party potential."
        </li>
        <li>
          <strong>Rest Modifier:</strong> Adjusts for whether the team is rested or on a back-to-back.
        </li>
      </ul>
      <p>
        <strong>Disclaimer:</strong> The Party Index is for entertainment and discussion. It’s not a definitive predictor of game outcomes, but a lens for exploring how off-ice factors might influence performance.
      </p>
    </section>
  );
}

export default CalculatingThePartyIndex;
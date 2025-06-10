import React from "react";
import { Link } from "react-router-dom";
import "../HeaderBar.css"

function HeaderBar() {
    return (
        <header className="header-bar-outer">
            <div className="header-title-block">
                <h1 className="page-header">NHL PARTY INDEX</h1>
                <h3 className="page-subheader">
                An analytical approach to identifying the statistical impact of road games that have a higher potential for off-ice festivities
                </h3>
            </div>
            <nav className="header-bar">
                <ul>
                    <li>
                        <Link to="calculating">Calculating The Party Index</Link>
                    </li>
                    <li>
                        <Link to="party-index-date">Look up Party Index by Date</Link>
                    </li>
                    <li>
                        <Link to="party-index-team">Look up Party Index by Team/Season</Link>
                    </li>
                    <li>
                        <Link to="about">About</Link>
                    </li>
                </ul>
            </nav>
        </header>
    )
}

export default HeaderBar;
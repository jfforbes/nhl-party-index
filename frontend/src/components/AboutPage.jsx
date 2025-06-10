import React from "react";
import "../App.css";
import "../pages.css"

function AboutPage() {
  return (
    <div className="page-container">
      <h1 className="page-title">How This Was Made</h1>
      <p>
        This project was built by James Forbes as a coding exercise to dive head-first into a variety of web technologies. 
      </p>
      <ul>
        <li>
            This project was built with a modern web stack.
        </li>
        <li>
            The frontend uses <strong>React</strong> (with <strong>Vite</strong> for fast development and builds) .
        </li>
        <li>
          The backend is powered by <strong>Python</strong> and <strong>FastAPI</strong>, with <strong>SQLite</strong> as the database.
        </li>
        <li>
            It is hosted on <strong>Github Pages</strong> pages with the backend hosted in <strong>Render</strong>
        </li>
        <li>
          Data is fetched from the <strong>NHL public API</strong> and processed with custom logic to generate the Party Index.
        </li>
        <li>
            I also have to be honest, this was heavily assisted by AI, specifically <strong>GitHub Copilot</strong>
        </li>
      </ul>
        <h1 className="page-title">Known caveats</h1>
        <p>There are some known caveats with this model that I will be trying to bubble up to the surface</p>
        <ol>
            <li>The formula doesn't take into account good home teams (or bad away teams). I have the backend setup to get away/home/season records, but haven't figured out how to implement it yet</li>
            <li>Younger teams just tend to be worse. I haven't figured out how to accommodate for this yet.</li>
        </ol>
 
    </div>
  );
}

export default AboutPage;

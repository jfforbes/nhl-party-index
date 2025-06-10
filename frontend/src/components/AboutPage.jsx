import React from "react";
import "../App.css";

function AboutPage() {
  return (
    <section className="about-section">
      <h2 className="about-header">How This Was Made</h2>
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
          Data is fetched from the <strong>NHL public API</strong> and processed with custom logic to generate the Party Index.
        </li>
      </ul>

 
    </section>
  );
}

export default AboutPage;

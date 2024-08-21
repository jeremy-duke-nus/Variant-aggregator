import "./App.css";
import React, { useState } from "react";
import Form from "./components/form";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [query, setQuery] = useState({});

  return (
    <>
      <div className="container" key="_main-container">
        <div className="row mt-4" key="_form">
          <Form submitQuery={setQuery} />
        </div>

        <div className="row mt-4" key="_results">
          <div className="col-md-8">
            <h1>Left column</h1>
          </div>

          <div className="col-md-4">
            <h1>Right column</h1>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;

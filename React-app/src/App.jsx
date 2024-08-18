import "./App.css";
import Form from "./components/form";
import React, { useState } from "react";

function App() {
  const [query, setQuery] = useState({});

  return (
    <>
      <Form submitQuery={setQuery} />
    </>
  );
}

export default App;

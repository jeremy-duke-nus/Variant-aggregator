import "./App.css";
import Form from "./components/form";
import React, { useEffect, useState } from "react";

function App() {
  const [query, setQuery] = useState({
    chromosome: "",
    position: "",
    reference: "",
    alternate: "",
  });

  function handleChild(variant) {
    setQuery(variant);
  }

  return (
    <>
      <Form setSubmission={handleChild} />
    </>
  );
}

export default App;

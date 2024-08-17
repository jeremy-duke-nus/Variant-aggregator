import "./App.css";
import Form from "./components/form";
import React, { useEffect, useState } from "react";

function App() {
  const [formValues, setFormValues] = useState({
    chromosome: "",
    position: "",
    reference: "",
    alternate: "",
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    const Variant = {
      chromosome: event.target.chromosome.value,
      position: event.target.position.value,
      reference: event.target.reference.value,
      alternate: event.target.alternate.value,
    };
    setFormValues(Variant);
  };

  return (
    <>
      <Form onSubmit={handleSubmit} />
    </>
  );
}

export default App;

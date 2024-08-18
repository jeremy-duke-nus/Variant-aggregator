import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Components.css";

function Form({ setSubmission }) {
  const [variant, setVariant] = useState({
    chromosome: "",
    position: "",
    reference: "",
    alternate: "",
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    const Var = {
      chromosome: event.target.chromosome.value,
      position: event.target.Position.value,
      reference: event.target.Reference.value,
      alternate: event.target.Variant.value,
    };
    setVariant(Var);
    setSubmission(variant);
  };

  const TextInputFields = ["Position", "Reference", "Variant"];

  return (
    <>
      <div className="container" key="search-container">
        <div className="row mt-4" key="search-form">
          <form onSubmit={handleSubmit}>
            <div className="row" key="form-content">
              <div className="col-md-2 mb-2">
                <select className="form-select" id="chromosome" required>
                  {Array.from({ length: 22 }, (_, index) => (
                    <option value={`chr${index + 1}`}>chr{index + 1}</option>
                  ))}
                  <option value="chrX">chrX</option>
                  <option value="chrY">chrY</option>
                </select>
              </div>

              {TextInputFields.map((fieldName) => {
                return (
                  <div className="col-md-2 mb-2">
                    <input
                      type="text"
                      className="form-control"
                      id={fieldName}
                      placeholder={fieldName}
                      required
                    />
                  </div>
                );
              })}

              <div className="col-md-2 mb-2">
                <div className="col-md-2 mb-2 button-container">
                  <div className="d-flex flex-column align-items-center">
                    <button type="submit" className="btn btn-primary">
                      Submit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default Form;

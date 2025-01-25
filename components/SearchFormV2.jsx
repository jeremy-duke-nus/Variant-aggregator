import React, { useState, useEffect } from "react";
import {
  ValidateCompleteFields,
  ValidateNucleotides,
  ConvertCoordinates,
} from "../utils/Validators";

import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";

import "../styles/SearchForm.css";

const SearchForm = ({ searchSetter }) => {
  const [isClickable, setClickable] = useState(false);
  const [formData, setFormData] = useState({
    input: "",
  });

  const ResetForm = () => {
    setFormData({
      input: "",
    });
    searchSetter(null);
  };

  const handleSubmit = (e) => {
    const search = formData.input.split(":");
    e.preventDefault();
    // Reset search data
    searchSetter({
      chromosome: "",
      position: "",
      reference: "",
      alternate: "",
    });

    const data = {
      chromosome: search[0],
      position: search[1],
      reference: search[2],
      alternate: search[3],
    };
    const validData = ConvertCoordinates(data);
    searchSetter(validData);
  };

  useEffect(() => {
    if (formData.input !== "") {
      setClickable(true);
      console.log(formData);
    } else {
      setClickable(false);
    }
  }, [formData]);

  const handleChange = (e) => {
    const value = e.target.value;
    const name = e.target.id;
    setFormData(() => ({ ...formData, [name]: value }));
  };

  const handleButtonClick = (input) => {
    setFormData({
      input: input,
    });
  };
  return (
    <div className="Search-Form">
      <Form onSubmit={handleSubmit} className="form-center">
        <Row className="input-row">
          <Form.Label>Search for a variant</Form.Label>
          <Form.Group as={Col} controlId="input" onChange={handleChange}>
            <Form.Control
              placeholder="chrom:pos:ref:alt"
              value={formData.input}
            />
          </Form.Group>
        </Row>
        <Row className="btn-row">
          <Button
            variant="secondary"
            onClick={() => handleButtonClick("17:7577538:C:T")}
          >
            SNV Example
          </Button>

          <Button
            variant="secondary"
            onClick={() => handleButtonClick("7:55268943:TGAA:T")}
          >
            Del Example
          </Button>

          <Button
            variant="secondary"
            onClick={() => handleButtonClick("7:55210968:A:AAATCAGAGG")}
          >
            Ins Example
          </Button>

          <Button variant="primary" type="submit" onSubmit={handleSubmit}>
            Submit
          </Button>

          <Button variant="danger" onClick={ResetForm} type="reset">
            Reset
          </Button>
        </Row>
      </Form>
    </div>
  );
};

export default SearchForm;

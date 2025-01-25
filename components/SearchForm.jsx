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
    chromosome: "",
    position: "",
    reference: "",
    alternate: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    searchSetter({
      chromosome: "",
      position: "",
      reference: "",
      alternate: "",
    });
    console.log(formData);
    const validData = ConvertCoordinates(formData);
    searchSetter(validData);
  };

  useEffect(() => {
    if (
      ValidateCompleteFields(formData) &&
      ValidateNucleotides(formData.reference) &&
      ValidateNucleotides(formData.alternate)
    ) {
      setClickable(true);
    } else {
      setClickable(false);
    }
  }, [formData]);

  const handleChange = (e) => {
    const value = e.target.value;
    const name = e.target.id;
    if (name !== "position") {
      setFormData(() => ({ ...formData, [name]: value }));
    } else {
      if (!isNaN(parseInt(value))) {
        setFormData(() => ({ ...formData, [name]: value }));
      } else {
        setFormData(() => ({ ...formData, [name]: "" }));
      }
    }
  };

  const ResetForm = () => {
    setFormData({
      chromosome: "",
      position: "",
      reference: "",
      alternate: "",
    });
    searchSetter(null);
  };

  const handleButtonClick = (chromosome, position, reference, alternate) => {
    setFormData({
      chromosome: chromosome,
      position: position,
      reference: reference,
      alternate: alternate,
    });
  };

  return (
    <div className="Search-Form">
      <Form onSubmit={handleSubmit} className="form-center">
        <Row className="input-row">
          <Form.Label>Search for a variant</Form.Label>
          {/*<Form.Group
            as={Col}
            controlId="input"
            onChange={handleChange}
            onBlur={handleChange}
          >
            <Form.Control
              placeholder="chrom:pos:ref:alt"
              value={formData.chromosome}
            />
          </Form.Group> */}

          <Form.Group
            as={Col}
            controlId="chromosome"
            onChange={handleChange}
            onBlur={handleChange}
          >
            <Form.Control
              placeholder="Chromosome"
              value={formData.chromosome}
            />
          </Form.Group>

          <Form.Group
            as={Col}
            controlId="position"
            onChange={handleChange}
            onBlur={handleChange}
          >
            <Form.Control placeholder="Position" value={formData.position} />
          </Form.Group>

          <Form.Group
            as={Col}
            controlId="reference"
            onChange={handleChange}
            onBlur={handleChange}
          >
            <Form.Control
              placeholder="Reference Allele"
              value={formData.reference}
            />
          </Form.Group>

          <Form.Group
            as={Col}
            controlId="alternate"
            onChange={handleChange}
            onBlur={handleChange}
          >
            <Form.Control
              placeholder="Variant Allele"
              value={formData.alternate}
            />
          </Form.Group>
        </Row>

        <Row className="btn-row">
          <Button
            variant="secondary"
            onClick={() => handleButtonClick(17, 7577538, "C", "T")}
          >
            SNV Example
          </Button>

          <Button
            variant="secondary"
            onClick={() => handleButtonClick(7, 55268943, "TGAA", "T")}
          >
            Del Example
          </Button>

          <Button
            variant="secondary"
            onClick={() => handleButtonClick(7, 55210968, "A", "AAATCAGAGG")}
          >
            Ins Example
          </Button>

          <Button
            variant="primary"
            disabled={isClickable ? false : true}
            type="submit"
            onSubmit={!isClickable ? handleSubmit : null}
          >
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

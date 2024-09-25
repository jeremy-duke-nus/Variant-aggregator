import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import LoadScreen from "./LoadScreen";

const Clinvar = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [clinvarData, setClinvarData] = useState(null);
  const fetchClinvarData = async (searchData) => {
    setClinvarData(null);
    setLoading(true);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/ClinVar?chromosome=${
          searchData.chromosome
        }&position=${
          searchData.position
        }&reference=${searchData.reference.toUpperCase()}&variant=${searchData.alternate.toUpperCase()}`
      );
      const data = await response.json();
      setClinvarData(data);
      console.log(data);
    } catch (error) {
      setClinvarData(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchClinvarData(searchData);
  }, [searchData]);

  return (
    <div className="results">
      <div className="cards">
        {loading ? (
          <LoadScreen />
        ) : clinvarData === null ? (
          <Card className="clinvar-card">
            <Card.Body>
              <Card.Title>
                <h2>Clinvar overview </h2>
              </Card.Title>
              <Card.Text>
                <br></br>
                <p>
                  Clinvar version: <b>03-06-2024</b>
                </p>
                <p>
                  <h1>Not found in ClinVar</h1>
                </p>
              </Card.Text>
            </Card.Body>
          </Card>
        ) : (
          <Card className="clinvar-card">
            <Card.Body>
              <Card.Title>
                <h2>Clinvar overview </h2>
              </Card.Title>
              <Card.Text>
                <br></br>
                <p className="reduced-space">
                  Clinvar version: <b>03-06-2024</b>
                </p>
                <p className="reduced-space">
                  Variant ID: <b>{clinvarData.accession}</b>
                </p>
                <p className="reduced-space">
                  Significance: <b>{clinvarData.significance}</b>
                </p>
                <p className="reduced-space">
                  Review Status: <b>{clinvarData.criteria}</b>
                </p>
                <p className="reduced-space">
                  Phenotype: <b>{clinvarData.diseases}</b>
                </p>
                <p className="reduced-space">
                  Linkout:
                  <b>
                    {" "}
                    Click{" "}
                    <a href={clinvarData.linkout} target="_blank">
                      {" "}
                      here{" "}
                    </a>{" "}
                    to visit ClinVar page
                  </b>
                </p>
              </Card.Text>
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Clinvar;

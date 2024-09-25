import React, { useState, useEffect } from "react";
import { Card, Accordion } from "react-bootstrap";

import LoadScreen from "./LoadScreen";

import "../styles/GnomAD.css";

const GnomADCards = (data) => {
  return (
    <>
      <div className="cards">
        <Card className="full-card">
          <Card.Title>GnomAD Exome</Card.Title>
          <Card.Text>
            <p className="reduced-space">
              <b>Exome MAF:</b> {data.data.summary.exome["exome_af"]}{" "}
            </p>
            <p className="reduced-space">
              <b>Exome FAF:</b> {data.data.summary.exome["exome_faf_popmax"]}{" "}
            </p>
            <p className="reduced-space">
              <b>Exome FAF popmax:</b>{" "}
              {data.data.summary.exome["exome_faf_popmax_population"]}{" "}
            </p>
          </Card.Text>
        </Card>

        <Card className="full-card">
          <Card.Title>GnomAD Genome</Card.Title>
          <Card.Text>
            <p className="reduced-space">
              <b>Genome MAF:</b> {data.data.summary.genome["genome_af"]}{" "}
            </p>
            <p className="reduced-space">
              <b>Genome FAF:</b> {data.data.summary.genome["genome_faf_popmax"]}{" "}
            </p>
            <p className="reduced-space">
              <b>Genome FAF popmax:</b>{" "}
              {data.data.summary.genome["genome_faf_popmax_population"]}{" "}
            </p>
          </Card.Text>
        </Card>
      </div>
      <br></br>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>
            <h2>Population breakdown</h2>
          </Accordion.Header>
          <Accordion.Body>
            <div className="cards">
              {data.data.populations.map((population, index) => {
                return (
                  <Card className={population.color}>
                    <Card.Body>
                      <Card.Title>{population.id}</Card.Title>
                      <Card.Text>
                        <h2 className="gnomad-af">
                          <p className="reduced-space">
                            <b>Exome AF:</b> {population.exome}
                          </p>
                        </h2>
                        <h2 className="gnomad-af">
                          <p className="reduced-space">
                            <b>Genome AF:</b> {population.genome}
                          </p>
                        </h2>
                      </Card.Text>
                    </Card.Body>
                  </Card>
                );
              })}
            </div>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </>
  );
};
const GnomAD = ({ searchData }) => {
  const [GnomADData, setGnomADData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [warnings, setWarnings] = useState(null);

  const fetchGnomADData = async (searchData) => {
    setGnomADData(null);
    setWarnings(null);
    setLoading(true);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/GnomAD?chromosome=${
          searchData.chromosome
        }&position=${
          searchData.position
        }&reference=${searchData.reference.toUpperCase()}&variant=${searchData.alternate.toUpperCase()}`
      );
      const data = await response.json();
      setGnomADData(data);
      if (data.populations.length === 0) {
        setWarnings("No data available for this variant.");
      }
    } catch (error) {
      setWarnings("An error occurred while fetching data from the server.");
      setGnomADData(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchGnomADData(searchData);
  }, [searchData]);

  return (
    <div className="results">
      <h2>Population data from GnomAD</h2>
      {loading && !warnings ? (
        <LoadScreen string={"population data from GnomAD"} />
      ) : warnings ? (
        <div className="warning">
          <h2>{warnings}</h2>
        </div>
      ) : GnomADData ? (
        <GnomADCards data={GnomADData} />
      ) : (
        <></>
      )}
    </div>
  );
};

export default GnomAD;

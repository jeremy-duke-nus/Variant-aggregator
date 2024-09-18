import React, { useState, useEffect } from "react";
import { Table, Card, Accordion } from "react-bootstrap";
import LoadScreen from "./LoadScreen";

const OncoKb = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [oncoKbData, setOncoKbData] = useState(null);
  const fetchOncoKb = async (searchData) => {
    setOncoKbData(null);
    setLoading(true);
    try {
      const response = await fetch(
        `https://0o7ehpwg62.execute-api.ap-southeast-1.amazonaws.com/prod/oncokb-v2?hgvsg=${searchData.notation}`
      );
      const data = await response.json();
      if (data.error) {
        setOncoKbData(null);
      } else {
        if (data.code !== 401) {
          setOncoKbData(data[0]);
        } else {
          setOncoKbData(null);
        }
      }
    } catch (error) {
      setOncoKbData(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchOncoKb(searchData);
  }, [searchData]);

  return (
    <div className="results">
      <div className="cards">
        {loading ? (
          <LoadScreen />
        ) : oncoKbData === null ? (
          <Card className="oncokb-card">
            <Card.Body>
              <Card.Title>
                <h2> OncoKb results </h2>
              </Card.Title>
              <Card.Text>
                <br></br>
                <h1>Error fetching data from OncoKb</h1>
              </Card.Text>
            </Card.Body>
          </Card>
        ) : oncoKbData.code === 200 ? (
          <Card className="oncokb-card">
            <Card.Body>
              <Card.Title>
                <h2> OncoKb results </h2>
              </Card.Title>
              <Card.Text>
                <br></br>
                <p className="reduced-space">
                  This variant {oncoKbData.hotspot === "True" ? "is" : "is not"}{" "}
                  a hotspot. It is a predicted {oncoKbData.effect} mutation with
                  highest sensitivity level of {oncoKbData.sensitivity}, highest
                  diagnostic level of {oncoKbData.diagnostic}, and highest FDA
                  approval level of {oncoKbData.fda}.
                </p>
                <p className="reduced-space">{oncoKbData.description}</p>
                <br></br>
                {oncoKbData.treatments.length > 0 ? (
                  <Accordion>
                    <Accordion.Item eventKey="0">
                      <Accordion.Header>
                        <h2>Drugs</h2>
                      </Accordion.Header>
                      <Accordion.Body>
                        <Table className="insilico-tbl">
                          <thead>
                            <tr>
                              <th>Drug</th>
                              <th>Indication</th>
                              <th>Level</th>
                            </tr>
                          </thead>
                          <tbody>
                            {oncoKbData.treatments.map((drug, index) => {
                              return (
                                <tr>
                                  <td>{drug.drug}</td>
                                  <td>{drug.indication}</td>
                                  <td>{drug.fda}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </Table>
                      </Accordion.Body>
                    </Accordion.Item>
                  </Accordion>
                ) : (
                  <></>
                )}
              </Card.Text>
            </Card.Body>
          </Card>
        ) : (
          <Card className="oncokb-card">
            <Card.Body>
              <Card.Title>
                <h2> OncoKb results </h2>
              </Card.Title>
              <Card.Text>
                <br></br>
                <h1>Not found in OncoKb</h1>
              </Card.Text>
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

export default OncoKb;

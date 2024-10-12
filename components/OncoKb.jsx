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
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/OncoKb?hgvsg=${searchData.notation}`
      );
      const data = await response.json();
      if (data.error) {
        setOncoKbData({});
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

  console.log(oncoKbData);
  return (
    <div className="results">
      <div className="cards">
        {loading ? (
          <LoadScreen string={"from OncoKb using amino acid change"} />
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
                  This variant is found in {oncoKbData.gene},{" "}
                  <span className="emphasis">{oncoKbData.geneType}</span>. The
                  variant was annotated as {oncoKbData.hgvsc}, p.
                  {oncoKbData.aachange} [
                  <a href={oncoKbData.linkout} target="_blank">
                    Linkout
                  </a>
                  ] and
                  <span className="emphasis">
                    {oncoKbData.hotspot === "True" ? " is" : " is not"} a
                    hotspot
                  </span>
                  . It is a predicted{" "}
                  <span className="emphasis">{oncoKbData.effect}</span> mutation
                  with highest sensitivity level of{" "}
                  <span className="emphasis"> {oncoKbData.sensitivity}</span>,
                  highest diagnostic level of{" "}
                  <span className="emphasis">{oncoKbData.diagnostic}</span>, and
                  highest FDA approval level of{" "}
                  <span className="emphasis">{oncoKbData.fda}</span>.
                </p>

                <br></br>
                {oncoKbData.treatments.length > 0 ? (
                  <Accordion>
                    <Accordion.Item eventKey="0">
                      <Accordion.Header>
                        <h2>Variant details</h2>
                      </Accordion.Header>
                      <Accordion.Body>
                        <p className="reduced-space">
                          {oncoKbData.description}
                        </p>
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="1">
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
                <h2>{oncoKbData.message}</h2>
              </Card.Text>
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

export default OncoKb;

import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import LoadScreen from "./LoadScreen";

const PRISM = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [prismData, setPrismData] = useState(null);
  const fetchPrismData = async (searchData) => {
    setPrismData(null);
    setLoading(true);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/Prism?chromosome=${
          searchData.chromosome
        }&position=${
          searchData.position
        }&reference=${searchData.reference.toUpperCase()}&variant=${searchData.alternate.toUpperCase()}`
      );
      const data = await response.json();
      if (data.error) {
        setPrismData(null);
      } else {
        setPrismData(data);
      }
    } catch (error) {
      setPrismData(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPrismData(searchData);
  }, [searchData]);
  return (
    <div className="results">
      <div className="cards">
        {loading ? (
          <LoadScreen string={"from Prism"} />
        ) : prismData === null ? (
          <></>
        ) : (
          <>
            <hr className="divider"></hr>

            <Card className="info-card col-6-card">
              <Card.Body>
                <Card.Title>
                  <h2>SingHealth PRISM </h2>
                </Card.Title>
                <Card.Text>
                  <br></br>

                  <p>
                    Variant is{" "}
                    <b>
                      <span className="emphasis">
                        <i>
                          {prismData.results.exists === "True"
                            ? "FOUND"
                            : "NOT FOUND"}{" "}
                        </i>
                      </span>
                    </b>
                    in PRISM BEACON
                  </p>
                </Card.Text>
              </Card.Body>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default PRISM;

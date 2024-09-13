import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import LoadScreen from "./LoadScreen";
import "../styles/Cards.css";

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
          <LoadScreen />
        ) : prismData === null ? (
          <></>
        ) : (
          <Card className="prism-card">
            <Card.Body>
              <Card.Title>
                <h2>SingHealth PRISM </h2>
              </Card.Title>
              <Card.Text>
                <br></br>

                <p>
                  Variant is{" "}
                  <b>
                    <i>
                      {prismData.results.exists === "True"
                        ? "NOT FOUND"
                        : "FOUND"}{" "}
                    </i>
                  </b>
                  in PRISM BEACON
                </p>
              </Card.Text>
            </Card.Body>
          </Card>
        )}
      </div>
    </div>
  );
};

export default PRISM;

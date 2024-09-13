import React, { useState, useEffect } from "react";
import { Tab, Tabs, Table, Accordion } from "react-bootstrap";

import LoadScreen from "./LoadScreen";

import "../styles/Insilico.css";

const TabbedTable = (data) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabClick = (index) => {
    setActiveTab(index);
  };

  return (
    <div>
      <Tabs activeKey={activeTab} onSelect={handleTabClick}>
        {data.data.map((item, index) => {
          return (
            <Tab eventKey={index} title={item.hgvsc.split(":").shift()}>
              <p>
                A total of <b>{item["total_predictions"]} </b>predictions were
                made for this variant. Pathogencity is supported by{" "}
                <b className="pathogenic">
                  {item["total_pathogenic"]} ({item["percent_pathogenic"]}%){" "}
                </b>{" "}
                of the tools.
              </p>
              <Accordion>
                <Accordion.Item eventKey="0">
                  <Accordion.Header>
                    <h1>Results</h1>
                  </Accordion.Header>
                  <Accordion.Body>
                    <Table className="insilico-tbl">
                      <thead>
                        <tr>
                          <th>Tool</th>
                          <th>Description</th>
                          <th>Scores</th>
                        </tr>
                      </thead>
                      <tbody>
                        {item.predictions.map((pred, index) => {
                          return (
                            <tr>
                              <td>{pred.name}</td>
                              <td>{pred.description}</td>
                              <td className={pred.classification}>
                                {pred.scores}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </Table>
                  </Accordion.Body>
                </Accordion.Item>
              </Accordion>
            </Tab>
          );
        })}
      </Tabs>
    </div>
  );
};

const Insilico = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [InsilicoData, setInsilicoData] = useState(null);
  const fetchInsilicoData = async (searchData) => {
    setInsilicoData(null);
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/Vep?hgvsg=${searchData.notation}`
      );
      const data = await response.json();
      if (data.error) {
        setError(data);
        setInsilicoData(null);
      } else {
        setInsilicoData(data);
      }
    } catch (error) {
      setError({
        error: "An error occurred while fetching data from the server.",
      });
      setInsilicoData(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchInsilicoData(searchData);
  }, [searchData]);

  return (
    <div className="results">
      <h2>In-silico prediction tools</h2>
      {loading ? (
        <LoadScreen />
      ) : InsilicoData ? (
        <TabbedTable data={InsilicoData} />
      ) : (
        <span className="h2-error">{error?.error}</span>
      )}
    </div>
  );
};

export default Insilico;

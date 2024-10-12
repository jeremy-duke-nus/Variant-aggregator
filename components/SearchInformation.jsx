import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";

const SearchInformation = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [entrezId, setEntrezId] = useState(null);
  const fetchEntrezId = async (searchData) => {
    setEntrezId(null);
    setLoading(true);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/resources/getEntrezId?hgvsg=${searchData.notation}`
      );
      const data = await response.json();
      if (data.error) {
        setEntrezId();
      } else {
        setEntrezId(data);
      }
    } catch (error) {
      setEntrezId();
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchEntrezId(searchData);
  }, [searchData]);

  return (
    <div className="search-info">
      {searchData !== null ? (
        <Card className="info-card col-6-card">
          <Card.Title></Card.Title>
          <Card.Body>
            <Card.Text>
              <h2>Search Information</h2>
              <p className="reduced-space">
                Chromosome: chr {searchData.chromosome}
              </p>
              <p className="reduced-space">Position: {searchData.position}</p>
              <p className="reduced-space">
                Reference Allele: {searchData.reference}
              </p>
              <p className="reduced-space">
                Alternate Allele: {searchData.alternate}
              </p>
              <p className="reduced-space">
                Normalized HGVSg: {searchData.notation.replace("%3E", ">")}
              </p>
              <p>
                <b>VarSome website: </b>
                <a
                  href={`https://varsome.com/variant/hg19/${searchData.chromosome}-${searchData.position}-${searchData.reference}-${searchData.alternate}?annotation-mode=somatic`}
                  target="_blank"
                >
                  Varsome Page
                </a>
              </p>
            </Card.Text>
          </Card.Body>
        </Card>
      ) : (
        <></>
      )}
    </div>
  );
};

export default SearchInformation;

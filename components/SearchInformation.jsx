import React from "react";
import { Card } from "react-bootstrap";

const SearchInformation = ({ searchData }) => {
  return (
    <div className="search-info">
      {searchData !== null ? (
        <Card className="search-card">
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
                Normalized HGVSg: {searchData.notation.replace('%3E', '>')}
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

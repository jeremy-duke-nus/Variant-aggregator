import React from "react";
import { Card } from 'react-bootstrap';

const SearchInformation = ({searchData}) => {
    return (
        <div className="search-info">
        {searchData !== null ? (
            <Card className="search-card">
              <Card.Title>
                <h1>Search Values</h1>
              </Card.Title>
              <Card.Body>
                <Card.Text>
                  <p><b>Chromosome:</b> {searchData.chromosome}</p>
                  <p><b>Position:</b> {searchData.position}</p>
                  <p><b>Reference Allele:</b> {searchData.reference}</p>
                  <p><b>Alternate Allele:</b> {searchData.alternate}</p>
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

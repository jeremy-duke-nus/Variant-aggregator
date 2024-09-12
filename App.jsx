import { useState } from "react";
import { Row, Card } from "react-bootstrap";
import AppHeader from "./components/Header";
import SearchForm from "./components/SearchForm";
import VEPAnnotations from "./components/FunctionalAnnotations";
import GnomAD from "./components/GnomAD";
import Insilico from "./components/Insilico";
import Beacon from "./components/BEACON";
import Clinvar from "./components/Clinvar";
import PRISM from "./components/PRISM";

import "./styles/App.css";

function App() {
  const [searchData, setSearchData] = useState(null);

  return (
    <div className="App">
      <div className="header-container">
        <AppHeader />
      </div>

      <div className="form-container">
        <SearchForm searchSetter={setSearchData} />
      </div>
      <hr className="hr-light"></hr>
      <div className="result-container">
        <div className="col-left">
          <Row>
            {searchData !== null ? (
              <Card className="search-card">
                <Card.Title>
                  <h1>Search Values</h1>
                </Card.Title>
                <Card.Body>
                  <Card.Text>
                    <p>
                      <b>Chromosome:</b> {searchData.chromosome}
                    </p>
                    <p>
                      <b>Position:</b> {searchData.position}
                    </p>
                    <p>
                      <b>Reference Allele:</b> {searchData.reference}
                    </p>
                    <p>
                      <b>Alternate Allele:</b> {searchData.alternate}
                    </p>
                  </Card.Text>
                </Card.Body>
              </Card>
            ) : (
              <></>
            )}
          </Row>

          <br></br>
          <Row>
            {searchData !== null ? (
              <VEPAnnotations searchData={searchData} />
            ) : null}
          </Row>

          <Row className="card-row">
            <div className="col-3">
              {searchData !== null ? <Clinvar searchData={searchData} /> : null}
            </div>

            <div className="col-3">
              {searchData !== null ? <PRISM searchData={searchData} /> : null}
            </div>

            <div className="col-3">
              {searchData !== null ? <Clinvar searchData={searchData} /> : null}
            </div>
          </Row>

          <Row>
            {searchData !== null ? <Insilico searchData={searchData} /> : null}
          </Row>

          <Row>
            {searchData !== null ? <GnomAD searchData={searchData} /> : null}
          </Row>
        </div>

        <div className="col-right">
          {searchData !== null ? <Beacon searchData={searchData} /> : null}
        </div>
      </div>
    </div>
  );
}

export default App;

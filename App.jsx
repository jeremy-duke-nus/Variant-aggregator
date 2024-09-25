import { useState } from "react";
import { Row, Card } from "react-bootstrap";
import AppHeader from "./components/Header";
import SearchForm from "./components/SearchForm";
import SearchInformation from "./components/SearchInformation";
import VEPAnnotations from "./components/FunctionalAnnotations";
import GnomAD from "./components/GnomAD";
import Insilico from "./components/Insilico";
import Beacon from "./components/BEACON";
import Clinvar from "./components/Clinvar";
import PRISM from "./components/PRISM";
import OncoKb from "./components/OncoKb";
import GeneRif from "./components/GeneRIF";

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
      <hr className="hr-dark"></hr>
      <div className="result-container">
        <div className="col-left">
          <Row className="card-row">
            <div className="col-6">
              <Row>
                <SearchInformation searchData={searchData} />
              </Row>

              <Row>
                {searchData !== null ? <PRISM searchData={searchData} /> : null}
              </Row>
            </div>

            <div className="col-6">
              <GeneRif searchData={searchData} />
            </div>
          </Row>
          <Row>
            {searchData !== null ? (
              <VEPAnnotations searchData={searchData} />
            ) : null}
          </Row>

          <Row>
            {searchData !== null ? <OncoKb searchData={searchData} /> : null}
          </Row>
          <Row className="card-row">
            {searchData !== null ? <Clinvar searchData={searchData} /> : null}
          </Row>

          <Row className="card-row"></Row>

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

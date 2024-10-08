import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import LoadScreen from "./LoadScreen";

const GeneRif = ({ searchData }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [GeneRifData, setGeneRif] = useState(null);
  const fetchGeneInfo = async (searchData) => {
    setGeneRif(null);
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `https://3puvk2tojb.execute-api.ap-southeast-1.amazonaws.com/prod/GeneInformation?hgvsg=${searchData.notation}`
      );
      const data = await response.json();
      if (data.error) {
        setError(data);
        setGeneRif(null);
      } else {
        setGeneRif(data);
      }
    } catch (error) {
      setError({
        error: "An error occurred while fetching data from the server.",
      });
      setGeneRif(null);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchGeneInfo(searchData);
  }, [searchData]);

  return (
    <div className="gene-info">
      {loading ? (
        <LoadScreen string={"gene information from Ncbi/Entrez"} />
      ) : GeneRifData ? (
        GeneRifData.status === 200 ? (
          <Card className="gene-card">
            <Card.Body>
              <Card.Text>
                <h2>{GeneRifData.gene}</h2>
                <p className="reduced-space">
                  <b>CKBoost website: </b>
                  <a
                    href={`https://ckbhome.genomenon.com/gene/show?geneId=${GeneRifData.gene_id}&tabType=GENE_VARIANTS`}
                    target="_blank"
                  >
                    CKBoost Page
                  </a>
                </p>
                <p className="reduced-space">
                  <b>VarSome website: </b>
                  <a
                    href={`https://varsome.com/variant/hg19/${searchData.chromosome}-${searchData.position}-${searchData.reference}-${searchData.alternate}?annotation-mode=somatic`}
                    target="_blank"
                  >
                    Varsome Page
                  </a>
                </p>
                <hr />
                <p className="reduced-space">{GeneRifData.summary}</p>
              </Card.Text>
            </Card.Body>
          </Card>
        ) : (
          <Card>
            <Card.Title></Card.Title>
            <Card.Body>
              <Card.Text>
                <p className="reduced-space">{GeneRifData.summary}</p>
              </Card.Text>
            </Card.Body>
          </Card>
        )
      ) : (
        <></>
      )}
    </div>
  );
};

export default GeneRif;

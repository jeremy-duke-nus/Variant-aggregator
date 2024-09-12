import React, { useState, useEffect } from 'react';

import "../styles/Beacon.css";

const Beacon = ({searchData}) => {
    const [results, setResults] = useState(null);
    
    const GenerateURI = (searchData) => {
        const uri = `https://beacon-network.org:443/#/widget?rs=GRCh37&chrom=${searchData.chromosome}&pos=${position}&ref=${searchData.reference}&allele=${searchData.alternate}`;
        setResults(uri);
    }
    const position = parseInt(searchData.position) - 1;

    useEffect(() => {
        setResults(null);
        GenerateURI(searchData);
    }, [searchData]);

    return (
    <>
        {results !== null ? 
        <div>
            <iframe src={results} className="beaconWidget" 
                    marginwidth="0" marginheight="0" 
                    frameborder="0" vspace="0" hspace="0"
                    title='BeaconWidget' key={results}>
            </iframe>
        </div> : <p>Results not available</p>}
    </>)
}

export default Beacon;
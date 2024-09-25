import React, { useState, useEffect } from "react";
import { useTable, useSortBy, usePagination } from "react-table";
import { Accordion } from "react-bootstrap";
import LoadScreen from "./LoadScreen";

import "../styles/VEP.css";

const AnnotationTable = ({ VepAnnotations }) => {
  const columns = React.useMemo(
    () => [
      {
        Header: "Gene Symbol",
        accessor: "gene_symbol",
      },
      {
        Header: "RefSeq",
        accessor: "transcript_id",
      },
      {
        Header: "Consequence",
        accessor: "consequence_terms[0]",
      },
      {
        Header: "HGVSc.",
        accessor: "hgvsc",
      },
      {
        Header: "HGVSp.",
        accessor: "hgvsp",
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    nextPage,
    previousPage,
    canNextPage,
    canPreviousPage,
    pageOptions,
    state,
    prepareRow,
  } = useTable(
    {
      columns,
      data: VepAnnotations,
      initialState: { pageIndex: 0, pageSize: 10 },
    },
    useSortBy,
    usePagination
  );

  const { pageIndex } = state;

  return (
    <Accordion>
      <Accordion.Item eventKey="0">
        <Accordion.Header>
          <h2>Annotations</h2>
        </Accordion.Header>
        <Accordion.Body>
          <table {...getTableProps()} className="table">
            <thead>
              {headerGroups.map((headerGroup) => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map((column) => (
                    <th
                      {...column.getHeaderProps(column.getSortByToggleProps())}
                    >
                      {column.render("Header")}
                      <span>
                        {column.isSorted
                          ? column.isSortedDesc
                            ? " 🔽"
                            : " 🔼"
                          : ""}
                      </span>
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {page.map((row) => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()}>
                    {row.cells.map((cell) => (
                      <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div className="pagination">
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
              Previous
            </button>
            <span>
              Page{" "}
              <strong>
                {" "}
                {pageIndex + 1} of {pageOptions.length}{" "}
              </strong>
            </span>
            <button onClick={() => nextPage()} disabled={!canNextPage}>
              Next
            </button>
          </div>
        </Accordion.Body>
      </Accordion.Item>
    </Accordion>
  );
};

const VEPAnnotations = ({ searchData }) => {
  const [VepAnnotations, setVepAnnotations] = useState(null);
  const [error, setError] = useState({ error: "" });
  const [isLoading, setLoading] = useState(false);
  const [tableData, setTableData] = useState(null);

  const fetchVepData = async (searchData) => {
    setVepAnnotations(null);
    setTableData(null);
    setError({ error: "" });
    setLoading(true);
    try {
      const response = await fetch(
        `https://grch37.rest.ensembl.org/vep/human/hgvs/${searchData.notation}?refseq=1&hgvs=1&content-type=application/json`
      );
      const data = await response.json();
      if (data.error) {
        setError(data);
      } else {
        setVepAnnotations(data);
      }
    } catch (error) {
      setError({
        error: "An error occurred while fetching data from the server.",
      });
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchVepData(searchData);
  }, [searchData]);

  useEffect(() => {
    if (VepAnnotations !== null) {
      const flattenedData = VepAnnotations?.flatMap(
        (item) => item.transcript_consequences
      );
      setTableData(flattenedData);
    }
  }, [VepAnnotations]);

  return (
    <div className="results">
      {isLoading ? (
        <LoadScreen string={"annotations from Vep"} />
      ) : tableData !== null ? (
        <AnnotationTable VepAnnotations={tableData} />
      ) : (
        <span className="h2-error">{error.error}</span>
      )}
    </div>
  );
};

export default VEPAnnotations;

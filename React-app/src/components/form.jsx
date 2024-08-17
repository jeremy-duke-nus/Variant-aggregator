import "bootstrap/dist/css/bootstrap.min.css";
import "./Components.css";

function Form({ handleSubmit }) {
  return (
    <>
      <div className="container">
        <div className="row mt-4" key="search-form">
          <form onSubmit={handleSubmit}>
            <div className="row">
              <div className="col-md-2 mb-2">
                <select className="form-select" id="chromosome" required>
                  {Array.from({ length: 22 }, (_, index) => (
                    <option value={`chr${index + 1}`}>chr{index + 1}</option>
                  ))}
                  <option value="chrX">chrX</option>
                  <option value="chrY">chrY</option>
                </select>
              </div>
              <div className="col-md-2 mb-2">
                <input
                  type="text"
                  className="form-control"
                  id="position"
                  placeholder="Position"
                  required
                />
              </div>
              <div className="col-md-3 mb-3">
                <input
                  type="text"
                  className="form-control"
                  id="reference"
                  placeholder="Reference"
                  required
                />
              </div>
              <div className="col-md-3 mb-3">
                <input
                  type="text"
                  className="form-control"
                  id="alternate"
                  placeholder="Variant"
                  required
                />
              </div>
              <div className="col-md-2 mb-2">
                <div className="col-md-2 mb-2 button-container">
                  <div className="d-flex flex-column align-items-center">
                    <button type="submit" className="btn btn-primary">
                      Submit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default Form;

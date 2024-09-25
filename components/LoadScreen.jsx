import "../styles/Loadscreen.css";

const LoadScreen = ({ string }) => {
  return (
    <div className="loading">
      <h2>Loading {string}...</h2>
    </div>
  );
};

export default LoadScreen;

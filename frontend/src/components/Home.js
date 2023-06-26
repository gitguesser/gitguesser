import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { BACKEND_URL } from "../config";
import "./Home.css";

function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state || {};

  const [playerName, setPlayerName] = useState("");
  const [name, setName] = useState(state.repo_name || "");
  const [owner, setOwner] = useState(state.repo_owner || "");
  const [branch, setBranch] = useState(state.repo_branch || "main");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    setLoading(true);
    e.preventDefault();

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        player_name: playerName,
        repo_name: name,
        repo_owner: owner,
        repo_branch: branch,
      }),
    };

    fetch(`${BACKEND_URL}/game/`, options)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((e) => {
          throw new Error(e.detail || "Unknown error");
        });
      })
      .then((json) => {
        const gameId = json.game_id;
        navigate("game", { state: { gameId } });
      })
      .catch((e) => {
        const message = "Error occurred: " + e.message;
        console.log(message);
        setError(message);
        setLoading(false);
      });
  };

  const inputs = [
    { label: "Player name", value: playerName, onChange: setPlayerName },
    { label: "Repository name", value: name, onChange: setName },
    { label: "Repository owner", value: owner, onChange: setOwner },
    { label: "Repository branch", value: branch, onChange: setBranch },
  ];
  return (
    <>
      <h1 className="title">gitguesser</h1>
      {loading ? (
        <div className="form loading">Loading...</div>
      ) : (
        <>
          <form className="form" onSubmit={handleSubmit}>
            {inputs.map(({ label, value, onChange }, index) => (
              <div key={index}>
                <div>
                  <label htmlFor={index}>{label}:</label>
                  <br />
                  <input
                    type="text"
                    id={index}
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    required
                  />
                </div>
              </div>
            ))}
            <br />
            <button className="startButton" type="submit">
              Start game
            </button>
            <br />
            <button
              className="searchRepoButton"
              onClick={() => navigate("search")}
            >
              Search repositories
            </button>
          </form>
          <br />
          {error !== null && <div className="form">{error}</div>}
        </>
      )}
    </>
  );
}

export default Home;

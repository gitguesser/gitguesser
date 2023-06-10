import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../config";
import './Home.css';

function Home() {
  const [playerName, setPlayerName] = useState("");
  const [name, setName] = useState("");
  const [owner, setOwner] = useState("");
  const [branch, setBranch] = useState("main");
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleSubmit = (e) => {
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
      });
  };

  const inputs = [
    { label: "Player name", value: playerName, onChange: setPlayerName },
    { label: "Repository name", value: name, onChange: setName },
    { label: "Repository owner", value: owner, onChange: setOwner },
    { label: "Repository branch", value: branch, onChange: setBranch },
  ];
  return (
    < >
      <h1 className="title">gitguesser</h1>
      <br />
      <form  className="form" onSubmit={handleSubmit}>
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
            <br />
          </div>
        ))}
        <br />
        <button className="startButton" type="submit">Start game</button>
      </form>
      {error !== null && <div>{error}</div>}
    </>
  );
}

export default Home;
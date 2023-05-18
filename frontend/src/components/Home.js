import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [gameId, setGameId] = useState();
  const navigate = useNavigate();

  const startGame = () => navigate("game", { state: { gameId } });

  return (
    <>
      <h1>Home</h1>
      <div>Game id:</div>
      <input type="text" onChange={(e) => setGameId(e.target.value)} />
      <br></br>
      <br></br>
      <button onClick={startGame}>Start a game</button>
    </>
  );
}

export default Home;

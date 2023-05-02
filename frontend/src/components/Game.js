import { useLocation } from "react-router-dom";

function Game() {
  const location = useLocation();
  const state = location.state;

  return (
    <>
      <h1>Game</h1>
      <div>Game id = {state.gameId}</div>
    </>
  );
}

export default Game;

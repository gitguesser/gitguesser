import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../config";
import "./Results.css";

function Results() {
  const location = useLocation();
  const state = location.state;
  const [gameResults, setGameResults] = useState(null);
  const [repository, setRepository] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    fetch(`${BACKEND_URL}/game/${state.gameId}/results`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((e) => {
          throw new Error(e.detail || "Unknown error");
        });
      })
      .then((json) => {
        setGameResults(json);
        fetch(`${BACKEND_URL}/repository/${json.repository_id}`)
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            return response.json().then((e) => {
              throw new Error(e.detail || "Unknown error");
            });
          })
          .then((json) => {
            console.log(json);
            setRepository(json);
            setLoading(false);
          })
          .catch((e) => {
            console.log(e.message);
            setError(e.message);
            setLoading(false);
          });
      })
      .catch((e) => {
        console.log(e.message);
        setError(e.message);
        setLoading(false);
      });
  }, [state.gameId]);

  const returnHome = () => {
    navigate("/");
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Game not found.</p>;
  }

  const startTime = new Date(gameResults.start_time);
  const endTime = new Date(gameResults.end_time);
  const duration = Math.abs(endTime - startTime) / 1000;

  const formatDuration = (duration) => {
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return seconds >= 10 ? `${minutes}:${seconds}` : `${minutes}:0${seconds}`;
  };

  return (
    <>
      <h1 className="title ">{gameResults.player_name}'s game results</h1>
      {gameResults && repository && (
        <div className="container">
          <div className="repo">
            repo: {repository.owner}/{repository.name}/{repository.branch}
          </div>
          <div className="answer">
            your answer: /{gameResults.player_answer}
          </div>
          <div className="answer">
            correct answer: /{gameResults.correct_answer}
          </div>
          <div className="time">time: {formatDuration(duration)}</div>
          <div className="score">score: {gameResults.score}</div>
          <button className="buttonOK" onClick={returnHome}>
            OK
          </button>
        </div>
      )}
    </>
  );
}

export default Results;

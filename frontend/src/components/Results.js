import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { BACKEND_URL } from "../config";

function Results() {
  const location = useLocation();
  const state = location.state;
  const [gameResults, setGameResults] = useState(null);
  const [repository, setRepository] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchGameResults = async () => {
      try {
        const response = await fetch(
          `${BACKEND_URL}/game/${state.gameId}/results/`
        );
        if (response.ok) {
          const data = await response.json();
          setGameResults(data);
        } else {
          setError(true);
        }
      } catch (error) {
        setError(true);
      }
    };

    const fetchRepository = async () => {
      try {
        const response = await fetch(
          `${BACKEND_URL}/repository/${state.gameId}/`
        );
        if (response.ok) {
          const data = await response.json();
          setRepository(data);
        } else {
          setError(true);
        }
      } catch (error) {
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchGameResults();
    fetchRepository();
  }, [state.gameId]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Game not found.</p>;
  }

  const startTime = new Date(gameResults.start_time);
  const endTime = new Date(gameResults.end_time);
  const duration = Math.abs(endTime - startTime) / 1000; // Duration in seconds

  const formatDuration = (duration) => {
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return `${minutes}:${seconds}`;
  };

  return (
    <>
      <h1>{gameResults.player_name}'s game results</h1>
      {gameResults && repository && (
        <div>
          <div>
            repo: {repository.repo_owner}/{repository.repo_name}/
            {repository.repo_branch}
          </div>
          <div>your answer: {gameResults.player_answer}</div>
          <div>correct answer: {gameResults.correct_answer}</div>
          <div>time: {formatDuration(duration)}</div>
          <div>score: {gameResults.score}</div>
        </div>
      )}
    </>
  );
}

export default Results;
import { useEffect, useState } from "react";
import { useLocation} from "react-router-dom";
import { BACKEND_URL } from "../config";

function Game() {
  const [error, setError] = useState(null);
  const location = useLocation();
  const { gameId } = location.state; 
  const [playerName, setPlayerName] = useState("");
  const [repositoryId, setRepositoryId] = useState("");
  const [directories, setDirectories] = useState([]);

  const handleClickDirectory = (directoryId, repositoryId) => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    fetch(`${BACKEND_URL}/repository/${repositoryId}/tree/${directoryId}`, options)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((e) => {
          throw new Error(e.detail || "Unknown error");
        });
      })
      .then((directory) => {
        const { subdirectories } = directory;
        setDirectories(subdirectories);
      })
      .catch((e) => {
        const message = "Error occurred: " + e.message;
        console.log(message);
        setError(message);
      });
  };

  useEffect(() => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    fetch(`${BACKEND_URL}/game/${gameId}`, options)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((e) => {
          throw new Error(e.detail || "Unknown error");
        });
      })
      .then((game) => {
        const { player_name, repository_id } = game;
        setPlayerName(player_name); 
        setRepositoryId(repository_id);

        fetch(`${BACKEND_URL}/repository/${repository_id}/tree`, options)
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            return response.json().then((e) => {
              throw new Error(e.detail || "Unknown error");
            });
          })
          .then((rootDirectory) => {
            const { subdirectories } = rootDirectory;
            setDirectories(subdirectories);
          })
          .catch((e) => {
            const message = "Error occurred: " + e.message;
            console.log(message);
            setError(message);
          });
      })
      .catch((e) => {
        const message = "Error occurred: " + e.message;
        console.log(message);
        setError(message);
      });
  }, [gameId]);

  return (
    <>
      <h1>gitguesser</h1>
      Player: {playerName}
      <h2>Directories:</h2>
      <ul>
        {directories.map((directory) => (
          <li key={directory.id} onClick={() => handleClickDirectory(directory.id, repositoryId)}>
            {directory.name}
          </li>
        ))}
      </ul>
      {error && <div>{error}</div>}
    </>
  );
}

export default Game;

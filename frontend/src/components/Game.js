\import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { BACKEND_URL } from "../config";

function Game() {
  const [error, setError] = useState(null);
  const location = useLocation();
  const { gameId } = location.state;
  const [playerName, setPlayerName] = useState("");
  const [repositoryId, setRepositoryId] = useState("");
  const [directories, setDirectories] = useState([]);
  const [prevPath, setPrevPath] = useState("");
  const [currentPath, setPath] = useState("gitguesser");
  const [answer, setAnswer] = useState(null);

  const handleClickDirectory = (directoryId, repositoryId, directoryName) => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    fetch(
      `${BACKEND_URL}/repository/${repositoryId}/tree/${directoryId}`,
      options
    )
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
        setPrevPath(currentPath);
        setPath((prevPath) => `${prevPath}/${directoryName}`);
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

  const handleClickChoose = (directoryName) => {
    console.log(`Chose directory: ${directoryName}`);
    setAnswer(directoryName);
  };

  const handleSubmit = (answer) => {
    if (answer) {
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          answer: answer,
        }),
      };

      fetch(`${BACKEND_URL}/game/${gameId}`, options)
        .then((response) => {
          if (response.ok) {
            console.log("Submitted successfully");
          } else {
            throw new Error("Failed");
          }
        })
        .catch((error) => {
          console.log("Error occured:", error.message);
        });
    }
  };

  return (
    <>
      <h1>gitguesser</h1>
      Player: {playerName}
      <br />
      Current path: {currentPath}
      <h2>Directories:</h2>
      <ul>
        {directories.map((directory) => (
          <li key={directory.id}>
            <button
              onClick={() =>
                handleClickDirectory(directory.id, repositoryId, directory.name)
              }
            >
              {directory.name}
            </button>
            <button onClick={() => handleClickChoose(directory.name)}>
              Choose
            </button>
          </li>
        ))}
      </ul>
      {answer && <div>Chosen directory: {answer}</div>}
      <button type="submit" onClick={() => handleSubmit(answer)}>
        Submit
      </button>
      {error && <div>{error}</div>}
    </>
  );
}

export default Game;

import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../config";
import "./Game.css";

function Game() {
  const [error, setError] = useState(null);
  const location = useLocation();
  const { gameId } = location.state;
  const [playerName, setPlayerName] = useState("");
  const [repositoryId, setRepositoryId] = useState("");
  const [directories, setDirectories] = useState([]);
  const [pathHistory, setPathHistory] = useState([]);
  const [currentPath, setCurrentPath] = useState("/");
  const [fileName, setFileName] = useState("");
  const [showAnswer, setShowAnswer] = useState("");
  const [answer, setAnswer] = useState(null);
  const [answerSubmitted, setAnswerSubmitted] = useState(false);
  const navigate = useNavigate();

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
        setPathHistory((prevPathHistory) => [
          ...prevPathHistory,
          {
            path: currentPath,
            directories: directories,
          },
        ]);
        setCurrentPath((prevPath) =>
          prevPath === "/"
            ? `${prevPath}${directoryName}`
            : `${prevPath}/${directoryName}`
        );
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
        const { player_name, repository_id, file_name } = game;
        setPlayerName(player_name);
        setRepositoryId(repository_id);
        setFileName(file_name);

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
    setShowAnswer(currentPath);
    setAnswer(currentPath.substring(1));
  };

  const handleSubmit = (answer) => {
    if (answer != null) {
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
            setAnswerSubmitted(true);
            console.log("Submitted successfully");
            console.log(answer);
            navigate("/results", { state: { gameId } });
          } else {
            throw new Error("Failed");
          }
        })
        .catch((error) => {
          console.log("Error occurred:", error.message);
        });
    }
  };

  const handleReturn = () => {
    if (pathHistory.length > 0) {
      const previousPathEntry = pathHistory[pathHistory.length - 1];
      setDirectories(previousPathEntry.directories);
      setCurrentPath(previousPathEntry.path);
      setPathHistory((prevPathHistory) =>
        prevPathHistory.slice(0, prevPathHistory.length - 1)
      );
    }
  };

  return (
    <>
      <h1 className="title">gitguesser</h1>
      <div className="form">
        <div className="fileName">Guess location of file : {fileName}</div>
        <div className="info">
          Player: {playerName}
          <br />
          Current path: {currentPath}
        </div>
        <button className="buttonChoose" onClick={() => handleClickChoose()}>
          Choose
        </button>

        <ul>
          {directories.map((directory) => (
            <li key={directory.id}>
              <button
                className="buttonDir"
                onClick={() =>
                  handleClickDirectory(
                    directory.id,
                    repositoryId,
                    directory.name
                  )
                }
              >
                {directory.name}
              </button>
            </li>
          ))}
        </ul>
        {showAnswer && (
          <div className="chosenDir">Chosen directory: {showAnswer}</div>
        )}
        <button
          className={`backButton ${currentPath === "" ? "hidden" : ""}`}
          onClick={handleReturn}
        >
          Back
        </button>
        <button
          type="submit"
          className="buttonSubmit"
          disabled={answer === null}
          onClick={() => handleSubmit(answer)}
        >
          Submit
        </button>
        {answerSubmitted && <>Answer submitted</>}
        {error && <div>{error}</div>}
      </div>
    </>
  );
}

export default Game;

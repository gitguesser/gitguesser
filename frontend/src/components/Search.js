import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../config";
import "./Search.css";

const Search = () => {
  const [keyword, setKeyword] = useState("");
  const [allRepositories, setAllRepositories] = useState([]);
  const [repositories, setRepositories] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSearch = () => {
    setLoading(true);
    fetch(`${BACKEND_URL}/search/?query=${keyword}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((e) => {
          throw new Error(e.message || "Unknown error");
        });
      })
      .then((json) => {
        setAllRepositories(json.repos);
        const randomRepositories = getRandomRepositories(json.repos, 10);
        setRepositories(randomRepositories);
        setLoading(false);
      })
      .catch((e) => {
        const message = "Error occurred: " + e.message;
        console.log(message);
        setError(message);
        setLoading(false);
      });
  };

  const handleRepoClick = (repo) => {
    navigate("/", {
      state: {
        repo_name: repo.name,
        repo_owner: repo.owner,
        repo_branch: repo.branch,
      },
    });
  };

  const handleReroll = () => {
    const randomRepositories = getRandomRepositories(allRepositories, 10);
    setRepositories(randomRepositories);
  };

  const getRandomRepositories = (repos, count) => {
    const shuffled = repos.sort(() => Math.random());
    return shuffled.slice(0, count);
  };

  return (
    <>
      <div className="search-label">
        Enter a keyword (you can also add something like "language:python" in
        the end)
      </div>
      <input
        className="search-input"
        type="text"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
      />
      <br />
      <br />
      <button className="search-button" onClick={handleSearch}>
        Search
      </button>
      <button className="reroll-button" onClick={handleReroll}>
        Reroll
      </button>
      <button className="home-button" onClick={() => navigate("/")}>
        Home
      </button>
      <br />
      <br />
      {loading && <div>Loading...</div>}
      {!loading && error === null && (
        <ul className="repo-list">
          {repositories.map((repo, id) => (
            <li key={id} className="repo-item">
              <button
                className="select-button"
                onClick={() => handleRepoClick(repo)}
              >
                {repo.owner}/{repo.name}
              </button>
            </li>
          ))}
        </ul>
      )}
      {!loading && error !== null && (
        <div className="error-message">{error}</div>
      )}
    </>
  );
};

export default Search;

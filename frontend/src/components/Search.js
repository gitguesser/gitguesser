import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BACKEND_URL } from "../config";
import "./Search.css";

const COUNT = 10;

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
        setRepositories(json.repos.slice(0, COUNT));
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
    const newRepositories = allRepositories
      .sort(() => Math.random() - 0.5)
      .slice(0, COUNT);
    setRepositories(newRepositories);
  };

  return (
    <span className="main">
      <div>
        <h1>Search repositories</h1>
        <div className="search-label">
          Enter a keyword (you can also add something like "language:python"):
        </div>
        <input
          className="search-input"
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <br />
        <br />
        <button
          className="search-button"
          onClick={handleSearch}
          disabled={keyword === ""}
        >
          Search
        </button>
        <button
          className="reroll-button"
          onClick={handleReroll}
          disabled={allRepositories.length === 0}
        >
          Reroll
        </button>
        <button className="home-button" onClick={() => navigate("/")}>
          Home
        </button>
        <br />
        <br />
        {loading && <div className="loading">Loading...</div>}
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
      </div>
    </span>
  );
};

export default Search;

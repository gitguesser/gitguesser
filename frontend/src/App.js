import { Routes, Route } from "react-router-dom";
import Game from "./components/Game";
import Results from "./components/Results";
import Home from "./components/Home";
import Search from "./components/Search";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="game" element={<Game />} />
        <Route path="results" element={<Results />} />
        <Route path="search" element={<Search />} />
      </Routes>
    </div>
  );
}

export default App;

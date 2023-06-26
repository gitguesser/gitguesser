import { render, screen } from "@testing-library/react";
import { MemoryRouter, useLocation, useNavigate } from "react-router-dom";
import "@testing-library/jest-dom";
import Results from "../components/Results";

jest.mock("react-router-dom", () => ({
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

describe("Results component", () => {
  beforeEach(() => {
    useLocation.mockReset();
    useNavigate.mockReset();
  });

  test("displays loading message while fetching data", () => {
    useLocation.mockReturnValue({ state: { gameId: "12345" } });

    render(<Results />, { wrapper: MemoryRouter });

    const loadingMessage = screen.getByText("Loading...");
    expect(loadingMessage).toBeInTheDocument();
  });

  test("displays game results correctly", async () => {
    useLocation.mockReturnValue({ state: { gameId: "12345" } });

    const gameResults = {
      player_name: "name",
      player_answer: "player-answer",
      correct_answer: "correct-answer",
      score: 100,
      start_time: "2023-06-26T12:00:00Z",
      end_time: "2023-06-26T12:10:00Z",
      repository_id: "repository-id",
    };

    const repository = {
      owner: "owner",
      name: "repo-name",
      branch: "main",
    };

    const mockFetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(gameResults),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(repository),
      });
    global.fetch = mockFetch;

    render(<Results />, { wrapper: MemoryRouter });

    await screen.findByText("name's game results");

    expect(
      screen.getByText(
        `repo: ${repository.owner}/${repository.name}/${repository.branch}`
      )
    ).toBeInTheDocument();
    expect(screen.getByText("your answer: /player-answer")).toBeInTheDocument();
    expect(
      screen.getByText(`correct answer: /correct-answer`)
    ).toBeInTheDocument();
    expect(screen.getByText(`score: ${gameResults.score}`)).toBeInTheDocument();
    expect(screen.getByText(`time: 10:00`)).toBeInTheDocument();
  });

  test("navigates home when 'OK' button is clicked", async () => {
    const navigateMock = jest.fn();
    useLocation.mockReturnValue({ state: { gameId: "12345" } });
    useNavigate.mockReturnValue(navigateMock);

    const gameResults = {
      player_name: "name",
      player_answer: "player-answer",
      correct_answer: "correct-answer",
      score: 100,
      start_time: "2023-06-26T12:00:00Z",
      end_time: "2023-06-26T12:10:00Z",
      repository_id: "repository-id",
    };

    const repository = {
      owner: "owner",
      name: "repo-name",
      branch: "main",
    };

    const mockFetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(gameResults),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(repository),
      });
    global.fetch = mockFetch;

    render(<Results />, { wrapper: MemoryRouter });

    await screen.findByText("name's game results");

    const okButton = screen.getByText("OK");
    okButton.click();

    expect(navigateMock).toHaveBeenCalledWith("/");
  });
});

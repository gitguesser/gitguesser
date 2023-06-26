import { render, fireEvent, waitFor, screen } from "@testing-library/react";
import { MemoryRouter, useNavigate, useLocation } from "react-router-dom";
import "@testing-library/jest-dom";
import Home from "../components/Home";
import { BACKEND_URL } from "../config";

jest.mock("react-router-dom", () => ({
  useNavigate: jest.fn(),
  useLocation: jest.fn(),
}));

describe("Home component", () => {
  beforeEach(() => {
    useNavigate.mockReset();
    useLocation.mockReset();
  });

  test("renders the form with inputs", () => {
    useLocation.mockReturnValue({
      state: {},
    });
    render(<Home />, { wrapper: MemoryRouter });
    const inputs = screen.getAllByRole("textbox");
    expect(inputs.length).toBe(4);
  });

  test("navigates to the search page when 'Search repositories' button is clicked", () => {
    const navigateMock = jest.fn();
    useNavigate.mockReturnValue(navigateMock);
    useLocation.mockReturnValue({
      state: {},
    });

    render(<Home />, {
      wrapper: MemoryRouter,
    });

    const searchButton = screen.getByText("Search repositories");
    fireEvent.click(searchButton);

    expect(navigateMock).toHaveBeenCalledWith("search");
  });

  test("submits the form and navigates to the game page", async () => {
    const navigateMock = jest.fn();
    useNavigate.mockReturnValue(navigateMock);

    const gameId = "12345";
    const responseJson = { game_id: gameId };
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(responseJson),
    });
    global.fetch = mockFetch;
    useLocation.mockReturnValue({
      state: {},
    });

    render(<Home />, {
      wrapper: MemoryRouter,
    });

    const playerNameInput = screen.getByLabelText("Player name:");
    const repoNameInput = screen.getByLabelText("Repository name:");
    const repoOwnerInput = screen.getByLabelText("Repository owner:");
    const repoBranchInput = screen.getByLabelText("Repository branch:");
    const startButton = screen.getByText("Start game");

    fireEvent.change(playerNameInput, { target: { value: "name" } });
    fireEvent.change(repoNameInput, { target: { value: "example-repo" } });
    fireEvent.change(repoOwnerInput, { target: { value: "example-owner" } });
    fireEvent.change(repoBranchInput, { target: { value: "main" } });
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(`${BACKEND_URL}/game/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          player_name: "name",
          repo_name: "example-repo",
          repo_owner: "example-owner",
          repo_branch: "main",
        }),
      });
    });
    await waitFor(() => {
      expect(navigateMock).toHaveBeenCalledWith("game", {
        state: { gameId },
      });
    });
  });

  test("displays error message when form submission fails", async () => {
    const errorDetail = "Game not found.";
    const responseJson = { detail: errorDetail };
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve(responseJson),
    });
    global.fetch = mockFetch;
    useLocation.mockReturnValue({
      state: {},
    });

    render(<Home />, { wrapper: MemoryRouter });

    const startButton = screen.getByText("Start game");
    fireEvent.click(startButton);

    await waitFor(() => {
      const errorElement = screen.getByText("Error occurred: " + errorDetail);
      expect(errorElement).toBeInTheDocument();
    });
  });
});

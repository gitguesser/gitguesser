import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { MemoryRouter, useLocation, useNavigate } from "react-router-dom";
import Game from "../components/Game";

jest.mock("react-router-dom", () => ({
  useLocation: jest.fn(),
  useNavigate: jest.fn(),
}));

describe("Game", () => {
  beforeEach(() => {
    useLocation.mockReturnValue({ state: { gameId: "123" } });
  });

  it("fetches game data and renders correctly", async () => {
    const navigateMock = jest.fn();
    useNavigate.mockReturnValue(navigateMock);

    render(<Game />, { wrapper: MemoryRouter });

    expect(screen.getByText(/Guess location of file:/)).toBeInTheDocument();
    expect(screen.getByText(/Player:/)).toBeInTheDocument();
    expect(screen.getByText(/Current path:/)).toBeInTheDocument();
    expect(screen.getByText(/Choose/)).toBeInTheDocument();
    expect(screen.getByText(/Back/)).toBeInTheDocument();
    expect(screen.getByText(/Submit/)).toBeInTheDocument();
    expect(screen.queryByText(/Chosen directory:/)).toBeNull();
    expect(screen.queryByText(/Answer submitted/)).toBeNull();
    expect(screen.queryByText(/Error occurred/)).toBeNull();
    expect(screen.queryByText(/Loading.../)).toBeNull();
  });

  it("handles click on back button and goes back to previous directory", async () => {
    const navigateMock = jest.fn();
    useNavigate.mockReturnValue(navigateMock);

    render(<Game />, { wrapper: MemoryRouter });

    const chooseButton = screen.getByText(/Choose/);
    fireEvent.click(chooseButton);

    const backButton = screen.getByText(/Back/);
    fireEvent.click(backButton);

    expect(screen.getByText(/Current path:/)).toHaveTextContent(
      "Player: Current path:"
    );
  });
});

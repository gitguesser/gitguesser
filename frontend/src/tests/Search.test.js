import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, useNavigate } from "react-router-dom";
import "@testing-library/jest-dom";
import Search from "../components/Search";

jest.mock("react-router-dom", () => ({
  useNavigate: jest.fn(),
}));

describe("Search", () => {
  it("renders the search component", () => {
    render(<Search />, { wrapper: MemoryRouter });

    expect(screen.getByText("Search repositories")).toBeInTheDocument();
    expect(screen.getByText("Search")).toBeInTheDocument();
    expect(screen.getByText("Reroll")).toBeInTheDocument();
    expect(screen.getByText("Home")).toBeInTheDocument();
  });

  it("performs a search and displays repositories", async () => {
    const mockRepositories = [
      { owner: "owner1", name: "repo1" },
      { owner: "owner2", name: "repo2" },
    ];

    const mockResponse = {
      ok: true,
      json: () => Promise.resolve({ repos: mockRepositories }),
    };

    const mockFetch = jest.fn().mockResolvedValue(mockResponse);
    global.fetch = mockFetch;

    render(<Search />, { wrapper: MemoryRouter });

    const keywordInput = screen.getByRole("textbox");
    const searchButton = screen.getByText("Search");

    fireEvent.change(keywordInput, { target: { value: "react" } });
    fireEvent.click(searchButton);

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/search/?query=react")
    );

    await screen.findByText("owner1/repo1");
    expect(screen.getByText("owner1/repo1")).toBeInTheDocument();
    expect(screen.getByText("owner2/repo2")).toBeInTheDocument();
  });

  it("handles error when search fails", async () => {
    const mockResponse = {
      ok: false,
      json: () => Promise.resolve({ message: "Search failed" }),
    };

    const mockFetch = jest.fn().mockResolvedValue(mockResponse);
    global.fetch = mockFetch;

    render(<Search />, { wrapper: MemoryRouter });

    const keywordInput = screen.getByRole("textbox");
    const searchButton = screen.getByText("Search");

    fireEvent.change(keywordInput, { target: { value: "react" } });
    fireEvent.click(searchButton);

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/search/?query=react")
    );

    await screen.findByText("Error occurred: Search failed");
    expect(
      screen.getByText("Error occurred: Search failed")
    ).toBeInTheDocument();
  });

  it("navigates to home when Home button is clicked", () => {
    const navigateMock = jest.fn();
    useNavigate.mockReturnValue(navigateMock);

    render(<Search />, { wrapper: MemoryRouter });

    const homeButton = screen.getByText("Home");
    fireEvent.click(homeButton);

    expect(navigateMock).toHaveBeenCalledWith("/");
  });
});

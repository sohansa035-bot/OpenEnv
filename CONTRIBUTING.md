# Contributing to OpenEnv

First off, thank you for considering contributing to OpenEnv! It's people like you that make OpenEnv such a great tool.

## 1. Local Setup Instructions

To get the environment running locally for development:

1. **Fork & Clone:**
   Fork the repository on GitHub and clone it to your local machine.
   ```bash
   git clone https://github.com/<your-username>/OpenEnv.git
   cd OpenEnv
   ```

2. **Install Dependencies:**
   We use `uv` for dependency management.
   ```bash
   uv sync
   ```

3. **Run the Server Locally:**
   ```bash
   uv run uvicorn server.app:app --port 8000 --reload
   ```

## 2. Coding Style Guidelines

To keep the codebase readable and maintainable, please follow these guidelines:

*   **Python:** We adhere to [PEP 8](https://peps.python.org/pep-0008/). Please use `ruff` or `black` for formatting.
*   **Type Hinting:** Ensure all new functions and methods have proper Python type hints.
*   **Documentation:** Update the `README.md` and inline docstrings when adding new features or making structural changes.

## 3. Pull Request (PR) Process

1. **Create a branch:** Create a descriptive branch for your feature or bug fix (e.g., `feature/add-new-scenario` or `fix/memory-leak`).
2. **Commit your changes:** Make sure your commit messages are clear and concise.
3. **Run tests:** Ensure any existing tests pass and add new ones if necessary.
4. **Push & PR:** Push your branch to your fork and submit a Pull Request to the `main` branch. 
5. **Review:** A maintainer will review your PR. Be prepared to respond to feedback and make necessary adjustments.

We look forward to your contributions!

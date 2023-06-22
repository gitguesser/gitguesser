# gitguesser

[![Testing](https://github.com/gitguesser/gitguesser/actions/workflows/test.yml/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gitguesser/gitguesser/main.svg)](https://results.pre-commit.ci/latest/github/gitguesser/gitguesser/main)
[![Generate docs](https://github.com/gitguesser/gitguesser/actions/workflows/docs.yml/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/docs.yml)
[![Deploy pages](https://github.com/gitguesser/gitguesser/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/pages/pages-build-deployment)

## Docs
The API docs are available [here](https://gitguesser.github.io/gitguesser/).

## Configuration

Environment variables are used to manage application settings.
Alternatively, you can store them in configuration files located in the
project's root directory. The default configuration file is `.env`.

The following variables are required:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `POSTGRES_DB`

The following variables are optional:
- `GITHUB_USERNAME`
- `GITHUB_TOKEN`

However, it is strongly recommended to provide them, as they can increase the GitHub API rate limit.

Here is an example of a valid configuration file:
<details>
<summary>Click to expand</summary>

```bash
POSTGRES_USER=gitguesser
POSTGRES_PASSWORD=gitguesser
POSTGRES_PORT=5432
POSTGRES_DB=gitguesser_db
```
</details>

## Using pre-commit for style checking (auto formatting)

Install `pre-commit`:
```
pip install pre-commit
```

Install the git hook scripts:
```
pre-commit install
```

Run on all files manually:
```
pre-commit run --all-files
```

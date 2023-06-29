# gitguesser

[![Testing](https://github.com/gitguesser/gitguesser/actions/workflows/test.yml/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gitguesser/gitguesser/main.svg)](https://results.pre-commit.ci/latest/github/gitguesser/gitguesser/main)
[![Generate docs](https://github.com/gitguesser/gitguesser/actions/workflows/docs.yml/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/docs.yml)
[![Deploy pages](https://github.com/gitguesser/gitguesser/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/gitguesser/gitguesser/actions/workflows/pages/pages-build-deployment)


## Screenshots
<summary>During game</summary>

![During game Screenshot](https://i.imgur.com/4SmzdSD.png)

<details>
<summary>Game start</summary>

![Game start Screenshot](https://i.imgur.com/5Cjzl7D.png)
</details>

<details>
<summary>Search repositories</summary>

![Search repositories Screenshot](https://i.imgur.com/t1Aq8wW.png)
</details>

<details>
<summary>Game results</summary>

![Game results Screenshot](https://i.imgur.com/8TRja4o.png)
</details>

## Docs
The API docs are available [here](https://gitguesser.github.io/gitguesser/).

## UML diagrams

<details>
<summary>Docker services</summary>

![Docker services UML](https://www.plantuml.com/plantuml/svg/LP2z2iCW4CVtUuhZzWIXIwUGeUzH_BYKa4H5RPRITw-Hn288v_t-7yEDCScGtjiANkf5lXZfuVJ20IE7VTOS2J-0gDtcdMMRa8mYb16DQh7AURQcQEU_DKp1sNGvhYLRyflcbP5wjdiHytmU2Bu0Hc7N3RNnd8NLZahxVlY7ZMhtnaNUXOHt8GH1wMc5Mn5WpFIupGy0)
</details>

<details>
<summary>Game</summary>

![Game UML](https://www.plantuml.com/plantuml/svg/RP0nRiCm34LtdeB8tWjaAD8flK0FGCkiJK2MLEghHMvVAqQDniYauJy-Vl5I8OwsH28Oel9L5YMIWEpyKTLPAhVrfI8E2rOaWKzlfKGB0ilfr0afvH6u6jxRSCycmzm68keQVddjy9chHWrWrvAh8VkDf9IURlYPlvhwxL_Eeq1eItUBAvgd8_MdwWjtPf95ULI8nKenvqBC_50foRTDWfKorz1j7KaPocxJ3CwV6uXPZolPAWS9iuviwGwCGvz-rcJNRsKrZOVJj64niAJwe_xqBwwrHLIwhBDjYRy0)
</details>


<details>
<summary>Search repositories</summary>

![Search repositories UML](https://www.plantuml.com/plantuml/svg/TOzBJiGm38RtFeKrUoum2pIiO8yuW2Tr6qjf71n7exaz2LH0X5ZLjR__aKjrCczx0d3nnFZAP26YST4ghYPS0IZq2Tyg6rB5rhzGkao25CgEfwTIaWHoqNmQ19Ko0y_YB-twUTl4Oxi2mB31XyS1d_6ziTsXZtrp86TSrMvaot7ysduhZBrPnfqyHCdRtFWm6X5dh55lcAGwwZfZIRK08avLZ7lUW3sopNn7_pfd_iUTyp8_idBYu3_GVUvfl8WDm1MZxbneOwIyu2ef_LBrVqvBXKiFQ7lw0000)
</details>

## Running

You need to have Docker installed. Then simply run the following command:
```
docker compose up --build
```

## Testing

Testing backend:
```
docker compose exec -w /backend backend pytest
```
Testing frontend:
```
docker compose exec -e CI=true -w /frontend frontend npm test
```
The backend tests will not work unless you provide a GitHub token first.

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
```bash
POSTGRES_USER=gitguesser
POSTGRES_PASSWORD=gitguesser
POSTGRES_PORT=5432
POSTGRES_DB=gitguesser_db
```

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

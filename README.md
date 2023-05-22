# gitguesser

## CONFIGURATION

Environment variables are used to manage application settings. 
Alternatively, you can store them in configuration files located in the 
project's root directory. The default configuration file is `.env`. During 
testing with `pytest`, the configuration is read from `.env.test`.

The following variables are required:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_SERVER`
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
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=gitguesser_db
```
</details>

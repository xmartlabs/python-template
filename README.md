# Xmartlabs Python Template

![python version](https://img.shields.io/badge/python-3.13-brightgreen)
![fastAPI version](https://img.shields.io/badge/fastapi-0.95.2-brightgreen)


## Components
- Rest API built with FastAPI and SQLAlchemy
- PostgreSQL database

## Project setup

The only things you need are [Docker](https://docs.docker.com/engine/install/), [Docker Compose](https://docs.docker.com/compose/install/), and a code editor with devcontainer support like [Visual Studio Code](https://code.visualstudio.com/download). Once you open the template with VS Code, it will recommend that you install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) if you don’t have it already. Then, a pop-up will appear to reopen the template in the devcontainer, or you can use `Ctrl / Cmd + shift + P` -> `Dev Containers: Open Folder in Container…`. Remember to add the `.env` file at the root folder; you can use `.env.example` as a reference.

And that's it, everything is ready to use. By using the VS Code terminal with `Ctrl / Cmd + J`, you'll be inside the container to run any command or start the server with `uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`.

You can connect to the container once it's running using `scripts/exec.sh bash` and execute commands from another terminal outside of VS Code. Also, for all the following commands that can be run inside the dev container, you can run `scripts/exec.sh {command}` from outside the container.

Once the containers and server are running, you can go to `http://localhost:8000/docs` to see the automatic interactive API documentation.

In case you don't to use VS Code and dev containers, or you want to set up the environment in a different way. You can use the `Dockerfile` in the root of the repository to create the image with everything needed to run the project. The `docker-compose.yaml` and `.env.example` files in the `.devcontainer` folder serve as references for recreating other services like the database. Also, you will need to run the `poetry install --no-ansi --no-root` command manually to install all the required dependencies.

Alternatively, you must have:

- `Python >3.13`
- [Poetry](https://python-poetry.org/docs/#installation) (don't forget to install the dependencies from the lock file)
- [PostgreSQL](https://www.postgresql.org/) database, setting the corresponding environment variables for the database connection.

### Customization

The project's name (`python-template`) can be edited following next steps:

1. Edit project's name in the [pyproject.toml](pyproject.toml) file
2. Set `PROJECT_NAME` env variable to be exactly the same as project's name in pyproject.toml. Ensure VSCode has this
variable loaded, otherwise the dev container might fail or not work as expected. You can open VScode with from cmd with:

```bash
PROJECT_NAME=your-awesome-project code <path/to/repo>
```


## Migrations

We use Alembic as database migration tool. You can run migration commands directly inside the dev container or use the provided shortcut in the `exec.sh` script.

- `migrate` – Runs all migrations.
- `makemigrations` – Compares the current database state with the table metadata and generates the necessary migration files.


## Code tools
Linters, formatters, etc.

- **Pycln**: Formatter for finding and removing unused import statements.
- **isort**: Tool to sort imports alphabetically and automatically separate into sections by type.
- **flake8**: Linting tool
- **mypy**: Static type checker
- **black**: PEP 8 compliant opinionated formatter

There is a shortcut under the `/scripts` directory that runs all this tools for you (`./exec.sh format`) or just run `format` inside the dev container.

![Screenshot](.docs/images/format.png)

## Tests
We use FastAPI's `TestClient` and `pytest` for testing. `./exec.sh test` shortcut can be used to run all tests or just `test` inside the dev container.

## Shell
You can start an interactive Python shell inside the dev container in two ways:

1. Simply run `shell` inside the container.
2. Alternatively, use the `exec.sh shell` command.

The shell provides some useful pre-imported stuff:

- `session`: A SQLAlchemy `Session` object
- `settings`: An instance of the app settings class
- All the SQLAlchemy models classes

![Screenshot](.docs/images/shell.png)

## Admin
The template includes an admin interface via [SQLAdmin](https://github.com/aminalaee/sqladmin). It's a flexible admin that can be configured in many ways.

*One note: You should be careful when adding relationships to the list or detail pages (specially large many-to-many / one-to-many relationships), because it's not very optimal in terms of DB querys in those cases (all the related objects would be loaded in memory).*

![Screenshot](.docs/images/admin.png)

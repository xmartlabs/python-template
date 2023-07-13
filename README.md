# Recsys Backend

## Components
- Rest API built with FastAPI and SQLAlchemy
- PostgreSQL database

## Project setup
You only need to install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/). 
To start the containers, just run `docker-compose up` (or `docker-compose up -d` if you want to run the containers in background); or `docker-compose create` and `docker-compose start` if you don't want to see the logs. 
When the containers are running, you can go to `http://localhost:8000/docs` to see the automatic interactive API documentation.

## Migrations
We use Alembic as database migration tool. To run its commands you can open an interactive shell inside the backend container, or use the following shortcuts under the `/scripts` directory:
- `./exec.sh migrate` -> runs all the migrations
- `./exec.sh makemigrations` -> compares the actual status of the DB against the table metadata, and generates the migrations based on the comparison

## Database initial load
1. Download the `movie_features.parquet` file from [this link](https://drive.google.com/file/d/1hM_j-UL8UGRZyNZntZG0tRXLJOluFpqc/view?usp=sharing)
2. Store the file on the following directory: `ml/data/preprocessed`
3. Initiate the backend database service
4. Run database migrations
5. Run the initial load: `./exec.sh load` in the `/scripts` directory

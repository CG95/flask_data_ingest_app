# How to install

## Using docker compose

docker-compose up -d
this installs the containers and starts the app if the csv files to be ingested are already put in their respective folders

## Import the csv files

To import the csv files before running the docker-compose command put the files on /data/ for the app and /tests/data for the unit tests.

## Environment variables needed

A .env file is needed to store the environment variables or setting the environment variables directly in the terminal

The variables to be set are:

- `DATABASE_URL` : the postgres connection string, e.g., postgresql://myuser:mypassword@postgresql/mydbname
- `POSTGRES_USER`: myuser
- `POSTGRES_PASSWORD`: mypassword
- `POSTGRES_DB` : mydbname
- `CACHE_REDIS_HOST`: the redis connection string, e.g., redis://redis:6379/0

## Generate csv data

There are sample csv files already included, but if you want to test with more data
just edit the variables NUM_SALES and NUM_SALES_TEST on generate_csv_data.py and run it

python generate_csv_data.py

## Swagger documentation of the API

You can consult the API documentation on
http://localhost:5000/swagger-ui

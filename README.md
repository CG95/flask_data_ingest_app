## How to install

# Using docker compose 
docker-compose up -d
this installs the containers and starts the app if the csv files to be ingested are already put in their respective folders

# Import the csv files
To import the csv files before running  the docker-compose command put the files on /data/ for the app  and   /tests/data for the unit tests.

# A .env file is needed to store the environment variables or setting the environment variables directly in the terminal
# The variables to be set are:
- `DATABASE_URL`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `CACHE_REDIS_HOST`

# Generate csv data 
If you need to generate the csv files to run the project use the generate_csv_data.py script, 
which will generate the csv files for the app and the unit tests

python generate_csv_data.py

# Swagger documentation of the API
You can consult the API documentation on
http://localhost:5000/swagger-ui

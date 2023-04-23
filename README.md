# KrakenFlex Back End Test

This repo implements a library that calls the Krakenflex test API to retrieve outages, 
filter them based on occurence time and occurence site, annotate them with the relevant
device names, and post the filtered annotated outages back to the API.

## Setup
To set up your python environment, install `poetry` following the instructions [here](https://python-poetry.org/docs/#installation). 
Then run `poetry install` from the project root to create a virtual environment and install the required dependencies.

You also need to add your API key to the `config.ini` file.

## How to run
From the project root, run
```
poetry run python main.py
```

## Running tests
```
poetry run pytest
```

## Linting
```
poetry run black .
poetry run isort .
```

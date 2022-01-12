# ase-project-backend

## Setup and Installation

### Python

We will use `python 3.8`, all of the required dependencies are included in `requirements.txt`.
Please use an environment manager (conda).
To install all dependencies, `pip install -r requirements.dev.txt`.

**When we run into problems that require new libraries, be sure to add them to `requirements.txt`!!!**

### External Requirements

### Env Variables
For now, we will use a preset public and private key for accessing external APIs... Please don't commit them!
The keys will be included in a `.env` file, which will be read using Pydantics `BaseSettings` class. More on this later...

### Local Dev Environment
I don't know how to use Black Linter with anything else other than VSCode, if you can set it up, go ahead.
Here's how to do it with VSCode.
```
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
```
Include this in your `.vscode/settings.json`
If you use pycharm then follow this [guide](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea).

As a rule: never commit your local IDE setting to this repository.

### Pre-commit

We have a pre-commit configuration that you can use to ensure that your code is formatted properly and passes flake8 (lint) checks before it is even committed. In order to set up pre-commit you need to install it locally, check instructions [here](https://pre-commit.com/#intro).

### FastAPI

We use [Fast API](https://fastapi.tiangolo.com/) as a server framework to serve requests, it is recommended to familiarize yourself with it before you dive into the code. Things will make more sense this way 🙂.

As a type validation, Fast API uses the [Pydantic](https://pydantic-docs.helpmanual.io/) library - which allows us to validate inputs and outputs and provide stricter typing that the python standard.

### Start the application

In order to start the app, and once your environment is activated and ready, simply run: `uvicorn server.main:app --reload`. Note that you will need to have installed the `uvicorn` server. You can pass in other parameters here to control the port and other configurations (the default port is 8000). Using the `--reload` flag will automatically reload the server after changes to the code are made.

You can also run the app inside vscode to allow for interactive debugging by running the command in debugging mode.

Once the app is started you should see the url where it is served as:
`Uvicorn running on http://127.0.0.1:8000`

If you then navigate to `http://127.0.0.1:8000/docs` you will be able to see all the routes that the API offers.

### Using Docker

We use Docker when deploying the application in order to maintain a clean and scalable environment. Docker

Install [docker](https://docs.docker.com/get-docker/) locally in order to be able to build and run the Docker file and container.

Once you have installed docker you can then build the image by running `docker build -t backend-app .`. This builds the docker image with the tag `backend-app`. The first time you do this, it might take some time to build as the image will need to download and install all dependencies.

To run the image after building you can run `docker run -it backend-app`. This runs the docker in interactive mode so you will be able to see environment logs. Depending on your local setup, this setup might not work due to missing environment variables - you need to ensure that you are passing these to the docker container on `run` - see more [here](https://docs.docker.com/engine/reference/commandline/run/).

## Running Tests and Code Quality

In order to run the test suite you can call `pytest` or `python -m unittest discover test` from the main directory.

New functionalities need to be unit tested to insure high coverage and reproducibility.

Test coverage is measured using `pytest-cov` and reported on any new MR.

## Contributing
Please make your own branch!
Contribution must be done via Pull Requests and merge with the `main` branch. This allows us to do code review, but also run unit tests and linting checks on the code itself.

Commit messages must try to follow the [conventional commits message format](https://www.conventionalcommits.org/en/v1.0.0-beta.2/).
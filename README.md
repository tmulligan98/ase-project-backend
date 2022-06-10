# ase-project-backend

## What's this?
The backend for our group's Disaster Management System

## Setup and Installation

### Python

We will use `python 3.8`, all of the required dependencies are included in `requirements.txt`.
Please use an environment manager (conda) or virtualenv to keep the dependencies of the project separate.
Install and create a virtual environment.

`pip install virtualenv`

`virtualenv .env`

`source .env/bin/activate`

To install all dependencies, 

`pip install -r requirements.dev.txt`.

**When we run into problems that require new libraries, be sure to add them to `requirements.txt`!!!**

### External Requirements

### Env Variables
For now, we will use a preset public and private key for accessing external APIs... Please don't commit them!
The keys will be included in a `.env` file, which will be read using Pydantics `BaseSettings` class. More on this later...

### Local Dev Environment
Add these lines in your vscode settings file to enable  support for code linting
```
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
```
Include this in your `.vscode/settings.json`
If you use pycharm then follow this [guide](https://black.readthedocs.io/en/stable/editor_integration.html#pycharm-intellij-idea).

As a rule: never commit your local IDE setting to this repository.


### Environment Variables
**What are these?**
These are variables used througout our system. For example, an access key to a given API
We will use a `.env` file to store out env variables. This file is read using the Pydantic `BaseSettings` class, which will contain secrete access keys for external APIs, such as TomTom. Any local environment values will be overwritten by those in the `.env` file.
For security reasons, the `.env` file is excluded from git.

For our application to work, you will need to create a `.env` file with the following environment variable(s):

    -TOM_TOM_ACCESS_Key
    -DATABASE_URL
    -DB_USER
    -DB_PASSWORD
    -DB_NAME
    -PGADMIN_EMAIL
    -PGADMIN_PASSWORD
    -AUTH_SECRET_KEY
    -CRYPTO_ALGORITHM

This `.env` file will be submitted as part of the submission and not included in this git repository for security purposes.

### Pre-commit

We have a pre-commit configuration that you can use to ensure that your code is formatted properly and passes flake8 (lint) checks before it is even committed. In order to set up pre-commit you need to install it locally, check instructions [here](https://pre-commit.com/#intro).

### FastAPI

We use [Fast API](https://fastapi.tiangolo.com/) as a server framework to serve requests, it is recommended to familiarize yourself with it before you dive into the code. Things will make more sense this way 🙂.

As a type validation, Fast API uses the [Pydantic](https://pydantic-docs.helpmanual.io/) library - which allows us to validate inputs and outputs and provide stricter typing that the python standard.



### Using Docker

We use Docker when deploying the application in order to maintain a clean and scalable environment. Docker

Install [docker](https://docs.docker.com/get-docker/) locally in order to be able to build and run the Docker file and container.

To run it make sure you have docker desktop running in your local machine and after creating the virtual environment and installing all the updated dependencies from requirements.txt use the following commands to setup the containers:

**Locally**
to run the application
`docker-compose --env-file ./.env up --build`
- Make sure you have a file called .env containing the required env variables in the same directory.Copy this file from our submission
- It will take some time to load it up
- After you can see the backend app starting on 0.0.0.0:8000/

If you then navigate to `http://0.0.0.0:8000/docs` you will be able to see all the routes that the API offers.
and to validate if the instance is connected to database, run:-

`docker exec -it postgresql_db bash`
,
and you will be entered in a postgresql shell.

`docker-compose down --volumes`

to reset


## Contributing
Please make your own branch!
Contribution must be done via Pull Requests and merge with the `main` branch. This allows us to do code review,and also run unit tests and linting checks on the code itself.

Commit messages must try to follow the [conventional commits message format](https://www.conventionalcommits.org/en/v1.0.0-beta.2/).

# CI/CD for Simple React-Flask Note-Taking App

The point of this project was to create a simple app that could be used to self-teach CI/CD, iteratively building on the app witht eh help of an automted CI/CD pipeline.

## Pipeline

* The backend Python code for Flask is linted using `flake8` to promote style adherence
* Unit tests are written using `pytest`, `pytest-mock` and `jest` libraries then ran before merging with main branch
* Jenkins pulls code from GitHub and builds Docker image from source code
* Deploy to Render (https://render.com/)

### Linting and Unit Tests
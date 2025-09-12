# CI/CD for React-Flask Note-Taking App

This project was created to simulate interative development of a full-stack application, with the support of an automated CI/CD pipeline.

## Infrastructure

### Frontend
![JavaScript](https://shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=000&style=flat-square)
![React](https://img.shields.io/badge/-ReactJs-61DAFB?logo=react&logoColor=white&style=flat-square)
![Jest](https://img.shields.io/badge/Jest-323330?style=flat-square&logo=Jest&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-green?logo=pytest&style=flat-square)

### Database
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=flat-square&logo=postgresql&logoColor=white)

### CI/CD
![Docker](https://img.shields.io/badge/docker-257bd6?style=flat-square&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?logo=jenkins&logoColor=white&style=flat-square)
![Render](https://img.shields.io/badge/Render-0099E5?logo=render&logoColor=white&style=flat-square)


## Pipeline

* Unit tests are run on `git commit` using Github Actions
* When a feature is complete, a **Pull Request** is made to merge the branch with main
  * Triggers GitHub Actions unit test before merge
* Jenkins pulls code from GitHub on merge with main
  * Builds Docker image from source code
  * Unit and integration tests run using Docker Compose
  * Images pushed to Docker Hub if tests pass
* Deploy to Render (https://render.com/)
  * Render pulls Docker images from Docker Hub
  * Deploys application with new feature 

### Unit Tests


## How to Run

## Architecture

## Approach & What I've Learnt



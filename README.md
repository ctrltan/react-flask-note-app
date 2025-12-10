# NoteTogether: React-Flask Note-Taking App

Live Link: https://note-together.onrender.com/

This is NoteTogether! A note-taking app with collaborative note-taking capabilities! Using a React client and a Flask API, users are able to create, edit, delete and share notes with other users. Using an Agile development process, I am able to implement new features and their UI along with unit tests!

## Infrastructure

### Backend
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-green?logo=pytest&style=flat-square)

### Frontend
![JavaScript](https://shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=000&style=flat-square)
![React](https://img.shields.io/badge/-ReactJs-61DAFB?logo=react&logoColor=white&style=flat-square)
<!--- ![Jest](https://img.shields.io/badge/Jest-323330?style=flat-square&logo=Jest&logoColor=white) --->

### Database
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://shields.io/badge/supabase-black?logo=supabase&style=flat-square)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

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

## Approach & What I've Learnt
**Database Management across Dev, Testing and Production Environments**

When developing locally, my approach was to create and delete a test table within a fixture for the backend unit tests. When implementing the first part of continuous integration with GitHub actions, I found that connecting to my locally hosted PostgreSQL DB would need to be set up in the GitHub actions virtual environment too.

My approach to this problem is to use a containerised PostgreSQL database with Docker for local development and testing (locally + GitHub): 
- This eliminates the need for dependency setup in both environments
- Easy to spin up the container and tear it down once tests are complete
- Simpler maintenance e.g. upgrading PostgreSQL in one place and not in each environment

✅ Successful!

**Authentication, Sessions and Simplified API requests**

Currently, the application protects user notes and enables single-user modidification by using `user_id` and `note_id` specific endpoints. After logging in, the API server sends the user's id and username back to the client to be used in future requests. A JWT token would also be sent to the client and used in requests to confirm the user making requests is authenticated. This was a method I used in a previous project.

Users should be able to use clean urls to make requests to the endpoint without the possibility of access to another user's data. There should also be a method to manage the JWT access token's lifecycle with a refresh token. Access should also be revocable if the user logs out, however, logging out on one device should not end the session on other devices.

My approach to this problem is to generate short-lived access and long-lived refresh JWT tokens. The access token payload will include the token expiry date, `user_id` and other identifiers necessary for requests. Each login will have its own refresh and access tokens to ensure same-account logins across devices and browsers and independent. Using a key-value cache such as Redis, the refresh token will be obtained using the login id as a key once the access token expires:
- Protects user ids and allows for cleaner URLs
- Simplifies authentication
- Allows for future scalability e.g. decomposition of backend into services with Redis cache as its own independently scalable service

✅ Successful!

**Near-Real Time Note Autosaving for Improved Database Performance**

The current approach for the app is for users to manually save notes after edits, writing over the existing note content in the PostgreSQL database. Whilst this approach is simple and fast to implement, it could negatively affect the application's performance and consequentially, user experience, as the user base increases. For example, frequent and concurrent note edits from multiple users at once increases database load. In the case of database connection failure, large edits could be lost. 

Users should have up to date notes and be able to continue editing even if a save fails or they go offline. There should also be a fault-tolerance process that ensures user note data won't be lost or unretrievable in the event of a database connection failure.

My approach to this problem is to in the event the client loses conneciton the server, notes that are currently being edited are stored in the client's `local storage`. When the client polls the server, looking to send the note data, if it is back online then the note will be saved to Redis under the `note-id`. This process will be triggered whenever the user stops typing, as opposed to periodically polling the server even when changes have not been made. When the user hits 'save' or leaves the page, the note in Redis will be saved to the PostgreSQL database. If the note saves, it will stay in Redis for a set TTL, available for fast access if the user requests it again. If the note save fails, a server function will queue the `note_id` and periodically check the database for an available connection and save the note when available:
- Reduces load on primary, PostgreSQL database by relying on secondary data stores to manage frequent access and editing which provides a faster user experience
- Improves fault-tolerance of note-saving across client and server

✅ Autosave and manual save logic
⏰ Implement Celery worker for note save retry w/ Redis queue as message broker
⏰ Add time jitter to Redis TTLs and decide TTL extension strategy

# Fitness-Planner-Tracker

The Personalized Workout Plan system is designed to for users to create Personalized Workout Plan system and track their progress towards achieving their fitness goals. 

## Setup and Deployment

To easily deploy and run the application, you can download the Docker image file and load it into your Docker environment. Follow the steps below:

### Downloading the Docker Image

1. Download the Docker image file from the following link:
    - [Download Docker Image](https://drive.google.com/drive/folders/1VPkCbyzDSEzE5bobjK5ydepRyzF8KfhZ?usp=drive_link)

### Loading the Docker Image

2. After downloading, load the image into Docker with the following command:
    ```bash
    docker load < /path/to/yourprojectname.tar
    ```
    Replace `/path/to/yourprojectname.tar` with the actual path to the downloaded Docker image file.

### Running the Docker Container

3. Run the application by starting a Docker container using the following command:
    ```bash
    docker run -p 8000:8000 yourprojectname
    ```
    This command maps port 8000 of the container to port 8000 on your host machine, making the application accessible via `http://localhost:8000`.

### Accessing the Application

4. Open your web browser and navigate to `http://127.0.0.1:8000/api/docs/` For Swagger API enpoints and documetnation.

## API Endpoints for Djoser library

Customizing Djoser can complicate updating the library due to potential conflicts with new versions. Descriptions for Djoser endpoints are provided bellow. 

| Endpoint                   | Method | Description                                                          |
|----------------------------|--------|----------------------------------------------------------------------|
| `/auth/jwt/create/`        | POST   | Returns a JWT access and refresh tokens.                             |
| `/auth/jwt/refresh/`       | POST   | Takes a refresh type JWT token and returns an access token.         |
| `/auth/jwt/verify/`        | POST   | Validates an access token.                                           |
| `/auth/users/`             | GET    | Retrieves a list of users registered in the system.                 |
| `/auth/users/`             | POST   | Register a new user.                                                 |
| `/auth/users/me/`          | GET    | Retrieves information about the currently authenticated user.       |
| `/auth/users/me/`          | PUT    | Updates the information of the currently authenticated user.        |
| `/auth/users/me/`          | PATCH  | Partially updates the information of the currently authenticated user. |
| `/auth/users/me/`          | DELETE | Deletes the currently authenticated user account.                    |
| `/auth/users/set_password/`| POST   | Allows authenticated users to set a new password.                    |
| `/auth/users/set_username/`| POST   | Allows authenticated users to set a new username.                    |


JWT acsess token duration is set to 24 hours. refresh token to 7 days.

Djangos superuser(admin)
username: admin
pass: admin1234  


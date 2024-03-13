# Fitness-Planner-Tracker

The Personalized Workout Plan system is designed to for users to create Personalized Workout Plan system and track their progress towards achieving their fitness goals. 

## Setup and Deployment

## Local Development

1. **Clone the Project Repository**:
    - Clone the project repository from the following link:
        - [Project Repository](https://github.com/JohnnGab/FitnessPlanner.git)
    - You can use Git to clone the repository with the following command:
        ```bash
        git clone https://github.com/JohnnGab/FitnessPlanner.git
        ```

2. **Navigate to the Project Directory**:
    - Change your working directory to the root directory of the cloned project:
        ```bash
        cd FitnessPlanner
        ```

3. **Building the Docker Image**:
    - Make sure you have Docker installed on your system.
    - Run the following command to build the Docker image:
        ```bash
        docker build -t fitnessplanner .
        ```

4. **Running the Docker Container**:
    - Once the image is built, you can run the Docker container with the following command:
        ```bash
        docker run -p 8000:8000 fitnessplanner
        ```.
    - This command will start the container and map port `8000` from the container to port `8000` on your host machine.

5. **Accessing the Application**:
    - After the container is running, you can access your application in a web browser by navigating to `http://localhost:8000`.
    - Fow testing and Swagger documentation use `http://localhost:8000/api/docs/`. Ex. 'http://127.0.0.1:8000/api/docs/' 

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


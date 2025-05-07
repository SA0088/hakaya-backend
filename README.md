
# Project Name: Hakaya 


## Project Description
Hakaya is a platform that allows users to create, share, and interact with various types of experiences. Users can upload and share stories, experiences, and reviews categorized into different themes like Adventure, Cooking, Volunteering, and more. 🌍✨

## Repository Description
This repository contains the backend code for the Hakaya platform. It is built using Django and Django Rest Framework to provide APIs for managing experiences, categories, reviews, and user interactions. 🚀

## 🧰 Tech Stack

- **Backend Framework**: Django
- **API Framework**: Django Rest Framework (DRF)
- **Authentication**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
- **Database**: PostgreSQL (or SQLite for development)
- **ORM**: Django ORM
- **Containerization**: Docker
- **Frontend**: React (frontend, not included in this repo)

## Frontend Repository Link
- [Frontend Repository](https://github.com/SA0088/hakaya-frontend) 

## Link to Deployed Site
- [Deployed Site](http://localhost:5173/login) 

## ERD Diagram
You can find the ERD (Entity Relationship Diagram) for the project here:
- ![ERD Diagram](https://drive.google.com/file/d/1J39aur3rJ9hsl6YiEyqjN4NZ6awsynyd/view?usp=sharing) 

## 🗂 Routing Table
Below is a list of available endpoints in the Hakaya backend:

| **Endpoint**                                  | **Method** | **Description**                                      | **Authentication**     |
|----------------------------------------------|------------|------------------------------------------------------|------------------------|
| `/`                                          | GET        | Welcome message                                      | No                     |
| `/users/signup/`                             | POST       | Create a new user and return JWT tokens              | No                     |
| `/users/login/`                              | POST       | Log in with credentials and return JWT tokens        | No                     |
| `/users/token/refresh/`                      | GET        | Refresh JWT tokens                                   | Yes (JWT Required)      |
| `/users/profile/`                            | GET        | Get the authenticated user's profile (including experiences and liked experiences) | Yes (JWT Required)      |
| `/categories/`                               | GET        | List all categories                                  | Yes (JWT Required)      |
| `/categories/<pk>/experiences/`              | GET        | Get experiences by category                          | Yes (JWT Required)      |
| `/experiences/`                              | GET        | List all experiences                                 | Yes (JWT Required)      |
| `/experiences/`                              | POST       | Create a new experience                              | Yes (JWT Required)      |
| `/experiences/new/`                          | POST       | Create a new experience (alternative method)         | Yes (JWT Required)      |
| `/experiences/<exp_id>/`                     | GET        | Get experience details                               | Yes (JWT Required)      |
| `/experiences/<exp_id>/`                     | PUT        | Update an experience                                 | Yes (JWT Required)      |
| `/experiences/<exp_id>/`                     | DELETE     | Delete an experience                                 | Yes (JWT Required)      |
| `/experiences/<pk>/liked/`                   | PUT        | Like/Unlike an experience                            | Yes (JWT Required)      |
| `/experiences/users/liked/`                  | GET        | Get all liked experiences by authenticated user      | Yes (JWT Required)      |
| `/experiences/<exp_id>/reviews/`             | POST       | Create a review for a specific experience            | Yes (JWT Required)      |
| `/reviews/<pk>/like/`                        | PUT        | Like/Unlike a review                                 | Yes (JWT Required)      |
| `/users/forgot-password/`                    | POST       | Send a password reset email                          | No                     |



## Installation Instructions

### Requirements
- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- PostgreSQL
- Redis (optional, for Celery task queuing)
- Pillow (for image handling)



### Docker Setup (Optional)

If you'd like to run the project using Docker, follow these steps:

1. Build the Docker images:
    ```bash
    docker-compose build
    ```

2. Start the containers:
    ```bash
    docker-compose up
    ```

    The backend will be available at `http://127.0.0.1:8000/` on your local machine.

## 🧊 IceBox Features ❄️

### Features Pending Implementation (Exciting Features! 🎉)

- **Password Reset**: Add a complete password reset flow to allow users to recover their accounts. 🔐
- **Pagination**: Implement pagination for experiences and reviews to handle large datasets more efficiently. 📄
- **Search**: Enable a search feature to allow users to find experiences based on keywords, categories, or tags. 🔍
- **Advanced Filtering**:Add filters for sorting experiences by date, likes, and categories to improve user experience.🎨
- **Admin Panel**: Build a custom admin panel for managing users, experiences, and reviews. 🖥️
- **User Notifications**: Implement real-time notifications for actions like new reviews, experience updates, etc. 📲
- **User Roles**: Add user roles (admin, moderator, user) with specific permissions to control access. 👥
- **Social Login**: Enable login via Google, Facebook, or other social platforms for an easier user sign-up process. 🌐
- **User Achievements**: Create a gamification feature where users can earn badges based on their activity. 🏆







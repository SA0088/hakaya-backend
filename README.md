
# Project Name: Hakaya 


## Project Description
Hakaya is a platform that allows users to create, share, and interact with various types of experiences. Users can upload and share stories, experiences, and reviews categorized into different themes like Adventure, Cooking, Volunteering, and more. 🌍✨

## Repository Description
This repository contains the backend code for the Hakaya platform. It is built using Django and Django Rest Framework to provide APIs for managing experiences, categories, reviews, and user interactions. 🚀

## Tech Stack
- **Backend:** Django, Django Rest Framework (DRF) 💻
- **Database:** PostgreSQL 🗄️
- **Authentication:** JWT (JSON Web Tokens) 🔑
- **Image Storage:** ImageField with Pillow 🖼️

## Frontend Repository Link
- [Frontend Repository](https://github.com/SA0088/hakaya-frontend) 

## Link to Deployed Site
- [Deployed Site](http://localhost:5173/experince) 

## ERD Diagram
You can find the ERD (Entity Relationship Diagram) for the project here:
- ![ERD Diagram](../hakaya-backend/ERD.png) 

## Routing Table
Below is a list of available endpoints in the Hakaya backend:

| HTTP Method | Route                               | Description                          |
|-------------|-------------------------------------|--------------------------------------|
| GET         | /experience/                        | Get a list of experiences            |
| POST        | /experiences/create/                | Create a new experience              |
| PUT         | /experiences/{id}/like/             | Like or unlike an experience         |
| GET         | /categories/                        | Get a list of categories             |
| GET         | /reviews/{id}/like-toggle/          | Toggle like status for a review      |
| POST        | /reviews/create/                    | Create a new review                  |

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

## Icebox Features

- **User Profile Management:** Allow users to update their profiles, including profile picture, bio, and personal details.
- **Search Functionality:** Enable searching for experiences based on categories, keywords, or tags.
- **Admin Panel Enhancements:** Improve the admin panel for better management of experiences and reviews.
- **User Notifications:** Notify users when someone likes their experience or review.
- **Rating System for Experiences:** Add a rating system (stars, 1-5) for experiences, in addition to likes.
- **Social Media Sharing:** Enable users to share experiences on social media platforms like Facebook or Twitter.





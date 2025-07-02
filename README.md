
# Django API Project

I'm not familiar with Flask but from the experience I have shown in Django, I'm confident that if given the time and opportunity, I will be able to familarise myself with Flask during the internship.

This project is a RESTful API built using Django and Django REST Framework, designed to handle tasks such as managing a to-do list. The project is deployed on Render, allowing users to interact with the API via the provided endpoints.

## Table of Contents

1. [About the Project](#about-the-project)
2. [Tech Stack](#tech-stack)
3. [Getting Started](#getting-started)
4. [API Endpoints](#api-endpoints)
5. [Deployment on Render](#deployment-on-render)
6. [Explanation of Solution](#explanation-of-solution)


## About the Project
This Django-based API was created to provide endpoints for managing tasks in a to-do list. Users can perform various actions, such as creating, reading, updating, and deleting tasks. Unlike similar projects that use Flask, this project utilizes the Django framework to leverage its robust ecosystem and features, such as ORM, authentication, and a strong community.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Hosting**: [Render](https://render.com/)

## Getting Started

### Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework 3.x

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Configure your database settings in `settings.py` for local development.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

4. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```
6. Test Endpoints with Postman



## API Endpoints

Here's an overview of the main API endpoints and their functionalities:
The code works in a way that you need to be logged in with your access token to use the task endpoints.
If any request is sent without the token in the headers, an error will be returned as a response. 


| Endpoint               | HTTP Method | Description                                       |
|------------------------|-------------|---------------------------------------------------|
| `/task`               | GET         | Retrieves a list of all tasks                     |
| `/task/<id>`          | GET         | Gets a specific task                              |
| `/task`               | POST        | Creates a task                                    |
| `/task/<id>`          | PATCH       | Updates a task                                    |
| `/user/register/`     | POST        | Creates or Registers a User                       |
| `/user/login/`        | POST        | Logs in and returns an access and refresh token   |
| `/user/tasks`         | GET         | Returns tasks that belong to logged in user       |
| `/user/register`      | GET         | Returns all registered or signed up Users         |



## Deployment on Render
Because, the evaluator might not be familiar with the django framework, I hosted the api on render. The base url is 
`https://python-developers-test.onrender.com`. Combining that with the endpoints in postman will enable you to test without setting up locally.
The project is deployed on Render, a cloud hosting provider that offers a simple way to deploy web applications.

## Explanation of Solution
Django allows the developer to write database code in the python language but by the addition of the import of the django rest framework the database code can be serialized into JSON data and JSON data can be 
converted back into Database code.

In order to use the task endpoints, the user has to firstly be signed as it is a protected route. 

User registers on the register endpoint then logs in on the login enpoint and receives an access and refresh token. The access token is used on the protected routes and the refresh token is used to refresh the access token after expiry.




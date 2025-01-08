# Proxy Server

This project is a simple proxy server built using Django that can handle various HTTP methods (GET, POST, PUT, DELETE)
and forward requests to a user-specified target URL. The proxy server accepts headers, text data, and JSON data from the
client, forwards them to the target server, and returns the response.

---

## Features

- Proxy requests to a dynamic target URL passed as a query parameter.
- Supports various HTTP methods: GET, POST, PUT, DELETE.
- Handles headers, query parameters, and request bodies (text, JSON).
- Returns the response from the target server with appropriate headers and status codes.
- Error handling for 4xx and 5xx server errors, as well as network issues.

---

## TL;DR

#### When using Docker (with Docker as the Python interpreter)

```shell
docker run -it --rm proxy
# OR
docker-compose up -d --build

# To stop and remove the containers
docker-compose down
```

#### When using a virtual environment

```shell
source venv/bin/activate && export $(cat .env | xargs)

python manage.py runserver 0.0.0.0:8000
```

---

## Usage

### 1. GET Request Example:

```shell
curl -X GET "http://127.0.0.1:8000/proxy/?target_url=https://api.example.com/data"
```

This forwards the GET request to https://api.example.com/data and returns the response.

### 2. POST Request Example:

```shell
curl -X POST "http://127.0.0.1:8000/proxy/?target_url=https://api.example.com/data" \
-H "Content-Type: application/json" \
-d '{"key": "value"}'
```

This forwards the POST request with the JSON body to the target URL.

### 3. PUT Request Example:

```shell
curl -X PUT "http://127.0.0.1:8000/proxy/?target_url=https://api.example.com/data" \
-H "Content-Type: application/json" \
-d '{"key": "new_value"}'
```

This forwards the PUT request to the target URL along with the provided data.

### 4. DELETE Request Example:

```shell
curl -X DELETE "http://127.0.0.1:8000/proxy/?target_url=https://api.example.com/resource/123"
```

This forwards the DELETE request to delete the resource at the target URL.

---

## Setup

### 1. Setup Virtual Environment

```shell
python -m venv venv

source venv/bin/activate
```

### 2. Install Packages

```shell
pip install --upgrade django requests pre-commit gunicorn whitenoise
```

`OR`

```shell
pip install -r requirements.txt
```

### 3. Add Package in Requirement file and configure pre-commit

_if change in packages then update the requirements with below cmd_

```shell
pip freeze > requirements.txt

pre-commit install
```

---

## Configure Django Project

### 1. When using Docker as Python interpreter

Ensure that your docker-compose.yml is correctly set up to handle the Django environment. Start by bringing up the
Docker containers:

```shell
docker-compose up -d --build
```

Make sure that Dockerfile and docker-compose.yml have the proper configurations for the Django project.

`OR`

### 1. Load Environment Variables for Local Development

When using a virtual environment:

```shell
cp .env.template .env

export $(cat .env | xargs)
```

This will load environment variables from the .env file.

### 2. Migrate to your database

Run the following commands to apply the database migrations:

```shell
python manage.py makemigrations

python manage.py migrate
```

### 3. Create Superuser

You can create a superuser for the Django admin by running:

```shell
python manage.py createsuperuser --username admin --email admin@example.com
```

### 4. Runserver

Start the Django development server:

```shell
python manage.py runserver 0.0.0.0:8000
```

When using Docker, this will be mapped to your local machine's port 8000, making the project accessible via
`http://localhost:8000`.
---

## Running Tests

The project includes a comprehensive set of test cases for the proxy server.

### Running the Tests

To run the tests, use the following command:

```shell
python manage.py test
```

---

## License

This project is licensed under the MIT License.

---

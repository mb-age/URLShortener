# URL Shortener

A simple URL shortener service implemented in [Django](https://www.djangoproject.com/) using [Django Rest Framework (DRF)](https://www.django-rest-framework.org/) and documented with [drf-yasg](https://drf-yasg.readthedocs.io/).


## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Configuration](#configuration)


## Features

- Shorten long URLs into unique, easy-to-remember short codes.
- Redirect users from short URLs to their original long URLs.
- Customizable shortcode length and characters.
- Expose a RESTful API for URL shortening and redirection.
- Basic analytics for tracking the number of times a short URL is accessed.
- API documentation using Swagger/OpenAPI through `drf-yasg`.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (== 3.11)
- [Django](https://www.djangoproject.com/) (== 4.2.7)
- [Django Rest Framework](https://www.django-rest-framework.org) (== 3.14.0)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mb-age/URLShortener.git
    ```

2. Navigate to the project directory:

    ```bash
    cd webhelpers
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

## API Documentation

API documentation is available using Swagger/OpenAPI through `drf-yasg`.

1. Start the development server:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) or [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) to access the Swagger UI.

3. Explore and interact with the API using the provided documentation.


## Usage

1. Start the development server:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to [http://127.0.0.1:8000/api/url](http://127.0.0.1:8000/api/url) to access the URL shortener.

3. Shorten a URL by entering it in the provided form.

4. Use the generated alias [http://127.0.0.1:8000/api/url/alias](http://127.0.0.1:8000/api/url/alias) to redirect to the original long URL.

5. Check the alias click count [http://127.0.0.1:8000/api/url/alias/request-count](http://127.0.0.1:8000/api/url/alias/request-count)

## Configuration

- Customize settings, such as alias length in the `settings.py` file.
- Adjust API-related settings and documentation configurations in the `webhelpers/settings.py` file.

# URL Shortener

A simple URL shortener service implemented in [Python](https://www.python.org/) using the [Django](https://www.djangoproject.com/) web framework.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)


## Features

- Shorten long URLs into unique, easy-to-remember short codes.
- Redirect users from short URLs to their original long URLs.
- Customizable shortcode length and characters.
- Basic analytics for tracking the number of times a short URL is accessed.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (== 3.11)
- [Django](https://www.djangoproject.com/) (== 4.2.7)
- [DRF](https://www.django-rest-framework.org) (== 3.14.0)

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

## Usage

1. Start the development server:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to [http://127.0.0.1:8000/api/url/create](http://127.0.0.1:8000/api/url/create) to access the URL shortener.

3. Shorten a URL by entering it in the provided form.

4. Use the generated alias (http://127.0.0.1:8000/api/url/<alias>) to redirect to the original long URL.

5. Check the alias click count (http://127.0.0.1:8000/api/url/<alias>/request-count)

## Configuration

- Customize shortcode length in the `settings.py` file.

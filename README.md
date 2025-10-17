![viewer/Static/Pics/home.jpg](https://github.com/Rayns15/Film-Catalog/blob/1957bd7d87d6ba3153b65ebada2a7fbf6d84b42d/viewer/Static/Pics/home.jpg))
# Film Catalog - A Django Movie Database

## Introduction

**"Film Catalog"** is a movie database and review website built using **Django** and **Tailwind CSS**. It includes several pages such as Home, About, Contact, Movie Listings, Genres, and custom 404 pages. The project features a clean and modern design that is fully responsive and optimized for performance. It includes a powerful admin interface for managing films, genres, and reviews, and is easy to customize and deploy to a production environment.

## Table of Content

  * [Introduction](https://www.google.com/search?q=%23introduction)
  * [Installation](https://www.google.com/search?q=%23installation)
  * [Technologies Used](https://www.google.com/search?q=%23technologies-used)
  * [Features](https://www.google.com/search?q=%23features)
  * [Pages](https://www.google.com/search?q=%23pages)
  * [Website Screenshots](https://www.google.com/search?q=%23website-screenshots)
  * [Admin Screenshots](https://www.google.com/search?q=%23admin-screenshots)
  * [Deployment](https://www.google.com/search?q=%23deployment)

## Installation

1.  Clone the repository:

<!-- end list -->

```
git clone https://github.com/Rayns15/Film-Catalog.git
```

2.  Navigate to the project directory:

<!-- end list -->

```
cd film-catalog
```

3.  Create and activate a new virtual environment:

<!-- end list -->

```
python -m venv env
source env/bin/activate
```

4.  Install the project dependencies:

<!-- end list -->

```
pip install -r requirements.txt
```

5.  Install the `django-tailwind` module:

<!-- end list -->

```
pip install django-tailwind
```

6.  Add `tailwind` to your `INSTALLED_APPS` list in `settings.py`:

<!-- end list -->

```python
INSTALLED_APPS = [
    # ...
    'tailwind',
    # ...
]
```

7.  Run the Tailwind CSS configuration command:

<!-- end list -->

```python
python manage.py tailwind init
```

8.  Create the database tables:

<!-- end list -->

```python
python manage.py migrate
```

9.  Run the development server:

<!-- end list -->

```python
python manage.py runserver
```

## Technologies used

1.  HTML
2.  CSS
3.  JavaScript
4.  Python

### Primary Modules used

1.  Django==4.2.6
2.  django-tailwind==3.6.0
3.  whitenoise==6.6.0
4.  psycopg2-binary==2.9.9
5.  Pillow==10.1.0

## Features

1.  Responsive design using Tailwind CSS
2.  Admin dashboard for managing films, genres, directors, and reviews
3.  User authentication (Log in, Log out, Sign up)
4.  Users can add films to their "Watchlist"
5.  Contact form for sending messages to the site owner

## Pages

  - `Home`: The landing page of the website, which displays featured films and a brief introduction.
  - `About`: A page that provides information about the website's purpose.
  - `Contact`: A page that contains a contact form for visitors to send messages.
  - `Movie List`: A page that displays a list of all films in the catalog, with options for sorting and filtering.
  - `Movie Detail`: A page that displays the details of a single film, including the title, poster, director, release year, synopsis, and user reviews.
  - `Genres`: A page that displays a list of film genres, with links to filtered lists of films for each genre.
  - `My Account`: A user profile page showing their watchlist and submitted reviews.
  - `Custom 404 Pages`: Custom error pages that display when a user navigates to a non-existent page or encounters an error.

## Admin Screenshots

## Deployment

To deploy this project to a web server, you can follow these general steps:

1.  Set up a web server that can run Python applications. This could be a VPS, a PaaS like Heroku, or a cloud-based server like AWS.
2.  Clone the repository to your server:

<!-- end list -->

```
git clone https://github.com/Rayns15/Film-Catalog.git
```

3.  Install the project dependencies on your server using `pip`:

<!-- end list -->

```
pip install -r requirements.txt
```

4.  Set up a database for the project, if necessary. You can use a database like PostgreSQL, MySQL, or SQLite, depending on your needs.
5.  Configure the settings.py file with your server's settings:

<!-- end list -->

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

ALLOWED_HOSTS = ['example.com', 'www.example.com']
```

The DATABASES setting specifies the database connection details. In this example, we're using PostgreSQL with a database named `mydatabase`, a user named `mydatabaseuser`, and a password of `mypassword`. The `STATIC_ROOT` and `MEDIA_ROOT` settings specify the file paths where static files and media files will be stored. The `ALLOWED_HOSTS` setting is a list of domain names that the application is allowed to serve.
6\. Run the python manage.py collectstatic command to collect all the static files into the STATIC\_ROOT directory:

```python
python manage.py collectstatic
```

7.  Start the Django development server, or set up a production server using a WSGI server like uWSGI or Gunicorn.

<!-- end list -->

```python
python manage.py runserver
```

8.  Access the website using your server's IP address or domain name, and the port number of the server if necessary. For example, if you're running the development server on port 8000, you can access the website at `http://your-server-ip:8000/`.

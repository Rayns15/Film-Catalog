![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

# Film Catalog - A Django Movie Database & Showtime Scheduler

## Introduction

**"Film Catalog"** is a full-stack web application built with **Django** and **Tailwind CSS**. Originally a simple movie database, this project has evolved into a comprehensive **Cinema Showtime Management System**.

It allows authenticated users to perform full CRUD (Create, Read, Update, Delete) operations on **Movies**, **Cinemas**, and **Showtimes**. The core of the application is the showtime scheduler, which links specific movies to cinemas at designated times. It also features a dynamic pricing system to manage ticket costs (e.g., weekday vs. weekend) and various surcharges for each cinema.

![media/Home_first](https://github.com/Rayns15/Film-Catalog/blob/f791caf5f00c6be2db72509f18002270f3a09abb/media/Home_new6.jpg)
![media/Home_second](https://github.com/Rayns15/Film-Catalog/blob/f791caf5f00c6be2db72509f18002270f3a09abb/media/Home_new.jpg)

## Table of Content

  * [Introduction](#introduction)
  * [Installation](#installation)
  * [Technologies Used](#technologies-used)
  * [Features](#features)
  * [Pages](#pages)
  * [Website Screenshots](#website-screenshots)
  * [Deployment](#deployment)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Rayns15/Film-Catalog.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd film-catalog
    ```

3.  Create and activate a new virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

4.  Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5.  Install the `django-tailwind` module:

    ```bash
    pip install django-tailwind
    ```

6.  Add `tailwind` to your `INSTALLED_APPS` list in `settings.py`:

    ```python
    INSTALLED_APPS = [
        # ...
        'tailwind',
        # ...
    ]
    ```

7.  Run the Tailwind CSS configuration command:

    ```python
    python manage.py tailwind init
    ```

8.  Create the database tables:

    ```python
    python manage.py migrate
    ```

9.  Run the development server:

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

* **Full CRUD for Movies:** Authenticated users can add, update, and delete movie listings.
* **Full CRUD for Cinemas:** A dedicated "View Cinemas" page to add new cinemas and manage existing ones.
* **Full CRUD for Showtimes:** A "Showtime Manager" page to schedule a movie at a specific cinema and time, with full update/delete capabilities.
* **Dynamic Price Management:** A system to set custom ticket prices (Adult, Child, Senior, Student) for Weekday vs. Weekend for *each* cinema.
* **Upgrades & Surcharges:** Ability to manage add-on costs like Weekend Surcharges, Holiday Surcharges, and Matinee Discounts per cinema.
* **Live Chat & Reviews:** A live chat feature on the movie detail page for users to discuss and review films.
* **User Authentication:** Full Log in, Log out, and Sign up functionality.
* **Responsive Design:** A clean, modern, and fully responsive UI built with Tailwind CSS.

## Pages

  - `Home`: The landing page, displaying all movie cards, filterable by genre. Logged-in users see "Update/Delete" controls.
  - `Movie Detail`: Shows all details for one movie, including a cast/crew list.
  - `Prices & Showtimes`: A detailed breakdown of a movie's showtimes, grouped by cinema, with their respective price upgrades and the live chat.
  - `Showtime Manager`: A full CRUD admin panel for scheduling, updating, and deleting all existing showtimes.
  - `View Cinemas`: A dashboard showing all cinemas, with links to "Add Cinema" and "Update Prices" for each.
  - `Ticket Prices`: A page to view and update the detailed ticket price structure (Adult, Child, etc.) for a specific cinema.
  - `About / Contact / Auth Pages`: Standard pages for information, contact, and user management (Login, Logout, Sign up).

## Website Screenshots

![media/Home_5](https://github.com/Rayns15/Film-Catalog/blob/f0056dbe6c07a4f02a05934aa384d27aaa7808db/media/Home_new4.jpg)
![media/Home_6](https://github.com/Rayns15/Film-Catalog/blob/db15d4dd70ab3f441de1aa620fac1dd4d50bbf5c/media/Home_new5.jpg)
![media/Home_third](https://github.com/Rayns15/Film-Catalog/blob/f791caf5f00c6be2db72509f18002270f3a09abb/media/Home_new2.jpg)
![media/Home_forth](https://github.com/Rayns15/Film-Catalog/blob/f791caf5f00c6be2db72509f18002270f3a09abb/media/Home_new3.jpg)

## Deployment

To deploy this project to a web server, you can follow these general steps:

1.  Set up a web server that can run Python applications. This could be a VPS, a PaaS like Heroku, or a cloud-based server like AWS.

2.  Clone the repository to your server:

    ```bash
    git clone https://github.com/Rayns15/Film-Catalog.git
    ```

3.  Install the project dependencies on your server using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up a database for the project, if necessary. You can use a database like PostgreSQL, MySQL, or SQLite, depending on your needs.

5.  Configure the `settings.py` file with your server's settings:

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

    ALLOWED_HOSTS = ['example.com', '[www.example.com](https://www.example.com)']
    ```

    The `DATABASES` setting specifies the database connection details. In this example, we're using PostgreSQL with a database named `mydatabase`, a user named `mydatabaseuser`, and a password of `mypassword`. The `STATIC_ROOT` and `MEDIA_ROOT` settings specify the file paths where static files and media files will be stored. The `ALLOWED_HOSTS` setting is a list of domain names that the application is allowed to serve.

6.  Run the `python manage.py collectstatic` command to collect all the static files into the `STATIC_ROOT` directory:

    ```bash
    python manage.py collectstatic
    ```

7.  Start the Django development server, or set up a production server using a WSGI server like uWSGI or Gunicorn.

    ```bash
    python manage.py runserver
    ```

8.  Access the website using your server's IP address or domain name, and the port number of the server if necessary. For example, if you're running the development server on port 8000, you can access the website at `http://your-server-ip:8000/`.
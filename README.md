![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

# Film Catalog - A Django Cinema Management System

## Introduction

**"Film Catalog"** is a full-stack web application built with **Django** and **Tailwind CSS**. Originally a simple movie database, this project has evolved into a comprehensive **Cinema Showtime Management System** featuring a modern, responsive, dark-mode UI.

It allows authenticated users (Staff) to perform full CRUD operations on **Movies**, **Cinemas**, and **Showtimes**. The core of the application is the showtime scheduler, which links specific movies to cinemas at designated times. It also features a dynamic pricing system to manage ticket costs (e.g., weekday vs. weekend) and various surcharges for each cinema.

![Home Page](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new6.jpg) 
![Showtime Manager](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new.jpg)

## Table of Contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Pages](#pages)
* [Website Screenshots](#website-screenshots)
* [Deployment](#deployment)

## Installation

**Prerequisites:** You must have Python and Node.js installed on your machine.

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
    # Windows
    env\Scripts\activate
    # Mac/Linux
    source env/bin/activate
    ```

4.  Install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Install Tailwind Dependencies:**
    (Note: You must have Node.js installed for this step).
    
    ```bash
    python manage.py tailwind install
    ```

6.  Create the database tables:
    ```bash
    python manage.py migrate
    ```

7.  Create a superuser (to access the admin panel and staff features):
    ```bash
    python manage.py createsuperuser
    ```

8.  Run the development server:
    *You will need two terminals running:*

    **Terminal 1 (Django Server):**
    ```bash
    python manage.py runserver
    ```

    **Terminal 2 (Tailwind Compiler):**
    ```bash
    python manage.py tailwind start
    ```

## Technologies Used

* **Frontend:** HTML5, CSS3, JavaScript, Tailwind CSS (via `django-tailwind`)
* **Backend:** Python, Django 4.2.6
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Utilities:** Whitenoise (Static files), Pillow (Image processing)

## Features

* **Modern UI:** A custom-designed dark/neon aesthetic using Tailwind CSS.
* **Cinema Locations Dashboard:** A visual grid of all cinemas, showing upcoming showtime counts and quick-access administrative links.
* **Showtime Manager:** An advanced filtering and scheduling interface. Filter by Movie, Cinema, or Date to find existing shows, or use the form to schedule new ones.
* **Full CRUD:** Complete Create, Read, Update, Delete functionality for Movies, Cinemas, and Showtimes.
* **Dynamic Price Management:** Custom ticket prices (Adult, Child, Senior, Student) configurable per cinema.
* **Surcharges:** Manage add-on costs like Weekend Surcharges and Matinee Discounts.
* **User Authentication:** Secure Log in, Log out, and Sign up functionality with staff permissions.

## Pages

* `Home`: The landing page displaying all movie cards with "Prices & Showtimes" buttons.
* `Cinema Locations`: A dashboard displaying all cinema venues, their locations, and quick links to manage prices or add shows.
* `Showtime Manager`: The administrative hub for scheduling. Includes a form to add new shows and a table to filter/update/delete existing ones.
* `Movie Detail`: Displays cast, crew, ratings, and detailed descriptions.
* `Ticket Prices`: A dedicated page to configure the pricing matrix for specific cinemas.
* `Auth Pages`: Login, Logout, and Profile management.

## Website Screenshots

### Cinema Locations Dashboard
![Cinema Locations](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new5.jpg)

### Showtime Manager
![Showtime Manager](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new4.jpg)

### Upcoming Showtimes & Ticket Prices
![Home Page](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new2.jpg)

### Upcoming Showtimes & Ticket Prices
![Home Page](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new3.jpg)

## Deployment

To deploy this project to a web server:

1.  Set up a server (VPS, Heroku, AWS, Railway, etc.).
2.  Configure environment variables (SECRET_KEY, DEBUG=False).
3.  Configure `settings.py` for the production database (PostgreSQL recommended).
4.  **Build Tailwind CSS:**
    ```bash
    python manage.py tailwind build
    ```
5.  **Collect Static Files:**
    ```bash
    python manage.py collectstatic
    ```
6.  Run the application using a WSGI server (e.g., Gunicorn).
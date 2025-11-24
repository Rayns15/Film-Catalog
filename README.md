![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

# Film Catalog - Django Cinema Booking & Management System

## Introduction

**"Film Catalog"** is a robust full-stack web application built with **Django** and **Tailwind CSS**. Originally a simple movie database, this project has evolved into a comprehensive **Cinema Booking & Management System** featuring a modern, responsive, dark-mode UI.

The application serves two distinct roles:
1.  **For Administrators (Staff):** A powerful backend to manage Movies, Cinema Locations, and complex Schedules. It includes a dynamic pricing engine (handling weekday vs. weekend rates and surcharges).
2.  **For Users:** A complete booking experience allowing users to browse movies, **select specific seats via an interactive visual map**, manage ticket types (Adult, Child, etc.), and view their booking history.

![Home Page](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new6.jpg) 

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

### User Features
* **Interactive Seat Booking:** A visual seat map allowing users to select specific seats (Rows A-D). The system tracks occupied vs. available seats in real-time.
* **Ticket Type Selection:** Users can choose between Adult, Child, Senior, and Student tickets, with dynamic total cost calculation.
* **My Bookings Dashboard:** A user profile section displaying past and upcoming bookings with the ability to cancel future reservations.
* **Authentication:** Secure Sign Up, Login, and Profile management.

### Staff/Management Features
* **Cinema Locations Dashboard:** A visual grid of all cinemas, showing upcoming showtime counts and quick-access administrative links.
* **Showtime Manager:** An advanced filtering and scheduling interface. Filter by Movie, Cinema, or Date to find existing shows, or use the form to schedule new ones.
* **Dynamic Price Management:** Custom ticket prices configurable per cinema (e.g., specific pricing for "Le Grand Rex" vs "AMC").
* **Surcharges:** Manage add-on costs like Weekend Surcharges and Matinee Discounts automatically.
* **Full CRUD:** Complete control over Movies, Cinemas, and Showtimes.

## Pages

* `Home`: The landing page displaying all movie cards with "Prices & Showtimes" buttons.
* `Select Seats`: The interactive booking interface with seat map and ticket counters.
* `My Bookings`: User history page showing confirmed tickets and cancellation options.
* `Cinema Locations`: Dashboard displaying venues and quick links to manage prices.
* `Showtime Manager`: Admin hub for scheduling and filtering showtimes.
* `Movie Detail`: Displays cast, crew, ratings, and detailed descriptions.
* `Ticket Prices`: Configuration page for the pricing matrix.

## Website Screenshots

### 1. Interactive Booking System (Seat Map)
![Book the tickets](https://github.com/Rayns15/Film-Catalog/blob/28e4c2ec991651d5602f1d876f833ffc6ca0cb09/media/Home_new7.jpg)

### 2. User Dashboard (My Bookings)
![My Bookings](https://github.com/Rayns15/Film-Catalog/blob/28e4c2ec991651d5602f1d876f833ffc6ca0cb09/media/Home_new8.jpg)

### 3. Cinema Locations (Staff View)
![Cinema Locations](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new5.jpg)

### 4. Showtime Manager (Staff View)
![Showtime Manager](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new4.jpg)

### 5. Movie Details & Pricing
![Movie Details](https://github.com/Rayns15/Film-Catalog/blob/994cdef6c3dda9f6f5ffc0f2f146edf4850edd55/media/Home_new3.jpg)

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
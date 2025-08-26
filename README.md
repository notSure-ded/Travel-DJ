# Django Travel Booking Application

This is a simple travel booking web application built with Python and Django. It allows users to view available travel options, book tickets, and manage their bookings. The project is deployed and live on PythonAnywhere.

**Live URL:** [http://6EyeSCream9.pythonanywhere.com/](http://6EyeSCream9.pythonanywhere.com/)

---

## Features

* **User Authentication:** Secure user registration, login, and logout functionality using Django's built-in authentication system.
* **Profile Management:** Users can view and update their profile information (name, email).
* **View Travel Options:** A comprehensive list of all available travel options (Flights, Trains, Buses).
* **Search and Filtering:** Users can filter travel options by type, source, destination, and date.
* **Booking System:** A complete booking workflow, including selecting seats and confirming a booking. The system validates against available seats.
* **Booking Management:** Users have a dedicated page to view their current and past bookings.
* **Cancellation:** Users can cancel their confirmed bookings, which automatically updates the number of available seats for that travel option.
* **Admin Panel:** A full admin interface to manage travel options and bookings.

---

## Tech Stack

* **Backend:** Python, Django
* **Database:** MySQL
* **Frontend:** Django Templates, Bootstrap 5
* **Testing:** Django's built-in unit testing framework

---

## Local Setup and Installation

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.8+
* Git
* MySQL Server

### 2. Clone the Repository

First, clone the project from your GitHub repository:
```bash
git clone [https://github.com/notSure-ded/Travel-DJ.git](https://github.com/notSure-ded/Travel-DJ.git)
cd Travel DJ
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

* **Create the environment:**
    ```bash
    python -m venv venv
    ```
* **Activate the environment:**
    * On Windows: `.\venv\Scripts\activate`
    * On macOS/Linux: `source venv/bin/activate`

### 4. Install Dependencies

Install Django and the MySQL client library:
```bash
pip install Django mysqlclient
```

### 5. Configure the Database

1.  **Create a MySQL database** for the project. You can use a tool like MySQL Workbench or the command line.
    ```sql
    CREATE DATABASE travel_db;
    ```
2.  **Update `settings.py`:** Open `travel_project/settings.py` and update the `DATABASES` section with your local MySQL credentials.
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'travel_db',
            'USER': 'your_mysql_user',
            'PASSWORD': 'your_mysql_password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
    ```

### 6. Run Migrations

Apply the database migrations to create the necessary tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Admin Account)

Create an admin account to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 8. Run the Development Server

You're all set! Start the development server:
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

---

## Using the Admin Panel

To add travel options for users to book, you need to use the admin panel.

1.  Navigate to the admin URL for the live site or your local version:
    * **Live Site:** `http://6EyeSCream9.pythonanywhere.com/admin/`
    * **Local:** `http://127.0.0.1:8000/admin/`
2.  Log in with the superuser credentials you created.
3.  In the admin dashboard, find the "Travel options" section and click **"+ Add"**.
4.  Fill in the details for a few sample trips and save them. These will now appear on the main page for users to view and book.

### Admin Credentials for Testing

For evaluation purposes, you can use the following credentials to log in to the admin panel on the live site:

* **Username:** `kunal`
* **Password:** `Kunal@567`

*(Note: You will need to create this user on your live site using the `createsuperuser` command in a PythonAnywhere Bash console if you haven't already.)*

---

## Running Tests

To run the unit tests for the application, stop the development server and run the following command:
```bash
python manage.py test

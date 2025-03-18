# PIN Authentication Project

A secure PIN authentication system built with Django that implements protection against shoulder surfing attacks. This project provides a unique approach to PIN entry that enhances security while maintaining usability.

## Prerequisites

- Python 3.12+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/19IT089-Shruti-S/pin_auth_project
   cd pin_auth_project
   ```

2. Set up a virtual environment (recommended):
   ```bash
   # Using pipenv (recommended)
   pip install pipenv
   pipenv install
   pipenv shell

   # OR using venv
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # If using pipenv, this step is already done
   # If using venv:
   pip install -r requirements.txt
   ```

## Database Setup

1. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure

- `pin_auth/` - Main application directory
  - `views.py` - Contains the core logic for PIN authentication
  - `models.py` - Database models
  - `forms.py` - Form definitions
  - `middleware.py` - Custom middleware
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JavaScript, etc.)


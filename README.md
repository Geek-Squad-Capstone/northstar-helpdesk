# northstar-helpdesk

IT Help Desk / Support Ticket Management System for the CPSC 4205 Capstone project.

## Development Environment Setup

This project uses Python, Django, SQLite, GitHub, and HTML.

## Requirements

- Python 3.13.x
- Git
- Django 6.1.1

## Clone the Repository

Clone the project repository to your computer:

```bash
git clone https://github.com/Geek-Squad-Capstone/northstar-helpdesk.git
```

Then move into the project folder:

```bash
cd northstar-helpdesk
```

Switch to the team integration branch:

```bash
git switch develop
```

## Create a Virtual Environment

Create a virtual environment for the project.

### Windows / Git Bash

```bash
py -3.13 -m venv setup
```

### macOS / Linux

```bash
python3 -m venv setup
```

## Activate the Virtual Environment

### Windows / Git Bash

```bash
source setup/Scripts/activate
```

### macOS / Linux

```bash
source setup/bin/activate
```

When the virtual environment is active, `(setup)` should appear at the beginning of the terminal prompt.

To leave the virtual environment:

```bash
deactivate
```

## Install Dependencies

Install the Python packages required by the project:

```bash
pip install -r requirements.txt
```

The current dependencies are:

```text
asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0
```

## Verify Django

Check the installed Django version:

```bash
python -m django --version
```

Expected version:

```text
6.1.1
```

## Run Migrations

Initialize or update the local database by running Django's migrations:

```bash
python manage.py migrate
```

A successful migration should complete without errors.

## Check the Project

Run Django's system check:

```bash
python manage.py check
```

A successful setup should return:

```text
System check identified no issues (0 silenced).
```

## Start the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Open the address shown in the terminal, usually:

```text
http://127.0.0.1:8000/
```

If the NorthStar Help Desk page loads successfully, the development environment is ready to use.
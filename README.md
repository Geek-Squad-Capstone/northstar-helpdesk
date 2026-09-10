# northstar-helpdesk
IT Help Desk / Support Ticket Management System for the CPSC 4205 Capstone project.


## Development Environment Setup

This project uses Python, Django, SQLite, GitHub, and HTML.

### Requirements
- Python 3.13.9
- Git
- Django 6.1.1

### Clone the Repository
Clone the project repository to your computer:

git clone https://github.com/Geek-Squad-Capstone/northstar-helpdesk.git

Then move into the project folder:

cd northstar-helpdesk

### Create a Virtual Environment
Create a virtual environment for the project:

python3 -m venv setup

### Activate the Virtual Environment
On macOS or Linux:

source setup/bin/activate

When the environment is active, (setup) should appear at the beginning of the Terminal prompt.

To leave the virtual environment:

deactivate

### Install Dependencies
Install the Python packages required by the project:

pip install -r requirements.txt

The current dependencies are:

asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0

### Verify Django
Check the installed Django version:

python -m django --version

Expected version:

6.1.1

### Check the Project
Run Django's system check:

python manage.py check

A successful setup should return:

System check identified no issues

### Start the Development Server
Start the Django development server:

python manage.py runserver

Open the address shown in Terminal, usually:

http://127.0.0.1:8000/

If the Django page loads successfully, the development environment is ready to use.

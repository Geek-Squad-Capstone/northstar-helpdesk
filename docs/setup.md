# Setup Guide

## Requirements

- Python 3.13.x
- Git
- Django 6.1.1
- SQLite
- A web browser

## Steps

1. Clone the NorthStar Help Desk repository.

```bash
git clone https://github.com/Geek-Squad-Capstone/northstar-helpdesk.git
```

2. Move into the `northstar-helpdesk` project folder.

```bash
cd northstar-helpdesk
```

3. Switch to the `develop` branch.

```bash
git switch develop
```

4. Create a virtual environment named `setup`.

For Windows:

```bash
py -3.13 -m venv setup
```

For macOS or Linux:

```bash
python3 -m venv setup
```

5. Activate the `setup` virtual environment.

For Windows PowerShell:

```powershell
.\setup\Scripts\Activate.ps1
```
For macOS or Linux:

```bash
source setup/bin/activate
```

When the virtual environment is active, `(setup)` should appear at the beginning of the terminal prompt.

6. Install the project dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

7. Verify the installed Django version.

```bash
python -m django --version
```

The expected output is:

```text
6.1.1
```

8. Run Django's system check.

```bash
python manage.py check
```

The expected output is:

```text
System check identified no issues (0 silenced).
```

9. Apply the database migrations.

```bash
python manage.py migrate
```

The migrations should complete without errors.

10. Create the initial NorthStar administrator

NorthStar requires an initial administrator account before additional users can be created through the web interface.

Open the Django shell:

```bash
python manage.py shell
```

10.1 Enter the following Python commands:

```python
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from support.models import UserProfile
from getpass import getpass

username = input("Administrator username: ").strip()
password = getpass("Administrator password: ")

validate_password(password)

user = User.objects.create_user(
    username=username,
    password=password
)

UserProfile.objects.create(
    user=user,
    role="administrator"
)

print("NorthStar administrator created successfully.")
exit()
```

11. Start the Django development server.

```bash
python manage.py runserver
```
After starting the development server, open the following address in a web browser:

```text
http://127.0.0.1:8000/
```

12. Log in to NorthStar

Select **Login** and enter the username and password created in Step 10.

Once logged in, the administrator should have access to **User Management** and **Category Management**.

Use **User Management** to create additional accounts with the appropriate roles:

- IT Administrator
- IT Technician
- Regular User

Use **Category Management** to add at least one ticket category before testing ticket submissions.

## Verify It Works

After starting the development server, open the following address in a web browser:

```text
http://127.0.0.1:8000/
```
The NorthStar Help Desk home page should load without an error.

Test the application with users assigned to each available role and verify that the correct permissions are displayed.

For an IT Administrator account, verify that the navigation includes:

- Home
- Dashboard
- Create Ticket
- My Tickets
- Ticket Queue
- Closed Ticket History
- Category Management
- User Management

Open `User Management` and confirm that an IT Administrator can create users, change user roles, and deactivate users.

For an IT Technician account, verify that the navigation includes:

- Home
- Dashboard
- Ticket Queue
- Closed Ticket History

Open `Ticket Queue` and confirm that the technician can access the following ticket actions:

- View Details
- Claim Ticket
- Edit Status
- Edit Priority
- Edit Category

For a Regular User account, verify that the navigation includes:

- Home
- Dashboard
- Create Ticket
- My Tickets

Open `My Tickets` and confirm that the regular user can view submitted tickets and access ticket details.

Confirm that a Regular User does not have access to technician or administrator features such as:

- Ticket Queue
- Closed Ticket History
- Category Management
- User Management

Submit a test ticket as a Regular User and confirm that the ticket is created successfully and appears under `My Tickets`.


## Troubleshooting

### Django Is Not Installed

If Django cannot be found, make sure the `setup` virtual environment is activated.

For macOS or Linux:

```bash
source setup/bin/activate
```

For Windows PowerShell:

```powershell
.\setup\Scripts\Activate.ps1
```

Then install the dependencies again:

```bash
pip install -r requirements.txt
```

### Database Migration Errors

If Django reports missing or unapplied migrations, run:

```bash
python manage.py migrate
```

### PowerShell Blocks Virtual Environment Activation

If PowerShell blocks the `Activate.ps1` script because of the execution policy, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again:

```powershell
.\setup\Scripts\Activate.ps1
```

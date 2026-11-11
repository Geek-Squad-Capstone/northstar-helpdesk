# NorthStar Help Desk

NorthStar Help Desk is an IT help desk and support ticket management system created for the CPSC 4205 Senior Capstone project. It is designed to help users submit support requests and allow IT staff to manage, assign, update, and track tickets.

## Status

*Feature Complete*

Core ticket management functionality has been implemented. Final documentation, setup verification, and release preparation are in progress. The application is not intended for production deployment in its current configuration.

## Team

- Christopher Armstrong: Project Manager
- Seungu Hong: QA & Security Lead
- Joseph Morgan: Developer

## Quick Start

### macOS or Linux

```bash
git clone https://github.com/Geek-Squad-Capstone/northstar-helpdesk.git
cd northstar-helpdesk
git switch develop
python3 -m venv setup
source setup/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Windows PowerShell

```powershell
git clone https://github.com/Geek-Squad-Capstone/northstar-helpdesk.git
cd northstar-helpdesk
git switch develop
py -3.13 -m venv setup
setup\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/ in a web browser.
```
## Documentation

- [Setup Guide](docs/setup.md)
- [Architecture](docs/architecture.md)
- [Decision Records](docs/decisions/0001-use-python-django.md)

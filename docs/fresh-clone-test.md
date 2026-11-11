
# Fresh Clone Test Report

## Test Information

- **Tester:** Seungu Hong
- **Date:** November 11, 2026
- **Operating System:** Windows 10
- **Terminal:** Windows PowerShell
- **Python Version:** 3.13.9
- **Django Version:** 6.1.1
- **Branch Tested:** `feature/category-admin-fix` (based on `develop`)

## Overall Result

**Status: PARTIAL PASS**

The application was successfully installed and tested after resolving several setup and application issues.

Most of the tested ticket management workflows worked successfully. However, some documentation and application issues remain unresolved. The test was conducted with assistance, so a completely independent setup using only the documentation has not yet been verified.

## Setup Issues

### 1. Missing PowerShell Activation Instructions

**Result: FAIL**

The setup instructions did not include the PowerShell command for activating the virtual environment.

The activation command used was:

```powershell
.\setup\Scripts\Activate.ps1
```

**Resolution:** The virtual environment was activated manually.

### 2. PowerShell Execution Policy

**Result: FAIL**

PowerShell blocked the virtual environment activation script because of the execution policy.

The following command was used to allow activation for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Resolution:** The activation script ran successfully after changing the process-level execution policy.

**Documentation Update Needed:** Add this troubleshooting instruction to the Setup Guide.

### 3. Django Installation and Database Setup

**Result: PASS**

- Installed project dependencies using `pip install -r requirements.txt`.
- Verified Django version 6.1.1.
- Ran `python manage.py check` successfully.
- Applied database migrations successfully.
- Created a local administrator account.
- Started the development server successfully.

## Application Issues

### 4. UserProfile Was Not Automatically Created

**Result: FAIL**

Creating a superuser did not automatically create a corresponding `UserProfile`.

A `UserProfile` had to be created manually through Django Admin. The administrator role was then assigned manually.

**Status:** Not fixed during this test.

### 5. Category Was Not Registered in Django Admin

**Result: FAIL**

The `Category` model existed in `support/models.py`, but it was not registered in `support/admin.py`.

As a result, the Category section was missing from Django Admin. The Category dropdown in the ticket creation form had no available options.

**Resolution:** Registered the `Category` model in `support/admin.py`.

The following code was used:

```python
from django.contrib import admin
from .models import Category, Ticket, UserProfile

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Ticket)
```

Ran `python manage.py check` successfully after the change.

Added test categories through Django Admin.

Verified that the Category dropdown worked and tickets could be created.

**Fixing Commit:** Included in this pull request.

### 6. User Management Menu Was Missing

**Result: FAIL**

The Setup Guide instructed the administrator to open User Management.

However, the User Management menu was not visible in the tested application.

Test users and their `UserProfile` records had to be created through Django Admin instead.

**Status:** Requires further investigation.

## Application Workflow Tests

### 7. Regular User Ticket Creation

**Result: PASS**

Created a test regular user.

Created a test ticket with a category, title, affected device, description, priority, and department.

Verified that the ticket appeared under My Tickets.

### 8. Administrator Ticket Management

**Result: PASS**

Verified that the administrator could:

- View the ticket in Ticket Queue.
- Claim the ticket.
- Change the ticket status.
- Change the ticket priority.
- Change the ticket category.
- Add a comment.
- Add an internal note.
- Close the ticket.

### 9. Comments and Internal Notes

**Result: PASS**

Verified that comments were visible to both the administrator and regular user.

Verified that internal notes were visible to the administrator but not displayed in the regular user's ticket details.

### 10. Closed Ticket History

**Result: PASS**

Verified that a closed ticket disappeared from Ticket Queue.

Verified that it appeared in Closed Ticket History.

Confirmed that the regular user could still view the closed ticket.

### 11. Reopen Ticket

**Result: PASS**

Verified that a regular user could reopen a closed ticket.

The ticket returned to Open status and appeared in Ticket Queue again.

**Note:** The intended permission for regular users to reopen tickets should be confirmed with the team.

## Items Not Yet Verified

- Complete setup using only the documentation without assistance.
- IT Technician role and its permissions.
- User Management functionality.
- Automatic `UserProfile` creation.
- Whether regular users are intended to reopen closed tickets.

## Conclusion

The fresh clone was successfully installed, and the main ticket management workflows tested during this session worked after resolving the Category registration issue.

However, the Setup Guide needs additional Windows PowerShell instructions, and the missing User Management menu and automatic `UserProfile` creation require further investigation.

A final independent retest should be performed after the documentation and application fixes are completed.

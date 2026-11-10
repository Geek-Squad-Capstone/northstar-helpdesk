# Architecture

## Overview

NorthStar Help Desk is a browser-based support ticket management application built with Python and Django for NorthStar Community Outreach. Regular users submit support requests and track their own tickets, technicians work from a shared ticket queue, and administrators manage users, categories, and ticket assignments. Django handles page requests, form validation, permissions, and database operations. SQLite stores the application's records in the development environment.

## Components

| Part | Job | Technology |
| --- | --- | --- |
| Web interface | Displays the dashboard, ticket forms, ticket lists, details, and administrative pages. | HTML, Django templates, CSS |
| URL routing | Maps browser requests to the appropriate application views. | Django, `helpdesk/urls.py` |
| Application logic | Processes ticket submission, status updates, assignment, comments, internal notes, and administrative actions. | Python, Django, `support/views.py` and `support/forms.py` |
| Authentication and permissions | Signs users in, identifies their roles, and restricts access to views and individual tickets. | Django authentication, `UserProfile`, `support/permissions.py` |
| Data models and storage | Stores users' roles, tickets, categories, comments, internal notes, and audit records. | Django ORM, SQLite, `support/models.py` |
| Activity tracking | Records selected ticket changes, including technician claims, status changes, and reopen actions. | `AuditLog` model and ticket methods in `support/models.py` |

## Data Flow

The following steps trace a regular user submitting a support ticket and then viewing it in **My Tickets**.

1. An authenticated regular user opens **Create Ticket** at `/tickets/create/`. The `create_ticket` view checks that the user has the `regular_user` role (administrators are also permitted).
2. Django renders `templates/create_ticket.html`, which displays the `TicketForm` fields for the category, title, device or system, description, priority, and department.
3. The user submits the form with an HTTP POST request. Django's CSRF protection checks the form token, and `TicketForm` validates the submitted field values.
4. When the form is valid, the view creates a `Ticket` object, sets its `submitted_by` field to the authenticated user rather than trusting a user-supplied requester ID, and saves it using Django's ORM.
5. Django stores the ticket in the local SQLite database. The ticket starts with the model's default status of `Open` and no assigned technician.
6. The user can open **My Tickets** at `/tickets/`, where the `tickets` view retrieves only records with `submitted_by=request.user` and renders them in `templates/tickets.html`.
7. When the user opens a ticket's details, `ticket_detail` checks that the requester owns the ticket or has a technician/administrator role before showing its information and comments.

## Security Notes

- **Role-based access control:** `support/permissions.py` implements `@role_required` to check authentication and the user's `UserProfile.role` on protected views. Unauthorized roles receive HTTP 403, while unauthenticated visitors are redirected to sign in. For example, regular users cannot open the technician queue or administrator category-management pages.
- **Ticket ownership:** The **My Tickets** view filters records by the signed-in user. The ticket-detail view separately checks ownership, allowing a regular user to view their own ticket while permitting technicians and administrators to inspect tickets for support work.
- **CSRF protection and input validation:** Django's CSRF middleware and form tokens protect standard form submissions, while Django `ModelForm` classes validate submitted fields. These controls do not eliminate the need for application-specific validation.
- **Audit history:** The `AuditLog` model records the acting user, ticket, action, and time for selected operations such as ticket claiming and status changes. Not every update currently creates an audit record, so it should not be treated as a complete history of all activity.
- **Development configuration risk:** `helpdesk/settings.py` currently has `DEBUG = True` and contains a hardcoded Django `SECRET_KEY`. Before deployment, a new secret should be stored securely outside version control and debug mode disabled.
- **Ticket intake risks:** The current `TicketForm` permits requesters to choose their own priority and does not limit its category choices to active categories. The submission view also redirects with a success message after an invalid POST.

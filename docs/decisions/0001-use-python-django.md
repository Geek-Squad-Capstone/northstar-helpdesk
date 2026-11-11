# 1. Use Python and Django for NorthStar Help Desk

**Status:** Approved
**Date:** 2026-11-11

## Context

During early project planning, the team needed to choose a technology stack for NorthStar Help Desk before building the application. NorthStar was intended to be a browser-based support ticket system with user accounts, role-based permissions, ticket submission, technician assignments, and administrative functions. We considered developing the application in Java with Spring Boot as an alternative to Python with Django. Both could support the required features, but we also had to consider development time, framework setup, authentication, database access, and the semester deadline. The instructor also raised deployment complexity as something to consider when choosing the stack.

## Decision

We will use Python and Django to develop the NorthStar Help Desk web application. Django will provide URL routing, authentication, form handling, templates, and database access through its object-relational mapper (ORM). We will use SQLite as the database for local development and testing. This approach would let us concentrate on implementing and testing the help desk requirements rather than building common web application features from scratch.

## Consequences

- **Easier:** Django provides built-in tools for authentication, forms, database models, migrations, and administration. These reduce the amount of setup and supporting code the team needs to write, making the planned help desk features more manageable within the semester.
- **Easier:** Python and Django offer a straightforward local development workflow, with dependencies listed in `requirements.txt` and database tables created using migrations.
- **Harder:** Choosing Django means giving up the opportunity to build the project in Java and gain experience with the Java/Spring Boot ecosystem. We will also need to learn Django's conventions and troubleshoot framework-specific issues.
- **Harder:** Django does not eliminate deployment or security work. A production release would still require a suitable hosting configuration, secure settings and secrets, and a review of whether SQLite is appropriate for the expected workload.

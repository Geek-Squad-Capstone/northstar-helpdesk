# Fresh Clone Test

*Follow-up Verification — Test 2*

## Tester

- **Name:** Joseph Morgan
- **Date:** November 11, 2026
- **Operating System:** Windows 11
- **Terminal:** Git Bash
- **Application Branch:** `develop`
- **Setup Instructions:** Updated `docs/setup.md` from `docs-setup-fixes`

## Result

**Pass** — The corrected setup procedure successfully initialized NorthStar Help Desk, and the tested application workflows passed.

The following were verified:

- A standard Django user and corresponding NorthStar `administrator` profile were created without using `createsuperuser`.
- The administrator logged in through NorthStar's web interface.
- User Management and Category Management were accessible.
- The administrator created a ticket category, an IT Technician, and a Regular User.
- The Regular User submitted a ticket successfully.
- The ticket appeared in My Tickets, and the technician could access Ticket Queue.

## Problems Found

1. **Shell mismatch:** The PowerShell virtual-environment activation command did not run in Git Bash. Activation succeeded using the Git Bash command. This was a terminal mismatch rather than an application failure.
2. **Interactive username prompt:** On the first administrator-creation attempt, a Python command was entered at the username prompt. This caused `NameError` exceptions and prevented account creation. Repeating the procedure with an actual username and password succeeded.

No additional application failures were encountered during the completed verification.

## Fixes Made

1. **Setup-guide corrections:** Added PowerShell activation and troubleshooting instructions, and replaced `createsuperuser` with the creation of a standard Django user and a NorthStar administrator `UserProfile`. [View fixing commit](https://github.com/Geek-Squad-Capstone/northstar-helpdesk/commit/2e3e6ff6aa01216562259d02e6faa98a75bffcf5).

The issues encountered during this follow-up were resolved during testing; no further changes were required.

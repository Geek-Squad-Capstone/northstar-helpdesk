# Team Development Workflow

## Claiming a Task and Updating the Kanban Board

The Capstone project board is located at:

https://github.com/orgs/Geek-Squad-Capstone/projects/1/

The board uses six status categories:

- **Backlog** — Work identified for the project but not yet ready to begin.
- **Ready** — Work that is defined and ready to be started.
- **In Progress** — Work that is actively being worked on.
- **Blocked** — Work that cannot continue because of a dependency or unresolved issue.
- **Review/Testing** — Work completed by the assignee and awaiting review or testing.
- **Done** — Work that has been reviewed, tested where applicable, and completed.

Some tasks depend on other work being completed first. These tasks will remain in **Backlog** and are marked with a red circle containing a dash.

Once their dependencies have been completed, the blocked indicator will disappear. If a Backlog task no longer has unresolved dependencies and is ready to begin, move it to **Ready**.

### Claiming a Task

To claim a task:

1. Open the task card.
2. Locate the **Assignees** section in the upper-right corner.
3. Select **Assign yourself**.
4. Move the card to **In Progress** when work begins.

When your work on the task is complete, move the card to **Review/Testing**.

If the task involves repository changes, open a pull request and allow another team member to review and test the work before it is merged.

After the work has been reviewed, tested where applicable, and merged, the reviewer should move the card to **Done**.

### Blocked Tasks

If progress on a task becomes blocked:

1. Move the card to **Blocked**.
2. Open the task card.
3. Leave a comment explaining the issue preventing the task from being completed.

Comments can be added using the comment field beneath the task history.

---

## Git Branching and Pull Request Workflow

Development work should normally begin from the latest version of the `develop` branch.

Create a separate branch for the assigned task and commit changes to that branch rather than committing directly to `develop` or `main`.

The normal workflow is:

`Update local develop → Create task branch → Make changes → Review with git status → Stage changes → Commit → Push branch → Open PR into develop → Peer review/testing → Merge into develop → Move task to Done`

The `develop` branch serves as the integration branch for ongoing work.

The `main` branch should remain stable and should only receive work that has already been integrated and tested through `develop`.

## Git Branching Workflow

The repository uses `main` and `develop` as the two shared branches.

- **`main`** — Stable branch containing tested and integrated work.
- **`develop`** — Integration branch for ongoing development.

Team members should not normally commit directly to either shared branch.

For each task:

1. Start from the latest version of `develop`.
2. Create a separate branch for the task.
3. Make and commit changes on that task branch.
4. Push the branch to GitHub.
5. Open a pull request targeting `develop`.
6. Another team member should review and test the changes.
7. Once approved, merge the pull request into `develop`.
8. Move the associated Kanban task to **Done**.

When a group of changes in `develop` has been tested and is considered stable, `develop` may be merged into `main`.

Branch names should describe the purpose of the work. Examples include:

- `feature/category-model`
- `setup/static-files`
- `fix/regular-user-role`
- `docs/git-workflow`
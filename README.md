## GitHub Actions workflows

This repo includes a couple of workflow files under [.github/workflows](.github/workflows) that demonstrate different scenarios.

### Actions Feature Demo

File: [.github/workflows/actions-feature-demo.yml](.github/workflows/actions-feature-demo.yml)

**Workflow trigger**:
- Manually triggered workflow via `workflow_dispatch` with input parameters.

**Job 1 (`Prep`)**:
- Prepares output values to be consumed by downstream jobs.

**Job 2 (`required_gate`)**:
- Depends on the `prep` job.
- A job that can fail based on input it receives from a previous job.

**Job 3 (`side_quest`)**:
- Also depends on the `prep` job.
- Runs in parallel to the `required_gate` job.

**Job 4 (`matrix_work`)**:
- Skip this job if the PR is a draft.
- Uses a matrix strategy to test the same job steps with multiple Python versions in parallel.
- Runs a Python script stored in the repo.
- Runs an inline Python script using the `python` shell.

**Job 5 (`summary`)**:
- Always runs, regardless of prior job success/failure.

<img width="1916" height="626" alt="Screenshot 2026-02-05 at 11 57 22 AM" src="https://github.com/user-attachments/assets/7d562737-2a61-45fb-a392-62a1846e570b" />


### Dependency Security Testing (reusable workflow caller)

File: [.github/workflows/caller-workflow.yml](.github/workflows/caller-workflow.yml)

Scenario coverage:
- Pull request triggered when a PR is marked ready for review on `main` or `release/**`.
- Calls a reusable workflow hosted in a central security repo.

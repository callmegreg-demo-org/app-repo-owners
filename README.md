## GitHub Actions workflows

This repo includes a couple of workflow files under [.github/workflows](.github/workflows) that demonstrate different scenarios.

### Actions Feature Demo

File: [.github/workflows/actions-feature-demo.yml](.github/workflows/actions-feature-demo.yml)

Scenario coverage:
- Manually triggered workflow via `workflow_dispatch` with input parameters.
- Passing values between jobs using outputs (`prep` → downstream jobs).
- Parallel job execution (`side_quest` runs alongside `required_gate`).
- Required gate job that can intentionally fail based on input it receives from a previous job.
- Matrix strategy job to test multiple Python versions in parallel.
- Running a Python script stored in the repo.
- Running an inline Python script using the `python` shell.
- A summary job that always runs, regardless of prior job success/failure.

<img width="1916" height="626" alt="Screenshot 2026-02-05 at 11 57 22 AM" src="https://github.com/user-attachments/assets/7d562737-2a61-45fb-a392-62a1846e570b" />


### Dependency Security Testing (reusable workflow caller)

File: [.github/workflows/caller-workflow.yml](.github/workflows/caller-workflow.yml)

Scenario coverage:
- Pull request triggered when a PR is marked ready for review on `main` or `release/**`.
- Calls a reusable workflow hosted in a central security repo.

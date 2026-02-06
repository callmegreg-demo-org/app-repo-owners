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

---

### Dependency Security Testing (reusable workflow caller)

File: [.github/workflows/caller-workflow.yml](.github/workflows/caller-workflow.yml)

Scenario coverage:
- Pull request triggered when a PR is marked ready for review on `main` or `release/**`.
- Calls a reusable workflow hosted in a central security repo.

---

### Merge Queue Demo

Demonstrates GitHub's merge queue feature with three different PR behaviors: fast pass, slow pass (10 minutes), and failure.

#### Workflow files

| Workflow | File | Purpose |
|---|---|---|
| **CI** | [.github/workflows/merge-queue.yml](.github/workflows/merge-queue.yml) | Required status check that runs on `pull_request` and `merge_group` events. Behavior is determined by the commit message. |
| **Open Good PRs** | [.github/workflows/create-good-pr.yml](.github/workflows/create-good-pr.yml) | Creates PRs that pass checks quickly. |
| **Open Slow PRs** | [.github/workflows/create-good-pr-with-sleep.yml](.github/workflows/create-good-pr-with-sleep.yml) | Creates PRs with commit message `slow` — the CI check sleeps for 10 minutes before passing. |
| **Open Bad PRs** | [.github/workflows/create-bad-prs.yml](.github/workflows/create-bad-prs.yml) | Creates PRs with commit message `fail` — the CI check will fail in the merge queue. |

#### How the CI check decides what to do

The **CI** workflow (`merge-queue.yml`) reads the HEAD commit message of the PR branch when running in the merge queue (`merge_group` event):

- **No keyword** → passes quickly (standard PR)
- Commit message contains **`slow`** → sleeps for 10 minutes, then passes
- Commit message contains **`fail`** → exits with failure

#### Prerequisites

1. **Enable the merge queue** on the `main` branch:
   - Go to **Settings → Rules → Rulesets** (or Branch protection rules).
   - Create or edit a ruleset/branch protection rule for `main`.
   - Enable **Require merge queue** and set **Build** job as a required status check.
   - Optionally configure the merge method (squash, merge, rebase) and queue limits.

2. **Create a Personal Access Token (PAT)**:
   - The PR-creation workflows use a `PR_PAT` secret to open PRs and push branches.
   - Create a PAT with `repo` scope and add it as a repository secret named `PR_PAT`.

#### Running the demo

Run the three `workflow_dispatch` workflows **in order**, with `count: 1` for each, and add each resulting PR to the merge queue before moving to the next.

**Step 1 — Create the fast-passing PR**

1. Go to **Actions → Action - Open Good PRs** and click **Run workflow** with `count: 1`.
2. Wait for the PR to be created. Open it and click **Merge when ready** (which adds it to the merge queue).

**Step 2 — Create the slow-passing PR**

3. Go to **Actions → Action - Open Slow PRs** and click **Run workflow** with `count: 1`.
4. Wait for the PR to be created. Open it and click **Merge when ready**.

**Step 3 — Create the failing PR**

5. Go to **Actions → Action - Open Bad PRs** and click **Run workflow** with `count: 1`.
6. Wait for the PR to be created. Open it and click **Merge when ready**.

#### Expected behavior

| Position | PR type | What happens in the merge queue |
|---|---|---|
| 1st | Good (fast) | ✅ Passes quickly and merges into `main`. |
| 2nd | Good (slow) | 😴 Sleeps for 10 minutes, then ✅ passes and merges into `main`. |
| 3rd | Bad (fail) | ❌ Fails the CI check and is **removed from the queue**. The PR remains open. |

> [!NOTE]
> **Key takeaway**: The merge queue tests each PR against the accumulated base (main + previously queued PRs). When a PR fails, it is ejected from the queue without blocking PRs ahead of it. PRs behind the failed PR may be re-tested.

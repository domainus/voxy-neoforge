# Pull Latest Log Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a helper script that snapshots Prism Launcher `latest.log` into the repo for repeatable debugging and analysis.

**Architecture:** Keep the implementation as a small shell script in `scripts/` that defaults to the user-provided Prism path and copies to a repo-local `.tmp/logs/` destination. Add one focused regression test that uses an env override for the source path, then document the workflow in `scripts/README.md`.

**Tech Stack:** Bash, Python `unittest`, existing repo script conventions.

---

### Task 1: Add failing regression test

**Files:**
- Create: `scripts/test_pull_latest_log.py`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test to verify it fails before the script exists**

### Task 2: Implement the script

**Files:**
- Create: `scripts/pull_latest_log.sh`

- [ ] **Step 1: Copy the configured source log into `.tmp/logs/latest-1.21.1.log` by default**
- [ ] **Step 2: Support an optional destination argument and an env override for tests**
- [ ] **Step 3: Print the destination path for downstream tooling**

### Task 3: Document usage

**Files:**
- Modify: `scripts/README.md`

- [ ] **Step 1: Add a README section for `pull_latest_log.sh`**
- [ ] **Step 2: Show how to chain it with the existing log-analysis scripts**

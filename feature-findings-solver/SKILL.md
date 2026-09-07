---
name: feature-findings-solver
description: Walk through each finding in a Bug Report one by one, explain it to the user, collect a decision, and patch both the Bug Report and the parent Feature document. Load this skill when the primary agent routes to findings resolution.
---

This skill governs the interactive findings resolution workflow. The primary agent loads this skill and executes every step directly, including directly engaging the user for decisions. No Task delegation.

# Input

The caller must provide:
- The **path** to the Bug Report created by `feature-reviewer`.
- The **path** to the parent Feature document that was reviewed.

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and update docs; write decisions into the bug report and patch the Feature document. | **Refuse to continue.** |
| BLOCKER | `solid-deep-design` | Evaluate solution trade-offs and architecture implications of each decision. | **Refuse to continue.** |
| REQUIRED | `memory-bank` | Load project context from `documentation/Memory/`. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `glossary-management` | Look up domain terms when explaining findings or proposed solutions. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `find-docs` | Retrieve up-to-date library/framework documentation for API-specific findings. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Core Principle: Freshness Before Every Finding

The parent Feature document changes between findings because each decision patches it. Before processing any finding, re-read the parent Feature document in full to determine if the finding is still relevant. A previous decision may have inadvertently resolved or obsoleted a later finding.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the `memory-bank` skill and read all Memory Bank files to understand:
- Project architecture and conventions
- Existing ADRs and design decisions
- Current system design and module structure

## Step 2 — Load the Bug Report

Read the Bug Report document at the provided path in full. Extract:
- The list of findings with their full details (description, severity, examples, why it matters, possible solutions, recommended solution, decision).
- The findings summary table.

Sort findings by severity (critical first, then high, moderate, low). This is the order to present them.

## Step 3 — Load the Parent Feature Document

Read the parent Feature document at the provided path in full. Understand:
- The problem statement and user stories
- The proposed solution and architecture
- Affected systems, modules, and processes
- Implementation steps and task breakdown

## Step 4 — Process Findings One by One

For each finding, execute the following sub-steps in order.

### 4a — Re-read the Parent Feature Document

Re-read the parent Feature document in full to capture any changes made by previous decisions. Determine if this finding is still relevant.

### 4b — Present the Finding to the User

If the finding is **no longer relevant**, inform the user, mark it as `Dismissed` in the bug report with the reason recorded in its Decision section, and skip to the next finding.

If the finding is **still relevant**, present it clearly. Explain:
- What the problem is in plain language
- How it affects users (with user stories or scenarios)
- How it affects the code (with concrete file paths, function names, or patterns)
- Why it matters if left unresolved
- The proposed solutions in a comparison table
- The recommended solution with reasoning

### 4c — Collect the User's Decision

Use the `question` tool to ask the user what they want to do. Offer these choices:
1. Accept the recommended solution
2. Choose a different proposed solution
3. Propose their own solution
4. Dismiss the finding

Wait for the user's response. Do not proceed until they answer.

### 4d — Write the Decision to the Bug Report

Use `documentation-management` to update the Bug Report:
1. In the finding's `Decision` section, write the user's decision including the solution chosen or dismissal reason.
2. In the findings summary table, change the Status from `Pending` to `Done` or `Dismissed`.

### 4e — Patch the Parent Feature Document

Use `documentation-management` to update the parent Feature document to reflect the user's decision:
- If the decision involves changing the architecture, implementation approach, affected systems, or task breakdown, edit those sections.
- If the decision involves clarifying or correcting something, update the relevant section.
- If the finding was dismissed, leave the Feature document unchanged (unless the user explicitly asked otherwise).
- Always preserve the Feature document's structure as defined by `documentation-management`.

### 4f — Move to the Next Finding

Return to Step 4a for the next finding. Continue until all findings have been processed.

## Step 5 — Final Report

After all findings have been processed, present a summary with:
- Bug Report path and Feature document path
- Counts: Resolved, Dismissed, Auto-resolved (obsoleted by previous decisions)
- A list of decisions applied

# Guidelines for Explaining Findings

- Be concrete, not abstract. Use names of real files, real functions, real user flows.
- Show, don't just tell. Always include examples — code snippets, user stories, or scenario walkthroughs.
- Connect to the user's goals. Frame every finding in terms of what the user will experience.
- Be opinionated about the recommended solution but always give the user the final say.
- Respect the user's time. Present the finding clearly and concisely.
- Do not rush decisions. Complex findings may need discussion.
- Use the project's ubiquitous language from the glossary.

# Safe Handling of the Current Feature State

Because the Feature document is patched after every decision, it evolves during the session. When re-reading it before each finding:
- Treat the current state as the source of truth.
- If a finding references a section that no longer exists, the finding is no longer relevant.
- If a finding references code or architecture changed by a previous decision, re-evaluate whether it still applies.
- Be transparent: explain which prior decision resolved the finding and how.

# Success Criteria

A successful outcome is:
- Every finding in the bug report has a Decision recorded (not empty).
- The findings summary table is updated: no findings remain `Pending`.
- The parent Feature document reflects all accepted decisions.
- No finding was skipped unless the user explicitly asked to skip it.

# Output

Return to the caller:
1. A summary of how many findings were resolved, dismissed, and auto-resolved.
2. The updated bug report path.
3. The updated Feature document path.

---
name: doc-exploration
description: Search the project's documentation system for all documents, ADRs, features, bugs, and tasks relevant to a given work context. Load this skill when the primary agent needs to find and surface related documentation.
---

This skill governs documentation exploration. The primary agent loads this skill and executes every step directly — no Task delegation.

# Input

The caller must provide:
- A **description** of the work context — the feature, bug fix, refactor, or task being worked on.
- The **type** of documentation being sought (e.g., "everything related to authentication", "ADRs only", "all relevant docs").

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Search, list, and read docs, ADRs, Features, Bugs, Tasks, and system documentation. | **Refuse to continue.** |
| BLOCKER | `memory-bank` | Load project context from `documentation/Memory/` to understand architecture and existing decisions. | **Refuse to continue.** |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the caller and stop.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the `memory-bank` skill and read all Memory Bank files to understand the project's architecture, conventions, active work, and current state.

## Step 2 — Understand the Work Context

Parse the caller's description carefully. Identify:
- The domain area being worked on (e.g., authentication, payments, UI components)
- The type of work (feature, bug fix, refactor, architecture change)
- Key terms, modules, systems, or processes mentioned
- Any constraints or requirements stated

## Step 3 — Search Documentation Broadly

Use `documentation-management` to perform broad searches across all documentation categories:

1. **Docs**: Search for system, module, and process documentation related to the work context.
2. **Features**: Search for existing Feature documents that overlap with or relate to this work.
3. **Bugs**: Search for Bug documents that are in the same domain or describe related issues.
4. **Tasks**: Search for Task documents that are related or may be prerequisites.
5. **Code Explanations**: Search for any code explanation documents about affected modules.

## Step 4 — Deep-Dive into ADRs

ADRs (Architecture Decision Records) are the most critical documentation to check. The work may:
- Conflict with an existing decision
- Require a new decision
- Be constrained by a past decision
- Supersede a past decision

Do the following:

1. **List all ADRs** using `documentation-management`. Get a complete inventory.
2. **Read every ADR** at least at the title/decision level. Do not skip any.
3. **Identify relevant ADRs** by matching against:
   - Domain terms from the work description
   - Module or system names mentioned
   - Architectural patterns referenced (e.g., "event sourcing", "microservices", "repository pattern")
   - Technical constraints or technology choices described
   - Cross-cutting concerns the work may affect
4. For each ADR flagged as relevant, **read its full content** to understand the decision, context, consequences, and status.
5. If an ADR seems even remotely related, err on the side of including it. The caller decides relevance.

## Step 5 — Compile and Return Results

Return a structured response:

1. **Relevant ADRs** — For each:
   - File path, Title, Status (accepted/proposed/superseded/deprecated)
   - Full content
   - Why it is relevant (1-2 sentences connecting to the work context)

2. **Relevant Documentation** — For each non-ADR document:
   - File path, Type (Doc/Feature/Bug/Task/Code Explanation)
   - Full content (or clear summary if very large)
   - Why it is relevant

3. **Summary Table**:

| # | Path | Type | Title/Description | Relevance |
|---|------|------|-------------------|-----------|

# Success Criteria

A successful outcome:
- Every ADR in the project has been checked.
- All relevant ADRs are returned with full content and a relevance explanation.
- All relevant non-ADR documentation is returned with full content or summary.
- The summary table provides a quick overview of everything found.
- Nothing potentially relevant is omitted. Over-inclusion is better than under-inclusion.

# Output

Return to the caller:
1. The structured results as described in Step 5.
2. A count: total ADRs checked, relevant ADRs found, relevant non-ADR docs found.

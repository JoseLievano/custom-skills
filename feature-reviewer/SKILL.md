---
name: feature-reviewer
description: Review an existing Feature document for issues, gaps, risks, and architectural concerns. Load this skill when the primary agent routes to feature review. Produces a comprehensive Bug Report with findings.
---

This skill governs the Feature document review workflow. The primary agent loads this skill and executes every step directly. No Task delegation — the primary agent does everything itself.

# Input

The caller must provide:
- A **brief** describing what the feature document is trying to accomplish.
- The **path** to the Feature document to review.

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and create docs; create the bug report document in the correct location. | **Refuse to continue.** |
| BLOCKER | `memory-bank` | Load project context from `documentation/Memory/`. | **Refuse to continue.** |
| REQUIRED | `glossary-management` | Look up domain terms relevant to the feature. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `find-docs` | Retrieve up-to-date library/framework documentation. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `solid-deep-design` | Evaluate the feature's architecture for SOLID principles and deep-module design. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the `memory-bank` skill and read all Memory Bank files to understand:
- Project architecture and conventions
- Existing ADRs and design decisions
- Current system design and module structure

## Step 2 — Load Domain Language

Load the `glossary-management` skill and retrieve all relevant domain terms for the feature's domain. Understand the project's ubiquitous language so you can verify the feature document uses correct terminology and respects domain boundaries.

## Step 3 — Read and Analyze the Feature Document

Read the Feature document at the provided path in full. Understand:
- The problem statement and user stories
- The proposed solution and architecture
- Affected systems, modules, and processes
- Implementation steps and task breakdown
- Risk assessment and testing decisions

## Step 4 — Cross-Reference Documentation

Load the `doc-exploration` skill and execute its workflow using the feature's domain and context. Its report will surface:
- ADRs that may conflict with or constrain the feature
- Existing Docs describing affected systems or processes
- Related Features or Bugs that overlap with this feature
- Code explanations for affected modules

## Step 5 — Explore the Codebase

Launch one or more `Explore` subagents to examine the actual code that the feature document references or would affect. Each subagent returns the content of files it finds. Iterate — launch additional Explore subagents until you have a solid understanding of:

- The current implementation of affected modules and systems
- How existing code aligns (or conflicts) with what the feature document proposes
- Code-level risks the feature document may have missed (tight coupling, hidden dependencies, missing abstractions)
- Whether the feature's planned changes are consistent with existing patterns and conventions
- File paths and function signatures the feature document may reference incorrectly

## Step 6 — Validate Technical Claims

Load `find-docs` and verify any library, framework, or API claims made in the feature document. Check that:
- APIs referenced actually exist and work as described
- Version compatibility is considered
- Performance claims are reasonable
- Security patterns follow best practices

## Step 7 — Evaluate Architecture

Load `solid-deep-design` and evaluate the feature's architecture for:
- SOLID principle violations
- Module depth and interface design quality
- Coupling and cohesion concerns
- Abstraction quality
- Testability and maintainability

## Step 8 — Identify Findings

Based on all analysis, identify every issue, gap, risk, or problem. For each finding, determine:

- **Severity**: `critical`, `high`, `moderate`, or `low`
- **Description**: What the problem is, clearly stated
- **Examples**: Concrete examples such as user stories that would break, code examples showing the problem, or process examples showing workflow failures
- **Why It Matters**: The impact if left unresolved
- **Possible Solutions**: A list of viable approaches to address the finding
- **Recommended Solution**: The best solution with reasoning for why it is superior
- **Decision**: Empty — this is where the user will record their decision when they review the findings

Severity guidelines:
- **Critical**: The feature cannot succeed as designed; fundamental flaw in architecture, security, or core assumptions
- **High**: Major gap that will cause significant rework, user-facing bugs, or performance degradation
- **Moderate**: Design concern that could become problematic or represents a missed opportunity
- **Low**: Minor improvements, edge cases, or documentation gaps

## Step 9 — Link to Affected Systems

Identify which Docs (system/process/module documentation) are affected by the findings and collect their wiki links for inclusion in the bug report.

## Step 10 — Create the Bug Report

Use `documentation-management` to create a Bug document in `Bugs/to-do/`. The bug report should be structured as follows:

**Title:** Review of [Feature Document Name]

**Tags:** Include `#architectural` plus appropriate importance tag based on the highest-severity finding.

**Content:** Follow the Bug Report template from `documentation-management` but adapt it as follows:

- **Summary**: Explain that this is a review of the feature document at the given path, with N findings.
- **Findings**: List all findings with their full details as described in Step 8.
- **Findings Summary Table**: At the end of the document, include a table:

| # | Title | Severity | Status |
|---|-------|----------|--------|
| 1 | [Title] | 🔴 Critical / 🟠 High / 🟡 Moderate / 🟢 Low | Pending |

Status values:
- **Pending**: The decision section is empty — user has not yet made a choice.
- **Done**: The user has made and recorded a decision.
- **Dismissed**: The user decided not to act on this finding.

- **Affected Documentation**: A section with wiki links to Docs of the affected systems, modules, and processes:
  - [[System-Doc-Name]] — brief note on how affected

# Success Criteria

A successful outcome is a Bug document that:
- Lives in `documentation/Bugs/to-do/` as specified by `documentation-management`.
- Follows the Bug Report template structure from `documentation-management`.
- Contains a thorough analysis of every finding with all required sections.
- Includes the findings summary table at the end.
- Includes a section linking to affected Doc documents.
- Every finding has its Decision section left empty (marked as "Pending").

# Output

Return to the caller:
1. The path to the created Bug Report document.
2. A summary table of all findings ordered by severity (highest first).
3. The count of findings by severity level.

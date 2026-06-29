---
name: feature-creator
description: Create a new Feature document from an idea or description. Load this skill when the primary agent routes to feature creation. Produces a PRD-style technical specification, then reviews it for findings.
---

This skill governs the Feature document creation workflow. The primary agent (not a subagent) loads this skill and executes every step directly. No Task delegation — the primary agent does everything itself.

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and create docs; verify documentation is initialized. | **Refuse to continue.** |
| BLOCKER | `solid-deep-design` | Governs all architecture and system design decisions. | **Refuse to continue.** |
| REQUIRED | `find-docs` | Retrieve up-to-date library/framework documentation. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `memory-bank` | Load project context from `documentation/Memory/`. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `tdd` | Apply test-driven development principles to the feature specification. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `glossary-management` | Use the project's ubiquitous language and domain glossary. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Success Criteria

A successful outcome is a Feature document that:
- Lives in the correct directory as specified by `documentation-management`.
- Follows the complete Feature document structure defined by `documentation-management`.
- Is a thorough, well-explained PRD ready to guide implementation.
- Has been reviewed for findings.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Review Existing Documentation

Load the `doc-exploration` skill and execute its workflow. It will guide you to:
- Search for relevant docs, features, bugs, and tasks
- Read every ADR and identify those that relate to or constrain this feature
- Return a structured report of all relevant documentation

## Step 2 — Explore the Glossary

Use the `glossary-management` skill to look up domain terms relevant to this feature. Understand the project's ubiquitous language before proceeding.

## Step 3 — Explore the Codebase

Launch one or more `Explore` subagents to examine code relevant to this feature. Each subagent returns the content of files it finds. Iterate — launch additional Explore subagents until you are confident you have enough understanding of the affected code for this feature.

## Step 4 — Analyze and Clarify

You now have:
- The user's original feature idea.
- Relevant documentation.
- Glossary/domain terms.
- Codebase understanding.

Analyze how this feature would be implemented:
- Which modules and files would be touched.
- How the design fits into the existing architecture.
- Architectural concerns, trade-offs, and unclear areas.

Then load the `interview-me` skill and conduct a structured interview with the user. Resolve every ambiguity. Do not proceed until you have a clear, shared understanding.

## Step 5 — Write the Feature Document

Load the `to-feature` skill and use it to create the Feature document. Follow its structure and placement rules exactly.

## Step 6 — Review the Feature Document

Load the `feature-reviewer` skill and execute its workflow against the newly created Feature document. Pass it:
- The path to the new Feature document.
- A brief of what the feature is trying to accomplish.

The review workflow will produce a bug report document with findings.

## Step 7 — Report to the User

Present the final output:
1. A brief description of the Feature document and its file path.
2. A table of findings from the review, ordered by severity.

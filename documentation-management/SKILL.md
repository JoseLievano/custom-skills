---
name: documentation-management
description: Manage Obsidian-based project documentation. Use this skill whenever a `documentation/` directory exists at the project root and the user wants to create, update, move, search, or list any documentation — bugs, features, tasks, ADRs, system docs, or code explanations. Trigger on commands like "create bug", "log a feature", "update docs", "set bug as done", "list in-progress tasks", "search docs", "explain this file", "initialize documentation", "create adr", "list adrs", or any mention of the project's docs, bugs, features, tasks, or ADRs. Also trigger proactively at the start of a session when a `documentation/` directory is detected, to confirm the doc system is ready.
---

# Documentation Management

Manages Obsidian-based project documentation for any project with a `documentation/` directory at the root. All documentation is human-readable in Obsidian and also machine-readable for agents.

## Setup

At the start of any documentation task:

1. Confirm `documentation/` exists at the project root
2. Read `documentation/doc-config.json` if it exists; otherwise use the defaults below
3. Check Obsidian CLI availability by running `obsidian help` — if it fails, fall back to direct file operations for all tasks

## Config File

`documentation/doc-config.json` is project-specific and lives inside the documentation directory. If it doesn't exist for an existing project, infer the structure from the actual directory layout and suggest creating the config.

```json
{
  "vault_name": "my-project",
  "directories": {
    "bugs": "Bugs",
    "features": "Features",
    "tasks": "Tasks",
    "docs": "Docs",
    "code": "Code",
    "adrs": "ADRs",
    "rules": "rules"
  },
  "statuses": {
    "bugs": ["to-do", "in-progress", "done"],
    "features": ["to-do", "in-progress", "done"],
    "tasks": ["current", "done"],
    "adrs": ["proposed", "accepted", "deprecated", "superseded"]
  },
  "obsidian": {
    "use_cli": true,
    "vault_name": null
  }
}
```

If `vault_name` is null, omit the `vault=` parameter from all CLI commands (Obsidian will use the most recently focused vault).

## Core Rules

**Only modify files when explicitly requested.** You can read, reference, and suggest changes freely — but always confirm before writing or moving:
> "Would you like me to update [filename] to reflect this?"

**Never move files without an explicit request.** Moving a file changes its status in the project.

**When using the Obsidian CLI:**
- Prefer CLI operations when `use_cli` is true and Obsidian is running
- Always include the `silent` flag to avoid disrupting the user's Obsidian session
- Fall back to direct file operations silently if the CLI is unavailable — don't surface the error to the user unless they're specifically asking about Obsidian

## Default Directory Structure

```
documentation/
├── doc-config.json         ← This skill's config (project-specific)
├── Bugs/
│   ├── to-do/
│   ├── in-progress/
│   └── done/
├── Features/
│   ├── to-do/
│   ├── in-progress/
│   └── done/
├── Tasks/
│   ├── current/
│   └── done/
├── Docs/
├── Code/
├── ADRs/
│   └── ADR-index.md        ← Master index of all ADRs (mandatory)
├── Memory/                 ← Memory Bank files (managed by memory-bank skill)
└── rules/
```

## Obsidian Conventions

All files use Obsidian markdown. Keep these consistent across all doc types:

**Tags** — `#tag-name` (kebab-case), placed at the top of the file.
- Type: `#bug`, `#feature`, `#task`, `#adr`, `#new-feature`, `#enhancement`, `#refactor`, `#integration`
- Importance: `#low`, `#medium`, `#high`, `#critical`
- Technical: `#performance`, `#security`, `#reliability`, `#architectural`, `#optimization`, `#usability`
- Status: `#in-progress`, `#blocked`, `#needs-review`, `#adr-proposed`, `#adr-accepted`, `#adr-deprecated`, `#adr-superseded`
- ADR Domain: `#data`, `#infrastructure`, `#frontend`, `#backend`, `#api-design`, `#testing`, `#devops`, `#architecture`

**Internal links** — `[[FileName]]` or `[[Folder/FileName|Display Text]]`

**Source code references** — plain text path from project root (not as Obsidian links):
```
src/components/Auth.tsx:42
```

**Diagrams** — Use Mermaid.js for flows, sequences, and state transitions.

## Document Types

### Bug Report

A Bug Report documents the technical analysis of a defect and the roadmap to fix it. It is not the final technical implementation plan.

Use a Bug Report to explain the problem, its impact, the analysis findings, the suspected or confirmed cause, and the evidence that supports that conclusion. A Bug Report should reference the exact code locations involved, explain why those parts of the code are responsible, and include logs when they help justify the diagnosis. If the cause is not fully confirmed, say so clearly and explain the current hypothesis and uncertainty.

Bug Reports are usually the result of analyzing the codebase, behavior, and runtime evidence. They should capture the reasoning behind the diagnosis, not just the symptom. They should also explain the proposed solution and validate that direction using the relevant technology skills and up-to-date documentation from Context7 when available.

Like Features, Bug Reports should include ordered non-blocking steps to resolve the issue and a final task breakdown that groups those steps by order and complexity. Those tasks are the actual implementation plans that will later be executed.

For the required template and structure, read [bug.md](references/doc-types/bug.md).

### Feature

A Feature document defines the technical roadmap for a feature we want to build. It is not the final technical implementation plan.

Use a Feature to describe the work at a technical level: what we want to build, which systems or modules are affected, the intended architecture, the main risks, and the ordered steps required to deliver it. A Feature can include technical reasoning, code explanations, examples, and high-level implementation ideas, but it should not contain the full execution detail for each step.

The most important part of a Feature is its step breakdown. Order steps in a non-blocking way so the feature can be built progressively. Put foundational or boilerplate work before dependent work, and make sure the sequence builds the feature step by step.

Features can be very small or very large. Some may have only 1-3 steps, while others may have 10 or more. Every Feature should end with a task breakdown that groups steps into tasks by order and complexity.

Those tasks are the actual implementation plans. A task can cover one step or a small group of closely related steps, and it should contain the detailed execution guidance, code-level decisions, and implementation detail needed to perform the work. Features define the roadmap; Tasks define the execution.

For the required template and structure, read [feature.md](references/doc-types/feature.md).

### Task

A Task document is the detailed implementation plan that will actually be executed by a developer or AI agent to modify the codebase.

Use a Task to expand one feature step, one bug-fix step, or a small group of closely related steps into concrete implementation work. A Task should contain the full detail needed to perform the work: the goal, parent context, selected skills, current documentation, affected files, implementation steps, design decisions, validation plan, and completion criteria.

Before creating a Task, read its parent document if one exists. Most Tasks come from a Feature or Bug, and the parent provides the real goal, constraints, dependencies, and architectural intent behind the work. If there is no parent, make that explicit inside the Task and include the missing context directly.

When creating a Task, review the available skills and select the ones that apply to the work. When Context7 is available, use it to gather up-to-date documentation for the relevant libraries, frameworks, APIs, or tools. If stack-specific skills exist for the technologies involved, use them so the Task reflects the conventions and best practices of that stack.

Every Task must define how completion will be validated. Prefer automatic verification when possible. When validation requires manual testing, document the manual checks for the user and do not attempt to execute those manual tests on the user's behalf.

For the required template and structure, read [task.md](references/doc-types/task.md).

### Architecture Decision Record (ADR)

An Architecture Decision Record captures a significant architectural decision made during the project, along with its context and consequences. ADRs follow the format defined by Michael Nygard.

Use an ADR to document decisions that affect the structure, non-functional characteristics, dependencies, interfaces, or construction techniques of the system. An ADR is not a general design doc — it captures a single, specific, concrete decision and the forces that shaped it. Record the context (the forces at play), the decision (what we chose and why), and the consequences (what becomes easier or more difficult).

ADRs are immutable once accepted. If a decision changes, create a new ADR that supersedes the old one and update the ADR index.

The `documentation/ADRs/ADR-index.md` file is **mandatory** — it serves as the master index of all ADRs. Every time an ADR is created, superseded, or changes status, the index must be updated.

For the required template, naming convention, and detailed agent workflows (including how to number ADRs, update the index, and handle superseding), read [adr.md](references/doc-types/adr.md).

## Commands Quick Reference

### Read & Search
| Command | Action |
|---------|--------|
| `list bugs [status?]` | List bugs, optionally filtered by status |
| `list features [status?]` | List features, optionally filtered by status |
| `list tasks [status?]` | List tasks, optionally filtered by status |
| `list adrs` | List all ADRs from the index |
| `search docs [query]` | Full-text search across documentation |
| `show doc [file]` | Read and summarize a documentation file |
| `show adr [number]` | Read and summarize a specific ADR |
| `find related [topic]` | Find all docs connected to a topic or concept |

### Create
| Command | Action |
|---------|--------|
| `create bug [name]` | New bug doc in `Bugs/to-do/` |
| `create feature [name]` | New feature doc in `Features/to-do/` |
| `create task [name] for [parent]` | New task doc linked to a parent bug/feature |
| `create doc [name]` | New system/process doc in `Docs/` |
| `create code explanation [file]` | New code explanation in `Code/` |
| `create adr [title]` | New ADR in `ADRs/` with status set and index updated |

### Update
| Command | Action |
|---------|--------|
| `update doc [file]` | Refresh a doc to match current project state |
| `update code explanation [file]` | Sync code explanation with its source file |

### Status Management
| Command | Action |
|---------|--------|
| `set bug [file] as "[status]"` | Move bug: to-do → in-progress → done |
| `set feature [file] as "[status]"` | Move feature: to-do → in-progress → done |
| `set task [file] as "[status]"` | Move task: current → done |
| `set adr [number] as "[status]"` | Update ADR status (proposed, accepted, deprecated, superseded) |

### Linking & Init
| Command | Action |
|---------|--------|
| `link task [task] to [parent]` | Add task link inside a parent bug/feature step |
| `init documentation` | Create the full documentation structure for a new project |

---

For detailed step-by-step workflows for each command, read [commands.md](references/commands.md).
For file templates and required structure for each doc type, read the corresponding file under [doc-types](references/doc-types/): [bug.md](references/doc-types/bug.md), [feature.md](references/doc-types/feature.md), [task.md](references/doc-types/task.md), [code-explanation.md](references/doc-types/code-explanation.md), [system-doc.md](references/doc-types/system-doc.md), [adr.md](references/doc-types/adr.md).
For Obsidian CLI syntax and patterns, read [obsidian-cli.md](references/obsidian-cli.md).

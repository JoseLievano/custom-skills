---
name: documentation-management
description: Manage Obsidian-based project documentation. Use this skill whenever a `documentation/` directory exists at the project root and the user wants to create, update, move, search, or list any documentation — bugs, features, tasks, system docs, or code explanations. Trigger on commands like "create bug", "log a feature", "update docs", "set bug as done", "list in-progress tasks", "search docs", "explain this file", "initialize documentation", or any mention of the project's docs, bugs, features, or tasks. Also trigger proactively at the start of a session when a `documentation/` directory is detected, to confirm the doc system is ready.
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
    "rules": "rules"
  },
  "statuses": {
    "bugs": ["to-do", "in-progress", "done"],
    "features": ["to-do", "in-progress", "done"],
    "tasks": ["current", "done"]
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
├── Memory/                 ← Memory Bank files (managed by memory-bank skill)
└── rules/
```

## Obsidian Conventions

All files use Obsidian markdown. Keep these consistent across all doc types:

**Tags** — `#tag-name` (kebab-case), placed at the top of the file.
- Type: `#bug`, `#feature`, `#task`, `#new-feature`, `#enhancement`, `#refactor`, `#integration`
- Importance: `#low`, `#medium`, `#high`, `#critical`
- Technical: `#performance`, `#security`, `#reliability`, `#architectural`, `#optimization`, `#usability`
- Status: `#in-progress`, `#blocked`, `#needs-review`

**Internal links** — `[[FileName]]` or `[[Folder/FileName|Display Text]]`

**Source code references** — plain text path from project root (not as Obsidian links):
```
src/components/Auth.tsx:42
```

**Diagrams** — Use Mermaid.js for flows, sequences, and state transitions.

## Commands Quick Reference

### Read & Search
| Command | Action |
|---------|--------|
| `list bugs [status?]` | List bugs, optionally filtered by status |
| `list features [status?]` | List features, optionally filtered by status |
| `list tasks [status?]` | List tasks, optionally filtered by status |
| `search docs [query]` | Full-text search across documentation |
| `show doc [file]` | Read and summarize a documentation file |
| `find related [topic]` | Find all docs connected to a topic or concept |

### Create
| Command | Action |
|---------|--------|
| `create bug [name]` | New bug doc in `Bugs/to-do/` |
| `create feature [name]` | New feature doc in `Features/to-do/` |
| `create task [name] for [parent]` | New task doc linked to a parent bug/feature |
| `create doc [name]` | New system/process doc in `Docs/` |
| `create code explanation [file]` | New code explanation in `Code/` |

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

### Linking & Init
| Command | Action |
|---------|--------|
| `link task [task] to [parent]` | Add task link inside a parent bug/feature step |
| `init documentation` | Create the full documentation structure for a new project |

---

For detailed step-by-step workflows for each command, read `references/commands.md`.
For file templates and required structure for each doc type, read `references/doc-types.md`.
For Obsidian CLI syntax and patterns, read `references/obsidian-cli.md`.

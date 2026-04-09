---
name: memory-bank
description: Manage the project Memory Bank — a set of structured markdown files inside `documentation/Memory/` that give AI agents persistent context across sessions. Use this skill whenever the user mentions the memory bank, asks to initialize or update it, or at the start of any task when `documentation/Memory/` exists. Trigger on phrases like "initialize memory bank", "update memory bank", "read memory bank", or any task that begins in a project with a `documentation/Memory/` directory. Also trigger proactively when `documentation/Memory/` is detected at session start, to load project context and confirm alignment with the user. Depends on the documentation-management skill — `documentation/` must exist before the Memory Bank can be initialized.
---

# Memory Bank

My memory resets completely between sessions. The Memory Bank is my only link to previous work — I rely on it ENTIRELY to understand the project and continue effectively. I MUST read ALL memory bank files at the start of EVERY task. This is not optional.

The memory bank files live at `documentation/Memory/` inside the project root.

## Session Start Protocol

At the start of every task:

1. Check if `documentation/Memory/` exists and contains the core files
2. If it exists: read ALL files (brief.md, product.md, context.md, architecture.md, tech.md, progress.md, known-issues.md)
3. Report status at the top of the first response:
   - `[Memory Bank: Active]` — all core files found and read
   - `[Memory Bank: Incomplete]` — directory exists but some core files are missing
   - `[Memory Bank: Missing]` — directory does not exist or is empty
4. If Active or Incomplete: briefly confirm your understanding of the project so the user can spot misalignments. Example:

> "[Memory Bank: Active] Building a React inventory system with barcode scanning. Currently implementing the scanner component. Recent focus: OAuth2 integration (see [[Features/in-progress/OAuth2-login-integration]])."

5. If Missing: warn the user and suggest running `initialize memory bank`

## Memory Bank Files

All files live in `documentation/Memory/`. All use Obsidian markdown. Files are kept factual and concise — not creative or speculative.

### `brief.md` — User-Owned
**Created and maintained by the user.** This is the foundation document. Never edit it directly. If you notice it is outdated or could be improved, suggest the update to the user.

- Core project requirements and goals
- Scope boundaries (what this project is and is not)
- Key constraints the user has set

### `product.md` — Agent-Maintained
Generated from `brief.md` during initialization. Updated when product direction changes.

- Why this project exists and what problem it solves
- How it should work from the user's perspective
- User experience goals and non-goals

### `context.md` — Agent-Maintained
Updated at the end of every significant task. Keep it short and factual.

- Current work focus (what is actively being worked on right now)
- Recent changes (last 2–3 significant actions taken)
- Immediate next steps

### `architecture.md` — Agent-Maintained
Updated when significant structural decisions are made.

- System architecture overview
- Source code paths and their roles
- Key technical decisions and why they were made
- Design patterns in use
- Component relationships
- Critical implementation paths

### `tech.md` — Agent-Maintained
Updated when dependencies or tooling changes.

- Languages, frameworks, and key libraries with versions
- Development setup and tooling
- Technical constraints
- Tool usage patterns specific to this project

### `progress.md` — Agent-Maintained
A dated log of significant work. Most recent entries at the top. Always link to related bugs, features, or tasks using Obsidian wiki links when applicable.

- Entries must have a date (`## YYYY-MM-DD`)
- Each entry is a concise bullet — what changed and why
- Link to related documentation: `[[Bugs/done/BugName]]`, `[[Features/in-progress/FeatureName]]`, `[[Tasks/done/TaskName]]`
- Focus on decisions and outcomes, not low-level implementation details
- New entries are prepended at the top — do not reorder old entries

### `known-issues.md` — Agent-Maintained
Architectural gotchas, constraints, sharp edges, and systemic patterns that could trip up future work. **This is not a bug tracker** — do not log specific, reproducible bugs here (those belong in `documentation/Bugs/`). Update when you discover a non-obvious constraint or recurring pattern.

- Environmental quirks (build system, OS, toolchain oddities)
- Framework or library behaviors that are surprising or non-obvious
- Architectural constraints that limit future decisions
- Patterns that have caused problems before and must be avoided
- Dependencies with known sharp edges

---

## Commands

### `initialize memory bank`

**Prerequisites:** `documentation/` must exist (run `init documentation` first if needed).

This is the most critical operation — the quality of initialization determines the effectiveness of all future sessions. Be thorough.

1. Check that `documentation/` exists. If not, stop and tell the user to run `init documentation` first.
2. Check if `documentation/Memory/` already exists with files — if so, warn the user that re-initializing will overwrite agent-maintained files and ask for confirmation. `brief.md` is never overwritten.
3. Create `documentation/Memory/` if it doesn't exist.
4. **Check for `brief.md`:**
   - If it exists: read it carefully — it is the source of truth for everything else
   - If it does not exist: create `documentation/Memory/brief.md` using the template from `references/file-templates.md`, then stop and ask the user to fill it in before continuing. Do not generate the other files until `brief.md` has real content.
5. Perform an exhaustive analysis of the project:
   - All source code files and their relationships
   - Configuration files and build system setup
   - Project structure and organization patterns
   - Existing documentation
   - Dependencies and external integrations
   - Testing frameworks and patterns
6. Generate all agent-maintained files from your analysis:
   - `product.md` — derived from `brief.md` and your understanding of the codebase
   - `context.md` — current state of the project (initial: what exists, what is incomplete)
   - `architecture.md` — structure discovered during analysis
   - `tech.md` — technologies and tooling found
   - `progress.md` — initial entry dated today summarizing the state at initialization
   - `known-issues.md` — any non-obvious constraints found during analysis
7. Present a summary of what you understood about the project, organized by file. Ask the user to verify the accuracy and correct any misunderstandings.
8. Suggest: "Would you like me to create a `[[Docs/Project-Overview]]` doc linking to these memory bank files?"

---

### `update memory bank`

Triggered explicitly by the user, or suggested by the agent after significant changes.

When triggered, MUST review every memory bank file — even ones that seem unchanged.

1. Review all project files relevant to recent changes
2. Update `context.md` with current focus, recent changes, and next steps
3. Prepend a new dated entry to `progress.md` for any significant work since the last entry, with links to related bugs/features/tasks
4. Update `architecture.md` if structural decisions were made
5. Update `tech.md` if dependencies or tooling changed
6. Update `known-issues.md` if new gotchas were discovered
7. Update `product.md` if product direction changed
8. Never update `brief.md` — suggest changes to the user instead
9. After updating, confirm which files were changed and what was updated

**When to proactively suggest an update** (do not suggest for minor changes):
- After implementing a significant feature or fixing a non-trivial bug
- After a major architectural decision
- When the context window is getting full
- When the current state diverges noticeably from what `context.md` describes

---

## Session End Protocol

At the end of every task (when work appears complete):

1. Always update `context.md` to reflect the current state
2. If changes were significant: prepend a dated entry to `progress.md` with Obsidian links to any related bugs/features/tasks
3. If the change was major: suggest "Would you like me to do a full memory bank update?"

---

## Context Window Management

When the context window is filling up during an extended session:

1. Suggest updating the memory bank to preserve current state
2. Recommend starting a fresh conversation
3. Assure the user that the next session will pick up from the memory bank automatically

---

## Core Rules

- **Read all files every session** — never skip a file, even if you think it hasn't changed
- **Never edit `brief.md`** — it is user-owned; only suggest changes
- **Prioritize `brief.md`** — if memory bank files contradict it, `brief.md` wins; flag the discrepancy
- **`known-issues.md` is not a bug tracker** — link to `[[Bugs/...]]` for specific bugs; this file tracks systemic patterns only
- **`progress.md` entries must have dates** — always use `## YYYY-MM-DD` and link to related documentation
- **Keep `context.md` short** — it should be scannable in seconds; remove stale entries aggressively
- **Use Obsidian wiki links** for all cross-references to documentation files: `[[Bugs/in-progress/FileName]]`, `[[Features/to-do/FileName]]`, `[[Tasks/done/FileName]]`

---

For file templates, read `references/file-templates.md`.

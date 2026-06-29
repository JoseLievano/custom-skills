# Memory Bank File Templates

Use these templates when creating memory bank files during initialization.

---

## `brief.md` — User Template

This file is created for the user to fill in. Do not populate it with assumptions.

```markdown
# Project Brief

## What is this project?
<!-- Describe the project in 2-4 sentences. What does it do and for whom? -->

## Core goals
<!-- What are the 3-5 most important things this project must achieve? -->
-
-
-

## Scope boundaries
<!-- What is explicitly OUT of scope? What should this project never do or become? -->

## Key constraints
<!-- Technical, timeline, team, or other constraints that shape decisions. -->

## Success criteria
<!-- How will you know when this project is done or working well? -->
```

---

## `product.md` — Agent Template

Generated from `brief.md` and codebase analysis. Do not use placeholder text — populate from real understanding.

```markdown
# Product

## Purpose
<!-- Why does this project exist? What problem does it solve? -->

## How it works
<!-- High-level description of the system from the user's perspective. -->

## User experience goals
<!-- What should using this feel like? What outcomes matter to the user? -->

## Non-goals
<!-- What this product deliberately does not try to do. -->
```

---

## `context.md` — Agent Template

Keep this short. Remove stale entries. Updated at the end of every significant task.

```markdown
# Active Context

## Current focus
<!-- What is being actively worked on right now? One or two sentences. -->

## Recent changes
<!-- Last 2-3 significant things that happened. Remove when no longer relevant. -->
-
-

## Next steps
<!-- Immediate next actions, in order of priority. -->
-
-
```

---

## `architecture.md` — Agent Template

```markdown
# Architecture

## Overview
<!-- 3-5 sentence description of the system structure. -->

## Source code map
<!-- Key directories and files and what they do. -->
| Path | Role |
|------|------|
| `src/` | |

## Key technical decisions
<!-- Decisions made and why. Include alternatives that were rejected if relevant. -->

## Design patterns
<!-- Patterns consistently used in this codebase. -->

## Component relationships
<!-- How major parts connect. Use a Mermaid diagram if helpful. -->

## Critical paths
<!-- The most important code paths — the ones that must always work. -->
```

---

## `tech.md` — Agent Template

```markdown
# Tech Stack

## Languages & Frameworks
| Technology | Version | Role |
|-----------|---------|------|
| | | |

## Key dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| | | |

## Development setup
<!-- How to get the project running locally. -->

## Technical constraints
<!-- Things the tech stack cannot or should not do. -->

## Tooling & patterns
<!-- Build system, linters, test runner, CI, deployment — and any project-specific usage patterns. -->
```

---

## `progress.md` — Agent Template

Most recent entries at top. New entries are prepended — never reorder existing entries.

```markdown
# Progress

## YYYY-MM-DD
<!-- Replace with actual date. First entry created during initialization. -->
- Memory bank initialized. Project analysis complete.
<!-- Add entries below for any significant state discovered during init. -->
```

**Entry format for subsequent updates:**
```markdown
## YYYY-MM-DD
- [What was done and why it matters] → [[Bugs/done/FileName]] or [[Features/in-progress/FileName]]
- [Another significant change]
```

---

## `known-issues.md` — Agent Template

```markdown
# Known Issues & Constraints

This file tracks architectural gotchas, systemic patterns, and non-obvious constraints.
It is NOT a bug tracker — specific bugs belong in `documentation/Bugs/`.

## Environmental
<!-- Build system, OS, toolchain, or CI quirks. -->

## Framework / Library behaviors
<!-- Surprising or non-obvious behaviors in dependencies. -->

## Architectural constraints
<!-- Structural limitations that affect future decisions. -->

## Patterns to avoid
<!-- Things that have caused problems before. -->

## Sharp edges
<!-- Dependencies or integrations with known tricky behaviors. -->
```

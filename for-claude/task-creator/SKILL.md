---
name: task-creator
description: Create a new Task document from a parent document (Feature, Bug, or other) that specifies a list of implementation tasks. Load this skill when the primary agent routes to task creation. Produces a deeply detailed technical implementation plan ready for execution, then reviews it with the task-reviewer.
---

This skill governs the Task document creation workflow. The primary agent loads this skill and executes every step directly. No Task delegation — the primary agent does everything itself.

# Input

The caller must provide:
- The **path** to the parent document (Feature, Bug Report, or other document) that contains the task list / step breakdown.
- The **task identifier** to create (e.g., "Task 2", "Step 3", "Phase 2 — Step 2.1").

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and create docs; verify documentation is initialized; follow the Task template. | **Refuse to continue.** |
| BLOCKER | `solid-deep-design` | Governs all architecture and system design decisions for the implementation plan. | **Refuse to continue.** |
| REQUIRED | `find-docs` | Retrieve up-to-date library/framework documentation at the exact version the project uses. Do not rely on internal knowledge for API details. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `memory-bank` | Load project context from `documentation/Memory/`. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `tdd` | Apply test-driven development principles to the implementation plan and define the test strategy. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `glossary-management` | Use the project's ubiquitous language and domain glossary. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Success Criteria

A successful outcome is a Task document that:
- Lives in the correct directory as specified by `documentation-management` (`documentation/Tasks/current/`).
- Follows the complete Task document structure defined by `documentation-management` (see `references/doc-types/task.md`).
- Is a deeply detailed, technically correct implementation plan that a developer or AI agent can execute with confidence.
- Reflects the parent document's intent, constraints, and architectural direction accurately.
- Accounts for all previous completed tasks in the parent's task list and the state of the codebase after those tasks.
- Uses version-matched documentation for every library, framework, API, and tool referenced.
- Has a test strategy with automatic validation steps and, when necessary, manual validation steps for UI/GUI work.
- Has been reviewed for findings by the `task-reviewer` skill.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the `memory-bank` skill and read all Memory Bank files to understand:
- Project architecture and conventions
- Existing ADRs and design decisions
- Current system design and module structure
- Coding standards and patterns used in the project

## Step 2 — Load Domain Language

Load the `glossary-management` skill and retrieve all relevant domain terms for the parent document's domain. Understand the project's ubiquitous language so the Task document uses correct terminology and respects domain boundaries.

## Step 3 — Review Existing Documentation

Load the `doc-exploration` skill and execute its workflow using the parent document's domain and context. Its report will surface:
- ADRs that may constrain or guide the Task's implementation approach
- Existing Docs describing affected systems or processes
- Related Features or Bugs that overlap with this work
- Code explanations for affected modules

Use this report to understand the full documentation landscape before writing the Task.

## Step 4 — Read and Analyze the Parent Document

Read the parent document at the provided path in full. Understand:
- The overall goal, problem statement, and motivation
- The architecture and design decisions the parent proposes or constrains
- Systems, modules, and processes affected
- The complete task list / step breakdown and how tasks relate to each other
- Dependencies between tasks and their execution order
- Constraints, risks, and testing decisions that apply to all tasks

Then, locate the specific task to create within the parent's task list. Extract:
- The task's goal and scope as defined by the parent
- Any specific requirements, files, or approaches the parent mandates for this task
- How this task depends on previous tasks and what it enables for subsequent tasks
- The completion criteria the parent expects for this task

If the parent document also references individual Task documents (via wiki links like `[[Task-Name]]`), note those links so you can cross-reference them in Step 5.

## Step 5 — Analyze Previous Completed Tasks

This is a critical step. The task you are creating does **not** exist in isolation — it builds on work that has already been done.

### 5a — Find Previous Task Documents

Identify all tasks in the parent's task list that come **before** the task you are creating. For each:
- Search for the corresponding Task document in `documentation/Tasks/current/` or `documentation/Tasks/done/` using the naming conventions defined by `documentation-management`.
- If a Task document exists, read it in full. Understand what was implemented, what design decisions were made, what files were created/modified, and what the final state of that work was.
- If a Task document does not exist yet but a previous task expects to have been completed, note this as a risk. The Task you create may need to account for the missing state.

### 5b — Explore Code Changes from Previous Tasks

Launch one or more `Explore` subagents to examine the codebase for changes made by the previous tasks. Focus on:
- New files created or modified by previous tasks
- New patterns, abstractions, or utilities introduced that this task should reuse
- The current shape of affected modules after previous tasks were applied
- Any differences between what the previous Task documents described and what actually exists in the codebase

The goal is to understand the **current state** of the codebase so the Task you write is accurate and builds on real, existing code — not on assumptions about what should exist.

## Step 6 — Explore the Broader Codebase

Expand exploration beyond the previous tasks. Launch additional `Explore` subagents to understand:
- The overall architecture of affected systems and modules
- Existing conventions, patterns, and code style in the affected areas
- Interfaces, types, and APIs already in place that the Task will interact with
- Potential edge cases, coupling points, or risks the Task should address

## Step 7 — Gather Version-Matched Technical Documentation

This step is mandatory whenever the Task involves any library, framework, API, CLI tool, CMS, or external technology.

### 7a — Identify Project Versions

Before querying any documentation, identify the **exact versions** of the technologies used in the project. Check:
- `package.json` (dependencies and devDependencies) for JavaScript/TypeScript projects
- `pom.xml` or `build.gradle` for Java projects
- `requirements.txt`, `pyproject.toml`, or `Pipfile` for Python projects
- `Cargo.toml` for Rust projects
- `Gemfile` for Ruby projects
- `composer.json` for PHP projects
- Any other project-specific dependency manifests

If the project does not pin exact versions (e.g., uses ranges like `^2.0.0`), note the resolved/lock-file version.

### 7b — Query Documentation at the Correct Version

Load the `find-docs` skill and, for each technology the Task will use:
- Query documentation at the **exact version** the project uses. Do not query for the latest version unless the project actually uses it.
- If the project uses Java 8, query Java 8 documentation — not Java 21.
- If the project uses React 17, query React 17 documentation — not React 19.
- If the project uses an older API version, query that version's docs — not the latest.

Use the version-verified documentation to validate:
- API signatures, method names, and parameter types used in code examples
- Configuration syntax and options
- Deprecated features to avoid
- Compatible patterns and best practices for the specific version

**Never trust internal knowledge alone for API details, signatures, or configuration options.** Always verify against the version-matched documentation.

## Step 8 — Design the Implementation Architecture

Load the `solid-deep-design` skill and, informed by all the context gathered so far, design the implementation architecture for this task:

- Apply SOLID principles to the design of new modules, classes, and functions
- Design for deep modules with minimal, stable interfaces
- Evaluate coupling and cohesion — ensure new code integrates cleanly with existing systems
- Plan for testability from the start
- Identify abstractions that serve this task while remaining consistent with the codebase's existing abstraction patterns
- Consider how the design decisions made here will affect subsequent tasks in the parent's task list

Document the design decisions, trade-offs, and rejected alternatives. These will become part of the Task document's **Design Decisions** section.

## Step 9 — Write the Task Document

Use `documentation-management` to create the Task document. Place it in `documentation/Tasks/current/` following the naming convention:
```
[ParentName]-step-[N]-[short-description].md
```

Follow the complete Task template from `documentation-management` (`references/doc-types/task.md`). Populate every section with thorough, actionable detail:

### Required Sections

| Section | What to Include |
|---------|----------------|
| **Tags** | `#task #current`, appropriate complexity tag, parent reference tag |
| **Parent** | Wiki link to the parent document and parent type (Feature / Bug / Standalone) |
| **Related Step(s)** | The specific step(s) from the parent this task covers |
| **Goal** | 1-2 sentences on what this task accomplishes and why |
| **Parent Context** | Summary of what the parent says about this task — goals, constraints, dependencies, architectural decisions |
| **Preconditions / Dependencies** | Prior tasks, configurations, or prerequisites that must already exist |
| **Skills and Documentation Preparation** | Skills reviewed and selected, documentation consulted with version info |
| **Related Existing Code** | Wiki links and source paths for relevant existing files |
| **Implementation Details (Approach)** | Strategy, design pattern, component interactions, key decisions — informed by `solid-deep-design` |
| **Files to Create/Modify** | Checkbox list of every file with its purpose |
| **Step-by-Step Implementation** | Each step with goal, dependencies, concrete actions, and code examples verified against version-matched docs |
| **Edge Cases** | For each implementation step, describe edge cases and how they are handled |
| **Design Decisions** | Each decision with reasoning, trade-offs, and rejected alternatives |
| **Testing Considerations** | Automatic and manual validation (see Step 10) |
| **Related Code Explanations** | Wiki links and paths to related files |
| **Completion Criteria** | Checkbox list of all conditions that must be met for the task to be considered done |

### Code Examples

When including code examples in the **Step-by-Step Implementation** section:
- Use the exact syntax, APIs, and patterns verified against version-matched documentation
- Match the project's existing code style, conventions, and patterns
- Show the code in context — not isolated snippets that lack necessary imports or setup
- Include inline reasoning where it helps explain why a particular approach was chosen

## Step 10 — Define the Test Strategy

Load the `tdd` skill and define the test strategy for this task. Add to the **Testing Considerations** section of the Task document:

### Automatic Validation

Define automatic checks as a checkbox list. These should be commands or tests the developer/agent can run to verify correctness:
- Unit tests for new functions, methods, or classes
- Integration tests for component interactions
- Lint and type-check commands
- Build verification commands
- Any project-specific test runners or frameworks

Each checkbox should be a concrete, executable action. Prefer:
- `[ ] Run \`pytest tests/test_auth.py -v\`` over `[ ] Write tests for auth`
- `[ ] Run \`npm run typecheck\`` over `[ ] Type check passes`

### Manual Validation

If the Task involves UI, GUI, visual output, or any behavior that cannot be reliably tested programmatically, add a **Manual Validation** subsection with checkboxes for the user to perform.

**Decision rule for automatic vs. manual:**
- If a UI/GUI test can be implemented **simply** using a testing library already in the project (e.g., React Testing Library, Playwright, Selenium already configured), include it as automatic validation.
- If implementing a UI/GUI test would require **significant setup** (installing new test frameworks, writing complex selectors, mocking browser APIs), do not attempt it. Instead, document the manual check for the user.
- For CLI output, logs, or text-based output, prefer automatic validation via stdout/stderr assertions.
- For visual layout, animations, or complex interactive behavior, prefer manual validation.

Manual validation items should describe exactly what the user should observe or verify:
- `[ ] Navigate to /dashboard and confirm the new widget renders correctly`
- `[ ] Verify the error toast appears with the correct message when submitting an empty form`
- `[ ] Confirm the button changes to a loading state during form submission`

## Step 11 — Review the Task Document

Load the `task-reviewer` skill and execute its workflow against the newly created Task document. Pass it:
- The path to the new Task document.
- A brief of what the Task is trying to accomplish and its parent context.

The `task-reviewer` will analyze the Task document, identify findings, and autonomously patch them — from most critical to lowest severity. It will return:
- Confirmation that the review is complete
- A summary table of all findings patched

No further action is needed after the review. The Task document is now reviewed, patched, and ready for execution.

## Step 12 — Report to the User

Present the final output:

1. **Confirmation**: A brief statement that the Task document has been created and reviewed.

2. **Document path**: The path to the new Task document.

3. **Task summary**: 2-3 sentences describing what the Task covers.

4. **Previous tasks analyzed**: List the previous Task documents that were analyzed (if any).

5. **Review findings table**: The summary table from `task-reviewer` showing findings that were patched during review:
   | # | Finding | Severity | Solution Applied |
   |---|---------|----------|------------------|
   | 1 | ... | 🔴 / 🟠 / 🟡 / 🟢 | ... |

6. **Manual validation notice**: If the Task includes manual validation steps, clearly state this:
   > **Manual validation required.** This task includes [N] manual validation steps that must be performed by a human. See the "Manual Validation" section in the Task document.

7. **Counts**: Total findings patched by severity level.

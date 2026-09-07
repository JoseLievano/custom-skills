---
name: task-executor
description: Execute an existing Task document end to end — implement the code, run the validations, self-review the result, patch every issue found, and update the Task document's completion criteria in place. Use this skill whenever the user asks to implement, execute, build, or run a Task document, says things like "implement task 4", "execute documentation/Tasks/current/....md", "build out this task doc", or "implement the plan we just wrote", and whenever an orchestrator dispatches a Task document for implementation. Covers the full cycle: implement, validate, review, fix.
---

# Task Executor

This skill takes a fully specified Task document and turns it into working, reviewed
code. You perform the whole cycle yourself: understand the Task, implement it, run
validations, review what you wrote, patch what you find, update the Task document, and
report.

The self-review in Step 7 is the part that matters most. Code that was just written by
the same agent that planned it is exactly where confident mistakes hide, so the review
is a separate pass with fresh eyes over every file you touched — not a formality.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| **Task document path** | Yes | The path to the Task `.md` document to execute. |
| **Technology stack** | Yes | The languages, frameworks, libraries, and technologies the task involves — e.g. `React, Express, PostgreSQL`, `Spring Boot, JPA, H2`, `Electron, React, MySQL`. Used to load matching skills. |

The technology stack list is load-bearing: it decides which technology skills get loaded,
and a wrong or thin list quietly degrades implementation quality. Check it against what
the Task document actually references.

When a person invoked this skill directly and an input is missing, ask them for it. When
an orchestrator dispatched you, there is nobody to answer — stop immediately and report
why you cannot continue.

## Loading a skill

Invoke each skill with the `Skill` tool, by name. If the harness has no `Skill` tool,
read `~/.claude/skills/<skill-name>/SKILL.md` (or the project's
`.claude/skills/<skill-name>/SKILL.md`) and follow it directly.

## Workflow

### Step 1 — Extract and validate inputs

Pull the Task document path and technology stack from the prompt.

Read the Task document to verify it exists and to understand the goal and scope, the
files to create or modify, and the expected completion criteria. If it does not exist,
say so and stop.

If the stack list looks incomplete given what the Task document references — the Task
describes React components but the list says only `Express, PostgreSQL` — note the
discrepancy in your final report and proceed with the list you were given plus whatever
the Task document clearly implies. Do not stop to ask; continue autonomously.

### Step 2 — Load prerequisite skills

| Priority | Skill | Purpose |
|----------|-------|---------|
| OBLIGATORY | `memory-bank` | Project context from `documentation/Memory/` — architecture, conventions, ADRs, coding standards. |
| OBLIGATORY | `documentation-management` | Task document structure, documentation navigation, completion-criteria updates. |

Read all Memory Bank files and confirm the documentation system is ready.

### Step 3 — Load implementation skills

| Skill | Purpose |
|-------|---------|
| `solid-deep-design` | Apply SOLID principles and deep-module design to every module, class, and function you write. |
| `find-docs` | Verify every library, framework, and API call against version-matched documentation. Do not trust internal knowledge for API details — that is where silent breakage comes from. |
| `tdd` | Apply test-driven development and follow the test strategy defined in the Task document. |

Then, for each technology in the stack list, check whether a matching skill exists — for
example `react-code-organization` for React, `react-best-practices` for React
performance, `shadcn-component-review` for shadcn UI components. Load the ones that
exist and follow their conventions. If no skill matches a technology, proceed without
one; that is fine.

### Step 4 — Build execution context

Read the Task document in full and extract:

- The implementation goal and scope.
- The parent document reference, if present.
- The exact files to create or modify.
- The step-by-step implementation plan.
- The testing strategy and validation commands.
- The completion criteria and any manual validation requirements.

Read the parent document too, when the Task references one, to understand the broader
requirements. Where the Task document and the codebase disagree, resolve it in favor of
what makes the codebase correct — the plan was written against an earlier state — and
record the deviation for the final report.

### Step 5 — Implement

1. Follow the Task document's step-by-step plan.
2. Write tests first where the Task defines testable behavior, per `tdd`.
3. Match the project's existing conventions, patterns, and code style.
4. Apply `solid-deep-design` so new and modified modules are cohesive, testable, and
   appropriately deep.
5. Implement the edge cases the Task document describes.
6. Keep changes inside the Task scope. Do not rewrite unrelated code.

If a requirement is impossible because the codebase differs from what the Task assumed,
implement the closest correct solution and document the deviation.

### Step 6 — Validate

Run the automatic validation checks from the Task document's "Testing Considerations"
section, plus the project's lint, typecheck, test, and build commands where they exist
and are relevant to the files you changed.

When a validation command is unavailable, fails for an unrelated pre-existing reason, or
cannot run in this environment, record that plainly in the final report — and in the Task
document when it affects completion status. Do not report a check as passing because it
was skipped.

### Step 7 — Review and auto-patch

Review the implementation before reporting success. Examine every file you created or
modified, looking for:

- **Bugs** — logic errors, incorrect API usage, unhandled edge cases, null/undefined
  handling, race conditions.
- **Architectural issues** — SOLID violations, tight coupling, shallow abstractions,
  misplaced responsibilities.
- **Correctness gaps** — missed Task steps, incomplete requirements, behavior that does
  not match the parent document.
- **Code quality** — style violations, inconsistent patterns, missing error handling,
  poor naming.
- **Test gaps** — missing edge-case coverage, tests that do not actually verify behavior,
  flaky tests.
- **Documentation accuracy** — comments or Task status that no longer match the code.

Then patch what you can within the Task scope:

1. Fix bugs directly in the source files.
2. Refactor architectural issues when the fix is proportional to the Task scope.
3. Add or correct tests for meaningful gaps.
4. Update inaccurate comments or documentation.
5. Re-run validation after each meaningful batch of fixes.

If you find a fundamental architectural problem whose fix would mean redesigning the
feature beyond this Task's scope, do not start a large refactor. Flag it in the final
report and record it in the Task document under `## Post-Review Notes`.

### Step 8 — Update the Task document

Read the Task document one final time, then update it **in place**:

- Keep it at its original input path. Do not move, rename, copy as a lifecycle
  transition, or relocate it to `done`, `completed`, `in-progress`, or any other
  directory. Moving Task documents is the user's call, not yours.
- Edit only completion criteria, validation status, review notes, and other Task-specific
  status information.
- Check off each completion criterion that is fully satisfied.
- Leave manual validation criteria unchecked unless they can genuinely be verified
  automatically.
- Leave any unmet criterion unchecked and document its current status.
- Add or update a `## Post-Review Notes` section when unresolved issues remain.
- When all automatic criteria are met, mark the task as ready for the user's manual
  validation, where that applies.

### Step 9 — Report

Return:

1. **Task document path** — the document that was executed.
2. **Implementation summary** — what was implemented and which files changed.
3. **Validation summary** — which commands ran and whether they passed.
4. **Review summary** — bugs fixed, architectural fixes made, test gaps filled, and
   anything left unresolved.
5. **Completion status** — whether all automatic completion criteria are now checked off.
6. **Manual validation notice**, when the Task includes manual steps:
   > **Manual validation required.** This task includes [N] manual validation steps that
   > must be performed by a human. See the "Manual Validation" section in the Task
   > document.
7. **Closing statement**:
   > Task execution and review complete. The Task document has been implemented and
   > autonomously reviewed. No further automated work is needed.

Returning this report matters: when an orchestrator dispatched you, it is the only thing
it sees, and it decides what happens to the next task.

## Execution notes

- **Execute directly.** Implementation, validation, review, patching, and Task document
  updates are all yours.
- **Read the Task document before writing code.** You need the scope to sanity-check the
  technology stack list and to report accurately.
- **Never move the Task document.** It stays at the path you were given for the entire
  workflow; update it in place only.
- **Keep the scope bounded.** Implement the Task, not adjacent improvements or unrelated
  refactors.
- **Preserve user work.** If the worktree has unrelated user changes, do not revert or
  overwrite them. Work around them unless they directly conflict with the Task
  requirements.
- **Prefer the file-editing tool; bash is the fallback.** Use the editing tool first. If
  it is unavailable or denied by the runtime, `bash` may create or edit files within the
  Task scope. Avoid destructive commands.

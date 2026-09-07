---
name: task-orchestrator
description: Implement every ordered task in a parent document — a Feature, Bug Report, ADR follow-up, or any implementation roadmap — one task at a time, creating a Task document, executing it, reviewing it, marking progress, and asking for approval before moving on. Use this skill whenever the user wants to implement a feature or bug document, work through a task list, or says things like "implement this feature", "start on the tasks", "run through the task breakdown", "continue with the next task", or "pick up where we left off" on a partially-completed roadmap. Resumes correctly from whatever is already done.
---

# Task Orchestrator

This skill implements a parent document completely by processing its task list in strict
order. For each task it creates a detailed Task document, executes it, reviews and
patches the implementation, marks progress, and then asks the user before continuing.

You do not implement code yourself here. You orchestrate: you own the sequencing, the
progress marking, and the conversation with the user, and you dispatch the actual
creation and execution work.

Order is the whole point. Task `N + 1` routinely depends on code and documentation that
Task `N` produces, so tasks are never reordered and never run in parallel — a plan that
looks parallelizable on paper usually is not once the code exists.

## Input

| Input | Required | Description |
|-------|----------|-------------|
| **Parent document path** | Yes | A Feature, Bug Report, or other parent document containing an ordered task list. |

If the parent document path is missing, stop immediately and report that the required
input was not provided. Do not ask follow-up questions to get started.

## Loading a skill

Invoke each skill with the `Skill` tool, by name. If the harness has no `Skill` tool,
read `~/.claude/skills/<skill-name>/SKILL.md` (or the project's
`.claude/skills/<skill-name>/SKILL.md`) and follow it directly.

## Delegation model

Each task's creation and execution runs in a **separate subagent**, dispatched with the
`Agent` tool using `subagent_type: "general-purpose"`. The subagent invokes the
`task-creation` or `task-executor` skill and returns a report.

This matters for two reasons: the implementation detail of task 3 does not have to sit
in your context while you run task 7, and you stay in the main context where you can
actually talk to the user for the approval gates.

If no `Agent` tool is available in the harness, run the `task-creation` and
`task-executor` skills inline instead and continue the same workflow. Everything else is
unchanged; you just carry more context.

## Mandatory skills

Load these before any orchestration work. If one is unavailable, stop and report the
blocker.

| Skill | Purpose |
|-------|---------|
| `memory-bank` | Project context from `documentation/Memory/`: architecture, conventions, ADRs, current progress, known issues. |
| `documentation-management` | Parent document types, Task document structure, task lifecycle, documentation update rules. |
| `solid-deep-design` | Keep the whole implementation sequence aligned with SOLID and deep-module architecture. |
| `doc-exploration` | Surface relevant ADRs, docs, code explanations, Features, Bugs, and Tasks before orchestration begins. |
| `find-docs` | Ensure downstream task creation and execution can verify version-matched framework, library, API, and tool documentation. |

## Workflow

### Step 1 — Load the mandatory skills

Load `memory-bank`, `documentation-management`, `solid-deep-design`, `doc-exploration`,
and `find-docs`. Use them to understand the project's architecture, documentation system,
relevant ADRs, and current state before you touch the parent document.

### Step 2 — Read and validate the parent document

Read the parent document in full, then confirm it contains a clear, ordered task list:

- A dedicated task section, usually near the end — `Task Breakdown`, `Tasks`,
  `Implementation Tasks`, or equivalent.
- Numbered or otherwise explicitly ordered entries.
- Enough detail to identify each task's purpose and boundaries.
- A sequence that can be processed one task at a time.

If there is no valid ordered task list, stop and report:

```
Cannot continue: the parent document does not contain a valid ordered task list.
```

Do not infer an implementation sequence from unrelated prose. A sequence you invented is
not the one the document's author intended, and every downstream Task document would
inherit that guess. The parent document must define the tasks explicitly.

### Step 3 — Extract, filter, and find the starting point

Extract every task in order. For each one capture: the identifier (`Task 1`, `Task 2`,
…), the title, a brief description of what it implements, its dependencies on previous
tasks, and any files, modules, technologies, or validation notes the parent document
mentions.

Preserve the document's exact order. Never reorder for convenience.

**3a — Determine completion status.** For each task, check the parent document's
completion markers: checked checkboxes (`[x]`), `DONE`, `COMPLETE`, strikethrough, or
whatever convention that document uses. If a task entry links to a Task document under
`documentation/Tasks/`, read it and verify its completion criteria are actually checked
off.

A task is **done** when the parent document marks it complete *and*, if a linked Task
document exists, that document's automatic completion criteria are checked off. Otherwise
it is **pending**.

**3b — Identify the starting point.** Walk the list from the beginning; the first task
that is not done is where the work begins. If every task is done, report "All tasks in
the parent document are already complete." and stop.

**3c — Report before proceeding.** Tell the user: total tasks found, how many are already
done (with identifiers), how many remain pending, and which task will be processed first.

### Step 4 — Process each pending task, one at a time

Starting from the task identified in 3b, run the full create-and-execute cycle for every
remaining pending task, in order. Skip the ones already marked done in Step 3.

**Read `references/task-cycle.md` now** — it contains the eight sub-steps of the cycle
(4a–4h), including the exact subagent prompt templates, the two user approval gates, and
the progress-marking rules. Follow it for every task, then return here for Step 5.

Never start a second cycle before the current one finishes.

### Step 5 — Final parent document and Memory Bank update

Once every task has completed successfully:

- Ensure every parent task entry links to its Task document.
- Ensure completed tasks are checked off or marked complete in the parent document's own
  style.
- Add a brief implementation summary if the parent document has a progress, status, or
  implementation-notes section.
- Do not rewrite unrelated sections of the parent document.

If `documentation-management` says the parent document's status should move to done, only
do that when every task completed and no manual validation or unresolved blocker remains.

Update the Memory Bank with the final state: all tasks completed, final implementation
status, and any remaining manual validation items.

### Step 6 — Report final results

Return:

1. The parent document path.
2. Confirmation that all tasks were processed in order.
3. A results table:

   | # | Task | Task document | Technologies | Implementation | Review | Manual validation |
   |---|------|---------------|--------------|----------------|--------|-------------------|
   | 1 | [Task title] | [path] | [tech list] | Complete | Complete | None / Pending |

4. Any tasks that could not be fully completed, if the workflow stopped early.
5. Any manual validation still required.
6. Confirmation that the parent document and Memory Bank have been updated.
7. A closing statement that the orchestration workflow is complete.

## Failure policy

This skill runs autonomously *within* each task but requires user approval *between*
tasks. Stop immediately and report the reason when:

- The parent document path is missing.
- The parent document cannot be read.
- The parent document has no valid ordered task list.
- A mandatory skill cannot be loaded.
- Task creation fails for a task.
- Task execution fails for a task.

In these cases report the blocker and exit rather than asking for clarification — and
always say which tasks completed before the failure, so the user can resume cleanly.

## Execution notes

- **Task order is mandatory.** Never reorder, never parallelize.
- **Creation and execution are separate phases per task.** Always create and review the
  Task document before executing it, and let the user approve the transition (4d).
- **Always wait for a dispatched subagent to finish.** Intermediate progress messages —
  including "created the Task, beginning review" — are not final results.
- **Do not duplicate the reviews.** `task-creation` reviews the Task document;
  `task-executor` reviews the code. Reviewing again from here wastes effort and produces
  conflicting patches.
- **Respect manual validation boundaries.** An agent cannot complete a manual UI or GUI
  check unless the project has genuinely automated it. Never mark one done on a guess.
- **Never move Task documents between directories.** Update file contents only — moving a
  Task document from `current/` to `done/` is the user's decision.
- **Always update the Memory Bank when the workflow stops**, whether it stopped because
  the user asked or because the work finished. The Memory Bank is what makes the next
  session resumable.

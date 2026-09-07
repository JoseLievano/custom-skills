# The Per-Task Cycle (Step 4)

Run these eight sub-steps for every pending task, in order, before starting the next
task. Two of them (4d and 4h) are user approval gates — they run in your context, not in
a subagent, because a subagent has nobody to ask.

## 4a — Create a task brief

Analyze the current task and write a short brief containing:

- The task number or identifier.
- The task's goal.
- Why it exists in the parent document.
- Which previous tasks should already be complete.
- Any important constraints, dependencies, or risks.

This is supporting context only. The `task-creation` skill still reads the full parent
document itself — the brief tells it what to pay attention to, it does not replace the
source.

## 4b — Dispatch task creation

Dispatch a subagent with the `Agent` tool (`subagent_type: "general-purpose"`) using this
prompt:

```
Invoke the `task-creation` skill with the Skill tool and follow it end to end.
If no Skill tool is available, read ~/.claude/skills/task-creation/SKILL.md
(or .claude/skills/task-creation/SKILL.md in the project) and follow it directly.

Create the Task document for [TASK_IDENTIFIER] from parent document
[PARENT_DOCUMENT_PATH].

Brief:
[TASK_BRIEF]

Progress context:
All tasks before [TASK_IDENTIFIER] in the parent document's ordered task list have
already been completed in sequence by this orchestrator, if any exist. Use the previous
Task documents and the current state of the codebase as context.

Return the path to the created Task document, a short description of it, the review
status, and any review findings patched by task-reviewer.
```

If the harness has no `Agent` tool, invoke the `task-creation` skill inline with the same
inputs.

Wait until the subagent returns its final report. It may emit an intermediate message
saying it created the Task and is beginning review — that is not completion.

**On failure**, stop the entire workflow and report: which task failed, the parent
document path, the failure reason returned, and which tasks completed before the failure.

## 4c — Read the created Task document

Read the Task document the subagent returned and extract:

- The Task document path.
- A brief summary of the Task's main goal.
- The files to create or modify.
- The libraries, frameworks, languages, tools, services, databases, APIs, CMSs, runtimes,
  or platforms involved.

Read it yourself rather than trusting the subagent's summary — you are about to build the
technology stack list from it, and that list determines which skills the executor loads.

## 4d — Approval gate: proceed to execution?

Pause and report to the user before executing:

- The Task document path.
- A 2–3 sentence summary of what the task will implement.

Then ask whether to continue with execution. Write this question as **plain text in the
chat** — do not use a question tool here. The user may want to read the Task document,
ask about it, request changes, or stop, and a two-button prompt gets in the way of that.
Any "continue", "yes", "go ahead", or similar signal means proceed to 4e.

**If the user wants to stop:**

1. Note in the Task document that it was created but not yet executed.
2. Update the parent document to record that the Task document exists but execution was
   deferred.
3. Update the Memory Bank with the session state — tasks completed, Task documents created
   but not executed, tasks remaining.
4. Stop and report: the Task document path (created, not executed), which tasks completed
   before the pause, and the remaining tasks with their status.

## 4e — Extract the technology stack list

Build the technology list the executor needs. Include everything the task touches:

- Languages: `TypeScript`, `Java`, `Python`, `Rust`.
- Frameworks: `React`, `Next.js`, `Spring Boot`, `Django`, `Electron`.
- Libraries: `Prisma`, `JPA`, `React Hook Form`, `TanStack Query`.
- Databases: `PostgreSQL`, `MySQL`, `SQLite`, `MongoDB`.
- UI systems: `shadcn/ui`, `Radix UI`, `Tailwind CSS`.
- Build and test tools: `Vite`, `Webpack`, `Jest`, `Vitest`, `Playwright`, `Pytest`.
- APIs, SDKs, CLIs, CMSs, cloud providers, external services.

If a technology is implied by the project configuration or the Task document but never
named outright, include it anyway and note internally that it was inferred. An incomplete
list means the executor loads the wrong skills, so err toward including a technology you
are unsure about. The prompt itself should carry a plain list of names.

## 4f — Dispatch task execution

Dispatch a subagent with the `Agent` tool (`subagent_type: "general-purpose"`) using this
prompt:

```
Invoke the `task-executor` skill with the Skill tool and follow it end to end.
If no Skill tool is available, read ~/.claude/skills/task-executor/SKILL.md
(or .claude/skills/task-executor/SKILL.md in the project) and follow it directly.

Execute this Task document: [TASK_DOCUMENT_PATH]

Technology stack list:
[TECH_STACK_LIST]

Task goal summary:
[TASK_GOAL_SUMMARY]

Implement the task, review the implementation, patch issues autonomously, update the Task
document completion criteria in place, and return the final execution and review report.
```

If the harness has no `Agent` tool, invoke the `task-executor` skill inline with the same
inputs.

Wait until the subagent finishes.

**On failure**, stop the entire workflow and report: which task failed, the Task document
path, the failure reason returned, and which tasks completed before the failure.

## 4g — Mark progress

**In the Task document:**

- Check off the automatic completion criteria that are satisfied.
- Do not claim manual checks are complete unless the Task document or the executor report
  explicitly says a human completed them.
- Mark implementation and automatic validation complete; record any manual validation that
  is still pending.

**In the parent document:**

- Add or update the link from the task entry to its Task document.
- Mark the entry as "automatic criteria done, manual verification pending", phrased to
  match the document's existing style.
- Do not mark the task fully done yet — that happens in 4h, after the user weighs in.

**Never move Task documents between directories.** Do not move, rename, or relocate a
Task document. Only the user moves them (for example from `documentation/Tasks/current/`
to `documentation/Tasks/done/`). You may only change file contents.

Record in your running orchestration summary: task identifier, Task document path,
technologies used, implementation status, review status, manual validation status.

## 4h — Approval gate: continue to the next task?

Report a brief summary of the completed task:

- Task identifier and title.
- Task document path.
- What was implemented, patched, or created.
- Review status (passed, findings patched, etc.).
- Whether any manual validation criteria remain pending.

Then ask whether to continue, using the `AskUserQuestion` tool (or your harness's
equivalent question tool):

```
header: "Continue to next task?"
options:
  - label: "Continue"
    description: "Proceed to the next task in the ordered list"
  - label: "Stop"
    description: "Stop the workflow here"
```

**If the user selects "Stop":**

1. Update the Memory Bank with the session state — completed tasks, their Task document
   paths, implementation status, pending manual validation.
2. Make sure the parent document reflects all completed progress.
3. Stop and report a final summary of completed and remaining tasks.

**If the user selects "Continue"**, do the manual completion criteria check below.

### Manual completion criteria check

Read the Task document and look for a manual criteria section — headings like `Manual
Validation`, `Manual Completion Criteria`, `Human Verification`, or similar.

**If manual criteria exist and are not marked complete** (no `[x]`, `COMPLETE`, or
equivalent), warn the user and ask with the question tool:

```
header: "Manual criteria not completed"
options:
  - label: "Complete manual revision"
    description: "I have completed the manual verification. Mark criteria as done and continue."
  - label: "Skip manual verification"
    description: "Go to the next task without completing the manual verification."
```

- **"Complete manual revision"** — mark the manual criteria complete in the Task document,
  mark the parent document's task entry fully done (automatic and manual satisfied), and
  proceed to the next task.
- **"Skip manual verification"** — leave the parent entry as "automatic criteria done,
  manual verification pending" and proceed to the next task without marking the manual
  criteria.
- **"Stop"** at any point — update the Memory Bank and the parent document, then stop and
  report the final summary.

**If there are no manual criteria, or they are already marked complete**, mark the parent
document's task entry fully done and proceed.

Then return to 4a for the next task in the ordered list.

---
name: bug-findings-solver
description: Resolve decision-style Bug Report findings interactively by analyzing each proposed solution with parallel read-only subagents, asking the user for a decision, and patching both the Bug Report and its parent Feature, Task, or documentation document. Use this skill whenever a Bug Report contains ordered findings from a document review, architecture review, feature review, task review, or similar analysis where the goal is to update the parent document rather than immediately fix code.
---

This skill governs the interactive Bug Report findings resolution workflow. The primary agent owns the workflow, user interaction, and document edits. Subagents are used only for read-only solution analysis.

# Input

The caller must provide:
- The **path** to the Bug Report document.
- The **path** to the parent document if known. The parent may be a Feature, Task, ADR, system doc, code explanation, or other documentation file.

If the parent path is not provided, infer it from the Bug Report by checking:
- Explicit `Parent`, `Reviewed Document`, `Feature`, `Task`, or `Source Document` fields.
- Obsidian links in the Summary, Findings, Affected Documentation, or Evidence sections.
- File names and titles that identify a reviewed Feature, Task, or document.

If multiple plausible parent documents exist and the correct one is ambiguous, ask one short clarification question before proceeding.

# Applies To

Use this skill for Bug Reports that contain review-style findings requiring decisions, especially reports produced by skills such as `feature-reviewer` or other document reviewers.

This skill is appropriate when:
- The Bug Report has findings sorted by severity or containing severity values.
- Each finding has a description, impact, possible solutions, and a recommended solution.
- The goal is to patch the parent document with the selected decisions.
- The Bug Report is not necessarily describing a runtime code defect.

Do not use this skill when:
- The user asks to implement the fix in code.
- The Bug Report only needs a task document created from its resolution steps.
- The Bug Report has no findings or decisions to process.

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and update documentation; preserve Bug, Feature, Task, ADR, and Doc structures. | **Refuse to continue.** |
| BLOCKER | `solid-deep-design` | Evaluate architectural trade-offs, module depth, seams, coupling, and overengineering risk. | **Refuse to continue.** |
| REQUIRED | `memory-bank` | Load project context from `documentation/Memory/` before evaluating solutions. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `glossary-management` | Use the project's ubiquitous language when explaining findings and patching documents. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `find-docs` | Retrieve up-to-date library, framework, API, or CLI documentation for technology-specific findings. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `doc-exploration` | Surface related ADRs, docs, features, tasks, bugs, and code explanations that constrain the decision. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Core Principles

## The Parent Document Is the Target

The objective is not to solve the bug in code. The objective is to decide what the parent document should say after reviewing the Bug Report's findings.

Patch code only if the user explicitly changes the task from decision resolution to implementation.

## Freshness Before Every Finding

Re-read the parent document before every finding. Earlier decisions may have changed the architecture, scope, user stories, implementation steps, task breakdown, or assumptions. A later finding may already be resolved or obsolete because of a previous decision.

Also re-read the Bug Report before every finding so decisions and status changes made earlier in the session are treated as the current source of truth.

## Primary Agent Owns the Decision

Subagents analyze options. They do not edit files, ask the user questions, or make final decisions. The primary agent synthesizes their reports, compares trade-offs, recommends the best option, asks the user, and applies the selected decision.

# Finding Format Expectations

Each finding should ideally include:
- Title or identifier.
- Severity: `critical`, `high`, `moderate`, or `low`.
- Description.
- Examples, user stories, scenarios, or code examples.
- Why it matters.
- Possible solutions.
- Recommended solution.
- Decision section, which may be empty.
- Status in a findings summary table, if present.

If the Bug Report lacks a Decision section or findings summary table, normalize it before processing by adding only the missing structure. Preserve the rest of the Bug Report template from `documentation-management`.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the mandatory skills and read all required project context:
- Memory Bank files.
- Documentation configuration and Bug Report structure from `documentation-management`.
- Glossary terms relevant to the Bug Report and parent document.
- Related docs through `doc-exploration`.
- ADRs and known architectural constraints.

## Step 2 — Read the Bug Report and Parent Document

Read the Bug Report in full. Extract:
- Findings and their order.
- Severity for each finding.
- Possible solutions and recommended solution for each finding.
- Current decision and status for each finding.
- Parent document references.

Read the parent document in full. Understand:
- The parent document type and required structure.
- Problem statement and user stories.
- Current architecture and design decisions.
- Affected systems, modules, and processes.
- Step breakdown, task breakdown, or implementation roadmap.
- Constraints inherited from ADRs, docs, and previous decisions.

Sort findings by severity if the Bug Report does not already impose an explicit order. Use this order: critical, high, moderate, low. Preserve the Bug Report's ordering inside the same severity level.

## Step 3 — Process Findings One by One

For each finding, execute Steps 3a through 3h before moving to the next finding.

### 3a — Re-read Current Documents

Re-read the Bug Report and parent document in full.

Skip the finding if it already has a recorded decision and a terminal status such as `Done`, `Dismissed`, `Accepted`, or `Resolved`, unless the user explicitly asked to revisit completed findings.

Determine whether the finding is still relevant against the current parent document.

If the finding is no longer relevant:
- Explain briefly which prior decision or parent-document change resolved it.
- Mark the finding as `Dismissed` or `Auto-resolved` in the Bug Report, depending on the table's status vocabulary.
- Record the reason in the finding's Decision section.
- Do not patch the parent document for this finding.
- Continue to the next finding.

### 3b — Prepare the Finding Brief

Create a concise internal brief for the finding that includes:
- Finding title, severity, and status.
- Description in plain language.
- Why it matters.
- User story or scenario impact.
- Code or architecture examples, using real file paths when available.
- Possible solutions listed in the Bug Report.
- Current recommended solution.
- Relevant parent-document sections.
- Constraints from ADRs, docs, Memory Bank, and glossary terms.

### 3c — Launch Parallel Solution Analysis Subagents

For each possible solution in the finding, launch one read-only `ask` mode subagent in parallel. If an explicit `ask` mode is unavailable, launch the most restrictive available research subagent and instruct it not to edit files.

Each solution subagent must:
- Load `memory-bank`, `documentation-management`, `solid-deep-design`, and `find-docs`.
- Use `glossary-management` and `doc-exploration` when relevant.
- Read the Bug Report and current parent document.
- Explore related documentation and codebase context.
- Validate technology-specific claims with up-to-date docs.
- Evaluate only its assigned solution.
- Return pros, cons, risks, implementation complexity, user impact, architecture impact, and whether it should be recommended.
- Not edit files.
- Not ask the user questions.

Use this prompt shape for each solution subagent:

```text
Analyze one possible solution for a Bug Report finding. Do not write or edit files.

Bug Report: [path]
Parent Document: [path]
Finding: [title / number / severity]
Assigned Solution: [solution text]

Load and apply: memory-bank, documentation-management, solid-deep-design, find-docs. Use glossary-management and doc-exploration when relevant.

Evaluate the assigned solution against:
- User story and end-user impact
- Architecture using SOLID and deep-module design
- Current parent document state
- Existing codebase and documentation constraints
- Implementation complexity and overengineering risk
- Compatibility with relevant library/framework/API documentation

Return:
1. One-sentence verdict
2. Pros
3. Cons
4. Risks and mitigations
5. Implementation complexity: low / medium / high
6. User impact: low / medium / high
7. Architecture impact: low / medium / high
8. Recommendation: recommend / do not recommend / recommend with changes
9. Suggested wording to patch into the parent document if selected
```

### 3d — Launch One Alternative-Solution Subagent

In parallel with the solution subagents, launch one additional read-only `ask` mode subagent to look for a better solution not listed in the Bug Report.

The alternative-solution subagent must:
- Know all current possible solutions and the current recommended solution.
- Search for a simpler, deeper, safer, or more user-aligned alternative.
- Avoid novelty for its own sake.
- Prefer a new solution only when it clearly improves the balance of user value, architecture, complexity, and project fit.
- Return the same fields as solution subagents.
- Include `Is this materially better than the current recommended solution? Yes/No` with reasoning.
- Not edit files.

### 3e — Synthesize the Recommendation

Wait for all subagent reports. Then compare every option using these criteria, in this order:
- Best outcome for the user stories and end users.
- Architectural fit using `solid-deep-design`: SRP, seams, dependency direction, module depth, locality, and testability.
- Compatibility with the current project state and existing documentation.
- Implementation complexity and risk.
- Avoidance of overengineering and unnecessary new abstractions.
- Long-term maintainability.

Confirm whether the Bug Report's original recommended solution is still the best choice.

If the alternative-solution subagent proposes a materially better option, include it as a first-class option and mark it as the recommended solution. If it is not better, mention it only if it adds useful context; do not distract the user with weak alternatives.

### 3f — Present the Finding and Options to the User

Present one finding at a time. Keep the explanation clear and bounded.

Include:
- Finding number/title and severity.
- The problem in plain language.
- Why it matters.
- One concrete user story or scenario.
- One concrete code or architecture example when available.
- A compact solution comparison table with pros, cons, complexity, and recommendation status.
- The recommended solution and why it is best.

Explain the recommendation in terms of:
- User-story value: what gets better for the user or future implementer.
- Architecture: why it fits SOLID and deep-module design.
- Practicality: why it fits the current project without overengineering.

Do not produce a long essay. The goal is enough context for a confident decision.

### 3g — Ask for the User's Decision

Use the `question` tool when available. Offer one option per viable solution and clearly mark the recommended option first.

Always include decision choices for:
- The recommended solution.
- Other viable listed solutions.
- The generated alternative, if it is viable enough to consider.
- Dismiss the finding.
- Defer or skip the finding for now.

Enable a custom response option so the user can ask a question, request clarification, or propose a different decision. If the question tool automatically adds a custom response option, do not add a duplicate `Other` choice.

If the user asks a question or requests clarification, answer it, then ask for the decision again. Do not patch documents until the user's decision is clear.

If the user proposes a custom solution, evaluate it against the same criteria. If needed, launch one read-only subagent to analyze the custom solution before recording it.

### 3h — Patch the Bug Report and Parent Document

After the user chooses, patch documents surgically.

Update the Bug Report:
- Write the chosen decision in the finding's Decision section.
- Include the option chosen, decision rationale, date, and whether the parent document was patched.
- Update the finding status in the findings summary table if present.
- Use `Done`, `Dismissed`, or `Deferred` according to the Bug Report's existing vocabulary.
- If the report lacks a summary table, do not invent an incompatible table unless normalization was already needed; a Decision section is sufficient.

Patch the parent document:
- Re-read it immediately before editing.
- Update only sections affected by the decision.
- Preserve the parent document's type-specific structure from `documentation-management`.
- For Feature documents, patch user stories, architecture, risks, implementation steps, and task breakdown as needed.
- For Task documents, patch parent context, implementation details, design decisions, validation, and completion criteria as needed.
- For ADRs, do not mutate accepted ADRs. If the decision changes an accepted ADR, recommend creating a superseding ADR through `documentation-management` instead.
- For Docs or Code explanations, patch the relevant explanation or process details without changing unrelated sections.
- If the user dismissed or deferred the finding, leave the parent document unchanged unless the user explicitly asked for a clarification note.

When patching, prefer small targeted edits over rewriting the whole document.

## Step 4 — Verify After Each Patch

After each finding's patches:
- Re-read the changed sections of the Bug Report and parent document.
- Confirm the Bug Report decision matches the parent document changes.
- Confirm no obvious contradiction was introduced.
- Note any later findings that may now be obsolete, but do not skip them until their turn.

## Step 5 — Final Report

After all findings have been processed or explicitly deferred, report:
- Bug Report path.
- Parent document path.
- Counts: decided, dismissed, deferred, auto-resolved.
- A concise table of decisions applied.
- Any findings still pending and why.

# Decision Quality Guidelines

Use these rules when comparing solutions:
- Prefer the solution that makes the parent document more executable and less ambiguous.
- Prefer deep modules over shallow pass-through abstractions.
- Prefer stable seams only where variation actually exists or testing requires a real adapter.
- Prefer preserving existing architecture when it is sound.
- Prefer simple local changes when they fully solve the user story.
- Avoid broad rewrites unless the finding shows the current approach cannot succeed.
- Treat implementation complexity as a cost, not a virtue.
- Treat user-facing correctness and maintainability as more important than elegance.

# User Presentation Template

Use this structure for each finding:

```markdown
## Finding [N]: [Title] ([Severity])

[One-paragraph explanation of the problem.]

Why it matters: [Short impact statement.]

User story impact: [Concrete scenario.]

Architecture/code example: [Concrete example or file path.]

| Option | Pros | Cons | Complexity | Recommendation |
|--------|------|------|------------|----------------|
| [Option A] | ... | ... | Low/Medium/High | Recommended |
| [Option B] | ... | ... | Low/Medium/High | Not recommended |

Recommended: [Option A]

Reason: [2-4 sentences connecting user value, SOLID/deep-module architecture, current project fit, and complexity.]
```

# Success Criteria

A successful outcome is:
- Findings are processed in severity order, unless the Bug Report explicitly defines a different order.
- Before every finding, the current parent document and Bug Report are re-read.
- Each possible solution is analyzed by a dedicated read-only subagent.
- One additional read-only subagent considers a new alternative solution.
- The user sees a clear comparison and chooses the decision.
- The Bug Report records every processed decision.
- The parent document reflects every accepted decision.
- Dismissed and deferred findings are recorded without unintended parent-document changes.
- No code is changed unless the user explicitly changes the scope to implementation.

# Output

Return to the caller:
1. A summary of findings processed, dismissed, deferred, and auto-resolved.
2. The updated Bug Report path.
3. The updated parent document path.
4. A table of decisions applied.
5. Any remaining pending findings and the reason they remain pending.

## Tasks

**Location:** `documentation/Tasks/[status]/[Task-Name].md`
**Lifecycle:** `current` → `done`

### What This Document Is

A Task document is a deeply detailed implementation plan. It is the actual document a developer or AI agent will execute to modify the codebase.

Use a Task to expand one implementation step, or a small grouped set of closely related steps, into actionable code-level work. It should contain the full detail needed to perform the work: the goal, parent context, selected skills, current documentation, affected files, implementation steps, design decisions, validation plan, and completion criteria.

Most Tasks come from a parent Feature or Bug. Read the parent document before creating the Task so the Task reflects the real goal, constraints, dependencies, and architectural intent behind the work. If a Task has no parent, make that explicit and include the missing context inside the Task itself.

When creating a Task, review the available skills and explicitly select the ones that apply. When Context7 is available, use it to gather up-to-date documentation for the relevant libraries, frameworks, APIs, or tools. If technology-specific skills exist for the stack, use them during task creation.

At the end of the Task, define clear completion criteria. Prefer automatic verification when possible. When manual testing is required, document the manual checks for the user and do not attempt to execute those manual tests on the user's behalf.

### Naming Convention
`[ParentName]-step-[N]-[short-description].md`

Standalone tasks with no parent can use:
`[Area]-task-[short-description].md`

If a task covers multiple closely related steps, use the first covered step number in the filename.

Examples:
- `Implement-Idempotency-step-2-1-IdempotencyManager.md`
- `OAuth2-Login-step-1-2-Configure-Dependencies.md`
- `Auth-task-session-cleanup.md`

### Required Tags
- `#task` — always present
- `#current` or `#done` — matches the directory
- Complexity: `#low-complexity` `#medium-complexity` `#high-complexity`
- Parent reference (kebab-case of parent, when a parent exists): `#parent-idempotency`, `#parent-oauth2-login`
- Standalone marker (only when there is no parent): `#standalone-task`

**Example:** `#task #current #high-complexity #parent-idempotency`

### Scope Rule

A task file documents ONLY the specific implementation step, or grouped set of closely related steps, that it addresses. It should not include implementation details for unrelated work — only the work needed to execute this task, plus brief forward/backward references for context.

### Template

```markdown
# Task: [Descriptive Name]

#task #current #medium-complexity #parent-[parent-name]
<!-- Use #standalone-task instead of #parent-[parent-name] only when there is no parent document -->

**Parent:** [[ParentBugOrFeatureName]] or [No parent]
**Parent Type:** [Feature | Bug | Standalone]
**Related Step(s):** [Phase 2, Step 2.1] or [Task group defined in parent]
**Estimated Complexity:** Medium

---

## Goal

[1-2 sentences: what this task accomplishes and why it's needed]

---

## Parent Context

[Summarize what the parent says about this task — the goal, constraints, dependencies, architectural decisions, and why this work exists. If there is no parent, explain that context directly here.]

---

## Preconditions / Dependencies

- [Prior task, boilerplate, config, or prerequisite that must already exist]
- [Constraint, assumption, or dependency to keep in mind]

---

## Skills and Documentation Preparation

### Skills Reviewed

- [Skill Name] — [Selected / Not needed] — [reason]
- [Skill Name] — [Selected / Not needed] — [reason]

### Documentation Reviewed

- Context7: [Library / framework / tool] — [what was reviewed and why]
- [Official doc / API reference / external source] — [what was reviewed and why]

### Related Existing Code

- [[RelatedFile-ext]] — [why it matters]
- `src/path/to/File.ext:line` — [relevant location]

---

## Implementation Details

### Approach

[Strategy, design pattern, component interactions, key decisions]

### Files to Create/Modify

- [ ] `src/path/to/File.ext` — [[File-ext]] — purpose in this task

---

## Step-by-Step Implementation

### Step 1: [Title]

**Goal:** [What this step accomplishes]
**Dependencies:** [What must already exist before this step, or None]

- [ ] [Concrete implementation action]
- [ ] [Concrete implementation action or verification]

**Why this step is critical:**
[Explanation of its role in the larger architecture]

#### Implementation

```[language]
// Code example with inline comments
```

#### Edge Cases
1. **Case:** [description] — [how it's handled]

---

## Design Decisions

**Decision 1:** [What was decided]
- **Why:** [Technical reasoning and trade-offs]
- **Alternatives considered:** [What else was evaluated and why it was rejected]

---

## Testing Considerations

### Automatic Validation

- [ ] [Automated test, lint, build, or verification command]
- [ ] [Another automated check]

### Manual Validation

- [ ] [Manual test for the user to perform]
- [ ] [Another manual check for the user if needed]

**Rule:** Run automatic checks when possible. If validation requires manual testing, document the steps here for the user and do not attempt to execute those manual tests yourself.

---

## Related Code Explanations

- [[RelatedFile-ext]] — [specific relationship]
- `src/path/to/File.ext:line` — [relevant detail]

---

## Completion Criteria

- [ ] Parent document reviewed and reflected accurately in this task
- [ ] Relevant skills reviewed and selected for this task
- [ ] Up-to-date documentation reviewed for the affected technologies
- [ ] All files created/modified as specified
- [ ] All implementation steps checked off
- [ ] Automatic validation passes
- [ ] Manual validation steps documented for the user when needed
- [ ] Code explanation files updated (if new files created)
- [ ] Parent bug/feature step marked complete, or standalone task status updated appropriately
```

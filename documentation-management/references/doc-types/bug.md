## Bugs

**Location:** `documentation/Bugs/[status]/[Bug-Name].md`
**Lifecycle:** `to-do` → `in-progress` → `done`

### What This Document Is

A Bug Report documents the technical analysis of a defect and the roadmap to fix it. It is not the final technical implementation plan.

Use a Bug Report to explain the issue, its impact, the analysis findings, the suspected or confirmed cause, and the evidence that supports that conclusion. It should point to the exact code files and lines involved, explain why those parts of the code are responsible, and include supporting logs when logs help justify the diagnosis. If the cause is not fully confirmed, state that clearly and explain the current hypothesis and uncertainty.

Bug Reports are usually the result of codebase analysis. They should capture the reasoning behind the diagnosis, not only the visible symptom. They should also record how the bug is reproduced or observed, what evidence was reviewed during the investigation, what remains uncertain, and how the proposed solution will be validated. Use the relevant technology skills and up-to-date documentation from Context7 when available.

Like Features, Bug Reports should include ordered non-blocking steps to resolve the issue and a final task breakdown that groups those steps by order and complexity. Bug Reports are created before task documents exist, so define the planned task names first and add task links later when the task files are created.

Use the template below when creating the document.

### Required Tags

Bug type (pick one): `#optimization` `#architectural` `#performance` `#security` `#reliability` `#usability`
Importance (pick one): `#low` `#medium` `#high` `#critical`

### Template

```markdown
#critical #reliability

## Bug: [Bug Title]

### Summary

[Detailed description of the bug and why it matters]

### Reproduction Conditions
1. [Step to reproduce or observe the issue]
2. [Next step]
3. [Observed failure]

### Environment / Preconditions (Optional)
- [Relevant environment, config, role, dataset, or runtime condition]

### Real-World Scenarios
[Concrete examples of when this bug manifests]

### Expected Behavior
[What should happen instead]

### Actual Behavior
[What is happening now]

### Impact
- [Impact item 1]
- [Impact item 2]

### Findings
- [Finding 1 discovered during analysis]
- [Finding 2 discovered during analysis]

### Investigation Scope
- **Code Reviewed:** `src/path/to/File.ext`, `src/path/to/OtherFile.ext`
- **Logs Reviewed:** [Yes / No] — [which logs or traces were checked]
- **Runtime Evidence:** [How the issue was reproduced, observed, or traced]

### Root Cause Analysis
[Explain the cause in detail. If the cause is not fully confirmed, state whether this is a strong hypothesis, partial hypothesis, or confirmed cause, and explain why.]

### Evidence in Code
- `src/path/to/File.ext:123` — [why this code is part of the cause]
- [[RelatedCodeExplanation-ext]] — [relevant technical explanation]

### Affected Systems / Modules
- [[System-Architecture-Doc]] — [how it is affected]
- [[Module-Explanation-File]] — [impact on this module]

### Affected Processes
- [[RelatedProcessDoc]] — [how it's affected]

---

## Supporting Logs (Optional)

```text
[Relevant log lines, stack traces, or runtime output]
```

### Log Analysis
[Explain how the logs support the diagnosis, or say clearly if the logs are inconclusive.]

### Confidence Level
[Confirmed | Strong hypothesis | Partial hypothesis]

[Explain what is known, what is inferred, and what still needs validation.]

### Remaining Uncertainty / Open Questions
- [Open question, ambiguity, or assumption]
- [What still needs confirmation]

---

## Solution Direction

### Proposed Fix
[High-level description of the solution and why it should resolve the issue]

### Why This Fix Is Correct
[Explain the technical reasoning behind the solution]

### Skills and Documentation Used During Analysis and Solution Validation
- [Skill Name] — [how it informed the proposed fix]
- Context7: [Library / framework / tool] — [what documentation was checked]
- [Official docs / external reference] — [what was validated]

### Files to Modify or Create
- `src/path/to/File.ext` — [what changes]

### Validation Strategy After Fix

#### Automatic Validation
- [ ] [Relevant test, lint, build, or verification command]

#### Manual Validation
- [ ] [Manual check the user should perform]

**Rule:** Prefer automatic validation when possible. If validation requires manual testing, document the manual steps here for the user and do not attempt to execute those manual checks on the user's behalf.

### Potential Risks / Notes
- [Risk, trade-off, or follow-up consideration]

---

## Resolution Steps

### Phase 1: [Phase Name]
- [ ] **Step 1.1:** [Description]
- [ ] **Step 1.2:** [Description]

### Phase 2: [Phase Name]
- [ ] **Step 2.1:** [Description]

---

## Task Breakdown

[Group the resolution steps above into ordered tasks. Use one task for a high-complexity step, or group a small set of closely related lower-complexity steps into a single task. At bug-report creation time, define the planned task names here even if the task files do not exist yet.]

### Task 1: [Task Name]
- **Steps Covered:** [Step 1.1]
- **Reason for Grouping:** [High complexity / dependency / standalone work]
- **Planned Task File:** `Bug-Name-step-1-1-short-description.md`
- **Task Document Link:** [Add when the task document is created]

### Task 2: [Task Name]
- **Steps Covered:** [Step 1.2, Step 2.1]
- **Reason for Grouping:** [These steps are closely related and can be executed together]
- **Planned Task File:** `Bug-Name-step-1-2-short-description.md`
- **Task Document Link:** [Add when the task document is created]

---

## Expected Outcome After Fix
- [Expected benefit 1]
- [Expected benefit 2]
```

### Link Requirements
- Link to `Code/` files with Obsidian wiki links: `[[FileName-ext]]`
- Link to `Docs/` files for affected processes: `[[ProcessName]]`
- Reference source code as plain text paths: `src/path/to/File.ext:123`

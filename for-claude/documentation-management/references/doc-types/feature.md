## Features

**Location:** `documentation/Features/[status]/[Feature-Name].md`
**Lifecycle:** `to-do` → `in-progress` → `done`

### What This Document Is

A Feature document defines the technical roadmap for a feature we want to build. We can consider a feature document a PRD. It is not the final technical implementation plan.

Use a Feature to describe what we want to build, the affected systems or modules, the intended architecture, the main risks, and the ordered non-blocking steps required to deliver it. A Feature can include technical reasoning, code explanations, examples, and high-level implementation ideas, but detailed execution belongs in Task documents.

The step breakdown is the most important part of the Feature. Order steps so implementation can move forward without blockers, placing foundational or boilerplate work before dependent work. At the end of the Feature, group the steps into tasks by order and complexity, because those tasks are the implementation plans that will actually be executed.

Features are created before task documents exist. When creating a Feature, define the task grouping and planned task names, but do not require task files or wiki links yet. Add the task document links later, when those task files are created.

Use the template below when creating the document.

### Required Tags

Feature type (pick one): `#new-feature` `#enhancement` `#integration` `#refactor`
Importance (pick one): `#low` `#medium` `#high` `#critical`

### Template

```markdown
#high #new-feature

## Feature: [Feature Name]

### Description
[Complete description of the feature and what it enables]

## Problem Statement

The problem that the user is facing, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Solution

The solution to the problem, from the user's perspective.

### Scope
[Which workflows, processes, or systems are impacted]

### Affected Systems / Modules
- [[System-Architecture-Doc]] — [how it's affected]
- [[Module-Explanation-File]] — [what changes]

### Impact Analysis
[How this affects existing functionality, performance, or behavior]

### Risk Assessment
[Possible side effects, breaking changes, or things to watch out for]

---

## Implementation Architecture

### Changes Required

#### 1. [Component/Module/File Name]
**Purpose:** [Why we're creating/modifying this]
**Changes:** [Detailed technical changes]
**Links:** [[Code-Explanation-File]]

---

## Implementation Steps

### Phase 1: [Phase Name]
- [ ] **Step 1.1:** [Technical task description]
- [ ] **Step 1.2:** [Technical task description]

---

## Potential Issues / Risks
- [Edge case or integration risk]

---

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

---

## Task Breakdown

[Group the implementation steps above into ordered tasks. Use one task for a high-complexity step, or group a small set of closely related lower-complexity steps into a single task. These tasks are the implementation plans that will actually be executed. At feature creation time, define the planned task names here even if the task files do not exist yet.]

### Task 1: [Task Name]
- **Steps Covered:** [Step 1.1]
- **Reason for Grouping:** [High complexity / dependency / standalone work]
- **Planned Task File:** `Feature-Name-step-1-1-short-description.md`
- **Task Document Link:** [Add when the task document is created]

### Task 2: [Task Name]
- **Steps Covered:** [Step 1.2, Step 1.3]
- **Reason for Grouping:** [These steps are low complexity and can be executed together]
- **Planned Task File:** `Feature-Name-step-1-2-short-description.md`
- **Task Document Link:** [Add when the task document is created]
```

### Link Requirements
- Link to `Code/` and `Docs/` files using wiki links
- Reference source files as plain text: `src/path/to/file.ext:42`
- Use full URLs for external API documentation

---
name: task-reviewer
description: Review an existing Task document for technical correctness, gaps, risks, and implementation issues. Load this skill when the primary agent routes to task review. Patches the Task document directly with recommended solutions — no separate Bug Report is created. The review is autonomous from most critical finding to lowest.
---

This skill governs the Task document review workflow. The primary agent loads this skill and executes every step directly. No Task delegation — the primary agent does everything itself.

Unlike `feature-reviewer`, this skill does **not** produce a Bug Report. Instead, it autonomously patches the Task document with the recommended solution for each finding, starting from the most critical and working down to the lowest severity.

# Input

The caller must provide:
- A **brief** describing what the Task document is trying to accomplish.
- The **path** to the Task document to review.

# Mandatory Skills

Before starting, load these skills. Each has a priority that determines what to do if it is unavailable.

| Priority | Skill | Purpose | If Unavailable |
|----------|-------|---------|----------------|
| BLOCKER | `documentation-management` | Find, read, and create docs; identify doc types and navigate the documentation system. | **Refuse to continue.** |
| BLOCKER | `memory-bank` | Load project context from `documentation/Memory/`. | **Refuse to continue.** |
| REQUIRED | `glossary-management` | Look up domain terms relevant to the Task's domain. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `find-docs` | Retrieve up-to-date library/framework documentation referenced in the Task. | **Tell the user** and ask if they want to continue. |
| REQUIRED | `solid-deep-design` | Evaluate the Task's architecture and implementation design for SOLID principles and deep-module design. | **Tell the user** and ask if they want to continue. |

Additionally, verify through `documentation-management` that the project has initialized its documentation system. If documentation is not initialized, inform the user and stop.

# Workflow

Follow these steps in order. Do not skip steps.

## Step 1 — Load Project Context

Load the `memory-bank` skill and read all Memory Bank files to understand:
- Project architecture and conventions
- Existing ADRs and design decisions
- Current system design and module structure

## Step 2 — Load Domain Language

Load the `glossary-management` skill and retrieve all relevant domain terms for the Task's domain. Understand the project's ubiquitous language so you can verify the Task document uses correct terminology and respects domain boundaries.

## Step 3 — Read and Analyze the Task Document and Its Parent

Read the Task document at the provided path in full. Understand:
- The **Goal**: what this task accomplishes and why
- The **Parent Context**: constraints, dependencies, and architectural decisions inherited from the parent
- The **Implementation Details**: approach, design patterns, files to create/modify
- The **Step-by-Step Implementation**: each concrete step, its goal, dependencies, code examples, and edge cases
- The **Design Decisions**: what was decided, why, and rejected alternatives
- The **Testing Considerations**: automatic and manual validation plans
- The **Completion Criteria**: how success is measured

**Then, check if the Task has a parent document.** Look at the `Parent:` field in the Task's frontmatter. If a parent document exists (Feature, Bug Report, or other), read that parent document in full to understand:
- The broader goal and motivation behind this task
- Any constraints, dependencies, or architectural decisions the parent imposes
- How this task fits into the larger body of work
- Any context the Task document may have omitted or misinterpreted

If the Task has no parent (`#standalone-task`), note this and proceed with the information available in the Task itself.

## Step 4 — Cross-Reference Documentation

Load the `doc-exploration` skill and execute its workflow using the Task's domain and context. Its report will surface:
- ADRs that may conflict with or constrain the Task's approach
- Existing Docs describing affected systems or processes
- Related Features or Bugs that overlap with this Task
- Code explanations for affected modules

## Step 5 — Explore the Codebase

Launch one or more `Explore` subagents to examine the actual code that the Task document references or would affect. Each subagent returns the content of files it finds. Iterate — launch additional Explore subagents until you have a solid understanding of:

- The current implementation of affected modules and systems
- How existing code aligns (or conflicts) with what the Task document proposes
- Code-level risks the Task document may have missed (tight coupling, hidden dependencies, missing abstractions)
- Whether the Task's planned changes are consistent with existing patterns and conventions
- File paths and function signatures the Task document may reference incorrectly
- Whether the Task's code examples are compatible with the actual codebase (APIs, types, patterns)

## Step 6 — Validate Technical Claims

Load `find-docs` and verify every library, framework, API, or tool claim made in the Task document. This is critical because Task documents contain concrete code examples that will be executed. Check that:
- APIs referenced actually exist and work as described
- Version compatibility is considered
- Code snippets use correct syntax, method signatures, and imports
- Configuration examples are valid
- Performance claims are reasonable
- Security patterns follow best practices
- Deprecated APIs are not recommended

## Step 7 — Evaluate Architecture

Load `solid-deep-design` and evaluate the Task's implementation design for:
- SOLID principle violations
- Module depth and interface design quality
- Coupling and cohesion concerns
- Abstraction quality
- Testability and maintainability
- Whether the design decisions are sound given the constraints
- Whether edge cases are adequately covered

## Step 8 — Identify Findings

Based on all analysis, identify every issue, gap, risk, or problem in the Task document. For each finding, determine:

- **Severity**: `critical`, `high`, `moderate`, or `low`
- **Description**: What the problem is, clearly stated
- **Why It Matters**: The impact if left unresolved
- **Possible Solutions**: A list of viable approaches to address the finding
- **Recommended Solution**: The best solution with reasoning for why it is superior

Severity guidelines for Task documents:
- **Critical**: The task cannot be executed as described; fundamental flaw in the implementation approach, uses APIs that don't exist, or contradicts the parent document's requirements
- **High**: Major gap that will cause the implementation to fail, produce incorrect behavior, or require significant rework
- **Moderate**: Design concern that could cause subtle bugs, missing edge case, or suboptimal approach
- **Low**: Minor improvements, style inconsistencies, documentation clarity issues, or nice-to-have refinements

## Step 9 — Apply Solutions (Patch the Task Document)

This step replaces the Bug Report creation from `feature-reviewer`. Instead of producing a separate document, you autonomously fix the Task document itself.

**Patching Rules:**

1. **Order**: Start from the most critical finding and work down to the lowest severity.
2. **Method**: Directly edit the Task document using the `Edit` tool. Insert corrections, additions, or modifications in the appropriate section of the document.
3. **Scope**: Only fix what is wrong or missing. Do not rewrite the entire document. Be surgical.
4. **Documentation**: For each patch applied, add a brief inline note at the point of the fix indicating what was corrected, using the format: `<!-- REVIEW-FIX: [brief description of what was fixed] -->`. This is optional and only when it helps future readers understand why content was changed.
5. **Preserve Intent**: Do not change the Task's goal or scope. Only fix technical correctness, completeness, and structural quality issues.
6. **Avoid Duplication**: If two findings are addressed by the same patch, apply it once and note that it resolves both.

**What Patches Look Like (per section of the Task document):**

| Section | Typical Patches |
|---------|----------------|
| **Goal** | Clarify scope if it contradicts parent document |
| **Parent Context** | Correct misinterpretations of parent requirements |
| **Preconditions / Dependencies** | Add missing dependencies, correct wrong assumptions |
| **Skills and Documentation Preparation** | Add missing skills, correct documentation references |
| **Implementation Details (Approach)** | Correct design pattern, fix architectural flaws |
| **Implementation Details (Files)** | Fix incorrect file paths, add missing files |
| **Step-by-Step Implementation** | Fix incorrect code examples, add missing edge cases, correct API usage, adjust step order for dependencies |
| **Design Decisions** | Correct flawed reasoning, add alternatives that should be documented |
| **Testing Considerations** | Add missing test cases, fix incorrect validation commands |
| **Completion Criteria** | Add missing criteria, fix incorrect criteria |

## Step 10 — Verify Consistency

After all patches are applied, re-read the Task document once more to verify:
- The document is internally consistent (no contradictions between sections)
- All patches were applied correctly and don't introduce new errors
- The Task still aligns with its parent document and the broader codebase
- Cross-references (file paths, wiki links, skill names) are correct

# Success Criteria

A successful outcome is a Task document that:
- Has been thoroughly analyzed for technical correctness, completeness, and architectural soundness
- Has all findings patched directly into the document — starting from the most critical to the lowest severity
- Every finding has its recommended solution applied as concrete edits to the relevant section(s)
- The Task can now be executed by a developer or agent with confidence that it is technically correct and complete
- The Task still faithfully implements the intent of its parent document (if one exists)

# Output

Return to the caller:
1. **Confirmation** that the Task document has been reviewed and all findings have been patched.
2. **Summary table** of all findings that were patched, ordered by severity (highest first):

| # | Finding | Severity | Solution Applied |
|---|---------|----------|------------------|
| 1 | [Finding name / brief description] | 🔴 Critical / 🟠 High / 🟡 Moderate / 🟢 Low | [Brief description of what was changed in the document] |
| 2 | ... | ... | ... |

3. **Counts by severity**: Number of critical, high, moderate, and low findings patched.

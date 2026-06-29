## Architecture Decision Records (ADRs)

**Location:** `documentation/ADRs/ADR-[NNN]-[short-title].md`
**Index File:** `documentation/ADRs/ADR-index.md` (mandatory)
**Lifecycle:** ADRs are standalone decisions with status tracking — they do not move between directories.

### What This Document Is

An Architecture Decision Record (ADR) captures a significant architectural decision made during the project, along with its context and consequences. ADRs follow the format defined by Michael Nygard.

ADRs serve as a historical record of why the system is the way it is. They document decisions that affect the structure, non-functional characteristics, dependencies, interfaces, or construction techniques of the system. An ADR is not a general design doc — it captures a single, specific, concrete decision and the forces that shaped it.

Each ADR should be self-contained and understandable on its own. ADRs are immutable once accepted: if a decision changes, create a new ADR that supersedes the old one and update the index.

### When to Write an ADR

Write an ADR when a decision:
- Affects the architecture of the system (structure, non-functional characteristics, dependencies, interfaces, or construction techniques)
- Involves a meaningful trade-off
- Is likely to be questioned or referenced later
- Has been discussed and requires a record of the rationale

Do not write an ADR for:
- Routine implementation choices that have no architectural impact
- Decisions that are obvious and uncontroversial
- Decisions that will be captured adequately in other documentation

### ADR Index File

The `documentation/ADRs/ADR-index.md` file is **mandatory**. It serves as the master index of all Architecture Decision Records in the project. Every time an ADR is created, superseded, or changes status, the index **must** be updated.

The index file contains a markdown table listing every ADR with:

| Field | Description |
|-------|-------------|
| **ADR** | The ADR number without leading zeros: `ADR 1`, `ADR 2`, etc. |
| **Title** | The full title of the decision |
| **Status** | Current status: `Proposed`, `Accepted`, `Deprecated`, or `Superseded` |
| **Date** | ISO date when the ADR was created (YYYY-MM-DD) |
| **Superseded By** | If the ADR is `Superseded`, the ADR number that replaces it |

The index file uses this exact template:

```markdown
# ADR Index

## Status Legend
- **Proposed:** The decision is under consideration
- **Accepted:** The decision has been agreed upon and is in effect
- **Deprecated:** The decision is no longer relevant (the thing it was about no longer exists)
- **Superseded:** The decision has been replaced by a newer ADR

| ADR | Title | Status | Date | Superseded By |
|-----|-------|--------|------|---------------|
| ADR 1 | [Title of first ADR] | Accepted | YYYY-MM-DD | — |
```

### Naming Convention

ADR filenames follow a strict format: `ADR-[NNN]-[short-title].md`

- `NNN` is a 3-digit, zero-padded sequential number (e.g., `001`, `002`, `010`)
- `short-title` is a kebab-case version of the decision title
- The title in the file should match: `ADR NNN: [Full Decision Title]`

Examples:
- `ADR-001-use-postgresql-as-primary-database.md`
- `ADR-002-adopt-event-driven-architecture.md`
- `ADR-003-use-oauth2-for-authentication.md`

### Required Tags

- `#adr` — always present
- Status tag: `#adr-proposed` `#adr-accepted` `#adr-deprecated` `#adr-superseded`
- Domain tag (pick one or more): `#data` `#infrastructure` `#frontend` `#backend` `#security` `#api-design` `#testing` `#devops` `#architecture`

### Template

Every ADR MUST contain exactly these five sections in this order: **Title**, **Status**, **Context**, **Decision**, **Consequences**.

```markdown
#adr #adr-accepted #data

## ADR NNN: [Short Noun Phrase — the decision]

### Status
[Proposed | Accepted | Deprecated | Superseded]

[If Superseded, include: Superseded by [ADR NNN](ADR-NNN-short-title.md)]

### Context

[Describe the forces at play, including technological, political, social, and project-local. These forces are probably in tension, and should be stated in value-neutral language — just the facts. The context should make it clear why the decision was needed and what constraints shaped the options.]

### Decision

[State the decision in full sentences, with active voice: "We will..." If there were alternatives considered, describe them briefly and explain why they were rejected.]

### Consequences

[Describe the resulting context, after applying the decision. All consequences should be listed, not just the "positive" ones. A particular decision may have positive, negative, and neutral consequences, but all of them affect the team and project in the future.]

- [Consequence 1: what becomes easier or more difficult]
- [Consequence 2: what becomes easier or more difficult]
```

### Agent Workflow: Creating a New ADR

When the user requests creating a new ADR, follow this procedure:

1. **Determine the next ADR number:**
   - Read `documentation/ADRs/ADR-index.md`
   - Find the highest existing ADR number in the index table
   - The new ADR number is the highest existing number + 1
   - If no ADRs exist yet, start at `001`

2. **Create the ADR file:**
   - Format the filename as `ADR-[NNN]-[kebab-case-title].md`
   - Fill in the template with the user's decision
   - Create the file at `documentation/ADRs/ADR-[NNN]-[kebab-case-title].md`

3. **Update the ADR index (mandatory):**
   - Read `documentation/ADRs/ADR-index.md`
   - Append a new row to the index table:
     ```
     | ADR NNN | [Title] | Accepted | YYYY-MM-DD | — |
     ```
   - If the index file does not exist yet, create it using the index template above

4. **When superseding an existing ADR:**
   - Update the superseded ADR's Status to `Superseded` and add the Superseded by link
   - Update the superseded ADR's tags from `#adr-accepted` to `#adr-superseded`
   - Update the ADR index row for the superseded ADR: change its Status to `Superseded` and set the `Superseded By` column to the new ADR number
   - Create the new superseding ADR normally

### Agent Workflow: Updating ADR Status

When an ADR status changes (e.g., from Proposed to Accepted):

1. Update the Status field and Status line in the ADR file
2. Update the status tag (e.g., `#adr-proposed` → `#adr-accepted`)
3. Update the ADR index row for that ADR

### Link Requirements
- Link to related system docs or code explanations with wiki links: `[[SystemDoc]]`
- Reference source code as plain text: `src/path/to/file.ext:42`
- Link to other ADRs in the Superseded by field: `[ADR NNN](ADR-NNN-short-title.md)`

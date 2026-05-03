# Command Workflows

Detailed step-by-step procedures for every documentation-management command.

---

## Read & Search Commands

### `list bugs [status?]`
**Example:** `list bugs`, `list in-progress bugs`, `list bugs to-do`
1. Read `doc-config.json` to find the bugs directory (default: `Bugs/`)
2. If a status is given, list files in that subdirectory only
3. If no status given, list all bugs grouped by status subdirectory
4. For each file, show: filename, first tag line (importance/type), and a one-line summary from the file title
5. Prefer CLI: `obsidian search query="tag:#bug" silent` — fall back to `ls documentation/Bugs/` if unavailable

---

### `list features [status?]`
Same pattern as `list bugs`, using the `Features/` directory.

---

### `list tasks [status?]`
Same pattern as `list bugs`, using the `Tasks/` directory (statuses: `current`, `done`).

---

### `search docs [query]`
**Example:** `search docs authentication`, `search docs upload idempotency`

1. Use Obsidian CLI first: `obsidian search query="[query]" limit=20 silent`
2. Fallback: use `grep -r "[query]" documentation/ --include="*.md" -l`
3. Present results grouped by doc type (Bugs, Features, Tasks, Docs, Code, ADRs)
4. For each result, show the file path and the matching excerpt

---

### `show doc [file]`
**Example:** `show doc Bugs/in-progress/Idempotency.md`

1. Resolve the file path relative to `documentation/`
2. Read the file using the CLI: `obsidian read file="[name]" silent` or direct file read
3. Summarize the contents: purpose, current status, key links, open checkboxes

---

### `find related [topic]`
**Example:** `find related authentication`, `find related PluginService`

1. Search for the topic across all documentation directories
2. Also search for wiki links pointing to any file whose name matches the topic
3. Group results: direct mentions, linked files, code explanations
4. Show a brief relationship summary for each result

---

### `list adrs`
**Example:** `list adrs`

1. Read `documentation/ADRs/ADR-index.md`
2. Parse the index table
3. Display all ADRs grouped by status, showing: number, title, status, date
4. If the index file does not exist, report that no ADRs have been created yet

---

### `show adr [number]`
**Example:** `show adr 3`, `show adr 001`

1. Normalize the number to a 3-digit zero-padded format
2. Look up the ADR in `documentation/ADRs/ADR-index.md` to find the filename
3. Read the ADR file from `documentation/ADRs/ADR-[NNN]-[title].md`
4. Summarize: the decision, current status, context, and key consequences
5. If superseded, show which ADR supersedes it

---

## Create Commands

### `create bug [name]`
**Example:** `create bug Race condition in file upload`

1. Read the bug template from `references/doc-types.md`
2. Convert the name to a kebab-case filename: `Race-condition-in-file-upload.md`
3. Ask the user for: severity tag, a brief description, and any known affected files
4. Fill in the template with what's provided — leave placeholder text for unknown sections
5. Create at `documentation/Bugs/to-do/[name].md`
   - CLI: `obsidian create name="[name]" content="[content]" silent`
   - Fallback: write the file directly
6. Confirm creation and show the file path

---

### `create feature [name]`
**Example:** `create feature OAuth2 login integration`

1. Read the feature template from `references/doc-types.md`
2. Convert to kebab-case filename
3. Ask the user for: importance tag, feature type tag, overview, and affected systems
4. Create at `documentation/Features/to-do/[name].md`
5. Confirm creation

---

### `create task [name] for [parent]`
**Example:** `create task Implement JWT token validation for OAuth2-login-integration`

1. Read the task template from `references/doc-types.md`
2. Resolve the parent bug or feature file path
3. Ask which step in the parent this task covers (e.g., "Phase 2, Step 2.1")
4. Generate filename using the naming convention: `[ParentName]-step-[N]-[short-description].md`
5. Fill in the template: parent link, related step, goal, context from parent
6. Create at `documentation/Tasks/current/[filename].md`
7. **Update the parent file:** add a task link in the relevant step:
   ```markdown
   - [ ] **→ See Task:** [[TaskFileName]]
   ```
   Ask user to confirm before updating the parent

---

### `create doc [name]`
**Example:** `create doc File Upload Process`

1. Read the system-doc template from `references/doc-types.md`
2. Ask the user: what system/workflow does this document describe? Who are the key participants?
3. Create at `documentation/Docs/[name].md` with the template scaffold
4. Confirm creation

---

### `create code explanation [file]`
**Example:** `create code explanation src/services/AuthService.ts`

1. Check if an explanation already exists in `documentation/Code/` for this file
   - Naming convention: replace `.` with `-` → `AuthService-ts.md`
2. If it exists, treat as `update code explanation` instead
3. If it doesn't exist:
    a. Read the source file
    b. Read the code explanation template from `references/doc-types.md`
    c. Generate the explanation: purpose, component info, fields, methods, relationships
    d. Create at `documentation/Code/[converted-name].md`
4. Ask: "Would you like me to check for any other files that should link to this one?"

---

### `create adr [title]`
**Example:** `create adr Use PostgreSQL as primary database`

1. Read the ADR template from `references/doc-types/adr.md`
2. **Determine the next ADR number:**
   a. Read `documentation/ADRs/ADR-index.md`
   b. Find the highest existing ADR number in the index table
   c. The new ADR number = highest existing + 1 (start at `001` if none exist)
3. Convert the title to kebab-case for the filename
4. Ask the user for: domain tags and whether the status is Proposed or Accepted
5. Fill in the template with the user's decision, context, and consequences
6. Create the file at `documentation/ADRs/ADR-[NNN]-[kebab-title].md`
7. **Update ADR-index.md (mandatory):**
   a. If the index file does not exist, create it using the index template from `references/doc-types/adr.md`
   b. Append a new row to the index table:
      ```
      | ADR NNN | [Title] | Accepted | YYYY-MM-DD | — |
      ```
8. Confirm creation and show the file path

---

## Update Commands

### `update doc [file]`
**Example:** `update doc documentation/Docs/File-Upload-Process.md`

1. Read the specified doc file
2. Identify all source code references in the file (paths like `src/...`)
3. Read each referenced source file to check for changes
4. Compare what the doc says against what the code actually does
5. List the differences found: "The doc says X, but the code now does Y"
6. Ask: "Would you like me to update these sections?" — then apply changes if confirmed
7. Also check: are any wiki links pointing to files that no longer exist? Flag broken links.

---

### `update code explanation [file]`
**Example:** `update code explanation src/services/AuthService.ts`

1. Derive the explanation filename (dot-to-dash convention)
2. If the explanation doesn't exist, redirect to `create code explanation`
3. If it exists:
   a. Read the explanation file
   b. Read the current source file
   c. Compare: new methods/fields, removed methods/fields, changed signatures, changed logic
   d. List specific changes needed
   e. Ask for confirmation, then apply updates
4. After updating, check if any other docs reference this file and suggest updating them too

---

## Status Management Commands

### `set bug [file] as "[status]"`
**Example:** `set bug documentation/Bugs/in-progress/Idempotency.md as "done"`

Valid statuses: `to-do`, `in-progress`, `done`

1. Resolve the full file path
2. Determine the target directory based on the new status
3. Move the file: `mv documentation/Bugs/[old-status]/[name].md documentation/Bugs/[new-status]/[name].md`
4. Update any wiki links in other files that point to the old path (Obsidian handles this if CLI is used, but verify)
5. **If moving to `done`:**
   - Ask: "Would you like me to update related documentation files?"
   - If yes: check all linked `Code/` and `Docs/` files, read their source code, update as needed
   - Check all related `Tasks/` files and confirm they are also marked done

---

### `set feature [file] as "[status]"`
Same workflow as `set bug`, using `Features/` directory.

---

### `set task [file] as "[status]"`
**Example:** `set task documentation/Tasks/current/Idempotency-step-2-1.md as "done"`

Valid statuses: `current`, `done`

1. Move the file to the target directory
2. **If moving to `done`:**
   - Read the task's `**Parent:**` link
   - Update the parent bug/feature: mark the related step checkbox as `[x]`
   - Ask: "Would you like me to update related code explanation files?"
   - If yes, update `Code/` files for any source files created or modified in this task

---

### `set adr [number] as "[status]"`
**Example:** `set adr 3 as "accepted"`, `set adr 1 as "deprecated"`

Valid statuses: `proposed`, `accepted`, `deprecated`, `superseded`

1. Normalize the ADR number to 3-digit zero-padded format
2. Look up the ADR filename from `documentation/ADRs/ADR-index.md`
3. Read the ADR file
4. Update the `### Status` section to the new status
5. Update the status tag (e.g., `#adr-proposed` → `#adr-accepted`)
6. **Update ADR-index.md:** change the Status column in the index table row for that ADR
7. **If setting to `superseded`:**
   - Also prompt the user: "Which ADR supersedes this one?"
   - Add the Superseded by line to the ADR file
   - Update the Superseded By column in the index

---

### `supersede adr [number] with [title]`
**Example:** `supersede adr 2 with Switch to MongoDB for document storage`

This is a convenience command that combines creating a new ADR and marking the old one as superseded.

1. Follow the `create adr` workflow to create the new ADR
2. After creation, follow the `set adr [number] as "superseded"` workflow for the old ADR:
   a. Update the old ADR's Status to `Superseded` with a link to the new ADR
   b. Update the old ADR's status tag
   c. Update the index: old ADR gets `Superseded` status and the new ADR number in Superseded By
3. Confirm both updates

---

## Linking Commands

### `link task [task] to [parent]`
**Example:** `link task Idempotency-step-2-1 to Idempotency`

1. Resolve both file paths
2. Find the relevant step in the parent file (ask the user which step if ambiguous)
3. Add the task link under that step in the parent:
   ```markdown
   - [ ] **→ See Task:** [[TaskFileName]]
   ```
4. Ensure the task file has the correct `**Parent:**` and `**Related Step:**` fields
5. Confirm both updates before applying

---

## Init Commands

### `init documentation`

Use this to set up a fresh documentation structure for a new project.

1. Ask the user: project name (for `vault_name` in config), and whether to use the default directory structure or a custom one
2. Create the directory tree:
   ```
   documentation/
   ├── doc-config.json
   ├── Bugs/
   │   ├── to-do/
   │   ├── in-progress/
   │   └── done/
    ├── Features/
    │   ├── to-do/
    │   ├── in-progress/
    │   └── done/
    ├── Tasks/
    │   ├── current/
    │   └── done/
    ├── Docs/
    ├── Code/
    ├── ADRs/
    │   └── ADR-index.md
    ├── Memory/
    └── rules/
   ```
3. Create `documentation/doc-config.json` with the project's values
4. Create `documentation/ADRs/ADR-index.md` using the index template (even if empty — the table header must exist)
5. Ask: "Would you like me to also initialize the Memory Bank? (requires filling in `documentation/Memory/brief.md` first)"
6. Ask: "Would you like me to create a README or overview doc in `Docs/` to describe this project?"
7. Confirm all created paths to the user

# Obsidian CLI Reference

Use the `obsidian` CLI to interact with a running Obsidian instance. Obsidian must be open for the CLI to work. Always run `obsidian help` first to confirm availability — if it fails, fall back to direct file operations.

## General Syntax

**Parameters** take a value with `=`. Quote values that contain spaces:
```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:
```bash
obsidian create name="My Note" silent overwrite
```

For multiline content, use `\n` for newline and `\t` for tab.

## Key Flags (apply to most commands)

| Flag | Effect |
|------|--------|
| `silent` | Prevents the file from opening in Obsidian — always use this to avoid disrupting the user |
| `overwrite` | Overwrites an existing file instead of erroring |
| `--copy` | Copies output to clipboard instead of printing |
| `total` | Appends a count to list command output |

## File Targeting

Many commands accept `file` or `path` to target a note. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed): `file="AuthService"`
- `path=<path>` — exact path from vault root: `path="Code/AuthService-ts.md"`

## Vault Targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault (use the `vault_name` value from `doc-config.json` when set):

```bash
obsidian vault="my-project" read file="AuthService"
```

---

## Common Commands

### Reading

```bash
# Read a note's content
obsidian read file="My Note"
obsidian read path="Bugs/in-progress/Race-condition.md"

# Read the daily note
obsidian daily:read
```

### Creating

```bash
# Create a new note
obsidian create name="New Note" content="# Title\nContent here" silent

# Create from a template
obsidian create name="New Bug" template="Bug Template" silent

# Create (or overwrite) a note
obsidian create name="Existing Note" content="New content" silent overwrite
```

### Appending

```bash
# Append content to a note
obsidian append file="My Note" content="New line added" silent

# Append to the daily note
obsidian daily:append content="- [ ] New task" silent
```

### Searching

```bash
# Full-text search
obsidian search query="authentication token" limit=10

# Search by tag
obsidian search query="tag:#bug" limit=20

# Search by tag and keyword
obsidian search query="tag:#in-progress authentication" limit=10
```

### Properties (Frontmatter / Metadata)

```bash
# Set a property on a note
obsidian property:set name="status" value="done" file="My Note" silent

# Get a property
obsidian property:get name="status" file="My Note"
```

### Backlinks

```bash
# Find all notes that link to a given note
obsidian backlinks file="AuthService-ts"
```

### Tags

```bash
# List all tags, sorted by frequency
obsidian tags sort=count counts
```

### Tasks

```bash
# List today's tasks
obsidian tasks daily todo

# List all incomplete tasks
obsidian tasks todo
```

---

## Documentation Management Patterns

These are the most common CLI patterns used by this skill:

```bash
# Create a new bug doc
obsidian create name="Race-condition-in-file-upload" \
  content="#critical #reliability\n\n### 🔴 CRITICAL: Race Condition in File Upload\n\n## Problem Explanation\n\n..." \
  silent

# Move a file by creating at new path and deleting old (Obsidian CLI may not have mv)
# Preferred: use the shell mv command on the vault files directly
mv documentation/Bugs/to-do/Bug-Name.md documentation/Bugs/in-progress/Bug-Name.md

# Search for all in-progress bugs
obsidian search query="tag:#bug tag:#in-progress" silent

# Append a task link to a bug step
obsidian append file="Bug-Name" \
  content="  - [ ] **→ See Task:** [[Bug-Name-step-2-1-description]]" \
  silent

# Find all notes that reference a code file
obsidian backlinks file="AuthService-ts"

# Update a property after moving to done
obsidian property:set name="status" value="done" file="Bug-Name" silent
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| `obsidian help` fails | Obsidian is not open or CLI not installed. Fall back to direct file operations silently. |
| `obsidian create` fails with "already exists" | Add the `overwrite` flag, or use `obsidian append` instead |
| Command returns empty results | Normal — the vault may not have matching content |
| Vault not found | Check `vault_name` in `doc-config.json`; try omitting `vault=` to use the active vault |

---

## Full Command Reference

Run `obsidian help` at any time to see the current, authoritative list of all available commands. The CLI evolves — when in doubt, check `obsidian help` rather than relying solely on this reference.

Full official documentation: https://help.obsidian.md/cli

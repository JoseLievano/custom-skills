---
name: glossary-management
description: Manages a ubiquitous language glossary inside the documentation/Glossary/ directory. Use this skill whenever the user wants to add, update, delete, or search terms in the project glossary, or when working with domain-specific language, shared terminology, or ubiquitous language definitions. Also use when the user asks what a term means in the context of this project.
---

# Glossary Management

Manages the project's ubiquitous language glossary — a shared dictionary of terms used by developers and AI agents to communicate clearly and consistently.

All glossary operations go through the CLI tool `glossary`. Never read or write glossary files directly, always use the CLI program "glossary".

## Setup

At the start of any glossary task, run from the **project root**:

```bash
glossary categories
```

If this returns exit code 1 with a `.glossaryrc not found` message, run init first:

```bash
glossary init \
  --json-path <abs-path-to-glossary.json> \
  --markdown-path <abs-path-to-Glossary.md>
```

Derive the paths from the `documentation-management` skill config, or ask the user. Paths must be absolute.

## Commands

### Look up a term
```bash
glossary search "<TermName>"
```
Returns full term JSON (including category) on stdout. Exit 1 + stderr message if not found.

### Add a term
Before calling add:
1. Use the memory bank (if available) to understand project context.
2. Suggest a definition and examples grounded in the project domain.
3. Confirm definition, examples, synonyms, and related terms with the user.
4. Decide which category the term belongs in.

```bash
glossary add \
  --term "<name>" \
  --category "<Category>" \
  --definition "<text>" \
  --examples "<text>" \
  --synonyms "<comma-separated or empty>" \
  --related "<comma-separated or empty>"
```

On exit 2: term already exists. Show the user the existing term (from stdout JSON) and ask whether to update it.

### Update a term (partial patch)
Only pass flags for fields that should change. Unspecified fields are preserved.

```bash
glossary update \
  --term "<name>" \
  [--category "<NewCategory>"] \
  [--definition "<text>"] \
  [--examples "<text>"] \
  [--synonyms "<text>"] \
  [--related "<text>"]
```

If changing `--category`: explain the reasoning to the user and get confirmation before running the command.

At least one optional flag must be provided — `update --term X` with no other flags returns an error.

### Delete a term
Before calling delete:
1. Run `search` to get the full term data.
2. Show it to the user and ask for explicit confirmation.

```bash
glossary delete --term "<name>"
```

### List terms in a category
```bash
glossary list --category "<Category>"
```

### List all terms
```bash
glossary list-all
```

### List all categories
```bash
glossary categories
```

### Regenerate Markdown
Only needed if Glossary.md is out of sync (write commands do this automatically):
```bash
glossary render
```

### Get help
```bash
glossary --help
glossary <command> --help
```

## Core Rules

- **Never modify glossary files directly.** All reads and writes go through the CLI.
- **Confirm before every write.** Before add/update/delete, show the user what will change and ask for confirmation.
- **Project context first.** When adding or updating terms, use memory bank context to ground definitions and examples in the actual project.
- **Agent-owned category decisions.** The agent picks the category for new terms. Create a new category if none of the existing ones fit.
- **Synonyms instead of duplicates.** If a near-duplicate term exists, prefer adding an alias to the `synonyms` field of the canonical term rather than creating a separate entry.

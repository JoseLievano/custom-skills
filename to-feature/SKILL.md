---
name: to-feature
description: Turn the current conversation context into a Feature document and publish it to the project documentation system. Use when the user wants to create a Feature from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a Feature document using the documentation-management skill. Do NOT interview the user — just synthesize what you already know.

The documentation-management skill must be loaded before this skill is used — it defines the Feature template, file location, tagging conventions, and status lifecycle. This skill defers all document structure authority to documentation-management.

## Process

1. Load the documentation-management skill and confirm `documentation/` exists at the project root. Read `documentation/doc-config.json` to determine the Features directory and status vocabulary.

2. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the Feature, and respect any ADRs in the area you're touching.

3. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

4. Write the Feature document following the template defined by "documentation managment" skill (the Features section). Place it in the correct status directory (`Features/to-do/` by default) with the naming convention `[Feature-Name].md`. Apply the required tags from the template.

5. Validate the document against the documentation-management conventions:
   - Required tags are present
   - Wiki links use `[[FileName]]` or `[[Folder/FileName|Display Text]]` format
   - Source code references use plain text paths from project root (e.g., `src/components/Auth.tsx:42`)
   - Internal links reference existing docs where applicable
   - The status directory matches the document's lifecycle stage

## Core Rules

- **Document structure authority belongs to documentation-management skill.** Never invent your own template or deviate from what `documentation managment skill` defines for Features. If a section from a different template (like a PRD) seems useful but is not in the Feature template, do not add it.
- **Never move files without an explicit request.** Status changes follow the documentation-management lifecycle.

## Code Explanations

**Location:** `documentation/Code/[FileName-ext].md`

### Naming Convention
Replace dots in the filename with dashes:
- `AuthService.ts` → `AuthService-ts.md`
- `user_model.py` → `user_model-py.md`
- `application.properties` → `application-properties.md`

### Required Tags

Architectural role (pick one): `#entry-point` `#logic` `#persistence` `#data-access` `#interface` `#transport` `#utility` `#config`

Technical context (pick applicable): `#async` `#ui` `#security` `#integration`

### Template

```markdown
# [FileName].[ext]

#logic #security

## Purpose
[High-level summary of what this component does and its role in the system]

---

## Component Information

**Type:** [Class | Module | Function Collection | Interface | Configuration | Script]
**Namespace/Path:** [Full directory path or package]
**Dependencies:** [Key external libraries or internal modules]

---

## Data Structures & State

### [fieldName]
**Type:** [Data type]
**Purpose:** [What this represents]
**Attributes:** [e.g., private, readonly, @Validated]

---

## Logic & Interface

### [methodName()]
**Purpose:** [What this logic performs]
**Parameters:** [Names and types]
**Returns:** [Return type and description]
**Errors/Exceptions:** [What can go wrong]

**Implementation Detail:**
[Step-by-step logic flow]

**Diagram (if complex):**
```mermaid
sequenceDiagram
    [Diagram here]
```

---

## Relationships & Traceability

**Related Files:**
- [[OtherFile-ext]] — [relationship explanation]
- `src/path/to/source.ext:line` — [direct source reference]

**Dependencies:**
- This file depends on: [[DependencyFile-ext]]
- This file is used by: [[ConsumerFile-ext]]
```

### Handling Missing Linked Files
If a referenced file doesn't have an explanation yet, still create the link: `[[MissingFile-ext]]`. Then prompt the user: "I noticed `MissingFile.ext` doesn't have an explanation file. Would you like me to generate one?"

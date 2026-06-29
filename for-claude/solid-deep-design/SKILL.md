---
name: solid-deep-design
description: Design modules and architecture combining SOLID structural principles with deep-module design philosophy. Use when writing code, implementing features, refactoring, reviewing code, designing architecture, planning technical implementations, creating Tasks/PRDs/Issues/Feature specifications, or evaluating module quality. This skill transforms code from "merely correct" to "architecturally sound" — achieving both structural integrity (SOLID) and high leverage (deep modules).
---

# SOLID + Deep Module Design

Two frameworks, one goal: code that is testable, maintainable, and AI-navigable.

- **SOLID** (from the `solid` skill) gives you structural rules — how modules relate, where dependencies point, how interfaces are shaped.
- **Deep modules** (from John Ousterhout's "A Philosophy of Software Design") give you a quality metric — is this module pulling its weight? Is there enough behavior behind its interface?

A module can be SOLID-compliant and still be shallow (a pass-through). A module can be deep but brittle if SOLID is ignored. This skill tells you how to achieve both.

> This skill references the `solid` skill for detailed explanations of SOLID principles, TDD, clean code, code smells, and design patterns. This skill adds the language of depth, seams, and adapters — and shows how they complete the SOLID picture.

---

## Language

Use these terms exactly. Consistent language across modules, reviews, and plans is the point — don't drift into "component," "service," "API," or "boundary."

### Structural Terms (from SOLID)

**Single Responsibility Principle (SRP)**
A module should have one, and only one, reason to change. Detection: can you describe what the module does without using "and"?

**Open/Closed Principle (OCP)**
Modules should be open for extension but closed for modification. New behavior comes from new code, not edits to existing, tested code.

**Liskov Substitution Principle (LSP)**
Subtypes must be substitutable for their base types without altering program correctness. This is why `InMemoryUserRepo` can replace `PostgresUserRepo` — they honor the same contract.

**Interface Segregation Principle (ISP)**
Clients should not be forced to depend on methods they do not use. Detection: if you see `throw new Error("Not implemented")` or empty method bodies, the interface is too fat.

**Dependency Inversion Principle (DIP)**
High-level modules should not depend on low-level modules. Both should depend on abstractions. Inject implementations; never `new ConcreteClass()` in business logic.

**Dependency Rule**
Source code dependencies point inward toward high-level policies (domain), never toward low-level details (infrastructure). `Infrastructure → Application → Domain`.

**Port**
An interface defined by the domain that external adapters satisfy. The contract at a boundary.

**Adapter**
A concrete implementation of a port. Connects the domain to infrastructure (database, HTTP, queue, filesystem). Describes role, not substance.

### Depth Terms (from Ousterhout)

**Module**
Anything with an interface and an implementation. Deliberately scale-agnostic — applies equally to a function, class, package, or tier-spanning slice.
_Avoid_: unit, component, service.

**Interface**
Everything a caller must know to use the module correctly. Includes the type signature, but also invariants, ordering constraints, error modes, required configuration, and performance characteristics.
_Avoid_: API, signature (too narrow — those refer only to the type-level surface).

**Implementation**
What's inside a module — its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.

**Depth**
Leverage at the interface — the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. A module is **deep** when a large amount of behaviour sits behind a small interface. A module is **shallow** when the interface is nearly as complex as the implementation.

**Seam**
A place where you can alter behaviour without editing in that place. The *location* at which a module's interface lives. Choosing where to put the seam is its own design decision, distinct from what goes behind it.
_Avoid_: boundary (overloaded with DDD's bounded context).

**Leverage**
What callers get from depth. More capability per unit of interface they have to learn. One implementation pays back across N call sites and M tests.

**Locality**
What maintainers get from depth. Change, bugs, knowledge, and verification concentrate at one place rather than spreading across callers. Fix once, fixed everywhere.

### Additional Terms

**Essential Complexity**
Complexity inherent to the problem domain. Cannot be removed, only managed.

**Accidental Complexity**
Complexity introduced by our solutions. CAN and SHOULD be minimized. Poor abstractions, unnecessary indirection, framework ceremony.

---

## Core Principles

### 1. The Interface Is the Test Surface

Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape. Tests should survive internal refactors — they describe behaviour, not implementation.

### 2. The Deletion Test

> Imagine deleting the module. If complexity vanishes, the module wasn't hiding anything (it was a pass-through). If complexity reappears across N callers, the module was earning its keep.

A pass-through module violates SRP (no real responsibility) AND has zero depth. A good deep module concentrates complexity that would otherwise scatter across callers.

### 3. One Adapter = Hypothetical Seam. Two Adapters = Real One.

Don't introduce a seam unless something actually varies across it. A single-adapter seam is just indirection. At least two adapters (typically production + test) justify the seam.

### 4. Design for Leverage, Not Just Correctness

SOLID ensures correctness and flexibility. Depth ensures the module earns its place. After satisfying SOLID, ask: "Is the interface small enough and the implementation substantial enough?" If not, deepen or consolidate.

### 5. The Dependency Rule Meets Seams

DIP tells you *how* to invert dependencies. Seams tell you *where* to put the inversion point. A port lives at a seam; an adapter satisfies it. The deepest modules define ports that callers depend on, with adapters swapped behind them.

---

## How SOLID Enables Deep Modules

### SRP → Module Cohesion

SRP says one reason to change. This is the FOUNDATION for depth:
- A module with multiple reasons to change WILL have a fragmented interface
- You can't concentrate behavior behind a small interface when behavior scatters across concerns
- **Design rule**: before asking "is this module deep?", first ask "does it have ONE reason to change?"

```typescript
// SHALLOW + violates SRP: does three things, interface exposes all of them
class OrderProcessor {
  validate(order: Order): ValidationResult { ... }
  calculateTotal(order: Order): Money { ... }
  save(order: Order): Promise<void> { ... }
  sendConfirmation(order: Order): Promise<void> { ... }
}

// DEEP + SRP: one responsibility, small interface, substantial implementation
class OrderPricing {
  calculateTotal(items: OrderItem[]): Money { ... }
  // Implementation handles: tax rules, discounts, tiered pricing, currency conversion
  // Interface: one method. Implementation: hundreds of lines of business rules.
}
```

### OCP → Interface Stability

OCP says extend without modifying existing code. This is WHY deep modules stay deep:
- A deep module's interface must survive feature additions
- If every new feature requires editing the interface, depth degrades
- **Design rule**: design interfaces that close for modification — the implementation grows behind them, not the surface

```typescript
// VIOLATES OCP + degrades depth: every new shipping type requires editing the interface
class ShippingCalculator {
  calculate(type: string, weight: number, destination: string): number {
    if (type === 'standard') return ...;
    if (type === 'express') return ...;
    // Each new type adds a branch — interface stays wide, implementation stays shallow
  }
}

// OCP + DEEP: interface closed, implementation extended through polymorphism
interface ShippingMethod {
  calculate(weight: number, destination: string): Money;
}
// Interface: one method. Implementation: each ShippingMethod is a deep module
// (carrier APIs, rate tables, zone calculations — all hidden)
```

### LSP → Seam Substitutability

LSP says subtypes must be substitutable. This is the CONTRACT for deep module seams:
- Adapters at a seam are subtypes of the seam's interface contract
- Without LSP, swapping adapters is dangerous — a mock may not behave like the real thing
- **Design rule**: every adapter at a seam must honor the interface contract defined at the seam. Tests must verify LSP compliance.

### ISP → Interface Minimality

ISP says clients shouldn't depend on unused methods. This is the CALLER-SIDE of depth:
- ISP prevents interfaces from bloating — keeping them small and focused
- A deep module can have multiple callers; ISP ensures each caller's interface stays minimal
- **Design rule**: split interfaces by caller need; depth is measured per-interface, not per-module

### DIP → Seams and Adapters

DIP says depend on abstractions, not concretions. This is the MECHANISM for seams:
- Define ports (interfaces) at seams
- Inject adapters (implementations) through dependency inversion
- **Design rule**: the seam is where the DIP inversion happens; the adapter is the concrete implementation. Don't define a port unless at least two adapters exist.

```
 ┌──────────────────────────────────────────────────┐
 │                   CALLERS                         │
 │  (depend on the port — DIP satisfied)             │
 └──────────────────────┬───────────────────────────┘
                        │  depends on
                        ▼
              ┌─────────────────┐
              │   PORT (seam)    │  ← the interface
              │  PaymentGateway  │
              └────────┬────────┘
                       │  implemented by
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │  Stripe  │ │  PayPal  │ │   Mock   │
   │ Adapter  │ │ Adapter  │ │ Adapter  │
   └──────────┘ └──────────┘ └──────────┘
```

---

## The Deletion Test in Practice

Apply the deletion test to every module you design, review, or plan:

**Step 1**: Imagine deleting the module entirely.
**Step 2**: Trace where its complexity would go.
**Step 3**: Judge the result.

| Deletion Result | Verdict | Action |
|-----------------|---------|--------|
| Complexity vanishes — nothing needed it | Pass-through (shallow, no SRP) | Delete it or merge into caller |
| Complexity reappears identically across N callers | Shallow — it was indirection | Merge the module into callers OR deepen it |
| Complexity reappears concentrated but N callers need to reimplement it | **Deep** — it was hiding real complexity | Keep it, it's earning its keep |
| Complexity scatters across N callers, each implementing slightly differently | **Deep** — it was providing leverage AND locality | Keep it, this is the ideal |

---

## Deepening Strategies

When you identify a cluster of shallow modules, deepening means merging them behind a single interface. Full details in [references/deepening-strategies.md](references/deepening-strategies.md).

### Dependency Categories

Classify each dependency of the candidate modules:

| Category | Description | Deepenable? | Test Strategy |
|----------|-------------|-------------|---------------|
| **In-process** | Pure computation, in-memory state, no I/O | Always | Test through the new interface directly |
| **Local-substitutable** | Has local test stand-in (PGLite, in-memory FS) | Yes, if stand-in exists | Test with stand-in in suite |
| **Remote but owned** | Your own services across network | Yes, with ports & adapters | Define port, inject in-memory adapter for tests |
| **True external** | Third-party (Stripe, Twilio) | Yes, with mocks | Inject as port, provide mock adapter |

### Seam Discipline

- **One adapter = hypothetical seam. Two adapters = real one.** Don't introduce a port unless at least two adapters are justified.
- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface.
- **Replace, don't layer.** Old unit tests on shallow modules become waste once tests at the deepened module's interface exist — delete them. Write new tests at the deepened module's interface.

---

## Design Process

### When Writing New Code

Apply this process for every new module:

1. **Start with responsibility** (SRP): what ONE thing does this module do? Write it as a single sentence without "and."
2. **Define the interface** (ISP + Depth): what must callers know? Keep it minimal. Aim for 1-3 entry points.
3. **Design for extension** (OCP): what will change? What will stay? Close the stable parts.
4. **Place the seam** (DIP + Seams): where does the interface live? Does it need adapters?
5. **Apply the deletion test**: does this module concentrate or scatter complexity?
6. **Measure depth**: is the interface small compared to what sits behind it?
7. **Write tests at the interface**: the interface IS the test surface.

### When Reviewing Code

For every module under review, ask:

| Question | Principle | Red Flag |
|----------|-----------|----------|
| Does this have ONE reason to change? | SRP + Depth | Describing it requires "and" |
| Can I extend it without modifying it? | OCP + Depth | if/else chains for types |
| Can I swap the adapter safely? | LSP + Seams | Type-checking in calling code |
| Are clients forced to depend on unused methods? | ISP + Depth | Empty method implementations |
| Do high-level modules depend on abstractions? | DIP + Seams | `new ConcreteClass()` in business logic |
| Would deleting it scatter complexity? | Deletion Test | Complexity vanishes on deletion |
| Is the interface much smaller than the implementation? | Depth | Interface ≈ implementation in complexity |

### When Creating Technical Plans (PRDs, Tasks, Issues, Features)

When planning a new feature or writing a technical implementation plan:

1. **Identify the modules** the feature will touch or create. Name them using domain language.
2. **For each new module**, apply the Design Process above before writing implementation details.
3. **For each existing module being modified**, apply the review questions. If a module already violates SOLID or is shallow, note the refactoring cost in the plan.
4. **Document seams**: where will the new feature's modules sit relative to existing architecture? What ports will they define? What adapters will they need?
5. **Apply the deletion test to the plan**: if you deleted this feature's modules, would complexity scatter? If yes — good, the modules are deep. If no — the plan is introducing pass-throughs.
6. **Include depth as an acceptance criterion**: "The X module has an interface of ≤ 3 public methods and encapsulates all X-related business rules."

---

## Quick Reference

### Design Decision Matrix

| Situation | SOLID Says | Depth Says | Combined Action |
|-----------|------------|------------|-----------------|
| Module does too many things | SRP: split it | Shallow: split degrades depth | Split into focused modules, each deep |
| New feature requires editing many files | OCP: design for extension | Low locality: scattered complexity | Consolidate behind stable interfaces |
| Adapter swap breaks callers | LSP: enforce contract | Seam integrity violated | Add contract tests at the seam |
| Interface has 15 methods, most unused | ISP: segregate | Interface too wide = shallow | Split by caller, measure depth per interface |
| Business logic calls `new Database()` | DIP: invert dependency | Seam in wrong place | Define port, inject adapter |
| Module's code is just delegation | SRP: maybe a coordinator | Shallow: pass-through | Merge into caller or deepen by absorbing logic |
| Testing requires mocking 10 dependencies | DIP: too many concretions | Interface too wide | Consolidate dependencies, deepen the module |

### Depth Diagnostic

For any module, answer:

```
Module: ______________________
Interface (public surface): ___ methods, ___ types, ___ error modes
Implementation: ___ lines, ___ dependencies, ___ business rules
---
SRP check: Does it have ONE reason to change? [Y/N]
Deletion test: Would deleting it scatter complexity? [Y/N]
Depth: Is the interface MUCH smaller than the implementation? [Y/N]
---
Verdict: [DEEP / SHALLOW / PASS-THROUGH]
Action:  [KEEP / DEEPEN / DELETE]
```

---

## References

- **`solid` skill** — Full SOLID principles, TDD, clean code, code smells, design patterns, testing strategy, complexity management. Use for detailed guidance on each principle.
  - `solid/references/solid-principles.md` — SRP, OCP, LSP, ISP, DIP with examples
  - `solid/references/architecture.md` — Hexagonal/ports-and-adapters, dependency rule
  - `solid/references/complexity.md` — Essential vs accidental complexity
  - `solid/references/code-smells.md` — Detection and solutions
  - `solid/references/testing.md` — Testing strategy and patterns
  - `solid/references/clean-code.md` — Naming, structure, value objects

- **This skill's references**:
  - `references/deepening-strategies.md` — Full deepening guide with dependency categories, seam discipline, and testing strategy

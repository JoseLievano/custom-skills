---
name: react-code-organization
description: Organize or refactor large React codebases into a feature-based architecture with clear boundaries between shared code, feature code, routing, layouts, hooks, services, and third-party facades. Use when creating a new React project structure, cleaning up a crowded `src/` tree, deciding where new React files belong, moving from type-based folders to feature-based folders, or enforcing import and ownership rules in React or React+TypeScript apps.
---

# React Code Organization

Use this skill to keep a large React codebase predictable. React is intentionally flexible about file structure, so apply one consistent structure and enforce it with placement and import rules rather than ad hoc folder growth.

React guidance this skill aligns with:
- Build UIs from reusable components.
- Keep components focused and pure during render.
- Extract reusable stateful logic into custom hooks.

## Workflow

1. Audit the current tree and identify business features, shared UI, layouts, routes, hooks, services, and library wrappers.
2. Define the target feature folders under `src/features/` and keep route-level assembly outside those folders.
3. Move each file according to ownership rules: feature-local stays inside the feature, cross-feature shared code moves to `src/`.
4. Add or preserve a feature public API file (`index.ts` or `index.js`) and stop deep imports into feature internals.
5. Enforce the boundaries: components render, hooks manage UI-facing logic, services talk to data sources, and `lib/` wraps third-party tools.

## Target Structure

Use this shape as the default baseline:

```text
src/
├── assets/
├── components/
│   ├── ui/
│   └── forms/
├── context/
├── data/
├── features/
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       ├── context/      # optional
│       ├── utils/        # optional
│       ├── types.ts      # optional
│       └── index.ts
├── hooks/
├── layouts/
├── lib/
├── pages/
├── router.tsx
├── services/
├── types/
└── utils/
```

## Placement Rules

Apply these rules mechanically:

| Question | Place it here |
| --- | --- |
| Used by only one business feature? | `src/features/[feature]/...` |
| Shared by two or more unrelated features? | `src/components/`, `src/hooks/`, `src/services/`, `src/utils/`, or `src/types/` |
| Defines page shell or frame structure? | `src/layouts/` |
| Is a route target that assembles features? | `src/pages/` |
| Wraps a third-party library? | `src/lib/` |
| Static routes/constants/mock data? | `src/data/` |

Do not put feature-specific code in global folders just because it is a component or a hook.

## Feature Rules

A feature is a user-visible business domain such as `authentication`, `projects`, or `todos`.

Inside each feature:
- Keep UI in `components/`.
- Keep stateful composition logic in `hooks/`.
- Keep API and external data calls in `services/`.
- Keep feature-only context, utils, and types local when they are not shared.
- Export the feature's public surface from `index.ts` or `index.js`.

Enforce the public API rule:
- Import from `src/features/[feature]`.
- Do not import from `src/features/[feature]/components/...` or other internals from outside the feature.
- Treat anything not re-exported from the feature index as private.

## Layer Rules

Keep the dependency direction simple:

| Layer | May import from | Must not import from |
| --- | --- | --- |
| `components/` | feature hooks, shared UI, local child components | feature services directly |
| `hooks/` | feature services, shared hooks, feature utils/types | feature components |
| `services/` | `src/lib/`, feature types/utils | feature hooks or components |

Keep components render-focused. If a component starts owning repeated effects, async orchestration, or business-state transitions, extract a hook.

## Routing Rules

Keep routing concerns out of features:
- Features are routing-agnostic.
- Pages are thin assemblers that compose feature exports.
- Layouts own shared chrome such as nav, sidebars, and page shells.
- The router owns paths, nested layouts, guards, and route loaders.

Use this rule of responsibility:
- `src/router.tsx`: route definitions, nested layout structure, loaders
- `src/layouts/`: app shell components that render once and expose `<Outlet />`
- `src/pages/`: route targets that compose features
- `src/features/`: feature UI and logic with no route ownership

## Shared Code Rules

- Keep tests, styles, and stories next to the component they belong to.
- Give each non-trivial component its own folder.
- Let components import their children, not siblings or parents.
- When siblings need shared code, move it up to a shared folder at the nearest common parent.
- Move code upward only when it is truly shared; do not globalize code prematurely.

## Library And Service Rules

Separate tool wrappers from business calls:
- `src/lib/`: facade over third-party libraries such as HTTP clients, analytics SDKs, or date libraries
- `src/services/`: business-oriented shared calls used by multiple features
- `src/features/[feature]/services/`: business calls used only by one feature

This keeps library swaps and cross-cutting concerns centralized.

## TypeScript Rules

For TypeScript projects:
- Keep app-wide shared types in `src/types/`.
- Keep feature-specific domain types in `src/features/[feature]/types.ts`.
- Re-export public feature types from the feature index.

## Enforcement

When cleaning up or reviewing a codebase:
- Flag deep imports into feature internals.
- Flag components that call services directly.
- Flag pages that own business logic or duplicated layout chrome.
- Flag feature folders that import routing APIs for route ownership.
- Prefer adding lint rules for restricted deep imports once the structure is in place.

## Reference

Read [references/organization-reference.md](references/organization-reference.md) when you need:
- a fuller target tree
- routing and loader examples
- the facade pattern rationale
- anti-patterns and fixes
- an ESLint restricted-imports example

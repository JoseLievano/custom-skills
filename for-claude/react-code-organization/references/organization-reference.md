# React Code Organization Reference

Use this file when the task needs concrete examples beyond the operating rules in `SKILL.md`.

## Target `src/` Tree

```text
src/
├── assets/
│   ├── images/
│   ├── icons/
│   └── styles/
├── components/
│   ├── ui/
│   │   ├── Button/
│   │   ├── Modal/
│   │   └── Spinner/
│   └── forms/
│       ├── FormInput/
│       └── FormSelect/
├── context/
├── data/
├── features/
│   ├── authentication/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   ├── utils/
│   │   ├── types.ts
│   │   └── index.ts
│   ├── projects/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── index.ts
│   └── todos/
│       ├── assets/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       ├── utils/
│       ├── types.ts
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

## Feature Example

```text
features/
└── todos/
    ├── components/
    │   ├── TodoList/
    │   │   ├── TodoList.tsx
    │   │   ├── TodoList.test.tsx
    │   │   └── TodoList.module.css
    │   ├── TodoItem/
    │   └── TodoFilters/
    ├── hooks/
    │   └── useTodos.ts
    ├── services/
    │   └── todoService.ts
    ├── utils/
    │   └── normalizeTodo.ts
    ├── types.ts
    └── index.ts
```

Only re-export what other parts of the app should consume:

```ts
export { TodoList } from './components/TodoList/TodoList'
export { TodoFilters } from './components/TodoFilters/TodoFilters'
export { useTodos } from './hooks/useTodos'
export type { Todo, CreateTodoDto } from './types'
```

## Facade Pattern

Keep third-party libraries behind app-owned entry points.

Example:
- `src/lib/api.ts` owns the HTTP client instance, interceptors, auth headers, and timeouts.
- Feature services import from `src/lib/api.ts`, not from `axios` directly.

Result:
- library swaps happen in one file
- cross-cutting behavior stays centralized
- feature services stay business-focused

## Layer Example

```text
components -> hooks -> services -> lib
```

Examples:
- `TodoList.tsx` renders UI and calls `useTodos()`
- `useTodos.ts` manages loading, error, and mutation state
- `todoService.ts` calls the backend
- `api.ts` wraps the HTTP library

## Routing Decision Map

| Concern | Place |
| --- | --- |
| Route paths | `src/router.tsx` |
| Layout nesting | `src/router.tsx` + `src/layouts/` |
| Shared shell with `<Outlet />` | `src/layouts/` |
| Route guards | router layer or shared route guard component |
| Route loaders | `src/router.tsx` |
| Page composition | `src/pages/` |
| Business UI and state | `src/features/` |

Golden rule:
- features do not own URLs
- pages assemble features
- router assembles pages into layouts

## Anti-Patterns

Avoid these:
- deep imports into feature internals
- pages that fetch data and manage feature business logic
- duplicated nav/sidebar markup inside page files
- components that call services directly
- feature folders that own route definitions
- dumping feature-specific code into `src/components/` because it is "just a component"

## ESLint Guardrail

Use a restricted-import rule once the structure is stable:

```json
{
  "rules": {
    "no-restricted-imports": [
      "error",
      {
        "patterns": [
          "../features/*/components/*",
          "../features/*/hooks/*",
          "../features/*/services/*"
        ]
      }
    ]
  }
}
```

Adjust the pattern to match the repo's alias strategy.

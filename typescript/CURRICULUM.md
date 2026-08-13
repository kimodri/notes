# Frontend TypeScript Project Curriculum

## Outcome

The goal is to become able to take a frontend idea from UI design through typed implementation, API integration, testing, and deployment, then reuse the same backend contract from a React Native client.

This is deliberately **not** a Node.js backend curriculum. Node.js appears only as the runtime for npm, Vite, linters, tests, code generation, and small development scripts. Production APIs are treated as separate systems that may be written in Laravel/PHP, FastAPI/Python, or another stack.

## How to read the depth labels

- **Deep**: explain it, use it without a recipe, recognize tradeoffs, and debug it.
- **Working**: use it correctly with documentation and explain its purpose.
- **Later**: recognize it, but do not delay projects to master it.

## How the projects become more independent

| Phase | Guidance | What is supplied |
| --- | --- | --- |
| Stages 1–3 | High | Small steps, examples, acceptance criteria, suggested file structure |
| Stages 4–7 | Medium | Requirements, API contract, checkpoints, selected hints |
| Stages 8–10 | Low | Product brief and quality bar; learner proposes architecture |
| Stages 11–14 | Professional | Ambiguous product brief, backend contract, constraints, review feedback |

Do not advance merely because the UI works. Advance when the stage's exit gate can be demonstrated and explained.

---

## Stage 1 — Small programs with real logic

### Project: Personal expense analyzer

Build a program that accepts an in-memory list of transactions, validates and normalizes it, calculates totals by category, finds unusual entries, and formats a report. Add tests for the pure calculation functions.

Alternative projects: grade report generator, shopping-cart price engine, or workout statistics analyzer.

**Why now:** This creates useful behavior immediately while keeping the browser, framework, and network out of the way. Errors can be traced directly to JavaScript logic or TypeScript modeling.

**TypeScript**

- **Deep:** inference, primitive types, arrays, object types, function parameters and returns, type aliases, optional properties, unions, literal types, `null`/`undefined`, narrowing, `unknown` versus `any`.
- **Working:** readonly data, tuples where position truly matters, `Record`, `Pick`, `Omit`, `Partial`, type-only imports.
- **Later:** enums, classes, declaration files, conditional and mapped type authoring.

**JavaScript**

- **Deep:** variables and scope, functions, objects, arrays, destructuring, spread, `map`/`filter`/`reduce`, equality, truthiness, control flow, modules, value versus reference behavior.
- **Working:** exceptions, dates and number formatting.

**Tools:** TypeScript compiler in strict mode, npm scripts, Git, VS Code type inspection, Vitest for pure functions. Node runs the tools and the small program; it is not the subject.

**Exit gate:** Given a new transaction requirement, independently update the model, implementation, and tests. Explain why an API value would initially be `unknown`, why `any` hides mistakes, and why TypeScript does not validate runtime data.

**Common gaps:** annotating every variable instead of using inference; using `any` to silence errors; confusing optional with nullable; type assertions used as conversions; putting all logic in one function; learning `enum` before ordinary unions and objects.

---

## Stage 2 — First browser TypeScript application

### Project: Accessible unit and currency-style converter

Build a responsive page with several conversion modes, formatted results, keyboard support, URL-shareable inputs, and no framework.

Alternative projects: tip splitter, color palette inspector, or reading-time calculator.

**Why now:** It introduces the browser and build pipeline without adding complex state or a network. It also makes the difference between compile-time types and browser runtime behavior visible.

**TypeScript**

- **Deep:** DOM element types, null checks, event types, discriminated unions for conversion modes, module boundaries.
- **Working:** `satisfies`, `as const`, generic DOM queries only when justified.
- **Later:** custom `.d.ts` files and elaborate generic helpers.

**JavaScript and web platform**

- **Deep:** ES modules, the DOM tree, selectors, attributes versus properties, event listeners, form submission, URL and `URLSearchParams`.
- **Working:** browser storage and history APIs.

**Tools:** Vite `vanilla-ts`, semantic HTML, modern CSS, browser DevTools, ESLint and Prettier. Keep `tsc --noEmit` as a separate check because Vite transpiles TypeScript but does not itself type-check it.

**Exit gate:** Build and deploy a static preview locally; diagnose a DOM nullability error; make the page usable with keyboard only; explain source TypeScript versus emitted browser JavaScript.

**Common gaps:** casting every selector result; using clickable `div`s; treating CSS and accessibility as later concerns; committing generated build output; assuming Vite's dev server is a production backend.

---

## Stage 3 — DOM, events, forms, and state

### Project: Local-first task or habit tracker

Features: create/edit/delete, filters, validation, derived counts, persistence, import/export JSON, confirmation for destructive actions, and an empty state.

Alternative projects: bookmark manager, meal planner, or inventory counter.

**Why now:** CRUD interactions expose state modeling problems early, before a framework hides the mechanics. Importing JSON forces runtime validation at a trust boundary.

**TypeScript**

- **Deep:** domain models versus form models, discriminated unions, exhaustive `switch`, safe parsing from `unknown`, reusable typed functions, immutable updates.
- **Working:** generic result types such as `Result<T, E>`, user-defined type guards.
- **Later:** generic class hierarchies and advanced type-level validation.

**JavaScript and browser**

- **Deep:** event propagation, `preventDefault`, form data, state as a single source of truth, render/update cycles, JSON serialization limitations, localStorage.
- **Working:** event delegation, custom events.

**Tools:** Vite, CSS, browser storage, a small runtime schema validator such as Zod after first writing one manual validator, accessibility checks.

**Exit gate:** Reload without losing data; reject malformed imports without crashing; distinguish loading/error/empty/success-like UI states even though data is local; add a feature without creating a second conflicting source of state.

**Common gaps:** storing DOM nodes as application state; mutating shared arrays; trusting `JSON.parse`; mixing persistence, domain logic, and rendering; validating only after submission; forgetting focus and error-message accessibility.

---

## Stage 4 — Asynchronous JavaScript and TypeScript

### Project: Search-as-you-type media explorer using a simulated API

Create a promise-based data source with variable delay and deliberate failures. Implement debouncing, cancellation, retry, stale-request protection, a detail view, and explicit loading/error/empty/success states.

**Why now:** A simulated API makes race conditions deterministic. The learner can understand the event loop and cancellation before debugging a real server and CORS simultaneously.

**TypeScript**

- **Deep:** `Promise<T>`, async function return types, `unknown` in `catch`, typed success/error results, state-machine unions.
- **Working:** generic async helpers, `Awaited`, abort-related DOM types.
- **Later:** complex promise combinator types.

**JavaScript**

- **Deep:** event loop mental model, promises, `async`/`await`, error propagation, timers, `Promise.all`, race conditions, closures, `AbortController`.
- **Working:** `allSettled`, concurrency limits.

**Tools:** DevTools network-style debugging, fake timers where useful, Vitest async tests.

**Exit gate:** Prove that an old slow response cannot overwrite a newer query; cancel work on a new search; show different UI for no matches, recoverable failure, and success.

**Common gaps:** `await` inside unnecessary loops; unhandled rejections; catching errors and discarding them; treating every failure as `Error`; spinner-only state design; using a timeout as a race-condition fix.

---

## Stage 5 — Consume a real REST API

### Project: Public catalog explorer

Use a stable public API to build list/detail pages with search, sort, filters, URL-backed state, pagination, caching hints, and resilient response parsing.

Good domains include books, countries, museums, games, or public datasets. Choose an API that supports the needed operations and has acceptable availability and terms.

**Why now:** Read-only data keeps risk low while introducing actual HTTP, unreliable networks, and contracts the frontend does not control.

**TypeScript**

- **Deep:** transport/DTO types versus UI/domain types, `unknown` at network boundaries, runtime parsing, optional and nullable fields, generic API results, mapping functions.
- **Working:** indexed access types, `keyof`, utility types, branded IDs only if they prevent a real mix-up.
- **Later:** generated clients until the handwritten request/response flow is understood.

**JavaScript, HTTP, and browser**

- **Deep:** `fetch`, JSON, headers, query strings, GET semantics, common 2xx/4xx/5xx statuses, the fact that `fetch` does not reject merely because the status is 404 or 500.
- **Working:** caching headers, rate limits, retries with restraint, API version paths/headers.

**Tools:** browser Network panel, REST client for inspection, runtime schema validation, Vite environment variables.

**Exit gate:** Handle malformed data, non-JSON errors, timeouts/cancellation, 404, 429, and 500 without a blank or broken screen. Keep filters in the URL and preserve them across refresh/navigation.

**Common gaps:** writing an interface and assuming it validates JSON; calling `response.json()` before checking content/status strategy; leaking API shapes throughout the UI; hard-coded base URLs; retrying non-idempotent requests blindly; hiding useful server errors.

---

## Stage 6 — Work from a foreign-backend API contract

### Project: Contract-driven customer directory

Build the frontend against a supplied OpenAPI document and mock server that resembles either Laravel API Resources or FastAPI response models. Then connect it to the real separately run API without changing UI components.

**Why now:** Professional frontend work often begins before the backend is finished. This project teaches collaboration through contracts instead of shared implementation language or copied model files.

**TypeScript**

- **Deep:** API boundary ownership, DTO-to-domain mapping, normalization, contract drift handling, runtime validation versus static types.
- **Working:** OpenAPI-generated types/client, schema versioning, adapters for inconsistent legacy responses.
- **Later:** publishing a full SDK or sophisticated code-generation templates.

**API collaboration**

- **Deep:** methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), status codes, JSON serialization, field naming and date conventions, stable error shapes, idempotency from a consumer perspective.
- **Working:** OpenAPI 3.x, API versioning, deprecation, contract tests.

**Tools:** OpenAPI document, mock service/MSW, `openapi-typescript` or a generated FastAPI client after one handwritten client, API changelog.

**Exit gate:** Swap mock and real base URLs by configuration; identify a breaking contract change; update generated types and adapters; explain why frontend and backend should share a schema/contract rather than import source-language models.

**Common gaps:** editing generated files; assuming generated static types validate runtime values; coupling components to Laravel/FastAPI envelopes; undocumented date/time assumptions; sharing an entire monorepo merely to share types.

---

## Stage 7 — Mutations, auth, authorization, validation, and uploads

### Project: API integration workbench, then a small issue tracker

First build a deliberately plain UI that exercises login/logout, session expiry, protected requests, field errors, pagination, filtering, optimistic versus confirmed updates, and multipart upload. Then apply those flows to a small issue tracker UI.

Run two auth modes as separate exercises:

1. Browser SPA with secure HTTP-only session cookie and CSRF flow (Laravel Sanctum is a realistic backend).
2. Bearer access token flow suitable for a mobile or third-party client (a FastAPI OAuth2-style API or Laravel Sanctum token API is realistic).

**Why now:** Authentication is easier to understand before a framework and state library obscure requests. The workbench isolates protocol mistakes; the issue tracker proves they can be expressed as good UX.

**TypeScript**

- **Deep:** typed error taxonomy, validation-error maps, authorization capabilities, mutation state, request payload versus response types, exhaustive auth states.
- **Working:** generic request client, middleware/interceptors, multipart types, token refresh coordination if the chosen backend uses refresh tokens.
- **Later:** implementing OAuth/OIDC protocols or cryptography yourself.

**Frontend/API knowledge**

- **Deep:** 400/401/403/404/409/422 distinctions; client versus server validation; cookies versus bearer tokens; credentials mode; CORS versus CSRF; never treating hidden UI as authorization; `FormData`; progress/size/type feedback; page/cursor pagination.
- **Working:** SameSite/Secure/HttpOnly attributes, refresh-token rotation at a design level, presigned uploads, idempotency keys.
- **Later:** enterprise SSO internals and custom auth servers.

**Tools:** DevTools Application and Network panels, MSW for failure cases, backend API supplied separately, environment-based API configuration.

**Exit gate:** Correctly render backend field errors; recover from expired authentication; prevent duplicate submission; distinguish forbidden from unauthenticated; upload with useful feedback; preserve pagination/filter state; explain where each credential lives and its XSS/CSRF tradeoff.

**Common gaps:** storing long-lived secrets in localStorage by default; confusing CORS with authentication; attempting to solve CORS in frontend code or with `no-cors`; assuming disabled buttons provide authorization; discarding 422 field errors; manually setting multipart `Content-Type` boundaries; endless refresh loops.

---

## Stage 8 — React with TypeScript

### Project: Rebuild the issue tracker in React

Reimplement Stage 7's product behavior, keeping the same API contract and test scenarios. Do not add a global state library at first.

**Why now:** Known product behavior leaves attention available for React's model. Comparing the vanilla and React versions reveals what React solves and what remains ordinary JavaScript, HTTP, and TypeScript.

**TypeScript and React**

- **Deep:** typed props, children, event handlers, component composition, controlled forms, `useState` inference, reducers with discriminated actions, refs, context boundaries, custom-hook contracts.
- **Working:** generic components only when multiple real consumers need them, typing third-party components.
- **Later:** polymorphic `as` components, elaborate component type utilities, class components.

**React/JavaScript**

- **Deep:** render purity, state snapshots, effects and cleanup, derived state, identity/keys, lifting versus colocating state, closures in hooks.
- **Working:** memoization after measurement, error boundaries.

**Tools:** React + TypeScript Vite template, React DevTools, React Router when multiple screens are real.

**Exit gate:** Explain every effect and remove unnecessary ones; keep server data, URL state, form state, and local UI state distinct; type components without `React.FC` being a reflex; preserve all Stage 7 failure handling.

**Common gaps:** using effects for derived values or event logic; giant context stores; optional props everywhere; duplicating server state locally; unstable list keys; using type assertions to force component props; forgetting semantic HTML inside JSX.

---

## Stage 9 — Larger frontend architecture

### Project: Team operations dashboard

Build a multi-route application with dashboard, resource lists/details, create/edit flows, role-sensitive actions, URL filters, reusable layout, and realistic API data.

**Why now:** The application is finally large enough for architecture choices to solve observed pain instead of being copied ceremonially from a template.

**Deep:** feature boundaries, dependency direction, server/client/form/URL state separation, API client and adapter layers, reusable design-system primitives, route-level error/loading behavior, authorization-aware UI, accessible navigation.

**Working:** TanStack Query for server state, React Router, React Hook Form plus schema validation, code splitting, optimistic mutations, error boundaries, lightweight client state store only if a concrete cross-feature need exists.

**Later:** micro-frontends, monorepos, custom framework infrastructure, universal rendering unless a product requires it.

**Exit gate:** Draw and defend the module boundaries; add a feature without editing unrelated layers; invalidate or update cache correctly after mutations; deep-link to every meaningful screen/filter; prevent components from making ad hoc network calls.

**Common gaps:** folders by file type only; premature shared abstractions; one global store for everything; query cache and local state disagreeing; API clients importing React; authorization logic scattered through presentational components.

---

## Stage 10 — Testing and production-quality practices

### Project: Production hardening sprint for Stage 9

Do not start a toy testing project. Harden the existing dashboard and fix defects discovered by the tests and audits.

**Why now:** Tests become meaningful when behavior, async boundaries, forms, routing, and failure cases exist. The task resembles professional stabilization work.

**Deep:** test behavior rather than implementation, testing pyramid/tradeoffs, deterministic data, mock boundaries, accessible queries, regression tests, static analysis, CI quality gates, error observability, security and performance basics.

**Working:** Vitest for logic, React Testing Library for components, MSW for API behavior, Playwright for critical user journeys, coverage as a diagnostic rather than a target, Lighthouse/accessibility tools, dependency auditing.

**Later:** exhaustive visual regression infrastructure, mutation testing, bespoke performance labs.

**Required quality gates:** format, lint, strict type-check, unit/component tests, production build, selected end-to-end tests, keyboard/a11y review, responsive review, no secrets in the bundle, useful error logging with sensitive-data redaction.

**Exit gate:** CI runs the gates; critical auth and CRUD paths have E2E coverage; network failure and 422/401/403 cases have integration coverage; a production-like build can be diagnosed from source maps/logs without exposing secrets.

**Common gaps:** snapshot-heavy tests; mocking every internal module; E2E testing every edge case; brittle CSS selectors; chasing 100% coverage; testing types at runtime; logging tokens or personal data.

---

## Stage 11 — Real Laravel and FastAPI integration sprints

### Project A: React frontend for Laravel

Integrate the dashboard with a separately owned Laravel API using API Resources, validation errors, pagination, uploads, and Sanctum. Prefer first-party cookie/session SPA auth for the browser where the deployment topology supports it; use API tokens for mobile or external clients.

### Project B: React frontend for FastAPI

Connect the same UI or an equivalent domain to FastAPI response models and OpenAPI. Generate the client/types, compare them with the Laravel workflow, and document contract differences.

**Why now:** The learner already knows the protocol and UI concerns, so framework-specific backend conventions can be understood as adapters rather than magical frontend rules.

**Deep:** integration diagnosis, contract negotiation, CORS/credential configuration from the browser's viewpoint, 422/error normalization, time/date and null conventions, backward-compatible change handling.

**Working:** Laravel Sanctum SPA/token modes, Laravel resource envelopes/pagination, FastAPI OpenAPI client generation, backend-provided schema pipelines.

**Later:** writing substantial Laravel/FastAPI business logic unless separately learning that backend stack.

**Exit gate:** Integrate with either backend without backend source imports; regenerate types in CI or a documented command; normalize each backend into stable frontend domain types; write a concise integration guide for the backend developer.

**Common gaps:** blaming all blocked requests on CORS; changing the frontend type instead of resolving contract drift; tying UI components to generated types; depending on undocumented backend behavior; expecting cookie auth to work identically in native mobile.

---

## Stage 12 — Frontend deployment

### Project: Deploy the production-hardened web client

Deploy a static SPA or appropriate frontend build independently from its Laravel/FastAPI API. Configure staging and production API URLs, SPA routing fallbacks, HTTPS, cache rules, error monitoring, and CI deployment.

**Why now:** Deployment reveals build-time configuration, origin, routing, caching, and observability issues that local development hides.

**Deep:** build-time versus runtime configuration, public versus secret variables, origins, HTTPS, SPA rewrites, asset caching/invalidation, rollback, source maps, API compatibility during independent releases.

**Working:** provider configuration, preview environments, CSP and security headers, bundle analysis, CDN concepts.

**Later:** advanced edge rendering and infrastructure orchestration.

**Exit gate:** Fresh deployment works from a deep link; no secret is bundled; staging cannot accidentally call production; frontend and API can roll forward/back without immediate breakage; deployment is repeatable from CI.

**Common gaps:** treating frontend environment variables as secrets; only testing `/`; caching `index.html` too aggressively; missing CORS production origin; no API version compatibility window; unhandled chunk-load errors after releases.

---

## Stage 13 — React Native with TypeScript

### Project: Mobile companion for a completed web app

Use Expo and React Native to implement authentication, list/detail, create/edit, offline-aware loading/error states, navigation, and one native capability such as camera/file selection or notifications.

**Why now:** React, TypeScript, API modeling, and testing are already familiar. The learner can focus on native UI, navigation, device permissions, storage, and platform constraints.

**Deep:** React Native primitives, layout with Flexbox, navigation, platform differences, touch/keyboard behavior, app lifecycle, network variability, secure credential storage, accessibility on mobile.

**Working:** Expo, file/image picker, deep links, native build/configuration, mobile testing, app-store build concepts.

**Later:** custom native modules, bare-workflow internals, complex animations, platform-specific native code.

**Exit gate:** Run on a real device; handle offline/reconnect and expired auth; never assume browser DOM/storage/cookies; produce an installable preview build; document platform-specific behavior.

**Common gaps:** trying to reuse DOM components; storing tokens in insecure general storage; tiny touch targets; ignoring safe areas and keyboards; assuming localhost refers to the development computer; treating mobile connectivity as stable.

---

## Stage 14 — Web and mobile clients sharing an API

### Project: Shared-contract multi-client release

Ship a React web client and React Native client against the same versioned Laravel or FastAPI API. Share contract generation, domain rules, and selected API utilities; keep platform UI and credential/storage adapters separate.

**Why now:** Sharing too early creates false abstractions. At this stage, duplication can be measured and only stable, platform-neutral code is extracted.

**Deep:** API contract as the shared boundary, platform adapters, compatible auth strategy, version skew, feature capabilities, release coordination, shared validation/domain logic versus platform UI.

**Working:** workspace/package organization if it reduces real duplication, generated OpenAPI package, per-client query caches, push/deep-link handoff.

**Later:** universal UI/component systems unless both products genuinely benefit.

**Exit gate:** Both clients survive a compatible API evolution; generated contracts cannot silently drift; auth is appropriate per platform; shared code contains no DOM or native dependency; each client has independent builds and tests.

**Common gaps:** forcing identical authentication on browser and mobile; sharing components merely because both use React; one release blocking every other release; generated-code edits; assuming same API means identical UX.

---

## Concepts to prioritize across the whole curriculum

### Understand deeply

- JavaScript runtime behavior: scope, closures, objects/references, array transforms, modules, event loop, promises, errors.
- Type inference, unions, narrowing, `unknown`, nullability, structural typing, generics used at real boundaries, and the compile-time/runtime distinction.
- Semantic HTML, CSS layout/responsiveness, accessibility, forms, browser DevTools, and URL state.
- HTTP semantics, status codes, JSON, trust boundaries, validation, auth flows, CORS/CSRF, and resilient UI states.
- React's state/render/effect model and separation of server, URL, form, and local state.
- Testing behavior, architecture boundaries, configuration, deployment, and observability.

### Working familiarity is enough

- Utility/mapped/conditional types as a consumer, declaration files, library type inspection.
- OpenAPI code generation, query/form libraries, state libraries, bundler configuration, CI/provider syntax.
- Cookie attributes, token refresh designs, CSP, caching, performance analysis, and native build settings.

### Safely learn later

- Type-level puzzles, recursive conditional types, decorators, namespaces, compiler internals.
- Node/Express/Nest backend development, ORMs in TypeScript, server-side TypeScript architecture.
- Micro-frontends, custom bundlers, custom auth protocols, complex native modules, premature monorepos.

## Portfolio capstone options

Each capstone must include responsive and accessible UI, a documented API contract, authentication/authorization, server validation display, pagination/search/filtering, an upload or media workflow, complete async states, tests, CI, and a deployed frontend.

1. **Field service operations platform — web + mobile candidate.** React web dashboard for dispatchers; React Native companion for technicians; jobs, schedules, status transitions, photos, offline-aware updates, and role-based actions. Laravel or FastAPI can serve both clients.
2. **Clinic appointment and patient portal.** Scheduling, provider search, patient documents, reminders, role-sensitive views, audit-friendly UI, and strong privacy/error handling. Use synthetic data only.
3. **Team asset and maintenance manager.** Asset catalog, QR/photo upload, maintenance history, filters, pagination, assignments, and reports. Natural React Native extension for scanning and field updates.
4. **Learning cohort platform.** Courses, assignments, submissions, feedback, progress dashboards, file uploads, instructor/learner permissions, and notifications.
5. **Small-business order and inventory console.** Product inventory, orders, status workflows, customer search, optimistic stock warnings, CSV/image uploads, and operational dashboards.

The strongest mobile extension is the field service platform; the asset manager is a close second.

## Suggested official references

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Vite guide](https://vite.dev/guide/)
- [Using TypeScript with React](https://react.dev/learn/typescript)
- [MDN HTTP guide](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [MDN Fetch guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [Laravel authentication](https://laravel.com/docs/12.x/authentication) and [Sanctum](https://laravel.com/docs/master/sanctum)
- [FastAPI client generation](https://fastapi.tiangolo.com/advanced/generate-clients/)
- [Playwright tests](https://playwright.dev/docs/writing-tests)
- [React Native TypeScript guide](https://reactnative.dev/docs/typescript)


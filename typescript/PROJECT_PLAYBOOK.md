# Project Playbook

Use this process for every future task in this curriculum.

## 1. Start with a project brief

Before coding, record:

- user/problem statement;
- must-have behavior and explicit non-goals;
- current stage and new concepts (normally three to five);
- acceptance criteria visible to a user;
- quality gates;
- what will be supplied versus decided independently.

The project should be small enough to finish but large enough that the target concepts are necessary. Avoid adding features only to touch more syntax.

## 2. Use just-in-time learning

For each new concept:

1. Explain the minimum mental model.
2. Show one small example or failing case.
3. Apply it immediately in the project.
4. Ask the learner to explain or modify it.
5. Revisit it in a later project without the recipe.

Keep a `LEARNING_NOTES.md` inside each project containing decisions, mistakes, and concise explanations—not copied documentation.

## 3. Build in vertical slices

Prefer an end-to-end thin feature over completing all types, then all UI, then all API code.

Example slices:

1. Display one hard-coded valid item.
2. Render a typed list.
3. Add one user action.
4. Persist or fetch it.
5. Handle invalid, loading, empty, and failure cases.
6. Add tests and accessibility polish.

Commit at working checkpoints when the repository workflow calls for commits.

## 4. Separate the learning roles

For early projects, Codex may provide scaffolding and small guided steps. It should not silently complete the entire project. The learner should type or direct the key implementation, predict results, and explain errors.

As stages advance:

- reduce implementation hints;
- provide product requirements and API contracts rather than file structures;
- require the learner to propose types, state ownership, module boundaries, and tests first;
- review decisions with tradeoffs rather than compare against one hidden “correct” architecture.

## 5. Use a fixed feedback loop

Every project cycles through:

1. **Plan:** requirements, data model, states, risks.
2. **Implement:** smallest vertical slice.
3. **Verify:** type-check, tests, build, and manual behavior.
4. **Review:** correctness, clarity, accessibility, API resilience, and architecture appropriate to the stage.
5. **Refactor:** only problems observed in the review.
6. **Reflect:** what was learned, what remains weak, and one change to make without guidance.

## 6. Definition of done

A project is complete when:

- its acceptance criteria work;
- strict type-check passes with no unexplained `any` or unsafe assertions;
- formatting, lint, relevant tests, and production build pass;
- loading, error, empty, and success states exist where applicable;
- keyboard/accessibility and responsive behavior match the stage;
- configuration contains no secrets or hard-coded production endpoints;
- the learner can explain the main data flow and at least two design choices;
- `LEARNING_NOTES.md` records mistakes and next steps;
- the stage exit gate is demonstrated.

Early stages can use a smaller subset of the gates, but type-checking and explanation are never skipped.

## 7. Assistance levels

- **Guided:** exact milestones, hints, and brief examples; learner writes the solution.
- **Coached:** acceptance criteria and checkpoints; hints only after an attempt or when blocked.
- **Independent:** product brief and constraints; learner proposes and builds; Codex acts as reviewer.
- **Professional simulation:** ambiguous requirements, API changes, bug reports, and review feedback; learner owns decisions and delivery.

## 8. When stuck

Use this escalation ladder:

1. Read the compiler/runtime error carefully and state what it says.
2. Inspect the smallest relevant value with DevTools or a focused test.
3. Form a hypothesis and make one change.
4. Consult the relevant official documentation.
5. Ask for a conceptual hint.
6. Ask for a localized example.
7. Request a direct fix only after recording why previous attempts failed.

This preserves momentum without turning the project into tutorial transcription.

## 9. Project folder convention

Use numbered, self-contained folders:

```text
01-expense-analyzer/
02-browser-converter/
03-local-task-tracker/
...
```

Each should normally contain:

```text
README.md            # brief, acceptance criteria, setup
LEARNING_NOTES.md    # decisions, mistakes, explanations
src/
tests/               # or colocated tests as the tool expects
package.json
tsconfig.json
```

Later projects may add `docs/api-contract.md`, generated API types, E2E tests, and deployment configuration. Do not centralize dependencies or create a monorepo until multiple completed projects prove that it would help.

## 10. Recommended first task

Treat the existing `hello-world` folder as a syntax scratchpad, not as a portfolio project. The first real task should be **Stage 1: Personal expense analyzer** in guided mode.

Its initial milestone is intentionally small: define five example transactions, calculate a total without `any`, and write one passing test. Later milestones add category summaries, input validation, error cases, and report formatting.


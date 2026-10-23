---
sessionId: session-261024-011210-qhcp
---

# Requirements

### Overview & Goals
The objective is to eliminate redundant inline property declarations across unit tests in `src/components/prefab/add_object/AddObject.spec.ts`. Extracting reusable fixture data and a mount helper maximizes developer productivity, reduces cognitive load, minimizes test maintenance overhead, and ensures consistent test setup.

### Scope
- **In Scope**:
  - Extracting default test props (`label: "Test Label"`, `options: [{ label: "Option 1", value: "1" }]`) into a centralized constant / factory helper.
  - Refactoring existing test cases in `AddObject.spec.ts` to consume the extracted fixture and mount helper.
- **Out of Scope**:
  - Modifying the production component implementation in `AddObject.vue`.
  - Altering test assertions or test behavior.

### User Stories
- As a developer maintaining `AddObject.spec.ts`, I want a unified way to instantiate the component with sensible default props so that tests remain concise, readable, and easy to maintain when component contracts evolve.

### Functional Requirements
- Define a default props fixture `DEFAULT_PROPS` for standard `AddObject` test scenarios.
- Provide a `mountAddObject` helper function that accepts optional prop overrides and merges them cleanly with defaults.
- Retain exact test semantics and behavior across all existing Vitest test cases.

### Non-Functional Requirements
- Maintain complete type safety using TypeScript.
- Ensure zero execution overhead and full test execution consistency across Vitest runs.

# Technical Design

### Current Implementation
In `src/components/prefab/add_object/AddObject.spec.ts`, multiple test cases duplicate identical inline prop definitions:
```typescript
props: {
  label: "Test Label",
  options: [{ label: "Option 1", value: "1" }],
}
```
This repetition adds friction to test updates and obscures the specific variables under test in each case.

### Key Decisions
- **Introduce `DEFAULT_PROPS` Constant & `mountAddObject` Factory**: Consolidating setup logic into a lightweight helper yields the greatest reduction in boilerplate and maximizes clarity by allowing each test case to specify only what makes it unique.

### Proposed Changes
- In `src/components/prefab/add_object/AddObject.spec.ts`:
  - Declare `DEFAULT_PROPS`:
    ```typescript
    const DEFAULT_PROPS = {
      label: "Test Label",
      options: [{ label: "Option 1", value: "1" }],
    };
    ```
  - Define `mountAddObject(props = {}, options = {})`:
    ```typescript
    function mountAddObject(props: Partial<typeof DEFAULT_PROPS> = {}, options = {}) {
      return mount(AddObject, {
        props: {
          ...DEFAULT_PROPS,
          ...props,
        },
        ...options,
      });
    }
    ```
  - Update all individual tests (`renders label correctly`, `renders options correctly`, `select is disabled when options are empty`, `select is not disabled when options are present`, `emits update:modelValue on change`, `calls showPicker on focus...`, `does not call showPicker on focus...`) to use `mountAddObject`.

### Risks
- **Risk**: Overwriting nested array properties during merge (e.g., custom `options` arrays).
  - *Mitigation*: Shallow property overriding (`...DEFAULT_PROPS, ...props`) cleanly replaces the entire `options` array when custom options are supplied.

# Testing

### Validation Approach
Verify that refactoring `src/components/prefab/add_object/AddObject.spec.ts` preserves existing test coverage and passes all assertions cleanly.

### Key Scenarios
- Component mounts with default props and renders label text `+Test Label`.
- Overriding options with empty array verifies disabled select behavior.
- Overriding options with multi-element array verifies option list rendering and value emission.
- Focus events trigger `showPicker` based on user activation state.

### Test Changes
- Update `src/components/prefab/add_object/AddObject.spec.ts` test suite to use the helper.
- Run `npm run test` or Vitest runner targeting `AddObject.spec.ts`.

# Delivery Steps

### ✓ Step 1: Extract Default Test Props and Mount Factory Helper
A reusable props constant and mount helper function are defined in `src/components/prefab/add_object/AddObject.spec.ts`.

- Extract `DEFAULT_PROPS` containing default `label` and `options` fixtures.
- Define a `mountAddObject(props = {}, options = {})` helper function that wraps `mount(AddObject, ...)` and merges custom props with `DEFAULT_PROPS`.
- Ensure clean type safety and proper integration with existing Pinia setup.

### ✓ Step 2: Refactor Test Cases and Verify Suite
All unit tests in `src/components/prefab/add_object/AddObject.spec.ts` use the centralized helper and execute without regressions.

- Replace duplicated inline `mount(AddObject, { props: { ... } })` calls across all test cases with `mountAddObject(...)`.
- Simplify specific test overrides (e.g., empty options, custom option lists) by passing only the relevant differential props.
- Run Vitest suite for `AddObject.spec.ts` to confirm all assertions continue to pass seamlessly.
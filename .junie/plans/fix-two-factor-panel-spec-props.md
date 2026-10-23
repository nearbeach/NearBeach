---
sessionId: session-261023-235150-16br
---

# Requirements

### Overview & Goals
Resolve Vue prop warnings and test failures in `src/components/login/login_page/two_factor_panel/TwoFactorPanel.spec.ts` by supplying required model props and valid enum values when mounting `TwoFactorPanel`.

### Scope
- **In Scope**:
  - Updating test setup in `src/components/login/login_page/two_factor_panel/TwoFactorPanel.spec.ts` to mock required `otpToken` and valid `buttonState` props.
  - Using `ObjectStateEnum` rather than raw arbitrary strings for `buttonState`.
  - Ensuring test assertions align with actual component behavior and i18n configurations.
- **Out of Scope**:
  - Modifying other unrelated login components or global test configurations.

### Functional Requirements
- `TwoFactorPanel` must receive the required `otpToken` prop when mounted in tests.
- `buttonState` must be passed valid `ObjectStateEnum` values (`ObjectStateEnum.NoAction`, `ObjectStateEnum.Disable`, etc.) satisfying the custom prop validator.
- Prop validation warnings must no longer appear during test execution.

# Technical Design

### Current Implementation
- `src/components/login/login_page/two_factor_panel/TwoFactorPanel.vue` defines:
  - `otpToken` as a required model via `defineModel("otpToken", { type: String, required: true })`.
  - `buttonState` with a custom validator checking membership against `Object.values(ObjectStateEnum)`.
- `src/components/login/login_page/two_factor_panel/TwoFactorPanel.spec.ts` currently mounts `TwoFactorPanel` with `props: { buttonState: "enabled" }` or `"disabled"`, omitting `otpToken` and supplying strings that fail the `ObjectStateEnum` validator.

### Key Decisions
- **Decision**: Import and use `ObjectStateEnum` directly in unit tests instead of magic strings.
  - *Rationale*: Eliminates validator check failures, reflects actual runtime usage in `LoginPage.vue`, and ensures compiler-level type safety.
- **Decision**: Supply a default string (e.g., `""`) for `otpToken` across all test mount options.
  - *Rationale*: Fulfills the `required: true` constraint of `defineModel("otpToken")`, suppressing Vue missing prop warnings.

### Proposed Changes
- In `src/components/login/login_page/two_factor_panel/TwoFactorPanel.spec.ts`:
  - Import `ObjectStateEnum` from `@/utils/enums/ObjectStateEnum`.
  - Update test helper / mount calls with `otpToken: ""` and `buttonState: ObjectStateEnum.NoAction` (or `ObjectStateEnum.Disable` for disabled states).
  - Verify related assertions match rendered elements and i18n outputs.

# Testing

### Validation Approach
Run the unit test suite via `vitest` for `TwoFactorPanel.spec.ts` and ensure zero console warnings and passing assertions.

### Key Scenarios
- **Valid Props Execution**: Mounting with `buttonState: ObjectStateEnum.NoAction` and `otpToken: ""` produces no Vue prop warnings.
- **Disabled Button State**: Mounting with `buttonState: ObjectStateEnum.Disable` renders the button with the disabled attribute.
- **Form Interaction & Events**: Emitting `signIn` and validating input triggers expected events without prop validation errors.

# Delivery Steps

### ✓ Step 1: Update prop mocking and enum types in TwoFactorPanel.spec.ts
`TwoFactorPanel.spec.ts` passes valid props to `TwoFactorPanel` matching component contracts and schema definitions.

- Import `ObjectStateEnum` from `@/utils/enums/ObjectStateEnum` into `src/components/login/login_page/two_factor_panel/TwoFactorPanel.spec.ts`.
- Update all `mount` calls in `TwoFactorPanel.spec.ts` to provide the required `otpToken` prop (e.g. `otpToken: ""`).
- Replace invalid string values (`"enabled"` and `"disabled"`) with valid `ObjectStateEnum` values (`ObjectStateEnum.NoAction` and `ObjectStateEnum.Disable`).

### ✓ Step 2: Align test assertions and verify test suite execution
All unit tests in `TwoFactorPanel.spec.ts` pass cleanly without Vue runtime prop warnings.

- Align component assertions with rendered DOM output and translation strings.
- Execute unit test suite using `vitest` to ensure zero prop validation errors or test failures.
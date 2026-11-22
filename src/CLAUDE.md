# Frontend (src/) conventions

See `/Architecture.md` section 4. Stack: Vue 3, TypeScript, Pinia, vue-router, petite-vue-i18n, Vite.

- **Components:** one folder per component: `Name.vue`, `Name.spec.ts`, `index.ts` barrel. Group by feature under `components/<feature>/`; shared pieces in `components/object_components/` and `components/prefab/`. Use `<script setup lang="ts">`.
- **State:** Pinia stores in `stores/` (user, permissions, object, nav, search, error, ...). Prefer a store over prop-drilling for cross-feature state.
- **HTTP:** use `composables/safeFetch` (handles CSRF via `getCsrfToken`); never raw `fetch` for state-changing calls. Backend is `/api/v1/...`. Permissions come from the backend; UI hiding is cosmetic.
- **i18n:** no hard-coded user-visible strings. Add keys to `locales/en.json` and `locales/ja.json`; `locales.spec.ts` fails if they drift.
- **Accessibility:** keep skip links, labels, focus order and contrast (`styles/_accessibility.css`); `e2e/test_accessibility.py` runs axe.
- **Styles:** PostCSS nesting; CSS variables in `styles/variables/_general_variables.css`, custom media in `_media_variables.css`.
- **Checks before finishing:** `npm run type-check`, `npm run lint`, `npm run test:unit`, `npm run format`.
- **Dev:** `npm run dev` (Vite :5173) alongside Django :8000. Output of `npm run build` goes to `NearBeach/static/NearBeach/`.

## Writing unit tests (Vitest)
Run `npm run test:unit` (watch mode) or `npx vitest run <path>` for one file. The only config is `vitest.config.ts`: it merges `vite.config.ts` (so the `@/` alias and the Vue plugin work), runs in Chromium via Playwright browser mode, and sets `environment: 'jsdom'`. Playwright browsers must be installed (`npx playwright install chromium`). `e2e/**` is excluded: that is the separate Python Playwright suite.

**Where:** the spec sits beside the file it tests, named `Name.spec.ts` (`safeFetch.spec.ts`, `error.spec.ts`). Nothing lives in a root `tests/` folder.

**Tooling:** `vitest` (`describe`, `test`, `expect`, `vi`) + `@vue/test-utils` (`mount`, `flushPromises`). Use these; `vitest-browser-vue` and `@pinia/testing` are installed but unused, so don't introduce them without reason. Import from `"vitest"` explicitly (no globals).

**Canonical examples, read one before writing:**
- Component with form, fetch and router: `components/organisation/new_organisation/NewOrganisation.spec.ts`
- Component that loads paged data into a store: `components/object_components/audit/AuditComponent.spec.ts`
- Pinia store: `stores/error/error.spec.ts`
- Composable: `composables/safeFetch.spec.ts`

**Recipe**
- **Pinia:** `beforeEach(() => setActivePinia(createPinia()))` for stores. For components, call it too, then read state with `useXStore()`.
- **i18n:** mount with `global: { plugins: [i18n] }` where `i18n` is `@/i18n.ts`. Assert on the English text from `locales/en.json`.
- **HTTP:** components call `safeFetch`, which wraps `fetch`, so mock `fetch`: `vi.spyOn(globalThis, "fetch").mockResolvedValue({ status, statusText, json: () => Promise.resolve(body) } as Response)`. Assert on `mock.calls[0][0]` (URL) and `[1].method` / `JSON.parse([1].body)`. Never hit a real server. `vi.restoreAllMocks()` in `afterEach`.
- **Router:** mock it, don't create one: `const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }))` then `vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }))`. Assert on `pushMock` calls.
- **Async:** `await flushPromises()` after a click that triggers a fetch; `await wrapper.vm.$nextTick()` after emitting events.
- **`whelk-ui` components** (`WlkButton`, `WlkTextInput`, ...): find them with `wrapper.findAllComponents(WlkTextInput)` and drive them with `vm.$emit("update:modelValue", v)` and `vm.$emit("change", { isValid })`, as `NewOrganisation.spec.ts` does, instead of typing into the DOM.
- **Status handling:** every call a component makes should be tested for success plus the failure branches it handles (typically 403 -> `{ name: "forbidden" }`, other errors -> error store message + `server-error`). Match whatever the component switches on.

**What a spec should cover:** initial render, each user interaction, success, each handled error status, and disabled/empty/loading states. Test behaviour (text, emitted events, store state, fetch calls), not implementation details. A new store or composable needs its own spec. New locale keys need no spec (`locales.spec.ts` checks `en.json`/`ja.json` parity).

**Style:** match the neighbouring spec's indentation (the repo is mixed tabs/2-space), run `npm run format`, `npm run lint` and `npm run type-check` before finishing. Test titles are plain sentences ("a 403 redirects to the forbidden page").

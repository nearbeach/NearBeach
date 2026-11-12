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

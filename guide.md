Separation of Concerns, Single Source of Truth, Unidirectional Data Flow, Prop Drilling, State Mutation, Derived State, Reactive Coupling, Side Effects, Composable Extraction, Reactivity Leaks, Watcher Abuse, Memory Leaks, Template Bloat, Type Safety, God Component, Presentational Components, Container Components, High Cohesion, Low Coupling, Composition over Inheritance, Immutability, Dependency Injection, Inversion of Control, Event-Driven Architecture, State Machines, Optimistic UI, Race Conditions, Idempotency, Caching Strategy, Stale-While-Revalidate, Code Splitting, Lazy Loading, Tree Shaking, Bundle Bloat, Render Bottlenecks, Virtual Scrolling, Debouncing, Throttling, Error Boundaries, Graceful Degradation, Defensive Programming, Strict Typing, Interface Segregation, Technical Debt, Refactoring, Modularity, Scalability, Maintainability, Abstraction Layers, Lifecycle Management. 

DOM & Render Optimization: Virtual Scrolling, Memoization (v-memo), Render Caching (v-once), Layout Thrashing Prevention, Reflow Elimination, Animations & Visual Smoothness: GPU Compositing (transform, opacity), 60fps Frame Budget, Hardware Acceleration, CSS Containment (contain: content), Network & Perceived Speed: Optimistic UI, Stale-While-Revalidate (SWR), Skeleton Screens, Progressive Hydration, Prefetching, Bundle & Execution Speed: Code Splitting, Lazy Loading, Web Workers (Off-Main-Thread Execution), Debouncing, Throttling
Act as a Senior Frontend Performance Engineer. Audit src/ and optimize UI speed and rendering using these principles: DOM & Render Optimization: Virtual Scrolling, Memoization (v-memo), Render Caching (v-once), Layout Thrashing Prevention, Reflow Elimination, Animations & Visual Smoothness: GPU Compositing (transform, opacity), 60fps Frame Budget, Hardware Acceleration, CSS Containment (contain: content), Network & Perceived Speed: Optimistic UI, Stale-While-Revalidate (SWR), Skeleton Screens, Progressive Hydration, Prefetching, Bundle & Execution Speed: Code Splitting, Lazy Loading, Web Workers (Off-Main-Thread Execution), Debouncing, Throttling. Do not edit files yet—list the top 5 bottlenecks found and propose your refactoring plan first. \

Vuejs frontend optimization keywords:
Frontend Optimization
Code splitting, lazy loading routes, defineAsyncComponent, v-once, v-memo, shallowRef, shallowReactive, computed caching, virtual scrolling, KeepAlive, tree-shaking, image optimization, WebP/AVIF formats, Vite bundle analyzer, brotli/gzip compression, debouncing/throttling, SSR/SSG (Nuxt), asset preloading, CSS purging, avoiding deep watchers 

Code Splitting: Breaking your JavaScript bundle into smaller chunks so users only download the code needed for the current page.
Lazy Loading Routes: Configuring Vue Router with dynamic import() statements so route components load only when a user navigates to them.
defineAsyncComponent: Loading heavy or rarely used components (like modals or charts) asynchronously on demand instead of at initial page load.
v-once: Rendering an element or component once and skipping all future re-renders, even if reactive data changes.
v-memo: Caching a sub-tree of a template and re-rendering it only when specific dependency values change.
shallowRef: Tracking reactivity only on .value replacement rather than deeply watching every nested property inside large objects.
shallowReactive: Making only the root-level properties of an object reactive to avoid the performance cost of deep proxy conversion.
computed Caching: Storing derived data so Vue recalculates it only when its reactive dependencies change, unlike methods that run on every render.
Virtual Scrolling: Rendering only the visible items in a massive list (using libraries like vue-virtual-scroller) instead of thousands of DOM nodes at once.
KeepAlive: Caching inactive component instances in memory when switching tabs or routes so their state is preserved without re-rendering.
Tree-Shaking: Automatically removing unused exports and dead code during the production build process.
Image Optimization: Resizing, compressing, and lazy-loading images (loading="lazy") to reduce network payload and speed up page paint.
WebP/AVIF Formats: Serving modern image formats that offer significantly smaller file sizes than JPEG or PNG at the same visual quality.
Vite Bundle Analyzer: Visualizing your final build output (e.g., with rollup-plugin-visualizer) to spot oversized third-party libraries.
Brotli/Gzip Compression: Compressing static text assets (JS, CSS, HTML) on the server or CDN so files transfer faster over the network.
Debouncing/Throttling: Limiting how frequently expensive functions (like search API calls or scroll listeners) fire during rapid user input.
SSR/SSG (Nuxt): Rendering pages on the server or at build time so users see immediate HTML content and search engines can index pages easily.
Asset Preloading: Using <link rel="preload"> or <link rel="prefetch"> hints to fetch critical fonts, scripts, or next-page assets early.
CSS Purging: Stripping unused CSS selectors from production stylesheets (built into tools like Tailwind CSS) to minimize stylesheet size.
Avoiding Deep Watchers: Preventing performance bottlenecks by watching specific properties instead of using deep: true on large nested structures.
Do not put all 20 optimizations into a single prompt. Sending them all at once forces OpenCode to read your entire codebase in one massive context window, wastes tokens on redundant file reads, and leads to rushed, superficial edits.
Instead, use 4 focused, sequential phases (4 prompts) grouped by architecture layer. This keeps OpenCode's file context tight per session, gives you clean git checkpoints after each step, and drastically lowers token consumption.

Why 4 Phases Minimizes Tokens
Scoped file reads: Each prompt targets only specific files (router/, vite.config, specific heavy components) instead of scanning the whole repo repeatedly.
Start fresh per phase: Run /new or /clear in OpenCode between phases so previous conversation history doesn't inflate token costs.
Measurable progress: You can audit bundle size and Lighthouse scores after each phase.

Phase 1: Bundle, Build & Route Splitting (Biggest Impact, Lowest Token Cost)
Targets: Code splitting, lazy loading routes, Vite bundle analyzer, tree-shaking, CSS purging, Brotli/Gzip, asset preloading.
Prompt 1:
"Analyze package.json, vite.config.*, index.html, and the router configuration (src/router/*). Do not scan unrelated component files yet.
Convert static route imports to dynamic import() lazy-loaded routes for code splitting.
Configure Vite (vite.config.*) for optimal manual chunk splitting, tree-shaking, CSS purging/minification, and Brotli/Gzip compression (vite-plugin-compression), plus add rollup-plugin-visualizer for bundle analysis.
Add critical font/asset <link rel="preload"> hints in index.html.
Apply these changes directly and summarize the updated files."

Phase 2: Heavy Component & List Rendering
Targets: defineAsyncComponent, KeepAlive, virtual scrolling, v-once, v-memo.
Prompt 2:
"Identify the heaviest UI views, modals, and large list/table components in src/views and src/components (skip small UI primitives like buttons/inputs).
Wrap heavy conditional components (modals, charts, drawers) with defineAsyncComponent.
Wrap dynamic tab/route views that benefit from state preservation in <KeepAlive> with an explicit max prop.
Replace large rendered lists (100+ items) with virtual scrolling, and apply v-once on static blocks or v-memo on expensive list items where appropriate.
List the files you modified and why."

Phase 3: Reactivity & Event Optimization
Targets: shallowRef, shallowReactive, computed caching, avoiding deep watchers, debouncing/throttling.
Prompt 3:
"Audit Vue <script setup> blocks and Pinia stores (src/stores/*) specifically for reactivity and event bottlenecks.
Replace ref/reactive with shallowRef/shallowReactive for large read-only datasets or third-party instances.
Convert expensive template function calls into cached computed properties.
Replace any watch(..., { deep: true }) with targeted property watchers.
Add debouncing or throttling to rapid search inputs, resize, or scroll handlers.
Make minimal, safe edits and list each optimized file."

Phase 4: Media & Rendering Architecture Audit
Targets: Image optimization, WebP/AVIF formats, SSR/SSG (Nuxt) evaluation.
Prompt 4:
"Scan templates and public/ / src/assets/ for image usage and check if this project requires SSR/SSG.
Add loading="lazy", decoding="async", and explicit width/height attributes to below-the-fold <img> tags, and update image pipelines/references to prefer WebP/AVIF formats.
Based on our current setup, briefly advise whether migrating to Nuxt (SSR/SSG) or keeping Vite SPA with prerendering (vite-plugin-ssr / vite-ssg) makes sense for SEO and First Contentful Paint—do not migrate frameworks automatically."

Token-Saving Tips When Running These in OpenCode
Clear context between prompts: Run /clear (or start a new session) before pasting the next prompt.
Commit between phases: Run git commit after each phase so you can easily revert if a shallowRef or v-memo breaks reactivity.
Pin specific folders: If your repo is large, mention exact folder paths (e.g., @src/views/Dashboard.vue) in Phase 2 and Phase 3 so OpenCode doesn't search the whole directory tree.
.opencode/
└── skills/
    ├── vue-opt-1-bundle/
    │   └── SKILL.md
    ├── vue-opt-2-rendering/
    │   └── SKILL.md
    ├── vue-opt-3-reactivity/
    │   └── SKILL.md
    └── vue-opt-4-media-ssr/
        └── SKILL.md


---
name: vue-opt-1-bundle
description: Phase 1 Vue optimization for route code-splitting, Vite bundling, tree-shaking, compression, CSS purging, and asset preloading.
---

# Phase 1: Bundle, Build & Route Splitting

## Context Scope (Token Guardrail)
- **ONLY inspect:** `package.json`, `vite.config.*`, `index.html`, CSS entry files, and router files (`src/router/*`).
- **DO NOT** read unrelated Vue components, stores, or utility files during this phase.

## Tasks
1. **Lazy Loading Routes & Code Splitting**: Convert static route component imports in `src/router/*` to dynamic `() => import(...)` imports.
2. **Vite Build Optimization (`vite.config.*`)**:
   - Configure `build.rollupOptions.output.manualChunks` to separate heavy vendor libraries (e.g., `vue`, `vue-router`, `pinia`, chart/UI libs).
   - Ensure tree-shaking and CSS minification/purging are active.
   - Add `rollup-plugin-visualizer` (configured to output `stats.html` on build) and `vite-plugin-compression` for Brotli/Gzip if not already present (install via package manager or list exact install command if lockfile changes are restricted).
3. **Asset Preloading**: Add `<link rel="preload">` tags in `index.html` for critical above-the-fold fonts or entry assets.

## Output Rules
- Apply changes directly to the targeted config/router files.
- Provide a concise bulleted summary of modified files and any newly added devDependencies.


---
name: vue-opt-2-rendering
description: Phase 2 Vue optimization for async components, KeepAlive, virtual scrolling, v-once, and v-memo.
---

# Phase 2: Heavy Component & List Rendering

## Context Scope (Token Guardrail)
- **ONLY inspect:** Page views (`src/views/*`, `src/pages/*`) and complex feature components (modals, charts, tables, large lists).
- **SKIP:** Small atomic UI primitives (buttons, badges, icons, basic inputs).

## Tasks
1. **Async Components**: Wrap heavy conditional components (modals, drawers, rich editors, charts) with `defineAsyncComponent(() => import(...))`.
2. **Component Caching**: Wrap dynamic route views or multi-tab switchers that benefit from state preservation in `<KeepAlive :max="5">` (adjust `max` reasonably).
3. **Large Lists & Virtual Scrolling**: Identify `v-for` loops rendering 100+ items or complex rows. Recommend or implement virtual scrolling (e.g., `@tanstack/vue-virtual` or `vue-virtual-scroller`) where appropriate.
4. **Template Memoization**:
   - Add `v-once` to purely static template blocks that never update after initial render.
   - Add `v-memo="[...]"` to expensive `v-for` items where updates depend only on specific primitive keys (e.g., `item.id`, `item.selected`).

## Output Rules
- Make targeted, safe edits without altering business logic.
- List each modified file and the specific directive/optimization applied.

---
name: vue-opt-3-reactivity
description: Phase 3 Vue optimization for shallowRef, shallowReactive, computed caching, watcher cleanup, and debouncing/throttling.
---

# Phase 3: Reactivity & Event Optimization

## Context Scope (Token Guardrail)
- **ONLY inspect:** `<script setup>` blocks, composables (`src/composables/*`), and state stores (`src/stores/*`).
- **SKIP:** Purely presentational templates and static CSS files.

## Tasks
1. **Shallow Reactivity**: Replace `ref()` or `reactive()` with `shallowRef()` or `shallowReactive()` for large read-only API arrays, chart/map instances, or objects replaced immutably.
2. **Computed Caching**: Move expensive filtering, sorting, or formatting function calls out of `<template>` expressions and into cached `computed()` properties.
3. **Eliminate Deep Watchers**: Find all `watch(..., { deep: true })` and `watchEffect` calls; replace deep watchers with explicit getter functions watching only the required nested properties.
4. **Debounce & Throttle**: Add debouncing (e.g., 300ms) to search/filter input handlers and throttling to `scroll` or `resize` event listeners (using existing utilities like `@vueuse/core` if installed, or a lightweight helper).

## Output Rules
- Ensure `.value` reassignment is preserved wherever `shallowRef` is introduced so reactivity does not break.
- Summarize every changed file and why the reactivity/event change improves runtime performance.


---
name: vue-opt-4-media-ssr
description: Phase 4 Vue optimization for lazy images, WebP/AVIF formats, and SSR/SSG architecture evaluation.
---

# Phase 4: Media & Rendering Architecture Audit

## Context Scope (Token Guardrail)
- **ONLY inspect:** Templates containing `<img>` or `<picture>` tags, `public/`, `src/assets/`, and `package.json`.
- **DO NOT** modify application state, routing logic, or build plugins during this phase.

## Tasks
1. **Image Attributes**: For all below-the-fold `<img>` elements, add `loading="lazy"`, `decoding="async"`, and explicit `width` and `height` attributes to prevent Cumulative Layout Shift (CLS). Keep hero/LCP images eager (`fetchpriority="high"`).
2. **Modern Formats (WebP/AVIF)**: Identify oversized `.png`/`.jpg` assets in `src/assets/` or `public/` and update image references or `<picture>` fallbacks to prefer `.avif`/`.webp` where available (or suggest `vite-imagetools` for automated build-time conversion).
3. **SSR/SSG Evaluation (Read-Only Advice)**: Inspect routing and data-fetching patterns to evaluate whether this app needs SSR/SSG (Nuxt or `vite-ssg`) for SEO/FCP, or if keeping a standard Vite SPA is optimal. **Do not migrate frameworks.**

## Output Rules
- Apply safe image attribute optimizations directly.
- End with a short 3–4 bullet architectural recommendation on SSR/SSG vs. SPA for this specific repo.


Scaling up
Feature-Sliced Design (FSD), modular domain architecture, Pinia modular stores, composables extraction, TypeScript strict mode, repository/service API layer, TanStack Query (Vue Query), Micro-Frontends (Module Federation), shared component library, design tokens, route-level permissions/RBAC, Web Workers, CI/CD automated testing, bundle budgets, error boundaries (onErrorCaptured), observability/Sentry

Phase 1: Architecture & State Scaling
Targets: Feature-Sliced Design (FSD), modular domain architecture, Pinia modular stores, composables extraction, TypeScript strict mode.
Goal: Break monolithic folders (components/, views/, stores/) into isolated, domain-driven feature modules so multiple developers can work without merge conflicts or tight coupling.
OpenCode Focus: Refactor folder structure by feature/domain, extract reusable logic out of giant .vue files into use* composables, split monolithic Pinia stores into small domain stores, and enforce strict: true in tsconfig.json.
Phase 2: Data Layer & Network Resilience
Targets: Repository/service API layer, TanStack Query (Vue Query), Web Workers, error boundaries (onErrorCaptured).
Goal: Decouple HTTP calls from UI components and handle caching, background refetching, heavy client compute, and graceful UI crashes at scale.
OpenCode Focus: Centralize raw fetch/axios calls into typed API service repositories, introduce TanStack Query for server-state caching and deduplication, offload heavy data parsing/filtering to Web Workers, and wrap feature modules in onErrorCaptured error boundaries.
Phase 3: Enterprise Governance, Multi-Team & Delivery
Targets: Shared component library, design tokens, route-level permissions/RBAC, Micro-Frontends (Module Federation), CI/CD automated testing, bundle budgets, observability/Sentry.
Goal: Standardize UI across teams, enforce security and performance guardrails automatically before deployment, and monitor production health.
OpenCode Focus: Consolidate base UI primitives with CSS design tokens, implement scalable meta-driven RBAC route guards, configure Vite bundle size budgets + Vitest/Playwright CI pipelines, integrate Sentry/observability hooks, and evaluate Module Federation if splitting across independent teams.

Frontend Security
XSS prevention, v-html sanitization (DOMPurify), Content Security Policy (CSP), CSRF protection, HttpOnly Secure cookies, short-lived JWTs/refresh rotation, route-level RBAC guards, client-side input validation (Zod/VeeValidate), Subresource Integrity (SRI), dependency vulnerability auditing (npm audit), environment variable hygiene (VITE_* exposure), HTTPS/HSTS enforcement, clickjacking protection (X-Frame-Options / frame-ancestors), rate-limiting/CAPTCHA on auth forms, sensitive data redaction in logs/storage 


Phase 1: XSS, Injection & Client Storage Hardening
Targets: XSS prevention, v-html sanitization (DOMPurify), client-side input validation (Zod/VeeValidate), environment variable hygiene (VITE_* exposure), sensitive data redaction in logs/storage.
Goal: Eliminate client-side injection vectors and stop sensitive secrets or tokens from leaking through localStorage, browser logs, or bundled environment variables.
OpenCode Focus: Audit every v-html and dynamic :href binding (sanitize with DOMPurify and block javascript: URLs), enforce schema validation (Zod/VeeValidate) on user forms, scrub secret keys from VITE_* env vars, and remove raw tokens/PII from localStorage and console.log.
Phase 2: Auth, Headers, Transport & Supply-Chain Security
Targets: HttpOnly Secure cookies, short-lived JWTs/refresh rotation, CSRF protection, route-level RBAC guards, Content Security Policy (CSP), clickjacking protection (X-Frame-Options / frame-ancestors), Subresource Integrity (SRI), HTTPS/HSTS enforcement, rate-limiting/CAPTCHA on auth forms, dependency vulnerability auditing (npm audit).
Goal: Lock down authentication flows, browser security headers, route access control, and third-party dependencies.
OpenCode Focus: Migrate token handling toward HttpOnly/Secure/SameSite cookie patterns with CSRF headers, harden Vue Router beforeEach RBAC guards (never relying on UI hiding alone), configure strict CSP and frame-ancestors headers in index.html/server config, add SRI hashes to external scripts, and run npm audit / lockfile checks.
Folder Structure
.opencode/skills/
1-opt-1-bundle/SKILL.md
1-opt-2-rendering/SKILL.md
1-opt-3-reactivity/SKILL.md
1-opt-4-media-ssr/SKILL.md
2-scale-1-architecture/SKILL.md
2-scale-2-data-layer/SKILL.md
2-scale-3-governance/SKILL.md
3-sec-1-xss-storage/SKILL.md
3-sec-2-auth-headers/SKILL.md

1. Frontend Optimization (4 Phases)
Skill 1: 1-opt-1-bundle (Bundle, Build & Route Splitting)
Files to inspect: package.json, vite.config.*, index.html, CSS entry files, and src/router/* (skip all components and stores).
Tasks:
Convert static route component imports in src/router/* to dynamic () => import(...) imports for code splitting.
Configure build.rollupOptions.output.manualChunks in vite.config.* to separate heavy vendor libraries (vue, vue-router, pinia, chart/UI libs).
Ensure tree-shaking and CSS minification/purging are active, and add rollup-plugin-visualizer (stats.html) plus vite-plugin-compression for Brotli/Gzip.
Add <link rel="preload"> tags in index.html for critical above-the-fold fonts or entry assets.
Skill 2: 1-opt-2-rendering (Heavy Component & List Rendering)
Files to inspect: Page views (src/views/*, src/pages/*) and complex feature components like modals, charts, tables, and large lists (skip small UI primitives like buttons and inputs).
Tasks:
Wrap heavy conditional components (modals, drawers, rich editors, charts) with defineAsyncComponent(() => import(...)).
Wrap dynamic route views or multi-tab switchers needing state preservation in <KeepAlive :max="5">.
Replace large v-for loops (100+ items or complex rows) with virtual scrolling (@tanstack/vue-virtual or vue-virtual-scroller).
Add v-once to purely static template blocks and v-memo="[...]" to expensive v-for items that depend only on specific primitive keys.
Skill 3: 1-opt-3-reactivity (Reactivity & Event Optimization)
Files to inspect: <script setup> blocks, src/composables/*, and src/stores/* (skip static templates and CSS).
Tasks:
Replace ref() or reactive() with shallowRef() or shallowReactive() for large read-only API arrays, chart/map instances, or objects replaced immutably.
Move expensive filtering, sorting, or formatting function calls out of <template> expressions into cached computed() properties.
Replace watch(..., { deep: true }) with explicit getter functions watching only required nested properties.
Add debouncing (~300ms) to search/filter input handlers and throttling to scroll or resize event listeners.
Skill 4: 1-opt-4-media-ssr (Media & Rendering Architecture Audit)
Files to inspect: Templates with <img> or <picture> tags, public/, src/assets/, and package.json (do not modify state, routing, or build plugins).
Tasks:
Add loading="lazy", decoding="async", and explicit width and height attributes to below-the-fold <img> tags; keep hero/LCP images eager with fetchpriority="high".
Identify oversized .png/.jpg assets and update references or <picture> fallbacks to prefer .avif/.webp (or recommend vite-imagetools).
Audit routing and data-fetching patterns to advise whether SSR/SSG (Nuxt or vite-ssg) is needed for SEO/FCP or if keeping a Vite SPA is best (without migrating frameworks).

2. Scaling Up (3 Phases)
Skill 5: 2-scale-1-architecture (Architecture & State Scaling)
Files to inspect: src/* directory layout, tsconfig*.json, src/stores/*, and bloated .vue files (>300 lines).
Tasks:
Group tightly coupled views, components, composables, and types into cohesive domain feature folders (src/features/<domain>/) following Feature-Sliced Design (FSD) principles.
Extract reusable stateful logic out of large .vue components into clean use<Feature>.ts composables.
Split monolithic Pinia stores into small, single-responsibility domain stores using Setup Store syntax.
Enable or tighten "strict": true in tsconfig*.json and resolve high-priority implicit any types in stores and composables.
Skill 6: 2-scale-2-data-layer (Data Layer & Network Resilience)
Files to inspect: src/api/*, src/services/*, stores/components making fetch/axios calls, heavy data-processing utilities, and top-level layout wrappers.
Tasks:
Centralize scattered fetch/axios calls out of .vue files into typed domain service modules (src/services/<domain>.service.ts) with shared interceptors.
Introduce TanStack Query (@tanstack/vue-query) for server-state endpoints needing caching, request deduplication, and background refetching.
Offload heavy client-side data transformations (large CSV/JSON parsing, complex filtering/sorting) to a dedicated Vite Web Worker.
Wrap major feature views in reusable Vue error boundary components using onErrorCaptured so single-widget crashes do not blank the entire app.
Skill 7: 2-scale-3-governance (Enterprise Governance, Multi-Team & Delivery)
Files to inspect: src/components/ui/*, CSS variables/theme files, src/router/*, src/main.ts, vite.config.*, and .github/workflows/*.
Tasks:
Consolidate hardcoded colors, spacing, and typography into CSS custom property design tokens and standardize base UI primitive props/slots.
Refactor route meta fields and router.beforeEach guards to enforce declarative role/permission (RBAC) checks across modules.
Set build.chunkSizeWarningLimit bundle budgets in vite.config.* and ensure CI pipelines run vue-tsc, Vitest unit tests, and Playwright E2E checks.
Add global error/performance hooks (app.config.errorHandler / Sentry readiness) in src/main.ts, and evaluate whether Module Federation / Micro-Frontends is needed for your team size.

3. Security (2 Phases)
Skill 8: 3-sec-1-xss-storage (XSS, Injection & Client Storage Hardening)
Files to inspect: Templates with v-html or dynamic :href/:src, form components, .env* files, localStorage/sessionStorage usage, and logging utilities.
Tasks:
Wrap every untrusted v-html binding in DOMPurify.sanitize(...) and audit dynamic :href bindings to block javascript: URI injection.
Enforce strict schema validation (zod or vee-validate) on all user input forms before submission.
Inspect .env* files and import.meta.env.VITE_* references to ensure zero private API secrets, database keys, or signing tokens leak into the client bundle.
Remove raw JWTs, passwords, or PII from localStorage/sessionStorage and strip sensitive payload dumps from console.log and error trackers.
Skill 9: 3-sec-2-auth-headers (Auth, Headers, Transport & Supply-Chain Security)
Files to inspect: Auth stores/services, HTTP interceptors, src/router/*, index.html, hosting configs (vercel.json, netlify.toml, nginx.conf, vite.config.*), auth forms, and package.json.
Tasks:
Configure HTTP clients with withCredentials: true for HttpOnly; Secure; SameSite cookie auth, attach CSRF token headers on state-mutating requests, and handle 401 refresh-token rotation safely without infinite retry loops.
Verify router.beforeEach blocks unauthenticated or unauthorized navigation before component mounting (never relying on v-if UI hiding alone).
Add Content Security Policy (CSP), clickjacking protection (frame-ancestors 'none' / X-Frame-Options: DENY), and HSTS headers in hosting configs, plus Subresource Integrity (integrity="...") hashes on external CDN tags in index.html.
Add client-side submit throttling/CAPTCHA hooks on login, registration, and password-reset forms, and run npm audit to flag vulnerable packages.

How to Run Through This Roadmap
Run one skill per OpenCode session, then run /clear and git commit before moving to the next skill.
Follow the sequence 1-opt-1 → 1-opt-4, then 2-scale-1 → 2-scale-3, and finish with 3-sec-1 → 3-sec-2.

You are executing a complete post-development Production Hardening Pipeline across three pillars in strict sequential order:
1. Frontend Optimization (verified in `/frontend-opt-tests`)
2. Architecture & Data Scaling (verified in `/scaling-tests`)
3. Application Security Hardening (verified in `/security-tests`)

### Context & Token Management Rules (160k Window Budget)
- Work sequentially stage-by-stage. Do NOT dump entire large files into your responses—output concise diffs, summaries, and test pass/fail results.
- Never read `node_modules/`, `dist/`, `.git/`, or lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`).
- Use existing installed libraries (e.g., Vitest, Playwright, VueUse, Zod, DOMPurify, TanStack Query) where present in `package.json`. Install missing lightweight utilities only if required and compatible with the existing package manager.
- Run verification tests after EACH stage and fix any regressions before moving to the next stage.

---

### STAGE 1: Frontend Optimization & Verification (`/frontend-opt-tests`)
**Implementation:**
1. **Bundle & Routing (`package.json`, `vite.config.*`, `index.html`, `src/router/*`):** Convert static route imports to lazy `() => import(...)`, configure `manualChunks` in Vite for vendor splitting, enable Brotli/Gzip compression and CSS minification/purging, and add `<link rel="preload">` for critical assets.
2. **Rendering (`src/views/*`, heavy components):** Wrap heavy modals/charts/drawers in `defineAsyncComponent`, wrap stateful dynamic views in `<KeepAlive :max="5">`, apply `v-once` on static blocks and `v-memo` on expensive list items, and virtualize 100+ item lists where applicable.
3. **Reactivity & Events (`<script setup>`, `src/composables/*`, `src/stores/*`):** Convert large read-only datasets/instances to `shallowRef`/`shallowReactive`, replace expensive template method calls with cached `computed` properties, replace `deep: true` watchers with targeted getters, and debounce/throttle rapid search/scroll handlers.
4. **Media:** Add `loading="lazy"`, `decoding="async"`, and explicit `width`/`height` to below-the-fold `<img>` tags; keep LCP/hero images eager (`fetchpriority="high"`).

**Verification (`/frontend-opt-tests`):**
- Create Vitest unit/component tests inside `/frontend-opt-tests` verifying:
  - Router routes use lazy async functions (`typeof route.component === 'function'`).
  - Heavy components resolve asynchronously and `<KeepAlive>` preserves component state.
  - Computed properties cache results (do not recompute on unrelated state changes) and debounced handlers throttle rapid calls.
  - Production build (`npm run build`) completes cleanly without chunk/import errors.
- Run the tests and confirm 100% pass before starting Stage 2.

---

### STAGE 2: Scaling Up & Verification (`/scaling-tests`)
**Implementation:**
1. **Modular Architecture & State (`src/*`, `src/stores/*`, `tsconfig*.json`):** Group tightly coupled feature code into cohesive domain modules (`src/features/<domain>/`), extract reusable stateful logic from large `.vue` files (>300 lines) into `use<Feature>.ts` composables, split monolithic Pinia stores into modular domain stores, and tighten TypeScript strictness (`strict: true`) on stores/services.
2. **Data Layer & Resilience (`src/services/*`, layouts):** Centralize raw `fetch`/`axios` calls out of `.vue` files into typed domain service repositories with shared interceptors, implement query caching/deduplication (TanStack Query or composable cache), offload heavy parsing/filtering to a Vite Web Worker if large data transforms exist, and wrap major feature views in an `onErrorCaptured` Error Boundary component.
3. **Governance & Observability (`src/components/ui/*`, `src/main.ts`, `vite.config.*`):** Consolidate hardcoded theme values into CSS custom property design tokens, configure `build.chunkSizeWarningLimit`, and register a global `app.config.errorHandler` hook in `src/main.ts`.

**Verification (`/scaling-tests`):**
- Create Vitest tests inside `/scaling-tests` verifying:
  - Domain service repositories handle mocked HTTP responses, errors, and request deduplication/caching properly.
  - Extracted composables and modular Pinia stores manage state independently without circular imports.
  - The `onErrorCaptured` Error Boundary catches child component errors gracefully and renders fallback UI without crashing the root app.
- Run the tests and confirm 100% pass before starting Stage 3.

---

### STAGE 3: Security Hardening & Verification (`/security-tests`)
**Implementation:**
1. **XSS & Input Sanitization:** Wrap every `v-html` binding in `DOMPurify.sanitize(...)`, block `javascript:` URIs in dynamic `:href` bindings, and enforce schema validation (e.g., Zod) on user forms.
2. **Secrets & Storage Hygiene:** Audit `.env*` and `import.meta.env.VITE_*` to ensure zero private secrets are bundled; strip raw JWTs, passwords, and PII from `localStorage`/`sessionStorage` and `console.log`.
3. **Auth, RBAC & Headers (`src/router/*`, HTTP client, `index.html`, hosting configs):** Configure HTTP clients for `HttpOnly; Secure; SameSite` cookie credentials + CSRF token headers + safe 401 refresh rotation; enforce strict `router.beforeEach` auth/RBAC guards before route mounting; add CSP, `frame-ancestors 'none'` / `X-Frame-Options: DENY`, and HSTS headers in hosting/server configs; add Subresource Integrity (`integrity` + `crossorigin`) to external CDN tags; and add submit throttling/abuse guards on auth forms.

**Verification (`/security-tests`):**
- Create Vitest security regression tests inside `/security-tests` verifying:
  - XSS payloads (`<img src=x onerror=alert(1)>`, `<script>`) passed into sanitized `v-html` helpers/components are stripped.
  - Unauthenticated and unauthorized users are blocked and redirected by `router.beforeEach` RBAC guards before protected views mount.
  - HTTP client attaches CSRF headers / credentials properly and handles 401 refresh without infinite loops, while storage/env checks confirm no secrets leak into `localStorage` or `VITE_*` variables.
- Run `npm audit --audit-level=high` (report any advisories) and run all tests across `/frontend-opt-tests`, `/scaling-tests`, and `/security-tests`.

---

### Final Deliverable
Output a concise **Executive Summary** containing:
1. Files modified per stage (Optimization, Scaling, Security).
2. Test execution results for `/frontend-opt-tests`, `/scaling-tests`, and `/security-tests`.
3. Any manual actions required (e.g., rotating exposed env keys, server-side cookie flags, or high-severity `npm audit` upgrades).



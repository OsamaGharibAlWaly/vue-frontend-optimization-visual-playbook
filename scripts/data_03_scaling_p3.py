"""Pillar 2, Phase 3: enterprise governance, multi-team and delivery."""

from catalogue import anatomy, catalogue, code, decision, flow, tree

c = catalogue(
    "03-scaling/phase-3-governance", "PILLAR 2 · SCALING",
    "Phase 3 standardizes UI across teams, enforces security and performance guardrails in CI, and adds production "
    "visibility so regressions are caught before users report them.",
)

c.add(
    "scaling-phase-3-overview", "Scaling Phase 3 Overview: Governance & Delivery", "SCALE · PHASE 3",
    "Design tokens, RBAC, budgets, CI checks and observability turn good intentions into automated guardrails.",
    flow([("DESIGN", "Tokens + shared UI primitives"),
          ("ACCESS", "Declarative RBAC route guards"),
          ("BUDGET", "Chunk size limits in Vite"),
          ("CI", "vue-tsc + Vitest + Playwright"),
          ("MONITOR", "Sentry hooks in production")],
          note="Scope: src/components/ui/*, theme files, router, main.ts, vite.config.* and .github/workflows/*."),
    "Governance is what makes the first two pillars survive the next ten developers and the next ten releases.",
    "Consolidate design tokens, add meta-driven RBAC, set bundle budgets, run CI checks and add observability hooks.",
)

c.add(
    "design-tokens", "Design Tokens in CSS Custom Properties", "SCALE · PHASE 3",
    "One source for color, spacing and typography keeps every team's UI consistent and themes cheap.",
    code(["/* hardcoded in 40 components */",
          ".button { color: #4f46e5;",
          "  padding: 8px 16px; }",
          ".card { padding: 16px;",
          "  border-radius: 10px; }"],
         [":root {",
          "  --color-brand: #4f46e5;",
          "  --space-2: 8px;",
          "  --radius-md: 10px;",
          "}",
          ".button { color: var(--color-brand);",
          "  padding: var(--space-2); }"],
         note="Name tokens by role (--color-brand), not by value (--purple-500), so themes can change meaning."),
    "Tokens remove visual drift and make dark mode or rebranding a variable swap instead of a repository-wide edit.",
    "Replace hardcoded colors, spacing and radii in this UI folder with CSS custom property design tokens.",
)

c.add(
    "shared-ui-library", "Shared Component Library", "SCALE · PHASE 3",
    "A small set of well-documented primitives with stable props and slots beats every team rebuilding a button.",
    tree([(0, "src/shared/ui/", "Import surface for all teams"),
          (1, "Button.vue", "Props: variant, size, loading"),
          (1, "Input.vue", "Slots: label, hint, error"),
          (1, "Modal.vue", "Teleport + focus trap"),
          (1, "tokens.css", "Design token source"),
          (1, "index.ts", "Named exports only"),
          (0, "docs/stories/", "Stories double as tests")],
          note="Shared primitives stay presentation-only; domain behaviour belongs in feature folders."),
    "Shared UI raises the floor of quality across teams and reduces accessibility work to one implementation.",
    "Consolidate duplicated buttons/inputs into src/shared/ui with typed props, slots and an index.ts export.",
)

c.add(
    "rbac-route-guards", "Meta-Driven RBAC Route Guards", "SCALE · PHASE 3",
    "Permissions live on route meta and are enforced in router.beforeEach before a view ever mounts.",
    code(["// route meta",
          "{ path: '/admin',",
          "  component: Admin,",
          "  meta: { roles: ['admin'] } }",
          "// UI hidden with v-if only"],
         ["router.beforeEach((to) => {",
          "  const needed = to.meta.roles",
          "  if (needed && !hasAnyRole(needed))",
          "    return { name: 'forbidden' }",
          "})",
          "// server still validates"],
         note="UI hiding is convenience, not security. The router guard and the API must both enforce access."),
    "Route-level permissions make access control declarative, reviewable and impossible to skip by deep-linking.",
    "Add declarative role/permission meta to these routes and enforce it in router.beforeEach before mounting.",
)

c.add(
    "ci-cd-tests", "CI Gates: vue-tsc, Vitest, Playwright", "SCALE · PHASE 3",
    "Automated checks are the only guardrail that runs when nobody is watching.",
    flow([("PUSH", "Developer opens a PR"),
          ("TYPES", "vue-tsc catches interface drift"),
          ("UNIT", "Vitest checks composables/services"),
          ("E2E", "Playwright checks critical journeys"),
          ("BUILD", "Bundle budget gate + deploy")],
          note="Fast checks first: type and unit tests before slower browser tests."),
    "CI turns conventions into enforcement. A pipeline with clear, fast failures keeps quality from depending on discipline.",
    "Ensure CI runs vue-tsc, Vitest and Playwright plus the production build before any deploy.",
)

c.add(
    "observability", "Observability: Error & Performance Hooks", "SCALE · PHASE 3",
    "Production feedback closes the loop: errors and long tasks should reach your dashboard, not the support inbox.",
    anatomy(("APP HOOKS", "app.config + performance"),
            [("Vue errors", "app.config.errorHandler → Sentry."),
             ("Boundary errors", "onErrorCaptured with component context."),
             ("Web Vitals", "LCP, INP and CLS reported per route."),
             ("Long tasks", "PerformanceObserver for jank spikes.")],
            note="Redact tokens and PII before any error leaves the browser."),
    "You cannot optimize or secure what you cannot see. Hooks make production behaviour measurable.",
    "Register app.config.errorHandler and Web Vitals reporting in src/main.ts with token/PII redaction.",
)

c.add(
    "module-federation", "Micro-Frontends: Decide With Data", "SCALE · PHASE 3",
    "Module Federation solves independent deployment across teams. It also adds runtime and operational complexity.",
    decision("Do multiple teams need to deploy separate parts of this UI independently?",
             [("YES", "Consider federation", "Define host/remote contracts, shared deps and versioning first."),
              ("NO", "Keep one build", "Feature folders + shared UI are simpler and faster.")],
             note="Adopt micro-frontends for organizational boundaries, not for code size alone."),
    "Federation is a last resort in the scaling roadmap. Start with module boundaries; escalate only when deployment ownership demands it.",
    "Evaluate team size and deployment needs, then write a short recommendation on Module Federation for this repo.",
)

"""Closing chapter: verification suites and the executive summary."""

from catalogue import bullets, catalogue, code, flow, metrics, timeline

c = catalogue(
    "05-proof-and-ship", "PROOF & SHIP",
    "The pipeline is only as strong as its gates. These three suites turn each pillar's claims into executable evidence, "
    "and the final summary is what you hand to a teammate, a manager, or a LinkedIn reader.",
)

c.add(
    "frontend-opt-tests", "Verification 1: /frontend-opt-tests", "PROOF · SUITE 1",
    "Prove that routes are lazy, heavy components load asynchronously, caching works and the production build is clean.",
    bullets([("Lazy routes", "typeof route.component === 'function' for every route."),
             ("Async components", "Heavy views resolve asynchronously with a fallback."),
             ("KeepAlive", "State survives switching between cached views."),
             ("computed caching", "No recompute on unrelated state changes."),
             ("Debounce", "Rapid calls collapse into one after the delay."),
             ("Build", "npm run build completes without chunk/import errors.")],
            note="Run this suite after every Phase 1-4 change; fix regressions before starting the scaling pillar."),
    "This suite protects the user-visible work from being silently undone by later refactors.",
    "Create Vitest tests in /frontend-opt-tests for lazy routes, async resolution, KeepAlive, computed caching, debounce and a clean build.",
)

c.add(
    "scaling-tests", "Verification 2: /scaling-tests", "PROOF · SUITE 2",
    "Prove that services handle HTTP outcomes, state modules stay independent, and error boundaries contain crashes.",
    bullets([("Services", "Mocked success, error and deduplication paths."),
             ("Caching", "Repeated query keys share one request."),
             ("State modules", "Composables and stores have no circular imports."),
             ("Error boundary", "Child throw renders fallback, root app survives."),
             ("Retry fallback", "Retry action remounts the failed feature."),
             ("Types", "vue-tsc passes with strict: true.")],
            note="A green suite here means the architecture changes did not break the performance work in Stage 1."),
    "Scaling changes touch many files; these tests are what make the refactor reversible and reviewable.",
    "Create Vitest tests in /scaling-tests for service responses, deduplication, modular state and onErrorCaptured fallback UI.",
)

c.add(
    "security-tests", "Verification 3: /security-tests", "PROOF · SUITE 3",
    "Prove that XSS payloads are stripped, guards block deep links, CSRF/credentials are attached and no secret leaks.",
    bullets([("XSS payloads", "<img src=x onerror=alert(1)> and <script> are stripped."),
             ("RBAC", "Unauthenticated and unauthorized users are redirected."),
             ("CSRF / 401", "Headers attached; refresh never loops forever."),
             ("Storage", "No raw JWT, password or PII in localStorage."),
             ("Environment", "No private value behind a VITE_* prefix."),
             ("Supply chain", "npm audit --audit-level=high reported.")],
            note="Security regressions are silent until an incident; make them loud in CI instead."),
    "Security tests are regression locks: they stop a future convenience change from reopening a closed hole.",
    "Create Vitest regression tests in /security-tests for sanitization, RBAC redirects, CSRF, 401 refresh and storage/env hygiene, then run npm audit.",
)

c.add(
    "executive-summary", "The Executive Summary", "PROOF · DELIVERABLE",
    "One short report closes the pipeline: what changed, what passed, and what a human still must do.",
    code(["## Executive Summary",
          "",
          "1. Files modified per stage",
          "   - Optimization: router, vite.config, views...",
          "   - Scaling: features/, services/, main.ts...",
          "   - Security: sanitizers, guards, headers...",
          "2. Tests: 100% pass in all three suites",
          "3. Manual actions: rotate keys, set cookies,",
          "   upgrade high-severity advisories"],
         ["## What to publish",
          "- Before/after LCP, TBT, CLS",
          "- Bundle size delta (gzip)",
          "- Screens from the visual playbook",
          "- The one prompt that fixed the biggest win",
          "- What you deliberately did NOT do"],
         note="A good summary is short enough to read in a standup and detailed enough to audit."),
    "The summary is the handover artifact. It turns a long refactor into three paragraphs a reviewer can trust.",
    "Write the executive summary with files modified per stage, all test results and the manual actions still required.",
)

c.add(
    "lighthouse-scorecard", "Before / After Scorecard", "PROOF · MEASUREMENT",
    "Numbers make the story credible. Capture the same metrics before and after, on the same device and network settings.",
    metrics([("LCP", "Largest Contentful Paint"),
             ("INP", "Interaction to Next Paint"),
             ("CLS", "Cumulative Layout Shift"),
             ("KB", "Entry bundle gzip")],
            [("LCP before", 82, "rose"), ("LCP after", 38, "green"),
             ("TBT before", 74, "amber"), ("TBT after", 28, "teal")],
            note="Keep the conditions identical: throttling, cache state, device profile and the same route."),
    "Optimization without measurement is opinion. A two-column scorecard turns the entire pipeline into evidence.",
    "Record LCP, INP, CLS and bundle size before and after this phase under identical throttling, then commit the numbers.",
)

c.add(
    "final-checklist", "The Roadmap Checklist", "PROOF · CLOSE",
    "Nine skills, three gates, one summary. This is the whole hardening pipeline on a single page.",
    timeline([("1-opt-1 → 1-opt-4", 0.00, 0.28, "cyan"),
              ("/frontend-opt-tests", 0.28, 0.10, "green"),
              ("2-scale-1 → 2-scale-3", 0.38, 0.24, "violet"),
              ("/scaling-tests", 0.62, 0.10, "green"),
              ("3-sec-1 → 3-sec-2", 0.72, 0.16, "amber"),
              ("/security-tests + summary", 0.88, 0.12, "teal")],
             note="Run one skill per session, /clear between phases, git commit between phases. Never batch all prompts at once."),
    "The checklist is the contract: one skill per session, a test gate per pillar, and a written handover at the end.",
    "Follow the sequence 1-opt-1 → 1-opt-4 → 2-scale-1 → 2-scale-3 → 3-sec-1 → 3-sec-2 with a commit and a green suite between each step.",
)

"""Build the all-in-one story README from the same data that renders the diagrams."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_00_story  # noqa: F401
import data_01_foundations_a  # noqa: F401
import data_01_foundations_b  # noqa: F401
import data_02_opt_phase1  # noqa: F401
import data_02_opt_phase2  # noqa: F401
import data_02_opt_phase3  # noqa: F401
import data_02_opt_phase4  # noqa: F401
import data_03_scaling_p1  # noqa: F401
import data_03_scaling_p2  # noqa: F401
import data_03_scaling_p3  # noqa: F401
import data_04_security_p1  # noqa: F401
import data_04_security_p2  # noqa: F401
import data_05_proof  # noqa: F401
from catalogue import ALL_CONCEPTS

CHAPTERS = [
    ("00-the-story", "0. The Story — Start Here"),
    ("01-foundations", "1. Foundations — 50 Mental Models"),
    ("02-optimization/phase-1-bundle", "2.1 Optimization Phase 1 — Bundle, Build & Route Splitting"),
    ("02-optimization/phase-2-rendering", "2.2 Optimization Phase 2 — Heavy Component & List Rendering"),
    ("02-optimization/phase-3-reactivity", "2.3 Optimization Phase 3 — Reactivity & Events"),
    ("02-optimization/phase-4-media-ssr", "2.4 Optimization Phase 4 — Media & Rendering Architecture"),
    ("03-scaling/phase-1-architecture", "3.1 Scaling Phase 1 — Architecture & State"),
    ("03-scaling/phase-2-data-layer", "3.2 Scaling Phase 2 — Data Layer & Resilience"),
    ("03-scaling/phase-3-governance", "3.3 Scaling Phase 3 — Governance & Delivery"),
    ("04-security/phase-1-xss-storage", "4.1 Security Phase 1 — XSS, Injection & Storage"),
    ("04-security/phase-2-auth-headers", "4.2 Security Phase 2 — Auth, Headers & Supply Chain"),
    ("05-proof-and-ship", "5. Proof & Ship — Verification Gates"),
]

MASTER_PROMPTS = [
    ("Skill 1 · 1-opt-1-bundle", "Optimization phase 1", """
Analyze package.json, vite.config.*, index.html, and the router configuration (src/router/*). Do not scan unrelated component files yet.

Convert static route imports to dynamic import() lazy-loaded routes for code splitting.

Configure Vite (vite.config.*) for optimal manual chunk splitting, tree-shaking, CSS purging/minification, and Brotli/Gzip compression (vite-plugin-compression), plus add rollup-plugin-visualizer for bundle analysis.

Add critical font/asset <link rel="preload"> hints in index.html.

Apply these changes directly and summarize the updated files."""),
    ("Skill 2 · 1-opt-2-rendering", "Optimization phase 2", """
Identify the heaviest UI views, modals, and large list/table components in src/views and src/components (skip small UI primitives like buttons/inputs).

Wrap heavy conditional components (modals, charts, drawers) with defineAsyncComponent.

Wrap dynamic tab/route views that benefit from state preservation in <KeepAlive> with an explicit max prop.

Replace large rendered lists (100+ items) with virtual scrolling, and apply v-once on static blocks or v-memo on expensive list items where appropriate.

List the files you modified and why."""),
    ("Skill 3 · 1-opt-3-reactivity", "Optimization phase 3", """
Audit Vue <script setup> blocks and Pinia stores (src/stores/*) specifically for reactivity and event bottlenecks.

Replace ref/reactive with shallowRef/shallowReactive for large read-only datasets or third-party instances.

Convert expensive template function calls into cached computed properties.

Replace any watch(..., { deep: true }) with targeted property watchers.

Add debouncing or throttling to rapid search inputs, resize, or scroll handlers.

Make minimal, safe edits and list each optimized file."""),
    ("Skill 4 · 1-opt-4-media-ssr", "Optimization phase 4", """
Scan templates and public/ / src/assets/ for image usage and check if this project requires SSR/SSG.

Add loading="lazy", decoding="async", and explicit width/height attributes to below-the-fold <img> tags, and update image pipelines/references to prefer WebP/AVIF formats.

Based on our current setup, briefly advise whether migrating to Nuxt (SSR/SSG) or keeping Vite SPA with prerendering (vite-plugin-ssr / vite-ssg) makes sense for SEO and First Contentful Paint—do not migrate frameworks automatically.

Apply safe image attribute changes and end with 3–4 bullets of architectural advice."""),
    ("Skill 5 · 2-scale-1-architecture", "Scaling phase 1", """
Inspect only src/* directory layout, tsconfig*.json, src/stores/*, and .vue files over 300 lines.

Group tightly coupled views, components, composables and types into src/features/<domain>/ folders following Feature-Sliced Design. Expose each feature through a public index.ts.

Extract reusable stateful logic from large .vue files into use<Feature>.ts composables.

Split monolithic Pinia stores into small Setup Stores with single responsibility.

Enable "strict": true in tsconfig*.json and resolve high-priority implicit any errors. Summarize each moved file."""),
    ("Skill 6 · 2-scale-2-data-layer", "Scaling phase 2", """
Inspect only src/api/*, src/services/*, components making fetch/axios calls, heavy data utilities, and top-level layouts.

Centralize raw fetch/axios calls into typed domain service modules (src/services/<domain>.service.ts) with shared interceptors.

Introduce TanStack Query (@tanstack/vue-query) for server-state endpoints needing caching, deduplication and background refetching.

Offload heavy parsing/filtering to a dedicated Vite Web Worker.

Wrap major feature views in reusable error boundaries using onErrorCaptured so one widget cannot blank the app. List every changed file."""),
    ("Skill 7 · 2-scale-3-governance", "Scaling phase 3", """
Inspect only src/components/ui/*, CSS theme files, src/router/*, src/main.ts, vite.config.*, and .github/workflows/*.

Consolidate hardcoded colors, spacing and typography into CSS custom property design tokens and standardize base UI props/slots.

Refactor route meta and router.beforeEach into declarative role/permission (RBAC) checks.

Set build.chunkSizeWarningLimit and ensure CI runs vue-tsc, Vitest and Playwright.

Add app.config.errorHandler / Sentry readiness in src/main.ts and briefly evaluate whether Module Federation is justified by our team size. Do not adopt it automatically."""),
    ("Skill 8 · 3-sec-1-xss-storage", "Security phase 1", """
Inspect only templates with v-html or dynamic :href/:src, form components, .env* files, localStorage/sessionStorage usage and logging utilities.

Wrap every untrusted v-html binding in DOMPurify.sanitize(...) with an explicit allowlist and block javascript: URIs in dynamic :href bindings.

Enforce strict schema validation (Zod or vee-validate) on all user input forms.

Inspect .env* and import.meta.env.VITE_* references to ensure zero private API secrets, database keys or signing tokens leak into the client bundle.

Remove raw JWTs, passwords and PII from localStorage/sessionStorage and strip sensitive payload dumps from console.log and error trackers."""),
    ("Skill 9 · 3-sec-2-auth-headers", "Security phase 2", """
Inspect only auth stores/services, HTTP interceptors, src/router/*, index.html, hosting configs and package.json.

Configure HTTP clients with withCredentials: true for HttpOnly; Secure; SameSite cookie auth, attach CSRF token headers on state-mutating requests, and handle 401 refresh-token rotation safely without infinite retry loops.

Verify router.beforeEach blocks unauthenticated or unauthorized navigation before component mounting—never rely on v-if hiding alone.

Add Content Security Policy, frame-ancestors 'none' / X-Frame-Options: DENY, and HSTS headers in hosting configs, plus Subresource Integrity hashes on external CDN tags.

Add client-side submit throttling/CAPTCHA hooks on auth forms and run npm audit --audit-level=high, reporting any advisories."""),
]

PIPELINE_PROMPT = """
You are executing a complete post-development Production Hardening Pipeline across three pillars in strict sequential order:

1. Frontend Optimization (verified in /frontend-opt-tests)
2. Architecture & Data Scaling (verified in /scaling-tests)
3. Application Security Hardening (verified in /security-tests)

Context rules:
- Work sequentially stage-by-stage. Never dump entire large files into responses—output concise diffs, summaries and test pass/fail results.
- Never read node_modules/, dist/, .git/ or lockfiles.
- Use installed libraries where present. Install missing lightweight utilities only if required.
- Run the verification tests after EACH stage and fix regressions before moving to the next stage.

Start with Stage 1 only: /frontend-opt-tests. Do not touch scaling or security files yet.
"""


def slug(text):
    """GitHub-style heading anchor: lowercase, strip punctuation, spaces to dashes."""
    import re
    cleaned = text.lower().replace("—", "")
    cleaned = re.sub(r"[^\w\s-]", "", cleaned, flags=re.UNICODE)
    return re.sub(r"\s", "-", cleaned).strip("-")


def md_escape(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def build():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    grouped = {}
    for concept in ALL_CONCEPTS:
        grouped.setdefault(concept["folder"], []).append(concept)

    out = []
    add = out.append

    add("# Vue Frontend Optimization — A Visual, Prompt-Driven Playbook")
    add("")
    add("> **154 diagrams · 12 sections · 9 copy-paste optimization prompts · 3 verification gates.**  ")
    add("> A single, systematic story that takes a Vue frontend from a slow first paint to a hardened, "
        "scalable production app — one concept, one picture, one prompt at a time.")
    add("")
    add("This repository turns `guide.md` into a visual handbook for engineers. Every concept in the guide "
        "gets its own high-resolution matplotlib diagram, a plain-English explanation, and a scoped prompt "
        "you can paste into OpenCode, Claude Code, Copilot CLI or any coding agent. The pictures are designed "
        "to be useful on their own in a code review, a standup, or a LinkedIn post.")
    add("")
    add("![The full journey](images/00-the-story/01-the-journey.png)")
    add("")
    add("---")
    add("")
    add("## The story in one paragraph")
    add("")
    add("A user opens your app. The entry bundle is too big, the list renders ten thousand rows, a deep watcher "
        "re-fetches on every keystroke, and an image pushes the heading down just as they click. You fix that in "
        "four ordered phases: **bundle/build**, **rendering**, **reactivity/events** and **media/architecture**. "
        "Then you make the fix survive growth with feature folders, typed services, query caching and CI gates. "
        "Finally you close the doors: sanitization, secret hygiene, cookie auth, CSP and dependency audits. "
        "Each stage has a test suite; the last page is a one-paragraph executive summary you can hand to anyone.")
    add("")
    add("## Contents")
    add("")
    add("| Chapter | What you get | Visuals |")
    add("|---|---|---:|")
    for folder, heading in CHAPTERS:
        items = grouped[folder]
        first = items[0]
        first_image = f"images/{folder}/01-{first['slug']}.png"
        add(f"| [{heading}](#{slug(heading)}) | {md_escape(first['subtitle'])} | [{len(items)}]({first_image}) |")
    add("| [Prompt Library](#prompt-library) | Nine phase prompts plus the pipeline master prompt | — |")
    add("| [Verification Gates](#verification-gates) | The three test suites and the final summary | — |")
    add("")
    add("## How to read it")
    add("")
    add("- **Skim:** open the images in `images/`; each is a self-contained explanation.")
    add("- **Study:** follow the chapters in order; every diagram has an idea, a takeaway and a prompt.")
    add("- **Ship:** run one skill per agent session, `/clear` between phases, commit between phases.")
    add("- **Verify:** a stage is done only when its named test suite is green.")
    add("- **Share:** link a single PNG in a post — a picture of a real bottleneck gets engineers talking.")
    add("")
    add("![How to use the playbook](images/00-the-story/04-how-to-read.png)")
    add("")
    add("## Regenerating the visuals")
    add("")
    add("```bash")
    add("python -m pip install matplotlib pillow")
    add("python scripts/validate.py      # check concept payload shapes")
    add("python scripts/qa.py            # check clipped text and collisions")
    add("python scripts/generate.py      # render all 154 PNGs + images/manifest.json")
    add("python scripts/build_readme.py  # rebuild this file")
    add("```")
    add("")
    add("Every diagram is 2720×1530 px. The design system lives in `scripts/design.py`; the concept catalogue "
        "lives in `scripts/data_*.py`. Change a concept once and both the image and this README update.")
    add("")
    add("---")
    add("")
    add("## Prompt Library")
    add("")
    add("**Do not paste all nine prompts at once.** That forces one giant file read, burns tokens and produces "
        "rushed edits. Run one skill per session, clear context, then commit. Pin exact paths (`@src/views/Dashboard.vue`) "
        "in large repos and never read `node_modules/`, `dist/`, `.git/` or lockfiles.")
    add("")
    for name, scope, prompt in MASTER_PROMPTS:
        add(f"### {name} — {scope}")
        add("")
        add("```text")
        add(prompt.strip())
        add("```")
        add("")
    add("### Production hardening pipeline — master prompt")
    add("")
    add("```text")
    add(PIPELINE_PROMPT.strip())
    add("```")
    add("")
    add("Token-saving rules: clear context between prompts, scope every read to named folders, commit after each "
        "phase so a shallowRef or v-memo regression is one `git revert` away, and audit bundle size plus Lighthouse "
        "after each stage rather than at the end.")
    add("")
    add("---")
    add("")

    visited = set()
    for index, (folder, heading) in enumerate(CHAPTERS):
        items = grouped[folder]
        add(f"## <a id=\"{slug(heading)}\"></a>{heading}")
        add("")
        add(items[0]["chapter_intro"])
        add("")
        if folder not in visited:
            visited.add(folder)
        for number, concept in enumerate(items, 1):
            image = f"images/{folder}/{number:02d}-{concept['slug']}.png"
            add(f"### {number:02d} · {concept['title']}")
            add("")
            add(f"![{concept['title']}]({image})")
            add("")
            add(f"**The idea.** {concept['subtitle']}")
            add("")
            add(f"**Why it matters.** {concept['takeaway']}")
            add("")
            add("**Prompt.**")
            add("")
            add("```text")
            add(concept["prompt"])
            add("```")
            add("")
        add("---")
        add("")

    add("## <a id=\"verification-gates\"></a>Verification Gates")
    add("")
    add("A stage is finished when its suite is green. The three suites are described in detail in chapter 5:")
    add("")
    add("1. `/frontend-opt-tests` — lazy routes, async resolution, KeepAlive, computed caching, debounce, clean build.")
    add("2. `/scaling-tests` — typed services, deduplication, modular state, error-boundary fallback.")
    add("3. `/security-tests` — sanitized XSS payloads, RBAC redirects, CSRF/credentials, storage and env hygiene, `npm audit`.")
    add("")
    add("### Executive summary template")
    add("")
    add("```markdown")
    add("## Executive Summary")
    add("")
    add("1. **Files modified per stage**")
    add("   - Optimization: router, vite.config, views, composables, images")
    add("   - Scaling: features/, services/, stores/, main.ts, CI config")
    add("   - Security: sanitizers, guards, headers, env and storage cleanup")
    add("2. **Test results**: 100% pass in /frontend-opt-tests, /scaling-tests, /security-tests")
    add("3. **Manual actions**: rotate exposed keys, set HttpOnly/Secure cookies at the server,")
    add("   upgrade high-severity npm advisories, enable HSTS after HTTPS verification")
    add("4. **Measured impact**: before/after LCP, INP, CLS and gzip bundle size")
    add("```")
    add("")
    add("---")
    add("")
    add("## Final word")
    add("")
    add("Performance work is not a pile of tricks. It is a loop: measure, locate, change one thing, verify, commit. "
        "The visuals in this repo exist to make each decision obvious enough to explain to a teammate in thirty "
        "seconds — and the prompts exist to make the change reproducible by any engineer on the team.")
    add("")
    add("Source material: `guide.md` in this repository. Built with Python + matplotlib; all diagrams are "
        "generated, none are hand-edited.")
    add("")

    path = os.path.join(root, "README.md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))
    print(f"Wrote {path} with {len(out)} lines from {len(ALL_CONCEPTS)} concepts.")


if __name__ == "__main__":
    build()

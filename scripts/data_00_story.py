from catalogue import bullets, catalogue, cycle, flow, hero, metrics, timeline

c = catalogue(
    "00-the-story", "THE STORY",
    "Every diagram in this repository is one page of the same story: a slow Vue app "
    "becomes a fast one, then a scalable one, then a safe one — and every step is "
    "verified before the next begins.",
)

c.add(
    "the-journey", "From White Screen to Production Hardened", "THE STORY · OPENING",
    "A single visual roadmap for the 100+ decisions behind a fast, maintainable, secure Vue frontend.",
    hero(
        [
            ("PILLAR 1 · OPTIMIZE", "Bundle, render, reactivity and media. Make the app feel instant."),
            ("PILLAR 2 · SCALE", "Feature architecture, data layer and governance for growing teams."),
            ("PILLAR 3 · SECURE", "XSS, secrets, auth, headers and the software supply chain."),
        ],
        strip="4 optimization phases  →  3 scaling phases  →  2 security phases  →  3 verification suites",
    ),
    "Speed is a system property. The three pillars are ordered: optimize what users feel first, then structure the code that keeps it fast, then close the doors that attackers use.",
    "Read the story top to bottom. Each concept has one diagram, one plain-English takeaway and one copy-paste prompt.",
)

c.add(
    "why-speed-is-a-feature", "Speed Is a Feature Users Feel Before They Measure", "THE STORY · THE STAKES",
    "Performance is not a Lighthouse score. It is a user deciding whether to stay, scroll or buy.",
    metrics(
        [("3s", "Load time many users still tolerate"),
         ("53%", "Mobile visits abandoned above 3s"),
         ("16.7ms", "Budget for one frame at 60fps"),
         ("1s", "Delay that breaks the feeling of instant")],
        [("Bounce risk", 88, "rose"), ("LCP delay", 70, "amber"),
         ("Main-thread jank", 64, "violet"), ("Bundle weight", 52, "cyan")],
        note="Measure first, then spend your effort where the budget is actually being burned: network, main thread, or render.",
    ),
    "A slow app loses attention before it loses arguments. Every optimization in this guide attacks one of four costs: bytes over the wire, JavaScript on the main thread, DOM work per render, or uncertainty in the UI.",
    "Before changing code, open DevTools Network + Performance and name the bottleneck out loud. Never optimize by vibes.",
)

c.add(
    "the-pipeline", "The Pipeline: Optimize, Scale, Secure, Verify", "THE STORY · MAP",
    "Three hardening pillars run in strict order, and a verification gate sits after each one.",
    flow(
        [("01 · OPTIMIZE", "Bundle, rendering, reactivity, media. Biggest perceived win, lowest token cost."),
         ("02 · SCALE", "Feature folders, typed services, caching, design tokens, CI guardrails."),
         ("03 · SECURE", "Sanitize input, lock auth, harden headers, audit dependencies."),
         ("04 · VERIFY", "Vitest suites per pillar, then a single executive summary.")],
        note="One skill per session. Clear context between phases. Commit between phases. Verify before advancing.",
    ),
    "The order is deliberate: architecture changes can invalidate performance work, and security work can break auth flows. Sequential stages with tests between them make regressions visible instead of mysterious.",
    "Follow /frontend-opt-tests → /scaling-tests → /security-tests. Do not start stage N+1 while stage N has a red test.",
)

c.add(
    "how-to-read", "How to Read This Playbook in Ten Minutes", "THE STORY · USAGE",
    "Use it as a story, a visual glossary, or a prompt deck — each concept works on its own.",
    bullets(
        [("Start with the map", "Read the first six diagrams. They explain the order and the rules."),
         ("Pick your layer", "Foundations, optimization, scaling or security — jump straight to the chapter."),
         ("Look at the picture", "Every diagram shows before/after, a flow, a tree, or a decision."),
         ("Copy the prompt", "Each concept ends with one scoped instruction you can paste into OpenCode."),
         ("Verify, then commit", "Run the named test suite and checkpoint before the next concept."),
         ("Share one page", "Each PNG stands alone, so you can post a single diagram on LinkedIn.")],
        note="One concept, one diagram, one prompt, one commit. The repository is designed to be skimmed and reused.",
    ),
    "A guide that cannot be scanned will not be used. The images are the table of contents; the prompts are the action; the tests are the proof.",
    "Bookmark the chapter you are working on today and open the matching prompt from the Prompt Library section.",
)

c.add(
    "measure-fix-loop", "The Loop That Makes Optimization Repeatable", "THE STORY · METHOD",
    "Measure, locate, patch, verify, ship — then repeat. Optimization is a loop, not a one-off cleanup.",
    cycle(
        [("Measure", "Lighthouse, Web Vitals, bundle report"),
         ("Locate", "Find the exact file and the exact cost"),
         ("Patch", "One scoped change, one concept"),
         ("Verify", "Tests + build + before/after numbers"),
         ("Ship", "Commit, monitor, then loop again")],
        center="FIX LOOP",
        note="Never batch ten optimizations into one prompt: context grows, edits get rushed, and you cannot tell which change helped.",
    ),
    "A loop with one change per iteration gives you attribution: you know which edit moved LCP, which one broke reactivity, and which one to revert.",
    "For every change, write the before number and the after number in the commit message. If you cannot measure it, call it a refactor, not a performance fix.",
)

c.add(
    "token-discipline", "One Skill Per Session: The Token Budget Is Real", "THE STORY · WORKFLOW",
    "Clear context, scope file reads, commit per phase — the same code with a tighter prompt costs far fewer tokens.",
    timeline(
        [("Prompt 1 · scoped", 0.00, 0.20, "cyan"),
         ("Edit + diff + test", 0.20, 0.17, "teal"),
         ("git commit", 0.37, 0.10, "green"),
         ("/clear context", 0.47, 0.11, "amber"),
         ("Prompt 2 · scoped", 0.58, 0.19, "violet"),
         ("Verify + commit", 0.77, 0.20, "blue")],
        note="Scope each prompt to exact folders. Do not read node_modules, dist, .git or lockfiles. Keep the agent's file context small.",
    ),
    "Large contexts are slow and expensive. The guide's four-phase prompt split exists because focused prompts produce better edits, cleaner checkpoints and lower token bills.",
    "Run /clear between phases, pin exact paths with @src/views/Dashboard.vue, and commit after every phase.",
)

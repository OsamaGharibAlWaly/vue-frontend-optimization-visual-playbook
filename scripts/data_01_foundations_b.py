"""Foundations 26-50: perceived speed, delivery and long-term quality."""

from catalogue import (anatomy, bullets, catalogue, code, compare, cycle,
                       decision, flow, layers, matrix, metrics, timeline, tree)

c = catalogue(
    "01-foundations", "FOUNDATIONS",
    "The second half of the foundation chapter turns architecture rules into user-visible behaviour: "
    "optimistic UI, caching, splitting, debouncing, error handling and the habits that keep code cheap to change.",
)

c.add(
    "optimistic-ui", "Optimistic UI", "FOUNDATIONS · PERCEIVED SPEED",
    "Apply the expected result immediately, then reconcile with the server. The interface feels instant.",
    timeline([("Click / submit", 0.00, 0.14, "cyan"),
              ("Optimistic paint", 0.14, 0.10, "green"),
              ("Request in flight", 0.24, 0.42, "amber"),
              ("Server confirms", 0.66, 0.10, "teal"),
              ("Reconcile / rollback", 0.76, 0.20, "violet")],
             note="Always define the rollback path before adding the optimistic update."),
    "Optimistic UI trades a moment of uncertainty for a much faster feel. It is only safe when failures are handled visibly.",
    "Apply this mutation optimistically, keep the previous snapshot, and roll back with a clear message on failure.",
)

c.add(
    "race-conditions", "Race Conditions", "FOUNDATIONS · CONCURRENCY",
    "Two requests for the same query can return out of order. The slower, older answer must not win.",
    timeline([("Type 'a'", 0.00, 0.18, "cyan"),
              ("Request A", 0.10, 0.52, "rose"),
              ("Type 'ab'", 0.34, 0.18, "teal"),
              ("Request B", 0.42, 0.28, "green"),
              ("B returns first → keep B", 0.70, 0.16, "violet")],
             note="Use AbortController, a request token, or a query library that cancels stale requests."),
    "Async results arriving in the wrong order is the classic source of stale search results and flickering UI.",
    "Abort the previous request in this watcher or tag each response with a token and ignore stale results.",
)

c.add(
    "idempotency", "Idempotency", "FOUNDATIONS · RESILIENCE",
    "Repeating the same operation must produce the same result. Retries then become safe instead of dangerous.",
    compare(["Retry a POST and create two orders",
             "Double click submits twice",
             "Refresh replays a payment",
             "Network retry duplicates webhooks"],
            ["Idempotency-Key header per intent",
             "Disable the button while pending",
             "PUT/PATCH with stable resource id",
             "Server deduplicates by key"],
            verdict="Client guardrails are not enough; the mutation needs a server-side idempotency key."),
    "Anything that can be retried will be retried. Design the mutation so the second attempt is harmless.",
    "Attach an idempotency key to this mutation and disable the submit control while the request is pending.",
)

c.add(
    "caching-strategy", "Caching Strategy", "FOUNDATIONS · NETWORK",
    "Every piece of data needs an owner and a lifetime: server cache, client store, or no cache at all.",
    layers([("SERVER STATE", "Vue Query / SWR", "Cache by query key, dedupe, background refresh."),
            ("CLIENT STATE", "Pinia domain store", "UI intent and session state, not fetched snapshots."),
            ("HTTP", "Cache-Control + ETag", "Let the browser/CDN avoid a round trip."),
            ("BUILD", "Hashed static assets", "Immutable files can be cached forever.")],
           note="One caching layer per data kind. Two owners means two versions of the truth."),
    "Cache policy is a design decision, not a library default. Wrong layers cause stale screens or needless requests.",
    "Classify this data as server or client state, assign one cache owner, and document its staleness window.",
)

c.add(
    "stale-while-revalidate", "Stale-While-Revalidate", "FOUNDATIONS · NETWORK",
    "Show cached data instantly, refresh it quietly in the background, then replace it when the new answer arrives.",
    cycle([("SERVE", "Return cached value now"),
           ("RENDER", "UI appears immediately"),
           ("REVALIDATE", "Fetch in the background"),
           ("REPLACE", "Swap in fresh data"),
           ("REPEAT", "Cache is ready next time")],
          center="SWR",
          note="Fresh enough beats blank. Pair it with a visible subtle refresh state for trust."),
    "SWR improves perceived speed without sacrificing freshness, because the refresh happens after paint.",
    "Configure this query to return cached data immediately and refetch on mount and focus.",
)

c.add(
    "code-splitting", "Code Splitting", "FOUNDATIONS · DELIVERY",
    "Ship the code for the current screen, not the whole app. Smaller entry chunks mean faster first paint.",
    compare(["One 1.8 MB app.js for every route",
             "Admin charts load for the login page",
             "Parse + compile blocks the main thread",
             "Every deploy invalidates the whole bundle"],
            ["Route and feature chunks",
             "Heavy widgets load on demand",
             "Entry parses in a fraction of the time",
             "Stable vendor chunks stay cached"],
            verdict="Split on navigation and on expensive features; verify with a bundle analyzer."),
    "The browser must download, parse and execute everything you send. The cheapest byte is the one you never ship.",
    "Convert this route or heavy feature to a dynamic import and inspect the new chunk graph.",
)

c.add(
    "lazy-loading", "Lazy Loading", "FOUNDATIONS · DELIVERY",
    "Defer a module until the user is likely to need it. Loading is a scheduling decision.",
    flow([("ENTRY", "Small initial bundle"),
          ("TRIGGER", "Route, hover, idle or intersection"),
          ("FETCH", "Dynamic import chunk"),
          ("FALLBACK", "Skeleton while pending"),
          ("MOUNT", "Component becomes interactive")],
          note="Preload on intent (hover/focus) to hide the network latency before the click."),
    "Lazy loading without a fallback feels broken. Always render a placeholder that occupies the final space.",
    "Wrap this heavy view in defineAsyncComponent with a skeleton loadingComponent and an errorComponent.",
)

c.add(
    "tree-shaking", "Tree Shaking", "FOUNDATIONS · DELIVERY",
    "The bundler drops exports nothing imports. Write code that can be dropped — keep side effects explicit.",
    compare(["import * as icons from 'icon-pack'",
             "Library re-exports everything from one file",
             "Top-level side effects block removal",
             "Dead code ships to every user"],
            ["import { Search } from 'icon-pack'",
             "ES modules with named exports",
             "sideEffects: false where truthful",
             "Analyzer confirms the drop"],
            verdict="Verify with the bundle analyzer; tree shaking is never a matter of faith."),
    "Tree shaking works best with static imports, named exports and pure modules. Wildcard imports defeat it.",
    "Replace wildcard imports in this file with named imports and confirm the chunk shrinks after build.",
)

c.add(
    "bundle-bloat", "Bundle Bloat", "FOUNDATIONS · DELIVERY",
    "Bloat is what happens when nobody owns the size budget. It creeps in one convenient import at a time.",
    metrics([("+1 MB", "Added by one 'harmless' library"),
             ("200ms", "Parse cost on a mid-range phone"),
             ("4 KB", "Target for a small feature chunk"),
             ("0", "Unused exports that should ship")],
            [("Entry JS", 92, "rose"), ("Vendor JS", 74, "amber"),
             ("CSS", 40, "cyan"), ("Images", 66, "violet")],
            note="Put a budget in vite.config and let CI fail when the app crosses it."),
    "Size is a product constraint like any other. Without a budget, every dependency looks free until the Lighthouse score drops.",
    "Run the bundle visualizer, find the largest module, and either lazy-load it or replace it.",
)

c.add(
    "render-bottlenecks", "Render Bottlenecks", "FOUNDATIONS · RENDER",
    "A bottleneck is a render that happens too often, touches too much, or does too much work per node.",
    metrics([("16.7ms", "Full frame budget at 60fps"),
             ("50+", "Nodes updated for one keystroke"),
             ("3x", "Re-renders per state change"),
             ("0", "Work that should be cached")],
            [("Deep watchers", 86, "rose"), ("Inline formatters", 70, "amber"),
             ("Large lists", 94, "violet"), ("Deep reactivity", 60, "cyan")],
            note="Profile with Vue Devtools: find the component that re-renders, then narrow its dependencies."),
    "Render cost is (number of nodes) × (number of renders) × (work per node). Attack whichever factor is largest.",
    "Profile this interaction, name the re-rendering component, and apply one of the three fixes before moving on.",
)

c.add(
    "virtual-scrolling", "Virtual Scrolling", "FOUNDATIONS · RENDER",
    "Render the 20 rows the user can see, not the 10,000 rows the data contains.",
    compare(["10,000 DOM rows mounted",
             "Huge layout + diff cost per update",
             "Slow initial paint and scrolling",
             "Memory grows with dataset size"],
            ["~20 visible rows + spacers",
             "Constant DOM size regardless of data",
             "Smooth scroll with recycled nodes",
             "Stable height prevents jumping"],
            verdict="Use virtualization at 100+ rows, or earlier when rows are complex."),
    "The DOM is the render bottleneck. Virtual scrolling caps it with a window and spacer elements.",
    "Replace this v-for with @tanstack/vue-virtual and keep a fixed row height or measured estimate.",
)

c.add(
    "debouncing", "Debouncing", "FOUNDATIONS · EVENTS",
    "Wait for a pause in the event stream before running the expensive work. Ideal for search input.",
    timeline([("k", 0.02, 0.06, "rose"), ("e", 0.09, 0.06, "rose"),
              ("y", 0.16, 0.06, "rose"), ("300ms quiet", 0.23, 0.28, "amber"),
              ("1 API call", 0.55, 0.34, "green")],
             note="Debounce = run once after silence. Pick 200-300ms for search, longer for expensive filters."),
    "Typing 'keyboard' should not fire seven requests. Debouncing collapses a burst into one intentional action.",
    "Wrap this search handler in useDebounceFn(fn, 300) and cancel it on unmount.",
)

c.add(
    "throttling", "Throttling", "FOUNDATIONS · EVENTS",
    "Run at most once per interval. Ideal for continuous events like scroll, resize and pointer move.",
    timeline([("scroll burst", 0.00, 0.50, "rose"),
              ("run", 0.02, 0.06, "green"), ("run", 0.24, 0.06, "green"),
              ("run", 0.46, 0.06, "green"), ("ignored events", 0.52, 0.42, "amber")],
             note="Throttle = at most one run per window. Use requestAnimationFrame for visual updates."),
    "Throttling keeps feedback responsive without doing layout work on every native event.",
    "Throttle this scroll/resize handler to one call per frame and read layout only inside that callback.",
)

c.add(
    "error-boundaries", "Error Boundaries", "FOUNDATIONS · RESILIENCE",
    "Catch a child's render error locally and show a fallback. One broken widget should not blank the app.",
    anatomy(("ERROR BOUNDARY", "onErrorCaptured + fallback UI"),
            [("Widget A", "Renders normally."),
             ("Widget B", "Throws during render."),
             ("Fallback", "Shows retry, keeps the rest alive."),
             ("Reporter", "Logs to Sentry with context.")],
            note="Return false from onErrorCaptured to stop propagation after you have handled it."),
    "Error boundaries turn a total outage into a degraded feature. They belong around independent feature roots.",
    "Wrap this feature view in an ErrorBoundary component with a retry button and error reporting hook.",
)

c.add(
    "graceful-degradation", "Graceful Degradation", "FOUNDATIONS · RESILIENCE",
    "Build for capable browsers, then define what the page does when a feature is missing or a request fails.",
    layers([("BASE", "Semantic HTML", "Works everywhere, even with JavaScript disabled."),
            ("ENHANCE", "CSS then JS", "Add capability progressively on top of the base."),
            ("FALLBACK", "Skeleton or cached data", "Keep the screen useful while fresh data is missing."),
            ("RECOVERY", "Retry / offline state", "Offer a safe default and a clear way forward.")],
           note="The app should lose features, not become unusable."),
    "Degradation is a product decision made in code: what is the minimum useful version of this screen?",
    "Define the fallback for this feature when its API fails and render it without blocking the rest of the page.",
)

c.add(
    "defensive-programming", "Defensive Programming", "FOUNDATIONS · RESILIENCE",
    "Validate at trust boundaries and assume partial data. Do not sprinkle checks through rendering code.",
    compare(["Assume the API always returns items[]",
             "Access nested fields without guards",
             "Catch errors with empty catch blocks",
             "Fail deep inside the renderer"],
            ["Validate DTOs with Zod at the service",
             "Provide defaults for optional fields",
             "Handle errors where you can recover",
             "Fail fast with a clear message"],
            verdict="Trust your own types; validate everything crossing a network, storage or user boundary."),
    "Defensive code belongs at the edges. Inside the system, types and invariants should already hold.",
    "Add a Zod schema at this service boundary and give the template a safe default for missing fields.",
)

c.add(
    "strict-typing", "Strict Typing", "FOUNDATIONS · QUALITY",
    "strict: true turns implicit assumptions into compiler errors. It is the cheapest long-term maintenance win.",
    code(["// tsconfig.json",
          '{ "compilerOptions": {',
          '    "strict": false',
          '  } }',
          "// props silently any, null slips through"],
         ["// tsconfig.json",
          '{ "compilerOptions": {',
          '    "strict": true,',
          '    "noUncheckedIndexedAccess": true',
          '  } }',
          "// every ambiguity becomes an error"],
         note="Enable strict first, then fix errors by domain; never silence them with broad any."),
    "Strict mode pays back on every refactor: the compiler finds the callers you forgot.",
    "Enable strict in tsconfig, run vue-tsc, and fix the errors in one domain at a time.",
)

c.add(
    "interface-segregation", "Interface Segregation", "FOUNDATIONS · QUALITY",
    "Expose small, purpose-built interfaces instead of one giant catch-all type or store.",
    compare(["One AppState with 60 fields",
             "Every component sees everything",
             "Any change touches all consumers",
             "Mocks need the whole object"],
            ["Per-feature state slices and DTOs",
             "Components declare the exact props they use",
             "Small types are easy to fake in tests",
             "Changes stay local"],
            verdict="Prefer many small contracts over one large one."),
    "Large interfaces force components to depend on fields they never use, which increases coupling and test cost.",
    "Replace this catch-all type with two narrow interfaces named after their consumers.",
)

c.add(
    "technical-debt", "Technical Debt", "FOUNDATIONS · QUALITY",
    "Debt is the gap between the code you have and the code you wish you had. Interest is paid on every change.",
    cycle([("NOTICE", "A shortcut with a limit"),
           ("RECORD", "Comment or ticket with why"),
           ("PAY", "Refactor it while context is fresh"),
           ("VERIFY", "Tests confirm behaviour"),
           ("MOVE ON", "Debt does not compound")],
          center="DEBT LOOP",
          note="Not all debt is bad. Undocumented debt in hot paths is the expensive kind."),
    "Debt becomes dangerous when nobody knows it exists. Write the limit down next to the shortcut.",
    "Log each shortcut with a one-line limit and upgrade condition, then pay the highest-interest one first.",
)

c.add(
    "refactoring", "Refactoring", "FOUNDATIONS · QUALITY",
    "Change the structure without changing behaviour. Tests are the safety net that makes this boring.",
    flow([("GREEN", "Start with passing tests"),
          ("SMALL STEP", "One structural edit"),
          ("RUN", "Re-run the test suite"),
          ("COMPARE", "Behaviour unchanged?"),
          ("COMMIT", "Checkpoint the refactor")],
          note="Never mix a refactor and a feature in the same commit; attribution disappears."),
    "Refactoring is a disciplined loop, not a week-long rewrite. Small steps with green tests keep risk near zero.",
    "Add a test around this behaviour, then apply one structural change and re-run it before continuing.",
)

c.add(
    "modularity", "Modularity", "FOUNDATIONS · ARCHITECTURE",
    "Modules hide their internals behind a public surface. You can replace one without rewriting the app.",
    tree([(0, "src/features/orders/", "One domain, one public index.ts"),
          (1, "components/OrdersTable.vue", "Presentation only"),
          (1, "composables/useOrders.ts", "Stateful logic"),
          (1, "api/orders.service.ts", "Typed HTTP boundary"),
          (1, "types.ts", "Domain DTOs"),
          (1, "index.ts", "The only import surface"),
          (0, "src/shared/ui/", "Framework-agnostic primitives")],
          note="Import from @/features/orders, never from its internal files."),
    "A public index.ts is a cheap enforceable boundary: it tells you exactly what the rest of the app may use.",
    "Add an index.ts to this feature and update imports to use the public surface only.",
)

c.add(
    "scalability", "Scalability", "FOUNDATIONS · ARCHITECTURE",
    "A scalable frontend grows by adding isolated features, not by making one giant app more complicated.",
    matrix(("Team size →", "Change cost ↑"),
           [("Isolated features", "New team owns a folder and ships independently."),
            ("Shared shell", "Only the app shell coordinates routes and tokens."),
            ("Chaotic core", "Every feature edits the same global files."),
            ("Duplicated apps", "No shared primitives, inconsistent UX.")],
           note="Scale the boundaries first; tools and micro-frontends come later."),
    "Micro-frontends solve organizational problems. Start with module boundaries and shared conventions before adopting them.",
    "Draw the ownership boundary for this feature and list the shared contracts it depends on.",
)

c.add(
    "maintainability", "Maintainability", "FOUNDATIONS · QUALITY",
    "Maintainable code is easy to understand on the first read and safe to change on the tenth.",
    bullets([("Named concepts", "Functions and files say what they own."),
             ("Small blast radius", "An edit affects one feature folder."),
             ("Visible dependencies", "Props, injections and stores are explicit."),
             ("Executable docs", "Tests describe the expected behaviour."),
             ("Consistent patterns", "One way to fetch, one way to format."),
             ("Measured performance", "Budgets prevent silent regressions.")],
            note="A new teammate should ship a small change on day one without asking permission."),
    "Maintainability is the compound result of the other foundations — not a separate activity at the end.",
    "Score this module on these six points and fix the weakest one with a single scoped change.",
)

c.add(
    "abstraction-layers", "Abstraction Layers", "FOUNDATIONS · ARCHITECTURE",
    "Each layer solves one problem and talks only to its neighbours. Leaks across layers create hidden coupling.",
    layers([("UI", "Views and widgets", "Render and emit. No HTTP, no caching rules."),
            ("APPLICATION", "Composables and stores", "Use cases and orchestration."),
            ("DOMAIN", "Entities and validation", "Rules that survive a framework change."),
            ("INFRASTRUCTURE", "HTTP, storage, analytics", "Details that can be swapped.")],
           note="Dependencies point inward; infrastructure never imports UI."),
    "Layers are useful only when they are enforced. One leaked import collapses the benefit of all of them.",
    "Move this HTTP call out of the view into the service layer and keep only a typed result in the component.",
)

c.add(
    "lifecycle-management", "Lifecycle Management", "FOUNDATIONS · REACTIVITY",
    "Every resource has a birth, a working life and a teardown. Vue gives you hooks; use them symmetrically.",
    cycle([("CREATE", "onMounted / watch / subscribe"),
           ("WORK", "Read reactive inputs"),
           ("UPDATE", "React to changes"),
           ("CLEAN", "onScopeDispose / abort"),
           ("DESTROY", "Component unmounts cleanly")],
          center="LIFECYCLE",
          note="If you can list what you create, you can list what you must cancel."),
    "Unmatched lifecycles are the root of timers firing after unmount and subscriptions piling up in long sessions.",
    "Audit this component: pair every listener, timer and subscription with a teardown in onScopeDispose.",
)

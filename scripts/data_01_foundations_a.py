"""Foundations 01-25: state, structure and reactivity mental models."""

from catalogue import (anatomy, catalogue, code, compare, cycle, decision,
                       flow, layers, matrix, metrics, timeline, tree, bullets)

c = catalogue(
    "01-foundations", "FOUNDATIONS",
    "Fifty mental models sit underneath every optimization. Learn these once and each later "
    "phase becomes an application of the same few rules: one owner for state, one direction "
    "for data, one reason for each component to change.",
)

c.add(
    "separation-of-concerns", "Separation of Concerns", "FOUNDATIONS · ARCHITECTURE",
    "A view renders, a composable decides, a service fetches. When those jobs stay apart, each can change alone.",
    layers([("VIEW", "Template + styles", "What the user sees. No fetching, no business rules, no raw mutation."),
            ("LOGIC", "use<Feature> composable", "State, derived values, intent and side effects in one readable place."),
            ("DATA", "Typed service / repository", "HTTP, caching and mapping live behind one narrow interface."),
            ("INFRA", "Router, store, plugins", "Cross-cutting wiring stays explicit and replaceable.")],
           note="Change one layer without touching the others — that is the whole point."),
    "Mixed concerns make every edit risky. Splitting by job, not by file type, is the first move in every refactor.",
    "Split this component into a presentational view, one use<Feature> composable and one typed service call.",
)

c.add(
    "single-source-of-truth", "Single Source of Truth", "FOUNDATIONS · STATE",
    "One authoritative value per fact. Every screen reads the same value instead of keeping a private copy.",
    anatomy(("ONE STORE", "One owner per domain fact"),
            [("Store / query cache", "The canonical value lives here."),
             ("View A", "Reads the value, never copies it."),
             ("View B", "Reads the same value, stays in sync."),
             ("Derived UI", "Computed from the value, not stored twice.")],
            note="Duplicated state is duplicated bugs: one screen updates, the other forgets."),
    "Copying server data into local state creates drift. Read the canonical store and derive everything else.",
    "Find local copies of server data in this component and replace each with a store getter or query result.",
)

c.add(
    "unidirectional-data-flow", "Unidirectional Data Flow", "FOUNDATIONS · STATE",
    "State flows down as props, events flow up as intent. The direction never reverses.",
    flow([("STATE", "Store owns the value"),
          ("PROPS", "Parent passes it down"),
          ("VIEW", "Child renders / emits"),
          ("ACTION", "Parent handles the event"),
          ("UPDATE", "Store changes once")],
          note="When data flows in one direction, a bug has one path to trace instead of many."),
    "Two-way mutation across sibling components hides causality. Events up, state down keeps every change explainable.",
    "Replace this child's direct state mutation with an emit to its parent and one store action.",
)

c.add(
    "prop-drilling", "Prop Drilling", "FOUNDATIONS · STATE",
    "Passing a value through five components that do not use it adds noise and coupling at every hop.",
    compare(["Pass user through Layout → Page → Panel → Row → Cell",
             "Every middle component declares props it never reads",
             "Rename the prop and touch the whole chain",
             "Tests must build the entire tree"],
            ["provide('currentUser', user) at the feature root",
             "inject() only in the leaf that needs it",
             "Store getter or query for cross-feature data",
             "Middle components stay dumb and reusable"],
            verdict="Drill one level for clarity; use provide/inject or a store beyond two."),
    "Drilling is not always wrong — one level is explicit and cheap. It becomes a smell when pass-through props outnumber real props.",
    "Replace this 3+ level prop chain with provide/inject scoped to the feature or a store getter.",
)

c.add(
    "state-mutation", "State Mutation", "FOUNDATIONS · STATE",
    "Mutating shared state in place hides the moment of change. Replace the object so the change is visible and traceable.",
    compare(["user.name = 'Ada' inside a child",
             "Nested object changed without a new reference",
             "shallowRef / memoized children never notice",
             "Undo and debugging become guesswork"],
            ["user.value = { ...user.value, name: 'Ada' }",
             "New reference marks the exact change point",
             "Watchers compare old vs new reliably",
             "Time travel and rollback stay possible"],
            verdict="Replace at the boundary; mutate only inside a local, owned scope."),
    "In-place mutation breaks shallow reactivity and memoization because nothing detects a new identity.",
    "Convert this nested mutation into a single immutable reassignment of the top-level value.",
)

c.add(
    "derived-state", "Derived State", "FOUNDATIONS · STATE",
    "If a value can be computed from existing state, do not store it. Derive it and let caching do the work.",
    code(["const filtered = ref([])",
          "watch(items, () => {",
          "  filtered.value = items.value.filter(...)",
          "})",
          "// two states can disagree"],
         ["const filtered = computed(() =>",
          "  items.value.filter(isVisible))",
          "",
          "// recomputes only when items changes",
          "// impossible to go out of sync"],
         note="computed() caches by dependency; a watcher copies state and creates a second source of truth."),
    "Derived state stored in a ref needs a watcher to stay correct. computed() makes correctness structural.",
    "Replace this ref + watcher pair with computed() and delete the synchronized copy.",
)

c.add(
    "reactive-coupling", "Reactive Coupling", "FOUNDATIONS · REACTIVITY",
    "When one render touches unrelated reactive values, every unrelated change re-renders it. Narrow the dependency.",
    compare(["One big reactive() object read by every widget",
             "A change to a date re-renders the chart",
             "Deep proxies track the entire object graph",
             "Render cost grows with app size"],
            ["Small refs / shallowRef per concern",
             "Each component reads only what it renders",
             "computed() isolates derived work",
             "Changes stay local to their consumers"],
            verdict="Coupling is measured in re-renders: fewer dependencies, fewer surprises."),
    "Reactivity is a dependency graph. The bigger the graph each component subscribes to, the more work every update causes.",
    "Split this shared reactive object into focused refs and read only the field each component needs.",
)

c.add(
    "side-effects", "Side Effects", "FOUNDATIONS · ARCHITECTURE",
    "Fetching, timers, logging and analytics are effects. Give them a named home and a cleanup path.",
    layers([("TRIGGER", "Action / watcher / lifecycle", "Say what happened, not how to do it."),
            ("EFFECT", "Service or composable", "Fetch, subscribe, persist — one place per effect."),
            ("CLEANUP", "onScopeDispose / AbortController", "Cancel before the owner disappears."),
            ("RESULT", "State update", "Only the result touches reactive state.")],
           note="An effect without cleanup is a leak waiting for a route change."),
    "Effects scattered in templates and computed getters run unpredictably and are hard to cancel.",
    "Move this effect into the composable, attach onScopeDispose, and return a cancel function.",
)

c.add(
    "composable-extraction", "Composable Extraction", "FOUNDATIONS · ARCHITECTURE",
    "When a component mixes state, Effects and markup, extract the behaviour into use<Feature>() and leave the view declarative.",
    compare(["400-line .vue file",
             "Fetching, filtering, timers and markup interleaved",
             "Hard to test without mounting the DOM",
             "Second screen copies the same logic"],
            ["useOrders() returns state + actions",
             "Template only binds what it needs",
             "Logic is testable as plain TypeScript",
             "Second screen reuses the same composable"],
            verdict="Extract by behaviour, not by line count: when logic has a name, it has a home."),
    "Composables are the Vue unit of reusable stateful logic. They keep business rules out of templates and out of global stores.",
    "Extract this component's fetch + filter + reset logic into use<Feature>.ts and keep only bindings in the view.",
)

c.add(
    "reactivity-leaks", "Reactivity Leaks", "FOUNDATIONS · REACTIVITY",
    "A proxy nested inside a plain wrapper can silently lose reactivity — or keep tracking long after it is needed.",
    compare(["ref(largeObject) deeply proxies every nested value",
             "Third-party instance wrapped in reactive()",
             "Destructured props lose their connection",
             "Unused computed keeps dependencies alive"],
            ["shallowRef for big or external objects",
             "toRaw / markRaw for instances that must stay plain",
             "toRefs when destructuring props",
             "Stop watchers that are no longer needed"],
            verdict="Keep only the reactive surface you actually render."),
    "Deep reactivity is convenient for small objects and expensive for large ones. Leaks also happen when tracking outlives the component.",
    "Audit this file for reactive() around third-party instances and narrow it with shallowRef or markRaw.",
)

c.add(
    "watcher-abuse", "Watcher Abuse", "FOUNDATIONS · REACTIVITY",
    "A watcher that recomputes, re-fetches and re-writes state is usually a computed, an effect or an event in disguise.",
    code(["watch(form, () => {",
          "  total.value = calc(form)   // derived",
          "  fetchResults(form)         // effect",
          "  log(form)                  // debug",
          "}, { deep: true })",
          "// runs on every nested keystroke"],
         ["const total = computed(() => calc(form.value))",
          "watch([id], ([next]) => fetchResults(next))",
          "// on submit: log once",
          "// effects only when a real dependency changes"],
         note="Three jobs in one deep watcher means three hidden render triggers."),
    "Watchers are for crossing boundaries: state → network, state → storage. Use computed for values.",
    "Replace this watcher: move derived work to computed, narrow dependencies, and keep only the side effect.",
)

c.add(
    "memory-leaks", "Memory Leaks", "FOUNDATIONS · REACTIVITY",
    "Listeners, timers and subscriptions that outlive a component keep the whole tree alive in memory.",
    compare(["addEventListener in onMounted, never removed",
             "setInterval left running after unmount",
             "WebSocket or query subscription not closed",
             "Detached DOM nodes still referenced"],
            ["onUnmounted(() => removeEventListener(...))",
             "clearInterval(timer) in onScopeDispose",
             "AbortController + subscription.unsubscribe()",
             "No retained references to old nodes"],
            verdict="Every resource you create needs a matching teardown in the same file."),
    "Leaks are invisible in development and fatal after a hundred route changes. Cleanup is part of the feature, not an afterthought.",
    "Add teardown for every listener/timer/subscription created in this component and verify with the heap profiler.",
)

c.add(
    "template-bloat", "Template Bloat", "FOUNDATIONS · RENDER",
    "Thousands of nodes and inline expressions make the renderer do work on every update.",
    compare(["2,000 v-for rows always mounted",
             "formatCurrency() called in the template",
             "Nested v-if/v-show chains",
             "Inline object literals recreate on render"],
            ["Virtualize long lists",
             "Precompute formatted values in computed",
             "Split conditionals into child components",
             "v-memo on rows keyed by primitive values"],
            verdict="Every node you avoid creating is a node you never have to diff."),
    "Vue's renderer is fast, but it still walks every node. Shrink the tree first, then optimize the diff.",
    "Virtualize this list and move the inline formatting calls into a computed map before touching reactivity.",
)

c.add(
    "type-safety", "Type Safety", "FOUNDATIONS · QUALITY",
    "Types move whole classes of bugs from runtime to editor time — especially at API and prop boundaries.",
    compare(["props: {} and any everywhere",
             "API response shape assumed, not checked",
             "Renaming a field breaks three screens silently",
             "Refactors rely on grep and hope"],
            ["defineProps<{ id: number; status: Status }>()",
             "Typed service returns a validated DTO",
             "Compiler flags every stale usage",
             "Refactors become mechanical"],
            verdict="Types pay off most at boundaries: props, stores, services and env variables."),
    "Type safety is not ceremony; it is the cheapest regression test you run on every keystroke.",
    "Type this component's props and its service response, then run vue-tsc and fix the reported errors.",
)

c.add(
    "god-component", "God Component", "FOUNDATIONS · ARCHITECTURE",
    "One component that fetches, decides, formats and renders every state becomes impossible to reason about or reuse.",
    compare(["One 1,200-line Dashboard.vue",
             "Owns 6 unrelated features",
             "Any edit risks every feature",
             "Cannot reuse one widget alone"],
            ["Feature folders with focused views",
             "Each widget owns one concern",
             "Shared logic in composables",
             "Blast radius of an edit is one file"],
            verdict="Split by reason to change, not by visual proximity."),
    "Large components concentrate coupling. The goal is not tiny files for their own sake but small reasons to change.",
    "List the reasons this component changes and split it along those boundaries into child views and composables.",
)

c.add(
    "presentational-components", "Presentational Components", "FOUNDATIONS · ARCHITECTURE",
    "A dumb component receives data and emits events. It has no store, no fetching and no knowledge of the app.",
    matrix(("More app knowledge →", "More presentation ↓"),
           [("Dumb widget", "Pure props in, events out; reusable everywhere."),
            ("Smart-looking widget", "Reads a store but only renders — acceptable at feature edges."),
            ("Pure layout", "Slots and styles only; no state at all."),
            ("Container", "Knows the app and dispatches work — keep it thin.")],
           note="The test: can you drop the component into another app without importing your store?"),
    "Presentational components are easy to test, storybook and reuse because they have no hidden dependencies.",
    "Remove store imports from this widget and pass the required data and callbacks as props/emits instead.",
)

c.add(
    "container-components", "Container Components", "FOUNDATIONS · ARCHITECTURE",
    "The container knows where data comes from; the children only know how to display it.",
    anatomy(("CONTAINER", "Connects app state to a view"),
            [("Fetch / query", "Reads server state via the data layer."),
             ("Store bindings", "Reads client state via typed getters."),
             ("Handlers", "Translates UI events into actions."),
             ("Child views", "Receive plain props and emit intent.")],
            note="Keep the container thin: wiring, no formatting, no deep markup."),
    "The container/presentational split localizes app knowledge so the expensive UI tests can stay shallow.",
    "Move this page's store reads and fetch calls into a container and leave the markup in a props-only child.",
)

c.add(
    "high-cohesion", "High Cohesion", "FOUNDATIONS · ARCHITECTURE",
    "Code that changes for the same reason lives together. That is what a feature folder really means.",
    matrix(("Cohesion →", "Change frequency ↑"),
           [("Feature folder", "View + composable + API + types for one domain."),
            ("Mixed folder", "File type grouping hides domain boundaries."),
            ("Scattered logic", "One feature change touches five folders."),
            ("Duplicate domain", "Two teams own the same concept differently.")],
           note="If two files always change together, put them together."),
    "Cohesion reduces merge conflicts and makes ownership obvious because one domain is one place.",
    "Move this feature's view, composable, API module and types into src/features/<domain>/.",
)

c.add(
    "low-coupling", "Low Coupling", "FOUNDATIONS · ARCHITECTURE",
    "Components should depend on narrow interfaces, not on each other's internals.",
    compare(["Import a sibling's store and reach into its nested state",
             "Props carry whole app objects",
             "Changing component A breaks component B",
             "Tests need the entire app mounted"],
            ["Import a typed service function or small store getter",
             "Props carry the minimum data needed",
             "Interfaces stay stable while internals change",
             "Tests mount one component with fake props"],
            verdict="Depend on what a module promises, never on how it is built."),
    "Low coupling is what makes parallel work possible: teams can change their own code without coordinating every edit.",
    "Replace this component's import of a sibling's internals with a typed service call or emitted event.",
)

c.add(
    "composition-over-inheritance", "Composition over Inheritance", "FOUNDATIONS · ARCHITECTURE",
    "Vue components compose through slots and props. Deep component inheritance creates fragile, hidden behaviour.",
    compare(["BaseForm → AuthForm → LoginForm inheritance chain",
             "Hidden overrides decide what renders",
             "One base change breaks every descendant",
             "Behaviour reused only through the chain"],
            ["<BaseForm><EmailField /><Submit /></BaseForm>",
             "useForm() shared by both forms",
             "Slots choose content, props choose behaviour",
             "Each piece can be swapped independently"],
            verdict="Prefer small pieces assembled explicitly over behaviour inherited implicitly."),
    "Composition makes data flow visible. Inheritance hides it in a chain you have to reconstruct mentally.",
    "Replace this component inheritance with a wrapper component using slots plus a shared composable.",
)

c.add(
    "immutability", "Immutability", "FOUNDATIONS · STATE",
    "Treat state snapshots as values. A new reference means something changed; the same reference means nothing did.",
    compare(["array.push(item) on a shallowRef array",
             "Nested assignment bypasses watchers",
             "Old and new snapshots are the same object",
             "Undo caches point at mutated data"],
            ["list.value = [...list.value, item]",
             "Replace at the level shallowRef tracks",
             "Old snapshots stay intact for diffing",
             "Undo becomes a stack of references"],
            verdict="Immutable updates turn 'did it change?' into a reference equality check."),
    "Immutability is the contract that makes memoization, shallow reactivity and time-travel debugging work.",
    "Rewrite this state change as a top-level reassignment and verify the memoized child still updates.",
)

c.add(
    "dependency-injection", "Dependency Injection", "FOUNDATIONS · ARCHITECTURE",
    "Supply dependencies from outside instead of constructing them inside. The consumer stays testable and swappable.",
    flow([("PROVIDE", "Root supplies an API client"),
          ("INJECT", "Feature requests the interface"),
          ("USE", "Composable calls typed methods"),
          ("TEST", "Inject a fake client")],
          note="In Vue, provide/inject is for dependencies; Pinia or Vue Query is for shared state."),
    "Hard-coded imports bind a component to one implementation. Injection lets tests replace it without mocking modules.",
    "Provide this API client at the feature root and inject it into the composable instead of importing it directly.",
)

c.add(
    "inversion-of-control", "Inversion of Control", "FOUNDATIONS · ARCHITECTURE",
    "Frameworks call your code. Let Vue own the lifecycle and keep your logic in hooks it can schedule and tear down.",
    compare(["Manual DOM queries + manual render timing",
             "Polling to detect changes",
             "Cleanup forgotten when unmounted",
             "Ordering bugs across features"],
            ["onMounted / watch / computed hook into Vue",
             "Reactive dependencies drive updates",
             "onScopeDispose handles teardown",
             "Framework orders the lifecycle"],
            verdict="Work with the framework scheduler; do not build a second one inside the app."),
    "Fighting the scheduler produces double renders and race conditions. Hooks are the contract for when code runs.",
    "Replace this manual DOM polling with a watcher/computed and move cleanup into onScopeDispose.",
)

c.add(
    "event-driven-architecture", "Event-Driven Architecture", "FOUNDATIONS · ARCHITECTURE",
    "Events describe what happened. Producers do not need to know who reacts, which keeps features independent.",
    flow([("USER", "Clicks, types, navigates"),
          ("EMIT", "Component announces an intent"),
          ("BUS / STORE", "Typed event or action dispatched"),
          ("HANDLERS", "Independent features react"),
          ("STATE", "Result updates the canonical state")],
          note="Use events for cross-feature notifications; use direct props for parent-child communication."),
    "Events decouple producers from consumers, but untyped global buses become invisible spaghetti. Keep the contract typed.",
    "Replace this cross-feature callback chain with a typed event or store action and document its consumers.",
)

c.add(
    "state-machines", "State Machines", "FOUNDATIONS · STATE",
    "Model UI as explicit states and allowed transitions. Impossible states become unrepresentable.",
    flow([("IDLE", "Nothing started"),
          ("LOADING", "Request in flight"),
          ("SUCCESS", "Data ready"),
          ("ERROR", "Failure with retry"),
          ("STALE", "Refreshing old data")],
          note="A boolean soup (isLoading + isError + hasData) permits 8 combinations; a machine permits four."),
    "Explicit states remove the impossible combinations that cause blank screens and double submissions.",
    "Replace these booleans with a discriminated union status and render one branch per state.",
)

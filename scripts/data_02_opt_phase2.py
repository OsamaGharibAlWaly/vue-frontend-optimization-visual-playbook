"""Pillar 1, Phase 2: heavy components and list rendering."""

from catalogue import bullets, catalogue, code, compare, flow, layers, metrics, timeline

c = catalogue(
    "02-optimization/phase-2-rendering", "PILLAR 1 · OPTIMIZATION",
    "Phase 2 targets the DOM and the frame budget. Scope the prompt to src/views, src/pages and complex feature "
    "components; skip small UI primitives like buttons and inputs.",
)

c.add(
    "phase-2-overview", "Phase 2 Overview: Heavy Component & List Rendering", "PHASE 2 · THE PLAN",
    "Five levers keep the DOM small and the renderer idle: async components, KeepAlive, virtualization, v-once and v-memo.",
    flow([("ASYNC", "Load heavy widgets on demand"),
          ("KEEP", "Cache stateful views"),
          ("WINDOW", "Render only visible rows"),
          ("FREEZE", "v-once for static blocks"),
          ("MEMO", "v-memo keyed on primitives")],
          note="Scope: src/views/*, src/pages/*, modals, charts, tables and large lists only."),
    "Rendering work is bounded by the number of nodes and how often they are touched. This phase shrinks both numbers.",
    "Identify the heaviest views, modals and large lists in src/views and src/components. Skip small UI primitives.",
)

c.add(
    "define-async-component", "defineAsyncComponent for Heavy Widgets", "PHASE 2 · ASYNC",
    "A modal, chart or rich editor that opens rarely should not be in the initial bundle at all.",
    code(["// Always loaded at startup",
          "import HeavyChart from './HeavyChart.vue'",
          "",
          "<HeavyChart v-if=\"showChart\" />",
          "// 480 KB in the entry chunk"],
         ["import { defineAsyncComponent } from 'vue'",
          "const HeavyChart = defineAsyncComponent({",
          "  loader: () => import('./HeavyChart.vue'),",
          "  loadingComponent: ChartSkeleton,",
          "  errorComponent: ChartError,",
          "  delay: 200, timeout: 10000",
          "})"],
         note="Keep the loader function at module scope so Vue can cache the resolved component."),
    "Async components convert a permanent download cost into a one-time cost paid only by users who open the feature.",
    "Wrap each heavy conditional modal, drawer, editor and chart with defineAsyncComponent and a skeleton fallback.",
)

c.add(
    "keep-alive", "KeepAlive for Stateful Views", "PHASE 2 · CACHING",
    "When users switch tabs often, unmounting and rebuilding the view wastes work and loses scroll/filter state.",
    code(["<component :is=\"currentView\" />",
          "// every switch: destroy + recreate",
          "// filters reset, scroll jumps"],
         ["<KeepAlive :max=\"5\">",
          "  <component :is=\"currentView\" />",
          "</KeepAlive>",
          "// inactive views cached, state kept",
          "// max bounds memory usage"],
         note="Use onActivated/onDeactivated to pause timers and refresh data when returning to a view."),
    "KeepAlive trades a bounded amount of memory for instant tab switching and preserved state — a good deal for navigation.",
    "Wrap dynamic tab/route views in <KeepAlive :max=\"5\"> and pause timers in onDeactivated.",
)

c.add(
    "virtual-scroll-impl", "Virtual Scrolling Implementation", "PHASE 2 · LISTS",
    "A virtualizer measures a scroll container, renders a window of rows and pads the rest with spacers.",
    code(["<div v-for=\"row in 10000Rows\"",
          "     :key=\"row.id\" class=\"row\">",
          "  {{ row.name }}",
          "</div>",
          "// 10,000 nodes sized and diffed"],
         ["<VirtualList v-slot=\"{ item }\"",
          "  :data=\"rows\" :item-size=\"48\">",
          "  <Row :item=\"item\" />",
          "</VirtualList>",
          "// ~20 nodes + two spacers"],
         note="Fixed item sizes are fastest; measured estimates work for variable-height rows."),
    "The virtualizer keeps DOM size constant, so scrolling a million rows costs the same as scrolling one hundred.",
    "Replace this 100+ item v-for with @tanstack/vue-virtual using a fixed row height where possible.",
)

c.add(
    "v-once", "v-once: Render Once, Skip Forever", "PHASE 2 · MEMO",
    "Static blocks never need a diff. v-once tells Vue to render them once and skip future updates entirely.",
    code(["<header>",
          "  <h1>{{ pageTitle }}</h1>",
          "  <p>{{ staticMarketingCopy }}</p>",
          "</header>",
          "// re-diffed on every state change"],
         ["<header v-once>",
          "  <h1>{{ pageTitle }}</h1>",
          "  <p>{{ staticMarketingCopy }}</p>",
          "</header>",
          "// skipped on every future render"],
         note="Only use it when the content truly never changes — a 'static' string that updates becomes a bug."),
    "v-once is the cheapest memoization: no dependencies to track, no comparisons to make.",
    "Add v-once to template blocks whose content never changes after the first render, then verify with Devtools.",
)

c.add(
    "v-memo", "v-memo: Cache an Expensive Subtree", "PHASE 2 · MEMO",
    "Give Vue a list of primitive dependencies. The subtree re-renders only when one of them changes.",
    code(["<div v-for=\"item in rows\" :key=\"item.id\">",
          "  <ExpensiveRow :item=\"item\"",
          "    :selected=\"item.id === selectedId\" />",
          "</div>",
          "// every hover re-renders all rows"],
         ["<div v-for=\"item in rows\" :key=\"item.id\"",
          "     v-memo=\"[item.id, item.updatedAt,",
          "               item.id === selectedId]\">",
          "  <ExpensiveRow :item=\"item\" />",
          "</div>"],
         note="v-memo dependencies must be primitives or stable references; new objects every render defeat it."),
    "v-memo is surgical: it avoids diff work for rows whose visible inputs did not change.",
    "Add v-memo=\"[...]\" to expensive v-for items using only primitive keys such as item.id and item.selected.",
)

c.add(
    "layout-thrashing", "Layout Thrashing Prevention", "PHASE 2 · LAYOUT",
    "Reading layout after writing styles forces the browser to recalculate synchronously, again and again in a loop.",
    timeline([("write style", 0.00, 0.18, "rose"),
              ("read offsetHeight", 0.18, 0.22, "amber"),
              ("forced reflow", 0.40, 0.18, "rose"),
              ("write + read...", 0.58, 0.26, "amber"),
              ("16.7ms budget gone", 0.84, 0.14, "violet")],
             note="Batch all reads first, then all writes — or use requestAnimationFrame for the write phase."),
    "Alternating reads and writes inside a loop turns one layout pass into N synchronous passes.",
    "Batch layout reads before writes in this loop and move style writes into a requestAnimationFrame callback.",
)

c.add(
    "reflow-elimination", "Reflow Elimination", "PHASE 2 · LAYOUT",
    "Some properties only repaint; others invalidate layout for the whole subtree. Prefer the cheaper ones.",
    compare(["Animating width / height / top",
             "Changing margins in a loop",
             "Reading layout after each write",
             "Layout recalculated for every frame"],
            ["Animate transform / opacity",
             "Use fixed-size boxes and spacers",
             "Read layout once, outside the loop",
             "Compositor handles the animation"],
            verdict="Reflow is not always avoidable, but it must never be inside an animation loop."),
    "A reflow recalculates positions for descendants. Compositor-only properties skip that work entirely.",
    "Change this animation from width/top to transform and verify in Devtools Rendering paint flashing.",
)

c.add(
    "gpu-compositing", "GPU Compositing: transform & opacity", "PHASE 2 · ANIMATION",
    "transform and opacity can be handled by the compositor without running layout or paint on the main thread.",
    compare(["left: 0 → 300px", "Triggers layout + paint each frame",
             "Main thread busy, frames drop", "Jank under heavy DOM"],
            ["transform: translateX(300px)", "Composited layer moves on GPU",
             "Main thread stays free", "Smooth even with complex UI"],
            verdict="Promote only what animates: too many layers cost memory."),
    "The compositor is a separate thread that can move pre-painted layers. Feed it properties it understands.",
    "Replace these position/size animations with transform and opacity, then record a Performance trace.",
)

c.add(
    "60fps-frame-budget", "The 16.7ms Frame Budget", "PHASE 2 · ANIMATION",
    "At 60fps the browser has about 16.7 ms for JavaScript, style, layout, paint and compositing — together.",
    metrics([("16.7ms", "Total budget per frame"),
             ("<10ms", "Leave headroom for the browser"),
             ("5ms", "Typical JS budget for smooth UI"),
             ("60fps", "The target users perceive")],
            [("JS + Vue render", 46, "rose"), ("Style + layout", 26, "amber"),
             ("Paint", 18, "violet"), ("Compositing", 10, "green")],
            note="Long tasks over 50ms are the ones Devtools flags; they are guaranteed dropped frames."),
    "Smoothness is a budget, not a feeling. Measure a frame trace and keep your JavaScript share small.",
    "Record a Performance trace of this interaction and reduce the longest task to under 10ms.",
)

c.add(
    "hardware-acceleration", "Hardware Acceleration", "PHASE 2 · ANIMATION",
    "Browsers promote selected elements to GPU layers. The trick is choosing the few elements that benefit.",
    layers([("PROMOTE", "transform / opacity animations", "Compositor can move them without main-thread work."),
            ("HINT", "will-change: transform", "Use sparingly and remove after the animation ends."),
            ("ISOLATE", "contain: paint", "Limit what must be repainted inside the layer."),
            ("AVOID", "Persistent layer explosion", "Each layer costs memory and GPU texture space.")],
           note="Acceleration is a tool for hot animations, not a default style on every element."),
    "Too many promoted layers make things worse. Promote during motion, then remove the hint.",
    "Apply will-change: transform only to the animating element and remove it after transitionend.",
)

c.add(
    "css-containment", "CSS Containment: contain: content", "PHASE 2 · LAYOUT",
    "Containment tells the browser this subtree cannot affect layout or paint outside its box.",
    code([".widget {",
          "  /* browser checks the whole",
          "     document for changes */",
          "}"],
         [".widget {",
          "  contain: content;",
          "  /* layout + paint + style",
          "     bounded to this box */",
          "}",
          "/* or: contain: layout paint; */"],
         note="Contained elements need explicit size; otherwise their contents can collapse."),
    "In large dashboards, containment reduces the scope of invalidation from the page to one widget.",
    "Add contain: content to independent dashboard widgets that have explicit dimensions.",
)

c.add(
    "skeleton-screens", "Skeleton Screens", "PHASE 2 · PERCEIVED SPEED",
    "A shaped placeholder communicates progress and reserves space, so the layout does not jump when data arrives.",
    timeline([("Navigate", 0.00, 0.10, "cyan"),
              ("Chunk fetch", 0.10, 0.30, "amber"),
              ("Skeleton visible", 0.20, 0.44, "teal"),
              ("Data arrives", 0.64, 0.12, "green"),
              ("Content swaps in", 0.76, 0.20, "violet")],
             note="Match the skeleton's dimensions to the real content to avoid Cumulative Layout Shift."),
    "Skeletons do not make data faster; they make waiting legible and prevent layout jumps.",
    "Add a skeleton loadingComponent to this async view with the same dimensions as the final content.",
)

c.add(
    "progressive-hydration", "Progressive Hydration", "PHASE 2 · DELIVERY",
    "Server-rendered HTML is visible immediately; hydration attaches interactivity feature by feature instead of all at once.",
    flow([("HTML", "Server sends complete markup"),
          ("PAINT", "User sees content instantly"),
          ("CRITICAL", "Hydrate visible interactive parts"),
          ("IDLE", "Hydrate the rest on demand"),
          ("LIVE", "Full app interactive")],
          note="Route-level code splitting and islands keep hydration work proportional to what is on screen."),
    "Full-app hydration can block the main thread even when the page already looks ready. Progressive hydration spreads the cost.",
    "Evaluate hydrating only this page's interactive islands first; defer below-the-fold widgets to idle time.",
)

c.add(
    "render-profiling", "Profile Renders Before Guessing", "PHASE 2 · PROOF",
    "Vue Devtools shows which components rendered and how long each took. Start there, not with a favorite directive.",
    bullets([("Enable render tracking", "Vue Devtools → Performance → record an interaction."),
             ("Find repeat offenders", "Components that render on unrelated state changes."),
             ("Check component cost", "A 30 ms row component needs memoization more than a wrapper does."),
             ("Check node count", "Thousands of nodes call for virtualization."),
             ("Patch one thing", "Keep attribution: one concept, one commit."),
             ("Re-record", "Compare the same interaction after the change.")],
            note="If the profile shows network time rather than render time, this phase is not the bottleneck."),
    "Measurement prevents cargo-cult optimization: v-once on a fast block changes nothing, while virtualizing a list changes everything.",
    "Record one interaction in Vue Devtools, name the most expensive component, and apply one targeted fix.",
)

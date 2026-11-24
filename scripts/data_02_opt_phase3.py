"""Pillar 1, Phase 3: reactivity and event optimization."""

from catalogue import catalogue, code, compare, timeline

c = catalogue(
    "02-optimization/phase-3-reactivity", "PILLAR 1 · OPTIMIZATION",
    "Phase 3 works inside <script setup>, composables and Pinia stores. The rule: track only what you render, "
    "compute instead of copying, and cancel anything that outlives a component.",
)

c.add(
    "phase-3-overview", "Phase 3 Overview: Reactivity & Events", "PHASE 3 · THE PLAN",
    "Five changes reduce how often code runs: shallow reactivity, computed caching, targeted watchers, debounce and throttle.",
    timeline([("Deep reactive graph", 0.00, 0.42, "rose"),
              ("Shallow surface", 0.25, 0.30, "teal"),
              ("computed cache", 0.40, 0.26, "green"),
              ("Targeted watchers", 0.58, 0.24, "cyan"),
              ("Debounce / throttle", 0.74, 0.24, "amber")],
             note="Scope: <script setup>, src/composables/*, src/stores/* only. Skip static templates and CSS."),
    "Reactivity is invisible until it is excessive. This phase narrows dependencies and controls event frequency.",
    "Audit <script setup> blocks and Pinia stores in src/stores/* for reactivity and event bottlenecks only.",
)

c.add(
    "shallow-ref", "shallowRef for Large or External Objects", "PHASE 3 · REACTIVITY",
    "shallowRef tracks only .value replacement. Perfect for big API arrays and third-party instances.",
    code(["const rows = ref([]) // deep proxy of every row",
          "const chart = reactive(new Chart(el))",
          "",
          "rows.value[0].name = 'Ada' // tracked deeply",
          "// thousands of nested proxies created"],
         ["const rows = shallowRef([])",
          "const chart = shallowRef(null)",
          "",
          "rows.value = [...rows.value, newRow]",
          "chart.value = new Chart(el)",
          "// only .value is tracked"],
         note="With shallowRef, mutating nested fields will not trigger updates — always replace .value."),
    "Deep proxies cost memory and tracking time. If you always replace the whole object, shallowRef is strictly cheaper.",
    "Replace ref/reactive with shallowRef for large read-only API arrays and third-party instances, using .value reassignment.",
)

c.add(
    "shallow-reactive", "shallowReactive for Flat Shapes", "PHASE 3 · REACTIVITY",
    "Make only root-level properties reactive when nested objects are treated as opaque values.",
    code(["const state = reactive({",
          "  filters: { q: '', tags: [] },",
          "  rows: [/* 5,000 objects */]",
          "})",
          "// deep conversion walks everything"],
         ["const state = shallowReactive({",
          "  filters: { q: '', tags: [] },",
          "  rows: []",
          "})",
          "state.filters = { q: 'vue' }",
          "// replace, do not mutate nested"],
         note="Use shallowReactive when the object has a stable shape but expensive nested contents."),
    "shallowReactive keeps the familiar object API while avoiding deep proxy conversion on large nested data.",
    "Convert this large reactive object to shallowReactive and replace nested objects instead of mutating them.",
)

c.add(
    "computed-caching", "computed Caching Over Template Calls", "PHASE 3 · REACTIVITY",
    "A method call in a template runs on every render. A computed runs only when its dependencies change.",
    code(["<template>",
          "  <li v-for=\"r in filteredRows()\">",
          "    {{ formatMoney(r.price) }}",
          "</li>",
          "</template>",
          "// two calls on every render"],
         ["const filteredRows = computed(() =>",
          "  rows.value.filter(matchesQuery))",
          "const formatted = computed(() =>",
          "  filteredRows.value.map(r => ({",
          "    ...r, price: formatMoney(r.price) })))"],
         note="computed caches by dependency; unrelated state changes do not recompute it."),
    "Moving work out of the template turns 'run every render' into 'run when inputs change'.",
    "Replace expensive function calls in this template with computed properties and verify caching in a test.",
)

c.add(
    "deep-watchers", "Replace Deep Watchers With Targeted Getters", "PHASE 3 · REACTIVITY",
    "deep: true walks the whole nested tree on every change. Watch the exact field you actually care about.",
    code(["watch(form, () => {",
          "  validate(form)",
          "}, { deep: true })",
          "// runs for any nested mutation",
          "// walks every nested property"],
         ["watch(",
          "  () => [form.value.email, form.value.age],",
          "  ([email, age]) => validate({ email, age })",
          ")",
          "// only the two fields we read"],
         note="For a single field, watch(() => obj.value.field) is enough — no deep option needed."),
    "A deep watcher on a large object is both broad and expensive. Targeted getters make intent obvious.",
    "Replace watch(..., { deep: true }) in this file with getters for the specific nested properties.",
)

c.add(
    "debounce-search", "Debounce Search Inputs", "PHASE 3 · EVENTS",
    "One request after the user stops typing beats seven requests for seven keystrokes.",
    code(["<input @input=\"onInput\" />",
          "",
          "function onInput(e) {",
          "  query.value = e.target.value",
          "  fetchResults(query.value)",
          "} // one API call per keystroke"],
         ["const onInput = useDebounceFn((e) => {",
          "  query.value = e.target.value",
          "  fetchResults(query.value)",
          "}, 300)",
          "onScopeDispose(() => onInput.cancel?.())"],
         note="VueUse's useDebounceFn/useDebounce already handle cancellation with the component scope."),
    "Debouncing reduces network load and render churn while preserving the feeling of instant feedback in the input itself.",
    "Add a 300ms debounce to this search/filter handler and cancel it when the component unmounts.",
)

c.add(
    "throttle-scroll", "Throttle Scroll & Resize Handlers", "PHASE 3 · EVENTS",
    "Native scroll and resize fire far faster than a frame. Throttle to one callback per animation frame.",
    code(["window.addEventListener('scroll',",
          "  () => updateHeader())",
          "// 100+ calls per second",
          "// layout read each time"],
         ["const onScroll = useThrottleFn(() => {",
          "  headerHidden.value = window.scrollY > 80",
          "}, 16) // one call per frame",
          "onScopeDispose(() =>",
          "  window.removeEventListener('scroll', onScroll))"],
         note="Prefer requestAnimationFrame for visual updates; use passive listeners when you never call preventDefault."),
    "Throttling keeps visual feedback smooth without saturating the main thread with redundant work.",
    "Throttle this scroll/resize handler to one call per frame and remove the listener on unmount.",
)

c.add(
    "race-fix", "Fixing Async Race Conditions", "PHASE 3 · CONCURRENCY",
    "When a newer request starts, cancel the older one — or tag results so stale answers can be discarded.",
    timeline([("Request A", 0.00, 0.48, "rose"),
              ("abort A", 0.34, 0.12, "amber"),
              ("Request B", 0.30, 0.38, "green"),
              ("B result accepted", 0.70, 0.16, "teal"),
              ("A result ignored", 0.68, 0.22, "violet")],
             note="Vue Query handles this by query key; AbortController works for manual fetches."),
    "A stale response overwriting a fresh one looks like a random bug. Cancellation makes ordering deterministic.",
    "Add AbortController to this watcher-driven fetch and abort the previous request before starting the next.",
)

c.add(
    "idempotent-actions", "Idempotent Actions & Retries", "PHASE 3 · RESILIENCE",
    "A retried mutation must not create a second order. Pair a client lock with a server-side key.",
    code(["async function submit() {",
          "  await api.createOrder(data)",
          "} // double click = two orders",
          "// retry on failure duplicates"],
         ["const pending = ref(false)",
          "async function submit() {",
          "  if (pending.value) return",
          "  pending.value = true",
          "  try { await api.createOrder(data,",
          "         { idempotencyKey: key }) }",
          "  finally { pending.value = false }",
          "}"],
         note="The UI lock is UX; the idempotency key is correctness."),
    "Client-side guards reduce accidents; only a server-side key makes retries genuinely safe.",
    "Add a pending guard and an idempotency key to this mutation before enabling automatic retries.",
)

c.add(
    "reactivity-leak-fix", "Fixing Reactivity Leaks", "PHASE 3 · REACTIVITY",
    "A memoized child that never updates usually means a shallow reference was mutated instead of replaced.",
    compare(["const rows = shallowRef([])",
             "rows.value.push(newRow) // no trigger",
             "v-memo child stays stale",
             "Devtools shows no render"],
            ["rows.value = [...rows.value, newRow]",
             "New reference triggers shallowRef",
             "v-memo sees changed item list",
             "Child updates exactly once"],
            verdict="shallow is fast only when you respect its one tracking rule."),
    "Switching to shallowRef without switching to immutable updates is the most common cause of 'broken reactivity' reports.",
    "Audit shallowRef usages for in-place mutation and convert each to a top-level reassignment.",
)

c.add(
    "watcher-cleanup", "Watcher Cleanup & stopHandle", "PHASE 3 · REACTIVITY",
    "Watchers created inside effects can outlive the scope that made them. Keep them tied to a scope or stop them explicitly.",
    code(["watchEffect((onCleanup) => {",
          "  const sub = source.subscribe(fn)",
          "  // no teardown",
          "})",
          "// subscription lives forever"],
         ["const stop = watchEffect((onCleanup) => {",
          "  const sub = source.subscribe(fn)",
          "  onCleanup(() => sub.unsubscribe())",
          "})",
          "onScopeDispose(stop)"],
         note="Component-scoped watchers stop automatically; manually created ones need a scope or stop call."),
    "Cleanup hooks are part of the watcher, not an optional courtesy — they prevent duplicated side effects over time.",
    "Register onCleanup and onScopeDispose for every watcher in this composable that subscribes to an external source.",
)

c.add(
    "memory-leak-fix", "Fixing Memory Leaks", "PHASE 3 · RESILIENCE",
    "After repeated navigation, heap size should return to baseline. If it grows, something still holds a reference.",
    compare(["Listeners attached in setup, never removed",
             "setInterval continues after unmount",
             "Cache grows without eviction",
             "Heap climbs on every route switch"],
            ["onScopeDispose removes listeners",
             "clearInterval in the same file",
             "Bounded cache with max entries",
             "Heap returns to baseline"],
            verdict="Verify in Devtools Memory: take three snapshots after three navigations."),
    "Leaks rarely show up in tests; they show up after a user has been in the app for an hour.",
    "Add teardown for every listener/timer in this component and verify the heap across three mount cycles.",
)

c.add(
    "template-bloat-fix", "Fixing Template Bloat", "PHASE 3 · RENDER",
    "When every row has inline expressions and deeply nested branches, even small state changes re-render the whole area.",
    compare(["{{ formatDate(item.date) }}",
             "v-if chains inside every row",
             "Inline object literals in props",
             "1 render = thousands of allocations"],
            ["Precomputed formatted fields",
             "Child component per row type",
             "Stable props from computed maps",
             "v-memo keyed on primitive fields"],
            verdict="Move computation out of the template before reaching for reactivity primitives."),
    "Template expressions execute in the render context. Removing them reduces per-render allocations and diff complexity.",
    "Move the formatting calls in this template into a computed map and memoize the rows on primitive keys.",
)

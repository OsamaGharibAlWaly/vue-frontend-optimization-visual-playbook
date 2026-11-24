"""Pillar 2, Phase 2: data layer and network resilience."""

from catalogue import anatomy, catalogue, code, cycle, flow, timeline

c = catalogue(
    "03-scaling/phase-2-data-layer", "PILLAR 2 · SCALING",
    "Phase 2 moves HTTP out of components, adds a caching layer for server state, offloads heavy compute and "
    "contains failures with error boundaries.",
)

c.add(
    "scaling-phase-2-overview", "Scaling Phase 2 Overview: Data Layer & Resilience", "SCALE · PHASE 2",
    "Typed services, query caching, workers and error boundaries make the app resilient under real network and data loads.",
    flow([("SERVICES", "Centralize raw HTTP calls"),
          ("QUERY", "Cache + dedupe server state"),
          ("WORKER", "Move heavy transforms off-thread"),
          ("BOUNDARY", "Contain render errors"),
          ("VERIFY", "Test with mocked responses")],
          note="Scope: src/api/*, src/services/*, fetch callers, heavy utilities and top-level layouts."),
    "At scale, data bugs are usually about ownership: who caches, who retries, who handles failure. This phase assigns each.",
    "Centralize fetch calls in typed services, introduce Vue Query, offload heavy transforms and wrap features in error boundaries.",
)

c.add(
    "repository-service-layer", "Repository / Service Layer", "SCALE · PHASE 2",
    "Components ask for domain data; a typed service knows the URL, mapping and error semantics.",
    code(["// Component.vue",
          "const res = await fetch('/api/orders')",
          "const data = await res.json()",
          "if (!res.ok) toast('failed')",
          "// HTTP details in the UI"],
         ["// services/orders.service.ts",
          "export async function listOrders(",
          "  signal?: AbortSignal): Promise<Order[]> {",
          "  const res = await http.get('/orders', { signal })",
          "  return OrderList.parse(res.data)",
          "}"],
         note="One service per domain; one shared HTTP client with interceptors and error mapping."),
    "Centralized services make caching, auth headers and retries possible in one place instead of twenty components.",
    "Move raw fetch/axios calls out of .vue files into typed src/services/<domain>.service.ts modules.",
)

c.add(
    "api-interceptors", "Shared HTTP Interceptors", "SCALE · PHASE 2",
    "Auth headers, CSRF tokens, error normalization and 401 refresh belong in the client, not in every call site.",
    code(["// repeated in 12 components",
          "fetch(url, { headers: {",
          "  Authorization: `Bearer ${token}`",
          "} })",
          "// and no refresh handling"],
         ["// api/http.ts",
          "http.interceptors.request.use(cfg => {",
          "  cfg.headers['X-CSRF-Token'] = csrf()",
          "  return cfg",
          "})",
          "http.interceptors.response.use(ok,",
          "  err => normalizeError(err))"],
         note="Keep refresh rotation in one place to avoid infinite retry loops."),
    "Interceptors enforce consistent transport behaviour, which is especially important for security and observability.",
    "Add shared request/response interceptors for credentials, CSRF headers and normalized errors in this HTTP client.",
)

c.add(
    "tanstack-query", "TanStack Query for Server State", "SCALE · PHASE 2",
    "Server state has different needs from UI state: caching, deduplication, refetch on focus and stale time.",
    code(["// manual cache in a store",
          "if (!rows.value) {",
          "  rows.value = await api.list()",
          "}",
          "// no dedupe, no background refresh"],
         ["const query = useQuery({",
          "  queryKey: ['orders', filters],",
          "  queryFn: ()api.orders.list(filters),",
          "  staleTime: 30_000",
          "})",
          "// cached, deduped, refetched"],
         note="Move fetched data out of Pinia; keep Pinia for UI intent and session state."),
    "Vue Query removes an entire category of loading, caching and invalidation code from components.",
    "Introduce @tanstack/vue-query for this endpoint with a stable query key and a documented staleTime.",
)

c.add(
    "query-dedup", "Request Deduplication", "SCALE · PHASE 2",
    "Five components asking for the same key should cause one network request, not five.",
    timeline([("Comp A requests", 0.00, 0.10, "rose"),
              ("Comp B requests", 0.03, 0.10, "rose"),
              ("Comp C requests", 0.06, 0.10, "rose"),
              ("Deduped single call", 0.16, 0.42, "green"),
              ("Shared result → all", 0.58, 0.34, "cyan")],
             note="A stable query key is what makes deduplication possible; avoid object literals with random keys."),
    "Dedup reduces server load and avoids flicker when several views mount at once.",
    "Replace manual request guards here with a query key that all consumers share, and verify one network call.",
)

c.add(
    "background-refetch", "Background Refetching", "SCALE · PHASE 2",
    "Keep showing cached data while a fresh request runs. Use refetchOnWindowFocus and refetchInterval deliberately.",
    cycle([("CACHED", "Show last good data"),
           ("STALE", "Mark after staleTime"),
           ("REFETCH", "On focus or interval"),
           ("REPLACE", "Swap only on success"),
           ("PERSIST", "Cache stays for next visit")],
          center="QUERY",
          note="Never clear cached data while refetching unless the error is fatal for this screen."),
    "Background refetching makes data fresh without making the UI blank — the same idea as stale-while-revalidate.",
    "Configure staleTime and refetchOnWindowFocus for this query and keep cached data visible during refresh.",
)

c.add(
    "worker-offload", "Offload Heavy Data Transforms", "SCALE · PHASE 2",
    "Large CSV parsing or filtering belongs in a worker so the UI thread never freezes.",
    anatomy(("WEB WORKER", "Compute isolated from the UI"),
            [("Main thread", "Posts raw file as ArrayBuffer."),
             ("Worker", "Parses, filters and aggregates."),
             ("Progress", "Posts periodic progress messages."),
             ("Result", "Main thread receives plain data.")],
            note="Transfer ArrayBuffers to avoid copying; post only the final structured data back."),
    "Workers turn a main-thread freeze into a background task with a progress indicator.",
    "Move this heavy parse/filter into a Vite worker, transfer the buffer and render progress from worker messages.",
)

c.add(
    "error-boundary-scale", "Error Boundaries at Feature Roots", "SCALE · PHASE 2",
    "Wrap each major feature view so one widget's render error cannot blank the whole app.",
    code(["<!-- no containment -->",
          "<AnalyticsWidget />",
          "<OrdersTable />",
          "// one throw = white screen"],
         ["<ErrorBoundary @error=\"report\">",
          "  <template #fallback>",
          "    <WidgetFallback @retry=\"reload\" />",
          "  </template>",
          "  <AnalyticsWidget />",
          "</ErrorBoundary>"],
         note="Return false from onErrorCaptured once handled, and log the component name with the error."),
    "Boundaries turn total failures into local, recoverable ones — a requirement for large apps with many teams.",
    "Wrap each major feature view in a reusable ErrorBoundary using onErrorCaptured with a retry fallback.",
)

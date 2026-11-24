"""Pillar 1, Phase 1: bundle, build and route splitting."""

from catalogue import bullets, catalogue, code, compare, flow, metrics

c = catalogue(
    "02-optimization/phase-1-bundle", "PILLAR 1 · OPTIMIZATION",
    "Phase 1 has the biggest impact for the least work. Scope the prompt to package.json, Vite config, "
    "index.html and the router — do not read unrelated components yet.",
)

c.add(
    "phase-1-overview", "Phase 1 Overview: Bundle, Build & Route Splitting", "PHASE 1 · THE PLAN",
    "Seven levers decide how many bytes arrive and how much JavaScript the browser must parse before first paint.",
    flow([("ROUTES", "Lazy import() per route"),
          ("VITE", "manualChunks + minify + purge"),
          ("TRANSFER", "Brotli/Gzip over the wire"),
          ("HINTS", "Preload critical assets"),
          ("PROOF", "Analyzer + size budget")],
          note="Scope: package.json, vite.config.*, index.html, CSS entry, src/router/* only."),
    "This phase touches configuration, not business logic. That makes it the safest place to start and easiest to measure.",
    "Analyze package.json, vite.config.*, index.html and src/router/* only. Do not scan unrelated component files yet.",
)

c.add(
    "route-code-splitting", "Convert Static Routes to Lazy Routes", "PHASE 1 · ROUTING",
    "A static import puts every page in the entry bundle. A dynamic import gives each route its own chunk.",
    code(["// router/index.ts",
          "import Dashboard from '@/views/Dashboard.vue'",
          "import Reports from '@/views/Reports.vue'",
          "",
          "{ path: '/dashboard', component: Dashboard }",
          "{ path: '/reports', component: Reports }"],
         ["// router/index.ts",
          "const Dashboard = () => import('@/views/Dashboard.vue')",
          "const Reports = () => import('@/views/Reports.vue')",
          "",
          "{ path: '/dashboard', component: Dashboard }",
          "{ path: '/reports', component: Reports }"],
         note="Vue Router only fetches a lazy component when that route is actually visited."),
    "Route-level splitting is the highest leverage change in most Vue apps: one line per route, immediate payload win.",
    "Convert every static route component import in src/router/* to a dynamic () => import(...) import.",
)

c.add(
    "dynamic-import-semantics", "What dynamic import() Actually Returns", "PHASE 1 · ROUTING",
    "import() is a promise of a module. The router understands a function returning that promise as an async component.",
    flow([("CALL", "Router invokes () => import()"),
          ("FETCH", "Browser requests the chunk"),
          ("RESOLVE", "Promise returns module exports"),
          ("DEFAULT", "Vue uses module.default"),
          ("MOUNT", "View appears after fallback")],
          note="Always provide a loading fallback; a blank route feels like a crash."),
    "Understanding the promise contract explains why typeof route.component === 'function' is the test for lazy routes.",
    "Verify each route component is a function, not an imported object, and add a loading fallback for slow networks.",
)

c.add(
    "vite-manual-chunks", "Vite manualChunks: Split Vendors Deliberately", "PHASE 1 · BUILD",
    "Vendor libraries change less often than app code. Separate chunks let returning users keep the cached parts.",
    code(["// vite.config.ts",
          "export default defineConfig({",
          "  build: { rollupOptions: { output: {} } }",
          "})",
          "// one giant vendor chunk"],
         ["manualChunks(id) {",
          "  if (id.includes('node_modules')) {",
          "    if (id.includes('vue')) return 'vue-vendor'",
          "    if (id.includes('echarts')) return 'charts'",
          "    return 'vendor'",
          "  }",
          "}"],
         note="Group by update frequency, not alphabetically. Too many chunks cause request overhead."),
    "Chunking improves caching, not total bytes. Split heavy libraries that change independently of your app code.",
    "Configure build.rollupOptions.output.manualChunks in vite.config.* to isolate vue, vue-router, pinia and chart libraries.",
)

c.add(
    "tree-shaking-build", "Tree-Shaking at Build Time", "PHASE 1 · BUILD",
    "ES modules let Rollup delete unused exports. Side effects and wildcard imports keep dead code alive.",
    compare(["import * as utils from './utils'",
             "CommonJS require() in dependencies",
             "Top-level side effects in modules",
             "Unused chart types still shipped"],
            ["import { formatDate } from './utils'",
             "ES modules + named exports",
             '"sideEffects": false when accurate',
             "Analyzer shows the reduction"],
            verdict="Tree-shaking is a property of module shape. Verify the result, never assume it."),
    "Clean named imports are free performance: the bundler removes code you never call.",
    "Replace wildcard imports in this module with named imports and confirm unused exports disappear from the build.",
)

c.add(
    "css-purging", "CSS Purging & Minification", "PHASE 1 · BUILD",
    "Ship the selectors you use. An unused design-system stylesheet can be larger than the app's JavaScript.",
    compare(["One global 350 KB stylesheet",
             "Every utility class ships",
             "Duplicate rules across features",
             "No minification in production"],
            ["Purge against template file globs",
             "Only used selectors survive",
             "CSS minified and hashed",
             "Critical CSS stays inline"],
            verdict="Purge with care: dynamically constructed class names must be safelisted."),
    "CSS is render-blocking. A smaller stylesheet means the browser can paint sooner.",
    "Enable CSS minification and purging in vite.config.*, and safelist any dynamically built class names.",
)

c.add(
    "brotli-gzip", "Brotli & Gzip Compression", "PHASE 1 · TRANSFER",
    "Text assets compress extremely well. Let the CDN or Vite plugin serve a much smaller payload with the same bytes of meaning.",
    metrics([("~70%", "Typical JS/CSS size reduction"),
             ("br", "Best for modern browsers"),
             ("gzip", "Universal fallback"),
             ("0", "Runtime cost to the app")],
            [("Uncompressed JS", 96, "rose"),
             ("Gzip", 34, "amber"),
             ("Brotli", 24, "green"),
             ("Images (no gain)", 90, "violet")],
            note="Compress text, not already-compressed images or fonts. Check the Content-Encoding response header."),
    "Compression is the cheapest speed win available: no code changes, no risk, large transfer savings.",
    "Add vite-plugin-compression for Brotli/Gzip and verify Content-Encoding: br on the built assets.",
)

c.add(
    "asset-preloading", "Preload Critical Assets", "PHASE 1 · HINTS",
    "Tell the browser about the font or entry chunk it will need immediately, instead of letting it discover them late.",
    code(["<!-- index.html: nothing hinted -->",
          "<html><head>",
          "  <title>App</title>",
          "</head></html>"],
         ["<!-- index.html -->",
          '<link rel="preload" as="font"',
          '  href="/fonts/inter.woff2" crossorigin>',
          '<link rel="preload" as="script"',
          '  href="/src/main.ts">',
          '<link rel="prefetch" as="style"',
          '  href="/next-route.css">'],
         note="preload = needed now. prefetch = needed later. Preloading too much steals bandwidth."),
    "Preloading fixes discovery delay, not download size. Use it for the one or two assets on the critical path.",
    "Add <link rel=\"preload\"> for critical above-the-fold fonts and entry assets in index.html.",
)

c.add(
    "bundle-analyzer", "Vite Bundle Analyzer", "PHASE 1 · PROOF",
    "A picture of the build output turns 'the bundle feels big' into 'this library is 480 KB'.",
    bullets([("rollup-plugin-visualizer", "Generate stats.html on every production build."),
             ("Find the largest tiles", "One dependency usually dominates the chart."),
             ("Check duplication", "Two versions of the same library hide in nested deps."),
             ("Check route chunks", "Confirm heavy pages are not in the entry."),
             ("Set a budget", "Fail CI when chunkSizeWarningLimit is exceeded."),
             ("Keep a baseline", "Compare before and after every phase.")],
            note="Analysis without a baseline is a guess. Save stats.html from before the first change."),
    "The analyzer is the measuring instrument for this entire phase. It tells you which lever is worth pulling.",
    "Add rollup-plugin-visualizer configured to emit stats.html, then run npm run build and inspect the largest chunk.",
)

c.add(
    "web-workers", "Web Workers: Off the Main Thread", "PHASE 1 · EXECUTION",
    "Move heavy parsing and computation to a worker so scrolling and input stay responsive.",
    bullets([("Main thread", "UI events, Vue rendering, layout, paint."),
             ("Worker thread", "CSV parsing, large JSON transforms, sorting."),
             ("Message boundary", "Post structured-cloneable data only."),
             ("Vite syntax", "new Worker(new URL('./parse.worker.ts', import.meta.url), { type: 'module' })."),
             ("Cancellation", "Terminate or ignore stale worker results."),
             ("Measure", "Profile long tasks before and after.")],
            note="Workers add message overhead; they pay off for tens of milliseconds of continuous CPU work."),
    "A 300 ms parse on the main thread is a 300 ms freeze. In a worker it is invisible to the user.",
    "Move this heavy parse/filter into a Vite module worker and post the result back as a plain object.",
)

c.add(
    "bundle-budget", "Bundle Budgets as a Guardrail", "PHASE 1 · GOVERNANCE",
    "A budget makes size a build failure instead of a surprise discovered in production.",
    code(["// vite.config.ts",
          "export default defineConfig({",
          "  build: {",
          "    chunkSizeWarningLimit: 500,",
          "    rollupOptions: { output: { manualChunks } }",
          "  }",
          "})"],
         ["// CI step",
          "- run: npm run build",
          "- run: node scripts/check-budget.mjs",
          "// fail if entry > 200 KB or any",
          "// chunk > 500 KB gzip"],
         note="A warning nobody reads is not a budget. Make the limit fail the pipeline."),
    "Budgets stop regression by one dependency at a time — exactly how bloat actually arrives.",
    "Set build.chunkSizeWarningLimit and add a CI step that fails when the entry or vendor chunk exceeds the budget.",
)

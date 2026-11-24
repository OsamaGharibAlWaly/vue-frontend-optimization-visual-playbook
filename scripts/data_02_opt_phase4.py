"""Pillar 1, Phase 4: media and rendering architecture."""

from catalogue import bullets, catalogue, code, compare, decision, flow, timeline

c = catalogue(
    "02-optimization/phase-4-media-ssr", "PILLAR 1 · OPTIMIZATION",
    "Phase 4 is the last optimization phase. Inspect image usage, public/ assets and package.json — "
    "evaluate SSR/SSG in writing, but never migrate a framework automatically.",
)

c.add(
    "phase-4-overview", "Phase 4 Overview: Media & Rendering Architecture", "PHASE 4 · THE PLAN",
    "Images usually dominate payload, while SSR/SSG decisions dominate First Contentful Paint and SEO.",
    flow([("INVENTORY", "Find every img / picture"),
          ("FORMAT", "AVIF / WebP with fallbacks"),
          ("ATTRIBUTES", "lazy, async, dimensions"),
          ("PRIORITY", "Eager hero, lazy rest"),
          ("ARCHITECTURE", "SPA vs SSR vs SSG advice")],
          note="Scope: templates with images, public/, src/assets/, package.json. Read-only advice for SSR."),
    "This phase changes bytes and architecture, not state. Keep it separate from reactivity work to avoid confusion.",
    "Scan templates and public/ / src/assets/ for image usage and check whether this project requires SSR/SSG.",
)

c.add(
    "image-optimization", "Image Optimization Checklist", "PHASE 4 · MEDIA",
    "Resizing, compressing and lazy-loading images usually removes more bytes than every JavaScript tweak combined.",
    bullets([("Right dimensions", "Serve 2x the displayed size, not the camera original."),
             ("Modern format", "AVIF or WebP with a JPEG fallback."),
             ("Below the fold", "loading=\"lazy\" and decoding=\"async\"."),
             ("Explicit size", "width and height prevent layout shift."),
             ("Responsive", "srcset for different viewport widths."),
             ("CDN", "Automatic format negotiation and caching.")],
            note="The LCP hero image is the exception: eager, high priority, never lazy."),
    "Images are often 60-80% of transferred bytes. A single unoptimized hero can outweigh the entire app bundle.",
    "Audit oversized images in public/ and src/assets/, then resize and convert them to WebP/AVIF with fallbacks.",
)

c.add(
    "webp-avif", "WebP & AVIF Formats", "PHASE 4 · MEDIA",
    "Modern codecs deliver the same visual quality at much smaller sizes than JPEG/PNG.",
    compare(["hero.jpg — 420 KB", "PNG screenshots — 1.2 MB",
             "No format negotiation", "Every browser downloads the largest file"],
            ["<picture> with AVIF → WebP → JPEG",
             "Vite imagetools converts at build time",
             "Typical 30-60% smaller payload",
             "Same visual quality at the right size"],
            verdict="Keep one fallback source for older browsers; let the CDN negotiate headers when available."),
    "Format conversion is a pure payload win with no behavioural risk, so it belongs early in the media phase.",
    "Update this image reference to prefer .avif/.webp with a JPEG fallback, or add vite-imagetools to the build.",
)

c.add(
    "lazy-images", "Lazy-Load Below-the-Fold Images", "PHASE 4 · MEDIA",
    "Browsers can defer off-screen images natively — no JavaScript observer needed for most cases.",
    code(["<img src=\"/big-chart.png\"",
          "     alt=\"Revenue chart\" />",
          "// downloaded at page load",
          "// competes with the app bundle"],
         ["<img src=\"/big-chart.webp\"",
          "     alt=\"Revenue chart\"",
          "     loading=\"lazy\"",
          "     decoding=\"async\"",
          "     width=\"640\" height=\"360\" />"],
         note="Never lazy-load the LCP/hero image: it delays the very metric you are trying to improve."),
    "Native lazy loading removes off-screen network pressure from the critical path with one attribute.",
    "Add loading=\"lazy\", decoding=\"async\" and explicit width/height to every below-the-fold <img> tag.",
)

c.add(
    "cls-dimensions", "Explicit Dimensions Prevent CLS", "PHASE 4 · MEDIA",
    "Without width and height, the browser cannot reserve space. Late images push content down and cause layout shift.",
    code(["<!-- no reserved space -->",
          "<img src=\"/banner.webp\" />",
          "<h1>Report</h1>",
          "// image arrives → heading jumps"],
         ["<!-- space reserved before load -->",
          "<img src=\"/banner.webp\"",
          "     width=\"1200\" height=\"400\"",
          "     style=\"aspect-ratio: 3 / 1;",
          "            width: 100%; height: auto\">",
          "<h1>Report</h1>"],
         note="aspect-ratio plus explicit attributes reserves space even with responsive CSS."),
    "Cumulative Layout Shift is a Core Web Vital and a trust problem: users click the wrong thing when content moves.",
    "Add width and height (or aspect-ratio) to every image that lacks them and measure CLS again.",
)

c.add(
    "fetchpriority", "fetchpriority for the Hero Image", "PHASE 4 · MEDIA",
    "Not all images are equal. Tell the browser which one is the LCP element so it stops competing with below-the-fold assets.",
    code(["<img class=\"hero\" src=\"/hero.avif\"",
          "     loading=\"lazy\" />",
          "// hero is delayed and competes",
          "// with six gallery images"],
         ["<img class=\"hero\" src=\"/hero.avif\"",
          "     fetchpriority=\"high\"",
          "     loading=\"eager\"",
          "     decoding=\"async\"",
          "     width=\"1200\" height=\"600\" />"],
         note="Combine with <link rel=\"preload\" as=\"image\"> only when the hero is discovered late by CSS."),
    "Priority hints make the browser's download queue match your product's visual hierarchy.",
    "Mark the hero/LCP image eager with fetchpriority=\"high\" and keep all gallery images lazy.",
)

c.add(
    "ssr", "SSR: HTML on the First Response", "PHASE 4 · ARCHITECTURE",
    "Server-side rendering sends meaningful HTML immediately, so users and crawlers see content before JavaScript runs.",
    flow([("REQUEST", "Browser asks for /report"),
          ("SERVER", "Render Vue tree to HTML"),
          ("RESPONSE", "Meaningful HTML arrives"),
          ("HYDRATE", "Vue attaches interactivity"),
          ("INTERACTIVE", "Full client app takes over")],
          note="SSR improves FCP and SEO but adds server complexity and hydration cost."),
    "SSR is a trade: faster first paint and crawlability in exchange for infrastructure and hydration work.",
    "Assess this route's SEO/FCP needs and list the server requirements before considering an SSR migration.",
)

c.add(
    "ssg", "SSG: Render Once at Build Time", "PHASE 4 · ARCHITECTURE",
    "For content that rarely changes, pre-render at build time and serve static HTML from a CDN.",
    flow([("CONTENT", "Data known at build time"),
          ("BUILD", "Generate HTML per route"),
          ("CDN", "Static files at the edge"),
          ("REQUEST", "Instant HTML response"),
          ("HYDRATE", "Client takes over")],
          note="Best for docs, marketing and blogs; unusable for per-user dashboards behind auth."),
    "SSG gives SSR-like first paint with none of the per-request rendering cost, as long as content is build-time data.",
    "Identify statically known routes here and recommend prerendering them instead of full SSR.",
)

c.add(
    "spa-ssr-decision", "SPA, SSR or SSG? A Decision Tree", "PHASE 4 · ARCHITECTURE",
    "The answer depends on SEO needs, data freshness and team capacity — not on what is fashionable.",
    decision("Does this route need indexable HTML and a fast first paint for anonymous users?",
             [("YES · SEO matters", "SSR or SSG", "Pick SSG when content is static; SSR when it is per-request."),
              ("NO · behind login", "Keep Vite SPA", "Use route splitting, skeleton screens and caching instead.")],
             note="Do not migrate frameworks automatically. Write a short recommendation and let the team decide."),
    "Framework migrations are expensive. Most authenticated products get more from a well-split SPA than from SSR.",
    "Write a 3-4 bullet SPA vs SSR/SSG recommendation for this repo based on its routing and data fetching.",
)

c.add(
    "vite-ssg", "Prerendering Without a Framework Migration", "PHASE 4 · ARCHITECTURE",
    "vite-ssg or vite-plugin-ssr can generate static HTML for selected routes while keeping the Vite SPA you already have.",
    code(["// vite.config.ts",
          "import ssg from 'vite-plugin-ssr'",
          "",
          "plugins: [vue(), ssg()]",
          "// selected routes prerendered",
          "// at build time"],
         ["// package.json",
          '"build:ssg": "vite build && vite-ssg"',
          "// or a route-level prerender",
          "// config for docs + marketing",
          "// only, not private routes"],
         note="Prerender only public, stable routes; authenticated dashboards still render on the client."),
    "Incremental prerendering is the middle path: improve public-page SEO without rewriting the app around Nuxt.",
    "Evaluate vite-ssg for this project's public routes and keep authenticated routes client-rendered.",
)

c.add(
    "prefetching", "Prefetch on Intent", "PHASE 4 · NETWORK",
    "Fetch the next route while the user is still hovering or reading. Latency disappears before the click happens.",
    flow([("HINT", "User hovers a link"),
          ("PREFETCH", "import() next route chunk"),
          ("CACHE", "Browser stores the module"),
          ("CLICK", "Route resolves instantly"),
          ("FALLBACK", "Normal lazy load if not cached")],
          note="Use requestIdleCallback for speculative prefetch; never prefetch every route on initial load."),
    "Prefetching moves work into idle time. It is the last mile that makes lazy routes feel local.",
    "Prefetch this next-likely route on hover/focus using requestIdleCallback or the router's prefetch hook.",
)

"""Pillar 3, Phase 1: XSS, injection and client-storage hardening."""

from catalogue import catalogue, code, compare, flow, layers

c = catalogue(
    "04-security/phase-1-xss-storage", "PILLAR 3 · SECURITY",
    "Phase 1 removes client-side injection vectors and stops secrets or tokens from leaking through storage, logs "
    "and bundled environment variables.",
)

c.add(
    "security-phase-1-overview", "Security Phase 1 Overview: XSS & Storage", "SECURITY · PHASE 1",
    "Sanitize at render boundaries, validate at input boundaries, and keep sensitive values out of the browser entirely.",
    flow([("INPUT", "Validate forms with Zod"),
          ("RENDER", "Sanitize v-html and URLs"),
          ("ENV", "Only public VITE_* values"),
          ("STORAGE", "No tokens or PII at rest"),
          ("LOGS", "Redact sensitive payloads")],
          note="Scope: v-html and dynamic :href templates, forms, .env* files, storage usage and logging utilities."),
    "Most frontend security incidents start with untrusted text becoming executable code, or a secret becoming public.",
    "Audit every v-html and dynamic :href, validate forms, scrub VITE_* secrets and remove tokens from storage and logs.",
)

c.add(
    "xss-prevention", "XSS Prevention Basics", "SECURITY · PHASE 1",
    "Vue escapes text by default. XSS appears when you opt out with v-html, dynamic attributes or raw DOM APIs.",
    compare(["v-html=\"untrustedHtml\"",
             ":href=\"userInput\" with javascript: URL",
             "innerHTML on a ref",
             "Untrusted JSON rendered as markup"],
            ["Text interpolation {{ value }}",
             "Sanitize HTML with DOMPurify",
             "Allowlist protocols for URLs",
             "Treat every network string as hostile"],
            verdict="Escaping is the default; every raw render needs a documented reason and a sanitizer."),
    "The attacker's input is data, never code. Keep it that way unless you have explicitly made it safe.",
    "Find every v-html, innerHTML and dynamic :href in this component and classify it as sanitized or remove it.",
)

c.add(
    "v-html-sanitization", "Sanitize v-html With DOMPurify", "SECURITY · PHASE 1",
    "If you must render HTML, pass it through a battle-tested sanitizer before Vue inserts it.",
    code(["<!-- dangerous -->",
          "<div v-html=\"comment.body\"></div>",
          "// body: <img src=x onerror=alert(1)>",
          "// executes in the user's browser"],
         ["import DOMPurify from 'dompurify'",
          "const clean = computed(() =>",
          "  DOMPurify.sanitize(comment.body, {",
          "    ALLOWED_TAGS: ['p','b','i','a'],",
          "    ALLOWED_ATTR: ['href']",
          "  }))",
          "<div v-html=\"clean\"></div>"],
         note="Allowlist tags and attributes; a plain boolean true leaves dangerous vectors open."),
    "DOMPurify removes scripts, event handlers and javascript: URLs while preserving the formatting you intended.",
    "Wrap this v-html binding in DOMPurify.sanitize with an explicit allowlist and add a regression test with an XSS payload.",
)

c.add(
    "javascript-uri-block", "Block javascript: URIs in Dynamic Links", "SECURITY · PHASE 1",
    "A dynamic :href can execute script when the value starts with javascript:. Allowlist safe protocols instead.",
    code(["<a :href=\"link\">Open</a>",
          "// link = 'javascript:alert(1)'",
          "// click executes attacker code",
          "// also check :src and srcdoc"],
         ["function safeUrl(input: string) {",
          "  const url = new URL(input, location.origin)",
          "  return ['http:', 'https:', 'mailto:'].includes(",
          "    url.protocol) ? url.href : '/'",
          "}",
          "<a :href=\"safeUrl(link)\">Open</a>"],
         note="Relative URLs are fine after normalization with a trusted base; reject everything else."),
    "Protocol validation is a small helper that closes a surprising number of injection paths.",
    "Add a safeUrl() helper to this component's dynamic :href bindings and test it with a javascript: payload.",
)

c.add(
    "zod-validation", "Schema Validation on User Forms", "SECURITY · PHASE 1",
    "Validate shape, length and type at the boundary with Zod or VeeValidate; never trust client values or API DTOs.",
    code(["function submit() {",
          "  api.createUser(form.value)",
          "} // form may contain anything",
          "// no shape, no limits"],
         ["const UserInput = z.object({",
          "  email: z.string().email(),",
          "  name: z.string().min(1).max(80)",
          "})",
          "function submit() {",
          "  api.createUser(UserInput.parse(form.value))",
          "}"],
         note="Client validation is UX; repeat it on the server because clients can be bypassed."),
    "A schema gives you a typed, validated value instead of an object full of assumptions.",
    "Add a Zod schema to this form and submit only the parsed result, with inline errors for invalid fields.",
)

c.add(
    "env-hygiene", "Environment Variable Hygiene", "SECURITY · PHASE 1",
    "Everything named VITE_* is embedded in the client bundle. Secrets must never live there.",
    code(["# .env — WRONG",
          "VITE_STRIPE_SECRET=sk_live_...",
          "VITE_DB_PASSWORD=...",
          "// bundled into app.js",
          "// readable in DevTools"],
         ["# .env — SAFE",
          "VITE_API_URL=https://api.example.com",
          "# server-only, never prefixed:",
          "STRIPE_SECRET=sk_live_...",
          "// proxy through your backend"],
         note="Audit the built JS for secret strings; assume any VITE_* value is public."),
    "There is no such thing as a private client-side environment variable. Move secrets behind a server endpoint.",
    "Inspect .env* and import.meta.env.VITE_* usages here and remove any private key, token or database credential.",
)

c.add(
    "secrets-redaction", "Redact Secrets in Logs & Errors", "SECURITY · PHASE 1",
    "console.log and error trackers often capture the whole request object — including tokens and PII.",
    compare(["console.log('payload', payload)",
             "Sentry.captureException(err, { extra: form })",
             "Full request body in devtools",
             "Session token in breadcrumbs"],
            ["Redact fields: token, password, card, email",
             "Log ids and status codes instead",
             "beforeSend hook scrubs Sentry events",
             "Production logs use structured safe fields"],
            verdict="Log enough to debug, never enough to impersonate a user."),
    "Logs are copied into tickets, dashboards and third-party tools; treat them as public storage.",
    "Add a redaction helper to this logger/error reporter and remove token or PII dumps from console.log calls.",
)

c.add(
    "storage-hygiene", "Storage Hygiene", "SECURITY · PHASE 1",
    "localStorage is readable by any script on the origin. Keep raw JWTs, passwords and PII out of it.",
    compare(["localStorage.setItem('token', jwt)",
             "User email + phone in localStorage",
             "Long-lived session survives logout",
             "XSS can steal the whole session"],
            ["HttpOnly cookie for the session",
             "Keep only non-sensitive UI prefs",
             "Clear storage on logout",
             "Use sessionStorage for short-lived drafts"],
            verdict="If a script can read it, an XSS payload can steal it."),
    "Storage hygiene limits the blast radius of XSS and reduces privacy exposure on shared devices.",
    "Remove raw tokens and PII from localStorage/sessionStorage in this feature and clear remaining keys on logout.",
)

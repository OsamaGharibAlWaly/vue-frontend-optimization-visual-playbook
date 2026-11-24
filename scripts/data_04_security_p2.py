"""Pillar 3, Phase 2: auth, headers, transport and supply chain."""

from catalogue import code, compare, cycle, decision, flow, layers, catalogue

c = catalogue(
    "04-security/phase-2-auth-headers", "PILLAR 3 · SECURITY",
    "Phase 2 locks down authentication flows, browser security headers, route access control and third-party dependencies.",
)

c.add(
    "security-phase-2-overview", "Security Phase 2 Overview: Auth & Headers", "SECURITY · PHASE 2",
    "Cookies, CSRF, RBAC, CSP and transport headers work together: no single one is sufficient.",
    layers([("AUTH", "HttpOnly cookie + refresh rotation", "JavaScript cannot read the session token."),
            ("TRANSPORT", "HTTPS/HSTS + CSRF headers", "Requests are encrypted and state changes are authorized."),
            ("BROWSER", "CSP + frame-ancestors + SRI", "Limit what scripts can run and who can embed the app."),
            ("ACCESS", "Router guards + server checks", "Block navigation and validate every request."),
            ("SUPPLY", "npm audit + pinned versions", "Know what is in your dependency tree.")],
           note="Scope: auth stores/services, interceptors, router, index.html, hosting configs and package.json."),
    "Security is defense in depth. Each layer assumes another one fails, so a single mistake is not a full compromise.",
    "Harden cookie auth, CSRF, RBAC guards, CSP/frame-ancestors/HSTS, SRI, abuse controls and run npm audit.",
)

c.add(
    "httponly-cookies", "HttpOnly Cookies for Sessions", "SECURITY · PHASE 2",
    "The browser sends the cookie automatically and JavaScript cannot read it — XSS no longer steals the session directly.",
    compare(["localStorage JWT + Authorization header",
             "Any script can read the token",
             "XSS = full account takeover",
             "Logout only clears one tab"],
            ["Set-Cookie: HttpOnly; Secure; SameSite=Lax",
             "fetch with credentials: 'include'",
             "XSS cannot read the cookie value",
             "Server controls expiry and revocation"],
            verdict="Pair with CSRF protection: ambient credentials make state-changing requests forgeable."),
    "HttpOnly removes the most valuable target from client-side script. It is the foundation of modern browser auth.",
    "Configure the HTTP client with withCredentials: true and move token storage to an HttpOnly; Secure cookie.",
)

c.add(
    "secure-samesite", "Secure & SameSite Cookie Flags", "SECURITY · PHASE 2",
    "Secure blocks plain HTTP transmission; SameSite limits when the browser sends the cookie on cross-site requests.",
    code(["Set-Cookie: session=abc; Path=/",
          "// readable over HTTP",
          "// sent on cross-site requests",
          "// CSRF risk"],
         ["Set-Cookie: session=abc;",
          "  HttpOnly; Secure;",
          "  SameSite=Lax; Path=/;",
          "  Max-Age=3600",
          "// or SameSite=Strict for admin"],
         note="Lax is the usual default; Strict is stronger but can break legitimate cross-site return flows."),
    "Cookie attributes are server configuration, not client code. Verify them in the browser's Application tab.",
    "Set HttpOnly, Secure and SameSite on the session cookie and verify the attributes in DevTools.",
)

c.add(
    "jwt-refresh-rotation", "Safe 401 Refresh Rotation", "SECURITY · PHASE 2",
    "When an access token expires, rotate the refresh token once, replay the original request, and stop on a second failure.",
    cycle([("REQUEST", "API returns 401"),
           ("REFRESH", "Single-flight refresh call"),
           ("ROTATE", "New refresh token stored"),
           ("REPLAY", "Retry original request once"),
           ("LOGOUT", "On second 401, end session")],
          center="401 FLOW",
          note="A retry counter or one shared promise prevents infinite 401 loops across parallel requests."),
    "Naive refresh logic is a common source of retry storms and account lockouts. One refresh per failure is the rule.",
    "Implement single-flight 401 refresh with a retry limit and logout on the second failure in this HTTP client.",
)

c.add(
    "csrf-protection", "CSRF Protection for State Changes", "SECURITY · PHASE 2",
    "Ambient cookies ride along on cross-site requests. Require an extra token that an attacker's site cannot read.",
    code(["POST /api/orders",
          "Cookie: session=abc",
          "// a malicious form can send this",
          "// from another origin"],
         ["http.post('/orders', data, {",
          "  headers: { 'X-CSRF-Token': getCsrf() }",
          "})",
          "SameSite=Lax + server token check",
          "// attacker cannot read or forge",
          "// the token"],
         note="SameSite helps but is not a substitute for a server-validated CSRF token."),
    "CSRF tokens make the browser's automatic cookie behaviour safe for mutations.",
    "Attach the CSRF header on every state-mutating request and confirm the server validates it.",
)

c.add(
    "rbac-guards", "RBAC Guards Before Mounting", "SECURITY · PHASE 2",
    "Client-side guards improve UX; the server must still authorize every request. Never rely on hiding a button.",
    code(["<!-- UI hiding only -->",
          "<button v-if=\"user.role === 'admin'\">",
          "  Delete",
          "</button>",
          "// direct URL still renders the page"],
         ["router.beforeEach(async (to) => {",
          "  if (!to.meta.roles) return true",
          "  const roles = await auth.roles()",
          "  return roles.some(r => to.meta.roles",
          "    .includes(r)) || { name: 'denied' }",
          "})"],
         note="Check on navigation and re-check on the server; roles cached in the client can be stale."),
    "Route guards stop deep links to protected screens before they render and before their data requests fire.",
    "Verify this router's beforeEach blocks unauthenticated and unauthorized navigation before the protected view mounts.",
)

c.add(
    "csp", "Content Security Policy", "SECURITY · PHASE 2",
    "CSP tells the browser which script, style, image and connect sources are allowed. Inline scripts become a thing of the past.",
    code(["<!-- no policy: any script can run -->",
          "<script>tracker()</script>",
          "// injected inline code executes",
          "// data can leave to any host"],
         ["Content-Security-Policy:",
          "  default-src 'self';",
          "  script-src 'self';",
          "  style-src 'self' 'unsafe-inline';",
          "  img-src 'self' data: https://cdn;",
          "  connect-src 'self' https://api"],
         note="Deploy in Report-Only first; Vite's inline dev script needs a nonce or hash in production."),
    "CSP is the strongest browser-level defense against XSS and data exfiltration, but it needs careful rollout.",
    "Add a strict CSP header in the hosting config, starting in Report-Only mode, and remove unsafe-inline where possible.",
)

c.add(
    "clickjacking-headers", "Clickjacking Protection", "SECURITY · PHASE 2",
    "Frame-ancestors in CSP (and X-Frame-Options as a fallback) stops attackers embedding your app in a transparent iframe.",
    code(["<!-- attacker page -->",
          "<iframe src=\"https://your-app\">",
          "  opacity: 0;",
          "</iframe>",
          "// user clicks hidden buttons"],
         ["Content-Security-Policy:",
          "  frame-ancestors 'none';",
          "",
          "X-Frame-Options: DENY",
          "// modern browsers use CSP;",
          "// legacy clients use the header"],
         note="If you legitimately need embedding, allowlist exact origins instead of using 'none'."),
    "A one-line header removes an entire class of UI redressing attacks.",
    "Set frame-ancestors 'none' and X-Frame-Options: DENY in this app's hosting configuration.",
)

c.add(
    "sri", "Subresource Integrity for CDN Tags", "SECURITY · PHASE 2",
    "SRI makes the browser verify a hash before executing a third-party script. A compromised CDN cannot inject code.",
    code(["<script",
          "  src=\"https://cdn/analytics.js\">",
          "</script>",
          "// any changed file executes",
          "// no integrity check"],
         ["<script",
          "  src=\"https://cdn/analytics.js\"",
          "  integrity=\"sha384-...\"",
          "  crossorigin=\"anonymous\">",
          "</script>"],
         note="Regenerate the hash on every library upgrade; a stale hash blocks the script entirely."),
    "SRI protects the supply chain at the point of use, especially for scripts loaded from outside your build.",
    "Add integrity and crossorigin attributes to every external script/style tag in index.html.",
)

c.add(
    "https-hsts", "HTTPS & HSTS", "SECURITY · PHASE 2",
    "TLS protects data in transit; HSTS tells browsers to refuse plain HTTP for your domain in the future.",
    code(["http://app.example.com",
          "// credentials and tokens",
          "// travel in clear text",
          "// downgrade attacks possible"],
         ["Strict-Transport-Security:",
          "  max-age=31536000;",
          "  includeSubDomains; preload",
          "// HTTPS enforced by the browser",
          "// including future visits"],
         note="Enable HSTS only after HTTPS works everywhere, including subdomains."),
    "HSTS turns a one-time redirect into a lasting guarantee that browsers will not fall back to HTTP.",
    "Enforce HTTPS and add the HSTS header to this app's hosting config after verifying all subdomains.",
)

c.add(
    "rate-limiting-captcha", "Abuse Controls on Auth Forms", "SECURITY · PHASE 2",
    "Login, registration and password reset need throttling and bot checks to resist credential stuffing.",
    compare(["Unlimited login attempts",
                           "Instant repeated submissions",
                           "Automated signup scripts",
                           "No signal about abuse"],
                          ["Throttle submit + server rate limits",
                           "CAPTCHA after repeated failures",
                           "Exponential backoff on 429",
                           "Audit log for auth events"],
                          verdict="Client throttling is UX; server rate limiting is the actual defense."),
    "Auth endpoints are public by definition. Rate limits make brute force economically pointless.",
    "Add submit throttling and a CAPTCHA hook to these auth forms, plus server-side rate limits and 429 handling.",
)

c.add(
    "npm-audit", "Dependency Vulnerability Auditing", "SECURITY · PHASE 2",
    "Your supply chain is code you did not write. Audit it in CI and upgrade high-severity advisories deliberately.",
    flow([("INVENTORY", "npm audit --audit-level=high"),
          ("TRIAGE", "Check reachability and severity"),
          ("UPGRADE", "Patch with a lockfile change"),
          ("VERIFY", "Re-run tests and build"),
          ("MONITOR", "Dependabot / Renovate in CI")],
          note="Never blindly accept a major upgrade; check the changelog and run the full suite."),
    "A vulnerable transitive dependency is a vulnerability in your app. Continuous auditing makes that manageable.",
    "Run npm audit --audit-level=high, report the advisories, and fix high-severity issues with tests re-run.",
)

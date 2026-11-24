"""Pillar 2, Phase 1: architecture and state scaling."""

from catalogue import bullets, catalogue, code, flow, layers, tree

c = catalogue(
    "03-scaling/phase-1-architecture", "PILLAR 2 · SCALING",
    "Phase 1 of scaling breaks monolithic folders into isolated, domain-driven modules so several developers "
    "can work without merge conflicts or tight coupling.",
)

c.add(
    "scaling-phase-1-overview", "Scaling Phase 1 Overview: Architecture & State", "SCALE · PHASE 1",
    "Feature folders, composables, small stores and strict types turn one big app into independent, testable domains.",
    flow([("FOLDERS", "Group by feature, not file type"),
          ("COMPOSABLES", "Extract stateful logic"),
          ("STORES", "Split into domain slices"),
          ("TYPES", "Enforce strict TypeScript"),
          ("TEST", "Verify no circular imports")],
          note="Scope: src/* layout, tsconfig*.json, src/stores/* and .vue files over 300 lines."),
    "Scaling is organizational before it is technical. The folder structure decides who can change what safely.",
    "Refactor folder structure by feature/domain, extract use* composables, split Pinia stores and enable strict: true.",
)

c.add(
    "feature-sliced-design", "Feature-Sliced Design in Practice", "SCALE · PHASE 1",
    "FSD orders layers so code only imports downward: app → pages → features → entities → shared.",
    layers([("APP", "Router, providers, global styles", "Wires everything together; owns no domain logic."),
            ("PAGES", "Route-level composition", "Assembles features for one screen."),
            ("FEATURES", "User interactions", "One business capability per folder."),
            ("ENTITIES", "Domain data and rules", "Types and pure logic shared across features."),
            ("SHARED", "UI primitives and utilities", "No app imports, no business knowledge.")],
           note="Imports point downward. A shared button must never import a feature store."),
    "Layered dependencies make it obvious where a piece of code belongs and prevent circular imports by construction.",
    "Map the current folders to these layers and move one feature into src/features/<domain>/ with a public index.ts.",
)

c.add(
    "domain-feature-folders", "Domain Feature Folders", "SCALE · PHASE 1",
    "A feature folder owns its view, composable, API calls and types. Everything else imports its public index.",
    tree([(0, "src/features/checkout/", "Owned by the checkout team"),
          (1, "ui/CheckoutForm.vue", "Presentation only"),
          (1, "model/useCheckout.ts", "State + intent"),
          (1, "api/checkout.service.ts", "Typed HTTP boundary"),
          (1, "model/types.ts", "Domain DTOs"),
          (1, "index.ts", "Public surface"),
          (0, "src/features/checkout/__tests__/", "Tests live with the feature")],
          note="If a file is used by two features, it moves down to entities or shared."),
    "Colocation makes the blast radius of a change visible and removes cross-team merge conflicts.",
    "Move this feature's view, logic, API and types into one folder and expose only index.ts to the rest of the app.",
)

c.add(
    "extract-usef-composable", "Extract use<Feature> Composables", "SCALE · PHASE 1",
    "A composable is a named unit of stateful logic you can test without mounting the DOM.",
    code(["// Dashboard.vue (600 lines)",
          "const rows = ref([])",
          "const loading = ref(true)",
          "watch(filters, async () => {",
          "  rows.value = await api.rows(filters)",
          "})",
          "// logic trapped in a component"],
         ["// useDashboard.ts",
          "export function useDashboard() {",
          "  const rows = shallowRef([])",
          "  const loading = ref(true)",
          "  // watch, fetch, format, return",
          "  return { rows, loading, refresh }",
          "}"],
         note="Return a small, typed surface; do not expose internal refs that callers can mutate freely."),
    "Composables turn component logic into reusable, unit-testable modules while keeping the view declarative.",
    "Extract stateful logic from this large .vue file into use<Feature>.ts and keep markup and bindings in the view.",
)

c.add(
    "modular-pinia-stores", "Split Monolithic Pinia Stores", "SCALE · PHASE 1",
    "One store per domain with Setup Store syntax keeps state, getters and actions together and independently testable.",
    code(["// stores/app.ts (everything)",
          "export const useAppStore = defineStore('app', {",
          "  state: () => ({ user, cart, filters,",
          "    notifications, orders, uiFlags })",
          "})"],
         ["// stores/cart.ts",
          "export const useCart = defineStore('cart', () => {",
          "  const items = shallowRef([])",
          "  const total = computed(() => sum(items.value))",
          "  return { items, total, add, remove }",
          "})"],
         note="Cross-store calls stay explicit: import the other store inside the action that needs it."),
    "A single global store becomes a hidden dependency graph. Small stores make ownership and testing straightforward.",
    "Split this monolithic store into single-responsibility Setup Stores and update feature imports to the new modules.",
)

c.add(
    "strict-typescript-scale", "Strict TypeScript at Scale", "SCALE · PHASE 1",
    "At scale, implicit any is a tax on every consumer. Strict types on stores and composables pay for themselves.",
    code(["// before",
          "const store = defineStore('x', {",
          "  state: () => ({ items: [] }),",
          "  actions: { load() { /* any */ } }",
          "})"],
         ["// after",
          "type Item = { id: number; name: string }",
          "export const useX = defineStore('x', () => {",
          "  const items = ref<Item[]>([])",
          "  async function load(): Promise<void> { /* */ }",
          "  return { items, load }",
          "})"],
         note="Fix strict errors by domain; do not add `as any` to silence them."),
    "Types are the interface between teams. Strictness makes a feature's contract visible before runtime.",
    "Enable strict: true in tsconfig*.json and resolve implicit any in stores and composables first.",
)

c.add(
    "migration-checklist", "Migrate Folders Without Stopping the Product", "SCALE · PHASE 1",
    "A big-bang restructure breaks everything. Move one domain at a time behind a stable public index.",
    bullets([("Pick a leaf domain", "Start with a feature that has few consumers."),
             ("Add public index.ts", "Create the new import surface first."),
             ("Move files", "Keep components, logic, API and types together."),
             ("Update imports", "Point consumers at index.ts only."),
             ("Run vue-tsc + tests", "Catch stale paths before merging."),
             ("Commit", "One domain per commit keeps reverts cheap.")],
            note="Never combine a folder move with a behaviour change; reviewers cannot verify both at once."),
    "Migration risk is proportional to batch size. One domain per commit keeps the app shippable throughout.",
    "Plan this folder migration as one domain per commit with vue-tsc and tests between each step.",
)

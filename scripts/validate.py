"""Check that every concept payload matches the visual template it uses."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_00_story  # noqa: F401
import data_01_foundations_a  # noqa: F401
import data_01_foundations_b  # noqa: F401
import data_02_opt_phase1  # noqa: F401
import data_02_opt_phase2  # noqa: F401
import data_02_opt_phase3  # noqa: F401
import data_02_opt_phase4  # noqa: F401
import data_03_scaling_p1  # noqa: F401
import data_03_scaling_p2  # noqa: F401
import data_03_scaling_p3  # noqa: F401
import data_04_security_p1  # noqa: F401
import data_04_security_p2  # noqa: F401
import data_05_proof  # noqa: F401
from catalogue import ALL_CONCEPTS


def expect(condition, msg):
    if not condition:
        raise AssertionError(msg)


def check(concept):
    v = concept["visual"]
    kind = v["kind"]
    name = concept["slug"]
    expect(bool(concept["title"] and concept["subtitle"] and concept["takeaway"] and concept["prompt"]),
           f"{name}: empty text field")
    if kind in ("flow", "cycle"):
        expect(2 <= len(v["steps"]) <= 7, f"{name}: steps count")
        expect(all(len(s) == 2 for s in v["steps"]), f"{name}: step tuple")
    elif kind == "compare":
        expect(all(isinstance(s, str) for s in v["before"] + v["after"]), f"{name}: compare items")
        expect(len(v["before"]) <= 5 and len(v["after"]) <= 5, f"{name}: compare too many items")
    elif kind == "code":
        expect(len(v["before"]) <= 13 and len(v["after"]) <= 13, f"{name}: code too many lines")
    elif kind == "layers":
        expect(all(len(i) == 3 for i in v["items"]), f"{name}: layer tuple")
        expect(len(v["items"]) <= 6, f"{name}: too many layers")
    elif kind == "tree":
        expect(all(len(r) == 3 for r in v["rows"]), f"{name}: tree tuple")
    elif kind == "metrics":
        expect(all(len(c) == 2 for c in v["cards"]), f"{name}: metric card tuple")
        expect(all(len(b) in (2, 3) for b in v["bars"]), f"{name}: metric bar tuple")
    elif kind == "matrix":
        expect(len(v["axes"]) == 2 and len(v["quadrants"]) == 4, f"{name}: matrix shape")
        expect(all(len(q) == 2 for q in v["quadrants"]), f"{name}: quadrant tuple")
    elif kind == "timeline":
        expect(all(len(r) == 4 for r in v["rows"]), f"{name}: timeline tuple")
    elif kind == "decision":
        expect(2 <= len(v["branches"]) <= 4, f"{name}: branch count")
        expect(all(len(b) == 3 for b in v["branches"]), f"{name}: branch tuple")
    elif kind == "bullets":
        expect(3 <= len(v["items"]) <= 6, f"{name}: bullet count")
        expect(all(len(i) == 2 for i in v["items"]), f"{name}: bullet tuple")
    elif kind == "anatomy":
        expect(len(v["center"]) == 2, f"{name}: center tuple")
        expect(4 <= len(v["nodes"]) <= 6, f"{name}: node count")
        expect(all(len(n) == 2 for n in v["nodes"]), f"{name}: node tuple")
    elif kind == "hero":
        expect(all(len(p) == 2 for p in v["pillars"]), f"{name}: pillar tuple")
    else:
        raise AssertionError(f"{name}: unknown template {kind}")


def main():
    for concept in ALL_CONCEPTS:
        check(concept)
    kinds = {}
    for concept in ALL_CONCEPTS:
        kinds[concept["visual"]["kind"]] = kinds.get(concept["visual"]["kind"], 0) + 1
    print(f"Validated {len(ALL_CONCEPTS)} concepts: {kinds}")


if __name__ == "__main__":
    main()

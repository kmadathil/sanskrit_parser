# -*- coding: utf-8 -*-
"""strī-pratyaya rule classification audit — phase W0 of word_formation_ordering_plan.md.

Answers ONE question for every rule in the ṭāp/ṅīp machine: **does it depend on the compound,
or only on the stem in front of it?** That is the split the word-formation ordering plan rests
on — a rule that decides a MEMBER's own feminine affix (कुमारी as a word) can have its verdict
computed early, while one that decides the COMPOUND's affix (त्रिलोकी, बहुकुमारी) cannot,
because the compound does not exist yet.

    python -m sanskrit_parser.generator.stri_rule_audit
    python -m sanskrit_parser.generator.stri_rule_audit --verbose

Why a script and not a one-off grep: the first hand count said 46 independent / 23 dependent,
and it was WRONG. Seven "independent" rules identify the pūrva by POSITION (`llp: ?dik`,
`llp: =pUta` …) instead of by a compound tag, so a tag-name scan silently under-counts the
dependent set. Any future hand count will make the same mistake; this one will not.

Result on 2026-08-05 (`sutras_antaranga.yaml`, 773 rules): **41 advisable early / 28
compound-dependent** — 21 by tag, 7 by position, **0 by derived tag**, 2 mixed. That zero is
the load-bearing one: no rule in the advisable set reads anything the samāsa pre-pass produces,
so the set can be evaluated before the pre-pass runs at all.

Classification is **per ARM**. Judging whole rules gave 39/30 and was WRONG in a way that
produced a wrong verdict: see `arms()` below and W1's अज case.

Five buckets, and the middle three are the reason this exists:

  * DEPENDENT (tag)      — names a compound saṁjñā: ?samAsa, ?bahuvrIhi, ?dvigu, …
  * DEPENDENT (position) — names no compound tag but reads `llp`/`rrp`, i.e. it identifies a
                           neighbouring member positionally. Compound-dependent in fact.
  * DEPENDENT (derived)  — reads a tag that some `bahiranga: -1` rule WRITES. This is the check
                           no hand count can do: it does not depend on knowing which tag names
                           "look like" compound tags, only on what the pre-pass actually emits.
  * MIXED                — some arms independent, some not. ADVISABLE: a dependent arm cannot
                           match in the advisory sandbox anyway (no compound tag on a bare
                           member, no `llp` in the sandbox window).
  * INDEPENDENT          — none of the above.

It also reports what each rule DOES (substitute the placeholder / block a competitor / reshape
the stem), because that is the other half of the design: **nothing inserts a strī pratyaya** —
every rule resolves a composer-supplied `strI_abs`, which is why member-level and
compound-level femininity share one slot.

Finally it lists the rules that read `?NI`/`?Ap` on their LEFT operand. Those constrain the
naming of the advisory tags: they are the declension family (6.1.68, 7.3.105–116, 7.1.54 …)
and must see the tag only on the MERGED stem, never on the bare base — which is why phase W1
writes `?NI_adv`/`?Ap_adv` rather than reusing `?NI`/`?Ap`.
"""
import argparse
import os

import yaml

# The file the engine actually loads (test/conftest.py: SutraFactory("sutras_antaranga.yaml")).
# The other YAMLs in this directory are alternative rule sets and are not audited.
DEFAULT_YAML = "sutras_antaranga.yaml"

COMPOUND_TAGS = (
    "samAsaPurva", "samAsa", "bahuvrIhi", "dvigu", "avyayIBAva", "tatpuruza",
    "dvandva", "upasarjana", "ajAdi_in_Dvigu", "uttara_strI", "samAhAra",
)
POSITIONAL_KEYS = ("llp", "rrp")


def _pairs(node, key=None, out=None):
    """Flatten a condition/update tree into (enclosing-key, string) pairs."""
    if out is None:
        out = []
    if isinstance(node, dict):
        for k, v in node.items():
            _pairs(v, k, out)
    elif isinstance(node, list):
        for x in node:
            _pairs(x, key, out)
    elif isinstance(node, str):
        out.append((key, node))
    return out


def _effect(rule):
    """What the rule does to the strī_abs placeholder."""
    upd = rule.get("update")
    if upd:
        for _, v in _pairs(upd):
            if v.startswith("=") and ("NI" in v or "Ap" in v):
                return f"substitute {v}"
        return "tag only"
    if rule.get("xform") is not None:
        return "xform (stem)"
    if rule.get("overrides") is not None:
        return "block (overrides)"
    return "none"


def load_rules(path=None):
    """The rule list, from the YAML the engine itself loads unless told otherwise."""
    path = path or DEFAULT_YAML
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f), path


def _prepass_written_tags(rules):
    """Every tag a `bahiranga: -1` rule sets. A strī rule reading one of these is
    compound-dependent no matter what the tag is called."""
    written = set()
    for r in rules:
        if not isinstance(r, dict) or r.get("bahiranga") != -1:
            continue
        for _, v in _pairs(r.get("update") or {}):
            if v.startswith("+"):
                written.add(v[1:])
    return written


def arms(condition):
    """A rule's condition as a list of ALTERNATIVE arms.

    Classification is PER ARM, not per rule — SK454+/4.1.4.1 अजाद्यतष्टाप् is why. Its first
    arm (`lp: ?ajAdi`) is the plain-word ajādi-prabalatva that gives अजा; its second names
    `?samAsa` for the compound case. Judging the rule as a whole let arm 2 disqualify arm 1,
    the advisory sandbox then dropped the rule, 4.1.63 जातेः ṅīṣ won unopposed, and अज was
    advised `?NI_adv` while the real derivation gives अजा. Found by probing W1, 2026-08-05."""
    if isinstance(condition, list):
        return [a for a in condition if isinstance(a, dict)] or [condition]
    return [condition]


def _arm_bucket(arm, written_tags=()):
    pairs = _pairs(arm)
    blob = " ".join(v for _, v in pairs)
    if "strI_abs" not in blob:
        return None
    if any(t in blob for t in COMPOUND_TAGS):
        return "DEPENDENT (tag)"
    if any(k in POSITIONAL_KEYS for k, _ in pairs):
        return "DEPENDENT (position)"
    if written_tags and ({v.lstrip("?!") for _, v in pairs if v.startswith("?")}
                         & set(written_tags)):
        return "DEPENDENT (derived)"
    return "INDEPENDENT"


def bucket_for(condition, written_tags=()):
    """The bucket a rule falls in, or None if it is not a strī-window rule.

    A rule with BOTH independent and dependent arms is "MIXED", and counts as advisable: the
    dependent arms cannot match in the advisory sandbox anyway, since they require a compound
    tag the bare member does not carry, or an `llp` the sandbox window does not supply.
    (Caveat, true today and worth re-checking if it changes: no strī arm reads a NEGATED
    `llp`, which is the one shape that could match against an absent neighbour.)

    Shared with the ENGINE (antaranga_prakriya._split_sutras), which classifies live Sutra
    objects from their retained `_cond_dict` so the advisory pre-pass and this audit can never
    drift apart. The engine passes no `written_tags`: the DEPENDENT (derived) check needs the
    -1 rules' update dicts, which Sutra objects do not retain, and it is the audit's guard test
    that keeps that bucket empty.
    """
    if condition is None:
        return None
    buckets = [b for b in (_arm_bucket(a, written_tags) for a in arms(condition))
               if b is not None]
    if not buckets:
        return None
    if all(b == "INDEPENDENT" for b in buckets):
        return "INDEPENDENT"
    if any(b == "INDEPENDENT" for b in buckets):
        return "MIXED (some arms independent)"
    # All dependent — report the most specific reason, in the order checked.
    for b in ("DEPENDENT (tag)", "DEPENDENT (position)", "DEPENDENT (derived)"):
        if b in buckets:
            return b
    return buckets[0]


def is_advisable(condition):
    """True if ANY arm's verdict can be computed before the compound exists."""
    return bucket_for(condition) in ("INDEPENDENT", "MIXED (some arms independent)")


def classify(rules):
    written = _prepass_written_tags(rules)
    stri, decl = [], []
    for r in rules:
        if not isinstance(r, dict) or r.get("condition") is None:
            continue
        pairs = _pairs(r["condition"])
        blob = " ".join(v for _, v in pairs)

        # The declension family — reads ?NI/?Ap on the LEFT operand. Reported separately;
        # these are what force the advisory tags to have their own names.
        left = sorted({v for k, v in pairs
                       if k in ("lp", "llp") and v in ("?NI", "?Ap", "?!NI", "?!Ap")})
        if left:
            decl.append((r.get("id"), r.get("bahiranga"), left))

        bucket = bucket_for(r["condition"], written)
        if bucket is None:
            continue
        tags = sorted({t for t in COMPOUND_TAGS if t in blob})
        pos = sorted({k for k, _ in pairs if k in POSITIONAL_KEYS})
        derived = sorted({v.lstrip("?!") for _, v in pairs if v.startswith("?")} & written)
        why = tags or pos or derived or []
        stri.append({
            "id": r.get("id"), "sutra": r.get("sutra", ""),
            "bahiranga": r.get("bahiranga"), "bucket": bucket,
            "why": why, "effect": _effect(r),
        })
    return stri, decl


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("yaml_file", nargs="?", default=DEFAULT_YAML)
    ap.add_argument("--verbose", action="store_true",
                    help="list every rule, not just the dependent ones")
    args = ap.parse_args()

    rules, path = load_rules(args.yaml_file)
    stri, decl = classify(rules)
    order = ("DEPENDENT (tag)", "DEPENDENT (position)", "DEPENDENT (derived)",
             "MIXED (some arms independent)", "INDEPENDENT")

    print(f"strī-pratyaya rule audit — {os.path.basename(path)} "
          f"({len(rules)} rules, {len(stri)} of them strī-window)\n")
    for bucket in order:
        rows = [r for r in stri if r["bucket"] == bucket]
        by_bah = {}
        for r in rows:
            by_bah[r["bahiranga"]] = by_bah.get(r["bahiranga"], 0) + 1
        spread = ", ".join(f"{n}@{b if b is not None else 'main'}"
                           for b, n in sorted(by_bah.items(), key=lambda kv: str(kv[0])))
        print(f"── {bucket}: {len(rows)}   ({spread})")
        if args.verbose or bucket != "INDEPENDENT":  # MIXED is always listed
            for r in sorted(rows, key=lambda r: str(r["id"])):
                bah = r["bahiranga"] if r["bahiranga"] is not None else "main"
                why = ",".join(r["why"]) if r["why"] else "-"
                print(f"     {str(r['id']):10s} bah={str(bah):>4s}  {why:22s} {r['effect']}")
        print()

    dep = sum(1 for r in stri if r["bucket"].startswith("DEPENDENT"))
    ind = len(stri) - dep   # INDEPENDENT + MIXED — both are advisable
    print(f"SPLIT: {ind} advisable early / {dep} compound-dependent "
          f"(of {len(stri)} strī-window rules)\n")

    effects = {}
    for r in stri:
        key = r["effect"].split()[0]
        effects[key] = effects.get(key, 0) + 1
    print("What they do to the placeholder (nothing INSERTS one):")
    for k, n in sorted(effects.items(), key=lambda kv: -kv[1]):
        print(f"     {k:12s} {n}")

    print(f"\nRules reading ?NI/?Ap on the LEFT operand — the declension family that must see")
    print(f"the tag only on the MERGED stem ({len(decl)}); this is why W1 uses ?NI_adv/?Ap_adv:")
    for rid, bah, left in sorted(decl, key=lambda x: str(x[0])):
        print(f"     {str(rid):10s} bah={str(bah if bah is not None else 'main'):>4s}  {left}")


if __name__ == "__main__":
    main()

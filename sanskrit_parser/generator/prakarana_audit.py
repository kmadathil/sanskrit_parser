# -*- coding: utf-8 -*-
"""Prakaraṇa completeness audit.

Verifies that every sūtra in an SK range is ACCOUNTED FOR — either implemented (a rule in the
YAMLs plus a row in generator_status.md's Implemented table) or explicitly deferred (a row in
its Skipped table). The target for a finished prakaraṇa is ZERO unaccounted, as tatpuruṣa
(SK684–828) and समासाश्रयविधि (SK985–1071) both achieve.

Written for phase X9 of samasa_asraya_plan.md and kept because the check is worth repeating:
the first run found a sūtra (SK1068/6.1.154 मस्कर) that had been silently skipped when its
phase was written, and an Implemented row whose SK cell was a RANGE that over-claimed it.

    python -m sanskrit_parser.generator.prakarana_audit 985 1071

Three checks, and the middle one is the one that catches real omissions:

  * rule present  — the sūtra's Ashtadhyayi id appears in one of the three YAMLs. A suffixed
    variant counts (6.1.153.1 satisfies 6.1.153), since splitting one sūtra across two rule
    blocks is a normal engine accommodation.
  * ACCOUNTED     — the SK number appears in an Implemented row or a Skipped row. A sūtra that
    is in neither has been forgotten, whatever the YAML says.
  * no rule AND no Skipped row — an adhikāra or a natural realization needs an explicit
    "Natural" Skipped row (the convention 2.1.11 विभाषा and 5.4.68 समासान्ताः follow), not
    silence.

Appearing in BOTH tables is normal and reported for information only: it means the sūtra is
implemented but an arm or vārtika of it is deferred (6.3.61's general form, 6.1.157's vārtika
tail, 8.4.11's वा …).

Note on status-doc formatting, learned the hard way: the SK cell may be **bolded** or
~~struck through~~, and may hold several numbers separated by `/` or a `1058–1071` range. A
range is convenient but DANGEROUS — it silently claims every number inside it. Prefer an
explicit list when the row does not cover the whole span.
"""
import os
import re
import sys

import yaml

_HERE = os.path.dirname(__file__)
_YAMLS = ("sutras_antaranga.yaml", "sutras.yaml", "sutras_hier.yaml")
# The SK cell: optional ** / ~~ decoration around numbers, slashes, commas and en/em dashes.
_SK_CELL = re.compile(r"\|\s*[*~]*([0-9/–\-,\s]+?)[*~]*\s*\|")
_SKMAP_ROW = re.compile(r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*(.*?)\s*\|")


def _path(name):
    return os.path.join(_HERE, name)


def sk_map(lo, hi):
    """{SK number: (Ashtadhyayi id, sūtra text)} for the range, from sk_map.md."""
    out = {}
    with open(_path("sk_map.md"), encoding="utf-8") as f:
        for line in f:
            m = _SKMAP_ROW.match(line)
            if m and lo <= int(m.group(1)) <= hi:
                out[int(m.group(1))] = (m.group(2), m.group(3))
    return out


def yaml_ids():
    ids = set()
    for name in _YAMLS:
        for rule in yaml.safe_load(open(_path(name), encoding="utf-8")):
            ids.add(str(rule["id"]))
    return ids


def _sk_numbers(chunk):
    """Every SK number a markdown table's first cell claims, expanding `a–b` ranges."""
    found = set()
    for line in chunk.split("\n"):
        m = _SK_CELL.match(line)
        if not m:
            continue
        for part in re.split(r"[/,]", m.group(1)):
            part = part.strip()
            if re.fullmatch(r"\d+", part):
                found.add(int(part))
                continue
            rng = re.fullmatch(r"(\d+)\s*[–\-]\s*(\d+)", part)
            if rng:
                found.update(range(int(rng.group(1)), int(rng.group(2)) + 1))
    return found


def status_tables():
    """(implemented SK numbers, skipped SK numbers) from generator_status.md."""
    text = open(_path("generator_status.md"), encoding="utf-8").read()
    split = text.index("## Skipped / Deferred Sutras")
    return _sk_numbers(text[:split]), _sk_numbers(text[split:])


def audit(lo, hi, out=sys.stdout):
    """Report on SK lo..hi. Returns the number of UNACCOUNTED sūtras (0 == complete)."""
    skm = sk_map(lo, hi)
    expected = hi - lo + 1
    ids = yaml_ids()

    def has_rule(aps):
        return any(i == aps or i.startswith(aps + ".") for i in ids)

    impl, skip = status_tables()
    unaccounted, undocumented, both = [], [], []
    for n in sorted(skm):
        aps, name = skm[n]
        in_impl, in_skip = n in impl, n in skip
        if not in_impl and not in_skip:
            unaccounted.append((n, aps, name))
        if not has_rule(aps) and not in_skip:
            undocumented.append((n, aps, name))
        if in_impl and in_skip:
            both.append((n, aps))

    p = lambda *a: print(*a, file=out)          # noqa: E731
    p(f"SK {lo}–{hi}: {len(skm)} of {expected} sūtras found in sk_map.md"
      f"  {'OK' if len(skm) == expected else '← GAP IN sk_map.md'}")
    p(f"  rule present in a YAML       : {sum(1 for n in skm if has_rule(skm[n][0]))}/{len(skm)}")
    p(f"  in an Implemented row        : {len(impl & set(skm))}/{len(skm)}")
    p(f"  in a Skipped row             : {len(skip & set(skm))}")
    p("")
    p(f"UNACCOUNTED (in neither table) : {len(unaccounted)}"
      f"{'   ← prakaraṇa COMPLETE' if not unaccounted else ''}")
    for n, aps, name in unaccounted:
        p(f"    SK{n:<6d} {aps:<10s} {name[:56]}")
    p(f"NO RULE and NO Skipped row     : {len(undocumented)}")
    for n, aps, name in undocumented:
        p(f"    SK{n:<6d} {aps:<10s} {name[:56]}")
    p(f"in BOTH tables (partials, ok)  : {len(both)}")
    for n, aps in both:
        p(f"    SK{n:<6d} {aps}")
    return len(unaccounted)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <first SK> <last SK>")
    sys.exit(1 if audit(int(sys.argv[1]), int(sys.argv[2])) else 0)

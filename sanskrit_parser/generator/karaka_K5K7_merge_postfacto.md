# Kāraka Phases K5–K7 — Post-facto Plan & Merge Record

**Date:** 2026-06-14
**Branch:** `claude/cranky-bhabha-1df4d6` (base K4 tip `756725b`)
**Scope:** the final three kāraka rule phases (SK 586–646), implemented in parallel
worktrees and merged here. This document records *what was actually done* (vs. the
forward-looking `karaka_plan.md`), including the merge mechanics and the open issues.

---

## 1. How the phases were produced

Three background agents ran in parallel, each in a pre-created worktree branched off
the K4 tip `756725b` (`claude/karaka-k5`, `-k6`, `-k7`). Each was seeded with a
design brief distilled from a prior (limit-interrupted) run's transcript, so it
implemented directly rather than re-deriving. All three completed their
implementations but hit the account usage limit **before** running the full suite or
committing. Their uncommitted work was committed as-is on each branch, then merged
(below).

> Lesson captured separately: `Agent isolation:"worktree"` bases off `master` (which
> lacks all generator work), so the worktrees had to be pre-created at the K4 tip.

---

## 2. What each phase implemented

### Phase K5 — Apādāna + pañcamī (SK 586–605), branch `claude/karaka-k5` → commit `39b509f`
- **Saṁjñā → `kAraka_apAdAna`:** 1.4.24 (general `semantic_DruvApAya`), 1.4.25–31
  verb-gated via `rp` (`?BItrA`, `?parAji`, `?vAraRArTa`, `?antarDi`, `?upayoga`,
  `?jani`, `?praBava`).
- **Vibhakti pañcamī:** 2.3.28 (`kAraka_apAdAna`→viBakti_5); 2.3.29 yoga-word peek
  (`=anya/=ArAt/=itara/=fte/=pUrva`); 2.3.24 akartari ṛṇe; karmapravacanīya pañcamī
  1.4.88/89/92 → 2.3.10/2.3.11 using **new** direction tags
  `kp_pancami_pUrva`/`kp_pancami_para` (kept distinct from K2's dvitīyā
  `kp_pUrva`/`kp_para` so 2.3.8 never fires on them).
- **Forks:** two 2-way vibhāṣā (2.3.25 guṇe, 2.3.33 stoka) and **two 3-way** forks
  (2.3.32 pṛthak/vinā/nānā, 2.3.35 dūra/antika) modelled as three rules with
  sub-sutra aps ordered HIGH→LOW so the two `optional` arms fork first and the
  non-optional arm is the final fall-through (exactly 3 branches via `?!has_viBakti`).
- **Lexicon:** `dhatu.py` Ayati/biBeti/parAjayate/vArayati/nilIyate/aDIte/prajAyate/
  praBavati; `pratipadika.py` cora/upADyAya/Satru/aDyayana/jAqya/stoka/**dUra/antika**/
  himavat/gaNgA; `avyaya.py` apa_kp/AN_kp; `paninian_object.py` +kp_pancami_*.
- **Tests:** 23 new cases (→ 101). **Deferred:** SK587/594 vā vārttikas, SK595
  ñc/āc/āhi yoga-words, SK602 yoga-vibhāga branch.
- *Counts on branch were left at the K4 baseline (394/68) — not updated.*

### Phase K6 — Ṣaṣṭhī (SK 607–631), branch `claude/karaka-k6` → commit `d253872`
- **Yoga-word peeks:** 2.3.26 hetu, 2.3.27 (fork), 2.3.30 atasartha, 2.3.31 enap
  (fork), 2.3.34 dūra/antika (fork), 2.3.64 kṛtvas+kāla, 2.3.72/73 tulya/āśis (forks).
- **Verb-conditioned śeṣa-ṣaṣṭhī:** 2.3.51–58 (jñā/adhi-i/kṛ-pratiyatna/ruj/nāth/
  hiṁsā/vyavahṛ-paṇ/div), 2.3.59 vibhāṣopasarge (fork), 2.3.61 preṣ/brū havis.
- **Kṛd-yoga:** 2.3.65 (`?kft` governor, guard `?!kft_aSazWI`), 2.3.67
  (`?kta_vartamAna`), 2.3.68 (`?kta_aDikaraRa`), 2.3.71 kṛtya (fork). The 2.3.69/70
  **prohibitions are realized as the negative `kft_aSazWI` guard** (governors tagged
  it), tested via negatives (दैत्यान् घातुको हरिः → dvitīyā). Distinct tag names were
  used because `kta`/`tfn` are already real pratyaya tags.
- **Lexicon:** new verb padas + governors (kfti/pAcaka/kartf/mata/GAtuka/gAmin/dAyin
  …), stems anna/cOra/havis/CAga/tulya/Ayuzya. No `paninian_object.py` change needed.
- **Tests:** +23 (→ 124 at merge). **Deferred:** SK624 (2.3.66 ubhayaprāpti — needs a
  real dual-kāraka kṛt-valency frame). **Counts updated on branch: 394→414, 68→71.**

### Phase K7 — Adhikaraṇa + saptamī (SK 632–646), branch `claude/karaka-k7` → commit `fef43b6`
- **Saṁjñā:** 1.4.45 ādhāra → `kAraka_aDikaraRa` (`semantic_ADAra`).
- **Saptamī:** 2.3.36 (+ dūra/antika च arm via `semantic_dUrAntika`), 2.3.37
  sati-saptamī (adjacent `semantic_BAvalakzaRa` pair), 2.3.42 pañcamī vibhakte,
  2.3.43 sādhu/nipuṇa arcā.
- **ṣaṣṭhī/saptamī forks** (2.3.38/39/40/41): noun is `semantic_Seza` ⇒ 2.3.50 gives
  ṣaṣṭhī; the marked rule is `optional: true` + `overrides:[2.3.50]` (apply⇒saptamī,
  skip⇒ṣaṣṭhī). **adhikaraṇa-default forks** (2.3.44/45/2.3.7): `overrides:[2.3.36]`.
- **KP tail:** 1.4.97 adhi-īśvare + a second 1.4.87 arm (`1.4.87.1`, upa-adhika), both
  setting `kp_saptamI`; 2.3.9 reads `?kp_saptamI` (overrides 2.3.8); 1.4.98 vibhāṣā
  kṛñi (fork). `paninian_object.py` +`kp_saptamI`.
- **Tests:** 20 new cases. **Deferred:** SK642 taddhita-lup, SK633/640 vārttikas,
  2.3.9 broader aiśvarya, SK646 surface. **Counts on branch left at 394/68 — not
  updated** (the agent planned 409/71 but stopped before writing it).

---

## 3. Merge actions (this branch)

1. Committed each agent's uncommitted output on its branch (39b509f / d253872 / fef43b6).
2. Sequential `git merge --no-ff` into `claude/cranky-bhabha-1df4d6`, **running only
   the kāraka tests after each**:
   | step | merge commit | conflicts | karaka tests |
   |---|---|---|---|
   | K5 | `4ed6a26` | none (clean) | **101 passed** |
   | K6 | `7b71b90` | dhatu / yaml / karaka_list / generator_status | **124 passed** |
   | K7 | `bf00749` | dhatu / paninian_object / yaml / karaka_list / generator_status | **141 passed, 3 failed** |
3. **Conflict-resolution method** (all conflicts were "both phases appended at the
   same locus"):
   - `sutras_antaranga.yaml`: deterministic reconstruction `ours(K4+K5+K6) + K7-tail`
     (each phase is a verified pure end-append; base line 8083 blank → phase separator).
     Final: 525 YAML rule items, loads clean.
   - `test/karaka_list.py`: reconstruction `ours-minus-final-']' + K7-cases + ']'`
     (git folded the shared trailing brackets; rebuilt to keep all cases well-formed).
     144 test cases, parses clean.
   - `dhatu.py`: single-hunk union (K5+K6 block then K7 block).
   - `paninian_object.py`: unioned the `_is_karaka_tag` tuple
     (`kp_pUrva/kp_para/kp_pancami_*` **and** `kp_saptamI`).
   - `generator_status.md`: resolved expediently during merges, then rebuilt
     authoritatively (commit `a75ab14`): K7 last, K6/K5 earlier, Next→K-UI, counts
     reconciled to **449 implemented / 78 deferred / ~592 total**.

---

## 4. Open issues (must fix before declaring K5–K7 green)

Two **cross-phase symbol collisions** (both K5↔K7) survive the mechanical merge and
regress 3 kāraka tests (141/144 pass):

1. **`biBeti` redefinition** — `dhatu.py` defines it twice: K5 with the `BItrA` tag
   (1.4.25 bhaya-hetu→apādāna) and K7 untagged ("generic adhikaraṇa verb"). K7's later
   definition shadows K5's ⇒ **SK588 चोराद्बिभेति** fails. *Fix:* rename K7's generic
   verb (e.g. its adhikaraṇa example uses a different dhātu) or have it reuse K5's.
2. **`semantic_dUrAntika` tag reuse** — K5's 2.3.35 (dūra/antika 3-way fork) and K7's
   2.3.36 (च: dūra/antika → saptamī) both key on it, so K7's rule fires on K5's SK605
   sentences ⇒ **SK605 दूरम्/अन्तिकम्** (×2) fail (fired trace `['2.3.36']`). *Fix:*
   give the two rules distinct tags (e.g. `semantic_dUrAntika_apAdAna` vs
   `_aDikaraRa`) and update the dependent yaml conditions + the SK605/SK633 test rows.

Also note the **count accounting is approximate** — K5 and K7 never updated their
branch counters, and the K4-era buckets (implemented/deferred/uncatalogued/total)
predate the kāraka section; the reconciled 449/78/~592 reflect +55 implemented / +~10
deferred and should be confirmed against the project's counting convention.

---

## 5. Remaining work

- [ ] Fix the two collisions above; re-run kāraka tests to 144/144.
- [ ] Run the **full generator suite** on the merged branch (awaiting go-ahead).
- [ ] Optional **Phase K-UI** — Vākya Composer (`karaka_plan.md` §4).
- [ ] Update `karaka_plan.md`'s top Status line (still says "K1–K7 not started").

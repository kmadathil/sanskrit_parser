# Bahuvrīhi-samāsa Implementation Plan (SK 829–900)

## Context

The generator has completed the **avyayībhāva** (SK 647–683) and **tatpuruṣa**
(SK 684–828) prakaraṇas on the `generator` branch, both built on a reusable
**samāsa pre-pass** (`AntarangaPrakriya._samasa_prepass`, all rules keyed
`bahiranga: -1`) that runs after the kāraka pre-pass + sup-insertion, scans adjacent
`(pūrva | uttara)` member windows, and assigns the samāsa saṁjñā / member-role / type
tags. The next samāsa type in SK order is **bahuvrīhi** (SK 829–900).

This plan covers the full bahuvrīhi prakaraṇa — the core samānādhikaraṇa formation
(SK829–830 / 2.2.23–24), the additional formation types (saṅkhyā/diś/sarūpa/saha,
SK843–850 / 2.2.25–28 + 6.3.82–83), the word-order rules (SK898–900 / 2.2.35–37), the
**puṁvadbhāva** cluster (SK831,836–842 / 6.3.34–41), and the **complete
samāsānta-affix cluster** (SK832–897 / 5.4.73–160, 7.4.13–15, 8.4.3/28, 6.1.66,
6.4.142/146) — as parallel-worktree phases B0–B4 + B-UI, mirroring the
`tatpuruza_plan.md` (T0–T5) and `karaka_plan.md` (K0–K7) structure. Each phase below
ends with a self-contained *Session prompt*.

> **STATUS (as-built, 2026-07-11): B0–B2 + B-UI complete; B3/B4 samāsānta complete for
> every affix family that declines cleanly; the rest deferred on known engine gaps (see
> §2a).** Implemented across commits `00a9b11`→`45f435b` on `generator`;
> `test/test_samasa_bahuvrihi.py` = 49 cases; full generator suite green. The Phases (§3)
> keep the original forward-looking Session prompts as a historical record —
> **§2a is the authoritative as-built account** (real mechanisms, deviations, gotchas).
>
> **Review round (2026-07-11):** 5.4.154 विभाषा remodelled as a **vivakṣā** (`?kap_vivakzA`,
> not an engine fork); the CLI `-k` accepts a **`?tag` token** (e.g. `?kap_vivakzA`) so kap
> is assertable from the CLI; **5.4.153 नद्यृतश्च** + **5.4.114 अङ्गुलेर्दारुणि** added (5.4.114
> was the one gap a completeness audit found); the **उरःप्रभृति gaṇa** filled
> (उरस्/सर्पिस्/पयस्/लक्ष्मी). **Completeness audit: every SK829–900 sūtra is now accounted —
> implemented, or in an explicit `generator_status.md` Skipped row.**
>
> **ā-stem ādeśa + 6.4.14 round (2026-07-11):** the two "deferred" bullets in §2a were
> **mis-diagnosed** and are corrected there; BOTH fixes have now landed. (a) The real cause
> of the ādeśa breakage was a stale **`?Ap`** tag surviving the substitution (not a stale
> sup), so a one-line `update: orp: [-Ap, -strI]` landed **niṅ SK872/5.4.134 → युवजानिः** and
> **अच् SK858/5.4.119 → उन्नसः**. (b) **6.4.14's `-as` arm was widened** beyond `+u` (guarded
> `?!avyaya`/`?!nipAta`/`?!sarvanAma`), giving यशाः/मनाः/**बहुयशाः** — so SK891 is now the
> canonical **बहुयशस्कः / बहुयशाः**. (c) **asic SK862/5.4.122** landed on the back of (b) → सुप्रजाः/सुमेधाः. Remaining in these
> families: only the अच् **ṇatva** cases (SK856/5.4.118 द्रुणसः, प्रणसः via 8.4.3/28) and the
> nañ arm of asic (अप्रजाः).

**Outcome:** a user can compose a bahuvrīhi (e.g. पीताम्बरः, प्राप्तोदको ग्रामः, उपदशाः,
सपुत्रः, बहुयशस्कः) and the generator derives the surface form — crucially, the
compound is **exocentric**: it declines in the **external referent's gender**
(पीताम्बरः masc / पीताम्बरा fem / पीताम्बरम् neut), not in the gender of either member.

---

## 0. Numbering convention (MANDATORY — applies to every phase)

Per the dual-sutra-numbering convention, **every sūtra reference must carry BOTH its
SK number and its Ashtadhyayi id**, SK-first, e.g. `SK830 / 2.2.24`. This is
non-negotiable and applies in **all four places**:

1. **This doc** — prose, tables, and bullets (the scope map in §2 lists both; keep both
   when referencing a sūtra inline).
2. **YAML block comments** in `sutras_antaranga.yaml` — the `# <N>:` comment line for
   each rule leads with the SK number and includes the id, e.g.
   `# 830: अनेकमन्यपदार्थे (SK830 / 2.2.24)`. (The `id:` field stays the bare Ashtadhyayi
   id, as the DSL requires.)
3. **Test-case `label`s** in `test/samasa_list.py` — every label carries both, e.g.
   `"label": "B0-pItAmbaraH-SK830-2.2.24"`.
4. **Fired-trace assertions** — the `"fired"` list uses the Ashtadhyayi ids (that is
   what `karaka_log` records), but the surrounding label/comment names the SK number so
   a reader can cross-map without the `skn` table.

The SK↔Ashtadhyayi map for this range is the `skn` field in `ashtadhyayi-com/data`
`sutraani/data.txt`; the §2 scope map reproduces it.

---

## 1. Why bahuvrīhi is architecturally different

| Samāsa | Compound gender | Mechanism |
|---|---|---|
| avyayībhāva | fixed napuṁsaka / avyaya | 2.4.18 + `_commit_samasa_napum` |
| tatpuruṣa / dvigu | uttara-pada's gender | 2.4.26 परवल्लिङ्गम् → `join_objects` "prefer last" |
| **bahuvrīhi** | **external referent (anyapadārtha)** | **NEW — this plan** |

A bahuvrīhi denotes *another* thing not connoted by its members (SK830 / 2.2.24
अनेकमन्यपदार्थे). Both members are prathamānta in the vigraha and both are upasarjana;
neither is grammatically pradhāna. The whole word behaves like an adjective agreeing
with an external substantive, so its **liṅga / vacana / vibhakti come from that
referent**, independent of both members (पीत+अम्बर: अम्बर is neuter, yet पीताम्बरः is
masculine when the referent, Viṣṇu, is masculine).

**The ONE genuinely new mechanism (Phase B0):** referent-gender override. The current
`join_objects` gender logic (`paninian_object.py:154–174`) prefers the last (uttara)
element's gender, falling back to the first's. Bahuvrīhi must override this so the
merged stem takes the **composer-supplied referent liṅga**. We reuse the existing
`?samasa_liNga_locked` escape hatch (already honoured by `join_objects:159–164`, set
today by `_commit_samasa_napum` for napuṁsaka dvigu): a B0 pre-pass rule sets the
compound gender = referent liṅga on the pūrva-most stem **and** `?samasa_liNga_locked`,
so `join_objects` propagates the referent gender rather than the uttara's. The composer
supplies the referent liṅga (+ vacana / vibhakti) directly — exactly as the tatpuruṣa
tests supply the uttara vibhakti directly.

**Reused as-is (no engine change):**
- The samāsa pre-pass spine: `_samasa_prepass`, `_samasa_prepass_branch`,
  `_samasa_window_fixpoint`, `_is_samasa_member`, `_nest_samasa_members`, the
  `?samAsa_vivakza` intent gate, vibhāṣā forking (`antaranga_prakriya.py:563–810`).
- Member-role tagging: pūrva → `?samAsaPurva` (+ `?upasarjana` via SK-earlier 1.2.43),
  uttara → `?samAsa` + type tag (here `?bahuvrIhi`).
- **2.4.71** सुपो धातुप्रातिपदिकयोः — luks the pūrva member's internal sup.
- `?swap_viBakti` + `_swap_sups` to consume a member's vigraha vibhakti.
- **`?samasanta_TaC` + `_insert_samasanta`** post-pass — the proven affix-insertion path
  for every bahuvrīhi samāsānta (generalize the marker so it can carry different
  affixes: kap / ḍac / ac / ṣac / …; see B3).
- The `join_objects` Tier-3 tag propagation — `?bahuvrIhi` is **already** in the
  tadDita-gated allowlist (`paninian_object.py:263`), so the strī-block gender/ṇatva
  rules already gated on `?bahuvrIhi` (SK 460–488, ṅīp/ṅīṣ/ḍāp) keep working.
- CLI `-B` / `--bahuvrihi` (`CustomActionBahuvrihi`, `cmd_line.py:252`) already tags a
  member `in_context(in_compound(p), "bahuvrIhi")` — extend, don't rebuild.

**Deferred (record in status), mirroring tatpuruṣa's 2.2.30 deferral:**
- **Physical pūrva-nipāta (2.2.30, and the word-order effect of SK898–900 / 2.2.35–37).**
  The pre-pass only writes tags; it never reorders members. For every case where the
  composer supplies members in the correct surface order, no reorder is needed. SK898
  (2.2.35 saptamī/viśeṣaṇa first) and SK899 (2.2.36 niṣṭhā first) *decide* which member
  is pūrva; we implement them as **tagging + a validation assertion on input order** and
  defer the physical reorder engine change. Noted explicitly in B2.
- Accent-gated rules (already deferred for SK 508/509 antodātta).

---

## 2. Scope map (SK 829–900)

| Block | SK / sūtra | Phase |
|---|---|---|
| **saṁjñā adhikāra** शेषो बहुव्रीहिः | SK829 / 2.2.23 | B0 |
| **core** अनेकमन्यपदार्थे (samānādhikaraṇa) | SK830 / 2.2.24 | B0 |
| **referent-gender override** (anyapadārtha) | — (new mechanism) | B0 |
| **puṁvadbhāva** स्त्रियाः पुंवत् … | SK831,836–842 / 6.3.34–41 | B1 |
| **saṅkhyā** bahuvrīhi | SK843 / 2.2.25 | B2 |
| **diś** अन्तराले | SK845 / 2.2.26 | B2 |
| **sarūpa / reciprocal** तत्र तेनेदमिति | SK846 / 2.2.27 | B2 |
| **saha / tulyayoga** तेन सहेति | SK848 / 2.2.28 + SK849–850 / 6.3.82–83 (saha→sa) | B2 |
| **word order** (deferred physical reorder) | SK898–900 / 2.2.35–37 | B2 |
| **samāsānta — affix insertion** (ap/ac/kap/ḍac/ṣac/asic/anic/ic) | SK832–835,844,847,851–863,866–867,889–897 / 5.4.73,113–128,151–160, 7.4.13–15, 8.4.3/28, 6.4.142/146 | B3 |
| **samāsānta — ādeśa / lopa / nipātana** (jñu, anaṅ, niṅ, id, pad, datṛ, kakud, hṛd, jambhā…) | SK864–865,868–888 / 5.4.125–150, 6.1.66 | B4 |
| **UI + CLI** | — | B-UI |

**Already implemented** (feminine-affix bahuvrīhi arm, part of the ṅīp/ṅīṣ prakaraṇa —
do **not** redo): SK460–462 (4.1.12/13/28 an-final bahuvrīhi ṅīp), SK463 (7.3.44
asuwapaH), SK483–488 (4.1.25–30 ūdhas / keval-ādi arms). B0 must not regress these.

**How to run this plan:** **Phase B0 must complete and merge first**; B1–B4 and B-UI
are then largely independent and can run in parallel worktrees, merged with
`/gen-merge`. B3 and B4 are the two large phases and may each be split further across
parallel worktrees by affix family. When spawning worktree-isolated background agents,
pin the base branch (the B0 tip) and forbid git surgery — merge prerequisites into the
base first.

---

## 2a. Implementation status (as-built, 2026-07-11)

Built sequentially on `generator` (not parallel worktrees). Commits: B0 `00a9b11`,
B1 `b8690af`, B2 `0cbac07`, B3-kap `04de0a1`, B3-ṣac/ap/ic+B4-jñu `3f54b6f`, B4-ext
`901965e`, B3/B4-more `0327301`, B-UI `45f435b`. Tests: `test/test_samasa_bahuvrihi.py`
(39 cases: structure/fired/surface + gender & vibhakti sweeps + CLI smoke), cases in
`test/samasa_list.py :: samasa_bv_tests`. Full suite 8188 green.

### Files touched (the whole prakaraṇa)
- `sutras_antaranga.yaml` — the bahuvrīhi rule blocks (B0–B4), all `bahiranga: -1`
  pre-pass rules appended after the tatpuruṣa block; plus a `?!bahuvrIhi_saha` guard
  added to the avyayībhāva **6.3.81**.
- `antaranga_prakriya.py` — **generalized `_insert_samasanta`**: a class-level
  `_SAMASANTA_AFFIXES = {"samasanta_TaC": wac, "samasanta_kap": kap, "samasanta_Sac":
  Sac, "samasanta_ap": ap_s, "samasanta_ic": ic_s}` map; the method inserts whichever
  affix the uttara's `?samasanta_*` marker names. Adding a family = one map entry.
- `pratyaya.py` — new samāsānta affixes `Sac` (षच्), `ap_s` (अप्), `ic_s` (इच्); `wac`/`kap` reused.
- `pratipadika.py` — B0–B4 stems (pIta/ambara/prApta/udaka; dIrGa/jaNGa/BArya/brAhmaRI/
  dattA/pAcikA/sukeSI; saha reused, dakziRa_dik; uras/vyUQa/mUrDan/loman/daRqa;
  UrDva/gandha/hfdaya/Darma/kakuda; jAyA/yuvan defined for the deferred niṅ).
- `cmd_line.py` — `--referent-linga` + `prepare_bahuvrihi(words, linga)`.
- `ui/app.py` — `/api/karaka` `referent_linga` → `run_karaka(..., referent_linga)` →
  `_apply_bahuvrihi`; `ui/templates/karaka.html` — referent-liṅga `<select>`.

### The ONE new mechanism — anyapadārtha gender (B0)
2.2.23+2.2.24 are **fused into a single `id: 2.2.24` rule** (the engine's `sutra_dict`
forbids duplicate ids, so the adhikāra can't be its own rule). The referent-gender lock
is **folded into that same rule** (`orp: [+samAsa, +bahuvrIhi, +samasa_liNga_locked]`):
the composer overrides the uttara's native gender to `?referent_pum|strI|napum` and the
rule pins it, so `join_objects` (`paninian_object.py:159–164`) propagates the referent
gender instead of the uttara's. Intent tag = **`?bahuvrIhi_vivakza`** (the composer/CLI
sets it; the uttara is NOT viBakti-constrained — it carries the referent's external case,
like the tatpuruṣa uttara). A **fem referent appends `strI_abs`** (ṭāp) so an a-stem
uttara feminises (पीताम्बर→पीताम्बरा). Gender sweep पीताम्बरः/पीताम्बरा/पीताम्बरम् + masc vibhakti
sweep prove exocentricity.

### Per-phase as-built + deviations from the original plan
| Phase | Done | Real detail / deviation |
|---|---|---|
| **B0** ✅ | SK829/830 fused | referent-gender lock folded into 2.2.24; `?bahuvrIhi_vivakza` intent; uttara not viBakti-gated; fem needs `strI_abs` |
| **B1** ✅ | 6.3.34 + 6.3.37/38/40/41 | saṁjñā-marker model (like tatpuruṣa 6.3.42); composer supplies the masc form; **the vigraha-femininity of the uttara is carried by a stable `?uttara_strI` tag** (its native `?strI` is overwritten by the B0 referent override); inherently-fem ā-stem uttaras modelled as an a-stem BASE (jaNGa/BArya) + `strI_abs`. Deferred: 6.3.35/36 (affix-context), 6.3.39 (taddhita-vṛddhi) |
| **B2** ✅ | 2.2.28 saha + 6.3.82/83; 2.2.26 diś | saha is indeclinable → its own formation rule (2.2.24 needs `?viBakti_1`); tags the saha pūrva `?bahuvrIhi_saha` so **6.3.82 (not the avyayībhāva 6.3.81) handles saha→sa** — 6.3.81 gained a `?!bahuvrIhi_saha` guard. saha needs a sup present (`has_viBakti`) for 6.3.82's `rp ?sup`. **Deviation from plan:** 2.2.25 (saṅkhyā→ḍac), 2.2.27 (sarūpa→ic), 2.2.35–37 (word order) deferred — see below |
| **B3** ✅ (families) | kap 5.4.151/153/154/155; ṣac 5.4.113/114/115; ap 5.4.117; ic 5.4.128 | **generalized `_SAMASANTA_AFFIXES`** is the enabler. 5.4.154's विभाषा is a **vivakṣā** (`?kap_vivakzA`, non-optional — बहुयशस्कम् with / बहुयशः without), not an engine fork. 5.4.151 उरःप्रभृति gaṇa filled (उरस्/सर्पिस्/पयस्/लक्ष्मी → प्रियसर्पिष्कः …); 5.4.153 नद्यृतश्च (बहुकुमारीकः/बहुमातृकः), 5.4.114 अङ्गुलेर्दारुणि (पञ्चाङ्गुलम्) added in review. Cases use a **neuter referent** where the masc s-stem 6.4.14 dīrgha would be needed (बहुयशः, not बहुयशाः) |
| **B4** ✅ (families) | jñu 5.4.129/130; anaṅ 5.4.132; anic 5.4.124; gandha→id 5.4.135; pāda 5.4.140; kakud 5.4.146; hṛd 5.4.150 | pre-pass uttara-substitution (`rc→""`, `r→"<stem>"`, mirroring tatpuruṣa 6.3.46). **Tractability boundary discovered** — see below |
| **B-UI** ✅ | CLI + composer API + frontend | `prepare_bahuvrihi`/`_apply_bahuvrihi` share the B0 tag contract; `referent_linga=""` is backward-compatible (avyayībhāva/tatpuruṣa unaffected). **Deviation:** the plan said "no engine changes" — true; but the UI needed a new `referent_linga` request field + `_apply_bahuvrihi` helper, not just presets |

### The samāsānta-ādeśa tractability boundary
A pre-pass uttara-substitution rewrites the stem **string** but leaves the member's
**stem-class tags** untouched. So:
- **Works out of the box** — substitution to an **n-stem** (धनुस्→धन्वन्, धर्म→धर्मन्) or a
  **consonant-final** stem (हृदय→हृद्, पाद→पाद्, ककुद→ककुद्): the source stems carry no
  class tag that misdirects the sup, so the existing `su` + the main-scan class rules
  give the right nom sg (सुधन्वा, कल्याणधर्मा, सुहृत्, द्विपात्; 8.4.56 वाऽवसाने gives the द्/त् pairs).
- **Needed a one-line tag clear — now DONE** — substitution *out of* a **feminine ā-stem**
  (जाया→जानि niṅ 5.4.134, नासिका→नस अच् 5.4.119): the source carries **`?Ap`**, which
  survives the substitution and drives ā-stem nom-sg su-elision → the surface lost its
  visarga (जानि, प्रनस). Adding `update: orp: [-Ap, -strI]` to the rule fixes it; both are
  now implemented — **युवजानिः** (5.4.134) and **उन्नसः** (5.4.119). Independently, अच् still
  needs the 8.4.3/28 **ṇatva across the compound** for द्रुणसः/प्रणसः (5.4.118 saṁjñā arm).

### Remaining work
> Two of these were mis-diagnosed in the first pass; both root causes have now been
> verified experimentally and are restated correctly below.

- **Stale stem-class tags after an ādeśa — a ONE-LINE YAML fix, not an engine step. ✅ APPLIED.**
  *(Supersedes the earlier "sup re-insertion via a `?resup` post-pass" note, which was
  wrong: sup morphemes (su/au/jas…) are class-neutral, so re-inserting `su` changes
  nothing.)* **Root cause (verified):** a pre-pass uttara-substitution rewrites the stem
  *string* (`rc→""`, `r→"<new>"`) but leaves the **old stem's class tags** on the member.
  Both `जाया` and `नासिका` carry **`?Ap`** (the ṭāp ā-stem marker), and `?Ap` drives
  ā-stem nom-sg su-elision — so the substituted `जानि` / `नस` lose their visarga
  (जानि, प्रनस). *Proof:* the very same a-stem `अम्बर` yields पीताम्बर**ः** normally but
  पीताम्बर (no visarga) with `?Ap` forced onto it.
  **Fix:** add `update: orp: [-Ap, -strI]` to the ādeśa rule, alongside its `xform`.
  **Landed:** niṅ **SK872/5.4.134** → **युवजानिः** (it also fixed the युवन् न्/ñ cascade), and
  अच् **SK858/5.4.119** → **उन्नसः** (उद्नसः is the other 8.4.45 वा fork). What remains of the
  अच् family is only the **saṁjñā arm SK856/5.4.118** (द्रुणसः) and **प्रणसः**, both of which
  need the 8.4.3/28 **ṇatva across the compound** — verified NOT firing (प्रनसः).
- **6.4.14's `-as` arm was `+u`-only — WIDENED. ✅ APPLIED.** *(Supersedes "6.4.14 dīrgha
  under the gender-override"; the gender-override was never the issue.)* **Root cause
  (verified):** the arm required `+u` (a u-it marker), so it fired only for u-it stems
  (matup / ktavatu / **īyasun**) and never for an underived अस्-final noun — a plain masc
  `यशस् + su` gave **यशः, not यशाः, even standalone** (`yaSas.its == []`).
  **Fix applied:** drop `+u` from the `-as` arm (the sūtra is अत्वसन्तस्य — *any* अस्-ending
  non-dhātu), keeping `?pum` + `?su` + `?!sambudDi` (अस्-stems lengthen only in nom sg:
  वेधाः but वेधसौ/वेधसः). **Guards added** — `?!avyaya`, `?!nipAta`, `?!sarvanAma` — because
  relaxing `+u` would otherwise catch the as-final *non-declining/pronominal* stems
  तिरस्/अधस् and, critically, **अदस्** (असौ has its own rules).
  **Result:** यशाः, मनाः, and **बहुयशाः** — so the SK891 pair is now the canonical
  **बहुयशस्कः / बहुयशाः** (the tests no longer need the neuter-referent workaround).
  Unchanged: श्रेयान्, विद्वान्, **असौ**, तिरः, अधः, and all neuters (मनः/यशः).
  With that in place, **asic SK862/5.4.122 was also landed** (new `asic` Pratyaya +
  `_SAMASANTA_AFFIXES` entry + the same `-Ap` clear) → **सुप्रजाः / सुमेधाः**; only its nañ
  arm (अप्रजाः) still awaits the nañ-bahuvrīhi formation path.
- **दतृ न्-declension** → **datṛ 5.4.141** (द्विदन्; engine currently gives द्विदत्).
- **Reduplication** → **reciprocal ic 5.4.127** (केशाकेशि, pairs with 2.2.27).
- **ḍac 5.4.73** (उपदशाः) is accent-only — no visible surface to verify (with 2.2.25).
- **5.4.133** dhanus-saṁjñā fork शतधनुः — the nitya 5.4.132 still fires in the vibhāṣā
  skip branch (needs 5.4.133 to override 5.4.132 in BOTH branches).
- Minor कप् (5.4.152/153/156/157/159/160, 7.4.13–15), अप् 5.4.116 (pūraṇī pl), gandha
  5.4.136/137 (same गन्धि surface as 5.4.135, needs सूप/पद्म stems + sense tags).
- **Formation deferrals (physical reorder):** 2.2.25 saṅkhyā (→ḍac), 2.2.27 sarūpa (→ic),
  2.2.35–37 word order — all need the vyadhikaraṇa-bahuvrīhi + physical **pūrva-nipāta
  2.2.30** engine step (the same mechanism tatpuruṣa deferred); B1 6.3.35/36/39.

---

## 3. Phases

### Phase B0 — Spine + bahuvrīhi saṁjñā + anyapadārtha gender + core formation — ✅ DONE (`00a9b11`; see §2a)

The foundational slice that proves the **exocentric, referent-gender** compound.
- **SK829 / 2.2.23 शेषो बहुव्रीहिः** — the adhikāra. No standalone rule needed; folded
  into 2.2.24 as the type tag.
- **SK830 / 2.2.24 अनेकमन्यपदार्थे** — the core defining rule (fused with 2.2.23).
  Condition: both members `?viBakti_1` (prathamā-vigraha) + `?samAsa_vivakza` +
  `?!samAsaPurva`; uttara `?prAtipadika` + `?!samAsa`. Update: pūrva
  `+samAsaPurva` (+ `+swap_viBakti` `+viBakti_1` to reset for external case), uttara
  `+samAsa +bahuvrIhi`. 1.2.43 upasarjana fires on the pūrva (reuse); optionally tag
  the uttara `?upasarjana` too (both members subordinate — a comment suffices).
- **Referent-gender override (NEW)** — a `bahiranga: -1` rule, condition
  `rp: ?bahuvrIhi` + a composer-supplied `?referent_pum|strI|napum` tag: set that
  liṅga on the pūrva-most stem + `?samasa_liNga_locked`, so `join_objects` locks the
  referent gender. Do **not** use 2.4.26. The composer also sets the uttara's
  `?viBakti_N` + `?vacana_M` to the referent's, so the retained uttara sup inflects in
  the referent's case/number.
- **2.4.71** (reuse): pūrva sup luks → पीत (no am).
- **Surface goal:** पीत(1) + अम्बर(1) → **पीताम्बरः**, with a **gender sweep** proving
  exocentricity: पीताम्बरः / पीताम्बरा / पीताम्बरम्, plus a vibhakti sweep in one gender.
  Also प्राप्तोदको ग्रामः (प्राप्त+उदक), बहुव्रीहिः itself.

**Files:** `sutras_antaranga.yaml` (new bahuvrīhi block after the tatpuruṣa block,
~line 10695); `antaranga_prakriya.py` (verify the referent-gender rule's lock reaches
`join_objects`; small tweak only if needed); `pratipadika.py` (stems: पीत, अम्बर,
प्राप्त, उदक — check for dupes first); `test/samasa_list.py` + new
`test/test_samasa_bahuvrihi.py` (three assertion levels: structure / fired-trace /
surface, modeled on `test_samasa_tatpurusha.py`) with a composer that accepts a
`referent_linga` field.

**B0 must complete and merge before B1–B4.**

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B0) and skim the
tatpuruṣa samāsa block in sutras_antaranga.yaml (~10695) + _samasa_prepass in
antaranga_prakriya.py + the gender logic in paninian_object.py:154–174. Implement the
bahuvrīhi foundation — an EXOCENTRIC compound that declines in an EXTERNAL REFERENT's
gender (not the uttara's, unlike tatpuruṣa 2.4.26). (1) sutras_antaranga.yaml: new
bahuvrīhi block of bahiranga: -1 pre-pass rules after the tatpuruṣa block. SK830/2.2.24
अनेकमन्यपदार्थे (fused with SK829/2.2.23 adhikāra): condition lp = (?viBakti_1,
?samAsa_vivakza, ?!samAsaPurva), rp = (?prAtipadika, ?!samAsa); update olp
+samAsaPurva +swap_viBakti +viBakti_1, orp +samAsa +bahuvrIhi. Reuse 1.2.43
upasarjana. (2) NEW referent-gender rule (bahiranga: -1, condition rp ?bahuvrIhi +
composer tag ?referent_pum|?referent_strI|?referent_napum): set that liṅga on the
pūrva-most stem AND ?samasa_liNga_locked so join_objects (paninian_object.py:159–164)
locks the referent gender; do NOT use 2.4.26. (3) 2.4.71 luks the pūrva sup (reuse).
(4) test/test_samasa_bahuvrihi.py (new, three levels) + cases in test/samasa_list.py;
extend the composer to accept a referent_linga (and set the uttara viBakti/vacana to
the referent's). Surface goal पीताम्बरः with a GENDER SWEEP (पीताम्बरः/पीताम्बरा/पीताम्बरम्)
proving referent-gender exocentricity, plus a vibhakti sweep. No regressions to the
existing ?bahuvrIhi strī-block rules (SK460–488). NUMBERING (per §0): every YAML block
comment and every test-case label carries BOTH the SK number and the Ashtadhyayi id,
SK-first — YAML `# 830: अनेकमन्यपदार्थे (SK830 / 2.2.24)`, test label
`"B0-pItAmbaraH-SK830-2.2.24"`. Full generator suite green (pytest -n 8 --dist
worksteal from generator/test). Update generator_status.md.
```

### Phase B1 — Puṁvadbhāva (SK831,836–842 / 6.3.34–41) — ✅ DONE (`b8690af`; 6.3.35/36/39 deferred; see §2a)

Feminine pūrvapada → masculine form in a samānādhikaraṇa bahuvrīhi. Needs feminine
stems that carry a **bhāṣitapuṁska** (corresponding-masculine) form + a not-ūṅ marker.
- **SK831 / 6.3.34 स्त्रियाः पुंवत्…**: the main rule — a bhāṣitapuṁska, non-ūṅ feminine
  pūrva in apposition takes its masculine form (दीर्घे जङ्घे यस्य → दीर्घजङ्घः), except
  before an ordinal / priyādi.
- **SK836 / 6.3.35 तसिलादिष्वाकृत्वसुचः**, **SK837 / 6.3.36 क्यङ्मानिनोश्च**: extend
  puṁvadbhāva before tasil-ādi affixes and kyaṅ/mānin.
- **Prohibitions:** SK838 / 6.3.37 न कोपधायाः (k-penult fem), SK839 / 6.3.38
  संज्ञापूरण्योश्च (name/ordinal), SK840 / 6.3.39 वृद्धिनिमित्तस्य…, SK841 / 6.3.40
  स्वाङ्गाच्चेतः (svāṅga -ī), SK842 / 6.3.41 जातेश्च (jāti).

Implement as pre-pass pūrva-substitution rules (like tatpuruṣa 6.3.42 puṁvadbhāva in
karmadhāraya, SK746 — reuse its shape) keyed on the fem pūrva + `?bahuvrIhi`. Add fem
stems with a masculine-form tag. Cases: दीर्घजङ्घः; a name/ordinal prohibition case.
Independent worktree off B0.

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B1); B0 is merged.
Implement the bahuvrīhi puṁvadbhāva cluster (feminine pūrvapada → masculine) as
bahiranga: -1 pre-pass pūrva-substitution rules keyed on the fem pūrva + ?bahuvrIhi,
reusing the shape of the existing SK746/6.3.42 karmadhāraya puṁvadbhāva. SK831/6.3.34
स्त्रियाः पुंवत् (main: bhāṣitapuṁska non-ūṅ fem → masc, दीर्घजङ्घः; blocked before
ordinal/priyādi), SK836/6.3.35 तसिलादिषु, SK837/6.3.36 क्यङ्मानिनोश्च; prohibitions
SK838/6.3.37 न कोपधायाः, SK839/6.3.38 संज्ञापूरण्योश्च, SK840/6.3.39 वृद्धिनिमित्तस्य…,
SK841/6.3.40 स्वाङ्गाच्चेतः, SK842/6.3.41 जातेश्च. Add feminine stems carrying a
bhāṣitapuṁska (masc-form) tag + a not-ūṅ marker (check pratipadika.py for dupes first).
Cases दीर्घजङ्घः + one prohibition case into test/samasa_list.py +
test_samasa_bahuvrihi.py, labels dual-numbered SK-first per §0 (e.g.
"B1-dIrGajaNGaH-SK831-6.3.34"), YAML comments likewise. Full suite green. Update
generator_status.md; defer the priyādi-gaṇa long tail with a Skipped row if not reached.
```

### Phase B2 — Additional formation types + word order — ✅ DONE for saha + diś (`0cbac07`); 2.2.25/2.2.27/2.2.35–37 deferred (see §2a)

- **SK843 / 2.2.25 संख्यया…**: indeclinable / āsanna / adūra / adhika + saṅkhyā →
  bahuvrīhi (उपदशाः "about ten"). Feeds ḍac in B3.
- **SK845 / 2.2.26 दिङ्नामान्यन्तराले**: compass names → intermediate direction
  (दक्षिणपूर्वा).
- **SK846 / 2.2.27 तत्र तेनेदमिति सरूपे**: two homonyms (both loc. or both instr.) in a
  reciprocity sense (केशाकेशि vigraha). Feeds ic (SK866 / 5.4.127) in B4.
- **SK848 / 2.2.28 तेन सहेति तुल्ययोगे**: सह + third-case word → bahuvrīhi (सपुत्रः).
  With **SK849 / 6.3.82 वोपसर्जनस्य** (saha → sa optionally: सपुत्रः / सहपुत्रः) and
  **SK850 / 6.3.83 प्रकृत्याशिषि** (saha stays in benediction, except go/vatsa/hala).
- **Word order SK898–900 / 2.2.35–37**: SK898 / 2.2.35 सप्तमीविशेषणे (saptamī /
  viśeṣaṇa member first, कण्ठेकालः), SK899 / 2.2.36 निष्ठा (niṣṭhā first, कृतकृत्यः),
  SK900 / 2.2.37 वाहिताग्न्यादिषु (āhitāgnyādi ākṛtigaṇa, optional niṣṭhā-first).
  Implement as **tagging + input-order validation**; **defer the physical member
  reorder** (record a Skipped row — same deferral posture as tatpuruṣa 2.2.30).

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B2); B0 is merged.
Implement the additional bahuvrīhi formation types + word-order rules as bahiranga: -1
pre-pass rules. SK843/2.2.25 संख्यया (saṅkhyā/āsanna/adūra/adhika + number → उपदशाः;
feeds ḍac), SK845/2.2.26 दिङ्नामानि (compass → intermediate, दक्षिणपूर्वा), SK846/2.2.27
तत्र तेनेदमिति सरूपे (homonym reciprocity, केशाकेशि vigraha; feeds ic), SK848/2.2.28 तेन सह
(सह + tṛtīyā → सपुत्रः) + SK849/6.3.82 वोपसर्जनस्य (saha→sa optional: सपुत्रः/सहपुत्रः) +
SK850/6.3.83 प्रकृत्याशिषि (saha stays in benediction except go/vatsa/hala). Word order
SK898/2.2.35 सप्तमीविशेषणे, SK899/2.2.36 निष्ठा, SK900/2.2.37 वाहिताग्न्यादिषु: implement
as member-role tagging + an input-order validation assertion; DEFER the physical
reorder engine change (Skipped row, mirroring tatpuruṣa 2.2.30). Cases उपदशाः,
सपुत्रः/सहपुत्रः into test/samasa_list.py + test_samasa_bahuvrihi.py, labels + YAML
comments dual-numbered SK-first per §0 (e.g. "B2-saputraH-SK848-2.2.28"). Full suite
green. Update generator_status.md with the deferrals.
```

### Phase B3 — Samāsānta: affix insertion — ✅ DONE for kap/ṣac/ap/ic (`04de0a1`,`3f54b6f`); mechanism generalized; रest deferred (see §2a)

All bahuvrīhi samāsānta rules that **add** an affix, via a generalized
`?samasanta_TaC`-style marker + `_insert_samasanta` (extend the marker to carry the
affix identity: kap / ḍac / ac / ṣac / ap / asic / anic / ic — one deepcopy-insert per
family). Each rule is a `bahiranga: -1` pre-pass rule setting the marker on the
qualifying uttara; the affix's own phonological consequences fire in the main scan.
- **kap (क):** SK889 / 5.4.151 उरःप्रभृतिभ्यः (व्यूढोरस्कः), SK890 / 5.4.152 इनः स्त्रियाम्,
  SK833 / 5.4.153 नद्यृतश्च + SK834 / 7.4.13 केऽणः hrasva + SK835 / 7.4.14 न कपि (blocks
  hrasva under kap); **SK891 / 5.4.154 शेषाद्विभाषा** (the big optional kap — बहुयशस्कः /
  बहुयशाः) + SK892 / 7.4.15 आपोऽन्यतरस्याम् (optional ā-hrasva) + prohibitions SK893 /
  5.4.155 न संज्ञायाम्, SK894 / 5.4.156 ईयसश्च, SK895 / 5.4.157 वन्दिते भ्रातुः, SK896 /
  5.4.159 नाडीतन्त्र्योः, SK897 / 5.4.160 निष्प्रवाणिश्च (kabbhāva nipātana).
- **ḍac (डच्):** SK851 / 5.4.73 बहुव्रीहौ संख्येये (उपदशाः) + SK844 / 6.4.142 ति
  विंशतेर्डिति (ति-lopa: आसन्नविंशाः).
- **ap (अप्):** SK832 / 5.4.116 अप्पूरणीप्रमाण्योः (कल्याणीपञ्चमाः), SK855 / 5.4.117
  अन्तर्बहिर्भ्यां लोम्नः (अन्तर्लोमः).
- **ṣac / ṣa (षच्):** SK852 / 5.4.113 सक्थ्यक्ष्णोः स्वाङ्गात्, SK853 / 5.4.114
  अङ्गुलेर्दारुणि, SK854 / 5.4.115 द्वित्रिभ्यां ष मूर्ध्नः + SK847 / 6.4.146 ओर्गुणः
  (guṇa under the tadDhita: बाहू → बाहवि).
- **ac (अच्):** SK856 / 5.4.118 अञ् नासिकायाः (नासिका → नस्) + SK857 / 8.4.3
  पूर्वपदात्संज्ञायामगः (ṇatva: द्रुणसः), SK858 / 5.4.119 उपसर्गाच्च (उन्नसः) + SK859 /
  8.4.28 उपसर्गाद्बहुलम् (ṇatva bahulam: प्रणसः), SK860 / 5.4.120 सुप्रातसुश्व… (nipātana
  list), SK861 / 5.4.121 नञ्दुःसुभ्यो हलिसक्थ्योः (optional).
- **asic / anic:** SK862 / 5.4.122 नित्यमसिच् प्रजामेधयोः (अप्रजाः), SK863 / 5.4.124
  धर्मादनिच्केवलात् (कल्याणधर्मा).
- **ic (इच्):** SK866 / 5.4.127 इच् कर्मव्यतिहारे (केशाकेशि — pairs with SK846 / 2.2.27),
  SK867 / 5.4.128 द्विदण्ड्यादिभ्यश्च (द्विदण्डि).

This phase is large; it may be split across parallel worktrees by affix family (kap /
ḍac+ap / ṣac / ac+ṇatva / asic+anic+ic). Add the required stems (उरस्, यशस्, नदी-class
fem, विंशति, पञ्चमी, लोमन्, सक्थि, अक्षि, अङ्गुलि, मूर्धन्, नासिका, प्रजा, मेधा, धर्म…).

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B3); B0 is merged.
Implement the FULL bahuvrīhi samāsānta AFFIX-INSERTION set, via a generalized
?samasanta marker + _insert_samasanta (extend the existing ?samasanta_TaC path so the
marker carries the affix identity — kap/ḍac/ac/ṣac/ap/asic/anic/ic — one deepcopy
insert per family; the affix's phonology fires in the main scan). Each rule is a
bahiranga: -1 pre-pass rule on the qualifying uttara. kap: SK889/5.4.151 उरःप्रभृतिभ्यः,
SK890/5.4.152 इनः स्त्रियाम्, SK833/5.4.153 नद्यृतश्च + SK834/7.4.13 केऽणः + SK835/7.4.14
न कपि, SK891/5.4.154 शेषाद्विभाषा (बहुयशस्कः/बहुयशाः) + SK892/7.4.15 आपोऽन्यतरस्याम् +
prohibitions SK893/5.4.155, SK894/5.4.156, SK895/5.4.157, SK896/5.4.159, SK897/5.4.160.
ḍac: SK851/5.4.73 + SK844/6.4.142 ति विंशतेः. ap: SK832/5.4.116 पूरणीप्रमाणी,
SK855/5.4.117 लोमन्. ṣac: SK852/5.4.113, SK853/5.4.114, SK854/5.4.115 + SK847/6.4.146
ओर्गुणः. ac: SK856/5.4.118 नासिका→नस् + SK857/8.4.3 ṇatva, SK858/5.4.119 + SK859/8.4.28
ṇatva bahulam, SK860/5.4.120 nipātana list, SK861/5.4.121 optional. asic/anic:
SK862/5.4.122, SK863/5.4.124. ic: SK866/5.4.127 (केशाकेशि, pairs with SK846/2.2.27),
SK867/5.4.128. Add all required stems (check pratipadika.py for dupes). This is a big
phase — you may split by affix family into parallel worktrees. Cases: बहुयशस्कः/बहुयशाः,
उपदशाः, व्यूढोरस्कः, केशाकेशि, अप्रजाः into test/samasa_list.py +
test_samasa_bahuvrihi.py, each with a sweep; every label + YAML comment dual-numbered
SK-first per §0 (e.g. "B3-bahuyaSaskaH-SK891-5.4.154"). Full suite green (watch
avyayībhāva/tatpuruṣa samāsānta tests). Update generator_status.md.
```

### Phase B4 — Samāsānta: ādeśa / lopa / nipātana — ✅ DONE for jñu/anaṅ/anic/gandha/pāda/kakud/hṛd (`3f54b6f`,`901965e`,`0327301`); ā→i/a-stem cases deferred (see §2a)

The samāsānta rules that **substitute or delete** part of the uttara stem (not
affix-insertion). Implement as `bahiranga: -1` pre-pass uttara-substitution rules
(char-window `l`/`lc`/`rc` or whole-stem replace, mirroring the tatpuruṣa
SK807 / 6.3.46 महत्→महा pattern), plus main-scan phonology where needed.
- **jñu ādeśa:** SK868 / 5.4.129 प्रसंभ्यां जानुनोर्ज्ञुः (प्रज्ञुः), SK869 / 5.4.130
  ऊर्ध्वाद्विभाषा (optional).
- **anaṅ:** SK870 / 5.4.132 धनुषश्च (धनुस् → धन्वन्, शार्ङ्गधन्वा), SK871 / 5.4.133 वा
  संज्ञायाम् (optional).
- **niṅ:** SK872 / 5.4.134 जायाया निङ् (जाया → जानि) + SK873 / 6.1.66 लोपो व्योर्वलि
  (युवजानिः).
- **gandha → id:** SK874 / 5.4.135 गन्धस्येत् (सुगन्धिः), SK875 / 5.4.136 अल्पाख्यायाम्,
  SK876 / 5.4.137 उपमानाच्च.
- **pāda → pad / lopa:** SK877 / 5.4.138 पादस्य लोपः (व्याघ्रपात्), SK878 / 5.4.139
  कुम्भपदीषु च (nipātana + ṅīp: कुम्भपदी), SK879 / 5.4.140 संख्यासुपूर्वस्य (द्विपात्).
- **danta → dat:** SK880 / 5.4.141 वयसि दन्तस्य दतृ (द्विदन्), SK881 / 5.4.143 स्त्रियां
  संज्ञायाम्, SK882 / 5.4.144 विभाषा श्यावारोकाभ्याम् (optional), SK883 / 5.4.145
  अग्रान्तशुद्ध… (optional).
- **kakud lopa:** SK884 / 5.4.146 ककुदस्यावस्थायां लोपः, SK885 / 5.4.147 त्रिककुत्पर्वते,
  SK886 / 5.4.148 उद्विभ्यां काकुदस्य, SK887 / 5.4.149 पूर्णाद्विभाषा (optional).
- **hṛd nipātana:** SK888 / 5.4.150 सुहृद्दुर्हृदौ (सुहृद्/दुर्हृद्).
- **nipātana:** SK864 / 5.4.125 जम्भा सुहरित…, SK865 / 5.4.126 दक्षिणेर्मा लुब्धयोगे.

Highly lexical; add one stem + one case per rule. May split into parallel worktrees.

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B4); B0 is merged.
Implement the FULL bahuvrīhi samāsānta ĀDEŚA / LOPA / NIPĀTANA set as bahiranga: -1
pre-pass uttara-substitution rules (char-window l/lc/rc or whole-stem replace, like
the tatpuruṣa SK807/6.3.46 महत्→महा rule), plus main-scan phonology where needed. jñu:
SK868/5.4.129 प्रसंभ्यां जानुनोः (प्रज्ञुः), SK869/5.4.130 optional. anaṅ: SK870/5.4.132
धनुषश्च (शार्ङ्गधन्वा), SK871/5.4.133 optional. niṅ: SK872/5.4.134 जायाया निङ् +
SK873/6.1.66 लोपो व्योर्वलि (युवजानिः). gandha→id: SK874/5.4.135, SK875/5.4.136,
SK876/5.4.137 (सुगन्धिः). pāda: SK877/5.4.138 lopa (व्याघ्रपात्), SK878/5.4.139 कुम्भपदी
nipātana +ṅīp, SK879/5.4.140 द्विपात्. danta→dat: SK880/5.4.141 (द्विदन्), SK881/5.4.143,
SK882/5.4.144 & SK883/5.4.145 optional. kakud lopa: SK884/5.4.146, SK885/5.4.147,
SK886/5.4.148, SK887/5.4.149. hṛd: SK888/5.4.150 सुहृद्/दुर्हृद्. nipātana: SK864/5.4.125
जम्भा, SK865/5.4.126 दक्षिणेर्मा. Add one lexical stem + case per rule (check
pratipadika.py for dupes). Big phase — may split into parallel worktrees by ādeśa
family. Cases into test/samasa_list.py + test_samasa_bahuvrihi.py with sweeps; every
label + YAML comment dual-numbered SK-first per §0 (e.g. "B4-prajYuH-SK868-5.4.129").
Full suite green. Update generator_status.md.
```

### Phase B-UI — Vākya Composer + CLI — ✅ DONE (`45f435b`; see §2a)

- **CLI** (`cmd_line.py`): `-B` / `--bahuvrihi` already tags a member; add a
  `--referent-linga` (and reuse `--samasa`) so the exocentric gender is supplied on the
  command line; verify the pre-pass summary prints the `?bahuvrIhi` role tag.
- **UI** (`ui/app.py`, compound grouping ~1209–1460): the `compounds` block carries
  `type` + `surface`; for bahuvrīhi the `surface` is a **gender/vibhakti paradigm**
  driven by the referent — ensure the composer requests and renders it. Add bahuvrīhi
  presets to the gallery. No engine changes.

**Session prompt:**
```
Read sanskrit_parser/generator/bahuvrihi_plan.md (§0 numbering convention, §1–§2, Phase B-UI); B0 is merged.
Extend the CLI + Vākya Composer for bahuvrīhi (NO engine changes). (1) cmd_line.py:
-B/--bahuvrihi already tags the member; add --referent-linga to supply the exocentric
referent gender (with --samasa), and verify the pre-pass summary prints the ?bahuvrIhi
role tag. (2) ui/app.py compound grouping (~1209–1460): the compounds block carries
type+surface — for bahuvrīhi the surface is a REFERENT-DRIVEN gender/vibhakti paradigm;
ensure the composer requests and renders it. Add bahuvrīhi presets to the /karaka
gallery. Smoke: build पीताम्बरः via -k pIta 1 -B ambara --samasa --referent-linga pum,
then a gender sweep. Any new presets/labels reference the sūtra dual-numbered SK-first
per §0. Full suite + gallery green. Update generator_status.md.
```

---

## 4. Test strategy

Follow the tatpuruṣa test pattern (`test/test_samasa_tatpurusha.py` +
`test/samasa_list.py`), three assertion levels per case:
1. **Structure** — pūrva has `?samAsaPurva` + `?upasarjana`; uttara has `?samAsa` +
   `?bahuvrIhi`; the compound gender = **referent** gender (locked, not uttara's).
2. **Fired trace** — the expected pre-pass sūtra ids appear in `karaka_log`.
3. **Surface** — full-pipeline output matches; run a **gender sweep** (masc/fem/neut
   referent) for B0 to prove exocentricity, plus vibhakti sweeps.

New file: `test/test_samasa_bahuvrihi.py`; bahuvrīhi cases appended to
`test/samasa_list.py` (extend the case schema with a `referent_linga` field). Canonical
cases: पीताम्बरः/पीताम्बरा/पीताम्बरम्, प्राप्तोदकः (B0); दीर्घजङ्घः (B1); उपदशाः, सपुत्रः/सहपुत्रः
(B2); बहुयशस्कः/बहुयशाः, व्यूढोरस्कः, केशाकेशि, अप्रजाः (B3); प्रज्ञुः, शार्ङ्गधन्वा, युवजानिः,
व्याघ्रपात्, द्विदन्, सुहृत् (B4).

**Dual numbering in tests (per §0):** every case `label` carries both the SK number and
the Ashtadhyayi id, SK-first (e.g. `"B0-pItAmbaraH-SK830-2.2.24"`,
`"B3-bahuyaSaskaH-SK891-5.4.154"`); the `"fired"` list holds the Ashtadhyayi ids that
`karaka_log` records, and the SK number lives in the label so a reviewer can cross-map.

**How to run** (per `MEMORY.md`):
```bash
cd <worktree>/sanskrit_parser/generator/test
PYTHONPATH=<worktree_root> /Users/karthik/venvs/sanskrit/bin/pytest -n 8 --dist worksteal
```
Quick slice while iterating: `pytest test_samasa_bahuvrihi.py`.

---

## 5. Verification (end-to-end)

1. **Per-phase pytest** — new `test_samasa_bahuvrihi.py` cases green + the full
   generator suite (~8,053 items, ~7.5 min at `-n 8`) with **no avyayībhāva / tatpuruṣa
   / kāraka / strī-block regressions** (the new rules are gated on `?bahuvrIhi` and the
   `?referent_*` tags; the referent-gender lock must not perturb the tatpuruṣa
   `join_objects` "prefer last" path).
2. **CLI smoke** (as-built) — `-k pIta 1 -k ambara 1 --samasa --referent-linga pum` →
   पीताम्बरः (strI → पीताम्बरा, napum → पीताम्बरम्); `-k saha 1 -k putra 1 --samasa
   --referent-linga pum` → सपुत्रः/सहपुत्रः. (The uttara is a `-k … vN` member, not `-B`.)
3. **UI** — `/api/karaka` with `referent_linga` renders the bahuvrīhi `compounds` block
   (`type: bahuvrIhi`); the `karaka.html` referent-liṅga dropdown drives it. Verified via
   the Flask test client; avyayībhāva उपकृष्णम् unregressed.
4. **Status doc** — update `generator/generator_status.md`: add the bahuvrīhi SK rows
   (829–900) to the implemented table, add Skipped rows for the deferred physical
   reorder (2.2.30/35–37) and any priyādi/long-tail gaps, update the Last/Next header
   and Summary counts, and add the new pratipadika/test rows.

---

## 6. Deliverables — ✅ delivered (see §2a for the full as-built account)

- ✅ Bahuvrīhi rule blocks in `sutras_antaranga.yaml` (B0–B4, `bahiranga: -1`).
- ✅ **Anyapadārtha referent-gender** mechanism (the one new mechanism), folded into the
  fused 2.2.24 rule + the composer's `?referent_*` override.
- ✅ **Generalized `_SAMASANTA_AFFIXES` map** (`antaranga_prakriya.py`) so
  `_insert_samasanta` handles all bahuvrīhi affix families (kap/ṣac/ap/ic added; the
  ādeśa families use pre-pass uttara-substitution instead).
- ✅ `test/test_samasa_bahuvrihi.py` (39 cases) + `samasa_bv_tests` in `test/samasa_list.py`.
- ✅ CLI `--referent-linga` (`prepare_bahuvrihi`) + composer API `referent_linga`
  (`_apply_bahuvrihi`) + `karaka.html` referent-liṅga dropdown.
- ✅ `generator_status.md` updates (Implemented rows for every landed sūtra; grouped
  Skipped rows with the precise engine-blocker for each deferral).
- This doc keeps the per-phase **Session prompts** as a historical record; **§2a is the
  authoritative as-built account**.

**Acceptance gate (per §0):** dual SK+Ashtadhyayi numbering, SK-first, is present in
this doc's prose/tables, every `sutras_antaranga.yaml` `# <N>:` block comment, every
`test/samasa_list.py` case `label`, and the `generator_status.md` rows — ✅ upheld.

**Deferred (all recorded in `generator_status.md`, each with its engine blocker — see
§2a for detail):** the ā-stem→i/a-stem samāsānta ādeśas (niṅ 5.4.134, अच् नासिका→नस्
5.4.118–121) need **sup re-insertion after a class-changing substitution** (+ compound
ṇatva for अच्); asic 5.4.122 + the masc बहुयशाः need **6.4.14 dīrgha under the
gender-override**; datṛ 5.4.141 needs the **दतृ न्-declension**; reciprocal ic 5.4.127
needs **reduplication**; ḍac 5.4.73 is **accent-only**; the formation deferrals
(2.2.25/2.2.27/2.2.35–37) + B1 6.3.35/36/39 need the **physical pūrva-nipāta (2.2.30)**
/ affix-context machinery; accent-gated SK 508/509 remain deferred. **None require more
YAML — each is a small, well-scoped engine step.**

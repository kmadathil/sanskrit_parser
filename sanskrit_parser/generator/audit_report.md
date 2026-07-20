# Generator Status Audit Report

## Date: 2026-04-03

## Summary

| Metric | Status Doc Claims | Actual (YAML) | Delta |
|---|---|---|---|
| SK-numbered sutras, implemented | 182 | ~180 | **-2** |
| Implemented sutras without SK number | ~92 | ~92 | ~0 |
| Skipped/deferred sutras | 54 | 54 | 0 |
| Distinct base sutra IDs in YAML | — | 272 | — |

## Discrepancies Found

### 1. SK211 (8.3.57 इण्कोः) — CLAIMED IMPLEMENTED, NOT FOUND IN YAML

- **Status doc:** Listed at line 54 as implemented
- **YAML files:** No rule block with `id: 8.3.57` exists in any of the three YAML files
- **Evidence:** Only referenced in test file comments (`vibhaktis_list.py`) as expected behavior
- **Impact:** The ṇatva-after-iṇ/ku rule (n→ṇ) is claimed as implemented but the sutra itself is missing. Tests referencing this behavior may be passing via other rules (e.g., 8.4.1) or the test expectations may be wrong.
- **Action needed:** Either implement 8.3.57 or clarify that 8.4.1 (रषाभ्यां नो णः समानपदे) handles the ṇatva logic and update the status doc to reflect this.

### 2. Sutra 1.1.26 (ष्णान्ता षट्) — IMPLEMENTED, NOT IN STATUS DOC

- **YAML:** Present in `sutras.yaml`, `sutras_hier.yaml`, `sutra_domains.yaml`
- **Status doc:** Not listed anywhere — neither in implemented nor skipped sections
- **Note:** This is the saṃjñā rule that tags ṣ/n-final numerals as ?zaT. It is functionally important for numeral declension (SK369).
- **Action needed:** Add to implemented sutras table.

### 3. Sutra 8.3.9 (नश्छव्यप्रशान्) — IMPLEMENTED, NOT IN STATUS DOC

- **YAML:** Present in all three YAML files
- **Status doc:** Not listed anywhere
- **Note:** This rule inserts ś after n before ch-group consonants.
- **Action needed:** Add to implemented sutras table or determine if it's covered by SK140 (8.3.7).

### 4. SK364 (6.4.127 अर्वणस्त्रसावनञः) — PARTIAL STATUS

- **Status doc:** Listed as partial (line 358) with note about nañ exception pending
- **YAML:** Implemented in `sutras_antaranga.yaml`
- **Status:** The status doc correctly notes this is partial. No change needed, but the "partial" status should be tracked more explicitly.

### 5. SK434 (8.3.58) — DUPLICATE ENTRY

- **Status doc:** Appears twice — once in the main implemented table (line 202) and once in the skipped table (line 376) with note "Implemented — see SK434 row above"
- **Impact:** Confusing. The skipped table entry should be removed.
- **Action needed:** Remove the duplicate row from the skipped table.

### 6. SK429 (3.2.60) — DEFERRED STATUS MAY BE OUTDATED

- **Status doc:** Listed as deferred (line 7) and in skipped table (line 374) with note "Natural — kañ/kvin falls out of existing infrastructure"
- **Skipped table note:** Says "kaY pratyaya added; tādṛk/tādṛśa compound stems implemented via SK430"
- **Impact:** The skipped table note suggests this is actually working now. The "Deferred" label in the header may be stale.
- **Action needed:** Verify if SK429 is truly working and move to implemented section if so.

### 7. Sutra 1.1.26 (ष्णान्ता षट्) — MISMATCHED SK NUMBER

- **Status doc:** Lists this as SK369 (line 158)
- **Actual:** This sutra is 1.1.26, and SK369 maps to 6.3.91 (आ सर्वनाम्नः)
- **Impact:** The SK number mapping appears incorrect.
- **Action needed:** Verify the correct SK number for 1.1.26.

## Sutras in Status Doc but NOT in YAML (Potentially Missing)

| SK | Sutra ID | Status Doc Description | YAML Status |
|---|---|---|---|
| 211 | 8.3.57 | इण्कोः — n→ṇ after iṇ/ku | **NOT FOUND** |

## Sutras in YAML but NOT in Status Doc (Undocumented)

| Sutra ID | Sutra Name | YAML Files | Notes |
|---|---|---|---|
| 1.1.26 | ष्णान्ता षट् | sutras.yaml, sutras_hier.yaml, sutra_domains.yaml | Important saṃjñā for numerals |
| 8.3.9 | नश्छव्यप्रशान् | sutras.yaml, sutras_hier.yaml, sutra_domains.yaml | n→ś before ch-group |

## Last Implemented Claim

**Status doc claims:** "Last implemented: SK 443 — 8.2.68 अहन्"

**Verification:** 8.2.68 is present in `sutras_antaranga.yaml` (line ~5066). ✓ Correct.

**Status doc also claims:** "SK441 (7.2.109 यः सौ) manually implemented"

**Verification:** 7.2.110 (not 7.2.109) is present. The status doc has a typo — it says 7.2.109 but the sutra name "यः सौ" is actually 7.2.110. ✓ Correct ID, wrong number in text.

**Status doc also claims:** "SK433 (8.2.76 र्वोरुपधायाः दीर्घ इकः)"

**Verification:** 8.2.76 is present in `sutras_antaranga.yaml`. ✓ Correct.

## Recommendations

1. **High Priority:** Investigate SK211 (8.3.57) — either implement it or clarify why it's not needed
2. **Medium Priority:** Add 1.1.26 and 8.3.9 to the implemented sutras table
3. **Medium Priority:** Remove duplicate SK434 entry from skipped table
4. **Low Priority:** Verify SK429 status and update if now working
5. **Low Priority:** Fix typo in "Last implemented" line (7.2.109 → 7.2.110)
6. **Low Priority:** Verify SK number mapping for 1.1.26

## Files Audited

- `sanskrit_parser/generator/generator_status.md`
- `sanskrit_parser/generator/sutras.yaml`
- `sanskrit_parser/generator/sutras_antaranga.yaml`
- `sanskrit_parser/generator/sutras_hier.yaml`
- `sanskrit_parser/generator/sutra_domains.yaml`
- `sanskrit_parser/generator/test/vibhaktis_list.py`
- `sanskrit_parser/generator/pratipadika.py`

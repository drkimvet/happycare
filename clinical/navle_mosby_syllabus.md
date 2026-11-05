# NAVLE and Mosby review (legal sources only)

Neither this map nor Instinct nor Plumb's replaces a veterinary license. 둘 중 하나가 면허를 대신하지는 않습니다.

This is a **study map**, not a book dump. Do not pirate Mosby. Do not fetch Mosby, Elsevier Q-banks, or NAVLE item banks from third-party mirrors. Do not commit a Mosby PDF. Original 가채점 only.

Gene leftovers 285–298 are closed (attending 2026-11-05: 유전자는 그까지 하면 됐고). Do not invent ALDH5A1, CLPX, or packet 299 as another ataxia gene.

## How this resident studies it

1. Pull the public ICVA blueprint (competencies + species weights). Do not reproduce the Species-and-Diagnoses PDF lists.
2. Gate night-critical SA traps from **named public** Merck / AAHA / ACVIM pages into `er_safety_card.md` and `resident_brief.py`.
3. If the attending later ferries a purchased Mosby / board-review PDF, run `python3 clinical/prep_legal_pdfs.py --in ~/Books --out textbooks` on the computer that holds the file. Summarize against a named public source in `source_verification.md`. Never dump a chapter or a Q-bank.
4. Do not ask the attending to hand-split books on a phone.
5. Midtown nights stay dog and cat. Equine / bovine / porcine weights are NAVLE-real; they are **not** new Midtown packets unless she names them.

Legal PDF helper: `clinical/prep_legal_pdfs.py`. Five-Minute title list (Wiley only): `clinical/five_minute_syllabus.md`.

## Public ICVA weights (2026–2027)

Source: [Prepare for the NAVLE](https://www.icva.net/navle/prepare-for-the-navle/) and the linked Candidate Handbook tables. Weights can move after the 2026 practice analysis; re-check the ICVA page, do not freeze a blogger's recap as law.

| Competency domain | Target |
| --- | --- |
| Clinical practice (data gathering + health maintenance) | 70% |
| Preventive medicine and animal welfare | 15% |
| Communication | 8% |
| Professionalism, practice management, wellness | 7% |

| Species | Target |
| --- | --- |
| Canine | 25.6% |
| Feline | 24.3% |
| Equine | 14.7% |
| Bovine | 13.3% |
| Porcine | 5% |
| Other small mammals | 3.3% |
| Ovine / caprine | 3.3% |
| Pet bird | 2.3% |
| Poultry | 2% |
| Non-species specific | 2% |
| Camelid / cervidae | 1.7% |
| Reptiles | 1.5% |
| Aquatics | 1% |

Dogs and cats are about half the paper. That is why this run starts SA endocrine, not another cerebellar gene.

## SA domain order (this run)

Closed gene chain is not on this list.

| Next | Domain | Public source, not a Mosby dump | Status |
| --- | --- | --- | --- |
| 299 | Canine hypothyroidism (not T4-alone) | Heseltine, Merck *Hypothyroidism in Animals*, May 2024 / May 2025 | This packet |
| 300 | Canine hyperadrenocorticism diagnosis traps (not the TBI Cushing reflex) | Merck HAC; do not harvest a UCCR / LDDST table | Next |
| 301 | Feline hyperthyroidism (full diagnostic gate; azotemia/amlodipine already exists) | Merck hyperthyroidism | After 300 |
| 302 | FeLV / FIV | Merck / AAHA retrovirus | After 301 |
| 303 | AAHA vaccination / core vs non-core | AAHA canine and feline vaccine guidelines | After 302 |

Already gated (do not reopen as if new): Addison, DKA / HHS, hypoglycemia, IMHA, leptospirosis, heartworm / caval, facial CN VII, and the 285–298 gene leftovers.

## What Mosby is for, legally

Mosby's review is a **purchased** Q-style drill, not a night law and not a repo file. When a legal split exists, use it to find which public-source trap to gate next. Do not copy stems, answer keys, or chapter text.

If no legal PDF is on disk, keep studying from ICVA + Merck / AAHA / ACVIM. That is enough to start.

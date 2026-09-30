# Veterinary AI landscape (19 Sep 2026)

Public marketing and product pages only. No product logins. Neither this resident nor any product below replaces a veterinary license. 둘 중 하나가 면허를 대신하지는 않습니다. Dr. Kim does not open Instinct; the resident researches, the attending decides.

## Who actually competes with a night-shift resident

| Product | Job | Corpus / dose rule | Beats us on | Loses to us on |
| --- | --- | --- | --- | --- |
| **Instinct Attending** | Clinical decision support | Closed: Plumb's + Standards of Care (ex-Plumb's Pro) + Clinician's Brief. Doses **retrieved** from Plumb's, not generated. Inline citations. No open web. Research preview for verified DVMs (US/CA/AU/NZ). | Licensed formulary lookup; interaction-adjacent safety; one-tap source inspect | No this-attending standing orders; no shift continuity; will not refuse a bad plan that is "on label" in Plumb; cannot flag a 2013 book error against 2024 guidelines; not a teacher; not Midtown-compact |
| **Plumb's / Standards** | Formulary + CDS articles | Licensed monographs, veterinary interaction checker, specialist-updated Standards | The actual mg/kg and interactions | Not a reasoner. Will not localize "soft belly + UOP 1 + right renomegaly" to the right kidney/ureter |
| **ScribbleVet** (Instinct, Jan 2026) | Ambient scribe | Note capture; Plumb lookup inside the SOAP | Charting speed, dental charts, PIMS transfer | Wrong job. A scribe is not a differential |
| **OpenVet** | "AI hospital" / species-aware CDS | Claims cited, species-aware, longitudinal record; "deterministic" dosing without naming Plumb; marketing confidence percents on demo cards | Record-plus-question framing; exotic/wildlife species list | Unlicensed formulary risk; confidence theater; PHI/longitudinal-data play; no hospital-specific don'ts |
| **VetRec DAVID** | Scribe + "clinical assistant" | SOAP, recap, phone; enterprise Ethos/Bond | Multi-site note ops | Assistant answers are not a closed Plumb corpus |
| **Digitail Tails** | PIMS-native ops AI | SOAP, intake, voice-to-invoice, some "diagnosis/treatment" help | Digitail workflow | Charge capture ≠ localization |
| **CoVet / Scribenote / Talkatoo / HappyDoc** | Scribes | Notes, sometimes offline | Documentation | Not CDS |
| **VetGPT / DVM Scribe** | Scribe + optional "specialists" | Visit → SOAP; consumer VetGPT also markets 64+ species photo/text | Exotics breadth (consumer) | Verify-yourself product; not attending-grade |
| **Petriage / Omelo / Petio** | Owner triage | Urgency score / pathways | Client-side sorting | Not for a DVM at 02:00 |

Sources: instinct.vet/products/attending, instinct.vet/blog/ai-vet-tool-attending-instinct, globenewswire 10 Sep 2026 Instinct release, instinct.vet/products/standards, openvet.ai, digitail.com/tails-ai, vetrec.io, vetgpt.com.

## Honest moat map

Instinct's real moat is **license + retrieval**. We will not out-Plumb Plumb. Claiming we can generate a safer monograph is how OpenVet-style tools get people hurt.

The winnable axis is **judgment under this attending**:

1. Species and disease gates before any number.
2. Refuse the dose when the corpus is silent (`△ confirm in Plumb`).
3. Separate "the drug is in Plumb" from "this patient should get that drug tonight."
4. Continuity: azotemic cat ≠ DexSP/NSAID; do not drain a soft abdomen without fluid:serum Cr/K; do not add a cefazolin CRI as theater.
5. Outdated-vs-guideline: Plunkett 2013 vs AAHA fluids 2024 / IRIS AKI / RECOVER; Zn3P2 gas is phosphine (PH3), not phosgene.
6. Decompressible disease gets a referral/consent sentence, not a watch-and-hope sentence.
7. Compact bilingual night answers. No PHI in git.

## What was implemented here

- `.cursor/skills/midtown-attending/SKILL.md` — resident rules that fire on live cases.
- `clinical/er_safety_card.md` — public-source hard stops, no Plumb text.
- `clinical/resident_brief.py` — machine-checkable gates so a one-liner cannot skip species, NAC-family mix, or abdomen-drain rules.
- `clinical/tests/` — invariants so the card cannot silently lose a hard stop.

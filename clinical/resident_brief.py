#!/usr/bin/env python3
"""Species-first resident brief. No invented doses. Not a formulary."""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable

LICENSE_LINE = (
    "Neither this resident nor Instinct Attending nor Plumb's replaces a veterinary license."
)
DOSE_POLICY = "△ confirm every mg/kg in Plumb or the hospital protocol. Do not invent a number."

LILY_RE = re.compile(r"\b(lilium|hemerocallis|easter lily|tiger lily|daylily|day lily|true lily|lily)\b", re.I)
XYLITOL_RE = re.compile(r"\bxylitol\b", re.I)
APAP_RE = re.compile(r"\b(acetaminophen|paracetamol|tylenol|apap)\b", re.I)
SAGO_RE = re.compile(r"\b(sago|cycad|cycas)\b", re.I)
PHOSPHIDE_RE = re.compile(r"\b(zinc phosphide|zn3p2|zn₃p₂|phosphide)\b", re.I)
PHOSGENE_RE = re.compile(r"\bphosgene\b", re.I)
NAC_RE = re.compile(r"\b(nac|n-acetylcysteine|acetylcysteine)\b", re.I)
BETA_LACTAM_RE = re.compile(
    r"\b(amoxicillin|ampicillin|amoxi|clavamox|cefalexin|cephalexin|penicillin|beta-?lactam)\b",
    re.I,
)
NSAID_RE = re.compile(r"\b(nsaid|meloxicam|carprofen|robenacoxib|onsior|rimadyl|metacam|deracoxib)\b", re.I)
DEX_RE = re.compile(r"\b(dexsp|dexamethasone|dexamethasone sp|azium)\b", re.I)
CEFAZOLIN_CRI_RE = re.compile(r"\bcefazolin\b.*\bcri\b|\bcri\b.*\bcefazolin\b", re.I)
DRAIN_RE = re.compile(r"\b(drain (the )?abdomen|abdominocentesis|peritoneal drain|tap the belly)\b", re.I)
AZOTEMIA_RE = re.compile(r"\b(aki|azotem|creatinine|iris|hydroneph|pyoneph|ureter)\b", re.I)
RENOMEGALY_RE = re.compile(r"\b(renomegal|enlarged kidney|big kidney|fluid-filled kidney)\b", re.I)
SOFT_ABD_RE = re.compile(r"\b(soft abdomen|no tension|non-tense|abdomen soft)\b", re.I)
UOP_RE = re.compile(r"\buop\b|urine output|oligur|anur", re.I)
BLOCKED_RE = re.compile(r"\b(straining|blocked|urethral obstruct|flc|unable to urinate)\b", re.I)
RODENTICIDE_RE = re.compile(r"\b(rodenticide|bromethalin|cholecalciferol|brodifacoum|bromadiolone|warfarin)\b", re.I)
GRAPE_RE = re.compile(r"\b(grapes?|raisins?|tamarinds?|zante currants?)\b", re.I)
EG_RE = re.compile(r"\b(ethylene glycol|antifreeze)\b", re.I)
PERMETHRIN_RE = re.compile(r"\bpermethrin\b", re.I)
CHOCOLATE_RE = re.compile(r"\b(chocolate|theobromine|methylxanthine)\b", re.I)
LINEAR_RE = re.compile(r"\b(linear (foreign )?body|string under (the )?tongue|dental floss|\byarn\b)\b", re.I)
YANK_STRING_RE = re.compile(r"\b(yank|pull|tug)\b.{0,20}\b(string|floss|yarn)\b", re.I)
GDV_RE = re.compile(r"\b(gdv|gastric dilatation|gastric dilation|gastric volvulus)\b", re.I)
PYO_RE = re.compile(r"\bpyometra\b", re.I)
FATE_RE = re.compile(r"\b(fate|saddle thrombus|aortic thrombo|arterial thromboembolism)\b", re.I)
HEAT_RE = re.compile(r"\b(heatstroke|heat stroke)\b", re.I)
ICE_RE = re.compile(r"\b(ice bath|ice-water|ice water)\b", re.I)
STASIS_RE = re.compile(r"\b(gi stasis|gut stasis|ileus)\b", re.I)
PROKINETIC_RE = re.compile(r"\b(metoclopramide|cisapride|prokinetic|syringe-?feed)\b", re.I)
IONOPHORE_RE = re.compile(r"\b(ionophore|monensin|lasalocid|salinomycin)\b", re.I)
ACE_RE = re.compile(r"\bacepromazine\b", re.I)
STORM_RE = re.compile(r"\b(thunderstorm|storm phobia|noise phobia|separation anxiety)\b", re.I)
ATROPINE_RE = re.compile(r"\batropine\b", re.I)
VIT_C_RE = re.compile(r"\b(anorex|not eating|inappeten)\b", re.I)

HINDGUT = {"hamster", "guinea pig", "rabbit", "chinchilla"}
SA = {"dog", "cat", "canine", "feline", "puppy", "kitten"}


def _norm_species(species: str | None) -> str:
    if not species:
        return ""
    s = species.strip().lower()
    aliases = {
        "canine": "dog",
        "feline": "cat",
        "puppy": "dog",
        "kitten": "cat",
        "gp": "guinea pig",
        "cavy": "guinea pig",
        "lagomorph": "rabbit",
        "ferret": "ferret",
        "bird": "bird",
        "avian": "bird",
        "horse": "horse",
        "equine": "horse",
        "bovine": "cattle",
    }
    return aliases.get(s, s)


def _blob(parts: Iterable[str | None]) -> str:
    return " ".join(p for p in parts if p)


def analyze(
    species: str | None,
    problem: str,
    meds_offered: str | None = None,
    uop_ml_per_kg_hr: float | None = None,
    abdomen: str | None = None,
) -> dict:
    """Return a machine-checkable brief. Never includes a mg/kg dose."""
    spec = _norm_species(species)
    text = _blob([problem, meds_offered, abdomen])
    hard_stops: list[str] = []
    do_not: list[str] = []
    do_next: list[str] = []
    localization = ""
    sources: list[str] = []
    nac_family = None

    if not spec:
        hard_stops.append("No species on the one-liner: no dose, no CRI, no typical fluid rate.")
        do_next.append("Ask species, weight, and the one problem that brought them in.")
        return _pack(spec, hard_stops, do_not, do_next, localization, sources, nac_family)

    if spec == "cat" and LILY_RE.search(text):
        hard_stops.append("Cat + true lily / pollen / vase water: treat as AKI emergency.")
        do_not.append("Do not wait for 'just GI' or treat it as a dog plant.")
        do_next.append("Decontamination if recent and safe; start IVF; baseline and serial creatinine/UOP.")
        localization = "Lily toxicosis localizes to feline AKI, not a primary GI plant."
        sources.append("Cornell CVM public toxin list; ASPCA APCC lily guidance")
        nac_family = None

    if XYLITOL_RE.search(text):
        if spec == "dog":
            hard_stops.append("Dog + xylitol: check glucose now. Charcoal does not bind xylitol (Merck).")
            do_not.append("Do not write charcoal as the decontamination plan.")
            do_not.append("Do not mix a xylitol NAC schedule into the APAP NAC family.")
            do_next.append("Glucose now and serially; dextrose if indicated; liver panel later. △ NAC in Plumb if used.")
            localization = localization or "Xylitol: canine hypoglycemia first, hepatic injury second."
            sources.append("Merck Veterinary Manual: Xylitol toxicosis in dogs")
            nac_family = "xylitol-consider"
        elif spec == "cat":
            do_not.append("Do not import canine xylitol hypoglycemia as the feline leading problem.")
            sources.append("Merck: cats are not the published xylitol hypoglycemia/liver species")

    if APAP_RE.search(text):
        if spec in {"cat", "ferret"}:
            hard_stops.append("Acetaminophen is contraindicated in cats (and ferrets) at analgesic intent (Cornell).")
            nac_family = "acetaminophen"
            do_not.append("Do not invent a hybrid NAC (APAP load + xylitol interval + liver-failure tail).")
            do_next.append("Name the APAP NAC family only; △ current Plumb/hospital load and maintenance.")
            sources.append("Cornell CVM public toxin list; ASPCA/VECCS APAP NAC historical family")
        elif spec == "dog":
            nac_family = "acetaminophen"
            do_not.append("Do not mix APAP NAC with xylitol or generic hepatic-failure schedules.")
            sources.append("ASPCA/VECCS historical APAP NAC family; △ Plumb")

    if SAGO_RE.search(text):
        hard_stops.append("Sago/cycad: entire plant toxic; hepatic; no specific antidote (ASPCA APCC).")
        do_not.append("Do not treat as a mild GI landscaping plant.")
        if nac_family and nac_family != "hepatic-failure":
            hard_stops.append("NAC family conflict: do not blend sago/hepatic-failure NAC with APAP or xylitol.")
        else:
            nac_family = "hepatic-failure"
        sources.append("ASPCA APCC sago palm public alert")

    if PHOSPHIDE_RE.search(text) or PHOSGENE_RE.search(text):
        hard_stops.append("Zinc phosphide → phosphine (PH3), not phosgene. Protect staff from the gas.")
        do_not.append("Do not induce emesis in a way that aerosols PH3 into faces.")
        sources.append("Chemistry of Zn3P2; ignore 2013 book 'phosgene' wording")

    if spec in HINDGUT and BETA_LACTAM_RE.search(text):
        hard_stops.append(f"{spec}: oral beta-lactam is a hindgut-dysbiosis hard stop (Merck exotic GI).")
        do_not.append("Do not write oral amoxicillin/ampicillin/cephalexin for hamster, guinea pig, or rabbit.")
        sources.append("Merck Veterinary Manual exotic/hindgut antimicrobial warnings")

    if spec == "cat" and BLOCKED_RE.search(text) and "male" in text.lower():
        hard_stops.append("Male cat + straining: urethral obstruction until proven otherwise.")
        do_not.append("Do not discharge as constipation.")

    azotemic = spec == "cat" and AZOTEMIA_RE.search(text)
    if azotemic and NSAID_RE.search(text):
        hard_stops.append("Azotemic cat: hold the NSAID.")
        do_not.append("Do not give 'just one dose' of meloxicam/robenacoxib/carprofen.")
        sources.append("IRIS AKI / NSAID renal-risk framing")
    if azotemic and DEX_RE.search(text):
        hard_stops.append("Azotemic cat: DexSP is not the plan.")
        do_not.append("Do not use dexamethasone as AKI treatment or as a substitute for localization.")

    if CEFAZOLIN_CRI_RE.search(text):
        hard_stops.append("Cefazolin CRI is not a default because the patient is sick.")
        do_not.append("Do not invent a cefazolin CRI from Gonzalez 2017 periop extra-label use.")
        sources.append("Gonzalez 2017 periop cefazolin extra-label (not a night CRI)")

    if DRAIN_RE.search(text) and "fluid:serum" not in text.lower() and "fluid-serum" not in text.lower():
        hard_stops.append("Do not drain a free abdomen without paired fluid and serum creatinine and potassium.")
        do_next.append("If fluid is present, pair fluid:serum Cr and K before any therapeutic tap story.")

    if spec == "cat" and (RENOMEGALY_RE.search(text) or AZOTEMIA_RE.search(text)):
        if SOFT_ABD_RE.search(text) or (abdomen and "soft" in abdomen.lower()):
            localization = (
                "Unilateral renomegaly + soft abdomen localizes to that kidney/ureter "
                "(hydro/pyo/obstruction), not uroabdomen, until fluid:serum Cr/K says otherwise."
            )
            do_not.append("Do not treat a soft, non-tense belly as a drainable uroabdomen.")
            do_next.append("Name the side. Offer referral/decompression/euthanasia, not 'watch the belly.'")
            sources.append("IRIS AKI; attending exam rule: UOP by weight, not pad wetness")

    if uop_ml_per_kg_hr is not None:
        if uop_ml_per_kg_hr >= 1.0:
            do_not.append(
                f"UOP {uop_ml_per_kg_hr:g} mL/kg/hr is not oliguria. Do not treat as anuric."
            )
        do_next.append("UOP is mL/kg/hr from closed collection or weighed litter, not a wet pad.")
        sources.append("IRIS AKI grading uses creatinine and quantified UOP")

    if UOP_RE.search(text) and uop_ml_per_kg_hr is None:
        do_next.append("Quantify UOP in mL/kg/hr. Pad wet ≠ urine output.")

    if RODENTICIDE_RE.search(text):
        do_not.append("Do not give vitamin K1 for an unknown block or for bromethalin/cholecalciferol/PH3.")
        do_next.append("Identify the family: anticoagulant vs bromethalin vs cholecalciferol vs phosphide.")
        sources.append("Four rodenticide families; vitamin K1 is not universal")

    if spec == "dog" and GRAPE_RE.search(text):
        hard_stops.append("Dog + grape/raisin/tamarind: treat as AKI risk (Merck).")
        do_not.append("Do not wait for 'just GI' or invent a grape toxic dose.")
        do_next.append("Decontaminate if recent and safe; IVF; serial creatinine. Ribes currants are not Vitis.")
        localization = localization or "Vitis/tamarind toxicosis localizes to canine AKI."
        sources.append("Merck: grape, raisin, and tamarind toxicosis in dogs")

    if EG_RE.search(text):
        hard_stops.append("Ethylene glycol: start fomepizole or ethanol early. Do not wait for crystals.")
        do_not.append("Do not defer known antifreeze exposure to a morning creatinine recheck.")
        sources.append("Merck: ethylene glycol toxicosis in animals")

    if spec == "cat" and PERMETHRIN_RE.search(text):
        hard_stops.append("Cat + permethrin (often a dog spot-on): tremors/seizures. Bath the product off.")
        do_not.append("Do not treat permethrin as organophosphate. Atropine is not the plan.")
        do_next.append("Methocarbamol is the tremor conversation; △ Plumb for the number.")
        sources.append("Published feline permethrin series; dvm360 cat-hazard review")
        if ATROPINE_RE.search(text):
            hard_stops.append("Atropine is not indicated for pyrethroid/permethrin tremors.")

    if CHOCOLATE_RE.search(text):
        do_not.append("Do not quote a memorized theobromine mg/kg as if it were Plumb.")
        do_next.append("Identify the product and calculate methylxanthine; then △ Plumb/ASPCA.")
        sources.append("Merck: chocolate toxicosis in animals")

    if spec in {"cat", "dog"} and (LINEAR_RE.search(text) or YANK_STRING_RE.search(text)):
        hard_stops.append("Linear foreign body: do not yank the visible string.")
        do_not.append("Do not pull string anchored under the tongue; Merck: sawing perforation risk.")
        do_next.append("Examine the tongue base. Imaging. Surgery conversation if anchored.")
        sources.append("Merck: gastrointestinal obstruction in small animals")

    if spec == "dog" and GDV_RE.search(text):
        hard_stops.append("GDV: stabilize, decompress, surgery. Not an observe-overnight disease.")
        do_not.append("Do not induce emesis for GDV.")
        sources.append("Merck/MSD: gastric dilation and volvulus in small animals")

    if PYO_RE.search(text):
        hard_stops.append("Pyometra: stabilize, then ovariohysterectomy unless a documented medical-breed plan.")
        do_not.append("Do not send a diestrus sick intact female home as a simple UTI.")
        sources.append("Merck: CEH–pyometra complex in small animals")

    if spec == "cat" and FATE_RE.search(text):
        hard_stops.append("Feline ATE: analgesia first. Cold, pulseless, painful hind limbs.")
        do_not.append("Do not promise thrombolysis as the night plan.")
        do_next.append("Confirm pulses/Doppler, echo when stable, clopidogrel conversation △ Plumb (FAT CAT).")
        sources.append("Merck: arterial thromboembolism in dogs and cats")

    if HEAT_RE.search(text):
        do_not.append("Do not use ice-water immersion as the default heatstroke cool.")
        do_next.append("Tepid water + airflow. Stop cooling when temperature is falling. Hospital stop-number.")
        sources.append("Public heatstroke cooling teaching; hospital protocol for the stop temperature")
        if ICE_RE.search(text):
            hard_stops.append("Ice-water immersion is not the default heatstroke cool.")

    if spec == "rabbit" and (STASIS_RE.search(text) or VIT_C_RE.search(text) or "feces" in text.lower()):
        hard_stops.append("Rabbit GI: distinguish stasis from obstruction before prokinetic or syringe-feeding.")
        do_not.append("Do not start metoclopramide/cisapride until obstruction is off the table.")
        do_next.append("Pain control and fluids first. Imaging if obstruction is in play (Merck / Illinois).")
        sources.append("Merck rabbit digestive disorders; Illinois rabbit GI stasis")
        if PROKINETIC_RE.search(text):
            hard_stops.append("Prokinetic/syringe-feed named before obstruction excluded: hold it.")

    if spec == "guinea pig" and VIT_C_RE.search(text):
        hard_stops.append("Anorexic guinea pig: vitamin C is obligate. This is not a dog ileus.")
        sources.append("Public exotic nutrition: Cavia requires dietary ascorbate")

    if spec == "horse" and IONOPHORE_RE.search(text):
        hard_stops.append("Horse + ionophore: cardiotoxic emergency. No specific antidote.")
        do_not.append("Do not treat ionophore as a simple gas-colic drip.")
        sources.append("Merck equine ionophore / feed contamination teaching")

    if ACE_RE.search(text) and STORM_RE.search(text):
        hard_stops.append("Acepromazine is not an anxiolytic for storm or separation distress.")
        do_not.append("Do not send acepromazine as the behavior plan.")
        sources.append("Public behavior positions: acepromazine is sedative, not anxiolytic")

    if NAC_RE.search(text) and nac_family is None:
        hard_stops.append("NAC named without an indication family: do not write it.")
        do_next.append("Pick APAP, xylitol-consider, or hepatic-failure. Then △ Plumb.")

    if not localization:
        localization = "Localize the problem list before choosing a drug from Plumb."

    if spec in SA or spec in HINDGUT or spec in {"horse", "cattle", "bird", "ferret"}:
        do_next.append("If a number is required, open Plumb or the hospital protocol. Do not generate mg/kg here.")

    # Deduplicate while preserving order
    hard_stops = list(dict.fromkeys(hard_stops))
    do_not = list(dict.fromkeys(do_not))
    do_next = list(dict.fromkeys(do_next))
    sources = list(dict.fromkeys(sources))
    return _pack(spec, hard_stops, do_not, do_next, localization, sources, nac_family)


def _pack(spec, hard_stops, do_not, do_next, localization, sources, nac_family) -> dict:
    return {
        "license": LICENSE_LINE,
        "role": "resident",
        "species": spec or None,
        "hard_stops": hard_stops,
        "localization": localization,
        "do_not": do_not,
        "do_next": do_next,
        "dose_policy": DOSE_POLICY,
        "nac_family": nac_family,
        "sources": sources,
        "mg_per_kg": None,
    }


def render(brief: dict) -> str:
    lines = [
        brief["license"],
        f"Role: {brief['role']} | Species: {brief['species'] or 'UNKNOWN'}",
        f"Gate: {brief['hard_stops'][0] if brief['hard_stops'] else 'no hard stop'}",
        f"Localization: {brief['localization']}",
        "Do not:",
    ]
    lines.extend(f"  - {x}" for x in (brief["do_not"] or ["(none)"]))
    lines.append("Do next:")
    lines.extend(f"  - {x}" for x in (brief["do_next"] or ["(none)"]))
    lines.append(f"Dose: {brief['dose_policy']}")
    if brief["nac_family"]:
        lines.append(f"NAC family: {brief['nac_family']} (do not mix)")
    if brief["sources"]:
        lines.append("Sources: " + "; ".join(brief["sources"]))
    assert brief["mg_per_kg"] is None
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Midtown resident brief. No invented doses.")
    p.add_argument("--species", default="")
    p.add_argument("--problem", required=True)
    p.add_argument("--meds", default="")
    p.add_argument("--uop", type=float, default=None, help="UOP in mL/kg/hr if known")
    p.add_argument("--abdomen", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    brief = analyze(args.species, args.problem, args.meds, args.uop, args.abdomen)
    if args.json:
        print(json.dumps(brief, indent=2))
    else:
        print(render(brief))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

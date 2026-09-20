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
PEACE_LILY_RE = re.compile(r"\b(peace lily|calla lily|spathiphyllum|zantedeschia)\b", re.I)
VALLEY_LILY_RE = re.compile(r"\b(lily-of-the-valley|lily of the valley|convallaria)\b", re.I)
HOPS_RE = re.compile(r"\b(hops|humulus)\b", re.I)
ALLIUM_RE = re.compile(r"\b(onion|garlic|chive|leek|allium)\b", re.I)
MACADAMIA_RE = re.compile(r"\bmacadamia\b", re.I)
TARTAR_RE = re.compile(r"\b(cream of tartar|tartaric)\b", re.I)
IVERMECTIN_RE = re.compile(r"\b(ivermectin|milbemycin|moxidectin|avermectin)\b", re.I)
CHELONIAN_RE = re.compile(r"\b(turtle|tortoise|chelonian|box turtle)\b", re.I)
MDR1_RE = re.compile(r"\b(mdr1|abcb1|collie|australian shepherd|sheltie|shetland|old english sheepdog)\b", re.I)
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
TENSE_ABD_RE = re.compile(
    r"\b(tense|tight|painful|guarded)\b.{0,28}\babdomen\b|\b(cranial|upper)\b.{0,20}\babdomen\b",
    re.I,
)
PANC_RE = re.compile(r"\bpancreat|\bfpl\b|\bspec fpl\b|\bsnap fpl\b|\bfpli\b|\btriaditis\b", re.I)
FPL_SNAP_WEAK_RE = re.compile(
    r"\b(?:snap\s*fpl|fpl\s*snap|spec\s*fpl|fpli)\b.{0,48}\b(?:weak|equivocal|faint|light)\b|"
    r"\b(?:weak|equivocal|faint|light).{0,48}\b(?:snap\s*fpl|fpl\s*snap|spec\s*fpl|fpli|\bfpl\b)\b",
    re.I,
)
OPIOID_RE = re.compile(
    r"\b(opioid|opiate|buprenorphine|methadone|fentanyl|hydromorphone|morphine|butorphanol)\b",
    re.I,
)
VOLUME_CC_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:cc|mL)\b", re.I)
SUCRALFATE_RE = re.compile(r"\bsucralfate\b", re.I)
DAYS_ABD_RE = re.compile(r"\b(few days|for days|days of|several days|\d+\s*days?)\b", re.I)
LOWFAT_RE = re.compile(r"\b(low[ -]?fat|fat[ -]?restrict|low fat diet)\b", re.I)
FIBER_RE = re.compile(r"\b(high[ -]?fib(?:er|re)|fibre|fiber)\b", re.I)
UOP_RE = re.compile(r"\buop\b|urine output|oligur|anur", re.I)
BLOCKED_RE = re.compile(r"\b(straining|blocked|urethral obstruct|flc|unable to urinate|not peeing)\b", re.I)
UROABD_RE = re.compile(r"\b(uroabdomen|urine in (the )?abdomen|ruptured bladder|bladder rupture)\b", re.I)
RODENTICIDE_RE = re.compile(r"\b(rodenticide|bromethalin|cholecalciferol|brodifacoum|bromadiolone|warfarin)\b", re.I)
GRAPE_RE = re.compile(r"\b(grapes?|raisins?|tamarinds?|zante currants?)\b", re.I)
EG_RE = re.compile(r"\b(ethylene glycol|antifreeze)\b", re.I)
PERMETHRIN_RE = re.compile(r"\bpermethrin\b", re.I)
CHOCOLATE_RE = re.compile(r"\b(chocolate|theobromine|methylxanthine)\b", re.I)
LINEAR_RE = re.compile(r"\b(linear (foreign )?body|string under (the )?tongue|dental floss|\byarn\b)\b", re.I)
YANK_STRING_RE = re.compile(r"\b(yank|pull|tug)\b.{0,20}\b(string|floss|yarn|vinyl|vynyl|plastic)\b", re.I)
VINYL_RE = re.compile(
    r"\b(viny+l|vynyl|plastic wrap|plastic wrapper|cling wrap|saran|packaging)\b",
    re.I,
)
JERKY_RE = re.compile(r"\b(jerky|beef stick|meat stick)\b", re.I)
SIBLING_RE = re.compile(
    r"\b(sibling|littermate|housemate|same household|both cats|two cats|the other cat|"
    r"copy (the )?(discharge|template)|same (discharge|template))\b",
    re.I,
)
THRESHOLD_RE = re.compile(
    r"\b(toxic threshold|below.{0,24}threshold|typical toxic)\b",
    re.I,
)
NPO12_RE = re.compile(
    r"\b(npo|withhold food|fast(?:ing)?).{0,28}(12|twelve)\s*h"
    r"|\b(12|twelve)\s*hours?.{0,28}(npo|withhold|no food|fast)",
    re.I,
)
GDV_RE = re.compile(r"\b(gdv|gastric dilatation|gastric dilation|gastric volvulus)\b", re.I)
PYO_RE = re.compile(r"\bpyometra\b", re.I)
FATE_RE = re.compile(r"\b(fate|saddle thrombus|aortic thrombo|arterial thromboembolism)\b", re.I)
HEAT_RE = re.compile(r"\b(heatstroke|heat stroke)\b", re.I)
ICE_RE = re.compile(r"\b(ice bath|ice-water|ice water)\b", re.I)
STASIS_RE = re.compile(r"\b(gi stasis|gut stasis|ileus)\b", re.I)
PROKINETIC_RE = re.compile(r"\b(metoclopramide|cisapride|prokinetic|syringe-?feed)\b", re.I)
IONOPHORE_RE = re.compile(r"\b(ionophore|monensin|lasalocid|salinomycin)\b", re.I)
NEPHROSPLENIC_RE = re.compile(r"\b(nephrosplenic|renosplenic|left dorsal displacement)\b", re.I)
LCV_RE = re.compile(r"\b(large colon volvulus|colonic volvulus|colon torsion)\b", re.I)
PHENYLEPHRINE_RE = re.compile(r"\bphenylephrine\b", re.I)
BUTAZONE_RE = re.compile(r"\b(phenylbutazone|bute|right dorsal colitis)\b", re.I)
BACTERIURIA_RE = re.compile(r"\b(subclinical bacteriuria|asymptomatic bacteriuria|bacteria on culture|culture positive)\b", re.I)
UTI_RE = re.compile(r"\b(uti|cystitis|pollakiuria|stranguria|flutd|convenia|enrofloxacin|baytril|14.?day)\b", re.I)
FQ_RE = re.compile(r"\b(enrofloxacin|marbofloxacin|orbifloxacin|pradofloxacin|ciprofloxacin|baytril|fluoroquinolone)\b", re.I)
CPR_RE = re.compile(r"\b(cpr|cpa|arrest|asystole|pea|recover)\b", re.I)
ANAPHYLAXIS_RE = re.compile(
    r"\banaphylax|\banaphyla|\ballergic shock\b|\bvaccine reaction\b|\bhymenoptera\b|"
    r"\bbee sting|\bwasp sting|\bhornet sting|\byellow jacket\b|\bangioedema\b|"
    r"\burticaria\b|\bhives\b|\bfacial swelling\b|"
    r"\bgallbladder (halo|wall edema)\b|\bgbwe\b",
    re.I,
)
DIPHEN_RE = re.compile(r"\b(diphenhydramine|benadryl)\b", re.I)
HIGH_DOSE_EPI_RE = re.compile(r"\b(high-?dose (epi|epinephrine)|0\.1\s*mg/kg\s*(epi|epinephrine))\b", re.I)
DKA_RE = re.compile(r"\b(dka|ketoacid|diabetic keto)", re.I)
SEIZURE_RE = re.compile(r"\b(seizure|status epileptic|cluster seizure|ictal|postictal)", re.I)
DIAZEPAM_PO_RE = re.compile(r"\b(oral diazepam|diazepam po|diazepam p\.o\.|send home diazepam|diazepam home)", re.I)
PENTOBARB_RE = re.compile(r"\bpentobarbital\b", re.I)
THIRTY_MIN_SE_RE = re.compile(r"\b(30|thirty)[ -]?min", re.I)
HHS_RE = re.compile(r"\b(hhs|honk|hyperosmolar|nonketotic)\b", re.I)
BICARB_RE = re.compile(r"\b(bicarbonate|nahco3|sodium bicarb)\b", re.I)
HYPOK_RE = re.compile(r"\b(hypokal|low potassium|k\s*[<=]\s*[123])", re.I)
ADDISON_RE = re.compile(r"\b(addison|hypoadren|acth stim|cosyntropin|docp|fludrocortisone)", re.I)
HYPERK_RE = re.compile(r"\b(hyperkalem|high potassium|k\s*[>=]\s*[6-9])", re.I)
HYPONA_RE = re.compile(r"\b(hyponatrem|low sodium)", re.I)
BRADY_SHOCK_RE = re.compile(r"\b(brady|slow heart|relative brady)", re.I)
PRED_ASSAY_RE = re.compile(r"\b(predniso|hydrocortisone)", re.I)
LDA_RE = re.compile(r"\b(lda|left displaced abomasum|displaced abomasum|rda|right displaced abomasum|abomasal volvulus|\bping\b)\b", re.I)
COLITIS_RE = re.compile(
    r"\b(colitis|salmonell|potomac|phf|neorickettsia|endotox|acute diarrhea|profuse diarrhea)\b",
    re.I,
)
POLYMYXIN_RE = re.compile(r"\bpolymyxin\b", re.I)
FLUNIXIN_RE = re.compile(r"\b(flunixin|banamine|anti-?endotoxin)\b", re.I)
SHOTGUN_ABX_RE = re.compile(
    r"\b(shotgun|start (iv )?(antibiotics?|abx)|penicillin.{0,40}gentamicin|gentamicin.{0,40}metronidazole|ceftiofur.{0,20}metro)\b",
    re.I,
)
PHF_STORY_RE = re.compile(r"\b(phf|potomac|neorickettsia|oxytetracycline|oxytet)\b", re.I)
ACE_RE = re.compile(r"\bacepromazine\b", re.I)
STORM_RE = re.compile(r"\b(thunderstorm|storm phobia|noise phobia|separation anxiety)\b", re.I)
ATROPINE_RE = re.compile(r"\batropine\b", re.I)
VIT_C_RE = re.compile(r"\b(anorex|not eating|inappeten)\b", re.I)
CHF_RE = re.compile(r"\b(chf|cardiogenic|congestive heart|pulmonary edema|left-sided heart)\b", re.I)
HYPOVOLEM_RE = re.compile(r"\bhypovolem|\bhemorrhagic shock\b", re.I)
HEMOABD_RE = re.compile(
    r"\b(hemoabdomen|haemoabdomen|hemoperitoneum|haemoperitoneum)\b",
    re.I,
)
SHOCK_BOLUS_RE = re.compile(r"\b(shock bolus|shock dose|fluid bolus)\b", re.I)
KCL_BOLUS_RE = re.compile(r"\b(kcl|potassium chloride).{0,24}\bbolus\b|\bbolus\b.{0,24}\b(kcl|potassium chloride)\b", re.I)
TAMPONADE_RE = re.compile(
    r"\b(pericard|tamponade|electrical alternans|globoid heart|muffled heart)\b",
    re.I,
)
FUROSEMIDE_RE = re.compile(r"\b(furosemide|lasix|torsemide)\b", re.I)
PNEUMO_RE = re.compile(
    r"\b(pneumothorax|tension pneumo|glide sign|barrel[- ]chested|barrel[- ]shaped thorax)\b",
    re.I,
)
PLEURAL_RE = re.compile(
    r"\b(pyothorax|pleural effusion|chylothorax|hemothorax|haemothorax|septic pleur)\b",
    re.I,
)

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
        "cow": "cattle",
        "calf": "cattle",
        "turtle": "turtle",
        "tortoise": "tortoise",
        "chelonian": "turtle",
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
        if VINYL_RE.search(text):
            hard_stops.append(
                "Vinyl/plastic wrapper is a GI foreign-body question, not a toxin antidote."
            )
            do_not.append("Do not charcoal plastic. Do not clear on a normal radiograph.")
        return _pack(spec, hard_stops, do_not, do_next, localization, sources, nac_family)

    if PEACE_LILY_RE.search(text):
        hard_stops.append("Peace/calla lily is insoluble oxalate (oral pain), not feline AKI.")
        do_not.append("Do not run the Easter-lily AKI protocol for peace or calla lily.")
        localization = "Oxalate irritant plant, not Lilium nephrotoxin."
        sources.append("Plunkett 3e appendix card (legal split) verified against Merck houseplants")
    elif VALLEY_LILY_RE.search(text):
        hard_stops.append("Lily-of-the-valley is a cardiac glycoside plant, not a feline AKI lily.")
        do_not.append("Do not treat Convallaria as Lilium/Hemerocallis AKI.")
        localization = "Cardiac glycoside (Convallaria), not true-lily nephropathy."
        sources.append("Plunkett 3e appendix card verified against public cardiac-glycoside plant lists")
    elif spec == "cat" and LILY_RE.search(text):
        hard_stops.append("Cat + true lily / pollen / vase water: treat as AKI emergency.")
        do_not.append("Do not wait for 'just GI' or treat it as a dog plant.")
        do_next.append("Decontamination if recent and safe; start IVF; baseline and serial creatinine/UOP.")
        localization = "Lily toxicosis localizes to feline AKI, not a primary GI plant."
        sources.append("Cornell CVM public toxin list; ASPCA APCC lily guidance; Merck houseplants")
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

    if spec == "cat" and BLOCKED_RE.search(text):
        hard_stops.append("Cat + straining / blocked: urethral obstruction until the bladder is empty and the urethra is patent.")
        do_not.append("Do not discharge as constipation.")
        do_not.append("Do not harvest a 2013 unblock recipe or force a catheter before potassium/ECG are known.")
        do_next.append("Palpate the bladder. ECG and potassium before sedation to unblock. Pain △ Plumb. Fluids AAHA-style; never bolus a KCl bag.")
        sources.append("Merck: urethral obstruction / obstructive uropathy in small animals")
        if NSAID_RE.search(text):
            hard_stops.append("Blocked / azotemia-risk cat: hold the NSAID.")
        if DEX_RE.search(text):
            hard_stops.append("DexSP is not how you unblock a cat.")

    if spec in {"dog", "cat"} and UROABD_RE.search(text):
        localization = localization or (
            "Uroabdomen localizes to a leak in the urinary tract, not to free fluid alone."
        )
        hard_stops.append(
            "Uroabdomen: pair fluid and serum creatinine and potassium before a therapeutic tap story."
        )
        do_not.append("Do not diagnose uroabdomen by free fluid alone. Do not invent the ratio; the hospital/book names it.")
        do_next.append("Stabilize hyperK and perfusion first. Diversion. Surgery after the leak is localized.")
        sources.append("Merck obstructive uropathy; Plunkett uroabdomen pair (legal split, no dump)")

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

    if spec in {"dog", "cat"} and CHF_RE.search(text):
        localization = localization or (
            "Cardiogenic shock / CHF localizes to the pump, not empty vessels."
        )
        hard_stops.append("CHF / cardiogenic: do not default a hypovolemic shock bolus.")
        do_not.append(
            "Do not harvest 2013 furosemide or hypertonic-saline shock tables. △ Plumb / AAHA."
        )
        do_next.append(
            "Oxygen. Name the shock type. AAHA: hypotension in CHF is an inotrope conversation, not a reflexive bolus."
        )
        sources.append("AAHA fluid therapy 2024 cardiac patients; Merck CHF diuretic conversation")
        if SHOCK_BOLUS_RE.search(text):
            do_not.append("Do not give a shock bolus because the patient is hypotensive and in CHF.")

    if spec in {"dog", "cat"} and HYPOVOLEM_RE.search(text):
        do_not.append("Hypovolemic shock: bolus ≠ overnight drip. Reassess perfusion. Do not invent the mL/kg.")
        if spec == "cat":
            do_not.append(
                "Do not wait for a dog-style tachycardia. Cat hypovolemic shock is often bradycardia, hypothermia, and hypotension."
            )
        sources.append("AAHA fluid therapy 2024 hypovolemia; Merck small-volume vs large-volume framing")

    if spec in {"dog", "cat"} and HEMOABD_RE.search(text):
        localization = localization or (
            "Hemorrhagic peritoneal fluid. Pair PCV/TS with peripheral blood. "
            "Not uroabdomen until Cr/K pairs say so."
        )
        hard_stops.append(
            "Hemoabdomen: pair abdominal vs peripheral PCV/TS. Clotting blood is a vessel or organ stick, not a diagnosis."
        )
        do_not.append("Do not give vitamin K unless the rodenticide family is anticoagulant.")
        do_not.append(
            "Do not invent a transfusion PCV cutoff. Do not harvest 2013 wrap, DPL, or mL/kg blood-product tables. "
            "A round belly is not required (you can bleed a lot before the waist looks big)."
        )
        do_next.append(
            "FAST serially. Blood-product conversation. Cats: type-specific blood — no universal donor. "
            "If still crashing, surgery is the conversation. Negative tap does not rule out retroperitoneal bleed."
        )
        sources.append("Merck blood transfusions; Plunkett hemoperitoneum headings (legal split, no dump)")

    if KCL_BOLUS_RE.search(text):
        hard_stops.append("Never bolus a bag that contains KCl (AAHA).")
        do_not.append("Do not run a potassium-supplemented bag as a shock bolus.")
        sources.append("AAHA fluid therapy 2024: never bolus fluids supplemented with KCl")

    if spec in {"dog", "cat"} and TAMPONADE_RE.search(text):
        localization = (
            "Obstructive shock: pericardial filling. Looks like right-sided CHF. "
            "The pump cannot fill until the sac is drained."
        )
        hard_stops.append(
            "Cardiac tamponade: pericardiocentesis is the treatment. "
            "Diuretics are contraindicated in acute tamponade (Merck)."
        )
        do_not.append("Do not run a CHF furosemide protocol. Do not harvest the 2013 pericardiocentesis step list.")
        do_not.append("Do not treat tamponade as empty-vessel shock with a default bolus.")
        do_next.append(
            "Oxygen. FAST/echo. ECG during any tap. Use the hospital pericardiocentesis protocol. △ Plumb if lidocaine is used."
        )
        sources.append("Merck: pericardial disease in dogs and cats")
        if FUROSEMIDE_RE.search(text):
            hard_stops.append("Do not give furosemide for acute tamponade.")

    if spec in {"dog", "cat"} and PNEUMO_RE.search(text):
        localization = localization or (
            "Pleural-space air. Tension pneumothorax is obstructive shock: barrel chest, no air sounds, crashing."
        )
        hard_stops.append(
            "Tension pneumothorax: decompress now. Do not wait for a radiograph."
        )
        do_not.append("Do not treat as CHF. Do not harvest the 2013 chest-tube or open-needle recipe.")
        do_next.append(
            "Oxygen. TFAST: absent glide sign is a hint, not 100%. Thoracocentesis by hospital protocol. "
            "If air reaccumulates in minutes, a thoracostomy tube is the conversation."
        )
        sources.append("Merck: initial triage — catastrophic pleural space / glide sign")
        if FUROSEMIDE_RE.search(text):
            hard_stops.append("Do not give furosemide for pneumothorax.")

    if spec in {"dog", "cat"} and PLEURAL_RE.search(text):
        localization = localization or (
            "Pleural-space fluid. Quiet chest is not automatically CHF. "
            "Name transudate vs exudate vs chyle vs blood after you tap."
        )
        hard_stops.append(
            "Pleural effusion: radiographs are not therapy. Tap a distressed patient first. Save EDTA + sterile red-top."
        )
        do_not.append(
            "Do not send a pyothorax home after one tap. Do not harvest 2013 sedation or chest-tube French-size tables."
        )
        do_not.append("Do not skip anaerobic culture on a septic pleural exudate.")
        do_next.append(
            "Oxygen. Cytology. Cat: echo still on the table (CHF vs pyothorax vs FIP vs lymphoma). "
            "Chyle: fluid vs serum triglycerides. Blood: PCV/TS pair. Pyothorax: chest-tube conversation."
        )
        sources.append("Merck diagnostic techniques for pleural fluid; Plunkett pleural-effusion headings (legal split, no dump)")
        if FUROSEMIDE_RE.search(text) and not CHF_RE.search(text):
            do_not.append("Do not Lasix pleural fluid until CHF is actually the localization.")

    if spec in {"dog", "cat"} and ANAPHYLAXIS_RE.search(text):
        anax_loc = (
            "Distributive shock (type I). Dog: liver / hepatic-vein / portal pooling — GI signs, "
            "hives may be absent. Cat: respiratory tract."
        )
        localization = f"{localization} Also {anax_loc}" if localization else anax_loc
        hard_stops.append(
            "Anaphylactic shock: epinephrine is the crash drug, not diphenhydramine and not DexSP."
        )
        do_not.append("Do not wait for hives. Do not send a collapsing vaccine or sting patient home as 'just GI.'")
        do_not.append(
            "Do not harvest 2013 epinephrine, fluid, or hetastarch tables. Do not use RECOVER high-dose epi. △ crash-cart / Plumb."
        )
        do_not.append(
            "Gallbladder halo / wall edema is associated in dogs, not pathognomonic. Tamponade and right-sided heart fail also."
        )
        do_next.append(
            "Oxygen. Name distributive shock. Fluids AAHA-style (reassess; never bolus a KCl bag). "
            "FAST the gallbladder AND the heart. Pair PCV/TS if there is abdominal fluid."
        )
        sources.append("Merck hypersensitivity / systemic anaphylaxis (Tizard, Jan 2024); Quantz 2009 JVECC ALT/GB wall")
        if DIPHEN_RE.search(text):
            hard_stops.append("Diphenhydramine does not reverse anaphylactic shock.")
        if DEX_RE.search(text):
            do_not.append("A steroid is adjunct at most, not the first syringe. Azotemic cat: still no DexSP.")
        if HIGH_DOSE_EPI_RE.search(text):
            hard_stops.append("High-dose epinephrine is not the anaphylaxis plan either.")

    if RODENTICIDE_RE.search(text):
        do_not.append("Do not give vitamin K1 for an unknown block or for bromethalin/cholecalciferol/PH3.")
        do_next.append("Identify the family: anticoagulant vs bromethalin vs cholecalciferol vs phosphide.")
        sources.append("Four rodenticide families; vitamin K1 is not universal")

    if spec == "dog" and (GRAPE_RE.search(text) or TARTAR_RE.search(text)):
        hard_stops.append("Dog + grape/raisin/tamarind/cream of tartar: treat as AKI risk (Merck 2024 tartaric acid).")
        do_not.append("Do not wait for 'just GI' or invent a grape toxic dose.")
        do_not.append("Do not keep the 2013 line that the grape principle is unknown as current fact.")
        do_next.append("Decontaminate if recent and safe; IVF; serial creatinine. Ribes currants are not Vitis.")
        localization = localization or "Vitis/tamarind/tartaric-acid toxicosis localizes to canine AKI."
        sources.append("Merck Sept 2024 grape/raisin/tamarind; Wegenast 2022. Plunkett 2013 mechanism outdated.")

    if spec == "dog" and HOPS_RE.search(text):
        hard_stops.append("Dog + hops: malignant-hyperthermia picture. Cool and support.")
        do_not.append("Do not use NSAIDs or dipyrone to treat hops hyperthermia (Merck).")
        do_next.append("Dantrolene is the antidote conversation; △ Plumb.")
        sources.append("Merck: hops toxicosis in animals")

    if ALLIUM_RE.search(text) and spec in {"dog", "cat"}:
        hard_stops.append("Allium (onion/garlic): Heinz-body hemolysis can be delayed by days.")
        localization = localization or (
            "Allium localizes to RBC oxidative injury (Heinz/metHb), not primary feline AKI within hours."
        )
        do_not.append("Do not clear as fine tonight because the PCV is still normal.")
        do_not.append("Do not run the lily AKI protocol for garlic. It is not a few-hour nephrotoxin.")
        do_not.append(
            "Hemoglobinuric nephrosis, if it happens, is after hemolysis (typically days), not within hours of ingestion."
        )
        do_next.append("Baseline and delayed PCV/smear. Cats are more sensitive; garlic worse than onion.")
        do_next.append("If creatinine is already up in a few hours, localize elsewhere.")
        sources.append("Merck: garlic and onion toxicosis")

    if THRESHOLD_RE.search(text):
        hard_stops.append(
            "Do not write 'below the toxic threshold' unless APCC/Plumb named a number for THIS product and THIS weight."
        )
        do_not.append(
            "A seasoning-powder jerky label is not a published milligram of allium. Do not clear the Heinz clock with that sentence."
        )
        sources.append("Merck: garlic and onion toxicosis — delayed hemolysis, not a printed safe dose")

    if spec == "cat" and NPO12_RE.search(text):
        hard_stops.append(
            "Do not NPO a vomiting cat for 12 hours. Forman: hepatic lipidosis. Call instead."
        )
        do_not.append("Do not paste a canine bland-diet NPO line onto a cat discharge.")
        sources.append("Forman ACVIM 2021 feline pancreatitis: do not withhold food")

    if spec in {"dog", "cat"} and SIBLING_RE.search(text):
        hard_stops.append(
            "Same household is not the same localization. Two patients = two discharges."
        )
        do_not.append(
            "Do not paste the cranial-abdomen / low-fat / sucralfate GI sheet onto the exposure-only sibling, "
            "or the allium-watch sheet onto the tense-abdomen cat."
        )
        do_not.append(
            "Do not paste leftover dentistry or heart paragraphs onto a toxin or GI discharge."
        )
        do_next.append(
            "Write THIS patient's problem list. Sibling gets their own encounter, their own macro "
            "(`dc-gi` vs `dc-toxin`), their own recheck."
        )
        sources.append("Forman ACVIM 2021 vs Merck allium: two clocks, two notes")

    if spec in {"dog", "cat"} and (PANC_RE.search(text) or TENSE_ABD_RE.search(text)):
        localization = (
            "Cranial / upper abdomen: pancreas, stomach, biliary, cranial SI "
            "(linear FB still on the list). If tension predates tonight's meal, do not collapse the timeline."
        )
        hard_stops.append(
            "fPL / SNAP fPL is supportive, not pathognomonic. Do not invent the lab cutoff."
        )
        do_not.append("Do not starve the pancreas. Forman: withholding food is not recommended (hepatic lipidosis).")
        do_not.append(
            "Do not start antibiotics for uncomplicated pancreatitis. Do not use DexSP or an NSAID as the pancreatitis plan."
        )
        do_not.append("Do not invent a sucralfate or IVF mg/kg or a round fluid rate.")
        do_next.append(
            "Weight. AUS of the cranial abdomen. Glucose. Offer food or a feeding-tube conversation. Analgesia △ Plumb."
        )
        sources.append("Forman ACVIM 2021 feline pancreatitis; AAHA fluids 2024")
        if DAYS_ABD_RE.search(text) and TENSE_ABD_RE.search(text):
            do_not.append("Do not treat days of a tense upper abdomen as tonight's dietary indiscretion alone.")
        if FPL_SNAP_WEAK_RE.search(text):
            hard_stops.append(
                "SNAP fPL weak/equivocal is an abnormal SNAP, not a diagnosis and not a negative. "
                "Forman: abnormal includes the equivocal range. Do not invent the Spec cutoff."
            )
            do_not.append(
                "Do not copy this SNAP onto the housemate. Do not start antibiotics because the dot was weak."
            )
            do_next.append(
                "Cluster: signs plus cranial imaging (AUS). Spec fPL only if the owner wants a number. Offer food."
            )
        if OPIOID_RE.search(text):
            hard_stops.append(
                "One-time opioid is analgesia, not a pancreatitis disease-modifier. "
                "Forman: opioids are the primary analgesics; buprenorphine is adequate for most cats."
            )
            do_not.append(
                "Do not withhold a single opioid for theoretical sphincter-of-Oddi spasm. "
                "Do not switch to an NSAID because the SNAP was weak."
            )
            do_not.append(
                "Opioid ileus is a watch if linear FB is still on the list, not a reason to leave a painful cat untreated."
            )
            if VOLUME_CC_RE.search(text):
                hard_stops.append(
                    "A cc/mL volume is not a dose until THIS vial's mg/mL and the body weight are on the note."
                )
                do_not.append(
                    "Do not copy the cc onto the housemate. Do not assume 0.3 mg/mL — Simbadol and hydromorphone are different bottles."
                )
                do_next.append(
                    "Write mg = mL × labeled concentration, then △ Plumb. Chart the drug name and the vial."
                )

    if SUCRALFATE_RE.search(text):
        do_not.append("Sucralfate is a GI coating, not pancreatitis therapy. Separate it from other orals. △ Plumb.")

    if spec == "cat" and LOWFAT_RE.search(text):
        hard_stops.append(
            "Low fat is fine as an easy-to-digest lever (not greasy leftovers). "
            "It is not feline pancreatitis therapy and not the allium 3-5 day clock."
        )
        do_not.append(
            "Do not copy a 3-5 day low-fat prescription from canine pancreatitis or from the allium hemolysis clock."
        )
        do_next.append(
            "Offer food now if obstruction is off the table. Highly digestible / what the cat will eat. No allium snacks. "
            "If the story is hard dry jerky, name digestibility — do not fight a soft diet as if it were a canine fat prescription."
        )
        sources.append("Forman ACVIM 2021 feline pancreatitis nutrition")

    if spec == "cat" and FIBER_RE.search(text):
        hard_stops.append(
            "High fiber is not the easy-to-digest diet. It adds residue and bulk."
        )
        do_not.append(
            "Do not send a hairball/weight/constipation high-fiber food as the post-jerky or pancreatitis plan."
        )
        do_next.append(
            "Easy-to-digest means highly digestible, moist, small meals. Low fat is acceptable as that lever "
            "(not greasy leftovers). High fiber works against it."
        )
        sources.append("Forman ACVIM 2021: highly digestible; fat is not the feline lever")

    if spec == "dog" and MACADAMIA_RE.search(text):
        do_not.append("Do not treat macadamia as bromethalin.")
        do_next.append("Usually self-limiting weakness/hyperthermia. Check for chocolate or xylitol coating.")
        sources.append("Merck: macadamia nut toxicosis in dogs; Plunkett coating caveat (legal split)")

    if IVERMECTIN_RE.search(text):
        do_not.append("Do not copy a 2013 heartworm preventative written as mg/kg. Units are µg. △ Plumb.")
        sources.append("Merck ABCB1; Plunkett 3e ivermectin chapter has a mg-vs-µg typeset trap")
        if spec in {"turtle", "tortoise"} or CHELONIAN_RE.search(text):
            hard_stops.append("Do not give ivermectin to turtles or tortoises.")
            sources.append("Plunkett exotic appendix (legal split); standard chelonian teaching")
        if spec == "dog":
            do_next.append("Ask breed / MDR1 before a high-dose extra-label macrolide.")

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

    if spec in {"cat", "dog"} and VINYL_RE.search(text):
        vinyl_loc = (
            "GI foreign body (sheet or strip plastic). Often radiolucent. "
            "Not a vinyl-chloride toxidrome from a jerky bag."
        )
        localization = f"{localization} Also {vinyl_loc}" if localization else vinyl_loc
        hard_stops.append(
            "Possible vinyl/plastic wrapper: treat as GI FB, not as a toxin you charcoal."
        )
        do_not.append("Do not clear on a normal radiograph. Plastic is often radiolucent.")
        do_not.append("Do not yank a strip. Do not push plastic with a prokinetic.")
        do_next.append(
            "Confirm the wrapper is actually missing. Tongue base. Rads + AUS. "
            "Endoscopy if gastric and retrieval is still the conversation."
        )
        sources.append("Merck: gastrointestinal obstruction in small animals (plastic is non-digestible)")

    if spec in {"cat", "dog"} and JERKY_RE.search(text):
        do_next.append(
            "Read THIS package: onion/garlic (allium clock), xylitol if sugar-free. "
            "One-time beef jerky is not the chronic chicken-jerky Fanconi story."
        )
        do_next.append(
            "Hard/dry jerky: the home-food lever is moisture and digestibility, not fat percent. "
            "Soft, highly digestible small meals if obstruction is off the table."
        )
        if not ALLIUM_RE.search(text):
            do_not.append("Do not assume the jerky is allium-free. Seasoning blends are often onion/garlic.")
        sources.append("Merck: garlic and onion toxicosis; xylitol if the label says sugar-free")

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

    if spec == "horse" and (NEPHROSPLENIC_RE.search(text) or (PHENYLEPHRINE_RE.search(text) and "colic" in text.lower())):
        do_not.append("Do not give phenylephrine to a horse >15 years (Merck: fatal hemorrhage).")
        do_next.append("Confirm left kidney–spleen window on rectal/US. Jog/roll only if this is LDD/NSE, not LCV.")
        sources.append("Merck: left dorsal displacement / nephrosplenic entrapment")
        if re.search(r"\b(1[6-9]|[2-9]\d)\s*(y|yo|year)", text, re.I):
            hard_stops.append("Age >15: phenylephrine is off the table for nephrosplenic entrapment.")

    if spec == "horse" and LCV_RE.search(text):
        hard_stops.append("Large colon volvulus: surgery now. Not phenylephrine, not 'jog it out.'")
        do_not.append("Do not use peritoneal fluid as the viability veto; Merck: tap correlates poorly with colon involvement.")
        sources.append("Merck: volvulus of the large colon in horses")

    if spec == "horse" and BUTAZONE_RE.search(text):
        do_not.append("Do not continue phenylbutazone into right-dorsal-colitis territory.")
        do_next.append("Stop the NSAID. Look for hypoproteinemia / ventral edema. △ Plumb for any replacement analgesic.")
        sources.append("Merck: right dorsal colitis associated with NSAIDs")

    if spec == "horse" and COLITIS_RE.search(text):
        hard_stops.append("Horse + acute colitis/diarrhea: isolate first (Salmonella) before the treatment plan.")
        do_not.append("Do not treat medical colitis as surgical large-colon volvulus.")
        do_not.append("Do not invent a flunixin anti-endotoxin dose or a L/day fluid recipe. △ Plumb.")
        do_next.append("Fluids and electrolytes first. Ice the feet now (PHF laminitis 20–30%; other colitis still laminitis-risk).")
        localization = localization or (
            "Acute enterocolitis / endotoxemia. Isolate. Not LCV unless the colic picture is sudden severe "
            "distention in a surgical candidate."
        )
        sources.append("Merck: salmonellosis in horses; Potomac horse fever / Neorickettsia risticii")
        if SHOTGUN_ABX_RE.search(text) and not PHF_STORY_RE.search(text):
            hard_stops.append(
                "Adult colitis: do not start a shotgun antibiotic. Merck: antimicrobials do not shorten "
                "colitis or decrease Salmonella shedding."
            )
            do_next.append("Antimicrobials are a neutropenia/bacteremia conversation, or PHF oxytetracycline if that story.")
        if PHF_STORY_RE.search(text):
            do_next.append("PHF/river-pasture story: oxytetracycline is the named conversation; △ the number in Plumb.")
        if POLYMYXIN_RE.search(text) and re.search(r"\b(azotem|creatinine|aki|kidney)", text, re.I):
            hard_stops.append("Polymyxin B is off if the horse is already azotemic.")
        if FLUNIXIN_RE.search(text) and re.search(r"\b(azotem|creatinine|aki|kidney)", text, re.I):
            hard_stops.append("Azotemic colitis: hold the NSAID / flunixin.")

    if spec in {"dog", "cat"} and BACTERIURIA_RE.search(text) and not re.search(r"\b(stranguria|pollakiuria|dysuria|hematuria|fever|pyelo)\b", text, re.I):
        hard_stops.append("Subclinical bacteriuria: do not treat just because the culture grew (ISCAID 2019).")
        do_not.append("Do not call a silent positive culture a UTI.")
        sources.append("ISCAID 2019 UTI guidelines")

    if spec in {"dog", "cat"} and UTI_RE.search(text):
        do_not.append("Do not write a 14-day course for sporadic cystitis. ISCAID 2019: 3–5 days.")
        do_not.append("Do not reach for a fluoroquinolone or 3rd-gen cephalosporin as first-tier sporadic cystitis.")
        do_next.append("Culture when you can. Analgesia. Young cat: FIC until culture says otherwise.")
        sources.append("ISCAID 2019: sporadic cystitis 3–5 d; reserve FQ/3rd-gen")
        if spec == "cat" and FQ_RE.search(text) and re.search(r"\b(young|2 yo|3 yo|flutd)\b", text, re.I):
            hard_stops.append("Young cat FLUTD: empiric fluoroquinolone is not the ISCAID plan.")

    if spec in {"dog", "cat"} and CPR_RE.search(text):
        do_not.append("Do not use high-dose epinephrine. Pardo/RECOVER 2024 withdrew it.")
        do_not.append("Do not repeat atropine during CPR. Once, early, only if high vagal tone is the story.")
        do_next.append("2-minute cycles. 100–120 compressions/min. Bag-mask if not intubated. Read the crash-cart chart; △ Plumb.")
        sources.append("Pardo et al. 2024 RECOVER updated CPR recommendations (JVECC)")
        if HIGH_DOSE_EPI_RE.search(text):
            hard_stops.append("High-dose epinephrine is not in the 2024 RECOVER algorithm.")

    if spec in {"horse", "cattle"} and CPR_RE.search(text):
        hard_stops.append("SA RECOVER 2024 is not the large-animal CPA protocol.")
        do_not.append("Do not copy dog/cat crash-cart epinephrine/atropine onto a horse or cow without the species protocol.")
        sources.append("Pardo 2024 is dogs and cats; large-animal CPA is a different algorithm")

    addison_picture = spec == "dog" and (
        ADDISON_RE.search(text)
        or (HYPERK_RE.search(text) and (HYPONA_RE.search(text) or BRADY_SHOCK_RE.search(text) or "collapse" in text.lower()))
    )
    if addison_picture:
        hard_stops.append(
            "Dog + Addison-crisis picture: fluids first. Do not call azotemia 'AKI' or send home as gastroenteritis."
        )
        do_not.append("Do not treat the potassium number alone. Fluids often drop K; calcium gluconate is an ECG/cardiac conversation.")
        do_not.append("Do not copy the 2013 NaCl drip recipe or jack a chronic Na <120. Myelinolysis risk. △ the fluid plan.")
        do_not.append("Do not copy a 2013 cortisol cutoff printed as mg/dL. Units are µg/dL. △ the lab.")
        do_next.append("ECG, glucose now. Pull ACTH stim (or baseline cortisol to rule out if stable). Mineralocorticoid after confirm/stable. △ Plumb.")
        localization = localization or (
            "Hypovolemic shock with relative bradycardia / hyperK / hypoNa localizes to mineralocorticoid crisis "
            "until UO and ACTH say otherwise. Atypical Addison can have normal electrolytes."
        )
        sources.append("Merck Jul 2024 Addison disease (Van Vertloo); Plunkett 3e chapter verified for traps only")
        if PRED_ASSAY_RE.search(text) and (ADDISON_RE.search(text) or "acth" in text.lower()):
            hard_stops.append("Prednisolone/hydrocortisone before the ACTH stim contaminates the cortisol assay. DexSP does not (Merck).")
        if re.search(r"\binsulin\b", text, re.I) and "glucose" not in text.lower():
            hard_stops.append("Do not give insulin for hyperK until glucose is known. Addison dogs are already hypoglycemia-risk.")

    if spec in {"dog", "cat"} and DKA_RE.search(text):
        hard_stops.append("DKA: fluids first. Do not start insulin while the patient is still a volume wreck or already hypokalemic.")
        do_not.append("Do not give bicarbonate as the default for DKA acidosis.")
        do_not.append("Do not copy the 2013 40–60 mL/kg/h fluid recipe or an insulin CRI from memory. △ Plumb.")
        do_next.append("Look for the trigger (UTI, pancreatitis, steroids). Confirm ketones knowing the strip misses BHB. Recheck K and phosphorus after insulin starts.")
        localization = localization or "Decompensated diabetes with ketosis. Goal tonight is perfusion and stopping ketogenesis, not euglycemia."
        sources.append("Merck diabetes mellitus in dogs and cats; AAHA 2026 feline DKA. Plunkett 3e chapter verified for traps only")
        if BICARB_RE.search(text):
            hard_stops.append("Bicarbonate is not the default DKA plan.")
        if HYPOK_RE.search(text) and re.search(r"\binsulin\b", text, re.I):
            hard_stops.append("Hypokalemic DKA: replace potassium before insulin. △ Plumb.")

    if spec in {"dog", "cat"} and HHS_RE.search(text):
        hard_stops.append("HHS is not DKA. Very high glucose/osmolality, little or no ketone.")
        do_not.append("Do not dump hypotonic fluid into a chronic hypernatremia / hyperosmolar diabetic.")
        do_next.append("Correct osmolality slowly. Fluids first. △ insulin in Plumb if used.")
        sources.append("Merck diabetes; Plunkett HHS chapter (legal split) for the ketone-negative trap only")

    if spec in {"dog", "cat"} and SEIZURE_RE.search(text):
        hard_stops.append(
            "Seizure emergency: status is >5 min or two or more without recovery, not the 2013 30-minute line."
        )
        do_not.append("Do not invent a diazepam/midazolam/phenobarbital/keppra number. △ crash-cart / Plumb.")
        do_next.append("Glucose and temperature now. Benzodiazepine first (ACVIM: midazolam IV or IN if no vein). Then a maintenance load.")
        localization = localization or (
            "Stop the seizure, then split reactive (glucose/toxin/heat) from epileptic. Do not call syncope a seizure."
        )
        sources.append("ACVIM 2024 SE/CS consensus (Charalambous); Merck emergency anticonvulsants. Plunkett 3e for traps only")
        if THIRTY_MIN_SE_RE.search(text):
            hard_stops.append("Do not wait 30 minutes to call status. Treat at 5 minutes / no recovery.")
        if DIAZEPAM_PO_RE.search(text):
            if spec == "cat":
                hard_stops.append("Do not send a cat home on oral diazepam (idiosyncratic hepatic necrosis).")
            else:
                hard_stops.append("Oral diazepam is not dog maintenance (Merck). Not a discharge ASM.")
        if PENTOBARB_RE.search(text):
            do_not.append("Do not copy the 2013 pentobarbital-second-line table. Refractory SE is an airway / propofol conversation. △ Plumb.")

    if spec == "cattle" and LDA_RE.search(text):
        hard_stops.append("Right-sided abomasal ping: treat as surgical (RDA vs AV). Do not medically 'watch overnight.'")
        do_not.append("Do not call sequestered-HCl alkalosis DKA. Cattle ketosis has no acidemia; late AV can add lactate acidosis.")
        do_next.append("Name the ping side and rib band. Lactate if right-sided. Merck: L-lactate ≤2 favors outcome; ≥6 is a poor-outcome flag.")
        sources.append("Merck May 2026: abomasal displacement and volvulus in cattle (Mann)")

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

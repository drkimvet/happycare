"""Invariants for the public ER card and attending skill. No Plumb text. No PHI."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
CARD = (ROOT / "clinical" / "er_safety_card.md").read_text(encoding="utf-8")
SKILL = (ROOT / ".cursor" / "skills" / "midtown-attending" / "SKILL.md").read_text(encoding="utf-8")
LAND = (ROOT / "clinical" / "vet_ai_landscape.md").read_text(encoding="utf-8")
BRIEF = (ROOT / "clinical" / "resident_brief.py").read_text(encoding="utf-8")
SYLL = (ROOT / "clinical" / "five_minute_syllabus.md").read_text(encoding="utf-8")
VERIF = (ROOT / "clinical" / "source_verification.md").read_text(encoding="utf-8")
MACRO = (ROOT / "clinical" / "vetspire_macros.md").read_text(encoding="utf-8")


class PublicCardInvariants(unittest.TestCase):
    def test_license_line_on_all_user_facing_docs(self):
        for name, text in ("card", CARD), ("skill", SKILL), ("landscape", LAND):
            self.assertIn("replaces a veterinary license", text, msg=name)

    def test_never_invent_doses(self):
        for text in (CARD, SKILL, LAND):
            self.assertIn("confirm", text.lower())
            self.assertIn("plumb", text.lower())

    def test_card_has_species_gates(self):
        for needle in (
            "lily",
            "xylitol",
            "acetaminophen",
            "sago",
            "phosphine",
            "hamster",
            "azotemic",
        ):
            self.assertIn(needle, CARD.lower(), msg=needle)

    def test_phosphine_not_phosgene_as_fact(self):
        self.assertIn("phosphine", CARD.lower())
        self.assertIn("not phosgene", CARD.lower())

    def test_three_nac_families_not_mixed(self):
        self.assertIn("do not mix", CARD.lower())
        self.assertIn("acetaminophen", CARD.lower())
        self.assertIn("xylitol", CARD.lower())
        self.assertIn("hepatic", CARD.lower())

    def test_abdomen_not_drained_without_paired_cr(self):
        self.assertIn("fluid and serum creatinine and potassium", CARD.lower())

    def test_uop_not_pad(self):
        self.assertIn("not oliguria", CARD.lower())
        self.assertIn("pad", CARD.lower())

    def test_no_dexsp_no_nsaid_on_azotemic_cat(self):
        self.assertIn("no nsaid", CARD.lower())
        self.assertIn("no dexsp", CARD.lower())

    def test_cefazolin_cri_not_default(self):
        self.assertIn("cefazolin cri", CARD.lower())

    def test_charcoal_does_not_bind_xylitol(self):
        self.assertIn("charcoal", CARD.lower())
        self.assertIn("xylitol", CARD.lower())

    def test_four_rodenticide_families(self):
        for family in ("anticoagulant", "bromethalin", "cholecalciferol", "zinc phosphide"):
            self.assertIn(family, CARD.lower(), msg=family)

    def test_cattle_ketosis_no_acidemia(self):
        self.assertIn("no acidemia", CARD.lower())

    def test_peritoneal_iodine_not_standard(self):
        self.assertIn("povidone-iodine peritoneal lavage is not standard", CARD.lower())

    def test_decompressible_gets_consent(self):
        self.assertIn("referral", CARD.lower())
        self.assertIn("decompression", CARD.lower())

    def test_no_owner_phi_patterns(self):
        blob = "\n".join((CARD, SKILL, LAND, BRIEF, SYLL, VERIF, MACRO))
        self.assertNotRegex(blob, r"\bVIN\s+\d{4,}\b")
        self.assertNotRegex(blob, r"Wlsdb840")
        self.assertNotRegex(blob, r"ykim", re.I)
        # Case nicknames stay out of the committed card so a repo clone is not a chart.
        self.assertNotRegex(blob, r"\bMoMo\b")
        self.assertNotRegex(blob, r"\bWillie\b")

    def test_no_plumb_monograph_dump(self):
        # A public APAP historical load may be named as a family, but the card
        # must not grow into a stolen formulary table of many mg/kg lines.
        mgkg = re.findall(r"\b\d+(?:\.\d+)?\s*mg/kg\b", CARD.lower())
        self.assertLessEqual(len(mgkg), 3, msg=mgkg)

    def test_skill_forbids_product_logins(self):
        self.assertIn("do not login", SKILL.lower())
        self.assertIn("vin", SKILL.lower())
        self.assertIn("do not impersonate", SKILL.lower())

    def test_skill_does_not_steer_attending_to_instinct(self):
        self.assertIn("does not open instinct", SKILL.lower())
        self.assertIn("do not recommend opening it", SKILL.lower())
        self.assertIn("associate professor", SKILL.lower())
        self.assertIn("veterinary clinical sciences", SKILL.lower())
        self.assertIn("small animal medicine & surgery", SKILL.lower())
        self.assertIn("long island university college of veterinary medicine", SKILL.lower())
        self.assertIn("dvm, phd, ffcp", SKILL.lower())
        self.assertIn("둘 중 하나가 면허를 대신하지는 않습니다", SKILL)

    def test_landscape_admits_plumb_moat(self):
        self.assertIn("will not out-plumb plumb", LAND.lower())
        self.assertIn("instinct attending", LAND.lower())
        self.assertIn("openvet", LAND.lower())
        self.assertIn("scribblevet", LAND.lower())

    def test_official_syllabus_not_a_book_mirror(self):
        self.assertIn("wiley.com", SYLL.lower())
        self.assertNotIn("booksvets", SYLL.lower())
        self.assertIn("do not fetch pdfs from third-party book mirrors", SYLL.lower())
        self.assertIn("978-1-119-51317-9", SYLL)

    def test_verification_log_flags_outdated_and_unit_traps(self):
        self.assertIn("tartaric", VERIF.lower())
        self.assertIn("µg/kg", VERIF)
        self.assertIn("no chapter dump", VERIF.lower())
        self.assertIn("dropped", VERIF.lower())
        self.assertIn("not a work item", VERIF.lower())
        self.assertIn("addisonian crisis", VERIF.lower())
        self.assertIn("dka", VERIF.lower())
        self.assertIn("30 minutes", VERIF.lower())
        self.assertIn("oral diazepam", VERIF.lower())
        self.assertIn("forman", VERIF.lower())
        self.assertIn("hepatic lipidosis", VERIF.lower())
        self.assertIn("radiolucent", VERIF.lower())
        self.assertIn("vinyl", VERIF.lower())
        self.assertIn("not lily", VERIF.lower())
        self.assertIn("shock type", VERIF.lower())
        self.assertIn("cardiogenic", VERIF.lower())
        self.assertIn("urethral obstruction", VERIF.lower())
        self.assertIn("uroabdomen", VERIF.lower())
        self.assertIn("tamponade", VERIF.lower())
        self.assertIn("diuretics are contraindicated", VERIF.lower())
        self.assertIn("pneumothorax", VERIF.lower())
        self.assertIn("glide sign", VERIF.lower())
        self.assertIn("pyothorax", VERIF.lower())
        self.assertIn("anaerobic", VERIF.lower())
        self.assertIn("hemoabdomen", VERIF.lower())
        self.assertIn("universal donor", VERIF.lower())
        self.assertIn("same household is not the same localization", VERIF.lower())
        self.assertIn("below the typical toxic threshold", VERIF.lower())
        self.assertIn("12-hour npo", VERIF.lower())
        self.assertIn("anaphylaxis", VERIF.lower())
        self.assertIn("shock organ", VERIF.lower())
        self.assertIn("not pathognomonic", VERIF.lower())
        self.assertIn("imha", VERIF.lower())
        self.assertIn("4 drops", VERIF.lower())
        self.assertIn("central pallor", VERIF.lower())
        self.assertIn("head trauma", VERIF.lower())
        self.assertIn("corticosteroids are contraindicated", VERIF.lower())
        self.assertIn("cushing", VERIF.lower())
        self.assertIn("gdv deepening", VERIF.lower())
        self.assertIn("double-bubble", VERIF.lower())
        self.assertIn("orogastric", VERIF.lower())
        self.assertIn("sepsis / sirs", VERIF.lower())
        self.assertIn("organ dysfunction", VERIF.lower())
        self.assertIn("high-dose corticosteroids", VERIF.lower())
        self.assertIn("name the space before the syringe", VERIF.lower())
        self.assertIn("open-mouth", VERIF.lower())
        self.assertIn("new-onset asthma", VERIF.lower())
        self.assertIn("bloody diarrhea is a **syndrome**", VERIF.lower())
        self.assertIn("not recommended in mild to moderate", VERIF.lower())
        self.assertIn("non-hemorrhagic diarrhea", VERIF.lower())
        self.assertIn("eclampsia", VERIF.lower())
        self.assertIn("oral calcium during pregnancy", VERIF.lower())
        self.assertIn("not for subcutaneous", VERIF.lower())
        self.assertIn("dystocia", VERIF.lower())
        self.assertIn("placental separation", VERIF.lower())
        self.assertIn("obstructive dystocia", VERIF.lower())

    def test_vetspire_macros_are_paste_ready_and_not_a_login(self):
        self.assertIn("do not login to vetspire", MACRO.lower())
        self.assertIn("do not auto-apply throughout", MACRO.lower())
        self.assertIn("{{patient.name}}", MACRO)
        self.assertIn("`ddx-master`", MACRO)
        self.assertIn("`dc-master`", MACRO)
        self.assertIn("`ddx-addison`", MACRO)
        self.assertIn("`dc-uo`", MACRO)
        self.assertIn("household siblings are two patients", MACRO.lower())
        self.assertIn("`ddx-anax`", MACRO)
        self.assertIn("`dc-anax`", MACRO)
        self.assertIn("`ddx-imha`", MACRO)
        self.assertIn("`dc-imha`", MACRO)
        self.assertIn("`ddx-tbi`", MACRO)
        self.assertIn("`dc-tbi`", MACRO)
        self.assertIn("`ddx-sepsis`", MACRO)
        self.assertIn("`dc-sepsis`", MACRO)
        self.assertIn("`dc-resp`", MACRO)
        self.assertIn("name the space before the syringe", MACRO.lower())
        self.assertIn("`ddx-ahds`", MACRO)
        self.assertIn("`dc-parvo`", MACRO)
        self.assertIn("`ddx-eclampsia`", MACRO)
        self.assertIn("`dc-eclampsia`", MACRO)
        self.assertIn("`ddx-dystocia`", MACRO)
        self.assertIn("`dc-dystocia`", MACRO)
        self.assertIn("bloody diarrhea is a syndrome", MACRO.lower())
        self.assertIn("weak/equivocal = abnormal snap", MACRO.lower())
        self.assertIn("replaces a veterinary license", MACRO.lower())
        self.assertNotIn("Wlsdb840", MACRO)
        self.assertIn("mg/dl", VERIF.lower())
        self.assertIn("dexsp", VERIF.lower())
        self.assertNotIn("booksvets", VERIF.lower())
        # Must not harvest the typeset trap as a usable dose.
        self.assertNotRegex(VERIF.lower(), r"heartworm preventative is 6 mg/kg")

    def test_card_covers_syllabus_night_gates(self):
        for needle in (
            "grape",
            "ethylene glycol",
            "permethrin",
            "linear",
            "gdv",
            "pyometra",
            "thromboembolism",
            "acepromazine",
            "peace lily",
            "hops",
            "macadamia",
            "subclinical bacteriuria",
            "3–5 days",
            "high-dose epinephrine",
            "atropine",
            "addisonian",
            "myelinolysis",
            "dka",
            "bicarbonate",
            "small-animal emergency",
            "status epilepticus",
            "oral diazepam",
            "forman",
            "fpl",
            "hepatic lipidosis",
            "radiolucent",
            "vinyl",
            "few-hour nephrotoxin",
            "low-fat",
            "allium hemolysis",
            "digestibility",
            "high fiber is not easy-to-digest",
            "post-obstructive",
            "pair fluid and serum creatinine",
            "tamponade",
            "diuretics are contraindicated",
            "glide sign",
            "decompress now",
            "pyothorax",
            "anaerobic",
            "cardiogenic",
            "never bolus a bag that contains kcl",
            "type-specific",
            "round belly is not required",
            "same snack is not the same disease",
            "below the typical toxic threshold",
            "12 hours",
            "two patients",
            "epinephrine is the crash drug",
            "hives may be absent",
            "gallbladder halo",
            "weak positive snap is abnormal",
            "not a diagnosis and not a negative",
            "buprenorphine is adequate for most cats",
            "sphincter-of-oddi",
            "a cc/ml draw is not a dose",
            "gabapentin does not replace the opioid",
            "anemia is not imha",
            "4 drops saline",
            "spherocytes are not a criterion",
            "steroids are contraindicated",
            "cushing reflex",
            "mannitol only if euvolemic",
            "right lateral",
            "do not invent a lactate cutoff",
            "gastropexy prevents volvulus",
            "infection plus organ dysfunction",
            "not a sirs checkbox",
            "high-dose steroids are not recommended",
            "name the space before the syringe",
            "lasix + albuterol + dexsp",
            "new cough in an older cat is often pneumonia",
            "bloody diarrhea is **not a diagnosis**",
            "antibiotics are **not routine**",
            "~25% of parvo",
            "oral calcium during pregnancy predisposes",
            "calcium chloride is not for sq",
            "slow iv **calcium gluconate**",
            "obstruction vs inertia before oxytocin",
            "placental separation",
            "oxytocin is not for a stuck fetus",
        ):
            self.assertIn(needle, CARD.lower(), msg=needle)


if __name__ == "__main__":
    unittest.main()

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
        blob = "\n".join((CARD, SKILL, LAND, BRIEF, SYLL, VERIF))
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
            "ionophore",
            "acepromazine",
            "peace lily",
            "hops",
            "macadamia",
            "rda",
            "nephrosplenic",
            "phenylephrine",
            "subclinical bacteriuria",
            "3–5 days",
        ):
            self.assertIn(needle, CARD.lower(), msg=needle)


if __name__ == "__main__":
    unittest.main()

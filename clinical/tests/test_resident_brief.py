"""Resident brief must gate species and refuse invented doses."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from clinical.resident_brief import analyze, render  # noqa: E402


class ResidentBriefTests(unittest.TestCase):
    def test_no_species_no_dose(self):
        b = analyze("", "vomiting, give cerenon 1 mg/kg")
        self.assertTrue(any("no species" in x.lower() for x in b["hard_stops"]))
        self.assertIsNone(b["mg_per_kg"])
        self.assertIn("license", b["license"].lower())

    def test_cat_lily_is_aki(self):
        b = analyze("cat", "ate easter lily, vomiting")
        self.assertTrue(any("aki" in x.lower() for x in b["hard_stops"]))
        self.assertTrue(any("dog" in x.lower() for x in b["do_not"]))

    def test_dog_xylitol_glucose_not_charcoal(self):
        b = analyze("dog", "ate xylitol gum")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("glucose", joined)
        self.assertIn("charcoal", joined)
        self.assertEqual(b["nac_family"], "xylitol-consider")

    def test_cat_apap_hard_stop_and_apap_nac_family(self):
        b = analyze("cat", "owner gave tylenol")
        self.assertTrue(any("contraindicated" in x.lower() for x in b["hard_stops"]))
        self.assertEqual(b["nac_family"], "acetaminophen")
        self.assertTrue(any("hybrid" in x.lower() for x in b["do_not"]))

    def test_do_not_mix_sago_and_apap_nac(self):
        b = analyze("dog", "acetaminophen and sago palm")
        self.assertTrue(any("blend" in x.lower() or "mix" in x.lower() for x in b["hard_stops"] + b["do_not"]))

    def test_hamster_amoxicillin_hard_stop(self):
        b = analyze("hamster", "URI, start amoxicillin PO")
        self.assertTrue(any("hindgut" in x.lower() for x in b["hard_stops"]))

    def test_azotemic_cat_no_nsaid_no_dex(self):
        b = analyze("cat", "AKI creatinine 4.7, give meloxicam and DexSP")
        joined = " ".join(b["hard_stops"]).lower()
        self.assertIn("nsaid", joined)
        self.assertIn("dexsp", joined)

    def test_cefazolin_cri_rejected(self):
        b = analyze("cat", "sick, start cefazolin CRI overnight")
        self.assertTrue(any("cefazolin cri" in x.lower() for x in b["hard_stops"]))

    def test_drain_abdomen_without_paired_cr(self):
        b = analyze("cat", "tap the belly / drain abdomen tonight")
        self.assertTrue(any("do not drain" in x.lower() for x in b["hard_stops"]))

    def test_right_kidney_soft_abdomen_localizes(self):
        b = analyze(
            "cat",
            "creatinine 4.7, right renomegaly, fluid-filled kidney",
            abdomen="soft abdomen, no tension",
            uop_ml_per_kg_hr=1.0,
        )
        self.assertIn("kidney/ureter", b["localization"].lower())
        joined = " ".join(b["do_not"]).lower()
        self.assertIn("not oliguria", joined)
        self.assertIn("uroabdomen", joined)
        self.assertTrue(any("referral" in x.lower() for x in b["do_next"]))

    def test_phosphide_is_phosphine(self):
        b = analyze("dog", "zinc phosphide rodenticide, book said phosgene")
        self.assertTrue(any("phosphine" in x.lower() for x in b["hard_stops"]))

    def test_unknown_rodenticide_not_vitamin_k(self):
        b = analyze("dog", "ate rodenticide, unknown block")
        self.assertTrue(any("vitamin k" in x.lower() for x in b["do_not"]))

    def test_dog_grape_is_aki(self):
        b = analyze("dog", "ate raisins")
        self.assertTrue(any("aki" in x.lower() for x in b["hard_stops"]))

    def test_ethylene_glycol_do_not_wait(self):
        b = analyze("cat", "licked antifreeze")
        self.assertTrue(any("fomepizole" in x.lower() for x in b["hard_stops"]))

    def test_cat_permethrin_not_atropine(self):
        b = analyze("cat", "dog permethrin spot-on, give atropine")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("permethrin", joined)
        self.assertIn("atropine", joined)

    def test_do_not_yank_linear_string(self):
        b = analyze("cat", "string under the tongue, yank the string")
        self.assertTrue(any("do not yank" in x.lower() for x in b["hard_stops"]))

    def test_gdv_no_emesis(self):
        b = analyze("dog", "GDV, induce emesis")
        self.assertTrue(any("emesis" in x.lower() for x in b["do_not"]))

    def test_rabbit_hold_prokinetic_until_obstruction_off(self):
        b = analyze("rabbit", "GI stasis, start metoclopramide and syringe-feed")
        self.assertTrue(any("obstruction" in x.lower() for x in b["hard_stops"]))

    def test_horse_ionophore(self):
        b = analyze("horse", "ate cattle feed with monensin")
        self.assertTrue(any("ionophore" in x.lower() or "cardiotoxic" in x.lower() for x in b["hard_stops"]))

    def test_acepromazine_not_for_storm(self):
        b = analyze("dog", "thunderstorm phobia, send home acepromazine")
        self.assertTrue(any("not an anxiolytic" in x.lower() for x in b["hard_stops"]))

    def test_peace_lily_is_not_feline_aki(self):
        b = analyze("cat", "ate peace lily")
        joined = " ".join(b["hard_stops"]).lower()
        self.assertIn("oxalate", joined)
        self.assertNotIn("aki emergency", joined)

    def test_lily_of_the_valley_is_cardiac(self):
        b = analyze("dog", "lily of the valley")
        self.assertTrue(any("cardiac glycoside" in x.lower() for x in b["hard_stops"]))

    def test_cream_of_tartar_is_grape_family(self):
        b = analyze("dog", "ate cream of tartar")
        self.assertTrue(any("tartaric" in x.lower() for x in b["hard_stops"]))

    def test_hops_no_nsaid_for_fever(self):
        b = analyze("dog", "got into hops, hyperthermia, give NSAID")
        self.assertTrue(any("nsaid" in x.lower() for x in b["do_not"]))

    def test_turtle_no_ivermectin(self):
        b = analyze("tortoise", "start ivermectin for mites")
        self.assertTrue(any("ivermectin" in x.lower() for x in b["hard_stops"]))

    def test_cattle_rda_not_overnight_medical(self):
        b = analyze("cattle", "fresh cow, right ping, possible RDA")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("surgical", joined)
        self.assertIn("dka", joined)

    def test_old_horse_no_phenylephrine(self):
        b = analyze("horse", "18 yo gelding, nephrosplenic entrapment, give phenylephrine")
        self.assertTrue(any("phenylephrine" in x.lower() for x in b["hard_stops"] + b["do_not"]))

    def test_large_colon_volvulus_is_surgery(self):
        b = analyze("horse", "broodmare, large colon volvulus")
        self.assertTrue(any("surgery" in x.lower() for x in b["hard_stops"]))

    def test_subclinical_bacteriuria_not_treated(self):
        b = analyze("dog", "subclinical bacteriuria, culture positive, start convenia")
        self.assertTrue(any("subclinical" in x.lower() for x in b["hard_stops"]))

    def test_sporadic_cystitis_not_14_days(self):
        b = analyze("dog", "sporadic cystitis, 14-day enrofloxacin")
        joined = " ".join(b["do_not"]).lower()
        self.assertIn("14-day", joined)
        self.assertIn("fluoroquinolone", joined)

    def test_high_dose_epi_withdrawn(self):
        b = analyze("cat", "CPA, high-dose epinephrine")
        self.assertTrue(any("high-dose" in x.lower() for x in b["hard_stops"] + b["do_not"]))

    def test_horse_cpr_not_sa_recover(self):
        b = analyze("horse", "arrest, start RECOVER epinephrine")
        self.assertTrue(any("large-animal" in x.lower() or "not the large-animal" in x.lower() for x in b["hard_stops"]))

    def test_render_and_cli_never_emit_mg_per_kg_number(self):
        b = analyze("cat", "lily, AKI, UOP 1", uop_ml_per_kg_hr=1.0)
        text = render(b)
        self.assertNotRegex(text, r"\b\d+(?:\.\d+)?\s*mg/kg\b")
        self.assertIn("license", text.lower())
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "clinical" / "resident_brief.py"),
                "--species",
                "cat",
                "--problem",
                "right renomegaly, creatinine 4.7",
                "--abdomen",
                "soft abdomen",
                "--uop",
                "1",
                "--json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        self.assertIsNone(payload["mg_per_kg"])
        self.assertIn("kidney/ureter", payload["localization"])


if __name__ == "__main__":
    unittest.main()

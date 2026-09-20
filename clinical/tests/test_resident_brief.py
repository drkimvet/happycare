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

    def test_blocked_cat_not_constipation(self):
        b = analyze("cat", "straining in the box, blocked, give DexSP")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("urethral obstruction", joined)
        self.assertIn("constipation", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("potassium", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_uroabdomen_not_free_fluid_alone(self):
        b = analyze("cat", "uroabdomen, ruptured bladder, tap the belly")
        loc = b["localization"].lower()
        self.assertIn("leak", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("pair", joined)
        self.assertIn("free fluid alone", joined)
        self.assertIsNone(b["mg_per_kg"])

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

    def test_vinyl_wrapper_is_fb_not_charcoal(self):
        b = analyze("cat", "2 whole beef jerky ingestion with potential vynyl")
        loc = b["localization"].lower()
        self.assertIn("foreign body", loc)
        self.assertIn("radiolucent", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("charcoal", joined)
        self.assertIn("prokinetic", joined)
        self.assertIn("wrapper", joined)
        self.assertIn("allium", joined)
        self.assertIn("digestibility", joined)
        self.assertNotIn("fanconi", " ".join(b["hard_stops"]).lower())
        self.assertIsNone(b["mg_per_kg"])
        both = analyze(
            "cat",
            "vynyl wrapper, fPL",
            abdomen="tense upper abdomen few days",
        )
        bloc = both["localization"].lower()
        self.assertIn("cranial", bloc)
        self.assertIn("foreign body", bloc)

    def test_no_species_still_flags_vinyl(self):
        b = analyze("", "ate vinyl wrapper")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("no species", joined)
        self.assertIn("foreign-body", joined)
        self.assertIn("charcoal", joined)
        self.assertIsNone(b["mg_per_kg"])

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

    def test_horse_colitis_isolate_and_ice(self):
        b = analyze("horse", "acute colitis, fever, diarrhea")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertTrue(any("isolate" in x.lower() for x in b["hard_stops"]))
        self.assertIn("ice", joined)
        self.assertIn("volvulus", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_horse_colitis_shotgun_abx_without_phf(self):
        b = analyze("horse", "acute diarrhea, start antibiotics penicillin gentamicin metronidazole")
        self.assertTrue(any("shotgun" in x.lower() for x in b["hard_stops"]))

    def test_horse_phf_oxytet_not_shotgun_stop(self):
        b = analyze("horse", "Potomac horse fever, river pasture, start oxytetracycline")
        joined = " ".join(b["hard_stops"]).lower()
        self.assertNotIn("shotgun", joined)
        self.assertTrue(any("oxytetracycline" in x.lower() for x in b["do_next"]))
        self.assertTrue(any("ice" in x.lower() for x in b["do_next"]))

    def test_horse_colitis_polymyxin_off_if_azotemic(self):
        b = analyze("horse", "colitis, azotemic, start polymyxin B")
        self.assertTrue(any("polymyxin" in x.lower() for x in b["hard_stops"]))

    def test_dog_addison_crisis_not_aki_or_gi(self):
        b = analyze("dog", "Addisonian crisis, collapse, hyperkalemia, hyponatremia, bradycardia")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("fluids first", joined)
        self.assertIn("gastroenteritis", joined)
        self.assertIn("mg/dl", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_pred_before_acth_contaminates_assay(self):
        b = analyze("dog", "suspect Addison, give prednisolone then ACTH stim")
        self.assertTrue(any("contaminat" in x.lower() or "assay" in x.lower() for x in b["hard_stops"]))

    def test_addison_insulin_needs_glucose_first(self):
        b = analyze("dog", "Addisonian crisis, hyperkalemia, give insulin")
        self.assertTrue(any("glucose" in x.lower() for x in b["hard_stops"]))

    def test_dka_fluids_before_insulin(self):
        b = analyze("dog", "DKA, start insulin now, give bicarbonate")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("fluids first", joined)
        self.assertIn("bicarbonate", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dka_hypokalemia_hold_insulin(self):
        b = analyze("cat", "DKA, hypokalemia, start insulin")
        self.assertTrue(any("potassium" in x.lower() or "hypokal" in x.lower() for x in b["hard_stops"]))

    def test_hhs_is_not_dka(self):
        b = analyze("cat", "hyperosmolar HHS, no ketones")
        self.assertTrue(any("not dka" in x.lower() for x in b["hard_stops"]))

    def test_status_is_five_minutes_not_thirty(self):
        b = analyze("dog", "status epilepticus for 30 min, still seizing")
        joined = " ".join(b["hard_stops"]).lower()
        self.assertIn("5 min", joined)
        self.assertIn("30", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_no_oral_diazepam_home(self):
        b = analyze("cat", "cluster seizures, send home diazepam PO")
        self.assertTrue(any("oral diazepam" in x.lower() or "hepatic" in x.lower() for x in b["hard_stops"]))

    def test_cat_allium_delayed_heinz(self):
        b = analyze("cat", "ate onion and garlic powder, tired only")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("heinz", joined)
        self.assertIn("do not clear", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_garlic_not_few_hour_nephrotoxin(self):
        b = analyze("cat", "garlic toxicity, does it affect kidney within few hrs")
        loc = b["localization"].lower()
        self.assertIn("rbc", loc)
        self.assertIn("not primary feline aki", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("lily", joined)
        self.assertIn("few-hour nephrotoxin", joined)
        self.assertIn("after hemolysis", joined)
        self.assertIn("localize elsewhere", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_low_fat_not_forman_default(self):
        b = analyze("cat", "low fat diet for 3-5 days, pancreatitis")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("easy-to-digest lever", joined)
        self.assertIn("allium hemolysis clock", joined)
        self.assertIn("obstruction is off the table", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_high_fiber_not_easy_digest(self):
        b = analyze("cat", "high fiber diet after beef jerky, easy to digest")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("high fiber is not the easy-to-digest", joined)
        self.assertIn("residue", joined)
        self.assertIn("low fat is acceptable", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_chf_no_default_shock_bolus(self):
        b = analyze("dog", "CHF pulmonary edema, give a shock bolus")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("cardiogenic", joined)
        self.assertIn("shock bolus", joined)
        self.assertIn("2013", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_hypovolemic_shock_not_tachycardia(self):
        b = analyze("cat", "hypovolemic shock, hemoabdomen")
        joined = " ".join(b["do_not"] + b["do_next"]).lower()
        self.assertIn("bradycardia", joined)
        self.assertIn("pcv/ts", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_never_bolus_kcl_bag(self):
        b = analyze("dog", "shock, bolus the KCl bag")
        self.assertTrue(any("kcl" in x.lower() for x in b["hard_stops"]))
        self.assertIsNone(b["mg_per_kg"])

    def test_tamponade_not_lasix_or_shock_bolus(self):
        b = analyze("dog", "pericardial tamponade, muffled heart, give furosemide and a shock bolus")
        loc = b["localization"].lower()
        self.assertIn("obstructive", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("diuretic", joined)
        self.assertIn("furosemide", joined)
        self.assertIn("2013", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_fpl_tense_upper_abdomen_is_forman_not_tonight_meal(self):
        b = analyze(
            "cat",
            "sucralfate IVF fPL test",
            abdomen="tense upper abdomen few days",
        )
        loc = b["localization"].lower()
        self.assertIn("cranial", loc)
        self.assertIn("timeline", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("pathognomonic", joined)
        self.assertIn("withhold", joined)
        self.assertIn("hepatic lipidosis", joined)
        self.assertIn("sucralfate", joined)
        self.assertIn("dietary indiscretion", joined)
        self.assertTrue(any("forman" in x.lower() for x in b["sources"]))
        self.assertIsNone(b["mg_per_kg"])

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

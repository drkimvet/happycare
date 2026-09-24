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
        b = analyze("dog", "GDV, induce emesis, trocar and send home, lactate 9 so euthanize")
        self.assertTrue(any("emesis" in x.lower() for x in b["do_not"]))
        loc = b["localization"].lower()
        self.assertIn("obstructive", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("right lateral", joined)
        self.assertIn("lactate cutoff", joined)
        self.assertIn("gastropexy", joined)
        self.assertIn("2013", joined)
        self.assertIsNone(b["mg_per_kg"])

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
        joined = " ".join(b["do_not"] + b["do_next"] + b["hard_stops"]).lower()
        self.assertIn("bradycardia", joined)
        self.assertIn("pcv/ts", joined)
        self.assertIn("type-specific", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_hemoabdomen_not_vitamin_k_or_invented_pcv_cutoff(self):
        b = analyze("dog", "hemoabdomen, give vitamin K, transfuse at PCV 20")
        loc = b["localization"].lower()
        self.assertIn("pcv/ts", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("anticoagulant", joined)
        self.assertIn("cutoff", joined)
        self.assertIn("round belly", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_anaphylaxis_epi_not_benadryl_or_hives_required(self):
        b = analyze(
            "dog",
            "anaphylaxis after vaccine, collapse, no hives, gallbladder halo, give diphenhydramine and DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("liver", loc)
        self.assertIn("hives may be absent", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("epinephrine is the crash drug", joined)
        self.assertIn("diphenhydramine does not reverse", joined)
        self.assertIn("not pathognomonic", joined)
        self.assertIn("2013", joined)
        self.assertNotIn("90 ml/kg", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_anaphylaxis_respiratory_not_high_dose_epi(self):
        b = analyze("cat", "anaphylaxis, vaccine reaction, dyspnea, high-dose epinephrine")
        loc = b["localization"].lower()
        self.assertIn("respiratory", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("epinephrine is the crash drug", joined)
        self.assertIn("high-dose epinephrine is not the anaphylaxis plan", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_anaphylaxis_epinephrine_is_not_cpr(self):
        b = analyze("dog", "anaphylaxis, give epinephrine")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertNotIn("2-minute cycles", joined)
        self.assertIn("epinephrine is the crash drug", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_sibling_cats_not_same_discharge_or_toxic_threshold_or_12h_npo(self):
        b = analyze(
            "cat",
            "two cats same household sibling garlic beef jerky, copy discharge, "
            "below the typical toxic threshold, withhold food 12 hours if vomiting",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("same household is not the same localization", joined)
        self.assertIn("two patients = two discharges", joined)
        self.assertIn("toxic threshold", joined)
        self.assertIn("12 hours", joined)
        self.assertIn("hepatic lipidosis", joined)
        self.assertIn("dentistry", joined)
        self.assertIn("dc-gi", joined)
        self.assertTrue(any("heinz" in x.lower() or "allium" in x.lower() for x in b["hard_stops"] + [b["localization"]]))
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

    def test_tension_pneumo_not_rads_first_or_lasix(self):
        b = analyze("dog", "tension pneumothorax, barrel-chested, no glide sign, give furosemide, wait for rads")
        loc = b["localization"].lower()
        self.assertIn("pleural", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("decompress now", joined)
        self.assertIn("radiograph", joined)
        self.assertIn("furosemide", joined)
        self.assertIn("2013", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_pyothorax_not_one_tap_home_or_lasix(self):
        b = analyze("cat", "pyothorax pleural effusion, one tap and send home, give furosemide")
        loc = b["localization"].lower()
        self.assertIn("pleural", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("radiographs are not therapy", joined)
        self.assertIn("one tap", joined)
        self.assertIn("anaerobic", joined)
        self.assertIn("lasix", joined)
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

    def test_snap_fpl_weak_positive_is_abnormal_not_diagnosis(self):
        b = analyze("cat", "fpl snap weak positive, tense cranial abdomen")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("abnormal snap", joined)
        self.assertIn("not a diagnosis and not a negative", joined)
        self.assertIn("equivocal", joined)
        self.assertIn("housemate", joined)
        self.assertNotRegex(" ".join(b["hard_stops"] + b["do_not"]), r"\b5\.[34]\b")
        self.assertIsNone(b["mg_per_kg"])

    def test_one_time_opioid_not_oddi_reason_to_skip_analgesia(self):
        b = analyze("cat", "mild pancreatitis, SNAP fPL weak positive, one-time buprenorphine")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("analgesia, not a pancreatitis disease-modifier", joined)
        self.assertIn("buprenorphine is adequate for most cats", joined)
        self.assertIn("sphincter-of-oddi", joined)
        self.assertIn("nsaid", joined)
        self.assertIn("ileus", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_opioid_cc_volume_is_not_a_dose_without_vial(self):
        b = analyze("cat", "mild pancreatitis, buprenorphine 0.16 cc IV")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("volume is not a dose", joined)
        self.assertIn("mg/ml", joined)
        self.assertIn("simbadol", joined)
        self.assertNotIn("0.16", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_gabapentin_does_not_replace_opioid_in_acute_pancreatitis(self):
        b = analyze("cat", "pancreatitis, colleague said give gabapentin instead of buprenorphine")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("does not replace opioid", joined)
        self.assertIn("primary analgesic", joined)
        self.assertIn("chronic", joined)
        self.assertIn("xylitol", joined)
        self.assertIn("housemate", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_imha_needs_saline_agglutination_not_garlic_pred(self):
        b = analyze("dog", "IMHA, autoagglutination, give prednisolone for garlic hemolytic anemia")
        loc = b["localization"].lower()
        self.assertIn("hemolysis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("4 drops", joined)
        self.assertIn("not imha until", joined)
        self.assertIn("heinz", joined)
        self.assertIn("immunosuppress", joined)
        self.assertIn("thromboprophylaxis", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_imha_spherocytes_not_a_criterion(self):
        b = analyze("cat", "IMHA, spherocytes, DexSP, transfuse at PCV 12")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("do not diagnose feline imha on spherocytes", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("pcv transfusion cutoff", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_tbi_no_dexsp_or_lasix_or_mannitol_while_dry(self):
        b = analyze(
            "dog",
            "head trauma, Cushing reflex, hypovolemic, give DexSP and furosemide and mannitol",
        )
        loc = b["localization"].lower()
        self.assertIn("cushing", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("steroids are contraindicated", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("furosemide", joined)
        self.assertIn("mannitol", joined)
        self.assertIn("hypovolemic", joined)
        self.assertIn("glucose", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_sepsis_is_not_a_sirs_checkbox(self):
        b = analyze(
            "dog",
            "sepsis, SIRS 2 of 4, lactate 6 so euthanize, DexSP and 90 mL/kg then send home as GI",
        )
        loc = b["localization"].lower()
        self.assertIn("organ dysfunction", loc)
        self.assertIn("distributive", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("not a sirs checkbox", joined)
        self.assertIn("lactate/map", joined)
        self.assertIn("source", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("just gi", joined)
        self.assertIn("2013", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_sepsis_hypothermia_not_waiting_for_fever(self):
        b = analyze("cat", "septic shock, hypothermic, start high-dose DexSP")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("hypothermic", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("source", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_dyspnea_name_the_space_before_cocktail(self):
        b = analyze(
            "cat",
            "open-mouth breathing, wheeze, give Lasix and albuterol and DexSP, then rads",
        )
        loc = b["localization"].lower()
        self.assertIn("name the space", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("lasix + albuterol + dexsp", joined)
        self.assertIn("furosemide", joined)
        self.assertIn("wrestle", joined)
        self.assertIn("anxiety", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_azotemic_asthma_cat_still_no_dexsp(self):
        b = analyze("cat", "asthma, AKI, creatinine high, start DexSP")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("no dexsp", joined)
        self.assertIn("name the space", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_ahds_is_not_a_diagnosis_and_not_routine_antibiotics(self):
        b = analyze(
            "dog",
            "AHDS HGE bloody diarrhea, send home as colitis, shotgun antibiotics, skip parvo SNAP",
        )
        loc = b["localization"].lower()
        self.assertIn("not a diagnosis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("parvo", joined)
        self.assertIn("colitis", joined)
        self.assertIn("shotgun", joined)
        self.assertIn("pcv", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_parvo_still_tested_if_stool_not_red(self):
        b = analyze("dog", "puppy parvovirus, diarrhea not bloody, unvaccinated")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("non-bloody", joined)
        self.assertIn("isolate", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_eclampsia_no_cacl_sq_no_prenatal_calcium(self):
        b = analyze(
            "dog",
            "nursing 3 weeks postpartum, tremors and seizure, give calcium chloride SQ, "
            "start oral calcium during next pregnancy",
        )
        loc = b["localization"].lower()
        self.assertIn("hypocalcemia", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("calcium gluconate", joined)
        self.assertIn("subcutaneous", joined)
        self.assertIn("pregnancy", joined)
        self.assertIn("glucose", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dystocia_oxytocin_not_for_obstruction(self):
        b = analyze(
            "dog",
            "bulldog dystocia, green discharge before first puppy, give oxytocin at home",
        )
        loc = b["localization"].lower()
        self.assertIn("placental separation", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("stuck fetus", joined)
        self.assertIn("c-section", joined)
        self.assertIn("breeder", joined)
        self.assertIn("hour", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_larpar_not_lasix_albuterol_not_ice_water(self):
        b = analyze(
            "dog",
            "Labrador inspiratory stridor, voice change, give Lasix and albuterol, ice-water bath",
        )
        loc = b["localization"].lower()
        self.assertIn("larynx", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("kennel cough", joined)
        self.assertIn("furosemide", joined)
        self.assertIn("bronchodilator", joined)
        self.assertIn("ice-water", joined)
        self.assertIn("aspiration", joined)
        self.assertIn("tie-back", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_larpar_no_throat_exam_without_tube(self):
        b = analyze("dog", "laryngeal paralysis, crashing")
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("tube", joined)
        self.assertIn("tracheostomy", joined)
        self.assertIn("rads are not diagnostic", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_toy_puppy_hypoglycemia_glucose_not_keppra(self):
        b = analyze(
            "dog",
            "Yorkie puppy seizure, give keppra, send home, pour Karo into mouth",
        )
        loc = b["localization"].lower()
        self.assertIn("glucose now is the syringe", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("keppra", joined)
        self.assertIn("pour syrup", joined)
        self.assertIn("insulinoma puppy", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_toy_puppy_hypoglycemia_no_npo(self):
        b = analyze("dog", "8-week Maltese, dull, hypoglycemia, NPO, insulinoma")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("npo", joined)
        self.assertIn("insulinoma", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_type_b_not_type_a_stop_bag_not_diphen_first(self):
        b = analyze(
            "cat",
            "type B cat, transfusion reaction, give type A blood, diphenhydramine first",
        )
        loc = b["localization"].lower()
        self.assertIn("stop and look", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("stop the bag first", joined)
        self.assertIn("type a blood to a type b cat", joined)
        self.assertIn("diphenhydramine is not first", joined)
        self.assertIn("no universal donor", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_taco_no_shock_bolus_no_restart_unit(self):
        b = analyze(
            "dog",
            "transfusion reaction TACO, restart the same unit, shock bolus",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("stop the bag first", joined)
        self.assertIn("restart the same unit", joined)
        self.assertIn("shock bolus", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_vestibular_not_dexsp_stroke(self):
        b = analyze(
            "dog",
            "old dog head tilt and nystagmus, give DexSP for stroke",
        )
        loc = b["localization"].lower()
        self.assertIn("peripheral vs central before home", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("dexsp", joined)
        self.assertIn("stroke", joined)
        self.assertIn("meclizine", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_vestibular_stop_metronidazole_and_horner_is_ear(self):
        b = analyze(
            "dog",
            "head tilt, nystagmus, Horner and facial paralysis, on metronidazole, vertical nystagmus",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("stop metronidazole", joined)
        self.assertIn("inner ear", joined)
        self.assertIn("vertical nystagmus", joined)
        self.assertIn("just old", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_snakebite_not_ice_tourniquet_dexsp_nsaid(self):
        b = analyze(
            "dog",
            "rattlesnake bite, ice the limb, tourniquet, give DexSP and carprofen",
        )
        loc = b["localization"].lower()
        self.assertIn("antivenom is the specific", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not ice, cut, suck, or tourniquet", joined)
        self.assertIn("tourniquet", joined)
        self.assertIn("dexsp is not the antivenom", joined)
        self.assertIn("nsaid", joined)
        self.assertIn("1–5 vials", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_coral_not_dry_bite_home(self):
        b = analyze(
            "dog",
            "coral snake, dry bite, send home",
        )
        loc = b["localization"].lower()
        self.assertIn("ventilate", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a spreading limb home as a dry bite", joined)
        self.assertIn("coral snake", joined)
        self.assertIn("ventilate", joined)
        self.assertIn("not manufactured", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_he_not_benzo_dexsp(self):
        b = analyze(
            "dog",
            "head pressing, hepatic encephalopathy, give diazepam and DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("ammonia is not the diagnosis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not give benzodiazepines for hepatic encephalopathy", joined)
        self.assertIn("dexsp", joined)
        self.assertIn("glucose now", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_he_somnolent_no_oral_lactulose_no_routine_ffp(self):
        b = analyze(
            "cat",
            "acute liver failure, somnolent, pour lactulose, FFP for prolonged PT",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not pour lactulose into a somnolent mouth", joined)
        self.assertIn("routine ffp", joined)
        self.assertIn("long pt", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_proptosis_lubricate_not_dry_home(self):
        b = analyze(
            "dog",
            "pug proptosis, send home dry, no lubricant",
        )
        loc = b["localization"].lower()
        self.assertIn("lubricate now", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a dry globe home", joined)
        self.assertIn("replacement or enucleation tonight", joined)
        self.assertIn("3-hour", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_proptosis_not_lobby_push_or_flunixin(self):
        b = analyze(
            "cat",
            "proptosis, push the globe back without sedation, flunixin and DexSP",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("vision is grave", joined)
        self.assertIn("without anesthesia", joined)
        self.assertIn("flunixin", joined)
        self.assertIn("dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_neonate_not_swing_doxapram_atropine(self):
        b = analyze(
            "dog",
            "newborn puppy, swing to clear airway, doxapram and atropine for bradycardia",
        )
        loc = b["localization"].lower()
        self.assertIn("warm before you feed", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not swing the neonate", joined)
        self.assertIn("doxapram is not routine", joined)
        self.assertIn("atropine is not for neonatal bradycardia", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_fading_kitten_not_tube_feed_cold_or_runt_home(self):
        b = analyze(
            "cat",
            "fading kitten, hypothermic, tube feed formula, send home as small of the litter",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("warm before you feed", joined)
        self.assertIn("tube-feed a cold", joined)
        self.assertIn("small of the litter", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_mastitis_not_sore_milk_home_or_dexsp(self):
        b = analyze(
            "dog",
            "postpartum fever, mastitis, send home as sore milk, give DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("name the gland or the uterus", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a septic dam home as sore milk", joined)
        self.assertIn("dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_gangrenous_mastitis_is_surgery_tonight(self):
        b = analyze(
            "dog",
            "gangrenous mastitis, necrotic gland, pups still nursing, flunixin",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("gangrene is surgery tonight", joined)
        self.assertIn("nsaid", joined)
        self.assertIn("1% iodine", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_glaucoma_not_conjunctivitis_home_or_atropine(self):
        b = analyze(
            "dog",
            "acute glaucoma, red painful eye, send home as conjunctivitis, atropine",
        )
        loc = b["localization"].lower()
        self.assertIn("measure iop now", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send home as conjunctivitis", joined)
        self.assertIn("atropine", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_latanoprost_before_lens_or_anterior_luxation(self):
        b = analyze(
            "dog",
            "glaucoma, latanoprost, anterior lens luxation, lens not seen",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("check the lens before latanoprost", joined)
        self.assertIn("anterior luxation", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_glaucoma_no_latanoprost_default_or_ivt_gentamicin(self):
        b = analyze(
            "cat",
            "glaucoma, latanoprost, intravitreal gentamicin, DexSP",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("prostaglandin analogs are uncommon", joined)
        self.assertIn("intravitreal gentamicin is contraindicated in cats", joined)
        self.assertIn("dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_confirmed_uti_does_not_close_hyperca(self):
        b = analyze(
            "cat",
            "UTI confirmed, hypercalcemia, iCa high, tCa high, maybe lymphoma, DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("not an albumin artifact", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("confirmed uti is infection, not fic", joined)
        self.assertIn("uti does not close the calcium problem list", joined)
        self.assertIn("do not dexsp", joined)
        self.assertIn("image for caox", joined)
        self.assertNotIn("fic until culture", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_uveitis_not_conjunctivitis_home_or_steroid_on_ulcer(self):
        b = analyze(
            "cat",
            "anterior uveitis, aqueous flare, send home as conjunctivitis, atropine, high IOP, DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("typically low", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send uveitis home as conjunctivitis", joined)
        self.assertIn("do not atropine uveitis if iop is high", joined)
        self.assertIn("dexsp-only", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_anterior_lens_luxation_no_latanoprost_refer_tonight(self):
        b = analyze(
            "dog",
            "terrier anterior lens luxation latanoprost",
        )
        loc = b["localization"].lower()
        self.assertIn("look at the lens", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("no latanoprost", joined)
        self.assertIn("refer tonight", joined)
        self.assertIn("miosis traps", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_hyphema_is_a_sign_not_aspirin_or_red_eye_home(self):
        b = analyze(
            "dog",
            "hyphema, blood in the anterior chamber, send home as red eye, aspirin",
        )
        loc = b["localization"].lower()
        self.assertIn("sign, not a diagnosis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("hyphema is a sign, not a diagnosis", joined)
        self.assertIn("aspirin is contraindicated", joined)
        self.assertIn("do not send hyphema home as a red eye", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_claw_corneal_laceration_look_at_lens_no_lobby_yank(self):
        b = analyze(
            "dog",
            "cat claw in the eye, corneal laceration, seidel positive, yank the thorn, send home",
        )
        loc = b["localization"].lower()
        self.assertIn("look at the lens", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a leaking globe home", joined)
        self.assertIn("do not yank a deep", joined)
        self.assertIn("traumatic lens sarcoma", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_sudden_blind_not_sards_without_erg_or_book_pred(self):
        b = analyze(
            "dog",
            "sudden blindness, SARDS, give prednisolone, DexSP",
        )
        loc = b["localization"].lower()
        self.assertIn("name the space", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not call sudden blindness sards without an erg", joined)
        self.assertIn("do not harvest book pred 1.0", joined)
        self.assertIn("do not dexsp or copy book pred", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_enrofloxacin_and_hypertensive_rd(self):
        b = analyze(
            "cat",
            "went blind after enrofloxacin, retinal detachment, ivermectin",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("enrofloxacin", joined)
        self.assertIn("measure bp tonight", joined)
        self.assertIn("ivermectin", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_eyelid_margin_not_glue_and_home(self):
        b = analyze(
            "dog",
            "eyelid laceration, lid margin, glue the lid and send home, chlorhexidine in the eye",
        )
        loc = b["localization"].lower()
        self.assertIn("repair tonight", loc)
        self.assertIn("figure-of-eight", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not glue-and-home", joined)
        self.assertIn("chlorhexidine", joined)
        self.assertIn("stain the", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_alkali_splash_not_neutralize(self):
        b = analyze(
            "dog",
            "alkali splash in the eye, neutralize with boric acid ointment",
        )
        loc = b["localization"].lower()
        self.assertIn("lavage now", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not neutralize", joined)
        self.assertIn("minimum of 20 minutes", joined)
        self.assertIn("boric-acid", joined)
        self.assertNotIn("alkaline phosphatase", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_chem_eye_not_send_home_burning_or_steroid(self):
        b = analyze(
            "cat",
            "bleach in the eye, chemical keratitis, steroid drop, send home still burning",
        )
        loc = b["localization"].lower()
        self.assertIn("lavage now", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send home still burning", joined)
        self.assertIn("do not put a topical steroid", joined)
        self.assertIn("fluorescein after", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_alkaline_phosphatase_is_not_chem_eye(self):
        b = analyze("cat", "alkaline phosphatase high, no eye signs")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("lavage now", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertNotIn("do not neutralize", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_melting_ulcer_not_steroid_or_home(self):
        b = analyze(
            "dog",
            "melting corneal ulcer, keratomalacia, steroid drop, send home",
        )
        loc = b["localization"].lower()
        self.assertIn("refer tonight", loc)
        self.assertNotIn("cat-claw or corneal laceration", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a melting eye home", joined)
        self.assertIn("do not steroid a melt", joined)
        self.assertIn("cytology and culture", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_descemetocele_not_grid_or_burr(self):
        b = analyze(
            "cat",
            "descemetocele, deep stromal ulcer, grid keratotomy, diamond burr, enrofloxacin, triple antibiotic",
        )
        loc = b["localization"].lower()
        self.assertIn("descemetocele", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not grid a melt", joined)
        self.assertIn("keratotomy is not recommended in cats", joined)
        self.assertIn("enrofloxacin", joined)
        self.assertIn("bnp", joined)
        self.assertNotIn("fic until culture", joined)
        self.assertNotIn("sporadic cystitis", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_indolent_ulcer_not_a_melt_and_no_grid_in_cat(self):
        b = analyze(
            "cat",
            "indolent ulcer, SCCED, loose epithelial lip, grid keratotomy",
        )
        loc = b["localization"].lower()
        self.assertIn("loose epithelial lip", loc)
        self.assertIn("not a melt", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not grid a cat", joined)
        self.assertIn("sequestrum", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_boxer_ulcer_not_antibiotic_alone(self):
        b = analyze(
            "dog",
            "Boxer ulcer, recurrent corneal erosion, steroid drop",
        )
        loc = b["localization"].lower()
        self.assertIn("loose epithelial lip", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("antibiotic drops alone", joined)
        self.assertIn("do not put a steroid", joined)
        self.assertIn("diamond burr or grid", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_sequestrum_not_pick_or_grid_or_home(self):
        b = analyze(
            "cat",
            "corneal sequestrum, black corneal plaque, pick the plaque, grid keratotomy, send home it will slough",
        )
        loc = b["localization"].lower()
        self.assertIn("keratectomy conversation", loc)
        self.assertIn("depth may be hidden", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not pick or peel", joined)
        self.assertIn("do not grid a cat", joined)
        self.assertIn("it will slough", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_sequestrum_is_not_this_disease(self):
        b = analyze("dog", "corneal sequestrum, brown corneal plaque")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("cat disease", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_dendritic_fhv_no_steroid_no_grid(self):
        b = analyze(
            "cat",
            "dendritic ulcer, FHV, sneezing, steroid drop, grid keratotomy",
        )
        loc = b["localization"].lower()
        self.assertIn("dendritic", loc)
        self.assertIn("uri supports", loc)
        self.assertIn("pcr is not required", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not put a steroid", joined)
        self.assertIn("do not grid a cat", joined)
        self.assertIn("l-lysine 500", joined)
        self.assertIn("antiviral", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_fhv_melt_not_just_herpes(self):
        b = analyze(
            "cat",
            "geographic ulcer, herpes keratitis, melting ulcer, send home just herpes",
        )
        loc = b["localization"].lower()
        self.assertIn("coalesced dendrites", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("just herpes", joined)
        self.assertIn("melting", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_dendritic_is_cat_conversation(self):
        b = analyze("dog", "dendritic ulcer, feline herpesvirus")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("cat conversation", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_eosinophilic_keratitis_stain_first_no_steroid_on_ulcer(self):
        b = analyze(
            "cat",
            "eosinophilic keratitis, pink corneal plaque, ulcer, steroid drop, valacyclovir, megestrol",
        )
        loc = b["localization"].lower()
        self.assertIn("pink-to-white", loc)
        self.assertIn("cytology", loc)
        self.assertIn("not a brown sequestrum", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("stain first", joined)
        self.assertIn("do not put a steroid", joined)
        self.assertIn("valacyclovir is contraindicated", joined)
        self.assertIn("megestrol is not the night default", joined)
        self.assertNotIn("do not pick or peel", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_pink_plaque_is_not_lip_rodent_ulcer(self):
        b = analyze(
            "cat",
            "white corneal plaque, proliferative keratitis, rodent ulcer of the lip, send home as conjunctivitis",
        )
        loc = b["localization"].lower()
        self.assertIn("not a lip rodent ulcer", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("skin complex", joined)
        self.assertIn("conjunctivitis", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_eosinophilic_keratitis_is_cat_conversation(self):
        b = analyze("dog", "eosinophilic keratitis, pink corneal plaque")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("cat conversation", joined)
        self.assertIn("pannus", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_lip_eosinophilic_ulcer_does_not_open_fek(self):
        b = analyze("cat", "rodent ulcer of the lip, eosinophilic granuloma, no eye signs")
        loc = (b.get("localization") or "").lower()
        self.assertNotIn("eosinophilic keratitis", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_kcs_stt_before_drops_not_conjunctivitis(self):
        b = analyze(
            "dog",
            "dry eye, KCS, mucopurulent ocular discharge, ulcer, steroid drop, send home as conjunctivitis",
        )
        loc = b["localization"].lower()
        self.assertIn("stt before any drops", loc)
        self.assertIn("not conjunctivitis until the strip", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send a sticky red", joined)
        self.assertIn("do not put a steroid combo", joined)
        self.assertIn("csa 0.2", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_kcs_atropine_and_skin_tacrolimus_and_excise_gland(self):
        b = analyze(
            "dog",
            "keratoconjunctivitis sicca, atropine, dermatologic tacrolimus, cherry eye, excise the gland",
        )
        loc = b["localization"].lower()
        self.assertIn("aqueous tear deficiency", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("atropine dries tears", joined)
        self.assertIn("dermatologic tacrolimus", joined)
        self.assertIn("do not excise", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_kcs_is_uncommon_fhv_on_list(self):
        b = analyze("cat", "dry eye, KCS, lusterless cornea")
        loc = b["localization"].lower()
        self.assertIn("cats uncommon", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("fhv scarring", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_kcs_melt_not_home(self):
        b = analyze(
            "dog",
            "KCS, melting ulcer, send home still melting",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("do not send a melting dry eye home", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cherry_eye_replace_do_not_excise(self):
        b = analyze(
            "dog",
            "cherry eye, red mass third eyelid, excise the gland, send home dry it will go back",
        )
        loc = b["localization"].lower()
        self.assertIn("prolapsed nictitans gland", loc)
        self.assertIn("do not excise", loc)
        self.assertIn("other eye", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not excise", joined)
        self.assertIn("it will go back", joined)
        self.assertIn("lubricate", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_cherry_eye_still_do_not_excise(self):
        b = analyze("cat", "cherry eye, nictitans gland prolapse")
        loc = b["localization"].lower()
        self.assertIn("tear gland", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("uncommon", joined)
        self.assertIn("do not excise", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dacryocystitis_not_conjunctivitis_check_tooth(self):
        b = analyze(
            "dog",
            "dacryocystitis, epiphora, medial canthus swell, send home as conjunctivitis, carnassial",
        )
        loc = b["localization"].lower()
        self.assertIn("lacrimal sac", loc)
        self.assertIn("carnassial", loc)
        self.assertIn("not conjunctivitis until the duct is open", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not send dacryocystitis home as conjunctivitis", joined)
        self.assertIn("jones", joined)
        self.assertIn("carnassial", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dacryo_no_harvest_nylon_or_flush_melt(self):
        b = analyze(
            "dog",
            "nasolacrimal obstruction, fistula at medial eyelid, 2-0 nylon, flush every 3 days, melting ulcer",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("nylon", joined)
        self.assertIn("do not flush a melting", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_orbital_cellulitis_not_conjunctivitis_lubricate(self):
        b = analyze(
            "dog",
            "orbital cellulitis, pain opening the mouth, exophthalmos, send home as conjunctivitis",
        )
        loc = b["localization"].lower()
        self.assertIn("pain on opening the mouth", loc)
        self.assertIn("not conjunctivitis", loc)
        self.assertIn("not proptosis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("lubricate", joined)
        self.assertIn("last molar", joined)
        self.assertIn("do not send orbital cellulitis home as conjunctivitis", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_painless_exophthalmos_not_default_cellulitis(self):
        b = analyze(
            "dog",
            "retrobulbar mass, painless exophthalmos, no pain opening the mouth",
        )
        loc = b["localization"].lower()
        self.assertIn("exophthalmos", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("painless exophthalmos is not default cellulitis", joined)
        self.assertIn("neoplasia", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_mmm_do_not_pry_draw_2m_first(self):
        b = analyze(
            "dog",
            "masticatory myositis, cannot open the jaw, pry the jaw open, steroid before titer, send home as picky",
        )
        loc = b["localization"].lower()
        self.assertIn("type 2m", loc)
        self.assertIn("limbs spared", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not pry the jaw", joined)
        self.assertIn("2m antibody before steroids", joined)
        self.assertIn("picky", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_trismus_with_risus_is_tetanus_not_mmm_only(self):
        b = analyze("dog", "trismus, risus sardonicus, sawhorse")
        loc = b["localization"].lower()
        self.assertIn("tetanus", loc)
        self.assertIn("not isolated masticatory", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("tetanus", joined)
        self.assertIn("not mmm", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_tetanus_risus_sawhorse_quiet_dark_not_just_lockjaw(self):
        b = analyze(
            "dog",
            "puncture wound, risus sardonicus, sawhorse, pry the jaw, send home as just lockjaw",
        )
        loc = b["localization"].lower()
        self.assertIn("tetanus", loc)
        self.assertIn("consciousness", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("quiet", joined)
        self.assertIn("do not pry the jaw", joined)
        self.assertIn("just lockjaw", joined)
        self.assertIn("plumb", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_tetanus_cat_can_get_it_no_harvest_iu(self):
        b = analyze(
            "cat",
            "tetanus, 500 IU antitoxin, metronidazole table, DexSP, AKI",
        )
        loc = b["localization"].lower()
        self.assertIn("tetanus", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("cats can get tetanus", joined)
        self.assertIn("do not harvest antitoxin", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_isolated_mmm_is_not_called_tetanus(self):
        b = analyze(
            "dog",
            "masticatory myositis, cannot open the jaw, temporalis swollen, limbs normal",
        )
        loc = b["localization"].lower()
        self.assertIn("type 2m", loc)
        self.assertNotIn("tetanospasmin", loc)
        joined = " ".join(b["hard_stops"] + b["do_next"]).lower()
        self.assertIn("2m antibody", joined)
        self.assertNotIn("just lockjaw", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cherry_eye_third_eyelid_is_not_tetanus(self):
        b = analyze("dog", "cherry eye, red mass at third eyelid")
        loc = b["localization"].lower()
        self.assertNotIn("tetanospasmin", loc)
        self.assertNotIn("sawhorse", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_tick_paralysis_search_coat_not_just_tired(self):
        b = analyze(
            "dog",
            "tick paralysis, Dermacentor, ascending flaccid, send home as just tired",
        )
        loc = b["localization"].lower()
        self.assertIn("flaccid", loc)
        self.assertIn("not tetanus", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("search the whole coat", joined)
        self.assertIn("just tired", joined)
        self.assertIn("not commercial in the us", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_botulism_carrion_no_harvest_iu(self):
        b = analyze(
            "dog",
            "botulism, spoiled food, flaccid paralysis, type C 10000 units",
        )
        loc = b["localization"].lower()
        self.assertIn("botulism", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("carrion", joined)
        self.assertIn("do not harvest", joined)
        self.assertIn("aminoglycoside", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_flaccid_is_not_called_tetanus(self):
        b = analyze("cat", "ascending flaccid tetraparesis, search the coat")
        loc = b["localization"].lower()
        self.assertIn("flaccid", loc)
        self.assertNotIn("tetanospasmin", loc)
        joined = " ".join(b["hard_stops"]).lower()
        self.assertIn("flaccid, not tetanus", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_lyme_tick_preventative_is_not_tick_paralysis(self):
        b = analyze("dog", "Lyme vaccine, tick preventative, no weakness")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("flaccid ascending", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_apn_coonhound_steroids_not_helpful(self):
        b = analyze(
            "dog",
            "coonhound paralysis, raccoon bite last week, DexSP, send home as just tired",
        )
        loc = b["localization"].lower()
        self.assertIn("apn", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("steroids are not helpful", joined)
        self.assertIn("just tired", joined)
        self.assertIn("search the coat", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_fulminant_mg_no_harvest_tensilon(self):
        b = analyze(
            "dog",
            "fulminant myasthenia, megaesophagus, Tensilon 0.2 mg/kg, send home as just GI",
        )
        loc = b["localization"].lower()
        self.assertIn("myasthenia", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not harvest tensilon", joined)
        self.assertIn("just gi", joined)
        self.assertIn("upright feeding", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_raw_chicken_flaccid_offers_apn(self):
        b = analyze("dog", "raw chicken, flaccid tetraparesis, Campylobacter")
        loc = b["localization"].lower()
        self.assertIn("apn", loc)
        joined = " ".join(b["do_next"] + b["hard_stops"]).lower()
        self.assertIn("raw chicken", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_bunny_hop_is_not_apn(self):
        b = analyze("dog", "polyradiculoneuritis, puppy bunny-hop, pelvic rigidity")
        joined = " ".join(b["hard_stops"]).lower()
        self.assertIn("protozoal", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_trigem_dropped_jaw_cannot_close_not_mmm(self):
        b = analyze(
            "dog",
            "dropped jaw, cannot close the mouth, pry the jaw, send home as picky",
        )
        loc = b["localization"].lower()
        self.assertIn("cannot close", loc)
        self.assertIn("not masticatory", loc)
        self.assertNotIn("type 2m", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not pry the jaw", joined)
        self.assertIn("picky", joined)
        self.assertIn("3–4 weeks", joined)
        self.assertIn("fluids", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cannot_open_is_still_mmm_not_trigem(self):
        b = analyze(
            "dog",
            "masticatory myositis, cannot open the jaw, temporalis swollen, limbs normal",
        )
        loc = b["localization"].lower()
        self.assertIn("type 2m", loc)
        self.assertNotIn("trigeminal neuritis", loc)
        self.assertNotIn("cannot close", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_trigem_cat_uncommon_no_harvest_steroid(self):
        b = analyze(
            "cat",
            "trigeminal neuritis, dropped jaw, steroid table, DexSP, AKI",
        )
        loc = b["localization"].lower()
        self.assertIn("trigeminal", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("uncommon", joined)
        self.assertIn("do not harvest a steroid table", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_2m_elisa_serum_before_steroids_not_ruleout(self):
        b = analyze(
            "dog",
            "2M ELISA, already on steroids 10 days, negative titer, send home as picky",
        )
        loc = b["localization"].lower()
        self.assertIn("type 2m", loc)
        self.assertIn("2m antibody before steroids", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("not a rule-out", joined)
        self.assertIn("serum", joined)
        self.assertIn("freeze", joined)
        self.assertIn("picky", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_2m_do_not_harvest_titer_or_follow_or_frontalis(self):
        b = analyze(
            "dog",
            "2M titer, follow the titer for response, 1:500, biopsy frontalis",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not harvest 2m titer cutoffs", joined)
        self.assertIn("do not follow the 2m titer", joined)
        self.assertIn("do not biopsy the frontalis", joined)
        self.assertIn("not prognosis", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_facial_cannot_blink_not_horner_or_conjunctivitis(self):
        b = analyze(
            "dog",
            "cannot blink, facial paralysis, drooping lip, send home as conjunctivitis",
        )
        loc = b["localization"].lower()
        self.assertIn("cannot blink", loc)
        self.assertIn("not horner", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("lubricate", joined)
        self.assertIn("stt", joined)
        self.assertIn("conjunctivitis", joined)
        self.assertIn("look in the ear", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_facial_horner_is_the_ear_no_steroid_table(self):
        b = analyze(
            "dog",
            "facial paralysis, Horner, cannot blink, steroid table, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("horner can blink", joined)
        self.assertIn("the ear", joined)
        self.assertIn("do not harvest a steroid table", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_facial_cat_uncommon_not_dropped_jaw(self):
        b = analyze("cat", "idiopathic facial paralysis, cannot blink, polyp")
        loc = b["localization"].lower()
        self.assertIn("facial paralysis", loc)
        self.assertNotIn("cannot close", loc)
        joined = " ".join(b["do_next"] + b["hard_stops"]).lower()
        self.assertIn("uncommon", joined)
        self.assertIn("polyp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_polyp_cat_stertor_look_both_not_just_uri(self):
        b = analyze(
            "cat",
            "young cat, stertor, nasopharyngeal polyp, send home as just URI",
        )
        loc = b["localization"].lower()
        self.assertIn("polyp", loc)
        self.assertIn("soft palate", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("both ears", joined)
        self.assertIn("just uri", joined)
        self.assertIn("call it cancer", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_polyp_traction_no_steroid_table(self):
        b = analyze(
            "cat",
            "aural polyp, retract the soft palate, VBO, steroid table, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not harvest a steroid table", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIn("septate", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_polyp_dog_rare_not_cat_script(self):
        b = analyze("dog", "inflammatory polyp, retract the soft palate")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("nasopharyngeal / aural inflammatory polyp until you look", loc)
        joined = " ".join(b["do_next"] + b["sources"]).lower()
        self.assertIn("uncommon in dogs", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_horner_isolated_can_blink_stain_look_ear(self):
        b = analyze(
            "dog",
            "isolated Horner, miosis, ptosis, third eyelid, send home as just a small pupil",
        )
        loc = b["localization"].lower()
        self.assertIn("can blink", loc)
        self.assertIn("not cn vii", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("stain", joined)
        self.assertIn("both ears", joined)
        self.assertIn("just a small pupil", joined)
        self.assertIn("do not harvest a first", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_horner_plexus_not_idiopathic(self):
        b = analyze(
            "dog",
            "Horner, brachial plexus avulsion, flaccid thoracic limb, cutaneous trunci lost, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("plexus", joined)
        self.assertIn("not idiopathic", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_horner_phenylephrine_no_minute_table(self):
        b = analyze("dog", "Horner, phenylephrine test")
        joined = " ".join(b["do_not"] + b["sources"]).lower()
        self.assertIn("phenylephrine", joined)
        self.assertIn("minute", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_anisocoria_big_pupil_not_horner(self):
        b = analyze(
            "dog",
            "anisocoria, dilated pupil, vision intact, send home as just a funny pupil",
        )
        loc = b["localization"].lower()
        self.assertIn("which pupil is wrong", loc)
        self.assertIn("not horner", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("iris atrophy", joined)
        self.assertIn("just a funny pupil", joined)
        self.assertIn("do not call the big pupil horner", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dysautonomia_not_single_eye_no_pilocarpine_table(self):
        b = analyze(
            "dog",
            "dysautonomia, bilateral mydriasis, pilocarpine, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("not a single-eye", joined)
        self.assertIn("pilocarpine", joined)
        self.assertIn("grave", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_optic_neuritis_dilated_fixed_not_cortex(self):
        b = analyze(
            "dog",
            "sudden blind, dilated and fixed pupils, optic neuritis, send home",
        )
        loc = b["localization"].lower()
        self.assertIn("not cortex", loc)
        self.assertIn("retrobulbar", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("pred 1.0", joined)
        self.assertIn("meningoencephalitis", joined)
        self.assertIn("normal-looking disc", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_optic_neuritis_no_pred_table_azotemic(self):
        b = analyze(
            "dog",
            "optic neuritis, pred 1.0, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("do not harvest book pred 1.0", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cortical_postictal_blind_normal_pupils_not_sards(self):
        b = analyze(
            "dog",
            "post-ictal blindness, normal pupils, send home as SARDS",
        )
        loc = b["localization"].lower()
        self.assertIn("cortical", loc)
        self.assertIn("normal pupils", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("call it sards", joined)
        self.assertIn("optic neuritis", joined)
        self.assertIn("post-ictal hour clock", joined)
        self.assertIn("home as sards", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cortical_forebrain_circle_toward_no_dexsp_stroke(self):
        b = analyze(
            "dog",
            "cortical blindness, normal PLR, circling, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("circle toward", joined)
        self.assertIn("do not dexsp cortical blindness as a stroke", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_seizure_dilated_fixed_blind_is_not_cortex_first(self):
        b = analyze(
            "dog",
            "seizure, sudden blind, dilated and fixed pupils, optic neuritis",
        )
        loc = (b["localization"] or "").lower()
        self.assertIn("not cortex", loc)
        self.assertNotIn("cortical / post-geniculate blindness", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_papilledema_not_blindness(self):
        b = analyze("dog", "optic neuritis, papilledema")
        joined = " ".join(b["do_not"] + b["do_next"]).lower()
        self.assertIn("papilledema", joined)
        self.assertIn("spares vision", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_hypertensive_rd_not_sards_not_lasix(self):
        b = analyze(
            "cat",
            "sudden blind, retinal detachment, hypertension, Lasix, send home as SARDS",
        )
        loc = b["localization"].lower()
        self.assertIn("systemic hypertension", loc)
        self.assertIn("not pulmonary htn", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("call it sards", joined)
        self.assertIn("do not lasix systemic hypertension", joined)
        self.assertIn("amlodipine / telmisartan", joined)
        self.assertIn("home as sards", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_htn_kidney_no_cookbook_azotemic(self):
        b = analyze(
            "dog",
            "systemic hypertension, CKD, DexSP, AKI, amlodipine",
        )
        loc = b["localization"].lower()
        self.assertIn("almost always secondary", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("kidney first", joined)
        self.assertIn("do not invent a first-line cookbook", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIn("harvest amlodipine or sildenafil", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_pulmonary_htn_is_not_systemic_script(self):
        b = analyze("dog", "pulmonary hypertension, sildenafil")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("acute systemic hypertension", loc)
        self.assertIn("pulmonary hypertension", loc)
        self.assertIn("not systemic htn", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertNotIn("amlodipine / telmisartan conversation", joined)
        self.assertIn("harvest sildenafil or tadalafil", joined)
        self.assertIn("pulmonary-artery drug", joined)
        self.assertIn("echo estimates the pressure", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_heartworm_exertional_syncope_is_ph_not_seizure(self):
        b = analyze(
            "dog",
            "heartworm, syncope after exercise, send home as a seizure, Lasix",
        )
        loc = b["localization"].lower()
        self.assertIn("pulmonary hypertension", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("call syncope a seizure", joined)
        self.assertIn("adulticide", joined)
        self.assertIn("do not lasix pulmonary hypertension", joined)
        self.assertIn("home as a seizure", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_caval_pigmenturia_extract_not_imha_not_melarsomine(self):
        b = analyze(
            "dog",
            "caval syndrome, pigmenturia, yank the worms, send home as a UTI",
        )
        loc = b["localization"].lower()
        self.assertIn("caval syndrome", loc)
        self.assertIn("mechanical hemolysis", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("equal-sign", joined)
        self.assertIn("right-jugular", joined)
        self.assertIn("not imha", joined)
        self.assertIn("home as a uti", joined)
        self.assertIn("lacerates worms", joined)
        self.assertIn("dump a melarsomine", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_heartworm_no_melarsomine(self):
        b = analyze(
            "cat",
            "heartworm, melarsomine, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("not recommended in cats", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_cat_hard_not_just_asthma_ag_can_lie(self):
        b = analyze(
            "cat",
            "feline heartworm, HARD, asthma, send home, open-mouth",
        )
        loc = b["localization"].lower()
        self.assertIn("not just asthma", loc)
        self.assertIn("not a dog caval", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("just asthma", joined)
        self.assertIn("negative antigen does not rule it out", joined)
        self.assertIn("home as just asthma", joined)
        self.assertIn("one-worm-death", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_dog_heartworm_is_not_feline_hard(self):
        b = analyze("dog", "heartworm antigen positive, wellness preventative")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("feline hard", loc)
        self.assertNotIn("not just asthma", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_heartworm_wellness_is_not_caval(self):
        b = analyze("dog", "heartworm antigen positive, wellness preventative")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("caval syndrome", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_ph_amlodipine_is_the_other_list(self):
        b = analyze(
            "dog",
            "cor pulmonale, amlodipine, DexSP, AKI",
        )
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("amlodipine is systemic hypertension", joined)
        self.assertIn("still no dexsp", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_tbi_cushing_reflex_is_not_amlodipine(self):
        b = analyze("dog", "TBI, Cushing reflex, hypertension, bradycardia")
        loc = (b["localization"] or "").lower()
        self.assertIn("cushing reflex", loc)
        self.assertNotIn("acute systemic hypertension", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_wellness_bp_not_a_screen(self):
        b = analyze("cat", "wellness, high blood pressure, no TOD")
        joined = " ".join(b["hard_stops"] + b["do_not"]).lower()
        self.assertIn("not a wellness screen", joined)
        self.assertIn("bouncing cuff", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_iris_atrophy_not_cn_iii_crash(self):
        b = analyze("dog", "old dog, iris atrophy, scalloped pupil, anisocoria")
        joined = " ".join(b["do_not"] + b["do_next"]).lower()
        self.assertIn("cn iii emergency", joined)
        self.assertIn("vision stays", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_miosis_ulcer_alone_is_not_horner(self):
        b = analyze("dog", "miosis, corneal ulcer, painful eye")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("horner (sympathetic)", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_polyp_wheeze_alone_is_not_stertor(self):
        b = analyze("cat", "expiratory wheeze, coughing, asthma")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("nasopharyngeal / aural inflammatory polyp until you look", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_facial_swelling_is_not_cn_vii(self):
        b = analyze("dog", "facial swelling, hives, vaccine")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("cannot blink", loc)
        self.assertNotIn("cn vii", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_ophthalmic_trigeminal_nerve_is_not_dropped_jaw(self):
        b = analyze("dog", "ophthalmic branch of the trigeminal nerve, corneal ulcer")
        loc = (b["localization"] or "").lower()
        self.assertNotIn("trigeminal neuritis", loc)
        self.assertNotIn("cannot close", loc)
        self.assertIsNone(b["mg_per_kg"])

    def test_anesthesia_recovery_is_still_anesthesia(self):
        b = analyze(
            "dog",
            "brachycephalic under anesthesia, closed pop-off, oxygen flush non-rebreathing, send home still recovering",
        )
        loc = b["localization"].lower()
        self.assertIn("recovery is still anesthesia", loc)
        self.assertIn("dedicated anesthetist", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("do not oxygen-flush a non-rebreathing", joined)
        self.assertIn("closed pop-off is barotrauma", joined)
        self.assertIn("confirm the tube with etco2", joined)
        self.assertIsNone(b["mg_per_kg"])

    def test_anesthesia_acei_and_full_insulin_fasted(self):
        b = analyze(
            "cat",
            "ASA 3 induction, enalapril this morning, full insulin while fasted, no ETCO2",
        )
        loc = b["localization"].lower()
        self.assertIn("recovery is still anesthesia", loc)
        joined = " ".join(b["hard_stops"] + b["do_not"] + b["do_next"]).lower()
        self.assertIn("hold ace inhibitors", joined)
        self.assertIn("full insulin", joined)
        self.assertIn("confirm the tube with etco2", joined)
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

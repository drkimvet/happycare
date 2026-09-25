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
        self.assertIn("laryngeal paralysis", VERIF.lower())
        self.assertIn("radiographs are not diagnostic", VERIF.lower())
        self.assertIn("tracheotomy", VERIF.lower())
        self.assertIn("puppy hypoglycemia", VERIF.lower())
        self.assertIn("do not harvest printed 25%", VERIF.lower())
        self.assertIn("not an insulinoma puppy", VERIF.lower())
        self.assertIn("transfusion reaction", VERIF.lower())
        self.assertIn("stop the bag first", VERIF.lower())
        self.assertIn("no universal donor", VERIF.lower())
        self.assertIn("vestibular", VERIF.lower())
        self.assertIn("peripheral vs central before home", VERIF.lower())
        self.assertIn("stop metronidazole", VERIF.lower())
        self.assertIn("snakebite", VERIF.lower())
        self.assertIn("637–647", VERIF)
        self.assertIn("1–5 vials", VERIF)
        self.assertIn("do not ice, cut, suck, or tourniquet", VERIF.lower())
        self.assertIn("antivenom is the specific", VERIF.lower())
        self.assertIn("hepatic encephalopathy", VERIF.lower())
        self.assertIn("ammonia is not the diagnosis", VERIF.lower())
        self.assertIn("do not give benzodiazepines for hepatic encephalopathy", VERIF.lower())
        self.assertIn("book nac 50", VERIF.lower())
        self.assertIn("proptosis", VERIF.lower())
        self.assertIn("lubricate now", VERIF.lower())
        self.assertIn("do not send a dry globe home", VERIF.lower())
        self.assertIn("3-hour", VERIF.lower())
        self.assertIn("fading neonate", VERIF.lower())
        self.assertIn("do not swing", VERIF.lower())
        self.assertIn("warm before you feed", VERIF.lower())
        self.assertIn("atropine is not for neonatal bradycardia", VERIF.lower())
        self.assertIn("0.0002 mg/g", VERIF.lower())
        self.assertIn("mastitis", VERIF.lower())
        self.assertIn("name the gland or the uterus", VERIF.lower())
        self.assertIn("gangrene is surgery tonight", VERIF.lower())
        self.assertIn("sore milk", VERIF.lower())
        self.assertIn("measure iop now", VERIF.lower())
        self.assertIn("do not send home as conjunctivitis", VERIF.lower())
        self.assertIn("check the lens before latanoprost", VERIF.lower())
        self.assertIn("uti does not close calcium", VERIF.lower())
        self.assertIn("do not dexsp for maybe-lymphoma", VERIF.lower())
        self.assertIn("frozen or cold sst can raise ica", VERIF.lower())
        self.assertIn("iop is typically low", VERIF.lower())
        self.assertIn("prostaglandin analogs are contraindicated", VERIF.lower())
        self.assertIn("do not latanoprost an anterior luxation", VERIF.lower())
        self.assertIn("do not dexsp-only a cat", VERIF.lower())
        self.assertIn("hyphema is a sign", VERIF.lower())
        self.assertIn("25 g", VERIF.lower())
        self.assertIn("unit trap", VERIF.lower())
        self.assertIn("do not yank a deep", VERIF.lower())
        self.assertIn("do not send a leaking globe home", VERIF.lower())
        self.assertIn("do not call it sards without an erg", VERIF.lower())
        self.assertIn("no effective treatment has been reported", VERIF.lower())
        self.assertIn("pred 1.0", VERIF.lower())
        self.assertIn("enrofloxacin", VERIF.lower())
        self.assertIn("eyelid laceration", VERIF.lower())
        self.assertIn("figure-of-eight at the eyelid margin", VERIF.lower())
        self.assertIn("do not glue-and-home a margin cut", VERIF.lower())
        self.assertIn("lavage now", VERIF.lower())
        self.assertIn("do not chemically neutralize", VERIF.lower())
        self.assertIn("minimum of 20 minutes", VERIF.lower())
        self.assertIn("2 liters", VERIF.lower())
        self.assertIn("boric acid", VERIF.lower())
        self.assertIn("melting ulcer / descemetocele", VERIF.lower())
        self.assertIn("do not send a melting eye home", VERIF.lower())
        self.assertIn("do not grid a melt", VERIF.lower())
        self.assertIn("cytology and culture", VERIF.lower())
        self.assertIn("recovery is still anesthesia", VERIF.lower())
        self.assertIn("dedicated anesthetist", VERIF.lower())
        self.assertIn("do not oxygen-flush a non-rebreathing", VERIF.lower())
        self.assertIn("2013", VERIF.lower())
        self.assertIn("aaha 2024", VERIF.lower())
        self.assertIn("indolent", VERIF.lower())
        self.assertIn("do not grid a cat", VERIF.lower())
        self.assertIn("loose epithelial lip", VERIF.lower())
        self.assertIn("keratotomies are not recommended in cats", VERIF.lower())
        self.assertIn("feline corneal sequestrum", VERIF.lower())
        self.assertIn("do not pick or peel it", VERIF.lower())
        self.assertIn("unique to the cat", VERIF.lower())
        self.assertIn("dendritic", VERIF.lower())
        self.assertIn("no steroid", VERIF.lower())
        self.assertIn("l-lysine 500", VERIF.lower())
        self.assertIn("just herpes", VERIF.lower())
        self.assertIn("eosinophilic keratitis", VERIF.lower())
        self.assertIn("valacyclovir", VERIF.lower())
        self.assertIn("rodent ulcer", VERIF.lower())
        self.assertIn("cytology confirms", VERIF.lower())
        self.assertIn("stt before any drops", VERIF.lower())
        self.assertIn("dermatologic tacrolimus", VERIF.lower())
        self.assertIn("quantitative kcs", VERIF.lower())
        self.assertIn("do not excise", VERIF.lower())
        self.assertIn("cherry eye", VERIF.lower())
        self.assertIn("major tear gland", VERIF.lower())
        self.assertIn("it will go back", VERIF.lower())
        self.assertIn("pocket", VERIF.lower())
        self.assertIn("dacryocystitis", VERIF.lower())
        self.assertIn("carnassial", VERIF.lower())
        self.assertIn("jones test", VERIF.lower())
        self.assertIn("2–0 nylon", VERIF.lower())
        self.assertIn("orbital cellulitis", VERIF.lower())
        self.assertIn("pain on opening the mouth", VERIF.lower())
        self.assertIn("last molar", VERIF.lower())
        self.assertIn("not proptosis", VERIF.lower())
        self.assertIn("masticatory", VERIF.lower())
        self.assertIn("do not pry the jaw", VERIF.lower())
        self.assertIn("2m antibody", VERIF.lower())
        self.assertIn("2 mg/kg", VERIF.lower())
        self.assertIn("tetanus", VERIF.lower())
        self.assertIn("consciousness is not affected", VERIF.lower())
        self.assertIn("just lockjaw", VERIF.lower())
        self.assertIn("500–1000 iu", VERIF.lower())
        self.assertIn("tick paralysis", VERIF.lower())
        self.assertIn("botulism", VERIF.lower())
        self.assertIn("flaccid", VERIF.lower())
        self.assertIn("not commercially available in the us", VERIF.lower())
        self.assertIn("10 000 units", VERIF.lower())
        self.assertIn("polyradiculoneuritis", VERIF.lower())
        self.assertIn("steroids are not helpful", VERIF.lower())
        self.assertIn("fulminant", VERIF.lower())
        self.assertIn("0.1–0.2 mg/kg", VERIF.lower())
        self.assertIn("trigeminal", VERIF.lower())
        self.assertIn("cannot close", VERIF.lower())
        self.assertIn("3–4 weeks", VERIF.lower())
        self.assertIn("do not harvest a steroid table", VERIF.lower())
        self.assertIn("2m antibody elisa", VERIF.lower())
        self.assertIn("not a rule-out", VERIF.lower())
        self.assertIn("not frontalis", VERIF.lower())
        self.assertIn("1:100 / 1:500", VERIF.lower())
        self.assertIn("cannot blink", VERIF.lower())
        self.assertIn("horner can blink", VERIF.lower())
        self.assertIn("idiopathic facial", VERIF.lower())
        self.assertIn("6–8 week", VERIF.lower())
        self.assertIn("inflammatory polyp", VERIF.lower())
        self.assertIn("retract the soft palate", VERIF.lower())
        self.assertIn("just uri", VERIF.lower())
        self.assertIn("15–50%", VERIF.lower())
        self.assertIn("isolated horner", VERIF.lower())
        self.assertIn("they can still blink", VERIF.lower())
        self.assertIn("first- / second- / third-order", VERIF.lower())
        self.assertIn("2.5% / 10%", VERIF.lower())
        self.assertIn("which pupil is wrong", VERIF.lower())
        self.assertIn("iris atrophy", VERIF.lower())
        self.assertIn("dysautonomia", VERIF.lower())
        self.assertIn("0.05–0.1%", VERIF.lower())
        self.assertIn("dilated, fixed", VERIF.lower())
        self.assertIn("retrobulbar", VERIF.lower())
        self.assertIn("meningoencephalitis", VERIF.lower())
        self.assertIn("pred 1.0", VERIF.lower())
        self.assertIn("blindness with normal pupils", VERIF.lower())
        self.assertIn("postictal", VERIF.lower())
        self.assertIn("circle toward", VERIF.lower())
        self.assertIn("post-ictal hour clock", VERIF.lower())
        self.assertIn("acute systemic hypertension", VERIF.lower())
        self.assertIn("extremely rare", VERIF.lower())
        self.assertIn("amlodipine mg/kg", VERIF.lower())
        self.assertIn("do not lasix systemic hypertension", VERIF.lower())
        self.assertIn("pulmonary hypertension", VERIF.lower())
        self.assertIn("primary pulmonary hypertension is rare", VERIF.lower())
        self.assertIn("sildenafil 1–3", VERIF.lower())
        self.assertIn("tricuspid or pulmonary regurgitant", VERIF.lower())
        self.assertIn("caval syndrome", VERIF.lower())
        self.assertIn("hemoglobinuria", VERIF.lower())
        self.assertIn("melarsomine is not recommended in cats", VERIF.lower())
        self.assertIn("equal signs", VERIF.lower())
        self.assertIn("feline hard", VERIF.lower())
        self.assertIn("not just asthma", VERIF.lower())
        self.assertIn("negative antibody does not rule out", VERIF.lower())
        self.assertIn("pulmonary thromboembolism", VERIF.lower())
        self.assertIn("warfarin is not recommended", VERIF.lower())
        self.assertIn("no small-animal gold standard", VERIF.lower())
        self.assertIn("weeks after adulticide", VERIF.lower())
        self.assertIn("nephrotic syndrome", VERIF.lower())
        self.assertIn("upc > 2 suggests", VERIF.lower())
        self.assertIn("not definitive", VERIF.lower())
        self.assertIn("clopidogrel 1–4", VERIF.lower())
        self.assertIn("protein-losing enteropathy", VERIF.lower())
        self.assertIn("gi signs can be minimal", VERIF.lower())
        self.assertIn("hypocholesterolemia", VERIF.lower())
        self.assertIn("fenbendazole 50", VERIF.lower())
        self.assertIn("gallbladder mucocele", VERIF.lower())
        self.assertIn("do not do transhepatic cholecystocentesis", VERIF.lower())
        self.assertIn("ursodiol 15–25", VERIF.lower())
        self.assertIn("halo", VERIF.lower())
        self.assertIn("feline neutrophilic cholangitis", VERIF.lower())
        self.assertIn("do not starve", VERIF.lower())
        self.assertIn("pred 2–4", VERIF.lower())
        self.assertIn("not a lobby chop", VERIF.lower())
        self.assertIn("feline hepatic lipidosis", VERIF.lower())
        self.assertIn("do not hang dextrose", VERIF.lower())
        self.assertIn("do not give ursodiol in hl", VERIF.lower())
        self.assertIn("idiopathic", VERIF.lower())

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
        self.assertIn("`ddx-larpar`", MACRO)
        self.assertIn("`dc-larpar`", MACRO)
        self.assertIn("`ddx-hypogly`", MACRO)
        self.assertIn("`dc-hypogly`", MACRO)
        self.assertIn("`ddx-txrxn`", MACRO)
        self.assertIn("`dc-txrxn`", MACRO)
        self.assertIn("`ddx-vest`", MACRO)
        self.assertIn("`dc-vest`", MACRO)
        self.assertIn("`ddx-snake`", MACRO)
        self.assertIn("`dc-snake`", MACRO)
        self.assertIn("`ddx-he`", MACRO)
        self.assertIn("`dc-he`", MACRO)
        self.assertIn("`ddx-propto`", MACRO)
        self.assertIn("`dc-propto`", MACRO)
        self.assertIn("`ddx-neonate`", MACRO)
        self.assertIn("`dc-neonate`", MACRO)
        self.assertIn("`ddx-mastitis`", MACRO)
        self.assertIn("`dc-mastitis`", MACRO)
        self.assertIn("`ddx-glaucoma`", MACRO)
        self.assertIn("`dc-glaucoma`", MACRO)
        self.assertIn("`ddx-hyperca`", MACRO)
        self.assertIn("`dc-hyperca`", MACRO)
        self.assertIn("`dc-uti`", MACRO)
        self.assertIn("uti does not close hypercalcemia", MACRO.lower())
        self.assertIn("`ddx-uveitis`", MACRO)
        self.assertIn("`dc-uveitis`", MACRO)
        self.assertIn("`ddx-lenslux`", MACRO)
        self.assertIn("`dc-lenslux`", MACRO)
        self.assertIn("latanoprost / miotics", MACRO.lower())
        self.assertIn("`ddx-hyphema`", MACRO)
        self.assertIn("`dc-hyphema`", MACRO)
        self.assertIn("`ddx-corneal`", MACRO)
        self.assertIn("`dc-corneal`", MACRO)
        self.assertIn("hyphema is a sign, not a diagnosis", MACRO.lower())
        self.assertIn("`ddx-sards`", MACRO)
        self.assertIn("`dc-sards`", MACRO)
        self.assertIn("do not: call it sards without an erg", MACRO.lower())
        self.assertIn("`ddx-eyelid`", MACRO)
        self.assertIn("`dc-eyelid`", MACRO)
        self.assertIn("glue-and-home a margin cut", MACRO.lower())
        self.assertIn("`ddx-chemeye`", MACRO)
        self.assertIn("`dc-chemeye`", MACRO)
        self.assertIn("do not: neutralize", MACRO.lower())
        self.assertIn("`ddx-melt`", MACRO)
        self.assertIn("`dc-melt`", MACRO)
        self.assertIn("do not: send a melting eye home", MACRO.lower())
        self.assertIn("`ddx-anes`", MACRO)
        self.assertIn("`dc-anes`", MACRO)
        self.assertIn("recovery is still anesthesia", MACRO.lower())
        self.assertIn("`ddx-indolent`", MACRO)
        self.assertIn("`dc-indolent`", MACRO)
        self.assertIn("do not: grid a cat", MACRO.lower())
        self.assertIn("`ddx-seq`", MACRO)
        self.assertIn("`dc-seq`", MACRO)
        self.assertIn("do not: pick or peel it", MACRO.lower())
        self.assertIn("`ddx-fhv`", MACRO)
        self.assertIn("`dc-fhv`", MACRO)
        self.assertIn("do not: steroid a stain-positive / fhv ulcer", MACRO.lower())
        self.assertIn("`ddx-fek`", MACRO)
        self.assertIn("`dc-fek`", MACRO)
        self.assertIn("do not: steroid a stain-positive cornea", MACRO.lower())
        self.assertIn("`ddx-kcs`", MACRO)
        self.assertIn("`dc-kcs`", MACRO)
        self.assertIn("do not: send home as conjunctivitis", MACRO.lower())
        self.assertIn("`ddx-cherry`", MACRO)
        self.assertIn("`dc-cherry`", MACRO)
        self.assertIn("do not: excise it", MACRO.lower())
        self.assertIn("`ddx-dacryo`", MACRO)
        self.assertIn("`dc-dacryo`", MACRO)
        self.assertIn("do not: send home as conjunctivitis", MACRO.lower())
        self.assertIn("`ddx-orbit`", MACRO)
        self.assertIn("`dc-orbit`", MACRO)
        self.assertIn("do not: send home as conjunctivitis", MACRO.lower())
        self.assertIn("`ddx-mmm`", MACRO)
        self.assertIn("`dc-mmm`", MACRO)
        self.assertIn("do not: pry the jaw open", MACRO.lower())
        self.assertIn("`ddx-tetanus`", MACRO)
        self.assertIn("`dc-tetanus`", MACRO)
        self.assertIn("do not: pry the jaw open", MACRO.lower())
        self.assertIn("just lockjaw", MACRO.lower())
        self.assertIn("`ddx-tick`", MACRO)
        self.assertIn("`dc-tick`", MACRO)
        self.assertIn("`ddx-botul`", MACRO)
        self.assertIn("`dc-botul`", MACRO)
        self.assertIn("search the whole coat", MACRO.lower())
        self.assertIn("just tired", MACRO.lower())
        self.assertIn("`ddx-apn`", MACRO)
        self.assertIn("`dc-apn`", MACRO)
        self.assertIn("`ddx-mg`", MACRO)
        self.assertIn("`dc-mg`", MACRO)
        self.assertIn("steroids are not helpful", MACRO.lower())
        self.assertIn("just gi", MACRO.lower())
        self.assertIn("`ddx-trigem`", MACRO)
        self.assertIn("`dc-trigem`", MACRO)
        self.assertIn("cannot close", MACRO.lower())
        self.assertIn("send home as picky", MACRO.lower())
        self.assertIn("`ddx-2m`", MACRO)
        self.assertIn("`dc-2m`", MACRO)
        self.assertIn("harvest 1:100 / 1:500", MACRO.lower())
        self.assertIn("post-steroid negative", MACRO.lower())
        self.assertIn("`ddx-face`", MACRO)
        self.assertIn("`dc-face`", MACRO)
        self.assertIn("horner can blink", MACRO.lower())
        self.assertIn("just a droopy face", MACRO.lower())
        self.assertIn("`ddx-polyp`", MACRO)
        self.assertIn("`dc-polyp`", MACRO)
        self.assertIn("just uri", MACRO.lower())
        self.assertIn("retract the soft palate", MACRO.lower())
        self.assertIn("`ddx-horner`", MACRO)
        self.assertIn("`dc-horner`", MACRO)
        self.assertIn("they can blink", MACRO.lower())
        self.assertIn("just a small pupil", MACRO.lower())
        self.assertIn("`ddx-aniso`", MACRO)
        self.assertIn("`dc-aniso`", MACRO)
        self.assertIn("just a funny pupil", MACRO.lower())
        self.assertIn("which pupil is wrong", MACRO.lower())
        self.assertIn("`ddx-optic`", MACRO)
        self.assertIn("`dc-optic`", MACRO)
        self.assertIn("not cortex", MACRO.lower())
        self.assertIn("normal disc", MACRO.lower())
        self.assertIn("`ddx-cortex`", MACRO)
        self.assertIn("`dc-cortex`", MACRO)
        self.assertIn("post-ictal hour clock", MACRO.lower())
        self.assertIn("just-seized blind dog", MACRO.lower())
        self.assertIn("`ddx-htn`", MACRO)
        self.assertIn("`dc-htn`", MACRO)
        self.assertIn("bouncing cuff", MACRO.lower())
        self.assertIn("not a water-pill", MACRO.lower())
        self.assertIn("`ddx-phtn`", MACRO)
        self.assertIn("`dc-phtn`", MACRO)
        self.assertIn("not a pa catheter", MACRO.lower())
        self.assertIn("not the same as high blood pressure", MACRO.lower())
        self.assertIn("`ddx-caval`", MACRO)
        self.assertIn("`dc-caval`", MACRO)
        self.assertIn("not a simple bladder infection", MACRO.lower())
        self.assertIn("yank and lacerate", MACRO.lower())
        self.assertIn("`ddx-hard`", MACRO)
        self.assertIn("`dc-hard`", MACRO)
        self.assertIn("not a dog arsenic", MACRO.lower())
        self.assertIn("both can lie", MACRO.lower())
        self.assertIn("`ddx-pte`", MACRO)
        self.assertIn("`dc-pte`", MACRO)
        self.assertIn("not the same as a clot in the back legs", MACRO.lower())
        self.assertIn("use warfarin", MACRO.lower())
        self.assertIn("`ddx-pln`", MACRO)
        self.assertIn("`dc-pln`", MACRO)
        self.assertIn("not “just a liver problem”", MACRO.lower())
        self.assertIn("treat upc > 2 as proof", MACRO.lower())
        self.assertIn("`ddx-ple`", MACRO)
        self.assertIn("`dc-ple`", MACRO)
        self.assertIn("losing protein through the gut", MACRO.lower())
        self.assertIn("weeks-long diet trial", MACRO.lower())
        self.assertIn("`ddx-gbm`", MACRO)
        self.assertIn("`dc-gbm`", MACRO)
        self.assertIn("not “just hepatitis”", MACRO.lower())
        self.assertIn("cholecystocentesis if mucocele is suspected", MACRO.lower())
        self.assertIn("`ddx-cchs`", MACRO)
        self.assertIn("`dc-cchs`", MACRO)
        self.assertIn("not a dog gallbladder", MACRO.lower())
        self.assertIn("dexsp / pred as the night plan", MACRO.lower())
        self.assertIn("`ddx-hl`", MACRO)
        self.assertIn("`dc-hl`", MACRO)
        self.assertIn("just picky", MACRO.lower())
        self.assertIn("hang dextrose", MACRO.lower())
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
            "inspiratory stridor is the larynx",
            "not ice-water as default",
            "not kennel cough",
            "tie-back is the surgery conversation",
            "glucose now is the syringe",
            "do not pour syrup into a collapsed mouth",
            "not an insulinoma puppy",
            "stop the bag first",
            "no universal donor",
            "do not restart the same unit",
            "peripheral vs central before home",
            "stop metronidazole",
            "steroids are contraindicated in geriatric idiopathic",
            "do not ice, cut, suck, or tourniquet",
            "antivenom is the specific",
            "ammonia is not the diagnosis",
            "do not give benzodiazepines for hepatic encephalopathy",
            "do not pour lactulose into a somnolent",
            "lubricate now",
            "do not send a dry globe home",
            "replacement or enucleation tonight",
            "do not swing the neonate",
            "warm before you feed",
            "atropine is not for neonatal bradycardia",
            "name the gland or the uterus",
            "gangrene is surgery tonight",
            "do not send a septic dam home as sore milk",
            "measure iop now",
            "do not send home as conjunctivitis",
            "check the lens before latanoprost",
            "uti does not close calcium",
            "confirmed uti is infection, not fic",
            "frozen or cold sst can raise ica",
            "red miotic painful eye with flare is not conjunctivitis",
            "iop is typically **low**",
            "look at the lens",
            "no latanoprost / miotics",
            "blood in the ac is a sign, not a diagnosis",
            "aspirin is contraindicated",
            "cat claw → look at the lens",
            "seidel the leak",
            "do not send a leaking globe home",
            "do not call it sards without an erg",
            "no effective treatment reported",
            "enrofloxacin in a cat",
            "harvest book pred 1.0",
            "repair tonight",
            "figure-of-eight at the margin",
            "do not glue-and-home a margin cut",
            "lavage now",
            "do not neutralize",
            "minimum of 20 minutes",
            "do not send a melting eye home",
            "do not grid a melt",
            "cytology and culture",
            "recovery is still anesthesia",
            "dedicated anesthetist",
            "do not oxygen-flush a non-rebreathing",
            "do not grid a cat",
            "loose epithelial lip",
            "do not pick or peel it",
            "it will slough",
            "just lockjaw",
            "quiet / dark",
            "cats can still get tetanus",
            "consciousness is not affected",
            "search the whole coat",
            "just tired",
            "tas is not commercial in the us",
            "carrion / spoiled food",
            "flaccid, not tetanus",
            "steroids are not helpful",
            "fulminant mg",
            "upright feeding",
            "raw chicken",
            "cannot blink",
            "horner can blink",
            "just a droopy face",
            "not just uri",
            "retract the soft palate",
            "benign pink stalk",
            "they can blink",
            "just a small pupil",
            "1st/2nd/3rd-order",
            "which pupil is wrong",
            "just a funny pupil",
            "not horner",
            "not cortex",
            "retrobulbar",
            "dilated and fixed",
            "normal pupils",
            "post-ictal",
            "stroke blindness",
            "not a wellness screen",
            "bouncing cuff",
            "not pulmonary htn",
            "amlodipine / telmisartan",
            "not a lasix pa-pressure drug",
            "syncope after exercise",
            "not a pa catheter",
            "equal signs",
            "right jugular",
            "melarsomine is not recommended",
            "not just asthma",
            "one dead adult",
            "negative ab is",
            "not the legs",
            "normal radiographs do not rule it out",
            "warfarin is not recommended",
            "look at the urine",
            "nephrotic tetrad",
            "upc > 2 suggests",
            "low cholesterol is this list",
            "gi signs can be minimal",
            "skip a long diet trial",
        ):
            self.assertIn(needle, CARD.lower(), msg=needle)


if __name__ == "__main__":
    unittest.main()

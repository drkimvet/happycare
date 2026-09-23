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
NSAID_RE = re.compile(
    r"\b(nsaid|meloxicam|carprofen|robenacoxib|onsior|rimadyl|metacam|deracoxib|"
    r"flunixin|banamine)\b",
    re.I,
)
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
GABAPENTIN_RE = re.compile(r"\b(gabapentin|neurontin)\b", re.I)
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
SEPSIS_RE = re.compile(
    r"\b(sepsis|septic shock|septicemia|septicaemia|\bsirs\b|"
    r"septic peritonitis|septic abdomen|endotoxem)\b",
    re.I,
)
AHDS_RE = re.compile(
    r"\b(ahds|\bhge\b|hemorrhagic (diarrhea|gastro|enter)|"
    r"haemorrhagic (diarrhea|gastro)|bloody diarrhea|"
    r"hematochezia|parvo|parvovirus)\b",
    re.I,
)
ECLAMPSIA_RE = re.compile(
    r"\b(eclampsia|puerperal tetany|periparturient hypocalc)\b|"
    r"\b(nursing|lactat|postpartum|post-partum|whelping|queening|litter).{0,48}"
    r"\b(tremor|twitch|tetany|seizure|stiff|panting)\b|"
    r"\b(tremor|twitch|tetany|seizure).{0,48}"
    r"\b(nursing|lactat|postpartum|litter|whelping)\b",
    re.I,
)
CA_CL_SQ_RE = re.compile(
    r"\bcalcium chloride\b.{0,24}\b(sq|sc|subcut)|"
    r"\b(sq|sc|subcut).{0,24}\bcalcium chloride\b",
    re.I,
)
PRENATAL_CA_RE = re.compile(
    r"\b(pregnan|gestation|prenatal).{0,40}\bcalcium\b|"
    r"\bcalcium\b.{0,40}\b(pregnan|gestation|prenatal)\b",
    re.I,
)
DYSTOCIA_RE = re.compile(
    r"\b(dystocia|uterine inertia|stuck (labor|labour|whelping|queening)|"
    r"can't (deliver|whelp|queen)|cannot (deliver|whelp)|"
    r"green (discharge|lochia)|blackish-green|"
    r"oxytocin)\b",
    re.I,
)
OBSTRUCT_LABOR_RE = re.compile(
    r"\b(obstruct|stuck fetus|malposition|narrow pelvis|pelvic fracture|"
    r"brachycephal|bulldog|boston terrier|\bpug\b)\b",
    re.I,
)
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
# Enrofloxacin is also an ocular/retina word. Do not open the cystitis block
# unless the one-liner actually has a urinary context.
URINE_CONTEXT_RE = re.compile(
    r"\b(uti|cystitis|pollakiuria|stranguria|flutd|convenia|14.?day|dysuria|hematuria|pyelo|bacteriuria)\b",
    re.I,
)
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
IMHA_RE = re.compile(
    r"\b(imha|immune-mediated hemolytic|autoagglutination|spherocyte|coombs|"
    r"direct antiglobulin|\bdat\b|hemolytic anemia)\b",
    re.I,
)
TBI_RE = re.compile(
    r"\b(tbi|head trauma|traumatic brain|intracranial pressure|\bicp\b|"
    r"brain herniat|cushing reflex|decerebrate)\b",
    re.I,
)
MANNITOL_RE = re.compile(r"\bmannitol\b", re.I)
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
DYSPNEA_RE = re.compile(
    r"\b(dyspnea|dyspnoea|open[- ]mouth|orthopnea|respiratory distress|"
    r"labored breath|can'?t breathe|wheez|\basthma\b|bronchoconstrict|"
    r"lower airway|feline asthma)\b",
    re.I,
)
ALBUTEROL_RE = re.compile(r"\b(albuterol|salbutamol|terbutaline|aerokat)\b", re.I)
LARPAR_RE = re.compile(
    r"\blaryngeal paralys|"
    r"\b(lar ?par|\bgolpp\b|tie[- ]?back|"
    r"arytenoid lateral|inspiratory stridor|change of voice|"
    r"voice change|hoarse (bark|voice)|raspy (bark|voice))\b|"
    r"\bstridor\b",
    re.I,
)
HYPOGLY_RE = re.compile(
    r"\b(hypoglyc|low blood sugar|low glucose)\b|"
    r"\b(yorkie|yorkshire|maltese|chihuahua|toy poodle|toy breed|"
    r"neonat|juvenile).{0,48}\b(seizure|tremor|dull|collapse|weak|ataxia|listless)\b|"
    r"\b(puppy|kitten).{0,32}\b(seizure|tremor|dull|collapse|hypoglyc)\b|"
    r"\b(seizure|tremor|dull|collapse).{0,32}\b(yorkie|maltese|chihuahua|puppy|kitten|toy)\b",
    re.I,
)
TOY_PUPPY_RE = re.compile(
    r"\b(yorkie|yorkshire|maltese|chihuahua|toy poodle|toy breed|"
    r"puppy|kitten|neonat|juvenile|8[- ]week|12[- ]week|16[- ]week)\b",
    re.I,
)
POUR_SUGAR_RE = re.compile(
    r"\b(pour|force|syringe).{0,28}\b(honey|karo|syrup|dextrose)\b|"
    r"\b(honey|karo|corn syrup).{0,28}\b(mouth|throat|pour|force)\b",
    re.I,
)
INSULINOMA_RE = re.compile(r"\binsulinoma\b", re.I)
TRANSFUSION_RE = re.compile(
    r"\btransfus|"
    r"\b(prbc|packed red|whole blood|fresh frozen plasma|\bffp\b|"
    r"blood type|dea\s*1|xenotransfus|neonatal isoeryth|"
    r"\btaco\b|trali|febrile non[- ]?hemolytic|hemolytic reaction|"
    r"blood product|crossmatch)\b",
    re.I,
)
XENOTRANS_RE = re.compile(
    r"\bxenotransfus|dog blood.{0,20}(for|to).{0,12}cat|canine blood.{0,20}(for|to).{0,12}cat|"
    r"give.{0,12}cat.{0,12}dog blood",
    re.I,
)
TYPE_B_CAT_RE = re.compile(
    r"\btype[- ]?b\b.{0,28}\b(cat|queen|kitten)\b|"
    r"\b(cat|queen|kitten).{0,28}\btype[- ]?b\b",
    re.I,
)
TACO_RE = re.compile(r"\btaco\b|circulatory overload|volume overload", re.I)
RESTART_UNIT_RE = re.compile(
    r"\b(restart|resume|continue).{0,28}\b(same )?(unit|bag|transfusion)\b",
    re.I,
)
UNIVERSAL_DONOR_RE = re.compile(r"\buniversal donor\b", re.I)
VESTIBULAR_RE = re.compile(
    r"\b(vestibular|head tilt|nystagmus|otitis interna|"
    r"geriatric vestibular|rolling (dog|around))\b",
    re.I,
)
SNAKE_RE = re.compile(
    r"\bsnakebite|\bsnake bite|\bsnake-bite|"
    r"\benvenom|"
    r"\bcrotal|"
    r"\bantivenom|\bantivenin|"
    r"\b(pit viper|rattlesnake|copperhead|cottonmouth|water moccasin|"
    r"coral snake|elapid)\b",
    re.I,
)
SNAKE_MYTH_RE = re.compile(
    r"\b(ice|icing|ice pack|cut (and )?suck|suck (the )?venom|"
    r"tourniquet|electric shock)\b",
    re.I,
)
DRY_BITE_RE = re.compile(r"\bdry bite\b", re.I)
CORAL_RE = re.compile(r"\b(coral snake|elapid)\b", re.I)
FASCIOTOMY_RE = re.compile(r"\bfasciotom", re.I)
SNAKE_VAX_RE = re.compile(r"\b(rattlesnake vaccine|snake vaccine)\b", re.I)
SEND_HOME_RE = re.compile(r"\b(send home|go home|discharge|home as)\b", re.I)
HE_RE = re.compile(
    r"\bhepatic encephalo|"
    r"\bhepatoencephalo|"
    r"\bhead[- ]press|"
    r"\bammonium biurate|"
    r"\bportosystemic|\bpss\b|\bliver shunt|"
    r"\bfulminant hepatic|"
    r"\bacute hepatic failure|"
    r"\bacute liver failure|"
    r"\bliver failure\b",
    re.I,
)
BENZO_HE_RE = re.compile(r"\b(diazepam|midazolam|alprazolam|alfaxalone|benzo)\b", re.I)
LACTULOSE_RE = re.compile(r"\blactulose\b", re.I)
SOMNOLENT_RE = re.compile(r"\b(somnolent|obtund|coma|comatose|unresponsive)\b", re.I)
FFP_RE = re.compile(r"\b(ffp|fresh frozen plasma|plasma transfusion)\b", re.I)
PROLONGED_PT_RE = re.compile(r"\b(prolonged (pt|ptt)|long pt|high inr)\b", re.I)
PROPTOSIS_RE = re.compile(
    r"\bproptos|"
    r"\b(globe prolapse|prolapsed globe|eye out of (the )?socket|"
    r"eye popped out|popped (out )?(the )?eye)\b",
    re.I,
)
PUSH_GLOBE_RE = re.compile(
    r"\b(push|pop|reduce|reduction).{0,24}\b(globe|eye)\b|"
    r"\bmanual reduction\b|"
    r"\bwithout sedation\b",
    re.I,
)
GLOBE_RUPTURE_RE = re.compile(
    r"\b(globe rupture|ruptured globe|corneal perforat|three extraocular|"
    r"3 extraocular|optic nerve avuls)\b",
    re.I,
)
NEONATE_RE = re.compile(
    r"\bneonat|"
    r"\bnewborn|"
    r"\bfading (puppy|kitten|neonat)|"
    r"\b(day[- ]old|hours?[- ]old|just born)|"
    r"\b(whelping box|c-section puppy|c-section kitten)\b",
    re.I,
)
SWING_RE = re.compile(r"\bswing", re.I)
DOXAPRAM_RE = re.compile(r"\b(doxapram|dopram)\b", re.I)
TUBE_FEED_RE = re.compile(r"\b(tube[- ]feed|stomach tube|formula|bottle feed)\b", re.I)
COLD_NEONATE_RE = re.compile(
    r"\bhypotherm|"
    r"\b(chilled|cold (puppy|kitten|neonat))\b",
    re.I,
)
SMALL_LITTER_RE = re.compile(r"\b(small of the litter|\brunt\b)\b", re.I)
MASTITIS_RE = re.compile(
    r"\bmastit|"
    r"\bmetritis\b|"
    r"\b(mammary|udder|teat).{0,28}\b(hot|pain|swol|abscess|gangrene)|"
    r"\b(postpartum|post-partum).{0,40}\b(fever|septic|discharge|lochia)|"
    r"\bgangrenous (mastit|gland|mammary)\b",
    re.I,
)
GANGRENE_GLAND_RE = re.compile(
    r"\b(gangrene|gangrenous|necrotic gland|teat rupture|ruptured teat)\b",
    re.I,
)
SORE_MILK_RE = re.compile(r"\b(sore milk|just mastitis|engorged|cabbage only)\b", re.I)
GLAUCOMA_RE = re.compile(
    r"\bglaucoma|"
    r"\bhigh iop\b|"
    r"\belevated iop\b|"
    r"\biop (high|elevated)\b|"
    r"\bbuphthalm|"
    r"\btonomet",
    re.I,
)
LATANOPROST_RE = re.compile(
    r"\b(latanoprost|xalatan|prostaglandin analog|pg analog)\b",
    re.I,
)
LENS_LUX_RE = re.compile(
    r"\blens lux|"
    r"\bluxated lens|"
    r"\banterior lux|"
    r"\b(lens not seen|before (the )?lens|"
    r"lens in (the )?anterior|aphakic crescent|primary lens instab)\b",
    re.I,
)
UVEITIS_RE = re.compile(
    r"\buveitis|"
    r"\biridocyclitis|"
    r"\baqueous flare|"
    r"\bhypopyon|"
    r"\bkeratic|"
    r"\bsynechia|"
    r"\bmiotic (painful )?(eye|pupil)\b",
    re.I,
)
HYPHEMA_RE = re.compile(
    r"\bhyphema|"
    r"\bblood in (the )?anterior|"
    r"\beight[- ]ball",
    re.I,
)
CORNEAL_LAC_RE = re.compile(
    r"\bcorneal (lacer|perforat|wound|foreign)|"
    r"\bpenetrating (corneal|ocular|intraocular)|"
    r"\biris prolapse|"
    r"\bseidel|"
    r"\bcat claw.{0,24}\b(eye|cornea|globe)",
    re.I,
)
# descemet / keratomalac / melting prefixes sit outside a trailing \b
# so descemetocele and keratomalacia match.
MELT_RE = re.compile(
    r"\bmelting (corneal )?ulcer|"
    r"\bkeratomalac|"
    r"\bdescemet|"
    r"\bcorneal malac|"
    r"\bmalacic (cornea|ulcer|stroma)|"
    r"\bstromal melt|"
    r"\bpaper[- ]thin cornea|"
    r"\bdeep stromal",
    re.I,
)
GRID_BURR_RE = re.compile(r"\b(grid|diamond burr|keratotom)", re.I)
INDOLENT_RE = re.compile(
    r"\bindolent|"
    r"\bscced\b|"
    r"\bboxer ulcer|"
    r"\brecurrent corneal (eros|ulcer)|"
    r"\bloose epithelial|"
    r"\bepithelial lip|"
    r"\bnon[- ]healing (superficial )?(corneal )?ulcer",
    re.I,
)
# sequestrum as a word; do not use \bsequestr alone (platelet sequestration).
SEQ_RE = re.compile(
    r"\bsequestrum|"
    r"\bcorneal sequestr|"
    r"\bnigrum|"
    r"\b(brown|black|dark) (corneal|cornea) (plaque|spot|lesion)",
    re.I,
)
PEEL_PLAQUE_RE = re.compile(
    r"\b(pick|peel|pluck|flick|lift).{0,20}\b(plaque|sequestrum|nigrum)|"
    r"\b(plaque|sequestrum|nigrum).{0,20}\b(pick|peel|pluck|flick|lift)",
    re.I,
)
# FHV / dendritic / geographic. Do not use \bbranching alone (branching vessels).
FHV_RE = re.compile(
    r"\bfhv|"
    r"\bfeline herpes|"
    r"\bherpesvirus|"
    r"\bherpetic kerat|"
    r"\bherpes.{0,24}\b(eye|cornea|kerat|conjunct|ulcer|rhino)|"
    r"\bdendritic|"
    r"\bgeographic (corneal )?ulcer|"
    r"\bbranching (corneal )?(ulcer|dendrit)",
    re.I,
)
URI_FHV_RE = re.compile(
    r"\bsneez|"
    r"\brhinit|"
    r"\buri\b|"
    r"\bupper respir|"
    r"\bnasal discharge|"
    r"\brhinotrache",
    re.I,
)
JUST_HERPES_RE = re.compile(r"\bjust herpes|\bonly herpes|\bherpes and home", re.I)
# FEK / pink-white plaques. Do not use \beosinophil alone (blood count)
# or \beosinophilic ulcer (lip rodent ulcer of the skin complex).
EK_RE = re.compile(
    r"\beosinophilic kerat|"
    r"\beosinophilic keratoconjunct|"
    r"\bfek\b|"
    r"\bproliferative keratoconjunct|"
    r"\bproliferative keratitis|"
    r"\b(pink|white|cream) (raised |vascular )?(corneal|cornea|limbal) (plaque|mass|infiltrate)|"
    r"\b(corneal|cornea|limbal).{0,16}(pink|white) (plaque|mass)",
    re.I,
)
VALACYCLOVIR_RE = re.compile(r"\bvalacyclovir|\bvalaciclovir", re.I)
MEGESTROL_RE = re.compile(r"\bmegestrol", re.I)
RODENT_ULCER_RE = re.compile(
    r"\brodent ulcer|"
    r"\beosinophilic (granuloma|plaque|skin)|"
    r"\blip (ulcer|rodent)",
    re.I,
)
# KCS / dry eye. Do not use \bstt\b alone (other eye packets say STT).
KCS_RE = re.compile(
    r"\bkcs\b|"
    r"\bkeratoconjunctivitis sicca|"
    r"\bdry eye|"
    r"\bschirmer|"
    r"\baqueous tear|"
    r"\bquantitative kcs|"
    r"\bqualitative kcs|"
    r"\blusterless cornea|"
    r"\bmucopurulent (ocular|eye) discharge",
    re.I,
)
CHERRY_EYE_RE = re.compile(
    r"\bcherry eye|"
    r"\bprolapse.{0,20}nictit|"
    r"\bnictitans gland|"
    r"\bthird eyelid gland|"
    r"\bgland of the (third|nictit)|"
    r"\bred (mass|lump).{0,24}(third eyelid|nictit)",
    re.I,
)
GO_BACK_GLAND_RE = re.compile(
    r"\b(it will go back|will recede|pop back|goes back on its own)",
    re.I,
)
EXCISE_GLAND_RE = re.compile(
    r"\b(excis|amputat|cut out|remove).{0,24}\b(gland|cherry)|"
    r"\b(gland|cherry).{0,24}\b(excis|amputat|cut out|remove)",
    re.I,
)
DERM_TAC_RE = re.compile(
    r"\b(dermatolog|skin|atopic|elidel|protopic).{0,24}\b(tacrolimus|pimecrolimus)|"
    r"\b(tacrolimus|pimecrolimus).{0,24}\b(skin|dermatolog|ointment|cream)",
    re.I,
)
SULFA_KCS_RE = re.compile(
    r"\b(sulfonamide|sulfamethoxazole|trimethoprim[- ]sulfa|\btms\b|\bprimor\b)",
    re.I,
)
BNP_RE = re.compile(
    r"\b(neomycin.{0,24}polymyxin|triple antibiotic|\bbnp\b|neopoly)",
    re.I,
)
# anesth prefix sits outside a trailing \b so anesthesia / anesthetic match.
ANESTH_RE = re.compile(
    r"\banesth|"
    r"\binduct|"
    r"\bintubat|"
    r"\bextubat|"
    r"\bpremed|"
    r"\basa\s*[1-5e]|"
    r"\bunder gas\b|"
    r"\bisoflurane|"
    r"\bsevoflurane|"
    r"\bnon[- ]rebreath|"
    r"\bpop[- ]off",
    re.I,
)
O2_FLUSH_NRC_RE = re.compile(
    r"\b(oxygen flush|o2 flush|flush valve).{0,40}\b(nrc|non[- ]rebreath)|"
    r"\b(nrc|non[- ]rebreath).{0,40}\b(oxygen flush|o2 flush|flush valve)",
    re.I,
)
POPOFF_RE = re.compile(r"\b(closed pop[- ]off|pop[- ]off closed|popoff closed)", re.I)
ACEI_RE = re.compile(r"\b(ace inhibitor|enalapril|benazepril|lisinopril)\b", re.I)
FULL_INSULIN_FAST_RE = re.compile(
    r"\b(full (dose )?insulin|insulin.{0,24}fast|fast.{0,24}insulin)\b",
    re.I,
)
ASPIRIN_RE = re.compile(r"\b(aspirin|asa)\b", re.I)
YANK_FB_RE = re.compile(
    r"\b(yank|pull|tug|pluck).{0,20}\b(foreign body|thorn|fb)\b|"
    r"\b(foreign body|thorn|fb).{0,20}\b(yank|pull|tug|pluck)\b",
    re.I,
)
SARDS_RE = re.compile(r"\bsards?\b|\bsudden acquired retinal", re.I)
RD_RE = re.compile(r"\bretinal detach|\bdetached retina|\bbullous retina", re.I)
SUDDEN_BLIND_RE = re.compile(
    r"\bsudden (blind|vision)|"
    r"\bacute (blind|vision loss)|"
    r"\bwent blind|"
    r"\blost (its |their |his |her )?vision|"
    r"\bbumping into (walls|things|furniture)",
    re.I,
)
ENRO_RE = re.compile(r"\b(enrofloxacin|baytril)\b", re.I)
EYELID_LAC_RE = re.compile(
    r"\beyelid lacer|"
    r"\blid lacer|"
    r"\blid[- ]margin|"
    r"\bcut (the )?eyelid|"
    r"\btorn eyelid|"
    r"\bfigure[- ]of[- ]eight|"
    r"\bcanalicul",
    re.I,
)
GLUE_LID_RE = re.compile(r"\b(glue|skin glue|dermabond|staple).{0,20}\b(lid|eyelid|margin)\b", re.I)
# alkali / chemical / lye prefixes sit outside a trailing \b group so
# "alkali splash" and "chemical keratitis" match; do not use \balkali alone
# (that would fire alkaline phosphatase).
CHEM_EYE_RE = re.compile(
    r"\bchemical keratit|"
    r"\bchemical (ocular |eye |corneal )?(burn|splash|injur|trauma)|"
    r"\b(ocular|eye|corneal) chemical|"
    r"\balkali splash|"
    r"\balkaline (burn|splash|chemical|cleaner|agent|product|gel)|"
    r"(?:"
    r"\b(?:alkali|lye|drain cleaner|oven cleaner|pool shock|bleach|dishwasher detergent|corrosive)\b"
    r".{0,48}"
    r"\b(?:eye|cornea|ocular|conjunct|globe)\b"
    r"|"
    r"\b(?:eye|cornea|ocular|conjunct|globe)\b"
    r".{0,48}"
    r"\b(?:alkali|lye|drain cleaner|oven cleaner|pool shock|bleach|dishwasher detergent|corrosive)\b"
    r")|"
    r"\bacid (splash|burn).{0,24}\b(?:eye|cornea|ocular)|"
    r"\b(?:eye|cornea|ocular).{0,24}\bacid (splash|burn)",
    re.I,
)
NEUTRALIZE_RE = re.compile(r"\bneutraliz|\bboric acid\b", re.I)
STEROID_DROP_RE = re.compile(
    r"\bsteroid drop|"
    r"\btopical steroid|"
    r"\bpred(nisolone)? drop|"
    r"\bpred acetate",
    re.I,
)
HIGH_IOP_RE = re.compile(r"\b(high iop|elevated iop|iop (high|elevated)|secondary glaucoma)\b", re.I)
IVT_GENT_RE = re.compile(
    r"\b(intravitreal|ivt).{0,24}\bgent|"
    r"\bgentamicin.{0,24}\b(intravitreal|ivt|ciliary)\b",
    re.I,
)
CONJUNCTIVITIS_HOME_RE = re.compile(r"\bconjunctiv", re.I)
HYPERCA_RE = re.compile(
    r"\bhypercalc|"
    r"\bhyper-?calce|"
    r"\bhica\b|"
    r"\bionized (ca|calcium)\b|"
    r"\b(high|elevated)\s+(ica|tca|calcium)\b|"
    r"\b(ica|tca)\s+(high|elevated)\b|"
    r"\btotal calcium\b|"
    r"\bpthrp\b",
    re.I,
)
CONFIRMED_UTI_RE = re.compile(
    r"\b(uti confirmed|confirmed uti|confirmed (bacterial )?(cystitis|uti)|"
    r"culture[- ](confirmed|positive)|"
    r"bacteria (on|in) (the )?(sediment|urine))\b",
    re.I,
)
METRONIDAZOLE_RE = re.compile(r"\b(metronidazole|\bmetro\b|flagyl)\b", re.I)
VERTICAL_NYSTAG_RE = re.compile(r"\bvertical nystagmus\b", re.I)
HORNER_FACE_RE = re.compile(
    r"\bhorner\b.{0,40}\b(facial|face|vii)\b|"
    r"\b(facial|face|vii).{0,40}\bhorner\b|"
    r"\bhorner\b",
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

    if spec in {"dog", "cat"} and TRANSFUSION_RE.search(text):
        rxn = bool(
            re.search(
                r"\b(reaction|fever|hemolysis|hemoglobinemia|hemoglobinuria|"
                r"urticaria|hives|dyspnea|dyspnoea)\b",
                text,
                re.I,
            )
        )
        tx_loc = (
            "Blood product. Type first. "
            "Fever, pigment, or new dyspnea on a bag is a reaction until you stop and look."
        )
        localization = f"{localization} Also {tx_loc}" if localization else tx_loc
        if rxn:
            hard_stops.append(
                "Transfusion reaction: stop the bag first. Do not restart the same unit."
            )
        do_not.append(
            "Do not harvest 2013 mL/kg/h, PCV formulas, or the book's two diphenhydramine numbers. "
            "Do not invent a PCV transfusion cutoff."
        )
        do_not.append(
            "Do not mix calcium-containing fluids in the blood line. Filter. Finish a unit in 4 hours."
        )
        do_next.append(
            "Type DEA 1 (dog) or AB (cat). Look for hemolysis vs TACO vs allergy vs a dirty unit. "
            "Major crossmatch if a dog is >4 days from a prior unit. △ hospital blood bank."
        )
        sources.append(
            "Merck blood transfusions (Blois); AVHTM TRACS 2021 named as further reading. "
            "Plunkett transfusion headings traps only."
        )
        if spec == "cat":
            hard_stops.append(
                "Cats: AB type-specific blood. No universal donor. Type B plus type A can kill on the first unit."
            )
            do_next.append(
                "Cat allergic signs are often respiratory. First-unit crossmatch is the Mik/FEA conversation."
            )
            if UNIVERSAL_DONOR_RE.search(text):
                hard_stops.append("Do not use a universal-donor story for a cat.")
            if TYPE_B_CAT_RE.search(text) and re.search(r"\btype[- ]?a\b", text, re.I):
                hard_stops.append("Do not give type A blood to a type B cat.")
            if XENOTRANS_RE.search(text):
                hard_stops.append(
                    "Dog-to-cat xenotransfusion is last-ditch, not the night default. AHTR risk."
                )
        if RESTART_UNIT_RE.search(text):
            hard_stops.append("Do not restart the same unit.")
        if TACO_RE.search(text) and SHOCK_BOLUS_RE.search(text):
            hard_stops.append("TACO: stop. Do not add a shock bolus.")
        if DIPHEN_RE.search(text) and rxn:
            hard_stops.append(
                "Diphenhydramine is not first for hemolysis or anaphylactic shock."
            )
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic cat: still no DexSP, including for a transfusion reaction.")

    if spec in {"dog", "cat"} and IMHA_RE.search(text):
        imha_loc = (
            "Intravascular or extravascular hemolysis, not empty-vessel blood loss. "
            "TS usually holds in hemolysis; it falls with hemorrhage."
        )
        localization = f"{localization} Also {imha_loc}" if localization else imha_loc
        hard_stops.append(
            "Anemia is not IMHA until ACVIM 2019: immune destruction plus hemolysis. "
            "Saline agglutination is 1 drop blood + 4 drops saline — rouleaux disperses."
        )
        do_not.append(
            "Do not call slide clumping IMHA without saline. Do not use spherocytes as a feline criterion "
            "(cats lack consistent central pallor). Do not invent a PCV transfusion cutoff."
        )
        do_not.append(
            "Do not start prednisolone for onion/garlic Heinz or zinc pyknocytes. "
            "Do not harvest 2013 immunosuppressant tables. Azotemic cat: still no DexSP."
        )
        do_next.append(
            "Spun PCV if agglutinating. Smear in the monolayer. DAT before steroids if you can. "
            "Infectious screen. Cats: type-specific blood. Dog: thromboprophylaxis is the conversation △ Plumb."
        )
        sources.append("ACVIM IMHA diagnosis 2019 (Garden); ACVIM IMHA treatment 2019 (Swann); Merck regenerative anemias")
        if spec == "cat":
            do_not.append("Do not diagnose feline IMHA on spherocytes.")
        if ALLIUM_RE.search(text):
            hard_stops.append("Allium Heinz hemolysis is oxidative, not primary IMHA. Do not immunosuppress it.")

    if spec in {"dog", "cat"} and TBI_RE.search(text):
        localization = (
            "Secondary brain injury. Cerebral perfusion is MAP minus ICP. "
            "Cushing reflex (hypertension + bradycardia) is late herniation, not a CHF Lasix cue."
        )
        hard_stops.append(
            "TBI: steroids are contraindicated. DexSP is not the head-trauma plan."
        )
        do_not.append(
            "Do not give hypotonic fluid. Do not harvest 2013 mannitol/hypertonic/30-percent-board tables. "
            "Do not Lasix intracranial pressure. Do not wait for a skull film as therapy."
        )
        do_not.append(
            "Do not mannitol a hypovolemic patient. Hypertonic saline is the dry-patient conversation; △ hospital / Plumb."
        )
        do_next.append(
            "ABC and perfusion first. Glucose now. Oxygen. Elevate the head, no jugular compression. "
            "Serial neuro. Seizures: existing status gates. △ any osmotic drug."
        )
        sources.append("Plunkett head-trauma headings (legal split): steroids contraindicated; Merck trauma minimum database")
        if DEX_RE.search(text):
            hard_stops.append("Do not give DexSP for TBI.")
        if FUROSEMIDE_RE.search(text):
            hard_stops.append("Do not give furosemide for intracranial pressure.")
        if MANNITOL_RE.search(text) and HYPOVOLEM_RE.search(text):
            hard_stops.append("Do not give mannitol until the patient is volume-resuscitated.")

    if spec in {"dog", "cat"} and VESTIBULAR_RE.search(text):
        vest_loc = (
            "Peripheral vs central before home. "
            "Head tilt is the inner ear or the brainstem, not a stroke cocktail."
        )
        localization = f"{localization} Also {vest_loc}" if localization else vest_loc
        hard_stops.append(
            "Vestibular: name peripheral vs central before home. "
            "Do not DexSP an old rolling dog as a stroke."
        )
        do_not.append(
            "Do not harvest 2013 meclizine, dimenhydrinate, diazepam, or maropitant tables. "
            "Antiemetic △ Plumb. Do not force-walk a rolling dog."
        )
        do_not.append(
            "Do not put chlorhexidine or aminoglycoside drops in an ear whose tympanic membrane you have not seen."
        )
        do_next.append(
            "Otoscopic exam. Mentation, vertical nystagmus, CP deficits. "
            "Horner + facial = middle/inner ear, not default idiopathic. △ Plumb."
        )
        sources.append(
            "Merck otitis media/interna (Hoff); Merck nitroimidazoles (metro neurotoxicity). "
            "Plunkett vestibular headings traps only."
        )
        if DEX_RE.search(text) or MANNITOL_RE.search(text):
            hard_stops.append(
                "Steroids are contraindicated in geriatric idiopathic vestibular. "
                "Mannitol is not the old-dog-tilt plan."
            )
        if METRONIDAZOLE_RE.search(text):
            hard_stops.append("Stop metronidazole. Do not harvest a mg/kg cutoff.")
        if VERTICAL_NYSTAG_RE.search(text):
            hard_stops.append("Vertical nystagmus is central until proven otherwise. Do not send home as just old.")
        if HORNER_FACE_RE.search(text):
            do_not.append(
                "Horner + vestibular is the bulla/inner ear until imaging says otherwise, not default idiopathic."
            )
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for vestibular signs.")

    if spec in {"dog", "cat"} and SNAKE_RE.search(text):
        snake_loc = (
            "Pit viper: local necrosis and coagulopathy. "
            "Coral: little local, neuro, ventilate. "
            "Antivenom is the specific, not a steroid or an NSAID."
        )
        localization = f"{localization} Also {snake_loc}" if localization else snake_loc
        hard_stops.append(
            "Snakebite: do not ice, cut, suck, or tourniquet. "
            "Antivenom is the specific △ hospital stock."
        )
        do_not.append(
            "Do not harvest appendix 1–5 vials or a Merck epinephrine mL line. "
            "Do not chase the snake. Antibiotics are not routine without necrosis. "
            "Fasciotomy is not the default. A rattlesnake vaccine does not replace antivenom."
        )
        do_next.append(
            "Quiet, limit activity, come now. Mark the swelling edge. Coags / echinocytes. "
            "Coral: ventilate. Antivenom anaphylaxis: epinephrine first. △ hospital / Plumb."
        )
        sources.append(
            "Merck snakebites in animals (Gwaltney-Brant). "
            "Plunkett snakebite ~637–647 dropped; appendix vials stay on the page."
        )
        if SNAKE_MYTH_RE.search(text):
            hard_stops.append("Do not ice, cut, suck, tourniquet, or electrically shock a snakebite.")
        if NSAID_RE.search(text):
            hard_stops.append("NSAIDs are not recommended for snakebite. Do not NSAID a swollen limb for pain.")
        if DEX_RE.search(text):
            hard_stops.append("DexSP is not the antivenom.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for snakebite.")
        if DRY_BITE_RE.search(text) and SEND_HOME_RE.search(text):
            hard_stops.append("Do not send a spreading limb home as a dry bite.")
        if CORAL_RE.search(text):
            hard_stops.append(
                "Coral snake: little local swelling, neurologic, ventilate. "
                "US coral antivenom is not manufactured."
            )
        if FASCIOTOMY_RE.search(text):
            hard_stops.append("Fasciotomy is not the default for a tight snakebitten limb.")
        if SNAKE_VAX_RE.search(text):
            hard_stops.append("A rattlesnake vaccine does not replace antivenom.")

    if spec in {"dog", "cat"} and HE_RE.search(text):
        he_loc = (
            "Hepatic encephalopathy or fulminant failure. "
            "Ammonia is not the diagnosis. Glucose now. "
            "Shunt HE is not the same as acute liver failure."
        )
        localization = f"{localization} Also {he_loc}" if localization else he_loc
        hard_stops.append(
            "HE/ALF: ammonia is not the diagnosis. Glucose now. "
            "Do not give benzodiazepines for hepatic encephalopathy."
        )
        do_not.append(
            "Do not pour lactulose into a somnolent mouth. "
            "Do not harvest 2013 20 mL/kg enemas, neomycin, or book NAC 50. "
            "Do not give routine FFP for a long PT. Do not default a low-protein l/d if there is no overt HE."
        )
        do_next.append(
            "Name the toxin (sago / xylitol / APAP / mushroom). "
            "Lactulose if they can swallow, titrate to soft stool △ Plumb. "
            "HE seizure: levetiracetam, not a benzo. △ Plumb."
        )
        sources.append(
            "Merck hepatic encephalopathy and fulminant hepatic failure (Center). "
            "Plunkett AHF/HE headings traps only."
        )
        if nac_family and nac_family not in {"hepatic-failure", "acetaminophen", "xylitol-consider"}:
            hard_stops.append("NAC family conflict: do not blend hepatic-failure NAC with another family.")
        elif not nac_family:
            nac_family = "hepatic-failure"
        if BENZO_HE_RE.search(text):
            hard_stops.append(
                "Do not give benzodiazepines for hepatic encephalopathy. "
                "Alfaxalone is also off. Levetiracetam △ Plumb."
            )
        if LACTULOSE_RE.search(text) and SOMNOLENT_RE.search(text):
            hard_stops.append("Do not pour lactulose into a somnolent mouth.")
        if FFP_RE.search(text) and PROLONGED_PT_RE.search(text):
            hard_stops.append(
                "Do not give routine FFP for a long PT. Balanced hemostasis; plasma if bleeding."
            )
        if DEX_RE.search(text):
            hard_stops.append("Glucocorticoids precipitate HE. DexSP is not the liver plan.")
        if NSAID_RE.search(text):
            hard_stops.append("Do not NSAID a failing liver.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for HE.")

    if spec in {"dog", "cat"} and PROPTOSIS_RE.search(text):
        prop_loc = (
            "Globe anterior, lids trapped behind the equator. "
            "Lubricate now. Replacement or enucleation tonight."
        )
        localization = f"{localization} Also {prop_loc}" if localization else prop_loc
        hard_stops.append(
            "Proptosis: lubricate now. Replacement or enucleation tonight. "
            "Do not send a dry globe home."
        )
        do_not.append(
            "Do not harvest the 2013 3-hour cutoff, flunixin table, or suture/stent argument. "
            "Do not put chlorhexidine in the eye. Do not promise vision."
        )
        do_next.append(
            "ABC / other trauma first. Fluorescein after it is moist. "
            "Enucleate if ruptured, three extraocular muscles gone, or the optic nerve is avulsed. "
            "E-collar. △ topical / systemic in Plumb."
        )
        sources.append(
            "Merck proptosis (Thomasy). Plunkett proptosed-globe headings traps only."
        )
        if spec == "cat":
            hard_stops.append("Cat proptosis: vision is grave even if the globe is salvaged.")
        if PUSH_GLOBE_RE.search(text):
            hard_stops.append(
                "Do not push a proptosed globe back in the lobby without anesthesia "
                "and a canthotomy / tarsorrhaphy plan."
            )
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send a dry globe home.")
        if GLOBE_RUPTURE_RE.search(text):
            hard_stops.append(
                "Rupture, three extraocular muscles, or optic-nerve avulsion is an enucleation conversation tonight."
            )
        if NSAID_RE.search(text):
            hard_stops.append("Do not NSAID a traumatic proptosis. Hold flunixin.")
        if DEX_RE.search(text):
            hard_stops.append("DexSP is not the first syringe for a proptosed globe.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for proptosis.")

    if spec in {"dog", "cat"} and NEONATE_RE.search(text):
        neo_loc = (
            "Fading neonate or newborn resuscitation. "
            "Warm before you feed. Fading is not a diagnosis."
        )
        localization = f"{localization} Also {neo_loc}" if localization else neo_loc
        hard_stops.append(
            "Neonate: do not swing the neonate. Warm before you feed. "
            "Atropine is not for neonatal bradycardia."
        )
        do_not.append(
            "Do not give routine doxapram. Do not copy the adult RECOVER cart. "
            "Do not harvest 80–100 mL/kg, 1–2 drops doxapram, or Merck 0.0002 mg/g epinephrine."
        )
        do_next.append(
            "Airway, rub, dry, oxygen / PPV. Glucose now. Look at the umbilicus and the dam. "
            "Type B queen: NI already gated. △ newborn crash-cart / Plumb."
        )
        sources.append(
            "Merck neonate management (Davidson); RECOVER newborn resuscitation. "
            "Plunkett fading-neonate headings traps only."
        )
        if SWING_RE.search(text):
            hard_stops.append("Do not swing the neonate. Concussion and hemorrhage.")
        if DOXAPRAM_RE.search(text):
            hard_stops.append("Doxapram is not routine. PPV first.")
        if ATROPINE_RE.search(text):
            hard_stops.append(
                "Atropine is not for neonatal bradycardia. Ventilate the hypoxia."
            )
        if TUBE_FEED_RE.search(text) and COLD_NEONATE_RE.search(text):
            hard_stops.append("Do not tube-feed a cold neonate. Warm before you feed.")
        if SEND_HOME_RE.search(text) or SMALL_LITTER_RE.search(text):
            hard_stops.append(
                "Do not send a cold, not-nursing neonate home as small of the litter."
            )

    if spec in {"dog", "cat"} and MASTITIS_RE.search(text):
        mast_loc = (
            "Name the gland or the uterus. "
            "Mastitis and metritis can coexist. Gangrene is surgery tonight."
        )
        localization = f"{localization} Also {mast_loc}" if localization else mast_loc
        hard_stops.append(
            "Postpartum dam: name the gland or the uterus. "
            "Do not send a septic dam home as sore milk."
        )
        do_not.append(
            "Do not harvest cephalexin, amox-clav, PGF2α, or oxytocin IU. "
            "Do not harvest a 1% iodine flush. Do not cabbage-leaf a shocky dam. "
            "Do not wean the whole litter from one sore gland."
        )
        do_next.append(
            "Culture milk even if it looks normal. Look at the neonates and the other glands. "
            "Nursling-safe antibiotic △ Plumb if she is stable. Fluids if septic."
        )
        sources.append(
            "Merck mastitis / metritis (Scully). Plunkett mastitis headings traps only."
        )
        if GANGRENE_GLAND_RE.search(text):
            hard_stops.append("Gangrene is surgery tonight. Do not let neonates nurse that gland.")
        if SEND_HOME_RE.search(text) or SORE_MILK_RE.search(text):
            hard_stops.append("Do not send a septic dam home as sore milk.")
        if DEX_RE.search(text):
            hard_stops.append("DexSP is not the postpartum-sepsis plan.")
        if NSAID_RE.search(text):
            hard_stops.append("Hold NSAID on a septic or azotemic dam.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for mastitis.")

    if spec in {"dog", "cat"} and GLAUCOMA_RE.search(text):
        g_loc = (
            "Acute red painful eye: measure IOP now if the globe is intact. "
            "Do not send home as conjunctivitis. Check the lens before latanoprost."
        )
        localization = f"{localization} Also {g_loc}" if localization else g_loc
        hard_stops.append("Measure IOP now. Do not send home as conjunctivitis.")
        do_not.append(
            "Do not atropine a hard mydriatic eye. "
            "Do not harvest 2013 mmHg, oral-CAI, mannitol, or glycerin tables. "
            "Do not put a steroid drop on an unstained cornea."
        )
        do_next.append(
            "Fluorescein first. Check the other eye. Lower pressure tonight △ Plumb / hospital. "
            "Buphthalmos is chronic — comfort / enucleation conversation."
        )
        sources.append(
            "Merck acute glaucoma (Thomasy). Plunkett acute-glaucoma headings traps only."
        )
        if ATROPINE_RE.search(text):
            hard_stops.append("Do not atropine a glaucomatous eye.")
        if LATANOPROST_RE.search(text) and LENS_LUX_RE.search(text):
            hard_stops.append(
                "Check the lens before latanoprost. Miosis traps an anterior luxation."
            )
        if spec == "cat" and LATANOPROST_RE.search(text):
            hard_stops.append(
                "Cat: prostaglandin analogs are uncommon (often uveitic). Not the dog default."
            )
        if spec == "cat" and IVT_GENT_RE.search(text):
            hard_stops.append("Intravitreal gentamicin is contraindicated in cats.")
        if MANNITOL_RE.search(text) and re.search(
            r"\b(azotem|dry|dehydrat|creatinine)", text, re.I
        ):
            hard_stops.append("Do not give mannitol if dry or azotemic.")
        if SEND_HOME_RE.search(text) and CONJUNCTIVITIS_HOME_RE.search(text):
            hard_stops.append("Do not send home as conjunctivitis.")
        if DEX_RE.search(text):
            hard_stops.append(
                "Fluorescein before any steroid drop. Azotemic: still no DexSP."
            )

    if spec in {"dog", "cat"} and UVEITIS_RE.search(text):
        u_loc = (
            "Red miotic painful eye with flare is uveitis until IOP says otherwise. "
            "IOP is typically low. Fluorescein first. Find the cause."
        )
        localization = f"{localization} Also {u_loc}" if localization else u_loc
        hard_stops.append(
            "Do not send uveitis home as conjunctivitis. Measure IOP. Fluorescein first."
        )
        do_not.append(
            "Do not put a steroid drop on an unstained cornea. "
            "Do not atropine if IOP is high. "
            "Do not harvest 2013 atropine q2–3h, pred, carprofen, meloxicam, flunixin, or aspirin tables."
        )
        do_next.append(
            "Look for flare, miosis, and a systemic story if both eyes. "
            "Atropine only on a hypotonic eye △ Plumb. Pain △ Plumb."
        )
        sources.append(
            "Merck anterior uveitis (Thomasy). Plunkett anterior-uveitis headings traps only."
        )
        if SEND_HOME_RE.search(text) and CONJUNCTIVITIS_HOME_RE.search(text):
            hard_stops.append("Do not send uveitis home as conjunctivitis.")
        if ATROPINE_RE.search(text) and HIGH_IOP_RE.search(text):
            hard_stops.append("Do not atropine uveitis if IOP is high.")
        if spec == "cat" and DEX_RE.search(text):
            hard_stops.append(
                "Cat uveitis: do not DexSP-only. Infectious / FeLV / FIV / FIP / toxo / crypto stay on the list."
            )
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for uveitis.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Hold NSAID on an azotemic uveitis patient.")

    if spec in {"dog", "cat"} and LENS_LUX_RE.search(text):
        lux_loc = (
            "Look at the lens. Anterior luxation is a referral tonight. "
            "No latanoprost. Check the other eye."
        )
        localization = f"{localization} Also {lux_loc}" if localization else lux_loc
        hard_stops.append(
            "Anterior lens luxation: no latanoprost. Miosis traps vitreous and raises IOP. Refer tonight."
        )
        do_not.append(
            "Do not measure IOP on top of the lens. Do not harvest Merck mannitol g/kg. "
            "Do not treat posterior luxation as the same night surgery."
        )
        do_next.append(
            "Measure IOP off the lens. Visual → lens-out conversation. Blind → globe-out conversation. "
            "Cats: chronic uveitis is the usual cause. Terrier / Shar-Pei: check the other eye."
        )
        sources.append(
            "Merck dislocation of the lens (Thomasy). Plunkett lens-luxation headings traps only."
        )
        if LATANOPROST_RE.search(text):
            hard_stops.append(
                "Check the lens before latanoprost. Miosis traps an anterior luxation."
            )
        if MANNITOL_RE.search(text) and re.search(
            r"\b(azotem|dry|dehydrat|creatinine)", text, re.I
        ):
            hard_stops.append("Do not give mannitol if dry or azotemic.")

    if spec in {"dog", "cat"} and HYPHEMA_RE.search(text):
        h_loc = (
            "Blood in the anterior chamber is a sign, not a diagnosis. "
            "Stain. IOP. BP. Platelets. Quiet plus E-collar."
        )
        localization = f"{localization} Also {h_loc}" if localization else h_loc
        hard_stops.append(
            "Hyphema is a sign, not a diagnosis. Do not send it home as a red eye."
        )
        do_not.append(
            "Do not give aspirin for the bleed. Do not harvest pilocarpine, epinephrine, "
            "or tPA printed as 25 g (unit trap). Do not put a steroid on an unstained cornea."
        )
        do_next.append(
            "Fluorescein. IOP. BP. Platelets / coag / rodenticide story. "
            "Treat the cause. TPA is not the night default. △ Plumb."
        )
        sources.append(
            "Merck anterior uvea / hyphema (Hamor). Plunkett hyphema headings traps only."
        )
        if ASPIRIN_RE.search(text) or NSAID_RE.search(text):
            hard_stops.append("Aspirin is contraindicated in hyphema. Hold NSAID for the bleed.")
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send hyphema home as a red eye.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no DexSP, including for hyphema.")

    if spec in {"dog", "cat"} and CORNEAL_LAC_RE.search(text):
        c_loc = (
            "Cat-claw or corneal laceration: look at the lens. Seidel the leak. "
            "Iris out or leaking is surgery / refer tonight."
        )
        localization = f"{localization} Also {c_loc}" if localization else c_loc
        hard_stops.append(
            "Do not send a leaking globe home. Look at the lens. E-collar."
        )
        do_not.append(
            "Do not yank a deep or intraocular foreign body in the lobby. "
            "Do not put a steroid on a stain-positive cornea. "
            "Do not harvest 7–0 / 9–0 or a 2 mm lens-capsule cutoff."
        )
        do_next.append(
            "Fluorescein and Seidel. Quiet. Offer referral. "
            "Lens-capsule rupture can be medical; still offer surgery. "
            "Cats: traumatic lens sarcoma conversation."
        )
        sources.append(
            "Merck penetrating injuries and corneal lacerations (Thomasy). "
            "Plunkett corneal-FB headings traps only."
        )
        if YANK_FB_RE.search(text):
            hard_stops.append("Do not yank a deep or intraocular foreign body in the lobby.")
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send a leaking globe home.")
        if DEX_RE.search(text):
            hard_stops.append("Do not put a steroid on a stain-positive cornea.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for a corneal laceration.")

    if spec in {"dog", "cat"} and (
        SUDDEN_BLIND_RE.search(text) or SARDS_RE.search(text) or RD_RE.search(text)
    ):
        b_loc = (
            "Sudden blind: name the space — media vs retina vs optic vs brain. "
            "BP now. Do not call it SARDS without an ERG."
        )
        localization = f"{localization} Also {b_loc}" if localization else b_loc
        hard_stops.append(
            "Do not call sudden blindness SARDS without an ERG. "
            "Do not pred a hypertensive patient as the blindness plan."
        )
        do_not.append(
            "Do not harvest book pred 1.0 for SARD / optic neuritis. "
            "Merck: no effective SARDS treatment reported. "
            "Do not skip the enrofloxacin or ivermectin history."
        )
        do_next.append(
            "Menace, dazzle, palpebral, PLR. Fundus or B-scan. BP. "
            "Flat ERG = SARDS. Normal ERG = optic pathway → neuro. Offer referral."
        )
        sources.append(
            "Merck acute vision loss / SARDS / retinal detachment (Thomasy). "
            "Plunkett sudden-blindness headings traps only."
        )
        if spec == "cat" and ENRO_RE.search(text):
            hard_stops.append(
                "Cat + enrofloxacin: acute retinal degeneration until the fundus and history say otherwise."
            )
        if IVERMECTIN_RE.search(text):
            hard_stops.append(
                "Ivermectin can cause retinal toxicity or central blindness. Do not harvest the µg table."
            )
        if DEX_RE.search(text) or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I):
            hard_stops.append(
                "Do not DexSP or copy book pred for SARDS. Measure BP first. Azotemic: still no DexSP."
            )
        if spec == "cat" and RD_RE.search(text):
            hard_stops.append("Cat retinal detachment: measure BP tonight. Hypertension is on the list.")

    if spec in {"dog", "cat"} and EYELID_LAC_RE.search(text):
        lid_loc = (
            "Lid-margin laceration: repair tonight. Figure-of-eight at the margin. "
            "Two-layer. Stain the cornea."
        )
        localization = f"{localization} Also {lid_loc}" if localization else lid_loc
        hard_stops.append(
            "Do not glue-and-home a lid-margin cut. Repair tonight. Stain the globe."
        )
        do_not.append(
            "Do not leave a knot on the conjunctiva rubbing the cornea. "
            "Do not put chlorhexidine in the eye. Do not harvest 3–0 to 6–0."
        )
        do_next.append(
            "Two-layer closure. Figure-of-eight at the margin. E-collar. "
            "Temporary tarsorrhaphy if they cannot blink. Look at the medial canthus and the rest of the head."
        )
        sources.append(
            "Merck eyelid lacerations (Thomasy). No dedicated Plunkett lid-laceration chapter in the owned splits."
        )
        if GLUE_LID_RE.search(text) or SEND_HOME_RE.search(text):
            hard_stops.append("Do not glue-and-home a lid-margin cut.")
        if re.search(r"\bchlorhex", text, re.I):
            hard_stops.append("Do not put chlorhexidine in the eye.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for an eyelid laceration.")

    if spec in {"dog", "cat"} and CHEM_EYE_RE.search(text):
        chem_loc = (
            "Chemical / alkali ocular burn: lavage now. "
            "Alkali is worse than acid (liquefactive; may take 12 h). "
            "Fluorescein after the flush."
        )
        localization = f"{localization} Also {chem_loc}" if localization else chem_loc
        hard_stops.append(
            "Lavage now. Do not neutralize. Fluorescein after a minimum of 20 minutes."
        )
        do_not.append(
            "Do not put a topical steroid on a chemical burn. "
            "Do not harvest book 2 liters or an acetylcysteine table. "
            "Do not send home still burning."
        )
        do_next.append(
            "Water or 0.9% saline now. Flip lids / flush fornices / third eyelid. "
            "E-collar. Pain △ Plumb. Watch 12 h for alkali depth. "
            "Ingested corrosive: no emesis, no charcoal."
        )
        sources.append(
            "Merck corrosive toxicoses (Gwaltney-Brant, Mar 2025). "
            "Plunkett chemical keratitis ~445–446 traps only (2 L / boric neutralize)."
        )
        if NEUTRALIZE_RE.search(text):
            hard_stops.append(
                "Do not neutralize. Book boric-acid ointment is a trap. "
                "Merck: neutralizing makes an exothermic thermal burn."
            )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ):
            hard_stops.append("Do not put a topical steroid on a chemical burn.")
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send home still burning.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for a chemical eye burn.")

    if spec in {"dog", "cat"} and MELT_RE.search(text):
        melt_loc = (
            "Melting ulcer / descemetocele: proteinase is eating stroma. "
            "Refer tonight if melting, deep, or Descemet is showing."
        )
        localization = f"{localization} Also {melt_loc}" if localization else melt_loc
        hard_stops.append(
            "Do not send a melting eye home. Cytology and culture tonight. "
            "Do not steroid a melt. Do not grid a melt."
        )
        do_not.append(
            "Do not harvest serum q-hours, acetylcysteine, or a homemade 50% cutoff. "
            "Do not tonometry on a paper-thin cornea. "
            "Do not put BNP in a cat. Do not give a cat systemic enrofloxacin for the eye."
        )
        do_next.append(
            "Cytology and culture (aerobic + fungal). Serum △ hospital. "
            "STT, lids, FB. Seidel if leak. E-collar. Offer ophtho tonight."
        )
        sources.append(
            "Merck deep stromal / descemetocele / iris prolapse (Thomasy). "
            "Merck cornea melting / proteinase (Hamor). "
            "Plunkett ulcerative keratitis ~444–446 traps only."
        )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ):
            hard_stops.append("Do not steroid a melt.")
        if GRID_BURR_RE.search(text):
            hard_stops.append(
                "Do not grid a melt. Grid / diamond burr is the indolent superficial conversation. "
                "Keratotomy is not recommended in cats."
            )
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send a melting eye home.")
        if spec == "cat" and BNP_RE.search(text):
            hard_stops.append("Do not put a neomycin-polymyxin (BNP) product in a cat.")
        if spec == "cat" and ENRO_RE.search(text):
            hard_stops.append(
                "Cat + enrofloxacin: retina until proven otherwise. "
                "Do not use systemic enrofloxacin as the melting-ulcer antibiotic."
            )
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for a melting ulcer.")

    if spec in {"dog", "cat"} and INDOLENT_RE.search(text):
        ind_loc = (
            "Indolent / Boxer / SCCED: superficial with a loose epithelial lip. "
            "Not a melt until stroma is gone."
        )
        localization = f"{localization} Also {ind_loc}" if localization else ind_loc
        hard_stops.append(
            "Find STT / lids / FB before you name it SCCED. "
            "Do not steroid a stain-positive cornea. Do not grid a cat."
        )
        do_not.append(
            "Antibiotic drops alone will not close an indolent ulcer. "
            "Do not call a melting or deep ulcer a Boxer ulcer."
        )
        do_next.append(
            "Dogs: dry cotton-tip debridement, then diamond burr or grid △ hospital. "
            "E-collar. Soft contact lens △ hospital. Cats: herpes / sequestrum; no keratotomy."
        )
        sources.append(
            "Merck cornea (Hamor): indolent / recurrent erosion; keratotomy not recommended in cats. "
            "No dedicated Plunkett SCCED chapter in the owned splits."
        )
        if spec == "cat" and GRID_BURR_RE.search(text):
            hard_stops.append(
                "Do not grid a cat. Keratotomy predisposes to corneal sequestrum."
            )
        if MELT_RE.search(text):
            hard_stops.append(
                "If it is melting or deep, this is not an indolent ulcer. Do not grid a melt."
            )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ):
            hard_stops.append("Do not put a steroid on a stain-positive indolent ulcer.")

    if spec == "cat" and SEQ_RE.search(text):
        seq_loc = (
            "Feline corneal sequestrum: brown-to-black necrotic plaque. "
            "Keratectomy conversation. Depth may be hidden."
        )
        localization = f"{localization} Also {seq_loc}" if localization else seq_loc
        hard_stops.append(
            "Do not pick or peel a sequestrum. Do not grid a cat. "
            "Do not send a painful plaque home as it will slough."
        )
        do_not.append(
            "Do not harvest a keratectomy or antiviral table. "
            "Do not skip the herpes / brachy / prior-grid story."
        )
        do_next.append(
            "E-collar. Offer keratectomy of the whole plaque. "
            "Graft if deep. Dense plaques hide depth. Pain △ Plumb."
        )
        sources.append(
            "Merck cornea (Hamor): sequestration unique to the cat. "
            "No dedicated Plunkett sequestrum chapter."
        )
        if PEEL_PLAQUE_RE.search(text) or GRID_BURR_RE.search(text):
            hard_stops.append("Do not pick, peel, or grid a feline corneal sequestrum.")
        if SEND_HOME_RE.search(text):
            hard_stops.append("Do not send a painful or deep sequestrum home as it will slough.")
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ):
            hard_stops.append("Do not put a steroid on an ulcerated sequestrum.")

    if spec == "dog" and SEQ_RE.search(text):
        hard_stops.append(
            "Corneal sequestrum is a cat disease. Name pigment, a foreign body, or a mass in the dog."
        )

    if spec == "cat" and FHV_RE.search(text):
        uri_bit = (
            "Sneezing / URI supports FHV."
            if URI_FHV_RE.search(text)
            else "URI if present supports FHV; absence does not rule it out."
        )
        fhv_loc = (
            "Feline herpes keratitis: dendritic ulcer is highly characteristic. "
            "Geographic is coalesced dendrites. "
            f"{uri_bit} PCR is not required tonight."
        )
        localization = f"{localization} Also {fhv_loc}" if localization else fhv_loc
        hard_stops.append(
            "Do not put a steroid on a stain-positive / FHV ulcer. "
            "Do not grid a cat."
        )
        do_not.append(
            "Do not harvest famciclovir, idoxuridine, or l-lysine 500. "
            "Do not skip lids / STT / FB. "
            "Do not send a melting FHV eye home as just herpes."
        )
        do_next.append(
            "Fluorescein; rose bengal can help fine dendrites. "
            "E-collar. Antiviral △ Plumb / hospital. "
            "If melting or Descemet is showing, refer tonight."
        )
        sources.append(
            "Merck owner FHV-1 (Gelatt): respiratory signs + keratitis suggest; "
            "dendritic ulcers confirm. Merck cornea / conjunctiva (Hamor). "
            "Plunkett ulcerative keratitis names idoxuridine / l-lysine 500 — traps only."
        )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ):
            hard_stops.append(
                "Do not put a steroid on a stain-positive / FHV ulcer. "
                "Corticosteroids can reactivate FHV and raise sequestrum risk."
            )
        if GRID_BURR_RE.search(text):
            hard_stops.append(
                "Do not grid a cat. Keratotomy predisposes to corneal sequestrum."
            )
        if MELT_RE.search(text) and (
            SEND_HOME_RE.search(text) or JUST_HERPES_RE.search(text)
        ):
            hard_stops.append(
                "Do not send a melting or descemetocele FHV eye home as just herpes."
            )
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for an FHV ulcer.")

    if spec == "dog" and FHV_RE.search(text):
        hard_stops.append(
            "Dendritic ulcer / FHV keratitis is the cat conversation. "
            "Name something else in the dog."
        )

    if spec == "cat" and EK_RE.search(text):
        ek_loc = (
            "Feline eosinophilic keratitis: pink-to-white raised corneal plaques. "
            "Cytology (eosinophils) confirms. Not a brown sequestrum. "
            "Not a lip rodent ulcer."
        )
        localization = f"{localization} Also {ek_loc}" if localization else ek_loc
        hard_stops.append(
            "Stain first. Do not put a steroid on a stain-positive cornea. "
            "Do not grid a cat. Cytology confirms FEK."
        )
        do_not.append(
            "Do not harvest cyclosporine 1–2% or dexamethasone 0.1%. "
            "Do not start megestrol as the night default. "
            "Do not call a lip rodent ulcer this eye."
        )
        do_next.append(
            "Fluorescein. Cytology of the plaque. FHV stays on the list. "
            "Immunomodulation △ ophtho / hospital after the stain. E-collar."
        )
        sources.append(
            "Merck tear stimulants (Whelan): names eosinophilic keratitis; "
            "printed CSA / tacrolimus / dex percents stay on the page. "
            "Merck antiviral: valacyclovir contraindicated in cats. "
            "No dedicated Plunkett FEK chapter."
        )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ) and (
            re.search(r"\bulcer|stain[- ]positive|fluorescein", text, re.I)
            or FHV_RE.search(text)
            or MELT_RE.search(text)
        ):
            hard_stops.append(
                "Do not put a steroid on a stain-positive / ulcerated FEK cornea. "
                "Packet 154 still owns an FHV ulcer tonight."
            )
        if GRID_BURR_RE.search(text):
            hard_stops.append(
                "Do not grid a cat. Keratotomy predisposes to corneal sequestrum."
            )
        if VALACYCLOVIR_RE.search(text):
            hard_stops.append(
                "Valacyclovir is contraindicated in cats (Merck antiviral)."
            )
        if MEGESTROL_RE.search(text):
            hard_stops.append(
                "Megestrol is not the night default for eosinophilic keratitis."
            )
        if RODENT_ULCER_RE.search(text):
            hard_stops.append(
                "Lip eosinophilic / rodent ulcer is the skin complex, not this cornea."
            )
        if SEND_HOME_RE.search(text) and CONJUNCTIVITIS_HOME_RE.search(text):
            hard_stops.append(
                "Do not send eosinophilic keratitis home as conjunctivitis."
            )
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for FEK.")

    if spec == "dog" and EK_RE.search(text):
        hard_stops.append(
            "Eosinophilic keratitis is a cat conversation. "
            "In the dog name pannus or immune keratitis, not FEK."
        )

    if spec in {"dog", "cat"} and KCS_RE.search(text):
        kcs_loc = (
            "Quantitative KCS: aqueous tear deficiency. "
            "STT before any drops. Dogs common; cats uncommon (FHV scarring). "
            "Not conjunctivitis until the strip."
        )
        localization = f"{localization} Also {kcs_loc}" if localization else kcs_loc
        hard_stops.append(
            "STT before any drops or cleaning. "
            "Do not put a steroid on an ulcerated KCS cornea. "
            "Do not send a sticky red eye home as conjunctivitis."
        )
        do_not.append(
            "Do not harvest CSA 0.2–2% or STT ≥ 2 mm. "
            "Do not put dermatologic tacrolimus in the eye. "
            "Do not excise a cherry-eye gland. Atropine dries tears."
        )
        do_next.append(
            "Fluorescein. Artificial tears tonight. Lacrimogenic △ Plumb. "
            "If melting or Descemet is showing, refer tonight (packet 150)."
        )
        sources.append(
            "Merck nasolacrimal (Hamor): quantitative KCS; STT before drops. "
            "Printed CSA / pilocarpine / STT ≥ 2 mm stay on the page. "
            "No dedicated Plunkett KCS chapter."
        )
        if (
            STEROID_DROP_RE.search(text)
            or DEX_RE.search(text)
            or re.search(r"\bpred(nisolone|nisone)?\b", text, re.I)
        ) and (
            re.search(r"\bulcer|stain[- ]positive|fluorescein|melt", text, re.I)
            or MELT_RE.search(text)
        ):
            hard_stops.append(
                "Do not put a steroid combo on an ulcerated or melting KCS cornea."
            )
        if ATROPINE_RE.search(text):
            hard_stops.append("Atropine dries tears. Do not atropine a dry eye.")
        if DERM_TAC_RE.search(text):
            hard_stops.append(
                "Do not put dermatologic tacrolimus or pimecrolimus in the eye."
            )
        if EXCISE_GLAND_RE.search(text) or (
            CHERRY_EYE_RE.search(text) and EXCISE_GLAND_RE.search(text)
        ):
            hard_stops.append(
                "Do not excise a nictitans / cherry-eye gland. Replace it. "
                "That gland is a tear gland."
            )
        if MELT_RE.search(text) and SEND_HOME_RE.search(text):
            hard_stops.append(
                "Do not send a melting dry eye home. Packet 150 still owns the melt."
            )
        if SEND_HOME_RE.search(text) and CONJUNCTIVITIS_HOME_RE.search(text):
            hard_stops.append(
                "Do not send a sticky red KCS eye home as conjunctivitis."
            )
        if SULFA_KCS_RE.search(text):
            do_next.append("Sulfonamide history sits on the KCS list.")
        if spec == "cat":
            do_next.append("Cat KCS is uncommon; chronic FHV scarring is on the list.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for KCS.")

    if spec in {"dog", "cat"} and CHERRY_EYE_RE.search(text):
        ch_loc = (
            "Cherry eye: prolapsed nictitans gland. "
            "It is a tear gland. Replace it. Do not excise. "
            "Check the other eye."
        )
        localization = f"{localization} Also {ch_loc}" if localization else ch_loc
        hard_stops.append(
            "Do not excise a cherry-eye gland. "
            "Lubricate if the gland is exposed. "
            "Do not send a dry gland home as it will go back."
        )
        do_not.append(
            "Do not harvest a pocket recipe or later-KCS percents. "
            "Do not call a whole third eyelid (Horner / Haw's) this surgery."
        )
        do_next.append(
            "Stain. STT before drops. Lubricate. "
            "Offer replacement / pocket tonight or in the morning if the cornea is safe."
        )
        sources.append(
            "Merck nasolacrimal (Hamor): preserve the nictitans gland. "
            "Printed excision percents stay on the page. "
            "No dedicated Plunkett cherry-eye chapter."
        )
        if EXCISE_GLAND_RE.search(text):
            hard_stops.append(
                "Do not excise a nictitans / cherry-eye gland. Replace it. "
                "That gland is a tear gland."
            )
        if GO_BACK_GLAND_RE.search(text) or (
            SEND_HOME_RE.search(text)
            and re.search(r"\b(dry|ulcer|exposed|stain)", text, re.I)
        ):
            hard_stops.append(
                "Do not send a dry or ulcerated cherry-eye gland home as it will go back."
            )
        if spec == "cat":
            do_next.append("Cat cherry eye is uncommon; still do not excise.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including for cherry eye.")

    if spec in {"dog", "cat"} and ANESTH_RE.search(text):
        an_loc = (
            "Anesthesia continuum: recovery is still anesthesia. "
            "Dedicated anesthetist. Confirm the tube with ETCO2."
        )
        localization = f"{localization} Also {an_loc}" if localization else an_loc
        hard_stops.append(
            "Recovery is still anesthesia. Dedicated anesthetist. "
            "Confirm the tube with ETCO2. Name the hypotension before a bolus."
        )
        do_not.append(
            "Do not oxygen-flush a non-rebreathing circuit. "
            "Do not leave a closed pop-off. "
            "Do not harvest AAHA mg/kg figures, MAP/ETCO2 bands, or ASA as a homemade cutoff."
        )
        do_next.append(
            "Checklist. Hands-on plus SpO2 / ETCO2 / BP / temp. "
            "Disconnect before you turn. Lean weight. IV catheter. "
            "Hold ACE-I this morning. Do not give full insulin to a fasted patient."
        )
        sources.append(
            "AAHA 2020 anesthesia and monitoring (Grubb / Sager); aaha.org/anesthesia. "
            "Fluids citation in that paper is 2013; night fluids are AAHA 2024."
        )
        if O2_FLUSH_NRC_RE.search(text):
            hard_stops.append(
                "Do not oxygen-flush a non-rebreathing circuit. That is barotrauma."
            )
        if POPOFF_RE.search(text):
            hard_stops.append("Closed pop-off is barotrauma. Open it.")
        if ACEI_RE.search(text):
            hard_stops.append("Hold ACE inhibitors the morning of anesthesia.")
        if FULL_INSULIN_FAST_RE.search(text):
            hard_stops.append("Do not give the full insulin dose to a fasted patient.")
        if NSAID_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic: still no NSAID, including peri-anesthesia.")

    if spec in {"dog", "cat"} and HYPERCA_RE.search(text):
        ca_loc = (
            "Ionized hypercalcemia is its own problem list. "
            "High iCa plus high tCa is not an albumin artifact."
        )
        localization = f"{localization} Also {ca_loc}" if localization else ca_loc
        hard_stops.append(
            "Do not DexSP for maybe-lymphoma before PTH/tissue. "
            "PTHrP negative does not rule out malignancy."
        )
        do_not.append(
            "Do not close calcium because a UTI is confirmed. "
            "Do not harvest a fluid or bisphosphonate table. "
            "Cats: idiopathic is most common; lymphoma is possible, not the default."
        )
        do_next.append(
            "Repeat iCa anaerobic (air lowers iCa; frozen/cold SST can raise it). "
            "PTH ± PTHrP. Image for CaOx and for a mass. Two problem lists if UTI is also present."
        )
        sources.append(
            "Merck hypercalcemia in dogs and cats (idiopathic most common in cats; "
            "tumor pair lymphoma + SCC). Lab preanalytical iCa comment."
        )
        if DEX_RE.search(text):
            hard_stops.append("Do not give DexSP before PTH/tissue on a hypercalcemic patient.")
        if URINE_CONTEXT_RE.search(text):
            hard_stops.append("UTI does not close the calcium problem list.")

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

    if spec == "cat" and DYSPNEA_RE.search(text):
        dyspnea_loc = (
            "Name the space before the syringe: upper airway vs bronchial (asthma) "
            "vs pleural vs CHF vs anemia/ATE vs anaphylaxis."
        )
        localization = f"{localization} Also {dyspnea_loc}" if localization else dyspnea_loc
        hard_stops.append(
            "Cat respiratory distress: oxygen and hands off first. Name the space before Lasix, DexSP, or albuterol."
        )
        do_not.append(
            "Do not stack Lasix + albuterol + DexSP. Do not wrestle for radiographs. "
            "Do not harvest puff / terbutaline / DexSP mg/kg tables."
        )
        do_not.append(
            "Do not send open-mouth breathing home as anxiety. "
            "New cough in an older cat is often pneumonia, not new asthma."
        )
        do_next.append(
            "Pattern: inspiratory stertor/stridor = upper; expiratory push/wheeze = bronchial; "
            "quiet restrictive = pleural (tap first). TFAST: glide, B-lines, LA, fluid, tamponade. △ Plumb."
        )
        sources.append(
            "Merck emergency evaluation (oxygen first); Merck respiratory signs "
            "(inspiratory upper vs expiratory lower); Merck feline bronchial asthma"
        )
        if FUROSEMIDE_RE.search(text) and not CHF_RE.search(text):
            hard_stops.append("Do not give furosemide until CHF pulmonary edema is the localization.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic cat: still no DexSP, including for suspected asthma.")
        if ALBUTEROL_RE.search(text) and (PLEURAL_RE.search(text) or PNEUMO_RE.search(text)):
            hard_stops.append("Bronchodilator is not therapy for pleural air or fluid.")

    if spec == "dog" and LARPAR_RE.search(text):
        larpar_loc = (
            "Upper airway: the larynx is not abducting. "
            "Old large-breed inspiratory stridor / voice change is laryngeal paralysis "
            "(GOLPP) until light-anesthesia laryngoscopy. Toy-breed honk may be collapse."
        )
        localization = f"{localization} Also {larpar_loc}" if localization else larpar_loc
        hard_stops.append(
            "Dog inspiratory stridor / laryngeal paralysis: oxygen, hands off, cool. "
            "Not a Lasix or albuterol cocktail. Not kennel cough."
        )
        do_not.append(
            "Do not harvest 2013 acepromazine, butorphanol, propofol, DexSP, or doxapram tables. "
            "Sedation is △ crash-cart / Plumb."
        )
        do_not.append(
            "Do not ice-water the obstruction fever as default heatstroke. "
            "Do not wrestle for radiographs (rads are not diagnostic of the larynx). "
            "Do not throat-exam a crashing dog without an ET tube and a tracheostomy plan ready."
        )
        do_not.append(
            "Do not flood with fluids: obstruction can make pulmonary edema. "
            "Do not Lasix this as CHF. Azotemic: still no DexSP."
        )
        do_next.append(
            "Oxygen. Tepid cool + airflow. △ sedation. If still crashing: intubate or tracheostomy. "
            "Aspiration pneumonia on the DDX once stable. Tie-back is the surgery conversation. "
            "GOLPP hindlimb/megaesophagus later — tonight is the airway."
        )
        sources.append(
            "Merck laryngeal paralysis dogs/cats (Kemp; rads not diagnostic; tracheotomy if severe); "
            "ACVS lar par (oxygen, cooling, sedation, possibly intubate); "
            "Cornell GOLPP (aspiration, hindlimb later). Plunkett p124–125 traps only."
        )
        if FUROSEMIDE_RE.search(text) and not CHF_RE.search(text):
            hard_stops.append("Do not give furosemide for laryngeal obstruction.")
        if ALBUTEROL_RE.search(text):
            hard_stops.append("Bronchodilator is not therapy for a paralyzed larynx.")
        if ICE_RE.search(text):
            hard_stops.append("Ice-water immersion is not the default cool for laryngeal obstruction heat.")
        if DEX_RE.search(text) and AZOTEMIA_RE.search(text):
            hard_stops.append("Azotemic patient: still no DexSP, including for laryngeal edema.")

    if spec == "cat" and LARPAR_RE.search(text):
        do_not.append(
            "Feline laryngeal paralysis is uncommon (Merck). Still name the space before the syringe."
        )
        sources.append("Merck: laryngeal paralysis is common in dogs and rare in cats")

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
        if GABAPENTIN_RE.search(text):
            hard_stops.append(
                "Gabapentin is a PO/chronic adjunct (Forman). It does not replace opioid primary analgesia for acute pancreatitis."
            )
            do_not.append(
                "Do not send gabapentin instead of buprenorphine for tonight's cranial pain. "
                "Overt bout: opioid. Long-term chronic: gabapentin/tramadol is the Forman conversation."
            )
            do_not.append(
                "Do not invent a gabapentin mg/kg. Read THIS bottle — some human gabapentin liquids contain xylitol."
            )
            do_next.append(
                "Tonight: opioid △ Plumb. Gabapentin only as a named outpatient adjunct, not onto the housemate."
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
        localization = (
            "Gastric volvulus: obstructive plus hypovolemic shock. "
            "Caudal vena cava and portal vein are compressed until the stomach is decompressed and derotated."
        )
        hard_stops.append("GDV: stabilize, decompress, surgery. Not an observe-overnight disease.")
        do_not.append("Do not induce emesis for GDV.")
        do_not.append(
            "Do not harvest 2013 orogastric-tube or trocar recipes. Do not send home after a trocar without a gastropexy conversation."
        )
        do_not.append(
            "Do not invent a lactate cutoff or euthanize on one number. Serial lactate after resuscitation is the conversation."
        )
        do_next.append(
            "Right lateral radiograph (reverse C / double bubble). Avoid ventrodorsal (aspiration). "
            "Fluids AAHA-style; never bolus a KCl bag. Gastropexy prevents volvulus recurrence, not all bloat. "
            "Post-op VPCs are common and delayed; △ lidocaine in Plumb."
        )
        sources.append("Merck: gastric dilation and volvulus in small animals")

    if spec in {"dog", "cat"} and SEPSIS_RE.search(text):
        localization = localization or (
            "Sepsis: infection plus organ dysfunction. Distributive shock "
            "(± hypovolemic ± cardiogenic) until the pocket is named."
        )
        hard_stops.append(
            "Sepsis is infection plus organ dysfunction, not a SIRS checkbox. Find the source."
        )
        do_not.append(
            "Do not invent SIRS 2/4–3/4 or HR/RR/temp/WBC cutoffs. Do not invent a lactate/MAP veto."
        )
        do_not.append(
            "Do not harvest 2013 shock-dose or hetastarch tables. Do not lead with high-dose DexSP."
        )
        do_not.append(
            "Do not send feverish or hypothermic collapse home as just GI. "
            "Antibiotics do not replace source control (OHE, explore, chest tube)."
        )
        do_next.append(
            "Name the pocket: abdomen, uterus, urine, chest, bite, catheter, GI leak. "
            "Culture if it does not delay the first antimicrobial. Fluids AAHA-style; never bolus a KCl bag. "
            "Cats can be hypothermic and bradycardic. Addison is a different syringe. △ Plumb."
        )
        sources.append(
            "Sharp JVECC 2023 defining sepsis; 2025 consensus (infection + organ dysfunction); "
            "Merck bacterial infections / septic shock; Merck triage: high-dose steroids not recommended"
        )

    if spec == "dog" and AHDS_RE.search(text):
        localization = localization or (
            "Hemorrhagic diarrhea is a syndrome, not a diagnosis. "
            "AHDS vs parvo vs Addison vs rodenticide vs FB until the test and the smear say."
        )
        hard_stops.append(
            "Bloody diarrhea is not a diagnosis. Fluids first. Parvo test if young, unvaccinated, or neutropenic."
        )
        do_not.append(
            "Do not send shocky bloody diarrhea home as colitis. "
            "Do not skip the parvo SNAP because the stool is not red (~25% of parvo is non-bloody)."
        )
        do_not.append(
            "Do not shotgun antibiotics onto every AHDS/HGE. "
            "Antibiotics are a sepsis or neutropenia conversation, not the mild case. "
            "Do not invent a PCV or neutrophil cutoff. Do not harvest ampicillin tables."
        )
        do_next.append(
            "PCV/TS now (hemoconcentration supports AHDS). Glucose. Isolate if parvo. "
            "Addison and anticoagulant rodenticide stay on the list. Offer food when vomiting allows. △ Plumb."
        )
        sources.append(
            "Merck AHDS (fluids first; antibiotics not routine if mild–moderate); "
            "Merck canine parvovirus (antigen test; isolate; nutrition)"
        )

    if spec in {"dog", "cat"} and ECLAMPSIA_RE.search(text):
        localization = localization or (
            "Periparturient hypocalcemia (eclampsia / puerperal tetany). "
            "Not idiopathic epilepsy until calcium and glucose are on the table."
        )
        hard_stops.append(
            "Eclampsia: slow IV calcium gluconate with ECG. Do not wait for the printer on classic tetany."
        )
        do_not.append(
            "Do not harvest calcium mL/kg or total-Ca cutoffs. Do not give calcium chloride subcutaneously."
        )
        do_not.append(
            "Do not load oral calcium during pregnancy to prevent this — Merck: it predisposes. "
            "Do not treat as idiopathic epilepsy. Do not ice-water the tetany fever as primary heatstroke."
        )
        do_next.append(
            "Glucose now. Interrupt nursing tonight; milk-replacer conversation. "
            "Recurrence with later litters is expected. △ Plumb."
        )
        sources.append(
            "Merck eclampsia in small animals (slow IV calcium gluconate; oral calcium in pregnancy predisposes)"
        )
        if CA_CL_SQ_RE.search(text):
            hard_stops.append("Calcium chloride is not for subcutaneous use.")
        if PRENATAL_CA_RE.search(text):
            hard_stops.append("Oral calcium during pregnancy is not prevention.")

    if spec in {"dog", "cat"} and DYSTOCIA_RE.search(text):
        localization = localization or (
            "Dystocia: obstruction versus inertia before any oxytocin. "
            "Green/black discharge before the first fetus is placental separation."
        )
        hard_stops.append(
            "Dystocia: name obstruction vs inertia before oxytocin. Oxytocin is not for a stuck fetus."
        )
        do_not.append(
            "Do not harvest oxytocin IU, three-dose, or hour-between-pups tables. "
            "Do not send oxytocin home with the breeder. Do not yank a stuck fetus."
        )
        do_not.append(
            "Do not invent a single hour cutoff (sources disagree). "
            "Green discharge before baby one is enough to come in."
        )
        do_next.append(
            "Glucose and calcium if inertia is the story (eclampsia overlap). "
            "C-section if obstructed, distressed, brachycephalic risk, or medical fails. △ Plumb / hospital."
        )
        sources.append(
            "Merck dystocia in small animals; Merck labor/delivery page "
            "(SQ calcium gluconate conflicts with the dystocia not-SC/IM line)"
        )
        if OBSTRUCT_LABOR_RE.search(text):
            hard_stops.append(
                "Obstructive or brachycephalic dystocia: C-section conversation. Not an oxytocin trial."
            )

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

    if spec in {"dog", "cat"} and URINE_CONTEXT_RE.search(text):
        do_not.append("Do not write a 14-day course for sporadic cystitis. ISCAID 2019: 3–5 days.")
        do_not.append("Do not reach for a fluoroquinolone or 3rd-gen cephalosporin as first-tier sporadic cystitis.")
        if CONFIRMED_UTI_RE.search(text):
            hard_stops.append(
                "Confirmed UTI is infection, not FIC. It does not close a calcium problem list."
            )
            do_next.append(
                "ISCAID 3–5 d if sporadic lower tract. Fever, lumbar pain, or azotemia flips to pyelo. "
                "Culture if not already. Analgesia △ Plumb. Hold NSAID if azotemic."
            )
        else:
            do_next.append(
                "Culture when you can. Analgesia. Young cat: FIC until culture says otherwise."
            )
        sources.append("ISCAID 2019: sporadic cystitis 3–5 d; reserve FQ/3rd-gen")
        if spec == "cat" and FQ_RE.search(text) and re.search(r"\b(young|2 yo|3 yo|flutd)\b", text, re.I):
            hard_stops.append("Young cat FLUTD: empiric fluoroquinolone is not the ISCAID plan.")
        if HYPERCA_RE.search(text):
            hard_stops.append("UTI does not close the calcium problem list. Write two lists.")
            do_next.append(
                "Image for CaOx. Repeat iCa anaerobic, not a frozen or cold SST. "
                "Do not DexSP for maybe-lymphoma before PTH/tissue."
            )

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

    if spec in {"dog", "cat"} and HYPOGLY_RE.search(text):
        toy = bool(TOY_PUPPY_RE.search(text))
        hypogly_loc = (
            "Brain without glucose. Glucose now is the syringe, not the diagnosis. "
            "Toy/neonate: missed meals / sepsis / PSS / parvo until proven otherwise."
            if toy
            else "Hypoglycemia is a sign. Split xylitol, insulin, sepsis, liver, and insulinoma (older dog)."
        )
        localization = f"{localization} Also {hypogly_loc}" if localization else hypogly_loc
        hard_stops.append(
            "Hypoglycemia: glucose now. Do not treat as idiopathic epilepsy first."
        )
        do_not.append(
            "Do not harvest 2013 25%/50% dextrose, 60 mg/dL, or neonate mL/100 g tables. △ Plumb."
        )
        do_not.append(
            "Do not pour syrup into a collapsed mouth (aspiration). "
            "Undiluted 50% dextrose in a tiny peripheral vein is a phlebitis/slough conversation."
        )
        do_next.append(
            "Warm. If they can swallow, feed. If not, IV/IO dextrose △ Plumb. "
            "They go home when they eat and hold glucose, not after one prettier number."
        )
        sources.append(
            "Merck puppy hypoglycemia (toy breeds, first 6 months, frequent meals); "
            "Merck neonate management. Plunkett p334–335 traps only."
        )
        if toy:
            do_not.append(
                "An 8-week Yorkie is not an insulinoma puppy. Do not NPO a toy puppy."
            )
            do_next.append(
                "DDX still sepsis, PSS, parvo, parasites, xylitol. Frequent commercial puppy meals once swallowing."
            )
        if POUR_SUGAR_RE.search(text):
            hard_stops.append("Do not pour syrup into a collapsed mouth.")
        if INSULINOMA_RE.search(text) and toy:
            hard_stops.append("A toy puppy is not an insulinoma until the rare workup says so.")
        if toy and re.search(r"\bnpo\b|withhold food|no food", text, re.I):
            hard_stops.append("Do not NPO a toy puppy.")
        if toy and re.search(r"\b(keppra|levetiracetam)\b", text, re.I):
            hard_stops.append("Keppra does not raise glucose. Glucose first.")

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

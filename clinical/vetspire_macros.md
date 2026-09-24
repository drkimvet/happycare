# Vetspire macros — Midtown SA ER (DDX + discharge)

Neither these macros nor Instinct nor Plumb's replaces a veterinary license. △ every mg/kg in Plumb or the hospital protocol. Do not login to Vetspire from an agent. Paste these yourself: **More → Macros**. In an encounter box type `\` then the name.

Variables used are public Vetspire merge fields (`{{patient.name}}`, `{{patient.Pronoun}}`, `{{client.givenName}}`, `{{location.name}}`, `{{location.phonenumber}}`, `{{provider.name}}`, `{{date}}`, `{{usern.name}}`). Square brackets `[like this]` are for you to fill. Do not invent a dose in the brackets.

Owner-facing discharge has no chart IDs and no “typical” mg/kg. Clinician DDX lives in Assessment. Discharge lives in Discharge Instructions.

---

## Scope (they do not auto-apply throughout)

These are **shortcuts**, not a hospital-wide template that fills every box.

- **One box at a time.** Type `\` in Assessment for `ddx-*`. Type `\` again in Discharge Instructions for `dc-*`. Nothing else on the encounter fills itself.
- **Almost any text box**, including notes and emails. Not pop-out windows. Not the product-label discharge field in Inventory.
- **This patient only, when you insert.** `{{patient.name}}` and friends fill at insert time. They do not rewrite old charts.
- **Not every case type.** These are Midtown SA ER phrases. Wellness, dentistry, equine — different macros.
- **Location.** Saving under More → Macros lets people with access use them. **Make Universal** (admin permission) is what shares them to every UR VetCare location. Without that, they may stay Midtown-only.
- Encounter **templates** are separate. A template can sit under the macros; the macros still have to be inserted (or spoken to AI Scribe: “insert ddx-uo into Assessment”).
- **Household siblings are two patients.** Same snack ≠ same discharge. Insert `dc-gi` only if THIS cat has a GI / cranial-abdomen localization. Insert `dc-toxin` only if THIS cat has a toxin clock. Do not paste leftover dentistry or heart paragraphs. Do not write “below the toxic threshold.” Do not NPO a cat 12 hours.

---

## How to load

1. Vetspire → **More → Macros** → New.
2. **Name** = the `code` below (example `ddx-uo`).
3. Paste the body. Save.
4. In the encounter: `\` + name.

Suggested names are short so they show up after three letters.

| Code | Where | Use |
| --- | --- | --- |
| `ddx-master` | Assessment | Blank SA ER differential |
| `ddx-uo` | Assessment | Male cat straining |
| `ddx-aki` | Assessment | Azotemia / renomegaly |
| `ddx-addison` | Assessment | Addisonian crisis |
| `ddx-dka` | Assessment | DKA |
| `ddx-hhs` | Assessment | Hyperosmolar diabetic |
| `ddx-gdv` | Assessment | GDV |
| `ddx-sepsis` | Assessment | Sepsis / SIRS / septic shock |
| `ddx-pyo` | Assessment | Pyometra |
| `ddx-fate` | Assessment | Feline ATE |
| `ddx-lily` | Assessment | True lily |
| `ddx-peace` | Assessment | Peace/calla (not AKI lily) |
| `ddx-grape` | Assessment | Grape / tartaric |
| `ddx-apap` | Assessment | Acetaminophen |
| `ddx-xylitol` | Assessment | Xylitol |
| `ddx-eg` | Assessment | Ethylene glycol |
| `ddx-perm` | Assessment | Cat permethrin |
| `ddx-choc` | Assessment | Chocolate |
| `ddx-linear` | Assessment | Linear FB |
| `ddx-heat` | Assessment | Heatstroke |
| `ddx-sz` | Assessment | Seizure |
| `ddx-abd` | Assessment | Acute abdomen |
| `ddx-gi` | Assessment | Vomit/diarrhea |
| `ddx-ahds` | Assessment | AHDS / HGE / parvo |
| `ddx-eclampsia` | Assessment | Eclampsia / puerperal tetany |
| `ddx-dystocia` | Assessment | Dystocia / stuck labor |
| `ddx-larpar` | Assessment | Dog stridor / laryngeal paralysis |
| `ddx-hypogly` | Assessment | Toy puppy / neonatal hypoglycemia |
| `ddx-txrxn` | Assessment | Transfusion reaction |
| `ddx-vest` | Assessment | Vestibular / head tilt |
| `ddx-snake` | Assessment | Snakebite / pit viper / coral |
| `ddx-he` | Assessment | HE / ALF / head press |
| `ddx-propto` | Assessment | Traumatic proptosis |
| `ddx-neonate` | Assessment | Fading / newborn resuscitation |
| `ddx-mastitis` | Assessment | Mastitis / metritis / septic dam |
| `ddx-glaucoma` | Assessment | Acute glaucoma / hard eye |
| `ddx-uveitis` | Assessment | Anterior uveitis / flare |
| `ddx-lenslux` | Assessment | Anterior lens luxation |
| `ddx-hyphema` | Assessment | Hyphema / AC blood |
| `ddx-corneal` | Assessment | Corneal laceration / cat claw |
| `ddx-sards` | Assessment | Sudden blind / SARDS / RD |
| `ddx-eyelid` | Assessment | Eyelid / lid-margin laceration |
| `ddx-chemeye` | Assessment | Chemical / alkali ocular burn |
| `ddx-melt` | Assessment | Melting ulcer / descemetocele |
| `ddx-anes` | Assessment | SA anesthesia / sedation |
| `ddx-indolent` | Assessment | Indolent / Boxer / SCCED |
| `ddx-seq` | Assessment | Feline corneal sequestrum |
| `ddx-fhv` | Assessment | Feline herpes / dendritic ulcer |
| `ddx-fek` | Assessment | Feline eosinophilic keratitis |
| `ddx-kcs` | Assessment | KCS / dry eye / STT |
| `ddx-cherry` | Assessment | Cherry eye / nictitans gland |
| `ddx-dacryo` | Assessment | Dacryocystitis / NLD obstruction |
| `ddx-orbit` | Assessment | Orbital cellulitis / retrobulbar |
| `ddx-mmm` | Assessment | Masticatory myositis / trismus |
| `ddx-tetanus` | Assessment | Tetanus / risus / sawhorse |
| `ddx-tick` | Assessment | Tick paralysis / flaccid LMN |
| `ddx-botul` | Assessment | Botulism / carrion / spoiled food |
| `ddx-apn` | Assessment | APN / coonhound / raw chicken |
| `ddx-mg` | Assessment | Myasthenia / fulminant / megaesophagus |
| `ddx-trigem` | Assessment | Trigeminal neuritis / dropped jaw |
| `ddx-2m` | Assessment | 2M antibody ELISA / MMM confirm |
| `ddx-face` | Assessment | Facial paralysis / cannot blink |
| `ddx-polyp` | Assessment | Cat NP / aural inflammatory polyp |
| `ddx-horner` | Assessment | Isolated Horner / small pupil + ptosis |
| `ddx-aniso` | Assessment | Anisocoria / the big pupil |
| `ddx-optic` | Assessment | Dilated fixed pupil / optic neuritis |
| `ddx-cortex` | Assessment | Cortical / post-ictal blindness |
| `ddx-htn` | Assessment | Acute systemic hypertension / TOD |
| `ddx-phtn` | Assessment | Pulmonary hypertension / syncope / RHF |
| `ddx-hyperca` | Assessment | Feline hyperCa ± UTI |
| `ddx-resp` | Assessment | Dyspnea / cat open-mouth |
| `ddx-chf` | Assessment | CHF vs other shock |
| `ddx-anax` | Assessment | Anaphylaxis / vaccine / sting |
| `ddx-hemo` | Assessment | Hemoabdomen |
| `ddx-imha` | Assessment | IMHA |
| `ddx-tbi` | Assessment | Head trauma / TBI |
| `ddx-uroabd` | Assessment | Uroabdomen |
| `ddx-panc` | Assessment | Pancreatitis |
| `ddx-uti` | Assessment | Sporadic cystitis |
| `ddx-rabbit` | Assessment | Rabbit not eating |
| `dc-master` | Discharge | Generic ER home |
| `dc-return` | Discharge | Come-back triggers only |
| `dc-gi` | Discharge | GI home care |
| `dc-ahds` | Discharge | AHDS / bloody diarrhea |
| `dc-parvo` | Discharge | Parvo isolation / decline |
| `dc-eclampsia` | Discharge | Eclampsia / nursing tetany |
| `dc-dystocia` | Discharge | Dystocia / C-section / decline |
| `dc-larpar` | Discharge | Lar par / tie-back / decline |
| `dc-hypogly` | Discharge | Toy puppy hypoglycemia |
| `dc-txrxn` | Discharge | After a transfusion reaction |
| `dc-vest` | Discharge | Vestibular / head tilt |
| `dc-snake` | Discharge | Snakebite going home |
| `dc-he` | Discharge | Hepatic encephalopathy / liver |
| `dc-propto` | Discharge | After proptosis replace / enucleate |
| `dc-neonate` | Discharge | Fading neonate going home |
| `dc-mastitis` | Discharge | Mastitis / metritis dam |
| `dc-glaucoma` | Discharge | After acute glaucoma |
| `dc-uveitis` | Discharge | Anterior uveitis going home |
| `dc-lenslux` | Discharge | Anterior lens luxation / referral |
| `dc-hyphema` | Discharge | Hyphema going home / work-up |
| `dc-corneal` | Discharge | Corneal laceration / leak |
| `dc-sards` | Discharge | Sudden vision loss / referral |
| `dc-eyelid` | Discharge | After lid-margin repair |
| `dc-chemeye` | Discharge | After chemical / alkali eye flush |
| `dc-melt` | Discharge | Melting ulcer / descemetocele / referral |
| `dc-anes` | Discharge | After anesthesia / recovery |
| `dc-indolent` | Discharge | After indolent / SCCED debridement |
| `dc-seq` | Discharge | Corneal sequestrum / referral |
| `dc-fhv` | Discharge | Feline herpes keratitis / ulcer |
| `dc-fek` | Discharge | Eosinophilic keratitis / plaques |
| `dc-kcs` | Discharge | KCS / dry eye going home |
| `dc-cherry` | Discharge | Cherry eye / gland replacement |
| `dc-dacryo` | Discharge | After NL flush / dacryocystitis |
| `dc-orbit` | Discharge | Orbital cellulitis / abscess |
| `dc-mmm` | Discharge | Masticatory myositis / cannot open jaw |
| `dc-tetanus` | Discharge | Tetanus / lockjaw going home |
| `dc-tick` | Discharge | After tick paralysis search |
| `dc-botul` | Discharge | Botulism / spoiled-food watch |
| `dc-apn` | Discharge | APN / coonhound going home |
| `dc-mg` | Discharge | Myasthenia / megaesophagus watch |
| `dc-trigem` | Discharge | Trigeminal neuritis / cannot close |
| `dc-2m` | Discharge | 2M antibody pending / MMM |
| `dc-face` | Discharge | Facial paralysis / cannot blink |
| `dc-polyp` | Discharge | Cat polyp traction / VBO / look again |
| `dc-horner` | Discharge | Horner going home / ear and limb watch |
| `dc-aniso` | Discharge | Anisocoria / big pupil going home |
| `dc-optic` | Discharge | Sudden blind / dilated fixed / referral |
| `dc-cortex` | Discharge | Post-ictal / cortical blindness watch |
| `dc-htn` | Discharge | Systemic hypertension / BP / eye watch |
| `dc-phtn` | Discharge | Pulmonary hypertension / syncope watch |
| `dc-hyperca` | Discharge | HyperCa ± UTI two lists |
| `dc-uti` | Discharge | Confirmed UTI / cystitis |
| `dc-uo` | Discharge | Post-unblock / decline unblock |
| `dc-aki` | Discharge | Kidney / ureter |
| `dc-addison` | Discharge | Addison start |
| `dc-dka` | Discharge | DKA / decline ICU |
| `dc-toxin` | Discharge | Generic toxin |
| `dc-lily` | Discharge | Cat lily |
| `dc-gdv` | Discharge | GDV surgery / decline |
| `dc-resp` | Discharge | Cat respiratory distress |
| `dc-sepsis` | Discharge | Sepsis / source-control / decline |
| `dc-pyo` | Discharge | Pyometra |
| `dc-fate` | Discharge | FATE |
| `dc-heat` | Discharge | Heatstroke |
| `dc-anax` | Discharge | Anaphylaxis / hives going home |
| `dc-imha` | Discharge | IMHA / hemolysis |
| `dc-tbi` | Discharge | Head trauma |
| `dc-sz` | Discharge | Seizure |
| `dc-ama` | Discharge | Against medical advice |
| `dc-euth` | Discharge | Euthanasia / aftercare (no PHI) |
| `dc-rdvm` | Discharge | rDVM follow-up |

---

## DDX (Assessment)

### `ddx-master`

Assessment / DDX — {{patient.name}} ({{patient.species}}, {{patient.breed}}, {{patient.sexTerm}})
Date: {{date}}  Clinician: {{usern.name}}

Problem list:
1. [primary]
2. [secondary]
3. [comorbidity]

Localization: [organ / system]. What would flip the plan: [one datum].

Differential (most to least):
1. [ ]
2. [ ]
3. [ ]
4. [ ]
5. [ ]

Ruled in / out tonight:
- [test]: [result] → [keeps / drops]

Do not (night gates):
- No species, no dose.
- No invented mg/kg. △ Plumb / hospital protocol.
- No NSAID or DexSP if azotemic.
- Do not drain a free abdomen without paired fluid:serum Cr and K.

Plan:
- Diagnostics: [ ]
- Treatments given: [name only; dose from order]
- Disposition: [admit / sx / home / euth / AMA]
- Owner conversation: [referral / decompression / risk]

License: this note does not replace a veterinary license.

### `ddx-uo`

UO until proven otherwise — {{patient.name}}
Intact/neutered male cat + straining / no urine / vocalizing.

DDX:
1. Urethral obstruction (plug, stone, spasm, stricture)
2. FLUTD / FIC without obstruction
3. Ureteral obstruction / pyonephrosis (if one kidney big, belly soft)
4. Constipation (do NOT discharge on this without a bladder check)
5. Addisonian-like electrolyte picture (less common in cats)
6. Spinal / LMN bladder

Tonight: bladder size [ ], UOP [mL/kg/hr or not quantified], K [ ], ECG [ ], Cr [ ].
Do not: send home as constipated. No NSAID if azotemic. △ unblock/analgesic doses in Plumb.

### `ddx-aki`

AKI / ureter — {{patient.name}}
Cr [ ]  UOP [ ] mL/kg/hr  Side of renomegaly [R/L/none]  Abdomen [soft / tense]

DDX:
1. Ureteral obstruction / hydro / pyonephrosis (unilateral big kidney + soft belly)
2. Intrinsic AKI (lily, grape/tartaric if dog, EG, pyelo, ischemia, leptospirosis if dog)
3. CKD decompensation
4. Post-renal (UO, uroabdomen) — need fluid:serum Cr/K before a therapeutic tap
5. Addison (dog) mimicking azotemia

Do not: drain a soft non-tense belly. Do not call UOP ~1 mL/kg/hr oliguria. No NSAID. No DexSP. Hold AlOH if not eating. Pain is part of the plan. △ opioid in Plumb.
Owner talk if one kidney is fluid-filled and the other is compromised: referral / decompression / euthanasia, not “watch the belly.”

### `ddx-addison`

Addisonian crisis — {{patient.name}}
Shock + relative bradycardia + hyperK [ ] + hypoNa [ ] + GI.

DDX:
1. Primary hypoadrenocorticism (typical)
2. Atypical Addison (normal electrolytes — still on the list)
3. UO / uroabdomen / AKI (azotemia + hyperK)
4. Whipworm / severe GI loss
5. Sepsis / cardiogenic shock (wrong heart-rate story)

Do not: call it AKI or send home as gastroenteritis. Do not treat the K number alone. Do not give prednisolone/hydrocortisone before ACTH (contaminates assay). DexSP does not. Do not give insulin for hyperK until glucose is known. Do not copy 2013 NaCl recipe; do not jack chronic Na <120 (myelinolysis). Book cortisol mg/dL is a unit trap (µg/dL). △ fluids/steroid/DOCP in Plumb.

### `ddx-dka`

DKA — {{patient.name}}
Glucose [ ]  Ketones [strip/blood/BHB]  pH/HCO3 [ ]  K [ ]  P [ ]

DDX:
1. DKA
2. HHS (very high glucose/osmolality, little ketone)
3. Sepsis / pancreatitis / UTI triggering decompensation
4. Hepatic lipidosis (cat) or other ketosis
5. Addison + stress hyperglycemia (wrong picture)

Do not: insulin first if still a volume wreck or already hypokalemic. Do not default bicarbonate. Do not trust a negative urine strip (misses BHB). Do not copy 2013 40–60 mL/kg/h. Goal is stop ketogenesis, not euglycemia tonight. △ insulin CRI in Plumb.
Trigger hunt: [UTI / panc / steroids / SGLT2 / other]

### `ddx-hhs`

HHS — {{patient.name}}
Glucose [ ]  Osm [ ]  Ketones [absent/trace]  Na [ ]

Not DKA. Do not dump hypotonic fluid into chronic hypernatremia. Fluids first. △ insulin if used.

### `ddx-gdv`

GDV — {{patient.name}}
Large-breed / distention / nonproductive retch / shock.

DDX:
1. GDV
2. Food bloat without volvulus
3. Mesenteric volvulus
4. Splenic torsion
5. Severe pancreatitis / peritonitis

Do not: induce emesis. Do not “watch overnight.” Do not harvest 2013 OG-tube/trocar recipes. Do not invent a lactate cutoff. Do not trocar-and-home without a gastropexy conversation.
Right lateral [reverse C / double bubble]. Avoid VD. Shock type: obstructive + hypovolemic. Post-op VPCs delayed. △ fluids / lidocaine in Plumb.

### `ddx-sepsis`

Sepsis / SIRS — {{patient.name}}
Suspected infection + organ dysfunction / shock. Fever is not required.

DDX:
1. Sepsis / septic shock (name the pocket)
2. Anaphylaxis / distributive look-alike
3. Hypovolemic or cardiogenic shock without infection
4. Addison (dog) / SIRS without a source
5. Pyometra / septic abdomen / pyothorax / uroabdomen / pneumonia / bite / catheter

Do not: invent SIRS 2/4–3/4 or HR/WBC cutoffs. Do not invent a lactate/MAP veto. Do not harvest 2013 shock-dose / hetastarch. Do not lead with high-dose DexSP. Azotemic cat: still no DexSP. Antibiotics do not replace source control.
Shock type: distributive (± hypovolemic ± cardiogenic). Culture if it does not delay the first antimicrobial. △ fluids / antimicrobial in Plumb.

### `ddx-pyo`

Pyometra — {{patient.name}}
{{patient.sexTerm}}. Diestrus / PU-PD / sick / vaginal discharge [Y/N].

DDX:
1. Closed or open pyometra
2. UTI / pyelonephritis
3. Pregnancy / mucometra
4. GI / Addison / DKA look-alikes

Do not: send home as UTI. Stabilize then OHE unless a documented medical-breed plan. △ in Plumb.

### `ddx-fate`

FATE / ATE — {{patient.name}}
Painful, cold, pulseless hind limbs. 5 Ps.

DDX:
1. Arterial thromboembolism (HCM / heart)
2. Acute spinal (T3–L3 vs L4–S3) — pulses usually present
3. Saddle thrombus vs bilateral iliac
4. Severe hypoperfusion / shock without thrombus

Do not: promise thrombolysis. Do not skip analgesia. Echo when stable. Clopidogrel conversation △ Plumb (FAT CAT).

### `ddx-lily`

True lily AKI — {{patient.name}}
Cat + Lilium / Hemerocallis / pollen / vase water.

DDX:
1. Lily toxicosis → feline AKI
2. Other nephrotoxin (EG, NSAID, lily-of-the-valley is NOT this)
3. Ureteral obstruction
4. Peace/calla (oxalate) — only if the plant ID is those genera

Do not: wait for “just GI.” Do not run this protocol for peace/calla or Convallaria. IVF, baseline + serial Cr/UOP. △ in Plumb.

### `ddx-peace`

Peace / calla lily — {{patient.name}}
Spathiphyllum / Zantedeschia. Insoluble oxalate: oral pain, not feline AKI.

Do not run the Easter-lily AKI protocol. Supportive oral / GI care. Confirm plant ID.

### `ddx-grape`

Grape / raisin / tamarind / cream of tartar — {{patient.name}}
Dog. Merck 2024 tartaric-acid family. Ribes currants are not Vitis.

DDX: Vitis/tartaric AKI vs dietary indiscretion vs other nephrotoxin.
Do not: wait for “just GI.” Do not invent a toxic dose. Do not keep the 2013 “unknown principle” as current fact. △ decontam/IVF in Plumb.

### `ddx-apap`

Acetaminophen — {{patient.name}}
{{patient.species}}. Cat/ferret: contraindicated at analgesic intent.

DDX: APAP toxicosis (metHb / liver) vs other hepatotoxin vs anemia.
NAC family = acetaminophen only. Do not blend xylitol or hepatic-failure NAC. Charcoal can bind oral NAC; separate them. △ current Plumb/hospital load.

### `ddx-xylitol`

Xylitol — {{patient.name}}
Dog until proven otherwise. Glucose NOW.

DDX: xylitol (hypoglycemia then liver) vs other sugar-alcohol vs primary liver.
Charcoal does not bind xylitol (Merck). Do not mix xylitol NAC into the APAP family. △ dextrose / NAC in Plumb if used.

### `ddx-eg`

Ethylene glycol — {{patient.name}}
Do not wait for crystals. Fomepizole or ethanol early. Do not defer a known lick to a morning creatinine. △ antidote in Plumb.

### `ddx-perm`

Permethrin on a cat — {{patient.name}}
Often a dog spot-on. Tremors/seizures. Bath the product off.

Do not treat as organophosphate. Atropine is not the plan. Methocarbamol conversation △ Plumb.

### `ddx-choc`

Chocolate / methylxanthine — {{patient.name}}
Product: [ ]  Amount: [ ]  Time: [ ]
Calculate from the actual product. Do not quote a memorized mg/kg as Plumb. △ Plumb/ASPCA.

### `ddx-linear`

Linear / plastic FB — {{patient.name}}
String / floss / yarn / vinyl wrapper. Sheet vs strip [ ]. Wrapper actually missing from the pack [ ].
Check under the tongue.

Do not yank. Do not charcoal plastic. Do not clear on a normal radiograph (often radiolucent). Merck: sawing if linear. Imaging. Endoscopy if gastric; surgery if anchored / obstructed.

### `ddx-heat`

Heatstroke — {{patient.name}}
Tepid water + airflow. Stop cooling when temperature is falling. Hospital stop-number.

Do not use ice-water immersion as the default. Watch GI, kidney, neuro, coagulation.

### `ddx-sz`

Seizure — {{patient.name}}
Cluster / status / isolated. Glucose [ ]  Temp [ ]  Toxin [ ]

DDX: idiopathic epilepsy vs toxin vs hepatic vs electrolyte vs intracranial vs heat vs hypoglycemia. Nursing / postpartum: eclampsia until calcium says otherwise.
Toy puppy / neonate seizure: glucose first. Use `ddx-hypogly`. Do not keppra-and-home.
Do not invent a midazolam/phenobarbital number. △ crash-cart / Plumb.

### `ddx-abd`

Acute abdomen — {{patient.name}}
Pain [ ]  Tense vs soft [ ]  Shock [ ]

DDX: GDV, peritonitis, pancreatitis, obstruction / linear FB, hemoabdomen, uroabdomen, pyometra, obstipation, referred spinal.
Do not drain without fluid:serum Cr/K if uroabdomen is in play. Localize before you tap.

### `ddx-gi`

Vomit / diarrhea — {{patient.name}}
Acute vs chronic. Blood [Y/N]. Toxin / FB / diet [ ].

DDX: dietary / infectious / pancreatitis / FB / Addison / toxin / metabolic / obstruction.
Do not send a diestrus sick female as “GI.” Do not send a straining male cat as “GI.”
Dog + blood in the stool: bloody diarrhea is not a diagnosis. Use `ddx-ahds`. Parvo test if young or unvaccinated even if the stool is not red.

### `ddx-ahds`

AHDS / parvo — {{patient.name}}
Bloody diarrhea is a syndrome, not a diagnosis. PCV/TS [ ]  Parvo SNAP [ ]  Vax [ ]  Age [ ]

DDX:
1. AHDS (old HGE) — hemoconcentration, fluids first
2. Parvovirus (young / unvax / neutropenic; ~25% not bloody)
3. Addison
4. Anticoagulant rodenticide / ulcer
5. FB / intussusception / pancreatitis / sepsis

Do not: send shock home as colitis. Do not skip the parvo test because the stool is brown. Do not shotgun antibiotics onto every AHDS. Do not invent a PCV/WBC cutoff. Do not harvest ampicillin tables. Isolate if parvo. Offer food when vomiting allows. △ Plumb.

### `ddx-eclampsia`

Eclampsia — {{patient.name}}
{{patient.sexTerm}}. Nursing / days post-whelping [ ]  Litter size [ ]  Tremor / tetany / seizure [ ].

DDX:
1. Eclampsia / puerperal tetany (hypocalcemia)
2. Hypoglycemia
3. Toxin / heat / primary epilepsy
4. Hypoparathyroidism (not the default nursing picture)

Do not: wait for the printer on classic tetany. Do not harvest calcium mL/kg. Do not give calcium chloride SQ. Do not load oral calcium during pregnancy (predisposes). Do not ice-water tetany fever as primary heatstroke. Glucose now. Interrupt nursing tonight. △ Plumb.

### `ddx-dystocia`

Dystocia — {{patient.name}}
{{patient.sexTerm}}. Whelping / queening. Green discharge before first baby [Y/N]. Pups out [ ]. Strain without delivery [ ].

DDX:
1. Uterine inertia (primary / secondary) — glucose and calcium on the list
2. Obstructive dystocia (malposition, oversized, narrow pelvis, brachycephalic)
3. Maternal illness / uterine rupture / torsion
4. Eclampsia overlapping labor

Do not: oxytocin into an obstruction. Do not send oxytocin home with the breeder. Do not harvest IU or hour-between-pups tables. Do not yank a stuck fetus. Green/black before baby one is placental separation — come now. C-section if stuck, distressed, or medical fails. △ Plumb.

### `ddx-hypogly`

Toy / neonatal hypoglycemia — {{patient.name}}
{{patient.species}}. Age [weeks]. Toy breed [Y/N]. Glucose [now / not yet]. Eating [Y/N]. Temp [ ].

DDX:
1. Transient toy-breed / neonatal hypoglycemia (missed meals, hepatic immaturity)
2. Sepsis / parvo / endotoxemia
3. Portosystemic shunt / hepatic
4. Parasites / malnutrition / xylitol
5. Insulinoma — older dog, not an 8-week Yorkie

Do not: keppra-first epilepsy. Pour syrup into a collapsed mouth. Harvest 2013 25%/50% dextrose tables. NPO. Send home still not eating. Call this insulinoma in a neonate.
Do next: glucose now, warm, feed if they can swallow, IV/IO dextrose △ Plumb if not. Frequent puppy meals. They hold glucose before discharge.

### `ddx-txrxn`

Transfusion reaction — {{patient.name}}
{{patient.species}}. Product [pRBC / whole blood / FFP]. Typed [DEA 1 / AB]. Crossmatch [ ]. Minutes into bag [ ].

DDX:
1. Acute hemolytic (AHTR) — pigment, PCV that did not rise
2. Febrile non-hemolytic (exclusion after you look)
3. TACO (overload) vs TRALI (uncommon)
4. Allergic / anaphylaxis (cat: often respiratory)
5. Bacterial contamination of the unit

Do not: restart the same unit. Diphenhydramine-first for hemolysis or shock. Harvest 2013 rates or diphen numbers. Universal-donor cat blood. Type A into a type B cat. Dog-to-cat xenotransfusion as default. Invent a PCV trigger. Mix calcium fluids in the line. DexSP if azotemic.
Do next: **stop the bag first.** Save the unit. Recheck PCV/TS, pigment, temp. Type and XM as indicated. TACO: no more volume. Anaphylaxis: epinephrine. △ hospital blood bank.

### `ddx-larpar`

Laryngeal paralysis / GOLPP — {{patient.name}}
{{patient.species}}. Inspiratory stridor / voice change / noisy pant. Breed/age [old large-breed vs toy honk].

DDX:
1. Laryngeal paralysis (idiopathic / GOLPP)
2. Laryngeal mass / foreign body / trauma
3. Tracheal collapse (toy-breed honk — different dog)
4. Aspiration pneumonia sitting on top of the airway
5. Heatstroke / obstruction edema
6. CHF (do NOT default Lasix because they are noisy)

Do not: Lasix + albuterol cocktail. Kennel cough. Ice-water. Wrestle for rads (rads are not diagnostic of the larynx). Harvest 2013 ace/butorphanol/DexSP/propofol/doxapram tables. Throat-exam a crashing dog without a tube ready. Flood with fluids. DexSP if azotemic.
Do next: oxygen, tepid cool, △ sedation. Crash: intubate or tracheostomy. Aspiration on the list once stable. Tie-back is the surgery conversation. GOLPP hindlimb later — tonight is the airway. Cats are uncommon; still name the space.

### `ddx-vest`

Vestibular — {{patient.name}}
Head tilt [L/R]. Nystagmus [horizontal / rotary / vertical]. Mentation [alert / dull]. Horner [Y/N]. Facial [Y/N]. Metro on board [Y/N].

DDX:
1. Peripheral idiopathic (geriatric) — exclusion, usually no Horner
2. Otitis interna / media (Horner + facial = the ear)
3. Metronidazole neurotoxicity — stop the drug
4. Central (MUO, infarct, tumor, FIP, thiamine) if vertical nystagmus / CP / dull
5. Hypothyroid neuropathy / polyp (cat) / ototoxin

Do not: DexSP/mannitol “stroke.” Harvest 2013 meclizine/diazepam tables. Chlorhex/aminoglycoside drops if TM not seen. Send dull + vertical nystagmus home as just old. Force-walk a rolling dog.
Do next: otoscopic exam, both ears. Peripheral vs central before home. Antiemetic △ Plumb. Stop metronidazole if listed.

### `ddx-snake`

Snakebite — {{patient.name}}
{{patient.species}}. Pit viper vs coral [ ]. Swelling mark time [ ]. Coags / echinocytes [ ]. Neuro [ ]. Spreading [Y/N].

DDX:
1. Crotalid (pit viper) envenomation — local swelling, necrosis, coagulopathy
2. Elapid (coral) — little local, neurologic, ventilate
3. Dry bite — do not send a spreading limb home on that word
4. Trauma / cellulitis / abscess / antivenom anaphylaxis

Do not: ice, cut, suck, tourniquet, electric shock. Chase the snake. Harvest appendix 1–5 vials or Merck epi mL. NSAID. DexSP-first. Fasciotomy as default. Vaccine as antivenom. Azotemic: still no DexSP.
Do next: quiet, limit activity. Antivenom is the specific △ hospital stock. Mark swelling. Coral: ventilate. Anaphylaxis: epinephrine first.

### `ddx-he`

HE / ALF — {{patient.name}}
{{patient.species}}. Glucose [ ]. Mentation [ ]. Jaundice [ ]. Ammonia [if drawn — not required]. Biurate crystals [Y/N]. Toxin [sago / xylitol / APAP / mushroom / none]. Swallowing [Y/N].

DDX:
1. Type A — fulminant hepatic failure (toxin, lepto, copper + NSAID, sepsis)
2. Type B — congenital / acquired portosystemic shunt (not the same as FHF)
3. Type C — cirrhosis + acquired shunts
4. Neuroglycopenia / thiamine / electrolyte lookalikes

Do not: benzodiazepines for HE. Pour lactulose into a somnolent mouth. Harvest 2013 20 mL/kg enemas or book NAC 50. Routine FFP for a long PT. DexSP / glucocorticoid. Default starve / l/d. Ammonia-tolerance test tonight. Mix NAC families.
Do next: glucose now. Lactulose if they can swallow △ Plumb. Name the toxin. HE seizure: levetiracetam. Plasma if bleeding.

### `ddx-propto`

Proptosis — {{patient.name}}
{{patient.species}} [brachy Y/N]. Lubricated [Y/N]. Pupil / PLR [ ]. Other eye [ ]. Extraocular muscles [count]. Globe intact [Y/N]. Other trauma [ ].

DDX / plan:
1. Traumatic proptosis — lids behind the equator
2. Replace + temporary tarsorrhaphy if globe intact
3. Enucleate if rupture / ≥3 extraocular muscles / optic-nerve avulsion
4. Concurrent HBC / bite / skull — ABC first

Do not: send a dry globe home. Lobby push without anesthesia. Harvest 2013 3-hour or flunixin tables. DexSP-first. Promise vision. Chlorhex in the eye. Steroid drop on an ulcer.
Do next: lubricate now. Replacement or enucleation tonight. E-collar. Cat: vision grave. △ Plumb.

### `ddx-neonate`

Fading / newborn — {{patient.name}}
Age [hours/days]. Temp [ ]. Glucose [ ]. Nursing [Y/N]. Umbilicus [ ]. Dam: type B [Y/N] mastitis/metritis [ ]. Congenital [cleft / atresia].

DDX:
1. Hypothermia / hypoglycemia / hypoxia (ABC, warm before feed)
2. Sepsis / omphalitis
3. Neonatal isoerythrolysis (type B queen)
4. Congenital defect / fading is not a diagnosis

Do not: swing. Routine doxapram. Atropine for neonatal bradycardia. Tube-feed a cold gut. Adult CPR cart. Harvest 80–100 mL/kg or Merck 0.0002 mg/g. Send home as small of the litter.
Do next: warm, rub, PPV if not vigorous. Glucose now. Look at dam and umbilicus. △ newborn crash-cart / Plumb.

### `ddx-mastitis`

Mastitis / metritis — {{patient.name}}
Postpartum day [ ]. Temp [ ]. Glands [which / gangrene Y/N]. Milk appearance [ ]. Lochia [odor / amount]. Eating [ ]. Neonates [nursing / fading].

DDX:
1. Mastitis (one or many glands) — culture even if milk looks normal
2. Metritis (not diestrus pyometra; SIPS is not systemically sick)
3. Both (hematogenous)
4. Sepsis / peritonitis / eclampsia / inflammatory mammary carcinoma

Do not: send a septic dam home as sore milk. Harvest cephalexin / PGF / oxytocin IU or 1% iodine flush. DexSP. NSAID if septic/azotemic. Wean the whole litter from one sore gland. Cabbage-only shock.
Do next: name the gland or the uterus. Gangrene is surgery tonight. Look at the neonates. Nursling-safe antibiotic △ Plumb.

### `ddx-glaucoma`

Acute glaucoma — {{patient.name}}
IOP OD [ ]  OS [ ]  fluorescein [ ]  lens [in situ / anterior / not seen]  other eye [ ].

DDX:
1. Primary glaucoma
2. Secondary (uveitis / lens luxation / intraocular tumor)
3. Not conjunctivitis until IOP is measured

Do not: send home as conjunctivitis. Atropine. Latanoprost before the lens is seen. Intravitreal gentamicin in a cat. Steroid drop on an ulcer. Harvest 2013 mmHg / mannitol / oral-CAI tables. DexSP if azotemic.
Do next: measure IOP now if globe intact. Fluorescein first. Check the lens before latanoprost. Lower pressure tonight △ Plumb / hospital. Check the other eye.

### `ddx-uveitis`

Anterior uveitis — {{patient.name}}
IOP [usually low / normal / high]  fluorescein [ ]  flare [ ]  miosis [ ]  OU vs OS/OD [ ]. Systemic signs [ ].

DDX:
1. Infectious / immune / neoplastic / traumatic / lens-induced
2. Cat: FeLV / FIV / FIP / toxo / crypto still on the list
3. Secondary glaucoma if IOP is not low
4. Not conjunctivitis until IOP and stain are done

Do not: send home as conjunctivitis. Steroid drop on an unstained cornea. Atropine if IOP is high. DexSP-only in a cat. Harvest 2013 atropine / NSAID tables. DexSP / NSAID if azotemic.
Do next: measure IOP. Fluorescein first. Find the cause. Atropine only on a hypotonic eye △ Plumb.

### `ddx-lenslux`

Lens luxation — {{patient.name}}
Lens [anterior / posterior / sublux / aphakic crescent]. IOP off the lens [ ]. Visual [dazzle / consensual]. Other eye [ ]. Breed [terrier / Shar-Pei / other].

DDX:
1. Primary (terrier / Shar-Pei, ADAMTS17)
2. Secondary (chronic uveitis — cats; hypermature cataract; chronic glaucoma)
3. Anterior luxation is not posterior luxation

Do not: latanoprost / miotics. Measure IOP on top of the lens. Harvest Merck mannitol g/kg. Treat posterior lux as tonight's ICLE. Send home if IOP is high.
Do next: refer tonight. Visual → lens-out conversation. Blind → globe-out. Check the other eye. △ Plumb / hospital.

### `ddx-hyphema`

Hyphema — {{patient.name}}
Hyphema is a sign, not a diagnosis. Stain [ ]  IOP [ ]  BP [ ]  platelets [ ]  petechiae [ ]  trauma [ ].

DDX:
1. Trauma
2. Uveitis / neoplasia / retinal tear
3. Hypertension
4. Coagulopathy / rodenticide / platelets
5. Not “just a red eye”

Do not: send home as red eye. Aspirin / NSAID for the bleed. Harvest pilocarpine / epinephrine / tPA-as-grams. Steroid on an ulcer. DexSP if azotemic.
Do next: fluorescein, IOP, BP, platelets. Quiet + E-collar. Treat the cause. TPA is not the night default. △ Plumb.

### `ddx-corneal`

Corneal laceration / cat claw — {{patient.name}}
Seidel [ ]  iris prolapse [ ]  lens [intact / capsule torn / not seen]  FB [surface / deep / intraocular]. Visual [dazzle / consensual].

DDX:
1. Partial-thickness laceration
2. Full-thickness / leak / iris prolapse
3. Lens capsule rupture (cat claw in a young dog)
4. Melting ulcer / descemetocele

Do not: yank a deep FB in the lobby. Send a leaking globe home. Steroid on a stain-positive cornea. Harvest 7–0 / 9–0 or 2 mm lens-capsule tables.
Do next: stain + Seidel. Look at the lens. E-collar. Offer referral. Lens-capsule rupture can be medical; still offer surgery. Cats: traumatic lens sarcoma conversation.

### `ddx-sards`

Sudden blindness — {{patient.name}}
Menace [ ]  dazzle [ ]  PLR [ ]  fundus [quiet / detached / not seen]  BP [ ]. History: enrofloxacin [ ] ivermectin [ ] PU/PD/PP [ ].

DDX:
1. Opaque media (already gated)
2. Retinal detachment (hypertension, mycosis, lens surgery, Shih Tzu / CEA)
3. SARDS (dog; ERG flat; fundus quiet at first)
4. Optic pathway (ERG normal → neuro)
5. Ivermectin / cat enrofloxacin

Do not: call it SARDS without an ERG. Pred / DexSP a hypertensive cat. Harvest book pred 1.0 for SARD. Skip the drug history.
Do next: name the space. BP now. Fundus or B-scan. Offer ERG / referral. Merck: no effective SARDS treatment reported.

### `ddx-eyelid`

Eyelid laceration — {{patient.name}}
Margin involved [Y/N]. Medial canthus / punctum [ ]. Fluorescein [ ]. Blink [ ]. Other trauma [ ].

DDX:
1. Lid-margin laceration (notch if not aligned)
2. Skin-only lid cut
3. Concurrent corneal / globe injury
4. Medial canthus / canaliculus involvement

Do not: glue-and-home a margin cut. Knot on the cornea. Chlorhex in the eye. Harvest 3–0 to 6–0. Skip the globe.
Do next: repair tonight. Two-layer. Figure-of-eight at the margin. E-collar. Tarsorrhaphy if they cannot blink. △ hospital suture cart.

### `ddx-chemeye`

Chemical / alkali eye — {{patient.name}}
Agent [alkali / acid / bleach / drain cleaner / unknown]. Lavage started [ ]. Minutes flushed [ ]. Lids / fornices / third eyelid swept [ ]. Fluorescein AFTER lavage [ ]. Ingested too [Y/N].

DDX:
1. Alkaline ocular burn (liquefactive; deeper; may take 12 h)
2. Acid ocular burn (coagulative; pain often limits exposure)
3. Retained product under lids / third eyelid
4. Concurrent ingested corrosive (no emesis)

Do not: neutralize (book boric-acid ointment is a trap; Merck: exothermic). Harvest 2 liters. Topical steroid. Send home still burning. Harvest an acetylcysteine table.
Do next: lavage now. Water or 0.9% saline, minimum of 20 minutes. Fluorescein after. E-collar. Pain △ Plumb.

### `ddx-melt`

Melting ulcer / descemetocele — {{patient.name}}
Depth [superficial / stromal / descemetocele / perforated]. Malacia [Y/N]. Seidel [ ]. STT [ ]. Cytology [ ]. Culture [aerobic + fungal]. Cause [KCS / lids / FB / unknown].

DDX:
1. Melting stromal ulcer (proteinase; infected until cytology says otherwise)
2. Descemetocele (fragile globe; surgery tonight)
3. Perforation / iris prolapse
4. Indolent superficial (Boxer) — not tonight’s melt; do not grid a melt or a cat

Do not: send a melting eye home. Steroid a melt. Grid a melt. Harvest serum q-hours / acetylcysteine. BNP in a cat. Systemic enro in a cat.
Do next: cytology and culture. Serum △ hospital. E-collar. Refer tonight if melting, deep, or Descemet is showing. △ Plumb.

### `ddx-anes`

Anesthesia — {{patient.name}}
ASA [framework only]. Dedicated anesthetist [Y]. ETCO2 confirms tube [ ]. Pop-off [open]. Circuit [RC / NRC]. ACE-I held [ ]. Insulin [not full if fasted]. Recovery plan [ ].

Do not: treat recovery as “done.” Oxygen-flush a non-rebreathing. Closed pop-off. Harvest AAHA mg/kg figures or MAP/ETCO2 bands. Grain-free echo as gospel. NSAID if azotemic.
Do next: recovery is still anesthesia. Hands-on + ETCO2 / SpO2 / BP / temp. Name the hypotension before a bolus. Disconnect before you turn. △ Plumb / hospital.

### `ddx-indolent`

Indolent / Boxer / SCCED — {{patient.name}}
Depth [superficial / stromal / melt]. Epithelial lip [Y/N]. STT [ ]. Lids / FB / cilia [ ]. Species [dog / cat].

DDX:
1. Indolent / SCCED (loose lip; Boxer over-represented)
2. Melting / deep stromal (other list — do not grid)
3. KCS / lid / ectopic cilia as the reason it will not heal
4. Cat: herpes / sequestrum — do not grid a cat

Do not: grid a cat. Treat a melt as a Boxer ulcer. Steroid on a stain-positive cornea. Antibiotic drops alone.
Do next: dogs — dry CTA then diamond burr or grid △ hospital. E-collar. Soft CL △ hospital.

### `ddx-seq`

Corneal sequestrum — {{patient.name}}
Color [brown / black]. Depth [hidden / superficial / deep]. Pain [ ]. Prior grid [Y/N]. Brachy / herpes [ ].

DDX:
1. Feline corneal sequestrum (necrotic stroma; unique to the cat)
2. Pigment / FB / melanoma (if not a plaque)
3. Melting ulcer underneath (other list)

Do not: pick or peel it. Grid a cat. Send home as “it will slough.” Harvest a keratectomy table.
Do next: E-collar. Keratectomy of the whole plaque. Graft if deep. Depth may be hidden. △ Plumb.

### `ddx-fhv`

FHV / dendritic ulcer — {{patient.name}}
Dendritic / geographic [ ]. URI / sneezing [ ]. Stain [fluorescein / rose bengal]. STT / lids / FB [ ]. Depth [superficial / melt / descemetocele].

DDX:
1. Feline herpes keratitis (dendritic confirms; geographic = coalesced dendrites)
2. Mechanical ulcer (lids / STT / FB) — still look
3. Melting / descemetocele (other list — not “just herpes”)
4. Sequestrum if a brown/black plaque is already there

Do not: steroid a stain-positive / FHV ulcer. Grid a cat. Send a melting eye home as just herpes. Harvest an antiviral or l-lysine table. Require PCR tonight.
Do next: E-collar. Antiviral △ Plumb / hospital. Lids / STT / FB. If melting or Descemet showing, refer tonight.

### `ddx-fek`

Eosinophilic keratitis — {{patient.name}}
Color [pink / white]. Limbal [Y/N]. Stain [ ]. Cytology [eos / not yet]. URI / dendrites [ ]. Lip lesion [Y/N].

DDX:
1. Feline eosinophilic keratitis (cytology confirms)
2. FHV ulcer / stromal keratitis (stain first — no steroid if open)
3. Sequestrum if brown/black
4. Lip rodent ulcer is the skin complex, not this cornea

Do not: steroid a stain-positive cornea. Grid a cat. Valacyclovir. Megestrol as the night default. Harvest CSA / dex percents. Send home as conjunctivitis.
Do next: fluorescein. Cytology of the plaque. FHV on the list. Immunomodulation △ ophtho / hospital after the stain. E-collar.

### `ddx-kcs`

KCS / dry eye — {{patient.name}}
STT [before drops / spoiled]. Stain [ ]. Discharge [mucopurulent / mucoid]. Neurogenic [dry nostril Y/N]. Sulfa [Y/N]. Cherry-eye history [ ].

DDX:
1. Quantitative KCS (aqueous deficiency; STT before drops)
2. Qualitative dry eye (STT may be normal)
3. Ulcer / melting on a dry eye (other list — no steroid)
4. Cat: FHV scarring

Do not: send home as conjunctivitis. Steroid combo on an ulcer. Atropine. Skin tacrolimus in the eye. Harvest CSA / STT ≥ 2 mm. Excise a cherry-eye gland.
Do next: fluorescein. Artificial tears. Lacrimogenic △ Plumb. If melting, refer tonight.

### `ddx-cherry`

Cherry eye — {{patient.name}}
Side [L / R / both]. Exposed / dry [ ]. Stain [ ]. STT [ ]. Other eye [ ].

DDX:
1. Prolapsed nictitans gland (cherry eye — a tear gland)
2. Scrolled nictitans cartilage / mass (not the default in a young brachy)
3. Horner / Haw's (whole third eyelid, no gland mass)

Do not: excise it. Cut it off in the lobby. Harvest a pocket recipe or later-KCS percents. Send a dry gland home as it will go back.
Do next: lubricate. Stain. STT. Replacement / pocket conversation. Look at the other eye.

### `ddx-dacryo`

Dacryocystitis / NLD — {{patient.name}}
Medial canthus [swell / fistula]. Jones [ ]. Flush [ ]. Tooth / carnassial [ ]. Culture [ ].

DDX:
1. Dacryocystitis / nasolacrimal obstruction (debris / FB / mass)
2. Carnassial tooth-root abscess (lookalike)
3. Refractory conjunctivitis that is actually overflow

Do not: send home as conjunctivitis. Skip the tooth. Harvest 2–0 nylon or a rabbit flush calendar. Flush a melting globe.
Do next: stain. Jones test. Flush △ hospital. Culture reflux. Image if flush fails.

### `ddx-orbit`

Orbital cellulitis — {{patient.name}}
Pain opening mouth [ ]. Exophthalmos [uni / bi]. Last molar swell [ ]. Tooth roots [ ]. Stain / blink [ ].

DDX:
1. Orbital cellulitis / retrobulbar abscess (painful mouth)
2. Tooth-root / grass awn / zygomatic sialadenitis
3. Hemorrhage or neoplasia if the mouth is painless
4. Proptosis if the lids are behind the globe (other list)

Do not: send home as conjunctivitis. Call it proptosis. Drain in the lobby without a protocol. Harvest a 4–8 week antibiotic table.
Do next: lubricate. Systemic antimicrobial △ Plumb. Drain behind the last molar if swollen △ hospital. Image if it relapses.

### `ddx-mmm`

Masticatory myositis — {{patient.name}}
Jaw open [mm / cannot]. Muscles [swollen / atrophied]. Limbs [normal]. 2M drawn before steroid [Y/N]. Serum frozen [Y/N]. Exophthalmos [ ].

DDX:
1. Masticatory myositis (type 2M; limbs spared)
2. Orbital cellulitis if one globe + last-molar swell (other list)
3. Tetanus if risus / sawhorse / generalized spasm
4. Polymyositis if the limbs are involved (2M negative)
5. Trigeminal neuritis if cannot close / dropped jaw (other list)

Do not: pry the jaw open. Steroid before the titer. Send home as picky. Harvest the printed steroid mg/kg. Harvest 1:100 / 1:500. Follow the titer for response.
Do next: serum for 2M ELISA before immunosuppression. Freeze if you treat tonight. Soft gruel or feeding tube. Immunosuppression △ Plumb.

### `ddx-tetanus`

Tetanus — {{patient.name}}
Wound [found / healed / not found]. Risus / sawhorse / third-eyelid spasm [ ]. Jaw [trismus / opens]. Limbs [stiff / normal]. Noise trigger [ ].

DDX:
1. Tetanus (C. tetani / tetanospasmin; consciousness spared)
2. Masticatory myositis if isolated jaw + temporalis + limbs normal (other list)
3. Strychnine if minutes after a bait (other conversation)
4. Distemper myoclonus if young / unvaccinated

Do not: pry the jaw open. Send home as just lockjaw. Harvest antitoxin IU or metro mg. DexSP as the plan.
Do next: quiet / dark. Search and debride the wound △ hospital. Antitoxin / metro / sedation △ Plumb. Soft food or airway.

### `ddx-tick`

Tick paralysis — {{patient.name}}
Coat search [done / repeat]. Tick or crater [found / not found]. Site [ears / toes / mouth / anus / other]. Limbs [ascend / tetra]. Chest [ ].

DDX:
1. Tick paralysis (flaccid ascending LMN; consciousness spared)
2. Botulism if carrion / spoiled food
3. Acute polyradiculoneuritis / fulminant MG
4. Coral / elapid if little local swell + neuro (other list)
5. Tetanus only if risus / sawhorse (other list)

Do not: treat flaccid as tetanus. Send home as just tired. Harvest TAS mL/kg (not commercial in the US).
Do next: search the whole coat again. Remove every tick. Respiratory watch. Acaricide △ hospital.

### `ddx-botul`

Botulism — {{patient.name}}
Carrion / spoiled food [ ]. Swallow / chew [ ]. Limbs [flaccid / tetra]. Chest [ ].

DDX:
1. Botulism (preformed toxin; ACh block)
2. Tick paralysis until the coat is searched
3. Acute polyradiculoneuritis / fulminant MG
4. Coral / elapid if the geography fits

Do not: harvest type A–E / 10 000-unit tables. Treat flaccid as tetanus. Aminoglycoside as the night antibiotic.
Do next: search the coat anyway. Respiratory watch. Antitoxin △ Plumb if toxin may still be circulating.

### `ddx-apn`

Acute polyradiculoneuritis — {{patient.name}}
Coat search [clear / tick found]. Raccoon [ ]. Raw chicken [ ]. Vaccine [1–2 wk / no]. Tail wag [ ]. Bladder [ ]. Chest [ ].

DDX:
1. APN / Coonhound (ventral roots; steroids are not helpful)
2. Tick paralysis until the coat is searched
3. Botulism if carrion / spoiled food
4. Fulminant MG if megaesophagus
5. Puppy bunny-hop rigidity = protozoal PRN (other conversation)

Do not: DexSP / pred as the plan. Send home as just tired. Harvest Tensilon mg. Skip the coat search.
Do next: respiratory watch. Supportive. Weeks to months. Physical therapy conversation.

### `ddx-mg`

Myasthenia gravis — {{patient.name}}
Form [focal / generalized / fulminant]. Megaesophagus [ ]. Exercise-rest [ ]. AChR drawn [ ]. Aspiration [ ].

DDX:
1. Fulminant MG if acute flaccid + megaesophagus
2. Generalized MG if rest-improves
3. Focal MG if face / pharynx / esophagus only
4. Tick / botulism / APN until those are off
5. Congenital if a young terrier (other conversation)

Do not: harvest Tensilon / pyridostigmine mg. Send regurg home as just GI. DexSP-first before the titer.
Do next: AChR antibody. Edrophonium △ Plumb if generalized. Upright feeding. Respiratory watch.

### `ddx-trigem`

Trigeminal neuritis — {{patient.name}}
Jaw [cannot close / dropped]. Eat / drink [ ]. Horner / facial / sensation [ ]. Trauma / TMJ [ ]. Vaccine / endemic [ ].

DDX:
1. Idiopathic trigeminal neuropathy (cannot close; recover 3–4 weeks)
2. Masticatory myositis if cannot open + temporalis (other list)
3. TMJ luxation / jaw fracture if trauma
4. Rabies if unvaccinated / endemic / other neuro
5. Lymphoma / protozoa if a cat or they do not recover

Do not: pry the jaw. Send home as picky. Harvest a steroid table. Call it MMM.
Do next: fluids and nutrition. Soft food or feeding tube. Lubricate if they cannot blink.

### `ddx-2m`

2M antibody ELISA — {{patient.name}}
Serum drawn before steroid [Y/N]. Tube [serum / whole blood]. Frozen [Y/N]. Already on steroid [ ]. Titer pending [ ]. Atrophy / fibrosis [ ].

DDX:
1. MMM if cannot open + 2M positive (confirms)
2. Still MMM if negative after steroids or fibrotic end-stage → temporalis biopsy (not frontalis)
3. Polymyositis if limbs involved (2M negative)
4. Trigeminal neuritis if cannot close (other list)

Do not: harvest 1:100 / 1:500. Follow the titer for response. Call a post-steroid negative a rule-out. Biopsy the frontalis. Send home pending as picky.
Do next: serum, not whole blood. Freeze if you treat tonight. Watch jaw motion, not the number. Immunosuppression △ Plumb after the draw.

### `ddx-face`

Facial paralysis — {{patient.name}}
Blink / palpebral [absent / weak / present]. Sensation [intact / reduced]. Horner [Y/N]. Head tilt [Y/N]. STT [ ]. Stain [ ]. Ear / TM [seen / not seen]. Dry nostril [Y/N].

DDX:
1. Idiopathic CN VII (exclusion; common in dogs, uncommon in cats)
2. Otitis media / interna if Horner ± tilt (other list)
3. Neurogenic KCS / dry nostril if the lesion is proximal
4. Hypothyroid neuropathy in the dog (not a T4 cutoff tonight)
5. Brainstem if other CN / mentation / ipsilateral limbs
6. Trauma / TECA / middle-ear mass / cat polyp

Do not: send home as conjunctivitis or just a droopy face. Call Horner this disease (Horner can blink). Harvest a steroid table. Skip the ear.
Do next: lubricate now. STT. Stain. Look in both ears. Artificial tears. Watch the cornea.

### `ddx-polyp`

Nasopharyngeal / aural polyp — {{patient.name}}
Age [ ]. Stertor [Y/N]. Soft palate retracted [Y/N]. Ear L / R [seen / not]. TM [intact / not seen]. Horner [Y/N]. Facial [Y/N]. Tilt [Y/N]. Imaging [none / bulla rads / CT].

DDX:
1. Inflammatory polyp (benign stalk from bulla / tube / pharynx; young cat)
2. Otitis media / interna if Horner ± facial ± tilt (other list)
3. Nasopharyngeal mass / foreign body / severe URI if only stertor
4. Cholesteatoma is the dog destructive cyst — rare in cats

Do not: send home as just URI or just a cold. Treat as otitis externa only. Call it cancer tonight. Harvest a traction-versus-VBO steroid table. Skip the palate.
Do next: both ears. Retract the soft palate. Traction if you can grab it; stalk left can grow back. VBO conversation if the canal is stenotic or the bulla is the home. Culture the bulla △ Plumb.

### `ddx-horner`

Horner — {{patient.name}}
Blink [present / absent]. Miosis [Y/N]. Ptosis [Y/N]. Third eyelid [ ]. Stain [ ]. Ear / TM [seen / not]. Facial [Y/N]. Tilt [Y/N]. Thoracic limb / cutaneous trunci [normal / flaccid / lost].

DDX:
1. Isolated Horner (sympathetic; they can blink) — still look in the ear
2. Otitis media / interna if facial ± tilt (other list)
3. T1–T2 / brachial plexus if the ipsilateral thoracic limb is dead
4. C1–C5 / C6–T2 myelopathy if the matching limbs are weak
5. Uveitis / ulcer / drugs if you have not stained (not Horner yet)

Do not: send home as conjunctivitis or just a small pupil. Call this CN VII (they blink). Call the small pupil CN III. Harvest a 1st/2nd/3rd-order or phenylephrine-minute table. Skip the ear because the face is normal.
Do next: stain. Both ears. Feel the limb and cutaneous trunci. Cat: polyp stays on the list.

### `ddx-aniso`

Anisocoria / big pupil — {{patient.name}}
Which pupil is wrong [big / small / not sure]. Vision [yes / no]. PLR big [Y/N]. PLR small [Y/N]. Stain [ ]. STT [ ]. IOP [ ]. Iris margin [scalloped / holes / normal]. Gut / bladder / dry eye [ ].

DDX:
1. Iris atrophy if old dog, scalloped pupil, vision stays
2. Atropine / parasympatholytic drop if the history fits
3. CN III / brainstem if other CN, mentation, or limbs go with it
4. Dysautonomia if bilateral mydriasis plus gut / bladder / third eyelid (other list)
5. Retina / optic nerve if big + blind + no PLR
6. Glaucoma if red, painful, cloudy — measure IOP (other list)

Do not: call the big pupil Horner. Call old-dog iris atrophy a CN III emergency. Harvest a dilute pilocarpine table. Send home as conjunctivitis or just a funny pupil. Dilate a high-IOP eye.
Do next: name which pupil is wrong. Stain. STT before drops. IOP if red / painful / cloudy.

### `ddx-optic`

Dilated fixed / optic neuritis — {{patient.name}}
Vision [none / reduced]. PLR [absent / present]. Disc [swollen / normal / not seen]. BP [ ]. Fundus / B-scan [ ]. ERG offered [Y/N]. Enrofloxacin / ivermectin [ ].

DDX:
1. Retina (RD / toxin / SARDS) if fundus or flat ERG says so — other list
2. Optic neuritis (disc swollen or retrobulbar-normal) — meningoencephalitis common
3. Chiasm / tract if both eyes and the pathway fits
4. Not cortex (those pupils are normal)
5. Not papilledema alone (usually still sees, still has PLR)

Do not: harvest book pred 1.0. DexSP a hypertensive or azotemic patient as the blindness plan. Call a normal disc “not optic nerve.” Call it SARDS without an ERG. Send home as just a funny pupil.
Do next: BP now. Fundus or B-scan. Offer ERG / referral. MRI / CSF if the nerve is the space.

### `ddx-cortex`

Cortical / post-ictal blindness — {{patient.name}}
Pupils [normal / dilated]. PLR [present / absent]. Just seized [Y/N]. Circle [toward L / toward R / none]. Glucose [ ]. Menace [ ].

DDX:
1. Post-ictal cortical blindness if they just seized (watch; do not invent hours)
2. Forebrain / radiation / occipital if it persists (other list)
3. Not SARDS / optic neuritis if pupils and PLR are normal
4. Unilateral forebrain if contralateral field + circle toward the lesion
5. Ivermectin can still be central (other list)

Do not: call it SARDS. Call it optic neuritis when the pupils are normal. DexSP this as a stroke. Harvest a benzo / PB table. Invent a post-ictal hour clock. Send a just-seized blind dog home as SARDS.
Do next: glucose now. Watch if post-ictal. Persistent → fundus. Dilated and fixed is the other list.

### `ddx-htn`

Systemic hypertension — {{patient.name}}
BP [ ] (calm / bouncing). TOD [eye / kidney / CNS / heart / none]. Fundus [RD / hemorrhage / tortuosity / normal / not seen]. Cause [CKD / hyperT / Cushing / DM / pheo / unknown]. Species [cat / dog].

DDX:
1. Secondary hypertension (default) — dog kidney first; cat kidney or hyperT
2. Hypertensive retinopathy / RD if sudden blind or hyphema (not SARDS)
3. Not pulmonary HTN (heartworm / PTE / left-heart — other list)
4. Not the TBI Cushing reflex (hypertension + bradycardia = late herniation)
5. Essential / primary is extremely rare — do not call it the default

Do not: harvest amlodipine or sildenafil numbers. Lasix systemic hypertension. DexSP the blind hypertensive eye. Treat one bouncing cuff with no TOD as gospel. Screen a healthy pet because humans do. Invent a dog first-line cookbook.
Do next: BP now if the disease causes hypertension or the eye/brain looks like TOD. Single high cuff + TOD is enough to treat. Cat: amlodipine / telmisartan conversation (ACEI / atenolol / Lasix generally do not drop feline systemic pressure). Dog: name the pages, △ Plumb / hospital.

### `ddx-phtn`

Pulmonary hypertension — {{patient.name}}
Syncope / collapse after exercise [Y/N]. Ascites / jugulars [Y/N]. Echo [TR / PR jet / not yet]. Cause [HW / PTE / lung / left-heart / shunt / unknown]. HW Ag [ ]. SpO2 [ ].

DDX:
1. Secondary PH (default) — heartworm, PTE, lung / hypoxemia, left-heart
2. Increased flow (VSD / PDA) or reverse PDA if polycythemia fits
3. Not systemic HTN / not amlodipine
4. Not a seizure if it is exertional syncope
5. Primary PH is rare except in people

Do not: harvest sildenafil or tadalafil numbers. Invent a TR-velocity cutoff. Lasix this as the PA-pressure drug. Dump an adulticide table tonight. Call syncope a seizure. Start amlodipine for this list.
Do next: oxygen if hypoxic. Echo, not a PA catheter. Name the cause. Sildenafil is the Merck dog conversation when they have signs (syncope / RHF) — △ Plumb. Pimobendan if left-heart PH. Treat the cause.

### `ddx-hyperca`

Hypercalcemia — {{patient.name}}
iCa [ ]  tCa [ ]  sample [anaerobic / air / frozen SST]. UTI [confirmed / no / pending]. PTH [ ]  PTHrP [ ]. Imaging [stones / mass / not yet].

DDX:
1. Idiopathic (most common in cats; exclusion)
2. Neoplasia (lymphoma + SCC in cats) — PTHrP negative does not rule out
3. CKD / hyperparathyroid / vitamin D / granuloma
4. Confirmed UTI is a second list, not the calcium explanation

Do not: close calcium because UTI grew. DexSP before PTH/tissue. Harvest a bisphosphonate or fluid table. Treat frozen-SST iCa as gospel. 14-day / FQ-first for sporadic cystitis.
Do next: two problem lists. Repeat iCa anaerobic. Image for CaOx. ISCAID 3–5 d if sporadic lower UTI. △ Plumb.

### `ddx-resp`

Dyspnea — {{patient.name}}
Oxygen / hands off first. Name the space before the syringe.

Pattern: inspiratory (upper) vs expiratory push/wheeze (bronchial / asthma) vs quiet restrictive (pleural) vs B-lines + big LA (CHF) vs pale (anemia) vs cold legs (FATE) vs vaccine/sting (anaphylaxis).

Dog + inspiratory stridor / voice change: use `ddx-larpar`. Not kennel cough. Not a Lasix cocktail.

DDX: CHF, asthma/bronchitis, pleural effusion, pneumothorax, aspiration, PTE, obstruction, anemia, ATE, anaphylaxis. Older-cat new cough: pneumonia still on the list.

Do not: stack Lasix + albuterol + DexSP. Do not wrestle for rads. Do not Lasix a quiet chest. Do not DexSP an azotemic cat. Do not harvest puff / terbutaline / DexSP tables. Do not send open-mouth home as anxiety. △ Plumb.

### `ddx-chf`

Shock type — {{patient.name}}
Hypovolemic vs cardiogenic vs distributive vs obstructive.

If cardiogenic: no shock-bolus-as-default. If hypovolemic: AAHA 2024 — bolus ≠ overnight drip. Reassess perfusion, electrolytes, UOP.
If distributive (anaphylaxis): epinephrine is the crash drug, not diphenhydramine / DexSP. Dog: liver/portal, hives may be absent. Cat: respiratory. Gallbladder halo is not pathognomonic — look at the heart.

### `ddx-anax`

Anaphylaxis — {{patient.name}}
{{patient.species}}. Trigger: [vaccine / sting / drug / food / unknown]. Hives [Y/N]. Collapse [Y/N].
Dog shock organ = liver / portal (GI). Cat = respiratory. Do not wait for skin signs.
Gallbladder halo [Y/N] — not pathognomonic (tamponade / right heart also). Heart FAST [ ].
Abdominal fluid: pair PCV/TS.
Do not: lead with diphenhydramine or DexSP. Do not harvest 2013 epi/fluid tables. No RECOVER high-dose epi. Azotemic cat: still no DexSP. △ crash-cart / Plumb.

### `ddx-hemo`

Hemoabdomen — {{patient.name}}
PCV/TS pair [abdomen vs peripheral]. Fast [ ].

DDX: ruptured mass (spleen/liver), trauma, coagulopathy (anticoagulant rodenticide), GDV-associated tear, ATE not this.
Vitamin K only if the rodenticide family is anticoagulant. Four families exist.

### `ddx-imha`

IMHA — {{patient.name}}
{{patient.species}}. Anemia [spun PCV]. SAT 4:1 [persists / disperses]. Smear monolayer [spherocytes dog only]. DAT [ ]. Bilirubin/Hb [ ]. TS [holds vs falls].
ACVIM 2019: immune destruction + hemolysis. Cats: do not use spherocytes as a criterion.
DDX: primary IMHA vs infectious vs zinc vs allium/Heinz vs blood loss vs microangiopathic.
Do not: pred garlic. Invent a PCV transfusion cutoff. DexSP if azotemic. Harvest 2013 immunosuppressant tables. Skip dog thromboprophylaxis conversation. Universal-donor cat blood. △ Plumb.

### `ddx-tbi`

Head trauma / TBI — {{patient.name}}
LOC [ ]. Pupils [ ]. Cushing (high BP + bradycardia) [Y/N]. Glucose [ ]. Volume status [ ].
Secondary injury. CPP = MAP − ICP. Steroids contraindicated.
Do not: DexSP. Hypotonic fluid. Mannitol while dry. Lasix for ICP. Harvest 2013 osmotic tables. Wait for a skull film.
Do next: oxygen, perfusion, glucose, head up / no neck pressure, serial neuro. Osmotic drug △ hospital / Plumb.

### `ddx-uroabd`

Uroabdomen — {{patient.name}}
Do not therapeutic-tap without paired fluid and serum creatinine and potassium.
DDX: uroabdomen vs ascites vs septic peritonitis vs hemoabdomen.
Soft non-tense + unilateral renomegaly is the kidney/ureter until those pairs say otherwise.

### `ddx-panc`

Pancreatitis — {{patient.name}}
{{patient.species}}. Spec / SNAP fPL [negative / weak-equivocal / positive]  AUS cranial [ ]  eating [ ].
Cluster diagnosis (Forman ACVIM): signs + imaging + fPLI. fPL is supportive, not pathognomonic. SNAP weak/equivocal = abnormal SNAP, not a diagnosis and not a negative. Do not invent the cutoff. Do not copy this SNAP onto a housemate.
Do not withhold food. Hepatic lipidosis risk. Cat: Forman does not require a canine-style low-fat 3–5 day diet.
Opioids are the primary analgesics (Forman). Buprenorphine is adequate for most cats. A one-time dose is analgesia, not a disease-modifier. Do not withhold for theoretical sphincter-of-Oddi spasm. Do not switch to an NSAID because SNAP was weak. Ileus is a watch if linear FB is still on the list.
Gabapentin does not replace the opioid for an acute/overt bout. Forman: PO option / long-term chronic adjunct (tramadol too). △ Plumb. Read the bottle for xylitol. Not for the housemate.
Antibiotics not routine if uncomplicated. No DexSP / NSAID as the pancreatitis plan.
Sucralfate is coating, not pancreatitis therapy. △ Plumb for fluids / antiemetic / opioid.

### `ddx-uti`

Lower urinary — {{patient.name}}
ISCAID 2019: sporadic cystitis 3–5 days, not 14. Subclinical bacteriuria is not a UTI.
Confirmed UTI is infection, not FIC. Still 3–5 d if sporadic lower tract. Fever / lumbar / azotemia = pyelo conversation.
UTI does not close hypercalcemia. Two problem lists. Image for CaOx. Do not DexSP before PTH/tissue.
Young cat without confirmation: FIC until culture says otherwise. Reserve FQ / 3rd-gen. △ Plumb. Hold NSAID if azotemic.

### `ddx-rabbit`

Rabbit not eating — {{patient.name}}
Stasis vs obstruction first. Pain and fluids. Do not start a prokinetic or syringe-feed until obstruction is off the table.

---

## Discharge (owner-facing)

### `dc-master`

Dear {{client.givenName}},

{{patient.name}} was seen at {{location.name}} on {{date}} for [reason]. {{patient.Pronoun}} is going home with you tonight.

What we found: [plain language, one or two sentences].

Medications: give exactly as labeled on the bottle / as written on the discharge sheet. Do not add pain medicine, human medicine, or leftover antibiotics.

Home care:
- [food / water / litter / activity]
- [wound / E-collar / bandage]

Please call {{location.phonenumber}} or return immediately if {{patient.name}} has trouble breathing, collapse, unrelenting pain, repeated vomiting, no urine, bloated belly, seizures, or you cannot give the prescribed care.

Follow-up: [rDVM / here] on [date].

{{provider.name}}
{{location.name}} | {{location.phonenumber}}

### `dc-return`

Return to {{location.name}} ({{location.phonenumber}}) or the nearest emergency clinic now if {{patient.name}} has: trouble breathing, pale or blue gums, collapse, seizure, unrelenting pain, a hard or bloated belly, repeated vomiting, no urine for more than [hours], or you cannot keep medications down.

### `dc-gi`

{{patient.name}} is going home after evaluation for vomiting / diarrhea.

Offer small frequent meals of food {{patient.name}} will actually eat. Water always available. No table scraps, bones, grapes, raisins, xylitol gum/peanut butter, onions, or garlic.

Cat: easy-to-digest = moist, highly digestible, small meals. Low fat is fine as that lever (not greasy leftovers). Do not use a high-fiber hairball/weight diet. Forman does not make fat the pancreatitis therapy. Do not withhold food for 12 hours if vomiting — call us. This sheet is for THIS patient's GI localization only. A housemate who only shared the snack gets `dc-toxin`, not this bland-diet / sucralfate block. Do not write “below the toxic threshold” unless APCC/Plumb named a number for THIS product.

Call {{location.phonenumber}} if vomiting continues, there is black or bloody stool, {{patient.pronoun}} will not drink, becomes lethargic, or the belly becomes tight.

Medications: as labeled only.

### `dc-ahds`

{{patient.name}} was treated for sudden bloody diarrhea (acute hemorrhagic diarrhea). This is not the same disease as parvovirus, Addison, or a bleeding ulcer — we tested or discussed those.

Fluids were the main treatment. Antibiotics are not automatic for every bloody-diarrhea dog. Give only the medicines we sent, as labeled. Offer small meals when vomiting has stopped. Water always available.

Return now for collapse, repeated vomiting, no urine, a swollen belly, or if {{patient.pronoun}} will not drink. Recheck as scheduled. {{location.phonenumber}}

### `dc-parvo`

{{patient.name}} has (or we could not rule out) parvovirus. This is contagious to other dogs. Isolate from unvaccinated dogs. Do not take {{patient.objectPronoun}} to a dog park, daycare, or boarding until we say the isolation clock is over.

This is hospital-level disease for most puppies.

[If declined:] Going home tonight against advice carries a high risk of dehydration and sepsis. You may return at any time.

Give only the medicines we sent. Offer food as instructed. Return now for collapse, unstoppable vomiting, or no urine. {{location.phonenumber}}

### `dc-eclampsia`

{{patient.name}} was treated for low blood calcium while nursing (eclampsia). This can look like a seizure. It is not “just epilepsy.”

Do not let the puppies or kittens nurse tonight until we say. Use the milk replacer as instructed. Give only the calcium or other medicines we sent, as labeled. Do not add human antacids or leftover steroids. Do not start calcium pills in a future pregnancy to “prevent this” unless a veterinarian has planned that after birth.

Return now for stiffness, tremors, panting, or another seizure. {{location.phonenumber}}

### `dc-larpar`

{{patient.name}} was treated for a noisy / obstructed upper airway (laryngeal paralysis). The voice box is not opening fully. This is not kennel cough and it is not a home inhaler disease.

Keep {{patient.objectPronoun}} cool, quiet, and on a harness rather than a neck collar. No hot cars, no midday walks, no extra excitement tonight.

Give only the medicines we sent, as labeled. Do not add leftover Lasix, human inhalers, or leftover steroids.

[If surgery / tie-back discussed:] Surgery can open one side of the airway. It does not cure the nerve disease. Coughing after eating and pneumonia are the risks we discussed.

[If declined:] Without opening the airway, another breathing crisis can happen, especially in heat or stress. You may return at any time.

Return now for louder breathing, blue or purple tongue, collapse, or if {{patient.pronoun}} will not settle. Watch later for cough, fever, or not eating (aspiration). {{location.phonenumber}}

### `dc-hypogly`

{{patient.name}} was treated for low blood sugar. Tiny puppies (and kittens) can drop glucose after a missed meal, stress, or illness. This is not “just tired from the trip.”

{{patient.Pronoun}} must eat frequent small meals of puppy (or kitten) food as instructed. Do not skip meals. Keep {{patient.objectPronoun}} warm. Do not pour syrup into the mouth if {{patient.pronoun}} cannot swallow — call us instead.

Return now for wobbliness, tremors, another seizure, collapse, or if {{patient.pronoun}} will not eat. Recheck as scheduled. {{location.phonenumber}}

### `dc-txrxn`

{{patient.name}} had a reaction during a blood transfusion. We stopped the bag. This can look like fever, vomiting, itching, trouble breathing, or red-brown urine.

Give only the medicines we sent, as labeled. Do not add leftover allergy pills or leftover steroids.

Return now for pale or yellow gums, red-brown urine, trouble breathing, collapse, or fever. Recheck as scheduled. {{location.phonenumber}}

### `dc-vest`

{{patient.name}} was treated for a balance / inner-ear problem (vestibular disease). This can look like a stroke. Many older dogs improve over days to weeks, but we still look for an ear infection or a medicine side effect.

Keep {{patient.objectPronoun}} padded and assisted so {{patient.pronoun}} does not fall. Give only the anti-nausea medicine we sent, as labeled. Do not add leftover steroids.

Return now for becoming dull, a worsening head tilt with a fever, not eating, or seizures. {{location.phonenumber}}

### `dc-snake`

{{patient.name}} was treated for a snake bite. Keep {{patient.objectPronoun}} quiet. Do not put ice on the wound, do not cut it, do not suck venom, and do not put a tourniquet on.

We discussed antivenom. Give only the medicines we sent, as labeled. Do not add leftover pain pills or leftover steroids.

Return now for spreading swelling, new bleeding, trouble breathing, collapse, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-he`

{{patient.name}} was treated for a liver-related brain problem (hepatic encephalopathy) or acute liver injury. This can look like a seizure or just being dull.

Give only the medicines we sent (often a stool-softening sugar called lactulose), as labeled. Aim for soft stools, not watery diarrhea. Do not add leftover steroids, leftover pain pills, or human sleep medicines.

{{patient.Pronoun}} must eat as instructed. Do not skip meals unless we said to wait.

Return now for circling, head pressing, another seizure, collapse, yellow gums, or black stool. {{location.phonenumber}}

### `dc-propto`

{{patient.name}} was treated for an eye that came out of the socket (proptosis). We lubricated it and either put it back and stitched the lids, or removed the eye.

Vision in that eye is not promised. Cats rarely keep vision. Keep the E-collar on. Give only the eye and pain medicines we sent, as labeled. Do not add leftover steroids or leftover pain pills. Do not put human eye drops or disinfectant in the eye.

Return now for the eye becoming more swollen or dry, yellow/green discharge, the stitches opening, or if {{patient.pronoun}} is in pain or not eating. {{location.phonenumber}}

### `dc-neonate`

{{patient.name}} is a newborn / very young puppy or kitten. Keep {{patient.objectPronoun}} warm. Feed only after {{patient.pronoun}} is warm and can swallow. Do not swing {{patient.objectPronoun}}. Do not pour formula into the mouth if {{patient.pronoun}} cannot swallow.

Give only the medicines we sent, as labeled. Weigh daily. Return now for nonstop crying, not nursing, cold body, trouble breathing, a red belly button, or black/cold toes. {{location.phonenumber}}

### `dc-glaucoma`

{{patient.name}} was treated for high pressure in the eye (glaucoma). This is painful and can take vision quickly. It is not simple conjunctivitis.

Give only the eye and pain medicines we sent, as labeled. Do not add leftover steroid drops or leftover pain pills. Keep the E-collar on if one was sent.

Return now if the eye becomes more cloudy or painful, if {{patient.pronoun}} stops seeing, or if {{patient.pronoun}} will not eat. The other eye still needs a check. {{location.phonenumber}}

### `dc-uveitis`

{{patient.name}} has inflammation inside the eye (uveitis). This is not simple conjunctivitis. We stained the cornea and checked the pressure.

Give only the eye and pain medicines we sent, as labeled. Do not add leftover steroid drops unless the stain was negative and we said to. Keep {{patient.objectPronoun}} out of bright light.

Return now if the eye becomes more painful or cloudy, if {{patient.pronoun}} stops seeing, or if {{patient.pronoun}} will not eat. Both eyes can be involved if this is a whole-body problem. {{location.phonenumber}}

### `dc-lenslux`

{{patient.name}} has a lens that has moved out of place. If it is in the front of the eye, this is an emergency. Referral for surgery was recommended.

Give only the medicines we sent, as labeled. Do not add leftover glaucoma drops (especially latanoprost) unless we wrote that on the label. Keep the E-collar on if one was sent.

Return now if the eye becomes more cloudy or painful, if {{patient.pronoun}} stops seeing, or if {{patient.pronoun}} will not eat. The other eye still needs a check. {{location.phonenumber}}

### `dc-hyphema`

{{patient.name}} has blood in the front of the eye (hyphema). That is a sign, not a diagnosis. We still need the work-up we discussed (blood pressure, clotting, the rest of the eye).

Give only the medicines we sent, as labeled. Do not give aspirin, leftover pain pills, or leftover steroid drops. Keep the E-collar on. Keep {{patient.objectPronoun}} quiet.

Return now if the eye fills more with blood, becomes more painful, or if {{patient.pronoun}} will not eat, has nosebleeds, or bruises. {{location.phonenumber}}

### `dc-corneal`

{{patient.name}} has a cut or puncture of the cornea. If the eye is leaking, or tissue is sticking out, this is an emergency. Referral was recommended if we discussed it.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops. Keep the E-collar on. Do not let {{patient.objectPronoun}} rub the eye.

Return now if the eye suddenly looks smaller or wetter, if yellow goo appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-sards`

{{patient.name}} lost vision suddenly. We checked the eyes and the blood pressure. This is not something to wait on at home without the follow-up we discussed.

Give only the medicines we sent, as labeled. Do not add leftover steroids. Keep {{patient.objectPronoun}} in a familiar room so {{patient.pronoun}} does not fall.

Referral for a retina test (ERG) or a neurologist was recommended if we discussed it. Return now for bumping harder, a red painful eye, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-eyelid`

{{patient.name}} had a cut eyelid repaired. The lid edge has to line up or the eye cannot blink well.

Give only the medicines we sent, as labeled. Keep the E-collar on. Do not let {{patient.objectPronoun}} rub the stitches. Do not put disinfectant in the eye.

Return now if the lid edge opens, the eye becomes more red or cloudy, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-chemeye`

{{patient.name}} got a chemical in the eye. We flushed it here. Alkali (drain cleaner, lye, some bleach/dishwasher products) can keep damaging the eye after it looks quieter.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops. Do not put vinegar, baking soda, or “neutralizer” in the eye. Keep the E-collar on.

Return now if the eye is more painful, cloudier, or smaller, if {{patient.pronoun}} cannot open it, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-melt`

{{patient.name}} has a deep or melting corneal ulcer. The clear surface of the eye can get thinner very fast. This is not a wait-at-home scratch.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops. Keep the E-collar on. Do not let {{patient.objectPronoun}} rub the eye.

Referral to an eye surgeon was recommended if we discussed it. Return now if the eye looks smaller or wetter, if a dark spot appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-anes`

{{patient.name}} had anesthesia or heavy sedation. The riskiest time is often after {{patient.pronoun}} wakes up, not only while {{patient.pronoun}} is asleep.

Give only the pain and anti-anxiety medicines we sent, as labeled. Keep {{patient.objectPronoun}} warm and quiet. Do not add leftover pain pills.

Return now for trouble breathing, pale or blue gums, collapse, repeated vomiting, or if {{patient.pronoun}} will not wake or eat. {{location.phonenumber}}

### `dc-indolent`

{{patient.name}} has a superficial ulcer that does not stick down. This is not the same as a melting, deep ulcer. It often needs the loose skin scraped and, in dogs, a special polish or grid. That is not done in cats.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops. Keep the E-collar on.

Return now if the eye gets much more painful or cloudy, if a dark spot appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-seq`

{{patient.name}} has a dark plaque on the clear part of the eye. In cats this is dead cornea. It is not something to pick at home, and it often needs surgery to remove.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops. Keep the E-collar on.

Referral for surgery was recommended if we discussed it. Return now if the eye is more painful, if the dark spot grows, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-fhv`

{{patient.name}} has a feline herpesvirus eye ulcer. Branching (dendritic) ulcers are typical. This is not a reason to add leftover steroid drops.

Give only the eye medicines we sent, as labeled. Keep the E-collar on. Reduce stress at home as discussed.

Return now if the eye becomes much more painful or cloudy, if a dark spot appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-fek`

{{patient.name}} has raised pink or white plaques on the clear part of the eye (eosinophilic keratitis). This is not ordinary conjunctivitis, and it is not the same as a lip sore.

Give only the eye medicines we sent, as labeled. Do not add leftover steroid drops unless we said the stain was negative. Keep the E-collar on.

Return now if the eye becomes much more painful or cloudy, if a dark spot appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-kcs`

{{patient.name}} has dry eye (not enough watery tears). The sticky discharge is from dryness, not “just conjunctivitis.”

Give only the tear and eye medicines we sent, as labeled. Do not add leftover steroid drops unless we said the stain was negative. Keep the E-collar on if one was sent.

Return now if the eye becomes much more painful or cloudy, if a hole or jelly-like melt appears, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-cherry`

{{patient.name}} has a prolapsed tear gland of the third eyelid (cherry eye). This gland makes tears. It should be put back, not cut out.

Give only the eye medicines we sent, as labeled. Keep the gland moist as shown. Do not try to cut or pinch it at home.

Surgery to replace the gland was recommended if we discussed it. Return now if the eye becomes painful or cloudy, if the pink mass looks dry, or if {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-dacryo`

{{patient.name}} has a blocked or infected tear duct (dacryocystitis). The watery or sticky eye is overflow or pus from the duct, not ordinary conjunctivitis.

Give only the eye medicines we sent, as labeled. Keep the face clean as shown. A tooth problem can look the same — return if we asked for dental follow-up.

Return now if the inner corner swells, a hole drains, the eye becomes painful, or {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-orbit`

{{patient.name}} has infection or swelling behind the eye (orbital cellulitis). The eye is pushed forward. This is not ordinary conjunctivitis, and it is not the same as an eye that popped out of the lids.

Give only the medicines we sent, as labeled. Keep the eye wet with the lubricant we sent. Soft food may be easier if opening the mouth hurts.

Return now if {{patient.pronoun}} cannot blink, the eye looks dry or cloudy, the face swells, or {{patient.pronoun}} will not eat. {{location.phonenumber}}

### `dc-mmm`

{{patient.name}} has inflammation of the chewing muscles (masticatory myositis). The jaw will not open. This is not “being picky,” and the jaw must not be forced open.

We drew blood for the chewing-muscle antibody test (2M) before steroids if we could. That result takes days, not tonight. Give only the medicines we sent, as labeled. Offer soft food or the feeding plan we showed. Do not try to pry the mouth open at home.

Return now if {{patient.pronoun}} cannot drink, the eyes bulge, the body goes stiff, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-tetanus`

{{patient.name}} has tetanus (lockjaw from a bacterial toxin). The face or body can go stiff. This is not “just being picky,” and the jaw must not be forced open.

Keep the room quiet and dim as we showed. Give only the medicines we sent, as labeled. Soft food if the mouth will open. Do not try to pry the mouth open at home.

Return now if breathing looks hard, the body goes rigid, {{patient.pronoun}} cannot swallow, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-tick`

{{patient.name}} had tick paralysis (a toxin from a tick that makes the body go limp). This is not “just being tired,” and it is not lockjaw.

We searched the coat and removed any ticks we found. Keep searching at home as shown, including ears, toes, and under the collar. Give only the medicines we sent, as labeled.

Return now if the legs get weaker, breathing looks hard, {{patient.pronoun}} cannot swallow, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-botul`

{{patient.name}} was treated for suspected botulism (a food toxin that makes the body go limp). This is not “just being tired.”

Give only the medicines we sent, as labeled. Do not feed leftover spoiled food or carrion. Soft food if swallowing is weak.

Return now if the legs get weaker, breathing looks hard, {{patient.pronoun}} cannot swallow, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-apn`

{{patient.name}} has an immune attack on the nerve roots (polyradiculoneuritis). The legs go limp. This is not “just being tired,” and steroids are not the treatment.

Keep searching the coat as shown. Soft bedding and the physical-therapy plan we showed. Give only the medicines we sent, as labeled.

Return now if breathing looks hard, {{patient.pronoun}} cannot swallow, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-mg`

{{patient.name}} has myasthenia (the nerves cannot talk to the muscles). Food can sit in a weak esophagus and go into the lungs.

Feed upright as shown. Give only the medicines we sent, as labeled. Do not add leftover steroids unless we said to.

Return now if breathing looks hard, coughing after meals, or {{patient.pronoun}} cannot swallow. {{location.phonenumber}}

### `dc-trigem`

{{patient.name}} has inflammation of the nerve that closes the jaw (trigeminal neuritis). The mouth hangs open. This is not “being picky,” and the jaw must not be forced shut.

Offer the soft food or feeding plan we showed. Fluids if we started them. This often improves over a few weeks. Do not try to pry the mouth closed at home.

Return now if {{patient.pronoun}} cannot drink, the eye dries, the face or legs go weak, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-2m`

{{patient.name}} had blood drawn for the chewing-muscle antibody test (2M ELISA) before steroids if we could. A positive test confirms masticatory myositis. A negative test after steroids, or in a very wasted head, does not prove it is not that disease.

The jaw must not be forced open. Offer the soft food or feeding plan we showed. This blood test is not an overnight result.

Return now if {{patient.pronoun}} cannot drink, the eyes bulge, the body goes stiff, or {{patient.pronoun}} collapses. {{location.phonenumber}}

### `dc-face`

{{patient.name}} cannot blink well on one side because the facial nerve is not moving the eyelids (facial paralysis). This is not “just a droopy face,” and it is not the same as Horner’s syndrome (those pets can still blink).

Put the lubricating drops or ointment in as we showed, as often as we wrote. Keep the Elizabethan collar on if we sent one. The ear still needs to stay clean and dry. This can last weeks or stay; the other side can later drop.

Return now if the eye looks cloudy, blue, or painful, if {{patient.pronoun}} stops eating, if a head tilt or rolling starts, or if the other side of the face drops. {{location.phonenumber}}

### `dc-polyp`

{{patient.name}} has a growth from the middle ear or the back of the nose (an inflammatory polyp). These are not cancer. They can block breathing or the ear and can grow back if the stalk is still there.

Keep the eye lubricated if we showed you how. Keep the ear clean and dry as we wrote. Do not use leftover ear drops unless we said the eardrum was seen. Surgery or another look may still be needed.

Return now if breathing is loud or hard, if {{patient.pronoun}} stops eating, if a head tilt or an eye that cannot blink starts, or if the face looks uneven. {{location.phonenumber}}

### `dc-horner`

{{patient.name}} has Horner’s syndrome: a small pupil, a droopy lid, and a raised third eyelid on one side because the sympathetic nerve to that eye is not working. {{patient.pronoun}} can still blink. This is not the same as facial paralysis.

Keep the eye clean. Use only the drops we sent. The ear still needs to stay clean and dry. We may still need another look at the ear or the front leg.

Return now if {{patient.pronoun}} cannot blink, the eye looks cloudy or painful, a head tilt or rolling starts, or the front leg on that side goes limp. {{location.phonenumber}}

### `dc-aniso`

{{patient.name}} has pupils that are not the same size. We decided which side is the problem. A large pupil that still sees is often an aging iris or a drop effect, not Horner’s syndrome (that is the small pupil).

Use only the eye medicines we sent. Do not put leftover atropine or other drops in unless we said to. Keep the eye from bright glare if it bothers {{patient.pronoun}}.

Return now if the eye turns red, cloudy, or painful, if vision is suddenly worse, if {{patient.pronoun}} starts vomiting or cannot urinate, or if the other side of the face or a leg goes weak. {{location.phonenumber}}

### `dc-optic`

{{patient.name}} suddenly cannot see well, and the pupils are large and do not shrink to light. That means the problem is in the retina or the optic nerve, not “just the brain cortex.” We still need blood pressure, a look at the back of the eye, and often a referral for an ERG or imaging.

Keep {{patient.pronoun}} in a safe, familiar room so {{patient.pronoun}} does not fall. Use only the medicines we sent. This is not a home steroid plan.

Return now if {{patient.pronoun}} seizes, cannot walk, the eye turns red or painful, or breathing gets hard. {{location.phonenumber}}

### `dc-cortex`

{{patient.name}} cannot see well right now, but the pupils still shrink to light. That usually means the problem is in the brain, not the retina or the optic nerve. If a seizure just happened, this can be the recovery phase and often improves.

Keep {{patient.pronoun}} in a quiet, familiar room so {{patient.pronoun}} does not fall. This is not a home steroid plan and not “SARDS tonight.”

Return now if another seizure starts, if the pupils become large and stay that way, if {{patient.pronoun}} cannot walk, or if breathing gets hard. {{location.phonenumber}}

### `dc-htn`

{{patient.name}} has high blood pressure that can damage the eyes, kidneys, brain, or heart. This is almost always from another disease (kidney disease or an overactive thyroid in cats; kidney disease first in dogs), not “essential hypertension like people.”

Give only the blood-pressure medicine we sent, as labeled. This is not a water-pill (Lasix) plan and not a home steroid plan. Recheck blood pressure as discussed. Keep {{patient.pronoun}} in a safe room if vision is poor.

Return now if vision suddenly worsens, if {{patient.pronoun}} seizes, cannot walk, cannot urinate, or if breathing gets hard. {{location.phonenumber}}

### `dc-phtn`

{{patient.name}} has high pressure in the lungs’ arteries (pulmonary hypertension). That is not the same as high blood pressure in the body. It often comes from heartworm, a clot, lung disease, or left-sided heart disease. Fainting after excitement or a pot-bellied right-heart look can be this disease, not “just a seizure.”

Give only the medicines we sent, as labeled. This is not a water-pill plan for the lung arteries and not a home steroid plan. Keep activity calm. Recheck and imaging as discussed.

Return now if {{patient.pronoun}} faints again, collapses, the belly swells, or breathing gets hard. {{location.phonenumber}}

### `dc-hyperca`

{{patient.name}} has a high blood calcium. That is a separate problem from a bladder infection if both are present. The infection does not explain the calcium.

Give only the medicines we sent, as labeled. Finish the antibiotic if one was started. We still need the calcium work-up (recheck blood, imaging for stones or a mass) as discussed.

Return now for straining without urine, vomiting, not eating, more drinking, or collapse. {{location.phonenumber}}

### `dc-uti`

{{patient.name}} has a confirmed bladder infection. This is not “just stress peeing” until a veterinarian says the infection is gone.

Give only the antibiotic and pain medicine we sent, as labeled. This is usually a short course, not leftover antibiotics from the cabinet. No extra pain pills.

If calcium was also high, that is a second problem — imaging and a recheck as discussed. Return now for straining without urine, fever, vomiting, or not eating. {{location.phonenumber}}

### `dc-mastitis`

{{patient.name}} was treated for an infected mammary gland and/or a postpartum uterine infection. This can make the mother and the babies sick.

Give only the antibiotic and pain medicine we sent, as labeled. Warm compresses on the sore gland as shown. Do not add leftover steroids or leftover pain pills.

The babies may need milk replacer. Weigh them daily. Return now if the gland turns dark or opens, the mother will not eat, she has a foul discharge, she collapses, or a baby stops nursing. {{location.phonenumber}}

### `dc-dystocia`

{{patient.name}} was treated for a difficult birth (dystocia). Some puppies or kittens cannot be born with medicine alone.

[If C-section:] Incision care as discussed. The mother and the babies need warmth, food, and a quiet room. Return for straining without producing a baby, green or foul discharge, collapse, or if the mother will not nurse and the babies are fading.

[If declined:] Surgery was recommended. Going home without delivering the remaining babies is life-threatening for the mother and the unborn. You may return at any time. Do not give oxytocin at home.

{{location.phonenumber}}

### `dc-uo`

{{patient.name}} was treated for a urinary blockage / urinary emergency.

{{patient.Pronoun}} must pass urine. If {{patient.pronoun}} strains without producing urine, cries in the box, or the belly becomes hard, this is an emergency — return immediately. {{location.phonenumber}}

No pain medicines other than what we sent. No meloxicam or other NSAID unless a veterinarian has checked kidney values and told you to give it.

[If declined unblock:] We recommended emergency unblocking and hospitalization. You have chosen to go home against that recommendation. {{patient.name}} is at risk of bladder rupture, high potassium, kidney injury, and death. You may return at any time.

### `dc-aki`

{{patient.name}} has a kidney / ureter emergency. Creatinine and urine output need follow-up.

What this means: one or both kidneys are not clearing waste normally. If imaging or exam suggested a blocked or fluid-filled kidney, the options we discussed were referral for decompression, continued hospital care, or humane euthanasia. Watching a tight or painful kidney problem at home is not a treatment.

No NSAID. No steroid “just in case.” Give only the medicines we sent, as labeled.

Return now for no urine, collapse, repeated vomiting, or worsening pain. {{location.phonenumber}}
Recheck labs: [when / where].

### `dc-addison`

{{patient.name}} was treated for a suspected or confirmed Addisonian crisis (adrenal hormone deficiency). This can look like a stomach upset or kidney failure. It is not those things.

{{patient.Pronoun}} needs the hormone replacement we prescribed, as labeled, and a recheck of electrolytes as scheduled. Stress (boarding, illness) may require a steroid adjustment — call before you change anything.

Return now for collapse, trembling, black stool, or refusal to eat. {{location.phonenumber}}

### `dc-dka`

{{patient.name}} has diabetic ketoacidosis or a related diabetic emergency. This is hospital-level disease.

[If going home against advice:] We recommended continued IV fluids and insulin in hospital until ketones and electrolytes are safer. Going home tonight carries a high risk of worsening acidosis, low potassium, and death. You may return at any time.

If discharged after stabilization: give insulin and food exactly as written. Do not change the insulin dose yourself. Check [glucose / ketones] as instructed. Return for vomiting, not eating, collapse, or heavy breathing. {{location.phonenumber}}

### `dc-toxin`

{{patient.name}} was evaluated for possible toxin exposure: [product].

At home: prevent re-exposure. Bring the package if you find it. Give only medicines we sent.
This is the toxin clock for THIS patient. A housemate with abdominal pain gets a separate GI discharge — do not paste bland-diet, sucralfate, or 12-hour NPO lines here, and do not paste leftover dentistry or heart text.
Do not write “below the toxic threshold” unless APCC/Plumb named a number for THIS product and THIS weight.
Do not withhold food for 12 hours. If vomiting continues, call.
If allium (onion/garlic): watch for pale gums, weakness, red-brown urine, or yellow gums over several days. Recheck PCV/smear as scheduled — tonight’s normal PCV does not close the clock.

Return now for seizures, tremors, trouble breathing, collapse, repeated vomiting, or no urine. {{location.phonenumber}}
ASPCA Animal Poison Control (you may call): 888-426-4435 (fee may apply).

### `dc-lily`

{{patient.name}} was exposed to a true lily (or pollen / vase water). In cats this is a kidney emergency, even if {{patient.pronoun}} looks brighter tonight.

Watch urine output. Recheck kidney values as scheduled — do not skip because {{patient.pronoun}} is eating. Return immediately if {{patient.pronoun}} stops urinating, vomits repeatedly, or becomes lethargic. {{location.phonenumber}}

### `dc-resp`

{{patient.name}} was treated for trouble breathing. This can be the airway, the lung, fluid or air around the lung, or the heart — they are not the same disease and they do not get the same home medicines.

Give only the medicines we sent, as labeled. Do not add human inhalers, leftover Lasix, or leftover steroids.

Keep {{patient.objectPronoun}} quiet and away from smoke, perfume, powder litter dust, and aerosols.

Return now for open-mouth breathing, blue or pale gums, crouching and not moving, collapse, or if you cannot hear {{patient.pronoun}} breathe comfortably. {{location.phonenumber}}

### `dc-gdv`

{{patient.name}} has (or we could not rule out) gastric dilatation-volvulus — a twisted stomach. This is a surgical emergency.

[If surgery done:] Incision care as discussed. No running / jumping until the recheck. The gastropexy lowers the chance the stomach twists again; it does not make bloating impossible. Return for retching, bloated belly, pale gums, collapse, or fainting. Arrhythmias can show up the next day.

[If declined:] Without surgery this condition is usually fatal. You have declined surgery after that discussion. You may return at any time. {{location.phonenumber}}

### `dc-sepsis`

{{patient.name}} was treated for a suspected serious infection with whole-body effects (sepsis). This is hospital-level disease.

[If remaining in hospital / referred:] We are looking for the source of infection and starting antimicrobials. Surgery may be needed to remove that source.

[If declined:] Antibiotics at home are not a substitute for finding and treating the source. {{patient.Pronoun}} can worsen suddenly (collapse, organ failure). You may return at any time.

Return now for collapse, trouble breathing, pale gums, no urine, repeated vomiting, or a swollen belly. {{location.phonenumber}}

### `dc-pyo`

{{patient.name}} was evaluated for a possible infected uterus (pyometra). The recommended treatment is surgery after stabilization.

[If declined:] Antibiotics alone are not a reliable cure for pyometra. {{patient.Pronoun}} can worsen suddenly (rupture, sepsis). Return for collapse, vomiting, or a swollen belly. {{location.phonenumber}}

### `dc-fate`

{{patient.name}} has a blood clot blocking blood flow to the legs (arterial thromboembolism). This is very painful. We treated pain and discussed the heart.

Home: pain medicine as labeled only. Watch for breathing trouble (heart failure) and for the legs becoming cold or more painful again. We do not promise that clot-dissolving drugs will restore the legs.

Return now for open-mouth breathing, collapse, or unbearable pain. {{location.phonenumber}}

### `dc-anax`

{{patient.name}} was treated for an allergic / anaphylactic reaction (vaccine, insect sting, drug, or unknown trigger).

Give only the medicines we sent, as labeled. Do not add human allergy pills or leftover steroids.

Return to {{location.name}} ({{location.phonenumber}}) or the nearest emergency clinic **now** if {{patient.name}} has trouble breathing, pale or blue gums, collapse, repeated vomiting or diarrhea, a swollen face that is worsening, or you cannot wake {{patient.objectPronoun}}. A second wave of signs can show up after {{patient.pronoun}} looks better.

Prevent re-exposure: [vaccine brand / insect / drug]. Recheck: [when / where].

### `dc-imha`

{{patient.name}} was treated for immune-mediated / hemolytic anemia — the body was destroying red blood cells.

This is hospital-level disease. Give only the medicines we sent, as labeled. Do not add human steroids or leftover antibiotics.

Return now for pale or yellow gums, collapse, trouble breathing, red-brown urine, or if {{patient.pronoun}} will not eat. Recheck blood counts as scheduled — do not skip because {{patient.pronoun}} looks brighter. {{location.phonenumber}}

### `dc-tbi`

{{patient.name}} was treated for head trauma. Keep {{patient.objectPronoun}} quiet, indoors, with the collar loose (no tight pressure on the neck).

Return now for worsening dullness, a seizure, unequal pupils, vomiting that you cannot stop, trouble breathing, or collapse. Do not give human steroids or leftover pain medicine. Recheck as scheduled. {{location.phonenumber}}

### `dc-heat`

{{patient.name}} was treated for heatstroke. Keep {{patient.objectPronoun}} cool, indoors, with water available. No hot cars, no midday walks.

Vomiting, bloody stool, stumbling, or yellow gums can show up later — return if any of these appear. {{location.phonenumber}}

### `dc-sz`

{{patient.name}} had a seizure / cluster.

Keep {{patient.objectPronoun}} safe: lights low, no stairs, no swimming. Do not put your hands in {{patient.possPronoun}} mouth. Time the event. If a seizure lasts more than 3 minutes, or {{patient.pronoun}} has more than [number] in 24 hours, return immediately. {{location.phonenumber}}

Give seizure medicine as labeled only.

### `dc-ama`

Against medical advice — {{patient.name}}

I have explained the recommended diagnostics / hospitalization / surgery and the risks of leaving, including worsening, organ failure, and death. The client has chosen to leave {{location.name}} with {{patient.name}} against that recommendation. They may return at any time. {{location.phonenumber}}

Client: {{client.name}}    Clinician: {{usern.name}}    {{date}}

### `dc-euth`

{{patient.name}} was humanely euthanized at {{location.name}} on {{date}} after discussion of [quality of life / disease]. Aftercare: [private cremation / communal / take home] as elected. No owner identifiers beyond the client already on this record.

We are sorry for your loss. {{location.phonenumber}}

### `dc-rdvm`

Please have {{patient.possPronoun}} regular veterinarian ({{rdvms}}) review this visit. Recheck on [date] or sooner if {{patient.name}} is not improving. Records can be sent from {{location.name}} at {{location.phonenumber}}.

---

## Notes for the attending

- I will not log into Vetspire. If a hospital admin must approve macros, send them this file.
- Do not put owner phones, chart IDs, or case nicknames into a shared macro.
- If a number is required, it goes on the product label / order, not inside these phrases.
- Two cats, one bag: two macros. `dc-gi` is not a household stamp.
- Exotic oral beta-lactam and horse/cow one-liners stay out of the night card; use `resident_brief.py` if they appear.

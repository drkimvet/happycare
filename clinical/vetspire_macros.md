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

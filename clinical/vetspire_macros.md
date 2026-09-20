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
| `ddx-resp` | Assessment | Dyspnea |
| `ddx-chf` | Assessment | CHF vs other shock |
| `ddx-hemo` | Assessment | Hemoabdomen |
| `ddx-uroabd` | Assessment | Uroabdomen |
| `ddx-panc` | Assessment | Pancreatitis |
| `ddx-uti` | Assessment | Sporadic cystitis |
| `ddx-rabbit` | Assessment | Rabbit not eating |
| `dc-master` | Discharge | Generic ER home |
| `dc-return` | Discharge | Come-back triggers only |
| `dc-gi` | Discharge | GI home care |
| `dc-uo` | Discharge | Post-unblock / decline unblock |
| `dc-aki` | Discharge | Kidney / ureter |
| `dc-addison` | Discharge | Addison start |
| `dc-dka` | Discharge | DKA / decline ICU |
| `dc-toxin` | Discharge | Generic toxin |
| `dc-lily` | Discharge | Cat lily |
| `dc-gdv` | Discharge | GDV surgery / decline |
| `dc-pyo` | Discharge | Pyometra |
| `dc-fate` | Discharge | FATE |
| `dc-heat` | Discharge | Heatstroke |
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

Do not: induce emesis. Do not “watch overnight.” Stabilize, decompress, surgery. △ fluids/analgesia in Plumb.

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

DDX: idiopathic epilepsy vs toxin vs hepatic vs electrolyte vs intracranial vs heat vs hypoglycemia.
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

### `ddx-resp`

Dyspnea — {{patient.name}}
Upper vs lower vs pleural vs look-alike (pain, shock, anemia).

DDX: CHF, asthma/bronchitis, pleural effusion, pneumothorax, aspiration, PTE, obstruction, anemia.
Do not drown a cat in “just oxygen and a DexSP” if azotemic or if the localization is pleural.

### `ddx-chf`

Shock type — {{patient.name}}
Hypovolemic vs cardiogenic vs distributive vs obstructive.

If cardiogenic: no shock-bolus-as-default. If hypovolemic: AAHA 2024 — bolus ≠ overnight drip. Reassess perfusion, electrolytes, UOP.

### `ddx-hemo`

Hemoabdomen — {{patient.name}}
PCV/TS pair [abdomen vs peripheral]. Fast [ ].

DDX: ruptured mass (spleen/liver), trauma, coagulopathy (anticoagulant rodenticide), GDV-associated tear, ATE not this.
Vitamin K only if the rodenticide family is anticoagulant. Four families exist.

### `ddx-uroabd`

Uroabdomen — {{patient.name}}
Do not therapeutic-tap without paired fluid and serum creatinine and potassium.
DDX: uroabdomen vs ascites vs septic peritonitis vs hemoabdomen.
Soft non-tense + unilateral renomegaly is the kidney/ureter until those pairs say otherwise.

### `ddx-panc`

Pancreatitis — {{patient.name}}
{{patient.species}}. Spec / SNAP fPL [ ]  AUS cranial [ ]  eating [ ].
Cluster diagnosis (Forman ACVIM): signs + imaging + fPLI. fPL is supportive, not pathognomonic. Do not invent the cutoff.
Do not withhold food. Hepatic lipidosis risk. Cat: Forman does not require a canine-style low-fat 3–5 day diet.
Antibiotics not routine if uncomplicated. No DexSP / NSAID as the pancreatitis plan.
Sucralfate is coating, not pancreatitis therapy. △ Plumb for fluids / antiemetic / opioid.

### `ddx-uti`

Lower urinary — {{patient.name}}
ISCAID 2019: sporadic cystitis 3–5 days, not 14. Subclinical bacteriuria is not a UTI.
Young cat: FIC until culture says otherwise. Reserve FQ / 3rd-gen. △ Plumb. Hold NSAID if azotemic.

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

### `dc-gdv`

{{patient.name}} has (or we could not rule out) gastric dilatation-volvulus — a twisted stomach. This is a surgical emergency.

[If surgery done:] Incision care as discussed. No running / jumping until the recheck. Return for retching, bloated belly, pale gums, or collapse.

[If declined:] Without surgery this condition is usually fatal. You have declined surgery after that discussion. You may return at any time. {{location.phonenumber}}

### `dc-pyo`

{{patient.name}} was evaluated for a possible infected uterus (pyometra). The recommended treatment is surgery after stabilization.

[If declined:] Antibiotics alone are not a reliable cure for pyometra. {{patient.Pronoun}} can worsen suddenly (rupture, sepsis). Return for collapse, vomiting, or a swollen belly. {{location.phonenumber}}

### `dc-fate`

{{patient.name}} has a blood clot blocking blood flow to the legs (arterial thromboembolism). This is very painful. We treated pain and discussed the heart.

Home: pain medicine as labeled only. Watch for breathing trouble (heart failure) and for the legs becoming cold or more painful again. We do not promise that clot-dissolving drugs will restore the legs.

Return now for open-mouth breathing, collapse, or unbearable pain. {{location.phonenumber}}

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

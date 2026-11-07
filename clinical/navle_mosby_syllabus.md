# NAVLE and Mosby review (legal sources only)

Neither this map nor Instinct nor Plumb's replaces a veterinary license. 둘 중 하나가 면허를 대신하지는 않습니다.

This is a **study map**, not a book dump. Do not pirate Mosby. Do not fetch Mosby, Elsevier Q-banks, or NAVLE item banks from third-party mirrors. Do not commit a Mosby PDF. Original 가채점 only.

Gene leftovers 285–298 are closed (attending 2026-11-05: 유전자는 그까지 하면 됐고). Do not invent ALDH5A1, CLPX, or packet 299 as another ataxia gene.

## How this resident studies it

1. Pull the public ICVA blueprint (competencies + species weights). Do not reproduce the Species-and-Diagnoses PDF lists.
2. Gate night-critical SA traps from **named public** Merck / AAHA / ACVIM pages into `er_safety_card.md` and `resident_brief.py`.
3. If the attending later ferries a purchased Mosby / board-review PDF, run `python3 clinical/prep_legal_pdfs.py --in ~/Books --out textbooks` on the computer that holds the file. Summarize against a named public source in `source_verification.md`. Never dump a chapter or a Q-bank.
4. Do not ask the attending to hand-split books on a phone.
5. Midtown nights stay dog and cat. Equine / bovine / porcine weights are NAVLE-real; they are **not** new Midtown packets unless she names them.

Legal PDF helper: `clinical/prep_legal_pdfs.py`. Five-Minute title list (Wiley only): `clinical/five_minute_syllabus.md`.

## Public ICVA weights (2026–2027)

Source: [Prepare for the NAVLE](https://www.icva.net/navle/prepare-for-the-navle/) and the linked Candidate Handbook tables. Weights can move after the 2026 practice analysis; re-check the ICVA page, do not freeze a blogger's recap as law.

| Competency domain | Target |
| --- | --- |
| Clinical practice (data gathering + health maintenance) | 70% |
| Preventive medicine and animal welfare | 15% |
| Communication | 8% |
| Professionalism, practice management, wellness | 7% |

| Species | Target |
| --- | --- |
| Canine | 25.6% |
| Feline | 24.3% |
| Equine | 14.7% |
| Bovine | 13.3% |
| Porcine | 5% |
| Other small mammals | 3.3% |
| Ovine / caprine | 3.3% |
| Pet bird | 2.3% |
| Poultry | 2% |
| Non-species specific | 2% |
| Camelid / cervidae | 1.7% |
| Reptiles | 1.5% |
| Aquatics | 1% |

Dogs and cats are about half the paper. That is why this run starts SA endocrine, not another cerebellar gene.

## SA domain order (this run)

Closed gene chain is not on this list.

| Next | Domain | Public source, not a Mosby dump | Status |
| --- | --- | --- | --- |
| 299 | Canine hypothyroidism (not T4-alone) | Heseltine, Merck *Hypothyroidism in Animals*, May 2024 / May 2025 | Shipped |
| 300 | Canine hyperadrenocorticism diagnosis traps (not the TBI Cushing reflex) | Van Vertloo Merck Jul 2024; AAHA 2023; Behrend ACVIM 2013. Do not harvest a UCCR / LDDST table | Shipped |
| 301 | Feline hyperthyroidism (full diagnostic gate; azotemia/amlodipine already exists) | Heseltine Merck May 2024. Do not harvest a methimazole / I-131 table | Shipped |
| 302 | FeLV / FIV | St Denis Merck Feb 2022; Whitbread serologic kits Aug 2026; AAFP 2020. Do not harvest a SNAP cutoff | Shipped |
| 303 | AAHA vaccination / core vs non-core | AAHA canine 2022/2024; AAHA/AAFP feline 2020. Do not harvest a mL or site-sarcoma table | Shipped |
| 304 | Canine ITP (not Cavalier macrothrombocytopenia) | McQuinn Merck Platelet Disorders Feb 2025 / Mar 2026; ACVIM LeVine 2024. Do not harvest a 30k or vincristine table | Shipped |
| 305 | Diabetes mellitus diagnosis traps (not a stress glucose, not DKA/HHS) | Buishand Merck May 2024 / May 2026; AAHA 2026 dog and cat diabetes guidelines. Do not harvest a U/kg or fructosamine table | Shipped |
| 306 | Canine lymphoma (not a CHOP table) | Fan Merck Lymphoma in Dogs Sept 2023 / Apr 2025; AAHA 2026 oncology guidelines. Do not harvest a CHOP or MST table | Shipped |
| 307 | Canine MCT (not a grade table) | Villalobos Merck cutaneous MCT Aug 2021 / Jun 2026; Whitbread Merck cytology Aug 2026. Do not harvest a Patnaik or 3-cm table | Shipped |
| 308 | Canine AGASACA (not hyperCa-alone) | Gallagher Merck Anal Sac Disease Aug 2025; Villalobos Merck apocrine anal-sac Aug 2021 / Jun 2026; Ham Merck hyperCa Jun 2023. Do not harvest an MST table | Shipped |
| 309 | Canine oral melanoma (not a dental tartar) | Mulherin Merck Oral Tumors Nov 2024; AAHA 2026 oncology. Do not harvest an MST or Oncept table | Shipped |
| 310 | Feline oral SCC (not a loose-tooth extraction) | Mulherin Merck Oral Tumors Nov 2024; AAHA 2026 oncology. Do not harvest an MST or piroxicam table | Shipped |
| 311 | Canine osteosarcoma (not a splint-and-home; not pulmonary-nodules-alone) | Chou Merck bone tumors Nov 2025; AAHA 2026 oncology. Named OSA left HIGH_MET so a bone mass is not labeled nodules. Do not harvest an MST or amputation table | Shipped |
| 312 | Canine hemangiosarcoma (not a wait-and-see hemoabdomen; not pulmonary-nodules-alone) | Center Merck hepatic neoplasia Aug 2023 / Jul 2026; Villalobos connective-tissue tumors Aug 2021; AAHA 2026 oncology. Named HSA left HIGH_MET. Do not harvest an MST or doxorubicin table. Do not use HSA letters (albumin) | Shipped |
| 313 | Canine mammary carcinoma (not a cyst-and-home; not pulmonary-nodules-alone) | Sorenmo Merck dogs Mar/Apr 2024; Lopes Merck cats Sept 2024; AAHA 2026 oncology. Named mammary adenocarcinoma left HIGH_MET. Do not harvest an MST or OHE table | Shipped |
| 314 | Feline IBD vs GI lymphoma (not a steroid-responsive diarrhea) | Collier Merck chronic enteropathies Aug 2025 / Jun 2026; Matsuyama Merck GI neoplasia Jan 2025; Marsilio ACVIM 2023 named only. Do not harvest a pred or chlorambucil table | Shipped |
| 315 | Feline CKD (not a fluids-only night) | Van Vertloo Merck renal dysfunction Mar 2025 / Oct 2026; IRIS named only. Do not harvest an IRIS creatinine or phosphorus-binder table | Shipped |
| 316 | Canine pancreatitis (not a SNAP-alone) | Steiner Merck pancreatitis Sept 2025; Forman ACVIM 2021 still owns cats. Do not harvest a SNAP cutoff or fluid table | Shipped |
| 317 | Canine EPI (not a bland-diet) | Steiner Merck EPI Sept 2025. Named pancreatic insufficiency / TLI only. Do not use EPI letters (epinephrine). Do not harvest a TLI cutoff or enzyme table | Shipped |
| 318 | Canine tracheal collapse (not a Lasix night) | Tonozzi Merck respiratory diseases Feb 2022 / May 2025; Kuehn owner page Sept 2024 named only. Do not harvest a stent or cough-suppressant table | Shipped |
| 319 | Brachycephalic airway (not a wait-and-see stertor) | ACVS Brachycephalic Syndrome; Tonozzi Merck Feb 2022 / May 2025. Named BOAS / elongated soft palate / stenotic nares only. Do not harvest a stenotic-nares grade or sedative table | Shipped |
| 320 | Canine megaesophagus (not a pneumonia-alone) | Defarges Merck esophageal dilatation Oct 2022 / May 2025. Named megaesophagus / megaoesophagus only. Do not harvest a barium or metoclopramide table. Packet 271 still owns congenital. Packet 163 still owns MG | Shipped |
| 321 | Canine vascular ring / PRAA (not a megaesophagus-alone) | Tou Merck vascular malformations May 2025; Roberts Merck esophageal anomalies Nov 2022 / Sept 2024 named only. Named PRAA / persistent right aortic arch / vascular ring / double aortic arch only. Do not harvest a barium or ligation table. Packet 320 still owns named megaesophagus. Packet 271 still owns congenital | Shipped |
| 322 | Canine esophageal FB (not a megaesophagus-alone) | Defarges Merck esophageal foreign bodies Oct 2022 / Sept 2024. Named esophageal / oesophageal foreign body or FB, or bone / fishhook / needle / rawhide in the esophagus. Do not harvest a barium or endoscopic-retrieval table. Packet 320 still owns named megaesophagus. Packet 321 still owns PRAA. Linear string stays GI | Shipped |
| 323 | Canine esophageal stricture (not a megaesophagus-alone) | Defarges Merck esophageal strictures Oct 2022 / May 2025. Named esophageal / oesophageal stricture or stenosis only. Do not harvest a balloon-dilation or barium table. Packet 322 still owns FB. Packet 321 PRAA can mimic. Packet 320 still owns named megaesophagus | Shipped |
| 324 | Canine esophagitis (not a megaesophagus-alone) | Defarges Merck esophagitis Oct 2022 / Sept 2024. Named esophagitis / oesophagitis only. Do not harvest a sucralfate or omeprazole table. Packet 323 still owns stricture. Packet 322 still owns FB. Packet 320 still owns named megaesophagus | Shipped |
| 325 | Canine cricopharyngeal achalasia (not a megaesophagus-alone) | Defarges Merck cricopharyngeal achalasia Oct 2022 / Sept 2024; Williamson Merck myopathies Feb 2026. Named cricopharyngeal only. Do not harvest a myectomy or barium table. Dogs only. Packet 320 still owns named megaesophagus. Packet 163 still owns MG. Packet 321 still owns PRAA | Shipped |
| 326 | Canine hiatal hernia (not a megaesophagus-alone) | Roberts Merck hernias Nov 2022 / Sept 2024. Named hiatal / hiatus / gastroesophageal hernia only. Do not harvest a fundoplication or barium table. Packet 320 still owns named megaesophagus. Packet 319 still owns BOAS. Packet 324 still owns esophagitis | Shipped |
| 327 | Canine PPDH (not a hiatal-alone) | Roberts Merck hernias Nov 2022 / Sept 2024; McMichael Merck diaphragmatic hernia May 2022 / Sept 2024. Named PPDH / peritoneopericardial / pericardiodiaphragmatic hernia only. Do not harvest a mesh table. Do not tap as tamponade. Packet 326 still owns hiatal | Shipped |
| 328 | Canine traumatic DH (not a PPDH-alone) | McMichael Merck diaphragmatic hernia May 2022 / Sept 2024. Named diaphragmatic hernia / traumatic DH / ruptured diaphragm only. Do not harvest a re-expansion table. Packet 327 still owns PPDH. Packet 326 still owns hiatal | Shipped |
| 329 | Canine umbilical hernia (not a DH-alone) | Roberts Merck hernias Nov 2022 / Sept 2024. Named umbilical hernia only. Do not harvest a mesh table. Packet 328 still owns traumatic DH. Packet 327 still owns PPDH | Shipped |
| 330 | Canine inguinal hernia (not an umbilical-alone) | Roberts Merck hernias Nov 2022 / Sept 2024. Named inguinal / scrotal hernia only. Do not harvest a mesh or laparoscopic table. Packet 329 still owns umbilical | Shipped |
| 331 | Canine linear FB (not an esophageal-FB-alone) | Winkler Merck GI obstruction Aug 2025. Named linear foreign body / linear FB / string under the tongue only. Do not harvest an enterotomy or 36–48 hour table. Do not yank. Packet 322 still owns esophageal FB | Shipped |
| 332 | Canine intussusception (not a linear-FB-alone) | Winkler Merck GI obstruction Aug 2025. Named intussusception / telescoping bowel / ileocecocolic intussusception only. Do not harvest a barium or 36–48 hour table. Packet 331 still owns linear FB | This packet |

Already gated (do not reopen as if new): Addison, DKA / HHS, hypoglycemia, IMHA, leptospirosis, heartworm / caval, facial CN VII, AAHA core vaccines, canine ITP, diabetes mellitus, canine lymphoma, canine MCT, canine AGASACA, canine oral melanoma, feline oral SCC, pathologic-fracture OSA (199), canine osteosarcoma HIGH_MET split (311), bare hemoabdomen (120), canine hemangiosarcoma (312), mastitis / septic dam, canine mammary carcinoma (313), PLE (178), feline IBD vs GI lymphoma (314), feline CKD (315), canine pancreatitis (316), canine EPI (317), canine tracheal collapse (318), canine BOAS (319), canine megaesophagus (320), canine vascular ring (321), canine esophageal FB (322), canine esophageal stricture (323), canine esophagitis (324), canine cricopharyngeal achalasia (325), canine hiatal hernia (326), canine PPDH (327), canine traumatic DH (328), canine umbilical hernia (329), canine inguinal hernia (330), canine linear FB (331), and the 285–298 gene leftovers.

## What Mosby is for, legally

Mosby's review is a **purchased** Q-style drill, not a night law and not a repo file. When a legal split exists, use it to find which public-source trap to gate next. Do not copy stems, answer keys, or chapter text.

If no legal PDF is on disk, keep studying from ICVA + Merck / AAHA / ACVIM. That is enough to start.

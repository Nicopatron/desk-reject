# Surgical nomenclature — colorectal

The terminology needed to *read* a colorectal surgical abstract: what the operation is called, how a complication is graded, and which outcome a number belongs to. Both registers are canonical — the same author submits to a Buenos Aires congress in Spanish and to a European one in English — so every procedure carries its Spanish name, its English name, and the abbreviation that will appear in the abstract.

Plain-language definitions for a non-clinical reader are in [glossary.md](./glossary.md). Venue rules are in [congress-rules.md](./congress-rules.md).

## Procedures

| Spanish | English | Abbreviation |
|---|---|---|
| Hemicolectomía derecha | Right hemicolectomy | RH |
| Hemicolectomía derecha laparoscópica | Laparoscopic right hemicolectomy | LRH |
| Hemicolectomía derecha laparo-asistida | Laparoscopic-assisted right hemicolectomy | LARH |
| Hemicolectomía izquierda | Left hemicolectomy | LH |
| Colectomía sigmoidea / Sigmoidectomía | Sigmoid colectomy / Sigmoidectomy | — |
| Resección anterior (de recto) | Anterior resection | AR |
| Resección anterior baja | Low anterior resection | LAR |
| Resección anterior ultrabaja | Ultra-low anterior resection | uLAR |
| Resección abdominoperineal | Abdominoperineal resection | APR |
| Resección total mesorrectal | Total mesorectal excision | TME |
| Resección parcial mesorrectal | Partial mesorectal excision | PME |
| Colectomía total | Total colectomy | — |
| Proctocolectomía total con pouch ileal | Total proctocolectomy with IPAA | IPAA |
| Anastomosis intracorpórea | Intracorporeal anastomosis | ICA |
| Anastomosis extracorpórea | Extracorporeal anastomosis | ECA |
| Anastomosis termino-terminal | End-to-end anastomosis | — |
| Anastomosis latero-lateral | Side-to-side anastomosis | — |
| Ileostomía de protección | Protective / diverting ileostomy | — |
| Colostomía terminal | End colostomy | — |
| Resección endoscópica de mucosa | Endoscopic mucosal resection | EMR |
| Disección endoscópica submucosa | Endoscopic submucosal dissection | ESD |
| TaTME (transanal TME) | Transanal total mesorectal excision | TaTME |
| Cirugía robótica colorrectal | Robotic colorectal surgery | — |

## Diagnoses — ICD-10

The codes most frequent in coloproctology.

| Code | Diagnosis | Notes |
|---|---|---|
| C18.0 | Carcinoma de ciego | Carcinoma of the caecum |
| C18.2 | Carcinoma de colon ascendente | "Right-sided colon cancer" |
| C18.3 | Carcinoma de ángulo hepático | |
| C18.4 | Carcinoma de colon transverso | |
| C18.5 | Carcinoma de ángulo esplénico | |
| C18.6 | Carcinoma de colon descendente | "Left-sided" |
| C18.7 | Carcinoma de colon sigmoide | |
| C18.9 | Carcinoma de colon, NOS | When the segment is not specified |
| C19 | Carcinoma de unión rectosigmoidea | |
| C20 | Carcinoma de recto | "Rectal cancer" |
| K50.x | Enfermedad de Crohn | K50.0 ileum, K50.1 colon, K50.8 both |
| K51.x | Colitis ulcerosa | K51.0 pancolitis, K51.2 ulcerative proctitis |
| K57.x | Enfermedad diverticular | The fifth digit is **bleeding**, not perforation: K57.20 *with* perforation and abscess **without** bleeding, K57.21 *with* perforation and abscess **with** bleeding. Diverticular disease *without* perforation is K57.3x — and K57.30 is divertic**ulosis**, a different entity from divertic**ulitis**. |
| K60.x | Fisura/fístula anal | |
| K62.5 | Hemorragia rectal | |
| K63.2 | Fístula intestinal | |
| — | Fístula / dehiscencia anastomótica | **ICD-10-CM has no dedicated code for anastomotic leak** — searching the official index for *anastomotic leak* returns nothing. The generic bucket is **K91.89**, *"Other postprocedural complications and disorders of digestive system"*, which is the bucket and not the diagnosis. Grade it by ISREC (below); the code is not where this complication is described. |

*Provenance: every code above was looked up individually against the NLM's official ICD-10-CM index (`clinicaltables.nlm.nih.gov/api/icd10cm/v3`) on 2026-07-22 — 23 code lookups plus a term search for* anastomotic leak. *Two of the seventeen rows came back wrong, both in the complications half, both corrected above; the other fifteen returned their titles verbatim. Until that morning this table had never been checked against anything, which is the whole reason two false rows sat in it next to fifteen true ones — an unverified reference is not a wrong reference, it is an unchecked one. `K50.x`, `K51.x`, `K57.x` and `K60.x` are category stems; the billable code carries a fifth digit this table does not resolve. **No rule in `rules.md` fires from any of this** — the table is a reading aid, never a constraint the editor can quote (R3).*

## Complications — Clavien-Dindo classification

| Grade | Definition |
|---|---|
| I | Any deviation from the normal postoperative course without need for pharmacological treatment (except antiemetics, antipyretics, analgesics, diuretics, electrolytes, physiotherapy) or surgical, endoscopic or radiological intervention |
| II | Requires pharmacological treatment (including transfusions and total parenteral nutrition) |
| III | Requires surgical, endoscopic or radiological intervention |
| III-a | Without general anaesthesia |
| III-b | Under general anaesthesia |
| IV | Life-threatening complication requiring ICU management |
| IV-a | Single-organ dysfunction (including dialysis) |
| IV-b | Multi-organ dysfunction |
| V | Death of the patient |

**Comprehensive Complication Index (CCI)**: 0–100 scale, weighted sum of all of a patient's complications.

> Slankamenac K, Graf R, Barkun J, Puhan MA, Clavien PA. *The comprehensive complication index: a novel continuous scale to measure surgical morbidity.* Ann Surg. 2013 Jul;258(1):1-7. PMID **23728278** · DOI 10.1097/SLA.0b013e318296c732 — verified against PubMed 2026-07-17.

## Anastomotic leak — ISREC classification

- **Grade A**: radiological leak with no clinical impact
- **Grade B**: requires active intervention but no re-laparotomy (percutaneous drainage, antibiotics)
- **Grade C**: requires re-laparotomy

> Rahbari NN, Weitz J, Hohenberger W, Heald RJ, Moran B, Ulrich A, et al. *Definition and grading of anastomotic leakage following anterior resection of the rectum: a proposal by the International Study Group of Rectal Cancer.* Surgery. 2010 Mar;147(3):339-51. PMID **20004450** · DOI 10.1016/j.surg.2009.10.012 — verified against PubMed 2026-07-17.

The corpus attributed both of these by author-and-year with no identifier. Both attributions turned out to be **correct** — which is worth stating as plainly as the one that didn't (`congress-rules.md`, STROCSS). An unverified reference is not a wrong reference; it is an unchecked one, and checking is cheap.

## Oncologic staging — TNM 8th edition (UICC/AJCC)

For colon and rectum. The source corpus carries the pointer, not the content — current tables are pulled from:

- https://www.uicc.org/resources/tnm-classification-malignant-tumours-8th-edition
- AJCC Cancer Staging Manual, 8th ed.

**This layer is a pointer, not a checklist, and the editor treats it as one.** The corpus contains no T/N/M category, so an abstract declaring "stage III disease" is **not** verifiable here. That is a stated limit, not an oversight: under R3 the editor may not flag what it cannot quote a rule for, so it returns clean on staging rather than guessing. If staging accuracy ever needs to be checkable, the 8th-edition tables have to be brought in from the sources above and cited item by item — nobody here has opened them.

## Standard reported outcomes

These are the outcomes a colorectal abstract is expected to report. A number in an abstract almost always belongs to one of them.

- **30-day / 90-day mortality**
- **Overall morbidity** — Clavien-Dindo ≥II
- **Major morbidity** — Clavien-Dindo ≥III
- **Anastomotic leak rate** — by ISREC grade
- **SSI** — surgical site infection: superficial, deep, organ-space
- **Reoperation rate**
- **Length of stay (LOS)** — mean + IQR ⚠ *pairing disputed — see `glossary.md`; corpus wording preserved, referred to the operator*
- **30-day readmission**
- **R0 / R1 / R2** — oncologic resection margin
- **Lymph node yield** — number of nodes resected; minimum 12 for colon
- **Disease-free survival (DFS)** / **Overall survival (OS)** — at 3 and 5 years

## Protocols and scores

- **ERAS** — Enhanced Recovery After Surgery, ERAS Society guidelines
- **POSSUM / P-POSSUM** — perioperative risk
- **CR-POSSUM** — the colorectal surgery variant
- **ASA** — American Society of Anesthesiologists physical status (I–V)
- **NSQIP** — ACS National Surgical Quality Improvement Program

## Writing conventions

Domain conventions recorded in the source corpus. They describe how the terminology appears on the page — which is how an abstract gets parsed, not a correction checklist.

- **First mention**: full name + abbreviation in parentheses — *"total mesorectal excision (TME)"*. Abbreviation alone thereafter.
- **English terms inside Spanish text** stay in italics when no established translation exists: *staple line*, *single-port*, *no-touch isolation technique*.
- **SI units** always (mm, cm, mL, g — never inches).
- **Operative time** in minutes (not hours-and-minutes in quantitative methods).

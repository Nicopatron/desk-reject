# Glossary

For reading the editor's output without a medical degree. Every term here appears in a critique or in the abstracts being critiqued. The full bilingual terminology is in [nomenclatura.md](./nomenclatura.md); venue rules are in [congress-rules.md](./congress-rules.md).

**Provenance rule.** Unmarked entries come from the operator's corpus. Entries marked **°** are standard surgical usage supplied for this glossary because the corpus *names* the term but never defines it — it is a nomenclature and style reference, not a clinical dictionary. The mark is not decoration: this build's whole ethic is that a claim you can't audit is worth less than one you can, so a definition that didn't come from the source says so. Nothing here is cited as authority; the glossary exists to make the output readable, and no rule in `rules.md` fires from it.

## The operation

**Anastomosis** ° — a surgical join between two hollow structures. Here: the two cut ends of bowel, reconnected after a segment is removed. It is the part that can come apart, which is why so much of this domain measures it. The corpus names its variants: **intracorporeal (ICA)** vs **extracorporeal (ECA)** — whether it is built inside the abdomen or outside through the wound; **end-to-end** vs **side-to-side** — how the two ends meet.

**Right hemicolectomy (RH)** ° — removal of the right colon, rejoined ileum-to-colon. **Low anterior resection (LAR)** ° — removal of the rectum with the anal sphincter preserved, so the patient still defecates through the anus. Preserved is not normal: most patients get some degree of **low anterior resection syndrome** — urgency, frequency, clustering, incontinence — and many spend the first months with a diverting ileostomy, not defecating through the anus at all. **Abdominoperineal resection (APR)** ° — removal of the rectum *and* the anus, which leaves a permanent colostomy. The difference between the last two is the one that matters to a patient. Each has a Spanish canonical form and an abbreviation that appears unexpanded after first mention; see [nomenclatura.md](./nomenclatura.md).

**TME — total mesorectal excision** (*resección total mesorrectal*) ° — the **mesorectum** is the fatty envelope around the rectum carrying its blood supply and lymph nodes, and it is where rectal cancer spreads first. TME removes that envelope *intact*, as one package, rather than cutting into it. **TaTME** is the transanal approach to it; **PME** is the partial version, for tumours high enough not to need the whole thing.

## What goes wrong

**Anastomotic leak** ° — the anastomosis fails to seal and bowel contents escape into the abdomen. Graded by **what it forces the team to do**: **ISREC grade A** = visible on imaging, no clinical impact · **grade B** = active intervention, no re-laparotomy (drainage, antibiotics) · **grade C** = re-laparotomy. The grade is the severity.

**Leak rate** ° — leaks divided by **the patients who had an anastomosis**, not by everyone operated on. An APR patient has no anastomosis and cannot leak, so including them inflates the denominator and deflates the rate. Reported by ISREC grade. The number a colorectal paper is usually about.

**Clavien-Dindo** — the complication scale, graded I to V by the intervention required, not by how bad it felt: **I** = deviation needing no drug or procedure · **II** = drugs (including transfusion) · **III** = a surgical, endoscopic or radiological intervention · **IV** = life-threatening, ICU · **V** = death. Two thresholds do the work in abstracts: **overall morbidity = ≥II**, **major morbidity = ≥III**.

**CCI — Comprehensive Complication Index** — 0–100, the weighted sum of *all* of one patient's complications. Clavien-Dindo grades the worst one; CCI adds them up.

**SSI — surgical site infection** — reported split three ways: superficial, deep, organ-space.

## What gets counted

**Lymph node yield** — how many nodes the resection retrieved. **Minimum 12 for colon** — a hard threshold, and one of the few numbers in this domain that is checkable against a stated floor.

**R0 / R1 / R2** ° — how much tumour was left behind. **R0** = none detectable, margins clear under the microscope · **R1** = clear to the eye, tumour at the margin under the microscope · **R2** = tumour visibly left behind. R0 is the goal and the one most abstracts report.

**LOS — length of stay** — reported as mean + IQR. ⚠ **Pairing disputed** — a mean pairs with an SD, an IQR with a median. Corpus wording preserved rather than silently corrected; referred to the operator (`rules-pending.md`).

**DFS / OS** — disease-free survival / overall survival, reported at 3 and 5 years.

**30-day / 90-day mortality**, **reoperation rate**, **30-day readmission** — the rest of the standard outcome set. See [nomenclatura.md](./nomenclatura.md#standard-reported-outcomes) for the full list.

**ASA** — American Society of Anesthesiologists physical status, I to V. How sick the patient was before anything happened.

**95% CI** (*IC95%* in Spanish) — the interval reported alongside an effect. The corpus's rule is that a magnitude never appears naked: every one carries a statistic.

## How the paper is shaped

**IMRaD** — the structure of an original article: Introduction, Methods, Results, and Discussion.

**Structured abstract** — an abstract with mandatory labelled sections (Background/Purpose · Methods · Results · Conclusions · Keywords), 250–300 words. The alternative is unstructured prose, which is what a case report uses. See [congress-rules.md](./congress-rules.md).

**Reporting guideline** — a checklist that dictates what a paper of a given design must report. The design picks the guideline, not the author: **STROCSS** for surgical cohorts, **STROBE** for observational studies, **CONSORT** for RCTs, **CARE** for case reports, **PRISMA** for meta-analyses.

**Retrospective vs prospective cohort** ° — *when the question was asked, relative to when the outcome happened.* **Retrospective**: it already happened; the author goes back through records written for other purposes — treating patients, not answering this question. **Prospective**: the question comes first, then patients are enrolled and the data is collected forward, on purpose, to answer it.

This is the single distinction the whole claim ladder pivots on ([`rules.md`](../rules.md) R5), so it is worth being exact about *why* it caps the claim. In a retrospective cohort nobody assigned the treatment *for the study's sake* — the surgeon chose, patient by patient, for reasons that are usually absent from the record. The healthier patient plausibly got the newer operation. So when the newer operation shows better outcomes, the design cannot separate *the operation worked* from *the patients were less sick to begin with*. That is what a ceiling of **L1 associate** means: not a demerit on the study, a fact about what it is able to answer. A randomised trial breaks that tie by taking the choice away from the surgeon — which is the only reason it reaches **L3 cause**.

**MeSH terms** ° — Medical Subject Headings, the controlled vocabulary the US National Library of Medicine maintains and indexes PubMed with. A structured abstract closes with 4–6 of them.

**PMID / DOI** — the identifiers that make a citation checkable. The corpus's verification rule: the PMID or DOI must open in a browser and match the cited title and authors. An unverified reference is assumed wrong, not assumed right — which needs no statistic to justify it, and the one that used to sit in this line had no source we could open, in a file whose whole job is telling you where things came from.

# Congress rules

The venues a colorectal abstract is written for, and the submission rules the corpus states as hard numbers. Terminology is in [nomenclatura.md](./nomenclatura.md); plain-language definitions are in [glossary.md](./glossary.md).

**Read the limit of this file first.** The corpus records which congresses are targeted and when they meet. It does not record any congress's own abstract rules. The word counts below are **journal submission defaults**, and the corpus states them with its own caveat — always check the venue's current instructions. Nothing here is a substitute for a live call for abstracts.

## Target congresses

| Congress | Society | Frequency | Typical month | Notes |
|---|---|---|---|---|
| ASCRS Annual Scientific Meeting | ASCRS | Annual | May–June | USA; the main meeting of the year |
| ESCP Annual Meeting | ESCP | Annual | September | Rotating host city in Europe |
| SAGES Annual Meeting | SAGES | Annual | March–April | USA; minimally invasive surgery emphasis |
| Congreso Argentino de Cirugía | AAC / MAAC | Annual | October–November | Buenos Aires; the main regional meeting |
| Congreso Argentino de Coloproctología | SACP | Annual | May–June | Argentina |

| Society | Full name | Site |
|---|---|---|
| ASCRS | American Society of Colon and Rectal Surgeons | https://fascrs.org |
| SAGES | Society of American Gastrointestinal and Endoscopic Surgeons | https://sages.org |
| ESCP | European Society of Coloproctology | https://escp.eu.com |
| AAC / MAAC | Asociación Argentina de Cirugía | https://aac.org.ar |
| SACP | Sociedad Argentina de Coloproctología | https://sacp.org.ar |

Two of the five meet in Spanish and three in English — which is why the language of an abstract is a property of its venue, not a preference.

### What this file does not have, and why the editor doesn't need it

**No submission deadlines.** The corpus records the month each congress meets, never the date its call for abstracts closes. Out of scope on purpose: a deadline is not an input to a critique. Check the live call.

**No per-congress abstract rules** — not one of the five. No word count, no structured-vs-unstructured mandate, no table or figure limit, no author format. Everything under *Abstract length and shape* below is a **journal default from the corpus, not a congress rule.** It is context for reading an abstract, not a rule the editor enforces.

That gap is real, and it costs less than it looks — because **word count is the most visible failure there is.** The submission portal counts the words and refuses the file; nobody submits 400 words to a 300-word call by accident. Under R7 the editor ranks by how *invisibly* a thing fails, so a rule that duplicates what the portal already enforces would spend the attention budget on the one error that cannot escape. The overclaim has no portal. That is where the three findings go.

What the editor does use from below: **the shape** of a structured abstract — which sections must exist — because a missing Methods section is how a design goes undeclared, and an undeclared design is what R2 gates on.

## Abstract length and shape

Journal submission defaults from the corpus. The corpus flags these as approximate and tells you to check the venue's current instructions to authors.

| Abstract type | Length | Shape |
|---|---|---|
| Structured abstract | 250–300 words | Background/Purpose · Methods · Results · Conclusions · Keywords |
| Case report abstract (CARE) | 150–250 words | Unstructured, continuous prose |

### What each section of a structured abstract must carry

- **Background / Purpose** — 1–2 sentences of context plus the objective
- **Methods** — design + setting + participants + intervention + primary outcome + statistical analysis
- **Results** — total n, key demographics, primary outcome with effect size + 95% CI / p-value
- **Conclusions** — 1–2 sentences of interpretation plus clinical implication
- **Keywords** — 4–6 MeSH terms

An unstructured CARE abstract runs introduction + case presentation + conclusion as prose, without those headers.

## Reporting guideline by study design

The guideline is determined by the **study design**, not by the venue — the corpus maps one to the other and does not tie either to a specific congress. A design named in an abstract implies its guideline.

| Study design | Guideline | Official site |
|---|---|---|
| RCT (randomized controlled trial) | CONSORT 2010 | https://www.equator-network.org/reporting-guidelines/consort/ |
| Observational (cohort, case-control, cross-sectional) | STROBE | https://www.strobe-statement.org |
| Case report / case series ≤4 | CARE | https://www.care-statement.org |
| Systematic review / meta-analysis | PRISMA 2020 | https://prisma-statement.org |
| Diagnostic accuracy | STARD 2015 | https://www.equator-network.org/reporting-guidelines/stard/ |
| Surgical studies / surgical cohorts | **STROCSS 2024** | https://www.strocssguideline.com |
| Quality improvement | SQUIRE 2.0 | http://www.squire-statement.org |
| Animal preclinical | ARRIVE 2.0 | https://arriveguidelines.org |

Corpus default: **STROCSS** for surgical cohorts, **STROBE** for general observational studies. RCTs are infrequent.

### Why the STROCSS row says 2024 and the source corpus said 2021

The corpus this file was built from — the operator's own reference file, `guidelines-papers.md:15`. **That file is his and it does not travel with this repo, so the pointer is a pointer for him, not for you**; what is auditable from here is the version, below, by PMID. It says **STROCSS 2021**. That is one version behind. STROCSS 2024 supersedes it. Verified against PubMed on 2026-07-17, whole lineage:

| Version | PMID | Where | Scope |
|---|---|---|---|
| STROCSS 2017 | 28890409 | Int J Surg | cohort studies |
| STROCSS 2019 | 31704426 | Int J Surg | cohort studies |
| STROCSS 2021 | 34774726 · 34820121 — co-published | Int J Surg 96:106165 · Ann Med Surg 72:103026 | + cross-sectional, case-control |
| **STROCSS 2024** | **38445501** — Int J Surg 110(6):3151-65 · DOI 10.1097/JS9.0000000000001268 | **current** | cohort, cross-sectional, case-control |

This is the failure class this editor exists for, one layer up: **an outdated guideline version is invisible.** The abstract still gets written, the reviewer still reads it, nothing errors. The corpus was right when it was written and quietly stopped being right. Nobody gets told.

**Item numbers are not cited from this file.** The version is verified; the checklist's internal numbering is not, because nobody here has opened the 2024 PDF. See `rules.md` R11.

**And the other seven rows have not been checked at all.** CONSORT, STROBE, CARE, PRISMA, STARD, SQUIRE, ARRIVE: their dates come from the same corpus, written before 2026, which has now been demonstrably one version stale exactly once. Assuming the rest are current is the error this section just documented. Logged in [`rules-pending.md`](./rules-pending.md); until each is checked against its own site, this table is a reading aid for those seven and a verified fact only for STROCSS.

## Mandatory statements

The corpus lists these as required at the end of an original article. It does not state whether a congress abstract requires any of them.

- Authors' contributions (CRediT taxonomy)
- Conflict of interest disclosure
- Funding statement
- Ethical approval statement
- Data availability statement

A case report additionally requires an **informed consent statement**: the patient authorised publication of the anonymised case. The corpus marks this one mandatory without qualification.

**These are manuscript requirements, and the editor does not fire on them.** The corpus lists them under *Original Article*; it never says whether a congress abstract carries any of them, and none of the five venues' rules are in hand. So the editor cannot claim a missing ethics statement is a violation in a 250-word abstract — it would be inventing a rule and enforcing it against a real author. Under R3 an unquotable constraint is no constraint: return clean.

## Limitations must be explicit

For the full manuscript the corpus requires limitations to be declared rather than avoided, at minimum: design (retrospective vs prospective) · single-centre vs multicentre · sample size and power · unmeasured confounders · generalisability. Its stated reason: a reviewer will mark them anyway if the author didn't mark them first.

**Same limit as above, and it bites harder here.** The corpus requires this of the manuscript and is silent on the abstract. It is tempting to extend it — a 250-word abstract with a causal conclusion and no limitations line *feels* like it should be flagged. The editor doesn't, and holding that line is the point: R0 says the claim is computed from the declared design, never felt. The abstract's conclusion still gets checked against its design by R5, which is a rule that exists. "Your abstract has no limitations line" is a rule that does not.

If a venue's real rules are ever obtained, this is the first thing to revisit (R11).

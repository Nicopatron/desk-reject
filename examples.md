# Examples

What this editor actually returns. **Every critique below is output — pasted from a run, not written by hand.** A worked example somebody wrote is a teacher for the drift, and it would teach the one thing this build spends its whole contract arguing against: that the editor never misses.

Three runs, three shapes: it **blocks**, it comes back **clean**, and it **refuses**. Then a section on what it got wrong, because it did.

## Read this before you read the examples

**These are a simulation of the runtime, not the runtime.** This editor's home is a Claude Project. To generate these, the folder was assembled into a system prompt and run through `claude -p` locally. Close, not the same, and the difference is visible in the output:

- **The local run does not isolate the machine's own global configuration.** Verified 2026-07-17: the flag that replaces the system prompt does not suppress the user-level instruction files underneath it, and one of those says *"always answer in Spanish."* **One of the three runs below (example 2) opens and closes in Spanish** around an English brief — R1 breaking, caused by the harness, not by the contract. The flag that would suppress it (`--bare`) requires an API key this operator doesn't have. These could not be run clean, so they are shown dirty, with the contaminated parts marked rather than trimmed.
- **Two of the three open by reporting that the agent's own shell tool is broken** and falling back to Track A. That is the harness talking, not the editor. Kept, marked, not counted as part of the critique. Only example 3 came back with no preamble at all.
- **What is not contaminated:** the reasoning about the abstract — the design read, the ceiling, the rung, what got quoted, what got refused. `check.py` computes the same three verdicts independently, offline, with no model involved, and agrees with all three.

**The abstracts are synthetic.** Invented for this file, no patient data, no real study, no real number. They are deliberately **not** the five inputs in [`JUDGE_GUIDE.md`](./JUDGE_GUIDE.md): this file ships inside the Project, so demonstrating on the judge's own test inputs would hand the model the answers before it sits the test — the exact failure this build caught in itself on 2026-07-22 and closed.

**Determinism, measured — the verdict held, the prose did not.** Example 1's input was run a second time, unchanged, against the same build. Both replicates returned the same ceiling (L1), the same asserted rung (L2), the same `blocks`, the same quoted span for the push, and the same secondary finding on the same sentence. What moved: which rule IDs got cited (`R5, R0` one time, `R0, R2, R5` the other), whether the intake count was shown as a ladder or left implicit, whether an *Open questions* section appeared at all, and length — 3.8KB against 2.5KB for one abstract. **And the R9 near-miss in section 4 appeared in one replicate and not the other.** Two runs of one input is the weakest evidence that exists, and it does not overturn 2026-07-17, when this setup returned *different ceilings* for the same input. What it shows is narrower: across this pair, the part a reader is asked to trust — the verdict and the span it rests on — was stable, and everything wrapped around it was not.

Every critique below was audited by [`rewrite-gate.py`](./rewrite-gate.py) — the build's own R9 check — and all three came back clean. Read the last section before deciding what that's worth.

---

## 1 — It blocks: the rung nobody notices

An adjusted retrospective cohort. The conclusion says *predicts*.

```
Background: Anastomotic leak after low anterior resection remains the complication that drives
reoperation and permanent stoma in rectal cancer surgery.

Methods: We retrospectively reviewed 300 consecutive patients who underwent low anterior resection
with total mesorectal excision at two centres between 2018 and 2023. Patients with a diverting
ileostomy formed the comparison group. The relationship between operative time and anastomotic leak
was adjusted for confounders by multivariable logistic regression including age, sex, BMI, ASA
score, neoadjuvant radiotherapy and tumour height.

Results: Leak occurred in 22 of 300 patients (7.3%). Operative time was longer in patients who
leaked (218 vs 176 minutes, p=0.01) and remained independently associated with leak after
adjustment (OR 1.012 per minute, 95% CI 1.004-1.021).

Conclusions: Operative time predicts anastomotic leak after low anterior resection and should be
incorporated into preoperative risk assessment.
```

> ⚠️ **Harness preamble, not the editor** — the agent's shell tool failed, so it fell back to Track A. Kept verbatim.
>
> *Sandbox tooling errored on every Bash call this turn (`EPERM` creating the session-env dir — unrelated to the command itself), so `check.py` can't be run against this abstract. Falling back to **Track A** (R0.1): the checklist applied by hand, in order.*

**The critique:**

> ## Revision Brief — "Anastomotic leak after low anterior resection remains"
>
> **Study as declared** (R2)
> - Design: retrospective, comparative, adjusted for confounders (multivariable logistic regression) — as stated
> - n: 300 — as stated
> - Control/comparison: as stated — *"Patients with a diverting ileostomy formed the comparison group"* (see Also #1 — this group does no visible work in the analysis the Conclusion draws on)
> - Centre: multi (two centres) — as stated
> - Venue: not stated
>
> 1 of 5 intake items missing (venue) → 0–1 missing, full critique, no cap.
>
> **Verdict** (R5)
> Design ceiling: **L1** · Highest claim asserted: **L2** → **blocks**
>
> ### The push
> > "Operative time predicts anastomotic leak after low anterior resection and should be incorporated into preoperative risk assessment."
> > — Conclusions, sentence 1
>
> Your design is retrospective, comparative, adjusted for the confounders you measured — R5 caps that at **L1 associate**. Adjustment narrows confounding for age, sex, BMI, ASA, neoadjuvant radiotherapy and tumour height; it does nothing for what wasn't measured, and here that includes the thing this design structurally cannot separate: a surgeon running longer because the dissection is already proving difficult, versus operative time as an independent forecaster of leak. Those look identical in a retrospective chart.
>
> L2 is reachable in R5's table only when the stated aim is prediction *and* it's validated. Neither holds: there's no stated predictive objective in this abstract, and nothing reported — no discrimination, no calibration, no held-out or external cohort — validates operative time as a predictor rather than a correlate. "Predicts" climbs a rung the design hasn't earned, and the clause behind it — folding an unvalidated number into preoperative risk assessment — recommends acting on that same unearned rung.
>
> This needs to sit at L1, not L2: what the data support is that operative time was independently associated with leak after adjustment. Nothing here builds or tests a predictor.
> `R5, R0` · confirmed
>
> ### Also
> 1. > "Patients with a diverting ileostomy formed the comparison group." — Methods
>    This comparison never resurfaces: Results reports no leak rate, n, or effect size by ileostomy status, and ileostomy status isn't among the six covariates the regression adjusts for. As written, the abstract declares a comparison group that does no visible work in the analysis the Conclusion is built on. `R3, R7`
>
> ### Open questions
> - Which venue is this for? Item (5) is unstated.
> - Was prediction the stated aim, and was operative time's discrimination/calibration checked anywhere (even informally)? That's what R5's L2 exception actually requires — it isn't in the abstract as given.
> - What was the diverting-ileostomy comparison for? If it's a separate finding not shown here, say so.
>
> ---
> **Decision Trace**: R0, R0.1 (Track A, hand-applied), R1, R2, R3, R5, R6, R7 · Track A
>
> **For your log** — paste into `decisions-log.md` (R10):
> ```
> 2026-07-22 | "LAR / operative time and leak" | push: "predicts" asserts L2 on a design capped at L1 (retrospective, adjusted, no stated predictive aim or validation) | rung L2 vs ceiling L1 | R5, R0 | author: ____
> ```

**What to look at.** It never touches the English, which is fine anyway. The `Also` is the interesting part: it caught that the comparison group declared in Methods never appears in Results and isn't among the adjusted covariates — a defect in an abstract *we* wrote, that we hadn't noticed when we wrote it. And the push refuses the tempting shortcut: the objection isn't that *predicts* is a strong word, it's that R5's L2 branch needs a stated prediction aim **and** validation, and neither is there.

**And it has a problem.** See section 4.

---

## 2 — It comes back clean

The same field, an honest conclusion. A checker that fires on everything is not a checker.

```
Background: Diverting ileostomy is used to mitigate the consequences of anastomotic leak after low
anterior resection, but its effect on the leak rate itself is debated.

Methods: Prospective comparative cohort of 250 patients undergoing low anterior resection at a
single centre between 2021 and 2024. Patients receiving a diverting ileostomy were compared against
a control group without diversion, defined a priori. The analysis was adjusted for confounders
using a propensity score.

Results: Leak occurred in 9 of 128 diverted patients (7.0%) and in 21 of 122 non-diverted patients
(17.2%), p=0.01.

Conclusions: In this cohort, diverting ileostomy was associated with a lower leak rate. The design
does not establish that diversion prevents leak, and selection by the operating surgeon cannot be
excluded.
```

> ⚠️ **Contaminated frame, kept verbatim** — this run opened *and* closed in Spanish, which is the harness's *"always answer in Spanish"* rule fighting the build's R1. The Revision Brief itself locked correctly to English, and the run says so mid-sentence: *"Salida en inglés porque así lo exige R1 (lock al idioma del abstract, sin excepción) — es el contrato del propio artefacto que estás corriendo, no una respuesta mía normal."* That same Spanish opening also reports the shell tool failing and the fall back to Track A — *"`check.py` no se pudo ejecutar esta vuelta por un error de entorno en Bash"* — which is the second run the preface counts, and the only place in this file you can check that count against the text. Opening and closing paragraphs are the simulation; the brief between them is the editor.

**The critique:**

> ## Revision Brief — "Diverting ileostomy is used to mitigate the consequences"
>
> **Study as declared** (R2) — Design: prospective comparative cohort, adjusted for confounders (propensity score) · n: 250 (128 diverted / 122 control) · Control/comparison: control group without diversion, defined a priori · Centre: single · Venue: not stated
>
> **Verdict** (R5): Design ceiling **L1 associate** · Highest claim asserted **L1 associate** → **clean**
>
> No finding I can quote. The conclusion's verb — "was associated with" — sits exactly on the ceiling a prospective, comparative, propensity-adjusted cohort carries; it doesn't climb into L2 or L3, and the same sentence names the thing the design can't rule out (selection by the operating surgeon). The numbers reconcile across sections: 9/128 = 7.0%, 21/122 = 17.2%, 128 + 122 = 250 — no mismatch.
>
> Not checked: target venue (item 5 of the intake is missing — doesn't cap this verdict at 0–1 missing, but worth naming for your log); staging, keywords, ethics/funding statements, per-venue word limits — no quotable rule for any of them (`reference/rules-pending.md`).
>
> ---
> **Decision Trace**: R2, R3, R5, R7 · Track A (hand-applied — check.py unavailable this run)

**What to look at.** Clean is a real result and it is stated plainly, not padded into a finding to look useful. It recomputed the arithmetic rather than accepting it. And it named **what it did not check** — which is the part that keeps a clean verdict from reading as coverage.

The closing line of that run, in Spanish, offered: *"Si querés, decime el congreso target y lo dejo completo en el intake."* That is friendlier than [`identity.md`](./identity.md) says this thing is. Harness or not, it drifts toward assistant.

---

## 3 — It refuses, and names what to declare

This is the failure the build found in itself on 2026-07-22 and turned into a rule. The abstract compares, and never says what it compared against.

```
Background: Transanal total mesorectal excision (TaTME) was introduced to improve specimen quality
in low rectal cancer.

Methods: We retrospectively reviewed all patients undergoing total mesorectal excision for mid and
low rectal cancer at our unit between 2019 and 2024. Cases were reviewed for specimen grade,
circumferential resection margin and 30-day morbidity.

Results: The rate of complete mesorectal specimens was 88% versus 79%. Circumferential resection
margin was involved in 4.1% versus 7.6%. 30-day morbidity was 21% versus 28%.

Conclusions: TaTME is safe and improves specimen quality compared with the laparoscopic approach.
```

*(No harness preamble on this one — it came back in English from the first token.)*

**The critique:**

> ## Revision Brief — "Transanal total mesorectal excision (TaTME) was introduced"
>
> **Study as declared** (R2)
> - Design: retrospective (as stated) · comparative vs. single-arm: unresolved — see below
> - n: not stated
> - Control/comparison: **MISSING**
> - Centre: single ("at our unit")
> - Venue: not stated
>
> Your abstract compares — *"The rate of complete mesorectal specimens was 88% versus 79%. Circumferential resection margin was involved in 4.1% versus 7.6%. 30-day morbidity was 21% versus 28%."* — and never says what it compared against. `R2`
>
> Methods declares one cohort: *"all patients undergoing total mesorectal excision for mid and low rectal cancer at our unit between 2019 and 2024."* It never says this cohort contains two techniques, never gives each its own n. The word "laparoscopic" appears for the first time in the Conclusion — *"compared with the laparoscopic approach"* — after three paired results have already gone by unlabelled. That could name an internal arm of the same retrospective review, or it could be a comparison against a benchmark from outside this cohort entirely (published rates, a historical series). Nothing in Methods settles which.
>
> I won't read a control group out of that, and I won't read the silence as you telling me there wasn't one either. Both are me picking your design for you, and one of them just looks modest.
>
> Any one of these and the verdict follows: the comparison arm and its n · that there was no control group · that this is single-arm or a case series.
>
> This isn't a formality here — your Conclusion is already at the top of the ladder (*"is safe and improves"*, L3 cause), which is exactly the case where the ceiling determination matters most and guessing would cost you the most.
>
> **Also missing, independent of the above**: total n is never stated anywhere in the abstract, and no target congress/journal is named.
>
> ### Open questions
> - What was compared: two arms within this same retrospective cohort (TaTME vs. laparoscopic), or TaTME against an outside benchmark? If two arms — n for each.
> - Total n reviewed.
> - Target congress or journal.
>
> Nothing else here is quotable as a finding without inventing a rule I don't have — I'm not raising the unlabelled percentages as a separate item; they're the evidence for the finding above, not a second one.
>
> ---
> **Decision Trace**: R1, R2 · Track A (hand-applied, no code tool)

**What to look at.** Until 2026-07-22 this abstract came back **L0, single-arm** — the script took the silence for a declaration that there was no control, which is a design the author never wrote, at whichever ceiling suited the checker. Now it refuses and says exactly which three declarations would settle it.

It also found the tell nobody planted: *"laparoscopic" appears for the first time in the Conclusion, after three paired results have already gone by unlabelled.* That is the reason the item is genuinely unresolvable rather than merely unstated, and no one writing the input had noticed it.

---

## 4 — What it got wrong

Every worked example scoring perfectly is how a folder teaches that the editor never misses. So:

**The push in example 1 hands the author their verb.** After the diagnosis, it closes:

> *"This needs to sit at L1, not L2: what the data support is that operative time was independently associated with leak after adjustment."*

The first half is direction and R9 explicitly permits it — *"This needs to sit at L0"* is the rule's own example of a legal move. The second half supplies the sentence: subject, the verb phrase the author needs, and the qualifier, in the register of their manuscript. R9 bans *"no replacement text, no suggested phrasing, no example sentence in the register of your manuscript, however short."* Whether that clause crosses the line is arguable. **That it is arguable is the finding** — this is the smuggled rewrite's whole shape, and the build named it the failure mode of the entire assignment.

**And `rewrite-gate.py` cleared it.** Not a bug in the implementation — a consequence of its design, which the file states in its own docstring: *"The tell is never the quotation mark… The tell is the FRAME around the quote."* It anchors on quotes deliberately, because R3 obliges the editor to quote the author in every finding, so a gate that fires on quoted text fires on the editor doing its job. Three of its four detection classes require a quoted span in the clause; the fourth is a fixed list of phrases like *"you could write."* An **unquoted declarative that supplies the phrasing anyway** matches none of them.

So the gate has a blind spot exactly where the failure is subtlest, and it took running the editor to see it. The gate is not deleted and not patched in a panic on deadline day — patching a detector against a single observed miss is how a checker learns the example instead of the class. It is logged in [`reference/rules-pending.md`](./reference/rules-pending.md), with what would close it.

**And it did not happen the second time.** The determinism replicate — same input, same build — reached the same verdict on the same span and closed without supplying any phrasing at all. So the blind spot is real and the behaviour that walks into it is intermittent, which is worse than a reproducible bug rather than better: there is no input that reliably triggers it, so there is no test to write that fails now and passes after a fix.

**One of three runs broke R1**, wrapping an English brief in Spanish on both ends, and the same one closed by offering to do more work for the author. The first is the harness; the second is drift toward assistant that the harness may have carried in with it. Neither would be visible if these examples had been written by hand instead of run — which is the argument for generating them, and it cost the polish to keep it.

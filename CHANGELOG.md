# Changelog

The build's own log: what changed, what it cost, what is still wrong. Newest first, one entry per real day.

This is **not** the assignment log. That one is [`decisions-log.md`](./decisions-log.md) — what the editor raised on *your* abstract and what you accepted or rejected, written by you (R10). This file is about the editor itself, written by its authors.

---

## 2026-07-22 — Day 2

**The day the build was run instead of read.** Day 1 shipped a green self-test, a mutation-tested suite, and six self-audit findings. None of it caught what running the thing caught in an afternoon.

### Fixed: three bugs in `check.py`, all pointing the same way

`JUDGE_GUIDE.md` locked five expected results on day 1, before the editor saw the inputs. Nobody put those inputs through `check.py`. When someone finally did, **three of the four scriptable abstracts disagreed with the script** — and all three times the script was wrong and the prediction was right.

*Which three, and what each was expected to return, is deliberately not written here.* This file ships inside the Project; naming the verdicts would rebuild the answer key one door down from the one closed below, hours after closing it. The evidence lives in `JUDGE_GUIDE.md` §*What happened when the predictions were tested*, which is now the one file kept outside.

| Bug | What it did |
|---|---|
| **Negation had no polarity** | `"grupo control"` sitting inside `"no hubo grupo control"` matched the *presence* detector. English survived only because `"no control group"` happened to be in the stated-absence list. So the same study, in Spanish, got a **more permissive** ceiling than in English — R1 refuted by the script that prints R1 in its banner on every run. The operator writes in Spanish. |
| **Silence read as a declaration** | Item (3) wanted the literal phrase `"control group"`. Two named arms, each with its own n, came back single-arm — and R2 says item (3) is a control **or comparison** group. |
| **The Background prior read as the claim** | A hedged sentence in **Background** is the literature's reason for doing the study. Scored as the author's own L3 assertion, it blocks the rationale of nearly every abstract ever written — including abstracts whose own conclusion never leaves the ceiling. |

**They fail in one direction: each reads the abstract toward the stronger design or the bigger claim.** That is R0 inverted, in the file that computes R0. A green suite could not see it, because every case in the suite had been written by the same reading. Fixed at the cause rather than the instance — polarity is a rule about negators near any ceiling-lifting feature, not a longer list of denied phrasings — and pinned: self-test **12 → 18 cases**, including the ES/EN minimal pair, so the two languages can never silently diverge again.

### Fixed: R2 now publishes what *stated* means, and that is the real repair

R0.1 promises *"same inputs, same answer"* across Track A (a human, by hand) and Track B (the script). It could not deliver. The definition of intake item (3) lived in a list of substrings inside `check.py` that the contract never published, so the human and the script were applying different rules and neither could see the gap.

R2 now carries the definition in the contract, where both tracks read it: four rows resolving to three states — present, absent, and one that is new. The new one is what costs us something: **an abstract that compares and names no group either way leaves item (3) MISSING** — not stated-absent. The script refuses the claim verdict and names what to declare.

R2 had held two rules that cannot both be true over that abstract: that item (3)'s silence resolves to *"stated: absent — silence, uncontradicted"* and that *"I never assume a control group exists because the prose implies a comparison."* One reads it single-arm, the other refuses to read it comparative. The code resolved the contradiction the way code does — silently, by picking one, toward the ceiling that suited it. Naming the third state is the fix; refusing is what naming it costs.

### Fixed: the species from day 1 — claims about artifacts that don't exist

Day 1 logged three instances and asked whether day 2 would fix the species or the instances. There were **five**, not three — **at their day-1 positions**: `rules.md:33` (a landing page and its browser gate — neither exists), `rules.md:35`, `README.md:37` and `JUDGE_GUIDE.md:138` (all three claiming `--self-test` pins the verdicts in `examples.md`; it runs embedded cases and never reads that file), and `README.md:63`, a dead link to a file that did not exist. All corrected, and not all the same way: `rules.md:35` now states what the self-test does and does not pin, the README and `JUDGE_GUIDE` sentences were rewritten out rather than relocated — grep them today and there is nothing to find — and the README link, now at `README.md:58`, resolves because `examples.md` exists. `rules.md` R0.1 now also names the limit that made the species possible: the two tracks converge only for the steps whose definitions are published.

### Fixed: the ICD-10 table had never been checked against anything

Verified code by code against the NLM's official ICD-10-CM index on 2026-07-22 — 23 lookups plus a term search. **Two rows were wrong**, both in the complications half:

- `K91.83` was labelled *"Anastomotic leak, postoperative."* It is **Postprocedural hepatorenal syndrome**. And searching the official index for *anastomotic leak* returns **nothing**: ICD-10-CM has no dedicated code for it. So the row was not stale, it was invented — describing the central complication of the whole domain, in the one reference table with no identifier to check it against, twenty-eight lines above a paragraph congratulating this build for verifying its citations.
- `K57.20 / K57.21` were captioned *without / with perforation*. The fifth digit is **bleeding**; both are with perforation and abscess. Disease *without* perforation is `K57.3x` — and `K57.30` is divertic**ulosis**, a different entity from divertic**ulitis**.

Fifteen of the seventeen rows were correct. The ratio is the number, not "the corpus is unreliable" — and it is the same one day 1 reported about the corpus: an unverified reference is not a wrong reference, it is an unchecked one. Day 1 wrote that sentence and then shipped an unchecked table. The table now carries its provenance and its date, and nothing in `rules.md` fires from it.

**`LAR`** in the glossary promised the patient *"still defecates normally."* Sphincter preserved is not function preserved — most patients get some degree of low anterior resection syndrome, and many spend months with a diverting ileostomy. The entry was marked `°` (written for the glossary, not from the corpus), which declares where a definition came from and does nothing about whether it is true.

### Found: the judge was being handed the answer key

`README.md` and `JUDGE_GUIDE.md` both said to load *this whole folder* as project knowledge. `JUDGE_GUIDE.md` is in the folder, with the expected result of every test in it. The model reads it: in a contaminated run on 2026-07-17, one cited the guide by name mid-critique and reported that the locked prediction had held — announcing it had read the answer before answering. No clean run said anything of the kind. **The sentence itself is quoted in `JUDGE_GUIDE.md`, not here**, for the reason below.

Both setup instructions now exclude the file. The cost is that the runs behind `examples.md` are the only ones that count, and the earlier contaminated ones are unusable.

**And the first draft of this entry leaked the same way.** It quoted that confession verbatim — test number, locked verdict and all — thirty-five lines under its own promise not to name them. This file ships inside the Project. A quarantine that covers one filename and not the log describing it is not a quarantine, and the leak read as evidence rather than as a disclosure, which is what made it hard to see. Caught by a reviewer, hours after the fix it was undermining.

### Decided: R5's hole stays open, and this is the entry that says why

Day 1 left the ceiling table's gap — prospective, comparative, unadjusted matches no row — *"deliberately unresolved… it waits for the domain review rather than being decided by whoever noticed."*

A domain review ran, and rejected the day-1 hypothesis with it: rows 2 and 3 cannot collapse, because row 3 is *"L1 (L2 if the stated aim is prediction and it's validated)"* — the adjustment **is** the gate to L2, and collapsing would hand L2 to unadjusted studies. There is no validated prediction without adjustment. So day 1's own guess at the fix was wrong, and the CHANGELOG line proposing it (above, under Day 1) is left standing rather than edited, because that is what this file is for.

A second candidate — widen row 2 to *retrospective **or** prospective*, unadjusted, still L1 — went to three independent reviewers instructed to refute it. **All three refused it, and the strongest objection was one nobody on this build had seen:** `check.py` fires `prospective` on the token, and *"retrospective analysis of a prospectively maintained database"* is standard surgical phrasing. Today that noise is harmless because row 2 requires `retrospective`. Widen the row and a token that describes a **database** starts carrying the weight of a **design**.

The second objection was ours, aimed back at us: fixing a clinical ceiling table on deadline day, from a reviewer's judgement, is precisely *"decided by whoever noticed"* — which would make the day-1 line above false, in the build whose previous round was marked down for a claim nobody could audit.

**So the hole stays, the script keeps refusing, and `refuse_contract_gap_prospective_unadjusted` stays in the suite.** It costs nothing; the fix would have cost a clinical judgement made on deadline day.

### Fixed: the authority claim, which was last round's push wearing new clothes

The README's second line said this editor was *"built from the correction logic of a working chief of colorectal surgery — the corrections he makes on an abstract before it goes out."* `identity.md` said it again, almost word for word.

Reviewers opened the reference file it points at. It is a nomenclature, venue and style reference — material for **writing** a paper. There is no record in it of corrections he made to anyone's abstract. The sentence describes an artifact that does not exist, and it describes it in the position where a reader decides whether to trust the rest.

Worse, the same README already contradicted it: the claim ladder — the actual critique mechanism — is declared *"our own synthesis. No paper contains it"* twelve lines down, and not one mechanism anywhere in the file is traced to him. So the authority sentence was borrowing a credential nothing else in the file supported.

What is true, and now what it says: **the domain comes from his reference file; the critique logic doesn't.** Two things also moved into *Limits, up front*, out of a 22KB changelog where nobody would find them — that **he has never run this**, and that his file **is not in this repo**, so "the corpus" is a source the reader cannot open. Alongside them, the part of the trail that *is* checkable without it: this build read that file closely enough to catch its STROCSS mapping was a version stale, and marks with `°` every glossary entry that didn't come from it.

A reviewer also killed the fix we were about to make. The first draft of the replacement claimed the domain rests on *"a domain the author knows first-hand."* The author does not — the surgeon is his father. Swapping one unauditable claim for another would have been worse than leaving it.

Two more of the same species went with it: the corpus was cited as `guidelines-papers.md:15`, a path syntax that promises a file the reader can open and cannot, now disclosed at the citation; and a statistic — *"roughly 25% of LLM-proposed references are fabricated"* — sat unsourced in the glossary, justifying the build's own verification rule. It is gone. The rule stands on its reasoning, which is what it should have been standing on in a file whose job is saying where things came from. And `rules-pending.md` claimed the editor *uses* one of its own pending rows, in the file whose entire job is holding what is **not** yet a rule.

### The audit ate its own rule, and a third of it died

Twenty-three findings came out of an adversarial pass. Ten were queued to act on today. Each went to **three independent reviewers with instructions to refute and a default of refuted** — the build's own R3, aimed at its own audit.

**Seven survived** and were fixed: both ICD rows, the LAR definition, and the four above. **Three were killed**, and the reasons are recorded below:

- *Widen R5's row 2* — refuted 3/3, above.
- *The ladder computes `ceiling(design)` and is blind to `ceiling(result)`, so an L1 verb over a statistically null difference should still fire* — refuted 2/3. The finding quoted half of the conclusion it was judging. The rest of that conclusion reported its own non-significance, named the selection bias it could not exclude, and asked for a trial — which is Lazarus's **low** spin level: *"spin reported with uncertainty **and** recommendations for further trials."* Firing on a conclusion that states its own uncertainty is the checker firing on everything.
- *`LOS — mean + IQR` is a mismatched pair* — refuted 2/3. The pairing is wrong, but the entry is **unmarked**, meaning the build attributes it to the operator's corpus. Silently correcting it would misrepresent the source we cite. It goes to the operator, not into a patch.

Three findings that read as solid, from a careful pass, and every one of them would have been a change for the worse. Two of the seven that *did* survive also came back with their proposed fix corrected by the reviewer rather than endorsed. This is the second time in two days the same lesson has landed: **a finding nobody tried to kill is a hypothesis wearing a finding's clothes** — and so is the fix attached to it.

### Found by running it: `rewrite-gate.py` has a blind spot, and it is where the failure is subtlest

One of the runs behind `examples.md` closed a push with *"what the data support is that operative time was independently associated with leak after adjustment."* Direction, then the author's sentence — subject, verb phrase, qualifier, in the register of their manuscript. R9 bans *"no suggested phrasing, no example sentence in the register of your manuscript, however short."* Whether that clause crosses the line is arguable; that it is arguable is the point, because this is the smuggled rewrite's exact shape and R9 calls it the failure mode of the whole assignment.

**The gate cleared it**, and not by accident. Three of its four classes require a quoted span in the clause and the fourth is a fixed phrase list, because R3 obliges the editor to quote the author in every finding — a gate that fires on quoted text fires on the editor doing its job. The docstring says so: *"The tell is never the quotation mark… The tell is the FRAME around the quote."* An unquoted declarative that supplies the phrasing anyway has no frame to catch.

Logged in `reference/rules-pending.md`, not patched. A detector patched against one observed miss learns the example instead of the class, and doing it on deadline day would be the same haste this build spent the morning undoing. The gate catches the framed rewrite, misses the unframed one, and now says so.

### Added: `examples.md`, and what it is worth

The fifth mandatory slot, generated by running the editor rather than written. Three runs, three shapes — blocks, clean, refuses — on abstracts deliberately **not** taken from `JUDGE_GUIDE.md`, because this file ships inside the Project and demonstrating on the judge's own test inputs would rebuild the answer key with a different filename.

It carries its own provenance note, and the note carries the parts that hurt: the local runtime is a **simulation** and does not isolate the machine's global configuration, so one of the three runs wraps its English brief in Spanish on both ends, which is R1 breaking; and that same run closes by offering to do more work for the author, which is friendlier than `identity.md` says this thing is. Both are written into the file rather than left for someone to notice.

Two things the editor found that nobody had planted: in one abstract, a comparison group declared in Methods that never reappears in Results and isn't among the adjusted covariates; in another, that the word naming the comparator first appears in the Conclusion, three paired results after the comparison starts. Both were defects in inputs **we** wrote and hadn't seen.

### Still broken / still true

- **`decisions-log.md` is still empty, on purpose.** Synthetic abstracts run by the build's own authors are not the operator's work, and writing them in would make the mechanism look exercised when it isn't — which is what that file's own comment refuses to do.
- **No receipt from the intended user.** The operator has still not run this on real work. Every claim here about what the editor does to real abstracts remains a claim about abstracts we wrote ourselves.
- **`contract-coherence` ran today — the fifth lens, and the one that reads the contract files against each other.** It found six things, two of them lethal and *both of them written today*: this entry leaking the answer key it was announcing the closure of, and it claiming `examples.md` existed before it did. Two audit lenses still never ran. What is listed here is what was found, not the floor of what is wrong.
- **`rewrite-gate.py` misses the unquoted rewrite**, above and in `examples.md` §4. Logged in `reference/rules-pending.md`, deliberately not patched today.
- **Determinism: measured once, and only the verdict held.** The replicate ran after the API limit reset. Same input, same build, twice: same ceiling, same rung, same `blocks`, same quoted span, same secondary finding. What differed was the rule IDs cited, whether the intake ladder was shown, whether an *Open questions* section existed, the length (3.8KB vs 2.5KB) — and whether the R9 near-miss happened at all. One input twice is not a determinism result; it does not overturn 2026-07-17, when the *ceilings* themselves differed. Written up in `examples.md`.
- **The contract got heavier, and that is the wrong direction.** `rules.md` 11.9KB → 14.2KB (R2's published definition, R0.1's statement of where the two tracks stop converging, R5's statement that it refuses on a missing row); `reference/output-contracts.md`, which `rules.md:3` declares *"contract too"*, 6.7KB → 8.7KB (two refusal shapes that existed only in `check.py`, and the third state of intake item 3 that the template was silently missing). **Effective contract: 18.6KB → 22.9KB, up 23% in one day.** Against last round's *"31KB of rules is a heavy contract"* there is still room, and every byte of it bought a definition that was previously hidden in a script — but said plainly, today's fix was paid for in the currency the judge already flagged, and the next one has less room to spend. And the number a judge running `du -sh` actually sees is bigger than either: **142KB of markdown plus 63KB of scripts**, of which the changelog you are reading is 30KB and `check.py` — which grew 31KB → 44.9KB today, mostly self-test cases and the comments explaining why each mechanism exists — is 44.9KB. Only `rules.md` and `output-contracts.md` are the contract. All of it is what gets loaded.
- **`rules.md:73` — R4.3 contradicts R9**, found on day 1 and untouched. R4.3 forbids saying what would make the claim pass; R9 permits direction (*"this needs to sit at L0"*), which is saying what would make it pass. Named, not resolved.
- **R5 labels its verb column *"Example verbs"*** while `check.py` treats the lexicon as closed. Found day 1, and not closed since — the script now states the conflict as unresolved at its own lexicon (`check.py:66-73`) instead of leaving the reader to find it. If closed, *"demonstrates efficacy"* returns clean on a real overclaim.

## 2026-07-17 — Day 1

**The thesis, and the contract that enforces it.**

### Added
- `rules.md` — R0–R11, one page, rule IDs citable from the first commit.
- `identity.md` · `README.md` · `JUDGE_GUIDE.md` (5 tests, expected locked before any run) · `decisions-log.md` (empty, on purpose) · `reference/` ×6.
- `check.py` (12/12 self-test) · `rewrite-gate.py` (24/24). Every lexicon entry traces to R5 — `"R5"`, `"R5 + forms"`, or `ES of "<verb>"`. No verb was invented for either script.
- **Mutation testing on the self-tests.** 9 mutations to load-bearing decisions; 8 died, 1 survivor documented as a genuinely redundant layer. A green suite that no mutation can turn red is decoration — this one was checked rather than assumed. The two extra `rewrite-gate` cases (22 → 24) are false-positive guards the mutation run exposed.

### Found: R5's ceiling table has a hole, and the code refused to paper over it

Implementing `step2_ceiling` against R5 surfaced a gap in the table **we wrote**:

| R5 row | Matches |
|---|---|
| Retrospective comparative, control, unadjusted | retrospective **only** |
| Retrospective/prospective comparative, **adjusted** | requires adjustment |

A **prospective, comparative, unadjusted** study matches neither. It falls through the table.

The script does not guess. It returns no ceiling and refuses the claim verdict — surfaced as a self-test case, `refuse_contract_gap_prospective_unadjusted`. The alternative was to quietly round the study to the nearest row, which is what a helpful implementation does and is exactly the failure this editor exists to catch: an unstated assumption, invisible, applied to someone's real abstract.

**A contract gap made loud beats a contract gap patched by whoever implements it last.** The fix belongs in `rules.md`, not in the code that reads it, and it is not written yet — the likely shape is that rows 2 and 3 collapse, because in our own table adjustment does **not** lift the ceiling (both are L1). If that holds, the table gets shorter and says something truer: adjusting for measured confounders narrows your interval; it does not buy you a rung.

Deliberately unresolved for now: the fix changes what the editor tells real surgeons, so it waits for the domain review rather than being decided by whoever noticed.

### Found: the source corpus is one version behind, and nothing said so

Building `congress-rules.md` surfaced a conflict. The operator's corpus (`guidelines-papers.md:15`) maps surgical cohorts to **STROCSS 2021**. That guideline has been superseded. Verified against PubMed, whole lineage: 2017 (PMID 28890409) → 2019 (31704426) → 2021 (34774726 · 34820121, co-published) → **2024 (38445501, current)**.

Fixed. But the interesting part is not the fix — it is the failure class. **An outdated guideline version is invisible.** The abstract still gets written. The reviewer still reads it. Nothing errors, nothing warns, no portal rejects it. The corpus was correct when it was written and quietly stopped being correct, and the only reason anyone found out is that someone went and looked.

That is R0 — the thesis of this editor — one layer above where we designed it to live. We aimed it at the surgeon's claim. It fired on our own source material first.

### Found: our own secondary source argues against a naive reading of R5

`reference/claim-ladder.md` cites Haber 2022 (PMID 35925053) for the numbers on how strongly its reviewers heard cause. Reading the actual abstract rather than the numbers we'd already extracted turned up its closing sentence: *"This research undercuts the assumption that avoiding 'causal' words leads to clarity of interpretation in medical research."* Over half of its reviewers heard causal implication in the word **association** — the word our ladder parks at L1.

Quoting Haber's percentages and dropping that sentence would have been spin, in a build about spin. Cheap to do, nearly impossible to catch, and fatal on the one axis this build claims.

So it's in the file, load-bearing: **Haber is now the strongest argument for R9.** If a word swap fixed the problem, a rewriter would be the right tool — hand you the correct verb, done. Haber measures that it doesn't. The verb is where the check starts, not where it ends, and handing you a better one would relocate the overclaim while convincing you it was handled. R9's refusal stopped being a rule about scope and became a consequence of the evidence.

The general lesson, logged because it will recur: **numbers extracted from a source are not the source.** Everything cited in this build gets read whole, including the parts that argue with us.

### Calibration: the corpus was right about the other two

Two attributions carried author-and-year with no identifier. Both check out:
- **CCI** → Slankamenac K, Graf R, et al. Ann Surg 2013 · PMID 23728278
- **ISREC leak grading** → Rahbari NN, Weitz J, Hohenberger W, Heald RJ, et al. Surgery 2010;147(3):339-51 · PMID 20004450

Worth stating as plainly as the one that failed. An unverified reference is not a wrong reference — it is an unchecked one, and the check costs a minute. One of three was stale.

### Decided: no word-count rule, and it follows from R7 rather than from laziness

The corpus has **no per-congress abstract rules** — not for any of the five venues. No word count, no section mandate, no table limit. Rather than fetch them, scoped them out, because the rule that would use them shouldn't exist: word count is the most *visible* failure in the domain. The submission portal counts the words and refuses the file. R7 ranks findings by how invisibly they fail, so a word-count rule would spend a slot of a three-finding budget on the one error that physically cannot reach a reviewer.

The overclaim has no portal. That is what the budget is for.

### Declared unverifiable, editor returns clean
- **TNM staging** — the corpus carries a pointer to the 8th-edition tables, not the tables. So "stage III disease" is not checkable here, and under R3 the editor may not flag what it has no quotable rule for. Nobody on this build has opened those tables; saying so is cheaper than pretending.
- **Ethics / funding / consent statements in abstracts** — the corpus requires them of the *manuscript* and is silent on abstracts. No rule, no finding.
- **A limitations line in an abstract** — same gap, and the tempting one. A 250-word abstract with a causal conclusion and no limitations line *feels* flaggable. R0 says the claim is computed, never felt. It doesn't fire.
- **Seven other guideline versions** in the STROCSS table (CONSORT, STROBE, CARE, PRISMA, STARD, SQUIRE, ARRIVE) — dates come from the corpus, unchecked against their official sites. The corpus has now demonstrably been stale once. Assuming the rest are current is exactly the error just found.

### Audited ourselves, and the contract failed its own rule

An adversarial pass over the day's work, every finding required to quote a verbatim span and its `file:line` — the build's own R3, turned on the build. Findings, all real, none fixed yet. **The line numbers below are day-1 positions and no longer resolve** — the files moved under them on day 2:

| Where | What |
|---|---|
| `rules.md:35` | Claims `--self-test` "pins every verdict in `examples.md`". **False twice over**: `examples.md` doesn't exist, and the self-test runs on embedded cases, not on it. |
| `rules.md:33` | Declares the landing page's browser gate "the official no-code verification path". **There is no landing page.** |
| `rules.md:61` | **R4.3 contradicts R9.** R4.3: never say what would make the claim pass. R9: direction is legal — *"This needs to sit at L0"*. That is saying what would make it pass. |
| `README.md:63` | Links `examples.md`. It doesn't exist, and `reference/output-contracts.md` delegates to it for what a critique *says* — so nothing in this repo shows the editor's actual output. |
| `rules.md` R5 | Labels its verb column **"Example verbs"** — illustrative — while `check.py` treats the lexicon as a **closed list**. If closed, a surgeon writing *"demonstrates efficacy"* gets **clean** on a real overclaim. If illustrative, nothing can be computed. R5 has to pick one and say so. |
| `rules.md` R5 + `reference/claim-ladder.md` | **A prospective, comparative, unadjusted study matches no row of the ceiling table.** Duplicated in both files. |

Three of these are one species: **`rules.md` asserts things about artifacts that don't exist.** That is this build's own thesis, aimed at the build — a claim made past what the design carries, invisible, surviving because nobody looked. It is also, precisely, the note this project got from the judge in the previous round: *a claim I can't audit, in a build whose whole ethic is auditability.*

Logged rather than quietly fixed, because the date matters: found on day 1, and whether we fix the species or just the three instances is what day 2 will show.

### Known broken / not yet built
- **`examples.md` does not exist** — the last of the five mandatory slots still missing, and now unblocked (`check.py` exists). It will be **generated by running the editor**, never hand-written. A worked example is a teacher; a hand-tuned one teaches the drift, and every example that scores perfect teaches that the editor never misses.
- **No receipt.** The operator has not run it. Nothing here has met a real abstract. Every claim in this folder about what the editor does to real work is, today, a claim about what it does to abstracts we wrote ourselves.
- **No landing page was ever built** — `rules.md`, at its day-1 line 33, said otherwise. Corrected 2026-07-22; the rule now states plainly that Track A applied by hand *is* the no-code path.
- **The audit is 2 lenses of 7.** Five lenses never ran: provenance re-verification, contract coherence, brief compliance, the previous round's debts, and domain medicine. **What's listed above is what two readers found before being stopped — not the floor of what's wrong.**
- **The 31KB debt is unmeasured.** Last round's note was *"31KB of rules is a heavy contract"*. `rules.md` is now 11.9KB — but `reference/` adds 42KB and `rules.md:3` declares `output-contracts.md` "contract too". Effective contract ≈ 18.6KB. Whether that closed the debt or relocated it is not yet judged, and self-absolution doesn't count.

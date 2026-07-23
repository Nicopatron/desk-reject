# desk-reject

**An editor for colorectal surgery congress abstracts. It won't fix your English — it finds the claim your study design can't carry, quotes the line, and hands it back.**

**The domain comes from a working chief of colorectal surgery's own reference file**: the nomenclature, the venues, the outcome set an abstract in this field is expected to carry. **The critique logic doesn't** — the claim ladder is this build's synthesis, and [`reference/claim-ladder.md`](./reference/claim-ladder.md) says so before it says anything else.

---

## Why this exists

**Bad English is visible. A claim your design can't carry is not.**

Your co-author fixes the English. The congress reviewer reads your abstract in a few minutes, in a batch of dozens. Nobody in that chain has the job of asking whether your retrospective series of 23 patients can support the word *superior* — and so it goes out, gets accepted, gets cited, and can't be walked back.

This is measured, not a hunch. In abstracts of non-randomized studies evaluating an intervention, **84% contain at least one instance of spin, and causal language is the most prevalent form — 53%** (Lazarus 2015, n=128, PMID 26462565; full provenance in [`reference/claim-ladder.md`](./reference/claim-ladder.md)).

And an AI that rewrites your abstract makes this *worse*. It polishes the prose and leaves the overclaim — or makes it more persuasive. **AI doesn't make science better. It makes bad science sound better.**

So this editor does the opposite of help. It computes what your design carries, quotes the line where your claim went past it, and gives you nothing to paste.

## Use it

1. Create a Claude Project (or any assistant that reads a folder).
2. Drop this folder in as project knowledge — **all of it except [`JUDGE_GUIDE.md`](./JUDGE_GUIDE.md)**, which carries the expected result of every test in it. Keep that one open beside you instead. A model that can read the answers has been caught reading them (`CHANGELOG`, 2026-07-22).
3. Paste your abstract. Spanish or English — it answers in whichever you wrote.

You get back a **Revision Brief**: at most three findings, exactly one marked as *the push*, each quoting the line it's about. Then you go fix it. It will not write it for you, and asking harder doesn't change that.

**It runs with no code tool.** A Claude Project can't execute Python, so the model applies the checklist in `check.py` by hand, step for step — that's the official path, not a fallback ([`rules.md`](./rules.md) R0.1). The scripts are there so you can audit that the procedure is real:

```bash
python3 check.py --self-test          # 18 synthetic cases embedded in the script
python3 rewrite-gate.py --self-test   # the editor audited for its own worst failure
```

Offline, stdlib only, no server, no key.

## See it in 3 minutes

Paste the trap draft in [`JUDGE_GUIDE.md`](./JUDGE_GUIDE.md): an abstract with clumsy ESL English **and** a conclusion its methods don't support.

A rewriter takes the bait — fixes the English, hands back a better-written abstract making the same unsupported claim. This one ignores the English entirely, quotes the contradiction, and names the rung. Then tell it *"I don't have time, just write it for me"* and watch it refuse and explain why the friction is the product.

## What it will not do

- **Write your prose.** Not the abstract, not a paragraph, not a sentence, not a word (R9). Including when you ask nicely, in a small way, for just one word.
- **Copyedit.** Grammar, tense, ESL phrasing: not its job, not even as an aside. Every one of those costs a slot from a three-finding budget.
- **Grade you.** No scores, no rubrics, no "strong abstract".
- **Guess.** No declared design, no claim verdict — it asks (R2). In doubt it assumes the *weaker* design.
- **Return fourteen findings.** An editor that hands you a list is a linter handing your judgment back. Choosing what not to say is the work.

## What's in the folder

| File | Job |
|---|---|
| [`identity.md`](./identity.md) | who the editor is, what it reviews, what it refuses |
| [`rules.md`](./rules.md) | how it critiques — R0–R11, one page, every rule citable |
| [`examples.md`](./examples.md) | what a real critique looks like, including the ones it gets wrong |
| [`reference/`](./reference/) | the ladder and its evidence · nomenclature · venues · glossary · output formats |
| [`check.py`](./check.py) · [`rewrite-gate.py`](./rewrite-gate.py) | the procedure, executable and auditable |
| [`decisions-log.md`](./decisions-log.md) | what it already raised on your abstract, and what you decided |
| [`CHANGELOG.md`](./CHANGELOG.md) | the build's own log — what changed, what it cost, what's still wrong |

Not a doctor? [`reference/glossary.md`](./reference/glossary.md) exists so you can read the output anyway.

## Limits, up front

- **He hasn't run it.** The surgeon whose reference file the domain came from has never put a real abstract through this editor. Every claim in this folder about what it does to real work is a claim about abstracts we wrote ourselves.
- **That reference file is his and it is not in this repo.** So "the corpus", where you see it cited, is a source you cannot open. What you *can* check without it: this build read it closely enough to catch that its STROCSS mapping was a version stale ([`reference/congress-rules.md`](./reference/congress-rules.md)), and every glossary entry that did **not** come from it carries a `°`. That is the audit trail we can actually hand you, and it is narrower than the word "corpus" makes it sound.
- **One surgeon's reference, not a consensus.** Not a guideline committee, not the literature.
- **The claim ladder is our own synthesis.** No paper contains it. The evidence it stands on is real and cited; the four rungs are a design tool. [`reference/claim-ladder.md`](./reference/claim-ladder.md) says so at the top and states the case *against* itself.
- **There is no EQUATOR reporting guideline for congress abstracts of observational surgical studies.** Verified. This ladder fills that gap as a synthesis, not as a standard.
- **It doesn't check staging, word counts, or ethics statements** — no rule it can quote, so it returns clean and says which. A clean verdict names what it didn't check.
- **The log is yours to paste.** Claude can't write files in a Project. Any claim that this thing logs your decisions automatically would be false.

## Credit

The methodology is [Clief Notes](https://www.skool.com/clief-notes) interpretable context: folders as architecture, each file doing one job.

The one-push review form — the single change that most improves the thing, not a list — is Jake Van Clief's.

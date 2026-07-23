#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check.py — R0.1 Track B: compute the claim verdict for an abstract.

Contract: ./rules.md, same directory. On any divergence, rules.md wins and this
file is the bug.

The runtime is a Claude Project, which has no code tool. This script will almost
never run. Its job is to be the executable spec of R0.1's Track A procedure — the
one a human applies by hand — so the output prints every step, its evidence, and
the rule that fired. Anything a reader cannot replicate with the printed table and
a highlighter does not belong in here.

R0.1's steps, in order, unreordered:

    STEP 1  extract the declared design                              (R2)
    STEP 2  read its ceiling from the R5 design table                (R5)
    STEP 3  scan the claim lexicon, ES+EN, keep the highest rung     (R5, R1)
    STEP 4  compare rung(verb) vs ceiling(design)
    STEP 5  verdict

R3 is the hard floor: every finding carries a verbatim span plus its location.
No span → no finding → clean on that axis.

Usage:
    python3 check.py --abstract <file>    exit 0 clean · 1 block · 2 refuse
    python3 check.py --self-test          exit 0 all pass · 1 any fail

Python 3 stdlib only.
"""

import argparse
import re
import sys
from bisect import bisect_right

# --------------------------------------------------------------------------
# Patterns
# --------------------------------------------------------------------------


def _rx(phrase):
    """Literal phrase -> case-insensitive, word-bounded regex with loose spacing.

    Loose spacing so a phrase survives the line wrap of a pasted abstract.
    Lookarounds instead of \\b because every phrase here starts and ends on a word
    character, and \\b misbehaves at accented boundaries in some readings.
    """
    body = r"\s+".join(re.escape(w) for w in phrase.split())
    return re.compile(r"(?<!\w)" + body + r"(?!\w)", re.IGNORECASE | re.UNICODE)


RUNG_NAME = {0: "L0 describe", 1: "L1 associate", 2: "L2 predict", 3: "L3 cause"}

# R5's claim ladder. Each entry: (rung, lemma, surface forms, provenance).
#
# Provenance is printed with every finding, so a reader can tell the contract's
# words from words this file added:
#   "R5"            verbatim from the R5 table in rules.md
#   "R5 + forms"    other inflections of a verb R5 names — same lexical item
#   "ES of <x>"     the Spanish register of an R5 entry. rules.md lists English
#                   only; R1 requires both languages and states the ladder
#                   resolves to the same rung in either. These translations are
#                   this file's addition and are flagged as such.
#
# reference/claim-ladder.md ratifies the lexicon as the build's own: "The verb
# lexicons in check.py are ours too — assembled for this build, in Spanish and
# English … visible in the script and arguable line by line, which is the only
# defence they have." That ratifies AUTHORSHIP and nothing else. Whether the
# list is CLOSED or merely illustrative is NOT settled: rules.md:85 labels its
# column "Example verbs" while this file reads the lexicon as closed. Logged in
# CHANGELOG.md §Still broken / still true, open since day 1. rules.md wins if it
# ever picks — see line 5.
# A verb outside the table produces no finding — R3: no quote, no finding,
# return clean.
#
# TODO: verificar — residual Track A gap. A human hand-applying R0.1 will judge
# a verb this table omits; the script returns clean on it. R0.1 promises "same
# inputs, same answer" across tracks, so an unlisted claim verb belongs in
# reference/rules-pending.md and then here — never improvised into a finding.
CLAIM_LEXICON = [
    # ---- L0 describe ----
    (0, "perform", ["performed", "perform", "performs", "performing"], "R5 + forms"),
    (0, "observe", ["observed", "observe", "observes", "observing"], "R5 + forms"),
    (0, "the rate was", ["the rate was"], "R5"),
    (0, "we report", ["we report", "we reported"], "R5 + forms"),
    (0, "realizar", ["se realizó", "se realizaron", "realizamos"], 'ES of "performed"'),
    (0, "observar", ["se observó", "se observaron", "observamos"], 'ES of "observed"'),
    (0, "la tasa fue", ["la tasa fue"], 'ES of "the rate was"'),
    (0, "reportamos", ["reportamos"], 'ES of "we report"'),
    # ---- L1 associate ----
    (1, "associated with", ["associated with"], "R5"),
    (1, "correlated", ["correlated", "correlates", "correlate", "correlating"], "R5 + forms"),
    (1, "linked to", ["linked to"], "R5"),
    (1, "asociado con", ["asociado con", "asociada con", "asociados con", "asociadas con",
                         "asociado a", "asociada a", "se asoció con", "se asociaron con"],
     'ES of "associated with"'),
    (1, "correlacionado", ["correlacionado con", "correlacionada con", "se correlacionó con",
                           "correlación con"], 'ES of "correlated"'),
    (1, "vinculado a", ["vinculado a", "vinculada a", "vinculados a", "vinculadas a"],
     'ES of "linked to"'),
    # ---- L2 predict ----
    (2, "predict", ["predicts", "predict", "predicted", "predicting"], "R5 + forms"),
    (2, "risk factor for", ["risk factor for"], "R5"),
    (2, "identifies patients who", ["identifies patients who"], "R5"),
    (2, "predecir", ["predice", "predicen", "predijo", "predijeron"], 'ES of "predicts"'),
    (2, "factor de riesgo", ["factor de riesgo para", "factor de riesgo de"],
     'ES of "risk factor for"'),
    (2, "identifica pacientes que", ["identifica pacientes que", "identifica a los pacientes que"],
     'ES of "identifies patients who"'),
    # ---- L3 cause ----
    (3, "reduce", ["reduces", "reduce", "reduced", "reducing"], "R5 + forms"),
    (3, "improve", ["improves", "improve", "improved", "improving"], "R5 + forms"),
    (3, "superior to", ["superior to"], "R5"),
    (3, "safe", ["safe"], "R5"),
    (3, "effective", ["effective"], "R5"),
    (3, "enable", ["enables", "enable", "enabled", "enabling"], "R5 + forms"),
    (3, "reducir", ["reduce", "reducen", "redujo", "redujeron"], 'ES of "reduces"'),
    (3, "mejorar", ["mejora", "mejoran", "mejoró", "mejoraron"], 'ES of "improves"'),
    (3, "superior a", ["superior a", "superiores a"], 'ES of "superior to"'),
    (3, "seguro", ["seguro", "segura", "seguros", "seguras"], 'ES of "safe"'),
    (3, "eficaz", ["eficaz", "eficaces", "efectivo", "efectiva", "efectivos", "efectivas"],
     'ES of "effective"'),
    (3, "permitir", ["permite", "permiten", "permitió", "permitieron"], 'ES of "enables"'),
]

# The features R5's design table is keyed on. Each is a literal word list, so
# STEP 1 reads as five yes/no questions a human answers off the printed evidence.
DESIGN_FEATURES = [
    ("rct", "RCT", [
        "randomized controlled trial", "randomised controlled trial", "RCT",
        "randomized", "randomised", "randomly assigned", "randomly allocated",
        "ensayo clínico aleatorizado", "ensayo aleatorizado",
        "aleatorizado", "aleatorizada", "aleatorizados", "aleatorizadas",
        # NOT "ECA" (ensayo clínico aleatorizado): in this corpus ECA is
        # extracorporeal anastomosis (nomenclatura.md), the exact variable half
        # these abstracts compare. The collision would fire RCT on every ECA arm.
    ]),
    ("retrospective", "retrospective", [
        "retrospective", "retrospectively", "retrospectivo", "retrospectiva",
        "retrospectivamente",
    ]),
    ("prospective", "prospective", [
        "prospective", "prospectively", "prospectivo", "prospectiva",
        "prospectivamente",
    ]),
    ("comparative", "comparative", [
        "comparative", "comparativo", "comparativa", "two-arm", "two arm",
        "dos brazos",
        # NOT "versus" / "vs": R2 — "I never assume a control group exists
        # because the prose implies a comparison."
    ]),
    ("control", "control group", [
        "control group", "control arm", "control cohort", "comparison group",
        "comparison arm", "grupo control", "grupo de control", "grupo comparativo",
        "grupo de comparación", "cohorte control", "brazo control",
    ]),
    ("no_control", "no control (stated)", [
        "case series", "serie de casos", "single-arm", "single arm",
        "un solo brazo", "no control group", "without a control group",
        "no comparison group", "sin grupo control", "sin grupo de control",
        "sin grupo comparativo", "uncontrolled",
    ]),
    ("adjusted", "adjusted", [
        "adjusted for", "multivariable", "multivariate", "propensity score",
        "propensity-matched", "propensity matched", "ajustado por", "ajustada por",
        "análisis multivariable", "análisis multivariado", "puntaje de propensión",
        "regresión logística multivariable",
    ]),
    ("prediction_aim", "prediction aim", [
        "aim was to predict", "aim of this study was to predict",
        "objective was to predict", "predictive model", "prediction model",
        "objetivo fue predecir", "objetivo de este estudio fue predecir",
        "modelo predictivo", "modelo de predicción",
    ]),
    ("validated", "validated", [
        "validation cohort", "internal validation", "external validation",
        "internally validated", "externally validated", "cross-validation",
        "cohorte de validación", "validación interna", "validación externa",
        "validación cruzada",
    ]),
]

# Structured-abstract headers, for the location half of R3. EN set from
# congress-rules.md §Abstract length and shape names five (Background/Purpose,
# Methods, Results, Conclusions, Keywords); the rest are this build's additions.
# ES register per R1.
SECTION_HEADERS = [
    "Background/Purpose", "Background", "Purpose", "Objective", "Aim",
    "Materials and Methods", "Methods", "Results", "Conclusions", "Conclusion",
    "Keywords",
    "Material y métodos", "Materiales y métodos", "Métodos", "Antecedentes",
    "Introducción", "Objetivo", "Resultados", "Conclusiones", "Conclusión",
    "Palabras clave",
]

# Where an abstract asserts its own finding. A verb in Background states the
# literature's prior — "ICA may reduce complications, but data in our population
# is limited" is the reason the study was done, not its claim — and reading it as
# the author's assertion fires on the rationale of very nearly every abstract
# written. R0 computes "the claim", and Lazarus 2015, this build's primary
# anchor, measures spin in abstract *conclusions*: "Abstract conclusions of 61
# (48%) articles featured a high level of spin" (claim-ladder.md).
# Hits outside these sections are printed as context, never dropped: R3 keeps
# every span, and the verdict names which ones it read.
CLAIM_SECTIONS = {
    "Results", "Conclusions", "Conclusion",
    "Resultados", "Conclusiones", "Conclusión",
}

_SECTION_RE = re.compile(
    r"^[\s#*_>-]*(" + "|".join(re.escape(h) for h in SECTION_HEADERS) + r")[\s*_]*(?::|\.|—|–|$)",
    re.IGNORECASE | re.UNICODE,
)

_COMPILED = {}


def _forms_rx(forms):
    key = tuple(forms)
    if key not in _COMPILED:
        _COMPILED[key] = [(f, _rx(f)) for f in forms]
    return _COMPILED[key]


# --------------------------------------------------------------------------
# R2's polarity, R2's intake item (3)
# --------------------------------------------------------------------------
#
# Two mechanisms live here, and both exist because a substring list cannot tell
# the difference between an abstract that HAS a control group and one that says
# it HASN'T. R2 turns on that difference twice over: item (3) resolves to
# "stated: absent — silence, uncontradicted", and "I never assume a control
# group exists because the prose implies a comparison."

# A control phrase sitting inside a negation states the control's ABSENCE. The
# window is four words and stops at the clause boundary, which is what a reader
# scanning backwards from the phrase does: "no hubo grupo control" negates,
# "Sin ajuste por confundidores, el grupo control recibió" does not. A list of
# negated surface forms was the other option and it is the one that produced the
# bug — every form it omits reads as presence, in the direction of the stronger
# design, which is R2 backwards.
NEGATORS = {
    "no", "sin", "ningun", "ningún", "ninguna", "ninguno", "nunca", "tampoco",
    "not", "without", "never", "neither", "nor", "lacked", "lacking",
    "absent", "absence",
}
_NEG_WINDOW = 4
# A paragraph break ends a clause; a line wrap does not. A pasted abstract wraps
# wherever the source did, and "Results were not\nadjusted for confounders" is
# one clause split by a newline — the same reason _rx() spaces loosely.
_CLAUSE_END_RE = re.compile(r"[.;:!?]|\n\s*\n")
_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)

# Two arms, each carrying its own n. R2 item (3) asks for a "control or
# comparison group"; an abstract that names two groups and gives each an n has
# declared one, whatever it calls it. A bare "4.1 vs 6.3" has not — that is the
# prose implying a comparison, which R2 refuses to read as a group.
_N_DECL_RE = re.compile(r"(?<!\w)n\s*=\s*\d+", re.IGNORECASE)
_VERSUS_RE = re.compile(r"(?<!\w)(?:versus|vs\.?)(?!\w)", re.IGNORECASE)


def _negated(text, offset):
    """True if the four words before `offset`, in the same clause, carry a negator."""
    head = text[:offset]
    bound = 0
    for m in _CLAUSE_END_RE.finditer(head):
        bound = m.end()
    words = _WORD_RE.findall(head[bound:])
    return any(w.lower() in NEGATORS for w in words[-_NEG_WINDOW:])


def _rx_hits(doc, rx):
    hits = []
    for m in rx.finditer(doc.text):
        line, section = doc.locate(m.start())
        hits.append({
            "span": " ".join(m.group(0).split()),
            "form": m.group(0),
            "line": line,
            "section": section,
            "offset": m.start(),
        })
    return hits


# --------------------------------------------------------------------------
# Locating a span (R3: verbatim span + its location)
# --------------------------------------------------------------------------


class Doc:
    def __init__(self, text):
        self.text = text
        self.line_starts = [0]
        for m in re.finditer(r"\n", text):
            self.line_starts.append(m.end())
        self.sections = []  # (line_index, header)
        for i, line in enumerate(text.split("\n")):
            m = _SECTION_RE.match(line)
            if m:
                self.sections.append((i, m.group(1)))

    def locate(self, offset):
        li = bisect_right(self.line_starts, offset) - 1
        section = "—"
        for start_line, header in self.sections:
            if start_line <= li:
                section = header
            else:
                break
        return li + 1, section

    def find(self, forms):
        """Every match of any form: (verbatim span, line, section). R3 evidence."""
        hits = []
        for form, rx in _forms_rx(forms):
            for m in rx.finditer(self.text):
                line, section = self.locate(m.start())
                hits.append({
                    "span": " ".join(m.group(0).split()),
                    "form": form,
                    "line": line,
                    "section": section,
                    "offset": m.start(),
                })
        hits.sort(key=lambda h: h["offset"])
        return hits


# --------------------------------------------------------------------------
# STEP 1 — the declared design (R2)
# --------------------------------------------------------------------------


def step1_design(doc):
    ev = {}
    for fid, _label, forms in DESIGN_FEATURES:
        ev[fid] = doc.find(forms)

    # Polarity, before anything is counted, on every feature whose presence
    # raises the ceiling. Those are the ones where a missed negation costs
    # something: it reads the STRONGER design out of the sentence that denies
    # it, which is R2 exactly backwards. "No adjustment for confounders was
    # performed" must not make a study adjusted, and "no hubo grupo control"
    # must not make it controlled.
    neg = []
    for fid in ("rct", "control", "adjusted", "prediction_aim", "validated"):
        hits = ev[fid]
        negated = [h for h in hits if _negated(doc.text, h["offset"])]
        if negated:
            off = {h["offset"] for h in negated}
            ev[fid] = [h for h in hits if h["offset"] not in off]
            neg += [dict(h, feature=fid) for h in negated]
            # Only the control has a meaningful opposite: a denied control is a
            # stated absence, with a span to quote for it. A denied adjustment
            # is just the default state and needs no bucket of its own.
            if fid == "control":
                ev["no_control"] = sorted(ev["no_control"] + negated, key=lambda h: h["offset"])

    arms = _rx_hits(doc, _N_DECL_RE)
    versus = _rx_hits(doc, _VERSUS_RE)

    present = {fid: bool(hits) for fid, hits in ev.items()}

    # R2 — the design has to be declared. Anything that names one of the axes
    # R5's table is keyed on counts as a declaration; nothing does not.
    declared = any(present[f] for f in
                   ("rct", "retrospective", "prospective", "comparative", "control", "no_control"))

    # R2 intake item (3), resolved to one of three states. The operative
    # definition of each is published in rules.md R2 — Track A applies it by
    # hand off the printed evidence below, and the two tracks converge because
    # the definition is the same text, not this file's private lexicon.
    #
    #   absent    the abstract says there is no control, or says nothing about
    #             groups at all and nothing in the prose contradicts that
    #   present   an arm is named, or two arms each carry their own n, or the
    #             study is randomised (the control is what randomisation
    #             randomises to)
    #   unstated  the prose compares and no group is named either way — the
    #             item is MISSING, not stated, and there is no ceiling to read
    #
    # The third state is the fix for R2's own contradiction. The reading that
    # took any silence as a stated absence, and "I never assume a control group
    # exists because the prose implies a comparison", cannot both hold over an abstract that compares
    # without naming a group: one reads it as single-arm, the other refuses to
    # read it as comparative. Taking silence for a declaration resolved that by
    # picking a design the author never wrote — invisibly, and toward the
    # stronger claim, which is the failure this editor exists to catch.
    compares = present["comparative"] or bool(versus) or len(arms) >= 2

    if present["no_control"]:
        intake3, why3 = "absent", "stated: the abstract declares there is no control group"
    elif present["control"]:
        intake3, why3 = "present", "stated: a control or comparison arm is named"
    elif len(arms) >= 2:
        intake3, why3 = "present", "stated: two arms, each declaring its own n"
    elif present["rct"]:
        intake3, why3 = "present", "stated: randomised — the control is what randomisation assigns to"
    elif compares:
        intake3, why3 = "unstated", "MISSING: the prose compares, but no group is named and no absence is declared"
    else:
        intake3, why3 = "absent", "stated by silence: nothing about groups, and nothing that compares"

    return {
        "evidence": ev,
        "present": present,
        "declared": declared,
        "arms": arms,
        "versus": versus,
        "negated_control": neg,
        "intake3": intake3,
        "intake3_why": why3,
        # No declared design, no row to read — R2's gate fires before any of this.
        "no_control_effective": declared and intake3 == "absent",
        "inferred_no_control": declared and intake3 == "absent" and not present["no_control"],
    }


# --------------------------------------------------------------------------
# STEP 2 — the ceiling, off R5's design table (R5)
# --------------------------------------------------------------------------


def step2_ceiling(d):
    """R5's design→ceiling table, transcribed. Returns every row the features
    satisfy; the caller takes the lowest (R2: in doubt, the weaker design)."""
    p = dict(d["present"])
    # The table's "control" column is R2 intake item (3), resolved — not the
    # literal phrase. A row that keys on the phrase reads a two-arm study with
    # no magic words as single-arm, which is how a design nobody declared got a
    # ceiling anyway. STEP 1 resolves the item; STEP 2 reads the resolution.
    p["control"] = d["intake3"] == "present"
    rows = []

    if d["no_control_effective"]:
        rows.append(("Case series / single-arm, no control", 0, None))

    if p["retrospective"] and p["control"] and not p["adjusted"]:
        rows.append(("Retrospective comparative, control, unadjusted", 1, None))

    if (p["retrospective"] or p["prospective"]) and p["control"] and p["adjusted"]:
        if p["prediction_aim"] and p["validated"]:
            note = "L2 — the stated aim is prediction and it is validated"
            rows.append(("Retrospective/prospective comparative, adjusted for confounders", 2, note))
        else:
            note = "L1 — the L2 branch needs a stated prediction aim AND validation; " \
                   "in doubt the weaker (R2)"
            rows.append(("Retrospective/prospective comparative, adjusted for confounders", 1, note))

    if p["rct"]:
        rows.append(("RCT", 3, None))

    return rows


# --------------------------------------------------------------------------
# STEP 3 — the claim lexicon (R5, R1)
# --------------------------------------------------------------------------


def step3_claims(doc):
    # One span, one entry. A surface form can belong to two lemmas at once —
    # "reduce" is both R5's English verb and the Spanish third person of
    # "reducir" — and printing the same quoted span twice would read as two
    # findings where there is one. Same rung either way, which is R1's point,
    # so the merged entry names both registers.
    by_offset = {}
    for rung, lemma, forms, provenance in CLAIM_LEXICON:
        for hit in doc.find(forms):
            key = (hit["offset"], hit["span"].lower())
            if key in by_offset:
                prev = by_offset[key]
                if prev["rung"] != rung:  # not reachable today; loud if the lexicon drifts
                    raise AssertionError(
                        'lexicon conflict: "%s" is both %s and %s'
                        % (hit["span"], RUNG_NAME[prev["rung"]], RUNG_NAME[rung]))
                prev["lemma"] += " / " + lemma
                prev["provenance"] += " / " + provenance
            else:
                by_offset[key] = dict(hit, rung=rung, lemma=lemma, provenance=provenance)
    found = list(by_offset.values())
    found.sort(key=lambda h: (-h["rung"], h["offset"]))
    return found


# --------------------------------------------------------------------------
# STEPS 4-5 — compare, verdict
# --------------------------------------------------------------------------


def check(text):
    doc = Doc(text)
    d = step1_design(doc)
    rows = step2_ceiling(d)
    claims = step3_claims(doc)

    ceiling = min((r[1] for r in rows), default=None)

    # The verdict reads the sections where the abstract asserts its own finding.
    # If it has none of them — an unstructured paragraph, a conclusion pasted on
    # its own — every hit counts, because there is no structure to read past.
    asserted = [c for c in claims if c["section"] in CLAIM_SECTIONS]
    context_only = [c for c in claims if c["section"] not in CLAIM_SECTIONS]
    if not asserted:
        asserted, context_only = claims, []

    highest = asserted[0]["rung"] if asserted else None
    # Every span at the top rung ships: they are the evidence for the one finding
    # R0.1 step 3 asks for, and picking among them would be choosing, not computing.
    top_spans = [c for c in asserted if c["rung"] == highest] if asserted else []

    # "code" is the branch; "verdict" is what gets printed. The two REFUSE branches
    # say very different things — one tells the author their abstract never declared
    # a design, the other tells the maintainer R5's table has a hole — so the code
    # keeps them apart where the verdict string alone would blur them.
    if not d["declared"]:
        code, verdict, reason = "REFUSE_NO_DESIGN", "REFUSE", (
            "R2: no declared design, no claim verdict. I don't guess it. "
            "Structural findings stay in scope (R2, R3).")
    elif d["intake3"] == "unstated":
        code, verdict, reason = "REFUSE_INTAKE_CONTROL_UNSTATED", "REFUSE", (
            "R2 item (3) — control or comparison group — is neither stated nor "
            "stated-absent. This abstract compares, and names no group either "
            "way. R2 forbids reading a control out of prose that implies a "
            "comparison, and reading silence as a stated absence would assume "
            "the design instead: single-arm, ceiling L0, on a study that may "
            "well be comparative. So there is no ceiling to read and no claim "
            "verdict. Declare any one of these and the verdict follows: the "
            "comparison arm and its n · that there was no control group · that "
            "the design is single-arm or a case series.")
    elif not rows:
        fired = sorted(f for f, v in d["present"].items() if v)
        code, verdict, reason = "REFUSE_CONTRACT_GAP", "REFUSE", (
            "CONTRACT-GAP — the declared features {%s} match no row of R5's design "
            "table, so there is no ceiling to read. rules.md wins: the table needs a "
            "row before this design gets a verdict. Not resolved here." % ", ".join(fired))
    elif highest is None:
        code, verdict, reason = "CLEAN_NO_SPAN", "CLEAN", (
            "R3: no quotable span in the claim lexicon, no finding.")
    elif highest > ceiling:
        code, verdict, reason = "BLOCK", "BLOCK", (
            "R5: the claim asserts %s; the declared design carries %s. "
            "rung(verb) > ceiling(design) blocks — it does not warn."
            % (RUNG_NAME[highest], RUNG_NAME[ceiling]))
    else:
        code, verdict, reason = "CLEAN_AT_OR_BELOW", "CLEAN", (
            "R5: the highest rung asserted is %s; the declared design carries %s."
            % (RUNG_NAME[highest], RUNG_NAME[ceiling]))

    return {
        "design": d, "rows": rows, "ceiling": ceiling,
        "claims": claims, "asserted": asserted, "context_only": context_only,
        "highest": highest, "top_spans": top_spans,
        "code": code, "verdict": verdict, "reason": reason,
    }


# --------------------------------------------------------------------------
# Report — the hand procedure, printed
# --------------------------------------------------------------------------

R7_RANKS = {
    1: "claim over design (L-violation) — invisible: survives review, gets cited, "
       "can't be walked back",
}


def report(res, source):
    d, out = res["design"], []
    w = out.append
    w("check.py — claim verdict (R0.1 Track B)")
    w("source: %s" % source)
    w('lexicon: ES+EN (R1 — "the claim ladder resolves to the same rung in either '
      'language: the design doesn\'t change with the words")')
    w("")

    w("STEP 1 — the declared design (R2)")
    for fid, label, _forms in DESIGN_FEATURES:
        hits = d["evidence"][fid]
        if hits:
            h = hits[0]
            w('  %-22s YES   "%s"   line %d (%s)' % (label, h["span"], h["line"], h["section"]))
            for extra in hits[1:3]:
                w('  %-22s       "%s"   line %d (%s)'
                  % ("", extra["span"], extra["line"], extra["section"]))
        else:
            w("  %-22s no" % label)
    if d["arms"]:
        w('  %-22s %s   %s' % ("n declared", "x%d" % len(d["arms"]),
                               ", ".join('"%s" (line %d)' % (h["span"], h["line"]) for h in d["arms"][:4])))
    if d["versus"]:
        h = d["versus"][0]
        w('  %-22s YES   "%s"   line %d (%s)' % ("compares (vs)", h["span"], h["line"], h["section"]))
    w("")
    if d["negated_control"]:
        h = d["negated_control"][0]
        w('  polarity: "%s" (line %d) sits under a negation -> it states the control is'
          % (h["span"], h["line"]))
        w("  ABSENT, not present. R2 — the weaker design, never the stronger.")
    w("  R2 item (3), control or comparison group: %s" % d["intake3"].upper())
    w("    %s" % d["intake3_why"])
    if d["intake3"] == "absent" and not d["present"]["no_control"]:
        w('    R2 — "stated: absent — silence, uncontradicted"')
        w('    R2 — "In doubt, assume the weaker design, never the stronger"')
    if d["intake3"] == "unstated":
        w('    R2 — "I never assume a control group exists because the prose implies a')
        w('         comparison" — so vs / versus / n-vs-n does not make a control, and')
        w("         silence next to comparing prose is a missing item, not a declaration")
    w("")
    w("  design declared: %s" % ("YES" if d["declared"] else "NO"))
    w("")

    w("STEP 2 — the ceiling, read off R5's design table")
    if res["rows"]:
        for label, ceil, note in res["rows"]:
            w("  %-64s %s" % (label, RUNG_NAME[ceil]))
            if note:
                w("      %s" % note)
        w("  ceiling = %s   (lowest matched row — R2: in doubt, the weaker design)"
          % RUNG_NAME[res["ceiling"]])
    else:
        w("  rows matched: none")
    w("")

    w("STEP 3 — the claim lexicon, highest rung asserted (R5)")
    if res["context_only"]:
        n_ctx = len(res["context_only"])
        w("  read: %s. %d hit%s outside them %s the prior, not the claim, and %s"
          % ("/".join(sorted(CLAIM_SECTIONS & {c["section"] for c in res["claims"]})) or "the whole text",
             n_ctx, "" if n_ctx == 1 else "s",
             "states" if n_ctx == 1 else "state", "is" if n_ctx == 1 else "are"))
        w("  not the verdict: %s"
          % ", ".join('%s "%s" (%s)' % (RUNG_NAME[c["rung"]][:2], c["span"], c["section"])
                      for c in res["context_only"][:4]))
    if res["asserted"]:
        for c in res["top_spans"]:
            w('  %-12s "%s"   line %d (%s)' % (RUNG_NAME[c["rung"]], c["span"], c["line"], c["section"]))
            w("               lemma: %s | provenance: %s" % (c["lemma"], c["provenance"]))
        lower = [c for c in res["asserted"] if c["rung"] != res["highest"]]
        if lower:
            w("  (%d lower-rung hit%s, not the verdict: %s)"
              % (len(lower), "" if len(lower) == 1 else "s",
                 ", ".join(sorted({'%s "%s"' % (RUNG_NAME[c["rung"]][:2], c["span"]) for c in lower}))))
        w("  highest rung asserted = %s" % RUNG_NAME[res["highest"]])
    else:
        w("  no lexicon hit")
    w("")

    w("STEP 4 — compare")
    if res["ceiling"] is None or res["highest"] is None:
        w("  not reached — %s" % ("no ceiling" if res["ceiling"] is None else "no rung asserted"))
    else:
        w("  rung(%s) > ceiling(%s)  ->  %s"
          % (RUNG_NAME[res["highest"]], RUNG_NAME[res["ceiling"]],
             "TRUE" if res["highest"] > res["ceiling"] else "FALSE"))
    w("")

    w("STEP 5 — verdict")
    w("  %s" % res["verdict"])
    for line in _wrap(res["reason"], 74):
        w("  %s" % line)
    if res["verdict"] == "BLOCK":
        w("  R7 rank 1 of 4 — %s" % R7_RANKS[1])
        w("  (rank computed, not chosen: an L-violation is R7's tier 1 by definition.")
        w("   R7 tiers 2-4 — numbers that don't reconcile, missing structure, everything")
        w("   else — are outside what this script computes.)")
    w("")
    w("  Rules: %s" % ", ".join(_fired(res)))
    return "\n".join(out)


def _fired(res):
    ids = ["R0.1", "R2"]
    if res["verdict"] == "BLOCK":
        ids += ["R3", "R5", "R7"]
    elif res["verdict"] == "CLEAN":
        ids += ["R3", "R5"]
    else:
        ids += ["R3", "R9"]
    return ids


def _wrap(s, width):
    words, lines, cur = s.split(), [], ""
    for word in words:
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------
# Self-test (R0.1: "Auditing me")
# --------------------------------------------------------------------------
#
# Every abstract below is SYNTHETIC — invented for this test, no patient data, no
# real study, no real number. They exist to pin a verdict, not to be true.
#
# What these pin: R5's table rows, R2's three states for intake item (3), the
# ES/EN pair R1 promises resolves identically, and the polarity of the two
# features that lift a ceiling. What they do NOT pin is examples.md — those come
# from running the editor, not this script, and rules.md R0.1 says so.

CASES = [
    (
        "block_es_superior_on_unadjusted_comparative",
        "ES · retrospective + control group, unadjusted -> L1. Conclusión says "
        '"superior a" -> L3. Climbs one rung past its ceiling.',
        """Título: Anastomosis intracorpórea versus extracorpórea en hemicolectomía derecha.
Métodos: Estudio retrospectivo comparativo en un centro. Se incluyeron 120 pacientes;
el grupo control recibió anastomosis extracorpórea. No se realizó ajuste por confundidores.
Resultados: La tasa fue del 4% en el grupo ICA.
Conclusiones: La anastomosis intracorpórea es superior a la extracorpórea.""",
        "BLOCK", 3, 1,
    ),
    (
        "block_en_superior_on_unadjusted_comparative",
        'EN mirror of the case above. "superior" resolves to the same rung in either '
        "language — R1: the design doesn't change with the words.",
        """Title: Intracorporeal versus extracorporeal anastomosis in right hemicolectomy.
Methods: Retrospective comparative single-centre study. 120 patients; the control group
received an extracorporeal anastomosis. No adjustment for confounders was made.
Results: The rate was 4% in the ICA group.
Conclusions: Intracorporeal anastomosis is superior to extracorporeal anastomosis.""",
        "BLOCK", 3, 1,
    ),
    (
        "block_case_series_reduced",
        'Case series, no control -> L0. "reduced" is L3. The widest gap the ladder has.',
        """Title: Transanal TME in a single unit.
Methods: Retrospective case series of 18 consecutive patients. No control group.
Results: Median length of stay was 5 days.
Conclusions: TaTME reduced length of stay in our unit.""",
        "BLOCK", 3, 0,
    ),
    (
        "block_l2_verb_on_adjusted_l1_ceiling",
        "Adjusted comparative with no prediction aim -> L1. \"predicts\" is L2. One "
        "rung, and it is the rung nobody notices.",
        """Title: Anastomotic leak after low anterior resection.
Methods: Retrospective comparative cohort with a control group, adjusted for
confounders by multivariable logistic regression.
Results: Leak occurred in 22 of 300 patients.
Conclusions: Operative time predicts anastomotic leak.""",
        "BLOCK", 2, 1,
    ),
    (
        "block_r2_weaker_of_two_designs",
        'Abstract names both "comparative" and "single-arm". R2: in doubt assume the '
        "weaker -> L0, not L1. An L1 verb then blocks.",
        """Title: ICA in right hemicolectomy.
Methods: Retrospective comparative review of a single-arm cohort with a control group.
Results: 60 patients.
Conclusions: Intracorporeal anastomosis was associated with shorter length of stay.""",
        "BLOCK", 1, 0,
    ),
    (
        "clean_rct_superior",
        "RCT -> L3 ceiling. An L3 verb sits exactly at it. 3 > 3 is false: the ladder "
        "blocks climbing, not arriving.",
        """Title: ICA versus ECA: a randomized controlled trial.
Methods: Multicentre randomized controlled trial with a control group. 400 patients
randomly assigned.
Results: The rate was 3% versus 7%.
Conclusions: Intracorporeal anastomosis is superior to extracorporeal anastomosis.""",
        "CLEAN_AT_OR_BELOW", 3, 3,
    ),
    (
        "clean_case_series_stays_at_l0",
        "Case series -> L0, and the prose never climbs off L0. The design and the verb "
        "agree; nothing to say.",
        """Title: Serie de casos de TaTME.
Métodos: Serie de casos retrospectiva de 12 pacientes. Sin grupo control.
Resultados: La tasa fue del 8%.
Conclusiones: Reportamos nuestra experiencia inicial. Se observó una estadía media de 6 días.""",
        "CLEAN_AT_OR_BELOW", 0, 0,
    ),
    (
        "clean_no_lexicon_hit_at_all",
        "R3 floor: the conclusion is vague but no lexicon verb appears. No span to "
        "quote -> no finding -> clean. The script may not flag what it cannot quote.",
        """Title: ICA in right hemicolectomy.
Methods: Retrospective comparative study with a control group.
Results: 90 patients.
Conclusions: Our findings merit further study.""",
        "CLEAN_NO_SPAN", None, 1,
    ),
    (
        "clean_adjusted_l1_verb_at_ceiling",
        'Adjusted comparative -> L1. "was associated with" is L1. Sits at the ceiling.',
        """Title: Leak after LAR.
Methods: Prospective comparative cohort with a control group, adjusted for confounders
using a propensity score.
Results: 250 patients.
Conclusions: Diverting ileostomy was associated with a lower leak rate.""",
        "CLEAN_AT_OR_BELOW", 1, 1,
    ),
    (
        "clean_l2_upgrade_prediction_aim_plus_validation",
        "R5's L2 branch: adjusted comparative + stated prediction aim + validated -> "
        'ceiling L2. "predicts" then sits at it.',
        """Title: A prediction model for anastomotic leak.
Methods: Retrospective comparative cohort with a control group, adjusted for
confounders. The objective was to predict anastomotic leak; the prediction model was
assessed in an external validation cohort.
Results: 800 patients.
Conclusions: The score predicts anastomotic leak.""",
        "CLEAN_AT_OR_BELOW", 2, 2,
    ),
    (
        "es_no_control_under_negation",
        "R1's minimal pair, Spanish half. The abstract declares it had no control. "
        '"grupo control" is in there, inside the negation that denies it — polarity, '
        "not a list of denied phrasings, is what reads it as an absence.",
        """Título: AIC en hemicolectomía derecha.
Métodos: Revisamos retrospectivamente 54 pacientes. No hubo grupo control.
Resultados: La tasa fue del 5.6%.
Conclusiones: La AIC es segura y eficaz.""",
        "BLOCK", 3, 0,
    ),
    (
        "en_no_control_under_negation",
        "The English half of the same pair. Same design, same declaration, same "
        "ceiling. If these two ever disagree, R1 is false and the banner this "
        "script prints on every run is false with it.",
        """Title: ICA in right hemicolectomy.
Methods: We retrospectively reviewed 54 patients. There was no control group.
Results: The rate was 5.6%.
Conclusions: ICA is safe and effective.""",
        "BLOCK", 3, 0,
    ),
    (
        "two_arms_with_n_state_the_comparison",
        "R2 item (3) asks for a control OR COMPARISON group. Two arms, each with its "
        "own n, is one — whatever the abstract calls it. The phrase "
        '"control group" never appears here.',
        """Title: ICA in right hemicolectomy.
Methods: Retrospective review of patients divided by anastomotic technique:
intracorporeal (n=31) and extracorporeal (n=48). No adjustment for confounders was performed.
Results: The leak rate was 3.2% and 8.3%.
Conclusions: Intracorporeal anastomosis was associated with a lower leak rate.""",
        "CLEAN_AT_OR_BELOW", 1, 1,
    ),
    (
        "refuse_intake_control_unstated",
        "The prose compares and names no group either way. R2 forbids reading a "
        "control out of it, and reading the silence as a stated absence would assume "
        "the design instead. The item is missing, so there is no ceiling — and the "
        "refusal names what to declare.",
        """Title: ICA versus ECA in right hemicolectomy.
Methods: We retrospectively reviewed 79 patients operated at our centre.
Results: The leak rate was 3.2% versus 8.3%.
Conclusions: Intracorporeal anastomosis is superior to extracorporeal anastomosis.""",
        "REFUSE_INTAKE_CONTROL_UNSTATED", 3, None,
    ),
    (
        "background_states_the_prior_not_the_claim",
        '"may reduce" is L3 and it is the literature\'s reason for doing the study, '
        "not this study's claim. Reading it as the author's assertion blocks the "
        "rationale of nearly every abstract ever written.",
        """Title: ICA in right hemicolectomy.
Background: ICA may reduce complications, but data in our population is limited.
Methods: Retrospective comparative cohort with a control group. No adjustment for
confounders was performed.
Results: 79 patients.
Conclusions: ICA was associated with a lower leak rate.""",
        "CLEAN_AT_OR_BELOW", 1, 1,
    ),
    (
        "negated_adjustment_does_not_open_the_l2_branch",
        "Polarity again, on the other feature that lifts a ceiling. Read as adjusted, "
        "this study clears R5's L2 branch and its L2 verb sits clean. It said it was "
        "not adjusted.",
        """Title: A prediction model for anastomotic leak.
Methods: Retrospective comparative cohort with a control group. The objective was to
predict anastomotic leak, assessed in an external validation cohort. Results were not
adjusted for confounders.
Results: 800 patients.
Conclusions: The score predicts anastomotic leak.""",
        "BLOCK", 2, 1,
    ),
    (
        "refuse_no_declared_design",
        "R2's intake gate. An L3 verb is right there, and the script still returns no "
        "claim verdict: no declared design, and it does not guess one.",
        """Title: ICA in right hemicolectomy.
Methods: We reviewed 120 patients operated at our centre between 2020 and 2024.
Results: The rate was 4%.
Conclusions: Intracorporeal anastomosis is superior to extracorporeal anastomosis.""",
        "REFUSE_NO_DESIGN", 3, None,
    ),
    (
        "refuse_contract_gap_prospective_unadjusted",
        "The hole in R5's table, made visible instead of patched: prospective + control "
        "+ unadjusted matches no row. Row 2 is retrospective-only; row 3 needs "
        "adjustment. Refuses rather than resolving it.",
        """Title: ICA versus ECA.
Methods: Prospective comparative cohort with a control group. No adjustment for
confounders was performed.
Results: 100 patients.
Conclusions: Intracorporeal anastomosis is superior to extracorporeal anastomosis.""",
        "REFUSE_CONTRACT_GAP", 3, None,
    ),
]


def self_test():
    failures = 0
    print("check.py --self-test — %d cases. All abstracts are SYNTHETIC.\n" % len(CASES))
    for name, what, text, want_code, want_rung, want_ceiling in CASES:
        res = check(text)
        problems = []
        if res["code"] != want_code:
            problems.append("branch %s, wanted %s" % (res["code"], want_code))
        if res["highest"] != want_rung:
            problems.append("highest rung %s, wanted %s" % (res["highest"], want_rung))
        if res["ceiling"] != want_ceiling:
            problems.append("ceiling %s, wanted %s" % (res["ceiling"], want_ceiling))
        status = "FAIL" if problems else "pass"
        if problems:
            failures += 1
        print("%-5s %s" % (status, name))
        for line in _wrap(what, 68):
            print("      %s" % line)
        if problems:
            for p in problems:
                print("      -> %s" % p)
            print(_indent(report(res, "<self-test: %s>" % name), "      | "))
        print("")
    print("%d/%d pass" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


def _indent(s, prefix):
    return "\n".join(prefix + line for line in s.split("\n"))


# --------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--abstract", metavar="FILE", help="abstract to check")
    ap.add_argument("--self-test", action="store_true", help="run the embedded cases")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.abstract:
        ap.print_help()
        return 2

    with open(args.abstract, encoding="utf-8") as fh:
        text = fh.read()
    res = check(text)
    print(report(res, args.abstract))
    return {"CLEAN": 0, "BLOCK": 1, "REFUSE": 2}[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())

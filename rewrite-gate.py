#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rewrite-gate.py — R9: audit the editor's own output for a smuggled rewrite.

Contract: ./rules.md, same directory. On any divergence, rules.md wins and this
file is the bug.

This reads the EDITOR's output, not the abstract. R9's open rewrite ("just write
it for me") is visible and gets refused on sight. The one this catches is the
other one: obeying the letter while dictating the line anyway.

    R9 — "diagnosis and direction are mine; replacement text is yours."

      "Your conclusion claims causality your design can't carry"   diagnosis, legal
      "This needs to sit at L0"                                    direction, legal
      "Change it to 'was associated with'"                         a rewrite, banned

The tell is never the quotation mark. R3 obliges the editor to quote the author's
span in every single finding, so a gate that fires on quoted text fires on the
editor doing its job. The tell is the FRAME around the quote — whether the editor
is handing you words or handing you back your own.

Four classes, each answerable with a highlighter and no code:

    A  an offer of prose. Fires alone: these phrases exist only to supply words.
    B  a writing verb OPENING the clause + a quoted span in that clause. The
       imperative is the whole tell — "Say 'X'" is the editor writing your line,
       "Your Conclusions say 'X'" is the editor quoting it (R3). English spells
       both the same, so position carries what morphology doesn't.
    C  a two-word replacement frame + a quoted span in the clause. English
       collapses imperative and infinitive ("change"), so both halves of the
       frame must be present before it fires.
    D  an arrow between two quoted spans:  "X" -> "Y".

Usage:
    python3 rewrite-gate.py --output <file>    exit 0 clean · 1 violation
    python3 rewrite-gate.py --self-test        exit 0 all pass · 1 any fail

Python 3 stdlib only.
"""

import argparse
import re
import sys

# --------------------------------------------------------------------------
# Patterns — the list IS the spec. Each finding prints the class and the phrase
# that fired, so the reader can rerun the decision by eye.
# --------------------------------------------------------------------------

# Class A — fires on its own. Nothing in this list has a use except to hand the
# author words for the manuscript.
CLASS_A = [
    # EN
    "you could write", "you might write", "you can write",
    "you could say", "you might say", "you can say",
    "you could put", "you might put",
    "for example you could", "for example, you could", "for instance you could",
    "try writing", "try saying", "consider writing", "consider saying",
    "phrase it as", "word it as", "rephrase it as", "reword it as", "rewrite it as",
    "suggested wording", "suggested phrasing", "suggested text",
    "should read", "it should say", "should instead say",
    "would be better as", "better phrased as", "better worded as",
    # ES
    "podrías escribir", "podés escribir", "podrías decir", "podés decir",
    "podrías poner", "podés poner",
    "por ejemplo podrías", "por ejemplo escribí", "por ejemplo poné", "por ejemplo decí",
    "quedaría mejor como", "quedaría mejor así",
    "debería decir", "tendría que decir", "debería quedar",
    "reformulalo como", "reformulá como", "reescribilo como", "reescribilo así",
    "sugerencia de redacción", "redacción sugerida", "texto sugerido",
    "en su lugar escribí", "en su lugar poné", "en su lugar decí",
]

# Class B — must OPEN the clause, and the clause must carry a quoted span.
#
# The clause-initial test is what does the work: it is the difference between
# "Say 'X'" and "Your Conclusions say 'X'", and mutating it away is what breaks
# pass_r3_inline_citation_en.
#
# The list still excludes "use", "put", "phrase", "word", "change" and "replace",
# which are nouns or indicatives in ordinary editor prose ("the word 'superior' is
# L3"). Second layer, not the first: the clause-initial test already covers the
# cases in the self-test, since none of those words open a clause. "change" and
# "replace" reappear in Class C, where both halves of the frame are required.
# The ES imperatives are unambiguous by morphology alone — voseo "decí" never
# collides with indicative "dice" — and are held to the same clause-initial test
# anyway, because one rule beats two.
CLASS_B_VERBS = [
    # EN imperatives
    "say", "write", "rephrase", "reword", "rewrite", "swap",
    # ES voseo imperatives (R1: Rioplatense)
    "decí", "escribí", "poné", "usá", "cambiá", "cambialo", "cambiala",
    "reemplazá", "reemplazalo", "reemplazala", "sustituí", "sustituilo",
    "reformulá", "reformulalo", "reescribí", "reescribilo",
    # ES usted imperatives — no collision with any indicative form
    "diga", "escriba", "ponga", "cambie", "reemplace", "sustituya",
    "reformule", "reescriba",
]

# Class C — (opening word, closing word). Both halves in one clause, plus a quote.
CLASS_C_FRAMES = [
    (r"chang(?:e|es|ed|ing)", r"to"),
    (r"replac(?:e|es|ed|ing)", r"with"),
    (r"substitut(?:e|es|ed|ing)", r"(?:for|with)"),
    (r"swap(?:s|ped|ping)?", r"for"),
    (r"cambiar(?:lo|la|los|las)?", r"por"),
    (r"reemplazar(?:lo|la|los|las)?", r"por"),
    (r"sustituir(?:lo|la|los|las)?", r"por"),
]

# A quoted span. The single-quote arm is fenced with non-word lookarounds so an
# apostrophe pair ("can't ... don't") cannot masquerade as a quotation.
QUOTE_RE = re.compile(
    r'"[^"\n]{1,90}"'
    r"|“[^”\n]{1,90}”"
    r"|«[^»\n]{1,90}»"
    r"|(?<!\w)'[^'\n]{1,90}'(?!\w)"
    r"|(?<!\w)‘[^’\n]{1,90}’(?!\w)",
    re.UNICODE,
)

# Class D — "X" -> "Y", with any of the arrows that show up in prose.
ARROW_RE = re.compile(
    r"(" + QUOTE_RE.pattern + r")\s*(?:→|->|=>|⇒)\s*(" + QUOTE_RE.pattern + r")",
    re.UNICODE,
)

# A clause. Not a sentence: the comma matters, because "Por ejemplo, decí 'X'"
# puts the imperative after it. The colon is NOT a splitter — "Decí: 'X'" is the
# violation in its most naked form and must stay in one piece.
#
# ponytail: a clause stops at the newline, so classes B and C miss a violation
# that wraps between its verb and its quote ("Cambiá\n'X' por 'Y'"). It needs the
# wrap to land inside a one-word window, and the fix costs an offset map from
# joined text back to real line numbers. Build that if a real brief ever wraps
# there. Classes A and D scan the full text and are unaffected.
CLAUSE_RE = re.compile(r"[^.,;!?\n]+", re.UNICODE)

_LEADING_NOISE = re.compile(r"^[\s>*#•·\-–—_]+", re.UNICODE)

_COMPILED = {}


def _rx(phrase, anchored=False):
    key = (phrase, anchored)
    if key not in _COMPILED:
        body = r"\s+".join(re.escape(w) for w in phrase.split())
        prefix = r"^" if anchored else r"(?<!\w)"
        _COMPILED[key] = re.compile(prefix + body + r"(?!\w)", re.IGNORECASE | re.UNICODE)
    return _COMPILED[key]


_CLASS_C_RX = [
    (open_w, close_w,
     re.compile(r"(?<!\w)" + open_w + r"(?!\w)[^.,;!?\n]{0,60}?(?<!\w)" + close_w + r"(?!\w)",
                re.IGNORECASE | re.UNICODE))
    for open_w, close_w in CLASS_C_FRAMES
]


# --------------------------------------------------------------------------
# The scan
# --------------------------------------------------------------------------


def _line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def scan(text):
    """Every R9 violation in the editor's output, each with its span and class."""
    findings = []

    # Class A — fires wherever it appears; no clause test, no quote test.
    for phrase in CLASS_A:
        for m in _rx(phrase).finditer(text):
            findings.append({
                "cls": "A", "pattern": phrase, "offset": m.start(),
                "line": _line_of(text, m.start()),
                "why": "an offer of prose: this phrase exists only to hand the author words",
            })

    # Class D — an arrow between two quoted spans.
    for m in ARROW_RE.finditer(text):
        findings.append({
            "cls": "D", "pattern": '"X" -> "Y"', "offset": m.start(),
            "line": _line_of(text, m.start()),
            "why": "one quoted span arrowed into another: the shape of a replacement",
        })

    # Classes B and C — clause by clause.
    for cm in CLAUSE_RE.finditer(text):
        clause = cm.group(0)
        quotes = QUOTE_RE.findall(clause)
        if not quotes:
            continue  # R3's quoting is the editor's job; a bare quote is not a rewrite.

        head = _LEADING_NOISE.sub("", clause)
        for verb in CLASS_B_VERBS:
            if _rx(verb, anchored=True).match(head):
                findings.append({
                    "cls": "B", "pattern": "clause opens with %r + a quoted span" % verb,
                    "offset": cm.start(), "line": _line_of(text, cm.start()),
                    "why": "an imperative writing verb opening the clause: the editor is "
                           "supplying the line, not quoting it",
                })
                break

        for open_w, close_w, rx in _CLASS_C_RX:
            m = rx.search(clause)
            if m:
                findings.append({
                    "cls": "C",
                    "pattern": "%s ... %s + a quoted span" % (open_w, close_w),
                    "offset": cm.start(), "line": _line_of(text, cm.start()),
                    "why": "a replacement frame closed around quoted text",
                })
                break

    findings.sort(key=lambda f: (f["offset"], f["cls"]))
    for f in findings:
        f["clause"] = _clause_at(text, f["offset"])
    return findings


def _clause_at(text, offset):
    for cm in CLAUSE_RE.finditer(text):
        if cm.start() <= offset < cm.end():
            return " ".join(cm.group(0).split())
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    return " ".join(text[line_start: line_end if line_end != -1 else len(text)].split())


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------


def report(findings, source):
    out = []
    w = out.append
    w("rewrite-gate.py — R9 audit of the editor's own output")
    w("source: %s" % source)
    w("")
    if not findings:
        w("CLEAN — no replacement text found.")
        w("  R9: diagnosis and direction are mine; replacement text is yours.")
        w("  Quoted spans are not flagged: R3 obliges every finding to carry the")
        w("  author's verbatim span, and a citation is not a replacement.")
        w("")
        w("  Rules: R3, R9")
        return "\n".join(out)

    w("VIOLATION — %d smuggled rewrite%s. R9: this is my bug, not the author's."
      % (len(findings), "" if len(findings) == 1 else "s"))
    w("")
    for f in findings:
        w("  line %d · class %s" % (f["line"], f["cls"]))
        w('    "%s"' % f["clause"])
        w("    fired: %s" % f["pattern"])
        w("    why:   %s" % f["why"])
        w("")
    w("  R9 — no replacement text, no suggested phrasing, no example sentence in the")
    w("       register of the manuscript, however short.")
    w("  R4.4 — never produce a corrected version, in whole or in part.")
    w("")
    w("  Rules: R4.4, R9")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------
#
# Every line below is SYNTHETIC editor output, written for this test. The FAIL
# cases are deliberate R9 violations; the PASS cases are the editor doing exactly
# what R3, R4.3 and R9 require, and each one is a trap the gate must not spring.
# The PASS half is the half that matters: a gate that flags R3's mandatory
# quoting breaks the editor.

CASES = [
    # ---------------- must fire ----------------
    ("fail_es_cambia_x_por_y", True,
     "R9's named shape, in Spanish: the replacement handed over whole.",
     'Cambiá "utilizamos" por "usamos".'),
    ("fail_en_say_x_instead_of_y", True,
     'R9\'s "say X instead of Y". The imperative "Say" opens the clause.',
     'Say "was associated with" instead of "was superior to".'),
    ("fail_en_change_it_to", True,
     "The exact line R9 draws as uncrossable.",
     'Change it to "was associated with".'),
    ("fail_es_por_ejemplo_podrias_escribir", True,
     'R9\'s "for example you could write…", hedged into a suggestion and still a rewrite.',
     'Por ejemplo, podrías escribir: "se observó una tasa menor de fuga".'),
    ("fail_en_you_could_write", True,
     "Same move in English. The modal changes nothing: the words are still supplied.",
     'You could write "the leak rate was lower in the ICA group".'),
    ("fail_arrow_between_quotes", True,
     "No verb at all, just an arrow. Still hands over the line.",
     'Conclusiones: "fue superior a" → "se asoció con".'),
    ("fail_en_replace_with", True,
     "Two-word frame closed around quoted text.",
     'Replace "reduces length of stay" with "was associated with a shorter stay".'),
    ("fail_es_reformulalo_como", True,
     "Direction and replacement fused into one sentence; the replacement half still counts.",
     'Reformulalo como: "la tasa fue del 4%".'),
    ("fail_en_suggested_wording", True,
     "A heading instead of a verb. The manuscript register gives it away.",
     'Suggested wording: "we report a leak rate of 4%".'),
    ("fail_es_deci_colon_quote", True,
     "The naked form. The colon must not be read as a clause break, or this escapes.",
     'Decí: "se asoció con una estadía más corta".'),

    # ---------------- must NOT fire (R3/R4.3 doing its job) ----------------
    ("pass_r3_blockquote_citation", False,
     "R3's mandatory verbatim span. If this fires, the gate breaks the editor.",
     '> "la ICA fue superior a la ECA" (Conclusiones, línea 14)'),
    ("pass_r3_inline_citation_en", False,
     'The imperative trap: "Conclusions say" is indicative and identical to the '
     'imperative "Say". Position is what separates them.',
     'Your Conclusions say "superior to" — R5 puts that on L3; your design carries L1.'),
    ("pass_diagnosis_es_no_quote", False,
     "R9's own example of legal diagnosis.",
     "Tu conclusión afirma causalidad que tu diseño no banca (R5)."),
    ("pass_direction_l0", False,
     "R9's own example of legal direction.",
     "This needs to sit at L0."),
    ("pass_r4_3_names_the_failure", False,
     "R4.3's exact prescribed form: what makes the claim fail, quoting the verb.",
     'This design can\'t carry "superior".'),
    ("pass_decision_trace", False,
     "The Decision Trace every critique closes with (R8).",
     "Rules: R0, R3, R5, R7."),
    ("pass_two_quoted_spans_one_line", False,
     "Two spans quoted in one line looks like X -> Y and is not: no arrow, no frame.",
     'You wrote "fue superior a" (Conclusiones) and "se asoció con" (Resultados).'),
    ("pass_instead_of_in_diagnosis", False,
     '"instead of" inside a diagnosis. Why "instead" is not a trigger on its own.',
     "Your conclusion asserts causation instead of association."),
    ("pass_change_in_r1_diagnosis", False,
     'The R1 line itself: "change" and quoted spans in one clause, zero rewriting. '
     "Why Class C needs both halves of its frame.",
     'El diseño no cambia con el idioma: "superior" y "superior" caen en el mismo escalón.'),
    ("pass_quote_then_direction", False,
     "Quote the span, then direct. Both legal, and adjacent — the commonest true negative.",
     'You wrote "es superior a" in your Conclusions; that has to sit at L0.'),
    ("pass_the_word_superior_is_l3", False,
     'Why "word" and "phrase" are not Class B verbs: as nouns they sit right next '
     "to the quote R3 demands.",
     'The word "superior" is an L3 verb; the phrase "se asoció con" is L1.'),
    ("pass_apostrophes_are_not_quotes", False,
     "Apostrophes must not read as a quoted span, or contractions manufacture findings.",
     "Your design can't carry it and the abstract doesn't say why."),
    ("pass_class_c_frame_without_quoted_text", False,
     "A full Class C frame directing the DESIGN, not the prose. R9 leaves direction "
     "legal, so the quoted span is what separates a rewrite from a redesign.",
     "Change the study design to prospective and the ceiling moves to L1."),
    ("pass_class_b_imperative_without_quoted_text", False,
     "An imperative opening the clause with no text supplied. Direction again — "
     'R9 calls "this needs to sit at L0" legal, and so is this.',
     "Write the Conclusions at L0 and the finding goes away."),
]


def self_test():
    failures = 0
    print("rewrite-gate.py --self-test — %d cases (%d must fire, %d must not). "
          "All editor output is SYNTHETIC.\n"
          % (len(CASES), sum(1 for c in CASES if c[1]), sum(1 for c in CASES if not c[1])))
    for name, want_fire, what, text in CASES:
        findings = scan(text)
        fired = bool(findings)
        ok = fired == want_fire
        if not ok:
            failures += 1
        print("%-5s %s" % ("pass" if ok else "FAIL", name))
        for line in _wrap(what, 68):
            print("      %s" % line)
        if not ok:
            if want_fire:
                print("      -> expected a violation, got clean. R9 leak.")
            else:
                print("      -> expected clean, got %d finding(s). False positive on "
                      "legal output:" % len(findings))
                for f in findings:
                    print("         class %s · fired: %s" % (f["cls"], f["pattern"]))
        print("")
    print("%d/%d pass" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--output", metavar="FILE", help="the editor's output to audit")
    ap.add_argument("--self-test", action="store_true", help="run the embedded cases")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.output:
        ap.print_help()
        return 2

    with open(args.output, encoding="utf-8") as fh:
        text = fh.read()
    findings = scan(text)
    print(report(findings, args.output))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

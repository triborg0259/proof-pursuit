#!/usr/bin/env python3
"""
pacchetto_submission.py — per ogni cella produce il PACCHETTO per la piattaforma:
  1. problema-N/submission/parte-K.argument.md  — Markdown (inglese) da incollare nel campo "Your argument": risultato, prova,
     verifica, fonti arXiv, codice, e come si sono comportati gli agenti (decisioni del loop, verdetti dei giudici);
  2. report/cells/pN_cK.tex                      — LaTeX con le stesse risorse per esteso (codice completo, riesecuzioni,
     citazioni), da linkare nel campo "Write-up link";
  3. SUBMISSIONS.md                              — indice: slot, titolo, stato, file da incollare, link del write-up.
Perché: la piattaforma vuole un argomento testuale e un link consultabile dai giudici; il repo pubblico su GitHub fa da hosting.
Uso: .venv/bin/python tools/pacchetto_submission.py
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/triborg0259/proof-pursuit/blob/main/"
CELLE = json.loads((ROOT / "runs" / "celle.json").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("br", ROOT / "tools" / "build_report.py")
br = importlib.util.module_from_spec(spec); spec.loader.exec_module(br)


def decisioni_md(run):
    """Le decisioni degli agenti in Markdown: cosa ha scelto il Researcher e perché, cosa ha detto il Referee."""
    righe = []
    for v in br.iterazioni(run):
        righe.append(f"- **{v['attempt_id']}** — Researcher: family `{v.get('family')}`, subgoal: {v.get('subgoal')}; declared `{v.get('claimed_status')}`.")
        if v.get("researcher_reason"):
            righe.append(f"  - Why this approach: {v['researcher_reason']}")
        if v.get("literature_position"):
            righe.append(f"  - Position w.r.t. the literature: {v['literature_position']}")
        righe.append(f"  - Referee: `{v.get('verdict')}` / `{v.get('review_status')}`" + (f"; fatal error: {v['fatal_error']}" if v.get("fatal_error") else "") + (f"; next: {v['next_blocker']}" if v.get("next_blocker") else ""))
        if v.get("creative"):
            righe.append(f"  - Creative agent activated ({v['creative']}): {v.get('creative_analysis')}")
    appr = run / "approval.json"
    if appr.exists():
        a = json.loads(appr.read_text()); righe.append(f"- **Human approval**: {a['approved_by']} at {a['approved_at']} (READY_FOR_HUMAN → ACCEPT).")
    return "\n".join(righe) or "- No agent run on this cell; the text was written by the team from its notes."


def codice_md(run):
    blocchi = []
    for v in br.iterazioni(run):
        a = br.leggi_json(run / "attempts" / f"{v['attempt_id']}.json") or {}
        oss = br.leggi_json(run / "verifica" / v["attempt_id"] / "osservazioni.json") or []
        for i, c in enumerate(a.get("code_used", []), start=1):
            blocchi.append(f"**{v['attempt_id']} / code_{i}** ({c.get('language')}, rigor `{c.get('rigor')}`): {c.get('purpose')}\n\n```{c.get('language','python')}\n{c.get('code','')}\n```\n" + (f"Trusted re-run by the orchestrator: `{oss[i-1][:300]}`\n" if i <= len(oss) else ""))
    return "\n".join(blocchi)


def token_md(run):
    """Token consumati dagli agenti su questa cella: Researcher (meta.usage) e Referee (referee_*.json usage).
    Gli output token includono il ragionamento (thinking): la CLI non lo riporta separatamente."""
    righe, tot_in, tot_out = [], 0, 0
    for att in sorted((run / "attempts").glob("attempt_*.json")):
        u = ((br.leggi_json(att) or {}).get("meta") or {}).get("usage") or {}
        if u:
            i, o = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0), u.get("output_tokens", 0)
            tot_in += i; tot_out += o
            righe.append(f"- Researcher {att.stem}: input {i:,} · output (incl. reasoning) {o:,}")
        r = br.leggi_json(run / "attempts" / att.name.replace("attempt_", "referee_")) or {}
        for x in r.get("usage", []):
            u = x.get("usage") or {}
            if u:
                i, o = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0), u.get("output_tokens", 0)
                tot_in += i; tot_out += o
                righe.append(f"- Referee judge {x['role']}: input {i:,} · output (incl. reasoning) {o:,}")
    if not righe:
        return "- Token counts not recorded for this run (older harness version; only cost and turns were logged)."
    return "\n".join(righe) + f"\n- **Total**: input {tot_in:,} · output {tot_out:,} tokens"


def fonti_md(n, pid):
    return "\n".join(f"- arXiv:{v['arxiv_id']} — *{v['title']}* ({', '.join(v['authors'][:3])}, {v['published'][:4]}), found by query `{v.get('query','')}`; abstract read, full text not relied upon." for v in br.fonti_arxiv(n, pid)) or "- No relevant arXiv entry found by the deterministic search."


def normalizza_math(testo):
    """Adatta il Markdown al campo della piattaforma ("$…$ inline, $$…$$ display"): ogni blocco $$…$$ su UNA riga,
    niente \\tag (numero messo a fianco), nessuna riga vuota dentro le formule. Il codice nei blocchi ``` non viene toccato."""
    pezzi = testo.split("```")
    for i in range(0, len(pezzi), 2):        # solo le parti fuori dai blocchi di codice
        t = pezzi[i]
        t = re.sub(r"\$\$(.+?)\$\$", lambda m: "$$" + " ".join(m.group(1).split()) + "$$", t, flags=re.S)
        t = re.sub(r"\\tag\{([^}]*)\}", r"\\qquad(\1)", t)
        pezzi[i] = t
    return "```".join(pezzi)


def pulisci_markdown(testo):
    """Testo pulito per il campo della piattaforma: niente #, **, backtick, tabelle o blocchi di codice; restano
    paragrafi, elenchi con trattino e le formule $…$ / $$…$$. Il codice completo sta nel write-up linkato."""
    pezzi = testo.split("```")
    fuori = []
    for i in range(0, len(pezzi), 2):
        t = pezzi[i]
        t = re.sub(r"(?m)^#{1,6}\s*(.+?)\s*$", lambda m: "\n" + m.group(1) + "\n", t)   # titoli → riga a sé (niente maiuscole: romperebbero le formule)
        t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)                                            # grassetto
        t = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"\1", t)                        # corsivo
        t = re.sub(r"`([^`\n]+)`", r"\1", t)                                                 # codice inline
        t = re.sub(r"(?m)^\|\s*-+[-|\s]*$\n?", "", t)                                         # separatori di tabella
        t = re.sub(r"(?m)^\|(.+)\|\s*$", lambda m: "- " + " · ".join(c.strip() for c in m.group(1).split("|")), t)  # righe tabella
        t = re.sub(r"(?m)^-{3,}\s*$", "", t)                                                  # linee orizzontali
        t = re.sub(r"\n{3,}", "\n\n", t)
        fuori.append(t)
    return "\n".join(f.strip("\n") for f in fuori if f.strip()) + "\n"


def argument(pid, n, k):
    sub = ROOT / f"problema-{n}" / "submission"
    base = (sub / f"parte-{k}.en.md").read_text(encoding="utf-8") if (sub / f"parte-{k}.en.md").exists() else "(no draft)"
    runs = br.cartelle_run(pid, k)
    testo = base + "\n\n## 6. How this result was obtained (multi-agent trace)\n" \
        "Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:\n" \
        + "\n".join(decisioni_md(r) for r in runs) + "\n\n## 6b. Tokens used by the agents\n" + "\n".join(token_md(r) for r in runs) + "\n\n## 7. arXiv literature consulted\n" + fonti_md(n, pid) \
        + f"\n\n## 8. Code\nThe complete code, with the orchestrator's trusted re-runs, is in the write-up {REPO}report/cells/{pid}_c{k}.tex and in the repository.\n" \
        + f"\n\n---\nFull write-up (LaTeX, all resources): {REPO}report/cells/{pid}_c{k}.tex · Repository: {REPO}\n"
    (sub / f"parte-{k}.argument.md").write_text(pulisci_markdown(normalizza_math(testo)), encoding="utf-8")
    return testo


def cella_tex(pid, n, k):
    corpo = br.sezione_cella(pid, n, k, CELLE[pid]["cells"][k])
    fonti = br.fonti_arxiv(n, pid)
    bib = "\n".join(f"\\bibitem{{{v['arxiv_id']}}} {br.tex(', '.join(v['authors']))}. \\emph{{{br.tex(v['title'])}}}. arXiv:{v['arxiv_id']} ({v['published'][:4]}). \\url{{{v['url']}}}" for v in fonti)
    out = ROOT / "report" / "cells" / f"{pid}_c{k}.tex"
    out.parent.mkdir(exist_ok=True)
    out.write_text(br.PREAMBOLO.replace("rapporto completo", f"Problem {n}, part {k}") + f"\\section{{Problem {n} — {br.tex(CELLE[pid]['title'])}}}\n" + corpo
                   + "\n\\section{arXiv literature consulted}\n" + ("\\begin{thebibliography}{99}\n" + bib + "\n\\end{thebibliography}\n" if bib else "None found.\n") + "\\end{document}\n", encoding="utf-8")


def main():
    righe = ["# Submission packages (one per platform slot)\n", "| Slot | Problem / part | Status (STATUS.md) | Paste into *Your argument* | *Write-up link* |", "|---|---|---|---|---|"]
    for pid in CELLE:
        n = pid[1]
        for k in CELLE[pid]["cells"]:
            argument(pid, n, k); cella_tex(pid, n, k)
            stato, _ = br.stato_cella(n, k)
            righe.append(f"| /p/{pid}/c{k} | problem {n}, part {k} | {stato} | `problema-{n}/submission/parte-{k}.argument.md` | {REPO}report/cells/{pid}_c{k}.tex |")
    righe.append("\nNumeric cells (p2/c1–c4): paste the value(s) in *Your answer* (see section 1 of the argument file) and put the argument file's content or link in the write-up. *Claude conversation*: leave empty unless a shareable link exists.")
    (ROOT / "SUBMISSIONS.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    print("scritti 24 argument.md, 24 report/cells/*.tex, SUBMISSIONS.md")


if __name__ == "__main__":
    main()

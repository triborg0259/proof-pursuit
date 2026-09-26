#!/usr/bin/env python3
"""
literature.py — ricerca bibliografica su arXiv per il Researcher.

Cosa fa: interroga l'API pubblica di arXiv (nessuna chiave) con una o più query, salva i risultati in
`<workdir>/literature.json` (id, titolo, autori, data, abstract, url) e li restituisce come sezione di prompt.
Perché: il Researcher deve dire in che rapporto sta il suo approccio con lo stato dell'arte, e per farlo con
citazioni vere (id arXiv reali, abstract letti) serve una ricerca deterministica prima del tentativo.
Limite dichiarato: si leggono solo gli abstract; il testo completo, se serve, lo scarica il modello in shell `full`.

Uso:
  python3 researcher/literature.py --workdir runs/X --query "Bulgarian solitaire" --query "partition shift cycle" [--max 5]
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API = "https://export.arxiv.org/api/query?"
NS = {"a": "http://www.w3.org/2005/Atom"}


def _testo(entry, tag):
    """Testo di un campo Atom, normalizzato su una riga (arXiv spezza titoli e abstract con a capo)."""
    nodo = entry.find(f"a:{tag}", NS)
    return " ".join((nodo.text or "").split()) if nodo is not None else ""


def _voce(entry):
    """Un risultato arXiv nel formato compatto che finisce nel prompt e nel file."""
    url = _testo(entry, "id")
    return {"arxiv_id": url.rsplit("/abs/", 1)[-1], "url": url, "title": _testo(entry, "title"),
            "authors": [" ".join((a.find("a:name", NS).text or "").split()) for a in entry.findall("a:author", NS)],
            "published": _testo(entry, "published")[:10], "abstract": _testo(entry, "summary")}


def _query_arxiv(query):
    """Frase esatta per le query di più parole (altrimenti arXiv fa OR fra i termini e pesca rumore, es. '2022');
    chi vuole la sintassi nativa (ti:, au:, AND, virgolette) la scrive e viene passata così com'è."""
    if any(tok in query for tok in ('"', "ti:", "au:", "abs:", " AND ", " OR ")):
        return query
    return f'all:"{query}"' if " " in query else f"all:{query}"


def cerca_arxiv(query, max_results=5, timeout=30):
    """Una query su arXiv (ordinata per rilevanza). Ritorna una lista di voci; errori di rete → lista vuota
    con avviso, perché la bibliografia è un aiuto e non deve bloccare il tentativo."""
    params = urllib.parse.urlencode({"search_query": _query_arxiv(query), "start": 0, "max_results": max_results,
                                     "sortBy": "relevance"})
    try:
        data = urllib.request.urlopen(ARXIV_API + params, timeout=timeout).read()
    except Exception as err:  # rete assente, timeout, risposta malformata
        print(f"[literature] arXiv non raggiungibile per '{query}': {err}", file=sys.stderr)
        return []
    return [_voce(e) for e in ET.fromstring(data).findall("a:entry", NS)]


def cerca_tutte(queries, max_results=5):
    """Esegue tutte le query e unisce i risultati senza duplicati (stesso id arXiv), rispettando il rate limit
    consigliato da arXiv (una richiesta ogni 3 secondi)."""
    viste, voci = set(), []
    for i, q in enumerate(queries):
        if i:
            time.sleep(3)
        for v in cerca_arxiv(q, max_results):
            if v["arxiv_id"] not in viste:
                viste.add(v["arxiv_id"])
                voci.append({**v, "query": q})
    return voci


def sezione_prompt(voci, max_abstract=900):
    """La sezione LITERATURE del prompt: id, titolo, autori, anno e abstract (accorciato) di ogni voce."""
    if not voci:
        return ""
    righe = ["# LITERATURE (arXiv abstracts found by a deterministic search; you have NOT read the full papers)"]
    for v in voci:
        autori = ", ".join(v["authors"][:4]) + (" et al." if len(v["authors"]) > 4 else "")
        righe.append(f"- [{v['arxiv_id']}] {v['title']} — {autori} ({v['published'][:4]}). "
                     f"Abstract: {v['abstract'][:max_abstract]}")
    righe.append("Use these to write `literature_position`: what the state of the art already gives for this cell, "
                 "and why your approach follows, adapts or departs from it. Cite by arXiv id. If you rely on a result "
                 "from a paper, quote the statement you use and mark it as CITED, not proved, unless you reproduce the proof.")
    return "\n".join(righe)


def carica(workdir: Path):
    """Le voci già salvate in <workdir>/literature.json, oppure lista vuota."""
    p = workdir / "literature.json"
    return json.loads(p.read_text()) if p.exists() else []


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--query", action="append", required=True, help="ripetibile")
    ap.add_argument("--max", type=int, default=5)
    a = ap.parse_args()
    voci = cerca_tutte(a.query, a.max)
    out = Path(a.workdir) / "literature.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(voci, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(voci)} voci salvate in {out}")
    for v in voci:
        print(f"  [{v['arxiv_id']}] {v['title'][:80]} ({v['published'][:4]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
parziali.py — genera una bozza di consegna PARZIALE per ogni cella senza consegna: enunciato ufficiale della parte,
cosa è stabilito (dalle note del team), letteratura arXiv pertinente, codice esistente, cosa resta aperto.
Perché: un risultato parziale descritto correttamente vale; ogni slot della piattaforma deve avere una traccia.
Non sovrascrive le consegne esistenti. Uso: .venv/bin/python tools/parziali.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLE = json.loads((ROOT / "runs" / "celle.json").read_text(encoding="utf-8"))
TESTI = json.loads((ROOT / "tools" / "parziali_testi.json").read_text(encoding="utf-8"))


def parte_enunciato(n, k):
    testo = (ROOT / f"problema-{n}" / "enunciato.md").read_text(encoding="utf-8")
    sez = re.split(r"(?m)^(?=## Parte )", testo)
    return next((s for s in sez[1:] if re.match(rf"## Parte {k}\b", s)), "").strip()


def fonti(n, pid):
    import importlib.util
    spec = importlib.util.spec_from_file_location("pr", ROOT / "tools" / "prepara_runs.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    f = ROOT / f"problema-{n}" / "fonti" / "arxiv.json"
    voci = [v for v in json.loads(f.read_text()) if m.pertinente(v, m.PAROLE[pid])] if f.exists() else []
    return "\n".join(f"- arXiv:{v['arxiv_id']} — {v['title']} ({', '.join(v['authors'][:3])}, {v['published'][:4]}); solo abstract letto." for v in voci) or "- Nessuna voce arXiv pertinente trovata dalla ricerca deterministica."


def codice(n, pid, k):
    righe = [f"- `{p.relative_to(ROOT)}`" for d in ("certificati", "esperimenti") for p in sorted((ROOT / f"problema-{n}" / d).glob("*.py"))]
    run = ROOT / "runs" / f"{pid}_c{k}"
    for a in sorted((run / "attempts").glob("attempt_*.json")) if run.exists() else []:
        att = json.loads(a.read_text())
        righe += [f"- Researcher {a.stem}, code_{i+1} ({c['language']}, {c['rigor']}): {c['purpose'][:120]}" for i, c in enumerate(att.get("code_used", []))]
    return "\n".join(righe) or "- Nessun codice ancora."


def scrivi(pid, n, k):
    out = ROOT / f"problema-{n}" / "submission" / f"parte-{k}.md"
    if out.exists():
        return False
    t = TESTI[f"{pid}_c{k}"]
    out.parent.mkdir(exist_ok=True)
    out.write_text(f"""# Problema {n} — Parte {k} — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
{parte_enunciato(n, k)}

**Cosa consegniamo.** {t['risultato']}

## 2. Dimostrazione
{t['argomento']}

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
{codice(n, pid, k)}

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
{fonti(n, pid)}
{t['letteratura']}

## 5. Limiti e parti irrisolte
{t['aperto']}
""", encoding="utf-8")
    return True


if __name__ == "__main__":
    for pid in CELLE:
        for k in CELLE[pid]["cells"]:
            if f"{pid}_c{k}" in TESTI:
                print(f"{pid}_c{k}:", "scritta" if scrivi(pid, pid[1], k) else "già presente")

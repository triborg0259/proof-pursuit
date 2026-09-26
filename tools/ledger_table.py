#!/usr/bin/env python3
"""Stampa una tabella Markdown da un ledger JSONL: python3 tools/ledger_table.py ledger.jsonl [tag]"""
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if len(sys.argv) > 2:
    rows = [r for r in rows if r["tag"] == sys.argv[2]]
print("| tag | args | seeds | budget/seed | iter | best | target | gap | cert |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    c = r.get("certify") or {}
    print(f"| {r['tag']} | {' '.join(r['args'])} | {len(r['seeds'])} | {r['budget_per_seed_s']}s | {r['iters_total']} | "
          f"{r['best_score']:.9f} | {r['target'] if r['target'] is None else round(r['target'],9)} | "
          f"{'' if r['gap_target_minus_best'] is None else format(r['gap_target_minus_best'],'.2e')} | "
          f"{c.get('summary','')} |")

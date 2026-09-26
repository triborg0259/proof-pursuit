"""Test del Referee B con backend mock: nessuna chiamata a modelli, nessun costo.

Coprono i casi richiesti da CLAUDE_CODE_B.md (prova autonoma, fonte vietata, citazione non
verificata, log falso, campionamento spacciato per enumerazione, float senza controllo,
computazione esatta con certificato) e la conversione verso shared/schemas/referee_report.schema.json.

Questi test verificano il CONTRATTO e la conversione, non la qualita' del giudizio del modello.

Esecuzione: python -m pytest tests/ -q     oppure     python tests/test_b_referee.py
"""
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from referees.adapter_b import MockBackend, build_review_input, review_attempt  # noqa: E402
from referees.contracts import AgentEnvelope, EvidenceReport, Issue, Provenance  # noqa: E402

WORKDIR = ROOT / "tests" / "fixtures" / "referee_b" / "toy_cell"
SCHEMA = json.loads((ROOT / "shared" / "schemas" / "referee_report.schema.json").read_text(encoding="utf-8"))


# =============================================================================== helper
def provenance(claim_id="main", categories=("PROVED_BY_US",), sufficient=True, permitted=True,
               external=False, computation=False):
    """Una voce di provenienza; i default descrivono un claim dimostrato in proprio e in regola."""
    return Provenance(claim_id=claim_id, categories=list(categories), evidence_sufficient=sufficient,
                      permitted_by_rules=permitted, relies_on_external_result=external,
                      uses_computation_as_proof=computation, references=[], notes="valutazione simulata nei test")


def envelope(verdict, *, sources=(), computations=(), rules=(), claims=None, notes="note simulate"):
    """Costruisce la risposta del modello come la restituirebbe il backend reale (dict JSON)."""
    report = EvidenceReport(evidence_verdict=verdict, source_issues=list(sources),
                            computation_issues=list(computations), rule_violations=list(rules),
                            claim_provenance=list(claims if claims is not None else [provenance()]),
                            reproducibility_notes=notes)
    return AgentEnvelope[EvidenceReport](report=report, limitation=None).model_dump(mode="json")


def issue(code, detail, severity, claim_ids=("main",)):
    return Issue(code=code, detail=detail, severity=severity, claim_ids=list(claim_ids))


def run(response):
    """Esegue il Referee B sulla fixture con una risposta simulata e ritorna (rapporto, backend)."""
    backend = MockBackend(response)
    report = asyncio.run(review_attempt(WORKDIR, backend))
    return report, backend


def check_schema(report):
    """Controllo dei campi obbligatori e degli enum di referee_report.schema.json."""
    missing = [k for k in SCHEMA["required"] if k not in report]
    assert not missing, f"campi mancanti nel rapporto: {missing}"
    assert report["verdict"] in SCHEMA["properties"]["verdict"]["enum"]
    assert isinstance(report["citation_issue"], bool) and isinstance(report["computation_issue"], bool)
    assert isinstance(report["highest_verified_cell"], int) and report["highest_verified_cell"] >= 0


# =============================================================================== costruzione dell'input
def test_review_input_registra_claim_e_artefatti():
    """L'adattatore traduce attempt.json nei contratti: bersaglio protetto, dipendenze, fonti, codice."""
    job = build_review_input(WORKDIR)
    assert job.cell.number == 1 and job.cell.target_claim_id == "main"
    assert job.cell.statement.startswith("Determine the exact value of T(G_0)")
    target = next(c for c in job.candidate.claims if c.id == "main")
    # claims_used[0] coincide con un claim verificato -> vc_1; claims_used[1] no -> dep_2 del candidato
    assert target.depends_on == ["vc_1", "dep_2"]
    assert [c.id for c in job.state.claims] == ["vc_1"]
    assert {a.id for a in job.candidate.artifacts} == {"code_1", "code_2"}
    assert all(a.kind == "CODE" for a in job.candidate.artifacts)
    assert job.candidate.method_tag == "exact_computation"


def test_payload_include_regole_e_codice_non_eseguito():
    """B riceve le regole della gara e il codice come testo da leggere; nulla viene eseguito."""
    _, backend = run(envelope("PASS"))
    assert len(backend.seen) == 1 and backend.seen[0]["role"] == "B"
    payload = backend.seen[0]["payload"]
    assert "rules" in payload["submission"], "il Referee B deve vedere le regole della competizione"
    assert payload["trusted_observations"] == [], "nessuna verifica indipendente e' stata eseguita"
    codice = payload["submission"]["candidate"]["artifacts"][0]["content"]
    assert "itertools" in codice and "rigor dichiarato dal candidato: exact" in codice


# =============================================================================== i sette casi richiesti
def test_prova_autonoma_senza_citazioni():
    """Prova che non dipende da fonti esterne: nessun problema di citazione, ma non e' ACCEPT."""
    report, _ = run(envelope("PASS", claims=[provenance(external=False)]))
    check_schema(report)
    assert report["verdict"] == "PARTIAL_PROGRESS"
    assert report["citation_issue"] is False and report["computation_issue"] is False
    assert report["fatal_error"] is None
    assert report["evidence_supported_claims"] == ["main"]


def test_fonte_valida_ma_vietata():
    """Dipendenza essenziale da un risultato citato, non ammessa dalle regole: rigetto con errore fatale."""
    report, _ = run(envelope("FAIL", rules=[issue("FORBIDDEN_SOURCE",
                    "Il target dipende in modo essenziale dal Teorema 1.2 citato; le regole non ammettono la letteratura come prova", "FATAL")],
                    claims=[provenance(categories=("KNOWN_IN_LITERATURE",), sufficient=False, permitted=False, external=True)]))
    check_schema(report)
    assert report["verdict"] == "REJECT"
    assert "FORBIDDEN_SOURCE" in report["fatal_error"] and "[main]" in report["fatal_error"]
    assert report["evidence_supported_claims"] == []


def test_citazione_non_verificata():
    """Fonte citata ma mai letta: e' una MANCANZA da colmare, non una frode accertata."""
    report, _ = run(envelope("PARTIAL", sources=[issue("SOURCE_NOT_RETRIEVED",
                    "Citazione presente ma il testo della fonte non e' stato consegnato ne' recuperato", "MISSING")],
                    claims=[provenance(categories=("UNVERIFIED",), sufficient=False, external=True)]))
    check_schema(report)
    assert report["verdict"] == "PARTIAL_PROGRESS"
    assert report["citation_issue"] is True
    assert report["fatal_error"] is None, "una verifica mancante non e' un errore fatale"
    assert "SOURCE_NOT_RETRIEVED" in report["next_blocker"]


def test_log_falso():
    """Un log consegnato dal candidato che non corrisponde al codice: difetto computazionale fatale."""
    report, _ = run(envelope("FAIL", computations=[issue("LOG_INCONSISTENT",
                    "Il log dichiara 40320 casi ma il codice consegnato ne enumera 5040", "FATAL")],
                    claims=[provenance(categories=("UNVERIFIED",), sufficient=False, computation=True)]))
    check_schema(report)
    assert report["verdict"] == "REJECT"
    assert report["computation_issue"] is True
    assert "LOG_INCONSISTENT" in report["fatal_error"]


def test_campionamento_spacciato_per_enumerazione():
    """Ricerca campionaria presentata come esaustiva: l'insieme coperto non sostiene il claim."""
    report, _ = run(envelope("FAIL", computations=[issue("NOT_EXHAUSTIVE",
                    "Il codice campiona 10^6 etichettature casuali ma il testo afferma di averle enumerate tutte", "FATAL")],
                    claims=[provenance(categories=("EXPERIMENTAL_ONLY",), sufficient=False, computation=True)]))
    check_schema(report)
    assert report["verdict"] == "REJECT" and report["computation_issue"] is True
    assert report["evidence_supported_claims"] == []


def test_floating_point_senza_controllo_dell_errore():
    """Float senza controllo dell'errore: resta esplorazione, non sostiene il claim come prova."""
    report, _ = run(envelope("PARTIAL", computations=[issue("UNCONTROLLED_ERROR",
                    "Il confronto usa float senza stima dell'errore; serve aritmetica esatta o a intervalli", "MISSING")],
                    claims=[provenance(categories=("EXPERIMENTAL_ONLY",), sufficient=False, computation=True)]))
    check_schema(report)
    assert report["verdict"] == "PARTIAL_PROGRESS"
    assert report["computation_issue"] is True
    assert report["evidence_supported_claims"] == [], "EXPERIMENTAL_ONLY non e' evidenza sufficiente"


def test_computazione_esatta_con_certificato_autentico():
    """Enumerazione esatta, riproducibile e con certificato: evidenze complete, ma il verdetto resta umano."""
    report, _ = run(envelope("PASS", claims=[provenance(categories=("COMPUTATIONALLY_VERIFIED", "PROVED_BY_US"),
                    computation=True)], notes="Enumerazione esatta di 40320 casi, interi Python, 0.36 s, riproducibile"))
    check_schema(report)
    assert report["verdict"] != "ACCEPT", "l'ACCEPT finale e' una decisione umana"
    assert report["verdict"] == "PARTIAL_PROGRESS"
    assert report["evidence_supported_claims"] == ["main"]
    assert "40320" in report["reasoning_summary"]


# =============================================================================== invarianti del contratto
def test_nessun_verdetto_accept_in_nessun_caso():
    """Nessuna combinazione di risposte del modello puo' produrre ACCEPT da questo componente."""
    for verdict in ("PASS", "PARTIAL", "FAIL"):
        extra = {"computations": [issue("X", "difetto", "FATAL")]} if verdict == "FAIL" else {}
        claims = [provenance(sufficient=verdict == "PASS")]
        report, _ = run(envelope(verdict, claims=claims, **extra))
        assert report["verdict"] != "ACCEPT"
        assert report["accept_requires_human"] is True


def test_accepted_claims_sempre_vuoto_e_stato_non_avanza():
    """B non promuove claim a progresso verificato e non incrementa highest_verified_cell."""
    report, _ = run(envelope("PASS"))
    assert report["accepted_claims"] == [], "solo orchestratore e umano popolano il progresso verificato"
    stato = json.loads((WORKDIR / "state.json").read_text(encoding="utf-8"))
    assert report["highest_verified_cell"] == stato["highest_verified_cell"] == 1


def test_errore_del_modello_non_diventa_un_rigetto():
    """Un output non conforme allo schema diventa UNKNOWN_STATUS con limitation, mai REJECT."""
    report, _ = run({"report": {"evidence_verdict": "INVENTATO"}, "limitation": None})
    check_schema(report)
    assert report["verdict"] == "UNKNOWN_STATUS"
    assert report["fatal_error"] is None
    assert "B:" in report["limitation"]


def test_timeout_non_diventa_un_rigetto():
    """Anche un timeout e' una limitazione operativa, non un difetto del tentativo."""
    backend = MockBackend(None)
    backend.generate = lambda **kwargs: asyncio.sleep(0.2)  # risposta piu' lenta del timeout
    job_report = asyncio.run(review_attempt(WORKDIR, backend, timeout=0.01))
    check_schema(job_report)
    assert job_report["verdict"] == "UNKNOWN_STATUS"
    assert "TimeoutError" in job_report["limitation"]


if __name__ == "__main__":
    for nome, funzione in list(globals().items()):
        if nome.startswith("test_"):
            funzione()
            print("ok", nome)

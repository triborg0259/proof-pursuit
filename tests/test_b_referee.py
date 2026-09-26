"""Test del Referee B (evidenze, fonti, calcolo, regole) attraverso il ponte `bridge_referee.py`.

Coprono i casi richiesti da CLAUDE_CODE_B.md — prova autonoma senza citazioni, fonte valida ma
vietata, citazione non verificata, log falso, campionamento spacciato per enumerazione, floating
point senza controllo, computazione esatta con certificato autentico — piu' gli invarianti del
contratto (mai ACCEPT, lo stato non avanza, un errore operativo non e' un rigetto).

Il backend e' simulato: risponde per il ruolo A e per il ruolo B senza nessuna chiamata a pagamento.
Verificano il CONTRATTO e la traduzione, non la qualita' del giudizio del modello.

Esecuzione: python -m pytest tests/ -q     oppure     python tests/test_b_referee.py
"""
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "referee"))
sys.path.insert(0, str(ROOT / "researcher"))

# `researcher/` non e' un package: i suoi moduli si importano come moduli di primo livello,
# come fa bridge_referee.py stesso.
from bridge_referee import converti_packet, costruisci_review_input  # noqa: E402
from referees.contracts import ReviewInput  # noqa: E402
from referees.hackathon import prepare_review  # noqa: E402

WORKDIR = ROOT / "tests" / "fixtures" / "referee_b" / "toy_cell"
SCHEMA = json.loads((ROOT / "shared" / "schemas" / "referee_report.schema.json").read_text(encoding="utf-8"))


# =============================================================================== helper
def provenienza(claim_id="main", categorie=("PROVED_BY_US",), sufficiente=True, permessa=True,
                esterno=False, calcolo=False):
    """Una voce di provenienza; i default descrivono un claim dimostrato in proprio e in regola."""
    return {"claim_id": claim_id, "categories": list(categorie), "evidence_sufficient": sufficiente,
            "permitted_by_rules": permessa, "relies_on_external_result": esterno,
            "uses_computation_as_proof": calcolo, "references": [], "notes": "valutazione simulata nei test"}


def segnalazione(codice, dettaglio, gravita, claim_ids=("main",)):
    return {"code": codice, "detail": dettaglio, "severity": gravita, "claim_ids": list(claim_ids)}


def evidenze(verdetto, *, fonti=(), calcoli=(), regole=(), claim=None, note="note simulate"):
    """Risposta del Referee B come la restituirebbe il backend reale."""
    return {"report": {"evidence_verdict": verdetto, "source_issues": list(fonti),
                       "computation_issues": list(calcoli), "rule_violations": list(regole),
                       "claim_provenance": list(claim if claim is not None else [provenienza()]),
                       "reproducibility_notes": note},
            "limitation": None}


def matematica(verdetto="PARTIAL", accettati=("main",)):
    """Risposta del Referee A: qui e' solo contorno, i test riguardano B."""
    return {"report": {"mathematical_verdict": verdetto, "first_fatal_error": None,
                       "accepted_mathematical_claims": list(accettati), "unproved_claims": [],
                       "missing_cases": [], "math_notes": "giudice matematico simulato"},
            "limitation": None}


class BackendSimulato:
    """Risponde ai due ruoli con risposte preparate. Nessuna rete, nessun costo."""

    def __init__(self, risposta_b, risposta_a=None):
        self.risposta_b, self.risposta_a = risposta_b, risposta_a or matematica()
        self.visti = []

    async def generate(self, *, role, system, payload, schema):
        self.visti.append({"role": role, "payload": payload})
        return self.risposta_a if role == "A" else self.risposta_b


def esegui(risposta_b, risposta_a=None, timeout=30):
    """Costruisce il ReviewInput dalla fixture, esegue la revisione e converte il pacchetto."""
    attempt = json.loads((WORKDIR / "attempt.json").read_text(encoding="utf-8"))
    job = costruisci_review_input(WORKDIR, attempt)
    backend = BackendSimulato(risposta_b, risposta_a)
    packet = asyncio.run(prepare_review(ReviewInput.model_validate(job), backend, [], timeout=timeout))
    pacchetto = json.loads(packet.model_dump_json())
    return converti_packet(pacchetto, attempt["attempt_id"]), pacchetto, backend


def controlla_schema(report):
    """Campi obbligatori ed enum di shared/schemas/referee_report.schema.json."""
    mancanti = [k for k in SCHEMA["required"] if k not in report]
    assert not mancanti, f"campi mancanti nel rapporto: {mancanti}"
    assert report["verdict"] in SCHEMA["properties"]["verdict"]["enum"]
    assert isinstance(report["citation_issue"], bool) and isinstance(report["computation_issue"], bool)
    assert isinstance(report["highest_verified_cell"], int) and report["highest_verified_cell"] >= 0


# =============================================================================== costruzione dell'input
def test_claim_usati_ma_non_verificati_diventano_claim_del_candidato():
    """`claims_used` senza riscontro nello stato non sparisce: diventa `dep_k`, da valutare."""
    attempt = json.loads((WORKDIR / "attempt.json").read_text(encoding="utf-8"))
    job = costruisci_review_input(WORKDIR, attempt)
    ids = {c["id"] for c in job["candidate"]["claims"]}
    assert ids == {"main", "dep_2"}, ids
    principale = next(c for c in job["candidate"]["claims"] if c["id"] == "main")
    assert principale["depends_on"] == ["verified_1", "dep_2"]
    assert [c["id"] for c in job["state"]["claims"]] == ["verified_1"]


def test_enunciato_preso_da_problem_md():
    """Senza `cell_statement` in state.json il bersaglio viene dalla riga `Cell N:` di problem.md."""
    attempt = json.loads((WORKDIR / "attempt.json").read_text(encoding="utf-8"))
    job = costruisci_review_input(WORKDIR, attempt)
    assert job["cell"]["statement"].startswith("Determine the exact value of T(G_0)")
    # il contratto impone che il candidato dichiari il bersaglio esatto
    assert job["candidate"]["claims"][0]["statement"] == job["cell"]["statement"]


def test_regole_lette_dal_file_condiviso():
    """Le regole arrivano da shared/competition_rules.example.json, non da un dizionario nel codice."""
    attempt = json.loads((WORKDIR / "attempt.json").read_text(encoding="utf-8"))
    job = costruisci_review_input(WORKDIR, attempt)
    attese = json.loads((ROOT / "shared" / "competition_rules.example.json").read_text(encoding="utf-8"))
    assert job["rules"] == attese
    assert job["rules"]["allow_literature_as_proof"] is False
    assert "NON sono le regole ufficiali" in job["rules"]["additional_rules"]


def test_il_referee_b_vede_le_regole_e_il_codice_non_eseguito():
    """B riceve le regole e il codice come testo da leggere; A non vede le regole; nulla viene eseguito."""
    _, _, backend = esegui(evidenze("PASS"))
    ruoli = {v["role"] for v in backend.visti}
    assert ruoli == {"A", "B"}
    payload_b = next(v["payload"] for v in backend.visti if v["role"] == "B")
    payload_a = next(v["payload"] for v in backend.visti if v["role"] == "A")
    assert "rules" in payload_b["submission"]
    assert "rules" not in payload_a["submission"], "il giudice matematico non deve vedere le regole"
    codice = payload_b["submission"]["candidate"]["artifacts"][0]["content"]
    assert "itertools" in codice and "rigor: exact" in codice


# =============================================================================== i sette casi richiesti
def test_prova_autonoma_senza_citazioni():
    """Prova che non dipende da fonti esterne: nessun problema di citazione."""
    report, _, _ = esegui(evidenze("PASS", claim=[provenienza(esterno=False)]))
    controlla_schema(report)
    assert report["citation_issue"] is False and report["computation_issue"] is False
    assert report["fatal_error"] is None
    assert report["verdict"] != "ACCEPT"


def test_fonte_valida_ma_vietata():
    """Dipendenza essenziale da un risultato citato, non ammessa dalle regole: rigetto."""
    report, _, _ = esegui(evidenze("FAIL", regole=[segnalazione("FORBIDDEN_SOURCE",
        "Il target dipende in modo essenziale dal Teorema 1.2 citato; le regole non ammettono la letteratura come prova",
        "FATAL")], claim=[provenienza(categorie=("KNOWN_IN_LITERATURE",), sufficiente=False, permessa=False, esterno=True)]))
    controlla_schema(report)
    assert report["verdict"] == "REJECT"
    assert report["citation_issue"] is True
    assert "Referee B" in report["fatal_error"]
    assert report["proposed_claim_ids"] == []


def test_citazione_non_verificata():
    """Fonte citata ma mai letta: e' una MANCANZA da colmare, non una frode accertata."""
    report, _, _ = esegui(evidenze("PARTIAL", fonti=[segnalazione("SOURCE_NOT_RETRIEVED",
        "Citazione presente ma il testo della fonte non e' stato consegnato ne' recuperato", "MISSING")],
        claim=[provenienza(categorie=("UNVERIFIED",), sufficiente=False, esterno=True)]))
    controlla_schema(report)
    assert report["citation_issue"] is True
    assert report["verdict"] != "REJECT", "una verifica mancante non e' un rigetto"
    assert report["proposed_claim_ids"] == [], "un claim non verificato non va proposto all'umano"


def test_log_falso():
    """Un log consegnato dal candidato che non corrisponde al codice: difetto computazionale fatale."""
    report, _, _ = esegui(evidenze("FAIL", calcoli=[segnalazione("LOG_INCONSISTENT",
        "Il log dichiara 40320 casi ma il codice consegnato ne enumera 5040", "FATAL")],
        claim=[provenienza(categorie=("UNVERIFIED",), sufficiente=False, calcolo=True)]))
    controlla_schema(report)
    assert report["verdict"] == "REJECT"
    assert report["computation_issue"] is True


def test_campionamento_spacciato_per_enumerazione():
    """Ricerca campionaria presentata come esaustiva: l'insieme coperto non sostiene il claim."""
    report, _, _ = esegui(evidenze("FAIL", calcoli=[segnalazione("NOT_EXHAUSTIVE",
        "Il codice campiona 10^6 etichettature casuali ma il testo afferma di averle enumerate tutte", "FATAL")],
        claim=[provenienza(categorie=("EXPERIMENTAL_ONLY",), sufficiente=False, calcolo=True)]))
    controlla_schema(report)
    assert report["verdict"] == "REJECT" and report["computation_issue"] is True
    assert report["proposed_claim_ids"] == []


def test_floating_point_senza_controllo_dell_errore():
    """Float senza controllo dell'errore: resta esplorazione, non sostiene il claim come prova."""
    report, _, _ = esegui(evidenze("PARTIAL", calcoli=[segnalazione("UNCONTROLLED_ERROR",
        "Il confronto usa float senza stima dell'errore; serve aritmetica esatta o a intervalli", "MISSING")],
        claim=[provenienza(categorie=("EXPERIMENTAL_ONLY",), sufficiente=False, calcolo=True)]))
    controlla_schema(report)
    assert report["computation_issue"] is True
    assert report["proposed_claim_ids"] == [], "EXPERIMENTAL_ONLY non e' evidenza sufficiente"


def test_computazione_esatta_con_certificato_autentico():
    """Enumerazione esatta e riproducibile: evidenze complete, ma il verdetto resta umano."""
    # un PASS deve coprire OGNI claim dichiarato, quindi anche il `dep_2` usato dal tentativo
    report, pacchetto, _ = esegui(evidenze("PASS", claim=[
        provenienza(categorie=("COMPUTATIONALLY_VERIFIED", "PROVED_BY_US"), calcolo=True),
        provenienza("dep_2", categorie=("PROVED_BY_US",))],
        note="Enumerazione esatta di 40320 casi, interi Python, 0.36 s, riproducibile"),
        risposta_a=matematica("PASS"))
    controlla_schema(report)
    assert report["verdict"] != "ACCEPT", "l'ACCEPT finale e' una decisione umana"
    assert pacchetto["review_status"] == "READY_FOR_HUMAN"
    assert report["proposed_claim_ids"] == ["main"], "il claim e' proposto all'umano, non accettato"
    assert report["accepted_claims"] == []


# =============================================================================== invarianti del contratto
def test_nessun_verdetto_accept_in_nessun_caso():
    """Nessuna combinazione di risposte dei modelli produce ACCEPT senza approvazione umana firmata."""
    for verdetto_b in ("PASS", "PARTIAL", "FAIL"):
        extra = {"calcoli": [segnalazione("X", "difetto", "FATAL")]} if verdetto_b == "FAIL" else {}
        claim = [provenienza(sufficiente=verdetto_b == "PASS")]
        for verdetto_a in ("PASS", "PARTIAL"):
            report, _, _ = esegui(evidenze(verdetto_b, claim=claim, **extra), matematica(verdetto_a))
            assert report["verdict"] != "ACCEPT", (verdetto_a, verdetto_b)
            assert report["accepted_claims"] == []


def test_lo_stato_condiviso_non_avanza():
    """highest_verified_cell e' una fotografia: il Referee non lo incrementa mai."""
    report, _, _ = esegui(evidenze("PASS"), matematica("PASS"))
    stato = json.loads((WORKDIR / "state.json").read_text(encoding="utf-8"))
    assert report["highest_verified_cell"] == stato["highest_verified_cell"] == 1


def test_errore_del_modello_non_diventa_un_rigetto():
    """Un output non conforme allo schema diventa UNKNOWN_STATUS, mai REJECT."""
    report, _, _ = esegui({"report": {"evidence_verdict": "INVENTATO"}, "limitation": None})
    controlla_schema(report)
    assert report["verdict"] == "UNKNOWN_STATUS"


def test_timeout_non_diventa_un_rigetto():
    """Anche un timeout e' una limitazione operativa, non un difetto del tentativo."""
    attempt = json.loads((WORKDIR / "attempt.json").read_text(encoding="utf-8"))
    job = costruisci_review_input(WORKDIR, attempt)

    class Lento:
        async def generate(self, **kwargs):
            await asyncio.sleep(0.2)

    packet = asyncio.run(prepare_review(ReviewInput.model_validate(job), Lento(), [], timeout=0.01))
    report = converti_packet(json.loads(packet.model_dump_json()), attempt["attempt_id"])
    controlla_schema(report)
    assert report["verdict"] == "UNKNOWN_STATUS"
    assert "TimeoutError" in report["reasoning_summary"]


if __name__ == "__main__":
    for nome, funzione in list(globals().items()):
        if nome.startswith("test_"):
            funzione()
            print("ok", nome)

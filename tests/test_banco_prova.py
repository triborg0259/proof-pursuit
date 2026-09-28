"""Test del banco di prova senza modelli: creazione dei casi con id neutri, classificazione dei verdetti,
matrice dei conteggi. Esecuzione: .venv/bin/python tests/test_banco_prova.py"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def carica_banco(cartella):
    """Importa tools/banco_prova.py puntando il banco a una cartella temporanea, così i test non sporcano il repo."""
    spec = importlib.util.spec_from_file_location("banco_prova", ROOT / "tools" / "banco_prova.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    modulo.BANCO = cartella
    modulo.ETICHETTE = cartella / "etichette.json"
    modulo.RISULTATI = cartella / "risultati.jsonl"
    return modulo


def test_crea_caso_e_variante_con_id_neutri():
    tmp = Path(tempfile.mkdtemp(prefix="pp_banco_"))
    banco = carica_banco(tmp)
    args = banco.build_parser().parse_args(["crea", "--run", "tests/fixtures/toy_fail", "--categoria", "corretta"])
    # la fixture non ha attempts/: ne creiamo uno minimo
    att = ROOT / "tests" / "fixtures" / "toy_fail" / "attempts"
    att.mkdir(exist_ok=True)
    (att / "attempt_001.json").write_text(json.dumps({"attempt_id": "attempt_001", "proof_attempt": "prova originale", "code_used": []}))
    try:
        banco.cmd_crea(args)
        variante = tmp / "variante.md"
        variante.write_text("prova con il caso r=0 saltato")
        banco.cmd_crea(banco.build_parser().parse_args(
            ["crea", "--da", "caso_01", "--categoria", "caso_mancante", "--proof-file", str(variante), "--nota", "salta r=0"]))
    finally:
        (att / "attempt_001.json").unlink(); att.rmdir()
    etichette = json.loads((tmp / "etichette.json").read_text())
    assert list(etichette) == ["caso_01", "caso_02"]
    assert etichette["caso_02"]["atteso"] == {"A": "FAIL", "B": None, "esito": "REJECT"}
    prova = json.loads((tmp / "caso_02" / "attempts" / "attempt_001.json").read_text())["proof_attempt"]
    assert prova == "prova con il caso r=0 saltato"
    # niente nel caso rivela la categoria
    contenuti = " ".join(p.read_text() for p in (tmp / "caso_02").rglob("*") if p.is_file())
    assert "caso_mancante" not in contenuti and "salta r=0" not in contenuti


def test_classificazione_e_tabella():
    banco = carica_banco(Path(tempfile.mkdtemp(prefix="pp_banco_")))
    assert banco.classifica("PASS", "PASS", "A") == "ok"
    assert banco.classifica("PASS", "FAIL", "A") == "falso_rifiutato"
    assert banco.classifica("FAIL", "PASS", "A") == "falso_accettato"
    assert banco.classifica("REJECT", "READY_FOR_HUMAN", "esito") == "falso_accettato"
    assert banco.classifica(None, "PASS", "B") is None                  # giudice non in causa
    assert banco.classifica("FAIL", "UNAVAILABLE", "A") is None         # nessun verdetto: non si conta
    etichette = {"caso_01": {"categoria": "corretta", "atteso": banco.atteso_per("corretta")},
                 "caso_02": {"categoria": "citazione_inventata", "atteso": banco.atteso_per("citazione_inventata")}}
    righe = [{"caso": "caso_01", "A": "PASS", "B": "PASS", "esito": "READY_FOR_HUMAN"},
             {"caso": "caso_02", "A": "PASS", "B": "PASS", "esito": "READY_FOR_HUMAN"},
             {"caso": "caso_02", "A": "PASS", "B": "FAIL", "esito": "REJECT"}]
    t = banco.conteggi(righe, etichette)
    assert t["A"]["corretta"]["ok"] == 1 and "citazione_inventata" not in t["A"]
    assert t["B"]["citazione_inventata"] == {"falso_accettato": 1, "ok": 1}
    assert t["esito"]["citazione_inventata"]["falso_accettato"] == 1


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)

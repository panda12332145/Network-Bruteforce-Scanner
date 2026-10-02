"""Testes do Network-Bruteforce-Scanner (sem rede externa)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service_checker import SERVICES, is_port_open, DEFAULT_USERS, DEFAULT_PASSWORDS
from src.nmap_engine import Colors


def test_services_map():
    assert SERVICES["ssh"] == 22
    assert SERVICES["ftp"] == 21
    assert len(SERVICES) >= 8


def test_wordlists_are_lab_defaults():
    # apenas credenciais genéricas de laboratório (nada pessoal)
    assert "admin" in DEFAULT_USERS and "123456" in DEFAULT_PASSWORDS
    assert all(len(p) <= 12 for p in DEFAULT_PASSWORDS)


def test_is_port_open_local():
    # porta fechada em localhost → False (sem rede externa)
    assert is_port_open("127.0.0.1", 1, timeout=0.5) is False


def test_scan_rejects_invalid_target():
    from src.main import scan
    # Alvo inválido/injetado deve morrer na validação, ANTES de input()/subprocesso.
    # stdin está fechado: se chegar em input(), levanta EOFError e o teste falha.
    scan("127.0.0.1; rm -rf /")
    scan("banana")


def test_colors_defined():
    assert Colors.OK and Colors.END


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")

import ipaddress

from .service_checker import is_port_open, check_ssh, check_ftp, SERVICES
from .nmap_engine import run_nmap, Colors


def scan(ip: str):
    """Função principal: Nmap + verificação de porta + bruteforce."""
    ip = ip.strip()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"{Colors.FAIL}[!] IP inválido: {ip!r} — informe um IPv4/IPv6 válido.{Colors.END}")
        return
    if input(f"⚠️  Confirme alvo LABORATÓRIO autorizado ({ip}) [digite 'sim']: ").strip().lower() != "sim":
        print(f"{Colors.WARN}Cancelado.{Colors.END}")
        return
    run_nmap(ip)
    print(f"\n{Colors.BLUE}{'─'*50}{Colors.END}")
    print(f"{Colors.BOLD}🔎 Verificando portas: {ip}{Colors.END}\n")

    open_ports = []
    for service, port in SERVICES.items():
        if is_port_open(ip, port):
            print(f"{Colors.OK}[ABERTA] {port}/{service}{Colors.END}")
            open_ports.append((service, port))
        else:
            print(f"{Colors.FAIL}[FECHADA] {port}/{service}{Colors.END}")

    print(f"\n{Colors.BOLD}🔑 Tentando bruteforce nas portas abertas...{Colors.END}")
    for service, port in open_ports:
        if service == 'ssh':
            ok, cred = check_ssh(ip, port)
            _report(service, port, ok, cred)
        elif service == 'ftp':
            ok, cred = check_ftp(ip, port)
            _report(service, port, ok, cred)


def _report(service, port, ok, cred):
    if ok:
        print(f"{Colors.OK}✓ {service.upper()}:{port} → {cred}{Colors.END}")
    else:
        print(f"{Colors.FAIL}✗ {service.upper()}:{port} → Sem credenciais válidas{Colors.END}")


if __name__ == "__main__":
    target = input("IP alvo: ")
    scan(target)

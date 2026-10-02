import subprocess
import tempfile
import os


class Colors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def run_nmap(ip: str):
    """Executa varredura Nmap de serviços e vulnerabilidades."""
    import shutil
    if not shutil.which("nmap"):
        print(f"{Colors.WARN}[!] Nmap não encontrado — instale com: sudo apt install nmap{Colors.END}")
        return
    print(f"{Colors.BLUE}🔍 Iniciando Nmap em {ip}...{Colors.END}")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as scan_f, \
         tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as vuln_f:
        scan_path, vuln_path = scan_f.name, vuln_f.name

    try:
        res = subprocess.run(
            ['nmap', '-p', '21,22,23,80,445,3306,3389,5900', '-T4', '-sV', ip],
            capture_output=True, text=True
        )
        with open(scan_path, 'w') as f:
            f.write(res.stdout)

        vuln = subprocess.run(['nmap', '--script', 'vuln', ip], capture_output=True, text=True)
        with open(vuln_path, 'w') as f:
            f.write(vuln.stdout)

        _print_results(scan_path)
        _print_results(vuln_path, highlight="VULNERABLE")
    finally:
        os.remove(scan_path)
        os.remove(vuln_path)


def _print_results(path: str, highlight: str = None):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or "Nmap" in line:
                continue
            if highlight and highlight in line:
                print(f"{Colors.FAIL}{line}{Colors.END}")
            elif 'open' in line:
                print(f"{Colors.WARN}{line}{Colors.END}")
            else:
                print(line)

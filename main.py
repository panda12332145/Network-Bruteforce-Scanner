#!/usr/bin/env python3
from src.main import scan
import sys

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("IP alvo: ").strip()
    scan(target)

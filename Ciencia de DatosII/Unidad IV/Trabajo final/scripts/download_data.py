"""Descarga el dataset UCI 697 y verifica su SHA-256 antes de extraerlo."""
from __future__ import annotations

import hashlib
import io
import sys
import zipfile

import requests

from tutoria_dss.config import DATA_PATH, DATA_SHA256, DATA_URL


def main() -> int:
    content = requests.get(DATA_URL, timeout=60).content
    digest = hashlib.sha256(content).hexdigest()
    if digest != DATA_SHA256:
        print(f"SHA-256 inesperado: {digest}", file=sys.stderr)
        return 3
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(content)) as bundle:
        DATA_PATH.write_bytes(bundle.read("data.csv"))
    print(f"SHA-256 verificado: {digest}\nGuardado: {DATA_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

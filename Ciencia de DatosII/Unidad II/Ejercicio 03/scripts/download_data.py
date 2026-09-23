from __future__ import annotations

import io
import sys
import zipfile

import pandas as pd
import requests

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import sha256


def main() -> int:
    if settings.data_source == "local":
        print(f"Modo local. Archivo configurado: {settings.dataset_path}")
        return 0
    if settings.data_source != "url" or not settings.dataset_url:
        print("Configure DATA_SOURCE=url y DATASET_URL en .env", file=sys.stderr)
        return 2
    raw = ROOT / "data/raw"
    raw.mkdir(parents=True, exist_ok=True)
    archive = raw / "sms_spam_collection.zip"
    if not archive.exists():
        response = requests.get(settings.dataset_url, timeout=60)
        response.raise_for_status()
        archive.write_bytes(response.content)
    digest = sha256(archive)
    if digest != settings.dataset_sha256:
        archive.unlink()
        print(f"SHA-256 inesperado: {digest}. Se eliminó la descarga.", file=sys.stderr)
        return 3
    with zipfile.ZipFile(archive) as bundle:
        content = bundle.read("SMSSpamCollection").decode("utf-8")
    rows = [line.split("\t", 1) for line in content.splitlines() if line.strip()]
    df = pd.DataFrame(rows, columns=[settings.target_column, settings.text_column])
    df.insert(0, "id", range(len(df)))
    df = df[["id", settings.text_column, settings.target_column]]
    df.to_csv(settings.dataset_path, index=False)
    print(f"Archivo ZIP verificado. SHA-256: {digest}")
    print(f"Guardado: {settings.dataset_path} · {len(df)} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

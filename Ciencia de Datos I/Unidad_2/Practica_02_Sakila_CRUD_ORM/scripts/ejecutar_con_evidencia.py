#!/usr/bin/env python3
"""Ejecuta un comando interactivo y guarda una evidencia local sanitizada."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import secrets
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "evidencias_locales"
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|pwd|token|secret|api[_-]?key)(\s*[:=]\s*)([^\s]+)"
)
MYSQL_PASSWORD = re.compile(r"(?<!\w)-p(?!\s)([^\s]+)")
MACOS_USER_PATH = re.compile(r"/Users/[^/\s]+")
LINUX_USER_PATH = re.compile(r"/home/[^/\s]+")
WINDOWS_USER_PATH = re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+")
PYTHON_INSTALL_PATH = re.compile(
    r"(?:/Library/Frameworks/Python\.framework|/usr/local/lib|/usr/lib|"
    r"[A-Z]:\\Program Files\\Python[^\\\s]*)[^\s\"']*",
    re.IGNORECASE,
)


def sanitize(text: str) -> str:
    text = ANSI_ESCAPE.sub("", text)
    text = SECRET_ASSIGNMENT.sub(r"\1\2[REDACTED]", text)
    text = MYSQL_PASSWORD.sub("-p[REDACTED]", text)

    replacements = [
        (str(ROOT), "<PROJECT_ROOT>"),
        (str(Path.home()), "<HOME>"),
    ]
    for original, replacement in sorted(replacements, key=lambda item: len(item[0]), reverse=True):
        if original:
            text = text.replace(original, replacement)

    text = MACOS_USER_PATH.sub("<HOME>", text)
    text = LINUX_USER_PATH.sub("<HOME>", text)
    text = WINDOWS_USER_PATH.sub("<HOME>", text)
    text = PYTHON_INSTALL_PATH.sub("<PYTHON_INSTALL>", text)

    for name, value in os.environ.items():
        if value and any(marker in name.upper() for marker in ("PASSWORD", "TOKEN", "SECRET", "API_KEY")):
            text = text.replace(value, "[REDACTED]")
    return text


def evidence_path(output_dir: Path) -> Path:
    timestamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    random_id = secrets.token_hex(4)
    return output_dir / f"ejecucion_{timestamp}_{random_id}.log"


def run_with_pty(command: list[str]) -> tuple[int, bytes]:
    import pty

    chunks: list[bytes] = []

    def capture(master_fd: int) -> bytes:
        chunk = os.read(master_fd, 4096)
        chunks.append(chunk)
        return chunk

    status = pty.spawn(command, master_read=capture)
    return os.waitstatus_to_exitcode(status), b"".join(chunks)


def run_without_pty(command: list[str]) -> tuple[int, bytes]:
    completed = subprocess.run(command, capture_output=True, check=False)
    output = completed.stdout + completed.stderr
    sys.stdout.buffer.write(output)
    sys.stdout.buffer.flush()
    return completed.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta un comando y guarda su salida en evidencias_locales/."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directorio local para los registros.",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("debe indicar un comando despues de --")

    try:
        if os.name == "posix":
            return_code, raw_output = run_with_pty(command)
        else:
            return_code, raw_output = run_without_pty(command)
    except FileNotFoundError:
        print(f"Error: no se encontro el comando {command[0]!r}.", file=sys.stderr)
        return 127

    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_path(args.output_dir)
    decoded_output = raw_output.decode("utf-8", errors="replace")
    header = (
        f"Fecha: {dt.datetime.now().astimezone().isoformat()}\n"
        f"Comando: {' '.join(command)}\n"
        f"Codigo de salida: {return_code}\n\n"
    )
    path.write_text(sanitize(header + decoded_output), encoding="utf-8")
    try:
        display_path = path.relative_to(ROOT)
    except ValueError:
        display_path = Path("<LOCAL_OUTPUT>") / path.name
    print(f"\nEvidencia local guardada en: {display_path}")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())

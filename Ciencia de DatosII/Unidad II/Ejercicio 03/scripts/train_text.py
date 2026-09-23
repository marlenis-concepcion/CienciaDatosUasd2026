from __future__ import annotations

from inf8239_u02.experiment import run


def main() -> None:
    out = run()
    print("Deduplicación:", out["dedup"])
    print("Particiones:", out["splits"])
    print(out["cv"].to_string(index=False))
    print("Decisión:", out["decision"])
    print(out["results"].round(4).to_string(index=False))
    print(f"Errores para análisis: {len(out['errors'])}")
    print("Artefactos guardados en reports/ y models/")


if __name__ == "__main__":
    main()

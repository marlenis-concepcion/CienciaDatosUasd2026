from __future__ import annotations

import json

from inf8239_u03.experiment import run


def main() -> None:
    out = run()
    print(json.dumps(out["partition"], indent=2, ensure_ascii=False))
    for key in ["grid", "valid", "test", "cold", "by_activity", "examples"]:
        print(f"\n== {key}\n", out[key].round(4).to_string(index=False))
    print("\nDecisión:", out["decision"]["razon"])
    print(json.dumps(out["extra"], indent=2))


if __name__ == "__main__":
    main()

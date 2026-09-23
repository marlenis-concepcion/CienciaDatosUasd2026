from __future__ import annotations

import argparse
import json

from inf8239_u02_cv.experiment import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=30)
    args = parser.parse_args()
    out = run(epochs=args.epochs)
    print("Decisión:", out["decision"])
    print(json.dumps(out["metrics"], indent=2, ensure_ascii=False))
    print(out["per_class"].round(3).to_string(index=False))
    print(out["confusions"].to_string(index=False))


if __name__ == "__main__":
    main()

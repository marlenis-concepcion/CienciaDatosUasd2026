from __future__ import annotations

import argparse
import json

from inf8239_u03_gen.experiment import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs-ae", type=int, default=30)
    parser.add_argument("--epochs-vae", type=int, default=40)
    args = parser.parse_args()
    out = run(args.epochs_ae, args.epochs_vae)
    print(out["reconstruction"].round(4).to_string(index=False))
    print(json.dumps({k: v for k, v in out["generation"].items()}, indent=2))
    print("Decisión:", out["decision"]["razon"])


if __name__ == "__main__":
    main()

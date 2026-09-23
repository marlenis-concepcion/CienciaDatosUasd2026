import argparse
from pathlib import Path

from src.config import ProjectConfig
from src.pipeline import OULADProject


def parse_args():
    parser = argparse.ArgumentParser(description="Proyecto final ML sobre OULAD.")
    parser.add_argument("--synthetic-only", action="store_true")
    parser.add_argument("--sample-size", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    root = Path(__file__).resolve().parent
    config = ProjectConfig(
        root=root,
        synthetic_only=args.synthetic_only,
        sample_size=args.sample_size,
    )
    metrics = OULADProject(config).run()
    print(metrics.round(4).to_string(index=False))


if __name__ == "__main__":
    main()

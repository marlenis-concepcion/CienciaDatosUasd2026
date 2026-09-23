import sys

from inf8239_u03.config import MOVIELENS_URL, ROOT
from inf8239_u03.data import download_zip

EXPECTED_SHA256 = "696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436"

destination, digest = download_zip(MOVIELENS_URL, ROOT / "data/raw")
print("Destino:", destination)
print("SHA-256:", digest)
if digest != EXPECTED_SHA256:
    print(f"SHA-256 distinto del registrado ({EXPECTED_SHA256}); los resultados pueden no coincidir.", file=sys.stderr)
    sys.exit(3)

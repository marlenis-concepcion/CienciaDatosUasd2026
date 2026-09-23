import json

from tutoria_dss.config import ROOT
from tutoria_dss.data import audit, load

summary = audit(load())
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/auditoria.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(summary, indent=2, ensure_ascii=False))

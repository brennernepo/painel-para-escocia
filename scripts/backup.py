"""Copia as tabelas do Supabase para backup/. Roda todo dia pelo GitHub Actions (e a leitura diária também evita
que o projeto gratuito do Supabase seja pausado por falta de uso).

    python scripts/backup.py
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from banco import _ler_tabela  # noqa: E402

for tabela in ("avaliacoes", "bandas_usuario"):
    linhas = sorted(_ler_tabela(tabela), key=lambda l: l.get("album_id") or l.get("banda_id"))
    (RAIZ / "backup" / f"{tabela}.json").write_text(json.dumps(linhas, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
    print(f"{tabela}: {len(linhas)} linhas")

"""Separa as bandas sem textos em português em lotes enxutos (sem faixas), para escrever bio e curiosidades.

    python scripts/preparar_lotes.py PASTA_DE_SAIDA [BANDAS_POR_LOTE]

Cada lote é uma lista de bandas com id, nome, país, anos, gêneros, resumos da Wikipedia e, por álbum, id, título,
ano e o resumo do artigo do álbum. O resultado de cada banda vai para textos/<id>.json (formato em catalogo.py).
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main(saida: str, por_lote: int = 36) -> None:
    pasta = Path(saida)
    pasta.mkdir(parents=True, exist_ok=True)
    feitas = {f.stem for f in (RAIZ / "textos").glob("*.json")}
    bandas = []
    for f in sorted((RAIZ / "catalogo").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        if b["id"] in feitas:
            continue
        bandas.append({
            "id": b["id"], "nome": b["nome"], "cena": b["cena"], "pais": b.get("pais"), "inicio": b.get("inicio"),
            "fim": b.get("fim"), "ativa": b.get("ativa"), "generos": b.get("generos"),
            "resumo_pt": b.get("resumo_pt", "")[:1200], "resumo_en": b.get("resumo_en", "")[:1200],
            "albuns": [{"id": a["id"], "titulo": a["titulo"], "ano": a["ano"], "resumo_en": a.get("resumo_en", "")[:600]}
                       for a in b["albuns"]],
        })
    for i in range(0, len(bandas), por_lote):
        n = i // por_lote + 1
        (pasta / f"lote_{n:02d}.json").write_text(json.dumps(bandas[i:i + por_lote], ensure_ascii=False, indent=1),
                                                  encoding="utf-8")
    print(f"{len(bandas)} bandas em {-(-len(bandas) // por_lote)} lotes")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 36)

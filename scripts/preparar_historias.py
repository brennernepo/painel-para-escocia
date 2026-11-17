"""Separa os álbuns sem história escrita em lotes, por prioridade, com o material de pesquisa de cada um.

    python scripts/preparar_historias.py CONTEXTO SAIDA [ALBUNS_POR_LOTE]

CONTEXTO é a pasta gerada por coletar_contexto.py. Ordem: (1) discos de listas famosas e o disco de entrada de cada
banda, (2) o resto das cenas favoritas, (3) todo o resto. Cada lote é uma lista de álbuns com banda, faixas, a
curiosidade já escrita e o material da Wikipedia. O resultado de cada álbum vai para
historias/<banda>/<id do álbum>.json = {"historia": "...", "faixas": {"<n>": "significado"}}.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

NUCLEO = {"Grunge", "Pós-grunge", "Heavy metal clássico e NWOBHM", "Thrash metal", "Groove, death e além", "Hard rock",
          "Nu metal e correlatos", "Clássicos do rock", "Rock brasileiro"}
LIMITE_TEXTO = 170_000  # caracteres de material por lote, para caber folgado no contexto de um agente


def main(contexto: str, saida: str, por_lote: int = 30) -> None:
    from catalogo import carregar  # importa aqui: o catálogo usa o cache do Streamlit
    bandas = carregar("")
    pasta_ctx, pasta = Path(contexto), Path(saida)
    pasta.mkdir(parents=True, exist_ok=True)
    feitos = {f.stem for f in (RAIZ / "historias").glob("*/*.json")}
    fila = []
    for b in bandas.values():
        for a in b["albuns"]:
            if a["id"] in feitos or a["futuro"]:
                continue
            prioridade = 1 if (a.get("listas") or a["id"] == b.get("porta_de_entrada")) else 2 if b["cena"] in NUCLEO else 3
            fila.append((prioridade, b["nome"].lower(), a.get("data") or "", b, a))
    fila.sort(key=lambda x: x[:3])
    lotes, atual, tamanho = [], [], 0
    for prioridade, _, _, b, a in fila:
        ctx_arq = pasta_ctx / f"{a['id']}.json"
        ctx = json.loads(ctx_arq.read_text(encoding="utf-8")) if ctx_arq.exists() else {}
        item = {"id": a["id"], "banda_id": b["id"], "banda": b["nome"], "titulo": a["titulo"], "ano": a["ano"],
                "prioridade": prioridade, "faixas": [{"n": f["n"], "titulo": f["titulo"]} for f in a["faixas"]],
                "curiosidade_atual": a.get("curiosidade") or "", "artigo_wikipedia": ctx.get("artigo", ""),
                "musicas_com_artigo": ctx.get("musicas", {})}
        peso = len(json.dumps(item, ensure_ascii=False))
        if atual and (len(atual) >= por_lote or tamanho + peso > LIMITE_TEXTO):
            lotes.append(atual)
            atual, tamanho = [], 0
        atual.append(item)
        tamanho += peso
    if atual:
        lotes.append(atual)
    for i, lote in enumerate(lotes, 1):
        (pasta / f"lote_{i:03d}.json").write_text(json.dumps(lote, ensure_ascii=False, indent=1), encoding="utf-8")
    por_prioridade = {p: sum(1 for x in fila if x[0] == p) for p in (1, 2, 3)}
    print(f"{len(fila)} álbuns em {len(lotes)} lotes; por prioridade: {por_prioridade}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30)

"""Listas famosas em que cada álbum aparece (com a posição) e prêmios de cada banda.

- Listas: séries do MusicBrainz (Rolling Stone 500, 1001 Discos, listas de metal e grunge...). Uma consulta por
  lista traz todos os álbuns dela com a posição.
- Prêmios: Wikidata (Hall da Fama do Rock e Grammys), pelo QID de cada banda do catálogo.

    python scripts/listas_e_premios.py

Saída: extras.json, mesclado pelo app (catalogo.py). As respostas ficam em .cache/.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_catalogo import RAIZ, baixar, mb  # noqa: E402

# id da série no MusicBrainz → nome curto que aparece no app
LISTAS = {
    "bb3d9d84-75b8-4e67-8ad7-dcc38f764bf3": "Rolling Stone 500",
    "4bc2a338-e1d8-4546-8a61-640da8aaf888": "1001 Discos",
    "d5471f85-4b54-45da-9de7-c9ad9843c4bd": "Rolling Stone 100 do metal",
    "5f94b783-4aec-4e62-83a4-29644e457d90": "Rolling Stone 50 do grunge",
    "08680475-5910-4454-bf74-c8a317366f9e": "Rolling Stone 40 do punk",
    "d1d985e6-94ea-4c68-a7ac-63b98b6c0318": "Apple Music 100",
    "acf170fe-b358-4140-9e32-93a9c7afa544": "The Guardian 100",
}
HALL_DA_FAMA = "Q179191"  # Rock and Roll Hall of Fame


def listas() -> dict:
    por_album = defaultdict(list)
    for serie, nome in LISTAS.items():
        res = mb(f"series/{serie}", inc="release-group-rels") or {}
        for r in res.get("relations", []):
            if r.get("target-type") != "release_group" and "release_group" not in r:
                continue
            numero = (r.get("attribute-values") or {}).get("number")
            por_album[r["release_group"]["id"]].append(
                {"lista": nome, "posicao": int(numero) if numero and numero.isdigit() else None})
        print(f"{nome}: {len(res.get('relations', []))} álbuns", flush=True)
    return por_album


def premios(qids: dict) -> dict:
    """qids: QID → id da banda. Devolve, por banda, o ano de entrada no Hall da Fama e o número de Grammys."""
    saida = defaultdict(dict)
    lista = sorted(qids)
    for i in range(0, len(lista), 60):
        valores = " ".join(f"wd:{q}" for q in lista[i:i + 60])
        consulta = f"""SELECT ?banda ?premio ?premioLabel ?data WHERE {{
          VALUES ?banda {{ {valores} }}
          ?banda p:P166 ?st. ?st ps:P166 ?premio.
          OPTIONAL {{ ?st pq:P585 ?data. }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}"""
        res = baixar("https://query.wikidata.org/sparql", {"query": consulta, "format": "json"}, intervalo=1.0) or {}
        grammys = defaultdict(set)
        for l in res.get("results", {}).get("bindings", []):
            banda = qids[l["banda"]["value"].rsplit("/", 1)[-1]]
            premio = l["premio"]["value"].rsplit("/", 1)[-1]
            rotulo = l.get("premioLabel", {}).get("value", "")
            ano = l.get("data", {}).get("value", "")[:4] or None
            if premio == HALL_DA_FAMA:
                saida[banda]["hall_da_fama"] = int(ano) if ano else True
            elif rotulo.startswith("Grammy Award for") or rotulo.startswith("Latin Grammy Award for"):
                grammys[banda].add((premio, ano))
        for banda, g in grammys.items():
            saida[banda]["grammys"] = len(g)
    return saida


def main() -> None:
    qids = {}
    for f in (RAIZ / "catalogo").glob("*.json"):
        b = json.loads(f.read_text(encoding="utf-8"))
        if b.get("wikidata"):
            qids[b["wikidata"]] = b["id"]
    extras = {"albuns": listas(), "bandas": premios(qids)}
    (RAIZ / "extras.json").write_text(json.dumps(extras, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    print(f"OK: {len(extras['albuns'])} álbuns em listas, {len(extras['bandas'])} bandas com prêmios", flush=True)


if __name__ == "__main__":
    main()

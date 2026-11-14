"""Filtra uma lista de nomes (marcadores de um blog, por exemplo) e mantém só artistas de rock e metal, pela Wikidata.

    python scripts/filtrar_acervo.py nomes.json saida.txt

nomes.json é uma lista de strings. A saída sai no formato de bandas.txt (Nome | gênero principal), em ordem
de notoriedade (número de Wikipedias com artigo), sem as bandas que já estão em bandas.txt.
"""

import json
import re
import sys
from pathlib import Path

from montar_catalogo import RAIZ, baixar, ler_lista, slug

FAMILIA = ("rock", "metal", "punk", "grunge", "hardcore", "psychedelic", "progressive", "new wave", "post-punk",
           "stoner", "doom", "industrial", "garage", "shoegaze", "rockabilly", "krautrock", "glam")
ARTISTA = {"Q215380", "Q5741069", "Q2088357", "Q9212979", "Q5"}  # banda, banda de rock, grupo musical, dupla, pessoa


def wd(params: dict) -> dict:
    return baixar("https://www.wikidata.org/w/api.php", {**params, "format": "json"}, intervalo=0.25) or {}


def candidatos(nome: str) -> list[str]:
    res = wd({"action": "wbsearchentities", "search": nome, "language": "pt", "uselang": "pt", "type": "item", "limit": 5})
    return [r["id"] for r in res.get("search", []) if slug(r.get("label", "")) == slug(nome)]


def main(entrada: str, saida: str) -> None:
    nomes = [n for n in json.loads(Path(entrada).read_text(encoding="utf-8"))
             if not re.fullmatch(r"[\d.]+", n) and "..." not in n and "�" not in n and len(n) > 1]
    ja = {slug(b["nome"]) for b in ler_lista(RAIZ / "bandas.txt")}
    achados = {}
    for i, nome in enumerate(nomes, 1):
        if slug(nome) in ja:
            continue
        ids = candidatos(nome)
        if ids:
            achados[nome] = ids
        if i % 100 == 0:
            print(f"{i}/{len(nomes)} nomes · {len(achados)} com item na Wikidata", flush=True)
    todos = sorted({q for ids in achados.values() for q in ids})
    entidades = {}
    for i in range(0, len(todos), 50):
        entidades.update(wd({"action": "wbgetentities", "ids": "|".join(todos[i:i + 50]), "props": "claims|sitelinks"})
                         .get("entities", {}))

    def valores(ent, prop):
        return [c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") for c in ent.get("claims", {}).get(prop, [])]

    generos = sorted({g for e in entidades.values() for g in valores(e, "P136") if g})
    rotulo = {}
    for i in range(0, len(generos), 50):
        for q, e in wd({"action": "wbgetentities", "ids": "|".join(generos[i:i + 50]), "props": "labels",
                        "languages": "en"}).get("entities", {}).items():
            rotulo[q] = e.get("labels", {}).get("en", {}).get("value", "")
    linhas = []
    for nome, ids in achados.items():
        for q in ids:
            e = entidades.get(q, {})
            if not set(valores(e, "P31")) & ARTISTA:
                continue
            gs = [rotulo.get(g, "") for g in valores(e, "P136")]
            rock = [g for g in gs if any(f in g.lower() for f in FAMILIA)]
            if rock:
                linhas.append((len(e.get("sitelinks", {})), nome, rock[0]))
                break
    linhas.sort(reverse=True)
    Path(saida).write_text("\n".join(f"{n} | {g}" for _, n, g in linhas) + "\n", encoding="utf-8")
    print(f"OK: {len(linhas)} artistas de rock/metal em {saida}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

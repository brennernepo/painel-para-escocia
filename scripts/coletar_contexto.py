"""Junta o material de pesquisa de cada disco para escrever a história do álbum e o significado das faixas.

Para cada álbum do catálogo:
- o artigo completo do disco na Wikipedia (inglês; português para os discos brasileiros sem artigo em inglês),
  limpo do código wiki e só com as seções que contam a história (contexto, gravação, composição, faixas, recepção);
- a introdução do artigo de cada música do disco que tenha artigo próprio (pela lista de faixas da Wikidata).

    python scripts/coletar_contexto.py SAIDA

Grava SAIDA/<id do álbum>.json com {"artigo": "...", "musicas": {"Título": "resumo"}}. As respostas ficam em
.cache/. Os textos da Wikipedia servem só de fonte para os agentes; não vão para o app.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_catalogo import RAIZ, baixar, resumos  # noqa: E402

SECOES_UTEIS = ("background", "recording", "production", "composition", "music", "lyric", "song", "theme", "concept",
                "writing", "release", "artwork", "cover", "packaging", "title", "legacy", "reception", "content",
                "style", "history", "development", "contexto", "gravação", "produção", "composição", "faixas",
                "lançamento", "capa", "repercussão", "legado", "história", "temas", "letras")
SECOES_INUTEIS = ("track listing", "personnel", "charts", "certifications", "references", "external links",
                  "release history", "notes", "sources", "further reading", "accolades", "lista de faixas",
                  "créditos", "ficha técnica", "referências", "ligações externas", "paradas", "certificações")


def limpar_wikitexto(txt: str) -> str:
    """Código wiki → texto corrido (bom o bastante para leitura, sem referências nem predefinições)."""
    txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
    txt = re.sub(r"<ref[^>]*/>", "", txt)
    txt = re.sub(r"<ref[^>]*>.*?</ref>", "", txt, flags=re.S)
    for _ in range(6):  # predefinições aninhadas {{...}}
        novo = re.sub(r"\{\{[^{}]*\}\}", "", txt)
        if novo == txt:
            break
        txt = novo
    txt = re.sub(r"\{\|.*?\|\}", "", txt, flags=re.S)  # tabelas
    txt = re.sub(r"\[\[(?:File|Image|Arquivo|Imagem|Ficheiro):[^\[\]]*(?:\[\[[^\]]*\]\][^\[\]]*)*\]\]", "", txt, flags=re.I)
    txt = re.sub(r"\[\[Category:[^\]]*\]\]|\[\[Categoria:[^\]]*\]\]", "", txt, flags=re.I)
    txt = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", txt)
    txt = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", txt)
    txt = re.sub(r"\[https?://\S+\]", "", txt)
    txt = re.sub(r"'{2,}", "", txt)
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


def secoes_relevantes(wikitexto: str, limite: int = 7000) -> str:
    """Introdução e as seções que contam a história do disco; corta listas de faixas, créditos e paradas."""
    partes = re.split(r"\n(==+)\s*([^=\n]+?)\s*\1\s*\n", "\n" + wikitexto)
    saida = [limpar_wikitexto(partes[0])]
    i, incluir = 1, True
    while i + 1 < len(partes):  # partes = [introdução, nível, título, corpo, nível, título, corpo, ...]
        nivel, titulo = partes[i], partes[i + 1]
        corpo = partes[i + 2] if i + 2 < len(partes) else ""
        if len(nivel) == 2:  # a seção de primeiro nível decide se ela e as subseções entram
            incluir = not any(x in titulo.lower() for x in SECOES_INUTEIS)
        if incluir:
            limpo = limpar_wikitexto(corpo)
            if limpo:
                saida.append(f"## {titulo}\n{limpo}")
        i += 3
    texto = "\n\n".join(s for s in saida if s)
    return texto[:limite]


def wikitextos(titulos: list[str], lang: str) -> dict:
    saida = {}
    for i in range(0, len(titulos), 50):
        lote = titulos[i:i + 50]
        res = baixar(f"https://{lang}.wikipedia.org/w/api.php", {
            "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main", "redirects": 1,
            "titles": "|".join(lote), "format": "json", "formatversion": 2,
        }, intervalo=0.3) or {}
        q = res.get("query", {})
        volta = {r["to"]: r["from"] for r in q.get("redirects", []) + q.get("normalized", [])}
        for p in q.get("pages", []):
            texto = ((p.get("revisions") or [{}])[0].get("slots", {}).get("main", {}).get("content", ""))
            original = volta.get(p.get("title"), p.get("title"))
            saida[volta.get(original, original)] = texto
    return saida


def musicas_com_artigo(rgids: list[str]) -> dict:
    """rgid → {título da faixa na Wikipedia: título do artigo}, pela lista de faixas (P658) da Wikidata."""
    saida = {}
    for i in range(0, len(rgids), 80):
        valores = " ".join(f'"{r}"' for r in rgids[i:i + 80])
        consulta = f"""SELECT ?rgid ?artigo WHERE {{
          VALUES ?rgid {{ {valores} }}
          ?album wdt:P436 ?rgid; wdt:P658 ?musica.
          ?a schema:about ?musica; schema:isPartOf <https://en.wikipedia.org/>; schema:name ?artigo.
        }}"""
        res = baixar("https://query.wikidata.org/sparql", {"query": consulta, "format": "json"}, intervalo=1.0) or {}
        for l in res.get("results", {}).get("bindings", []):
            saida.setdefault(l["rgid"]["value"], []).append(l["artigo"]["value"])
    return saida


def main(destino: str) -> None:
    pasta = Path(destino)
    pasta.mkdir(parents=True, exist_ok=True)
    albuns = []
    for f in sorted((RAIZ / "catalogo").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        for a in b["albuns"]:
            titulo = unquote(a["wikipedia"].rsplit("/wiki/", 1)[1]).replace("_", " ") if a.get("wikipedia") else None
            albuns.append((a["id"], titulo))
    titulos = sorted({t for _, t in albuns if t})
    print(f"{len(albuns)} álbuns, {len(titulos)} com artigo em inglês", flush=True)
    textos = wikitextos(titulos, "en")
    musicas = musicas_com_artigo([rg for rg, _ in albuns])
    todos_artigos = sorted({m for lista in musicas.values() for m in lista})
    print(f"{len(todos_artigos)} músicas com artigo próprio", flush=True)
    intros = resumos(todos_artigos, "en")
    feitos = 0
    for rg, titulo in albuns:
        artigo = secoes_relevantes(textos.get(titulo, "")) if titulo else ""
        musica = {m: (intros.get(m, {}).get("texto") or "")[:900] for m in musicas.get(rg, [])}
        musica = {m: t for m, t in musica.items() if t}
        if artigo or musica:
            (pasta / f"{rg}.json").write_text(json.dumps({"artigo": artigo, "musicas": musica}, ensure_ascii=False),
                                             encoding="utf-8")
            feitos += 1
    print(f"OK: material para {feitos} álbuns em {pasta}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])

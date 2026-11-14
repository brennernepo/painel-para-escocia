"""Monta o catálogo a partir de bandas.txt.

Fontes, todas abertas e sem chave:
- MusicBrainz: banda, discografia de estúdio, faixas, datas e nota do público;
- Cover Art Archive: capa de cada álbum;
- Wikidata e Wikipedia: foto, resumo, início/fim da banda e notas da crítica (caixa "Professional ratings").

As respostas ficam em .cache/, então rodar de novo só busca o que é novo. Saída: catalogo/<banda>.json.
Os textos em português (bio e curiosidades) entram depois, em textos/<banda>.json, e são mesclados pelo app.

    python scripts/montar_catalogo.py              # todas as bandas de bandas.txt
    python scripts/montar_catalogo.py --so Nirvana # só uma
    python scripts/montar_catalogo.py --lista outro.txt
"""

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import quote

import requests

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / ".cache"
SAIDA = RAIZ / "catalogo"
UA = {"User-Agent": "discoteca-pessoal/1.0 (+https://github.com/brennernepo/discoteca)"}
MB = "https://musicbrainz.org/ws/2"
PALAVRAS_ROCK = ("rock", "metal", "grunge", "punk", "hardcore", "sludge", "doom", "thrash", "stoner", "psychedelic",
                 "progressive", "blues", "alternative", "garage", "hard rock", "mpb", "brazilian", "industrial")
_ultimo = {}


RENOVAR = False  # --renovar: busca de novo as listas de álbuns, para achar lançamentos novos


def baixar(url: str, params: dict | None = None, intervalo: float = 0.0, tentativas: int = 6,
           fresco: bool = False) -> dict | None:
    """GET com cache em disco e intervalo mínimo por host. Devolve JSON (ou {"_texto": ...}) ou None em 404."""
    chave = hashlib.sha1((url + json.dumps(params or {}, sort_keys=True)).encode()).hexdigest()
    arquivo = CACHE / f"{chave}.json"
    if arquivo.exists() and not fresco:
        return json.loads(arquivo.read_text(encoding="utf-8"))
    host = url.split("/")[2]
    for n in range(tentativas):
        espera = intervalo - (time.time() - _ultimo.get(host, 0))
        if espera > 0:
            time.sleep(espera)
        _ultimo[host] = time.time()
        try:
            r = requests.get(url, params=params, headers=UA, timeout=30)
        except requests.RequestException:
            time.sleep(3 * (n + 1))
            continue
        if r.status_code == 404:
            dados = None
            break
        if r.status_code in (429, 500, 502, 503, 504):  # o MusicBrainz recusa acima de 1 pedido/s: espera curta
            time.sleep(1.5 * (n + 1))
            continue
        r.raise_for_status()
        dados = r.json() if "json" in r.headers.get("content-type", "") else {"_texto": r.text}
        break
    else:
        return None  # sem cache: tenta de novo na próxima rodada
    CACHE.mkdir(exist_ok=True)
    arquivo.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return dados


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def ler_lista(caminho: Path) -> list[dict]:
    bandas, cena = [], "Outros"
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if linha.startswith("[") and linha.endswith("]"):
            cena = linha[1:-1]
            continue
        nome, _, dica = (p.strip() for p in linha.partition("|"))
        bandas.append({"nome": nome, "dica": dica, "cena": cena})
    return bandas


# ---------------------------------------------------------------------------
# MusicBrainz
# ---------------------------------------------------------------------------
def mb(caminho: str, fresco: bool = False, **params) -> dict | None:
    return baixar(f"{MB}/{caminho}", {**params, "fmt": "json"}, intervalo=1.1, fresco=fresco)


def achar_artista(nome: str, dica: str) -> dict | None:
    """Melhor candidato: nome igual, estilo de rock/metal e a dica (país, estilo) batendo com a descrição."""
    res = mb("artist/", query=f'artist:"{nome}"', limit=15) or {}
    alvo = slug(nome)
    melhor, nota_melhor = None, -1
    for c in res.get("artists", []):
        tags = " ".join(t["name"] for t in c.get("tags", [])).lower()
        desc = f'{c.get("disambiguation", "")} {c.get("country", "")} {c.get("type", "")}'.lower()
        nota = int(c.get("score", 0))
        nota += 60 if slug(c["name"]) == alvo else 0
        nota += 40 if any(p in tags or p in desc for p in PALAVRAS_ROCK) else 0
        nota += sum(15 for p in re.findall(r"\w+", dica.lower()) if len(p) > 2 and (p in desc or p in tags))
        nota += min(sum(t.get("count", 0) for t in c.get("tags", [])), 30)
        if nota > nota_melhor:
            melhor, nota_melhor = c, nota
    return melhor


def em_cache(caminho: str, **params) -> dict | None:
    """Resposta do MusicBrainz já guardada em .cache/, sem ir à rede."""
    url, params = f"{MB}/{caminho}", {**params, "fmt": "json"}
    arquivo = CACHE / f"{hashlib.sha1((url + json.dumps(params, sort_keys=True)).encode()).hexdigest()}.json"
    return json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else None


def albuns_de_estudio(mbid: str) -> list[dict]:
    """Discos de estúdio. O filtro release-group-status=website-default já tira os grupos que só têm edições piratas,
    o que poupa uma consulta por pirata (os Beatles caem de 705 grupos para 187). Respostas antigas, guardadas sem o
    filtro, continuam valendo: os piratas delas saem depois, por não terem edição oficial."""
    grupos, offset = [], 0
    while True:
        base = {"artist": mbid, "type": "album", "inc": "ratings", "limit": 100, "offset": offset}
        antiga = None if RENOVAR else em_cache("release-group", **base)
        pag = antiga if antiga is not None else (
            mb("release-group", fresco=RENOVAR, **base, **{"release-group-status": "website-default"}) or {})
        grupos += pag.get("release-groups", [])
        offset += 100
        if offset >= pag.get("release-group-count", 0):
            break
    vistos, albuns = set(), []
    for g in sorted(grupos, key=lambda g: g.get("first-release-date") or "9999"):
        extras = set(g.get("secondary-types") or []) - {"Soundtrack"}  # trilhas da própria banda contam (Help!, Purple Rain)
        if g.get("primary-type") != "Album" or extras or not g.get("first-release-date"):
            continue
        if slug(g["title"]) in vistos:
            continue
        vistos.add(slug(g["title"]))
        albuns.append(g)
    return albuns


def faixas_e_capa(rgid: str) -> tuple[list[dict], str | None]:
    """Faixas da edição oficial mais antiga e a capa (da edição mais antiga que tenha capa)."""
    res = mb("release", **{"release-group": rgid, "status": "official", "inc": "recordings+media", "limit": 25}) or {}
    edicoes = sorted(res.get("releases", []), key=lambda r: (r.get("date") or "9999", -len(r.get("media", []))))
    if not edicoes:
        return [], None
    base = next((e for e in edicoes if any(m.get("tracks") for m in e.get("media", []))), edicoes[0])
    faixas = []
    for m in base.get("media", []):
        for t in m.get("tracks", []):
            faixas.append({"n": len(faixas) + 1, "titulo": t.get("title", ""), "ms": t.get("length")})
    com_capa = next((e for e in edicoes if e.get("cover-art-archive", {}).get("front")), None)
    capa = f"https://coverartarchive.org/release/{com_capa['id']}/front-250" if com_capa else None
    return faixas, capa


# ---------------------------------------------------------------------------
# Wikidata e Wikipedia
# ---------------------------------------------------------------------------
def wikidata_entidades(qids: list[str]) -> dict:
    saida = {}
    for i in range(0, len(qids), 50):
        res = baixar("https://www.wikidata.org/w/api.php", {
            "action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "sitelinks|claims", "format": "json",
        }, intervalo=0.3) or {}
        saida.update(res.get("entities", {}))
    return saida


def ano_da_claim(entidade: dict, prop: str) -> str | None:
    for c in entidade.get("claims", {}).get(prop, []):
        v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
        if isinstance(v, dict) and v.get("time"):
            return v["time"][1:5]
    return None


def albuns_na_wikidata(qids: list[str]) -> dict:
    """rgid do MusicBrainz → títulos dos artigos do álbum na Wikipedia (en e pt) e ids no Spotify e no YouTube."""
    saida = {}
    for i in range(0, len(qids), 15):
        valores = " ".join(f"wd:{q}" for q in qids[i:i + 15])
        consulta = f"""SELECT ?rgid ?en ?pt ?spotify ?youtube WHERE {{
          VALUES ?artista {{ {valores} }}
          ?album wdt:P175 ?artista; wdt:P436 ?rgid.
          OPTIONAL {{ ?a schema:about ?album; schema:isPartOf <https://en.wikipedia.org/>; schema:name ?en. }}
          OPTIONAL {{ ?b schema:about ?album; schema:isPartOf <https://pt.wikipedia.org/>; schema:name ?pt. }}
          OPTIONAL {{ ?album wdt:P2205 ?spotify. }}
          OPTIONAL {{ ?album wdt:P4300 ?youtube. }}
        }}"""
        res = baixar("https://query.wikidata.org/sparql", {"query": consulta, "format": "json"}, intervalo=1.0) or {}
        for linha in res.get("results", {}).get("bindings", []):
            rgid = linha["rgid"]["value"]
            atual = saida.setdefault(rgid, {})
            for campo in ("en", "pt", "spotify", "youtube"):
                if campo in linha:
                    atual.setdefault(campo, linha[campo]["value"])
    return saida


def resumos(titulos: list[str], lang: str) -> dict:
    """Primeiro parágrafo e miniatura de cada artigo, de 20 em 20."""
    saida = {}
    for i in range(0, len(titulos), 20):
        lote = titulos[i:i + 20]
        res = baixar(f"https://{lang}.wikipedia.org/w/api.php", {
            "action": "query", "prop": "extracts|pageimages", "exintro": 1, "explaintext": 1, "exlimit": 20,
            "piprop": "thumbnail", "pithumbsize": 500, "redirects": 1, "titles": "|".join(lote), "format": "json",
        }, intervalo=0.3) or {}
        q = res.get("query", {})
        volta = {r["to"]: r["from"] for r in q.get("redirects", []) + q.get("normalized", [])}
        for p in q.get("pages", {}).values():
            titulo = p.get("title", "")
            original = volta.get(titulo, titulo)
            original = volta.get(original, original)
            saida[original] = {"texto": (p.get("extract") or "").strip(), "foto": p.get("thumbnail", {}).get("source")}
    return saida


NUMERO = r"(\d+(?:[.,]\d+)?)"


def notas_da_critica(wikitexto: str) -> dict:
    """Lê a caixa de avaliações do artigo do álbum: AllMusic e Metacritic, e a média das demais notas."""
    caixa = re.search(r"\{\{\s*(?:Album|Music) ratings(.*?)\n\}\}", wikitexto, re.S | re.I)
    if not caixa:
        return {}
    corpo = caixa.group(1)
    notas, allmusic = [], None
    for num, fonte in re.findall(r"\|\s*rev(\d+)\s*=\s*([^\n|]+)", corpo, re.I):
        valor = re.search(rf"\|\s*rev{num}score\s*=\s*([^\n]+)", corpo, re.I)
        if not valor:
            continue
        v = valor.group(1)
        nota = None
        estrelas = re.search(rf"\{{\{{\s*Rating\s*\|\s*{NUMERO}\s*\|\s*{NUMERO}", v, re.I)
        fracao = re.search(rf"{NUMERO}\s*/\s*{NUMERO}", v)
        if estrelas:
            nota = float(estrelas.group(1).replace(",", ".")) / float(estrelas.group(2).replace(",", ".")) * 10
        elif fracao and float(fracao.group(2).replace(",", ".")) in (5, 10, 100):
            nota = float(fracao.group(1).replace(",", ".")) / float(fracao.group(2).replace(",", ".")) * 10
        if nota is None or not 0 <= nota <= 10:
            continue
        notas.append(nota)
        if "allmusic" in fonte.lower():
            allmusic = nota
    mc = re.search(r"\|\s*MC\s*=\s*[^\n]*?(\d{1,3})\s*/\s*100", corpo)
    saida = {}
    if allmusic is not None:
        saida["allmusic"] = round(allmusic, 1)
    if mc:
        saida["metacritic"] = int(mc.group(1))
    if notas:
        saida["media"] = round(sum(notas) / len(notas), 1)
        saida["fontes"] = len(notas)
    return saida


def wikitextos(titulos: list[str]) -> dict:
    saida = {}
    for i in range(0, len(titulos), 50):
        lote = titulos[i:i + 50]
        res = baixar("https://en.wikipedia.org/w/api.php", {
            "action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main", "redirects": 1,
            "titles": "|".join(lote), "format": "json", "formatversion": 2,
        }, intervalo=0.3) or {}
        q = res.get("query", {})
        volta = {r["to"]: r["from"] for r in q.get("redirects", []) + q.get("normalized", [])}
        for p in q.get("pages", []):
            rev = (p.get("revisions") or [{}])[0]
            texto = rev.get("slots", {}).get("main", {}).get("content", "")
            original = volta.get(p.get("title"), p.get("title"))
            saida[volta.get(original, original)] = texto
    return saida


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------
def ler_antigo(nome: str) -> dict:
    """Ficha já gravada da banda. No --renovar ela poupa a busca do artista e as faixas dos álbuns conhecidos,
    então a rodada semanal no GitHub só consulta as discografias e os álbuns novos."""
    arquivo = SAIDA / f"{slug(nome)}.json"
    return json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {}


def faixas_do_catalogo(album: dict) -> list[dict]:
    def ms(duracao: str | None) -> int | None:
        if not duracao:
            return None
        m, s = duracao.split(":")
        return (int(m) * 60 + int(s)) * 1000
    return [{"n": f["n"], "titulo": f["titulo"], "ms": ms(f.get("duracao"))} for f in album["faixas"]]


def completar(ficha: dict, antigo: dict) -> None:
    """Se a Wikipedia ou a Wikidata falharem nesta rodada, fica o que já se sabia (foto, resumos, notas da crítica)."""
    if not antigo:
        return
    for campo in ("wikidata", "inicio", "fim", "generos", "foto", "wikipedia", "resumo_pt", "resumo_en"):
        if not ficha.get(campo) and antigo.get(campo):
            ficha[campo] = antigo[campo]
    velhos = {a["id"]: a for a in antigo.get("albuns", [])}
    for a in ficha["albuns"]:
        velho = velhos.get(a["id"], {})
        for campo in ("critica", "wikipedia", "resumo_en", "spotify", "youtube"):
            if not a.get(campo) and velho.get(campo):
                a[campo] = velho[campo]


def montar(bandas: list[dict]) -> None:
    SAIDA.mkdir(exist_ok=True)
    fichas = []
    for i, b in enumerate(bandas, 1):
        antigo = ler_antigo(b["nome"]) if RENOVAR else {}
        cand = {"id": antigo["mbid"]} if antigo.get("mbid") else achar_artista(b["nome"], b["dica"])
        if not cand:
            print(f"[{i}/{len(bandas)}] NÃO ACHEI: {b['nome']}", flush=True)
            continue
        art = mb(f"artist/{cand['id']}", inc="url-rels+genres+tags") or {}
        qid = next((r["url"]["resource"].rsplit("/", 1)[-1] for r in art.get("relations", [])
                    if r.get("type") == "wikidata"), None)
        albuns = albuns_de_estudio(cand["id"])
        if antigo and (not art.get("id") or not albuns):  # MusicBrainz fora do ar: não estraga a ficha que já existe
            print(f"[{i}/{len(bandas)}] {b['nome']}: sem resposta, mantida a ficha anterior", flush=True)
            continue
        conhecidos = {a["id"]: a for a in antigo.get("albuns", []) if a.get("faixas")}
        for a in albuns:
            if a["id"] in conhecidos:  # --renovar: faixas e capa de álbuns já catalogados não mudam
                a["_faixas"], a["_capa"] = faixas_do_catalogo(conhecidos[a["id"]]), conhecidos[a["id"]]["capa"]
            else:
                a["_faixas"], a["_capa"] = faixas_e_capa(a["id"])
        fichas.append({**b, "art": art, "qid": qid, "albuns": albuns, "antigo": antigo})
        print(f"[{i}/{len(bandas)}] {b['nome']} → {art.get('name')} ({art.get('disambiguation', '')}) · "
              f"{len(albuns)} álbuns", flush=True)

    qids = [f["qid"] for f in fichas if f["qid"]]
    entidades = wikidata_entidades(qids)
    albuns_wd = albuns_na_wikidata(qids)

    titulo_banda = {}
    for f in fichas:
        links = entidades.get(f["qid"] or "", {}).get("sitelinks", {})
        titulo_banda[f["nome"]] = {lang: links[f"{lang}wiki"]["title"] for lang in ("pt", "en") if f"{lang}wiki" in links}
    res_pt = resumos([t["pt"] for t in titulo_banda.values() if "pt" in t], "pt")
    res_en = resumos([t["en"] for t in titulo_banda.values() if "en" in t], "en")
    titulos_album = sorted({v["en"] for v in albuns_wd.values() if "en" in v})
    res_album = resumos(titulos_album, "en")
    textos_album = wikitextos(titulos_album)

    for f in fichas:
        art, ent = f["art"], entidades.get(f["qid"] or "", {})
        t = titulo_banda[f["nome"]]
        pt, en = res_pt.get(t.get("pt", ""), {}), res_en.get(t.get("en", ""), {})
        vida = art.get("life-span") or {}
        fim = vida.get("end") or ano_da_claim(ent, "P576")
        generos = [g["name"] for g in sorted(art.get("genres", []), key=lambda g: -g.get("count", 0))][:5]
        ficha = {
            "id": slug(f["nome"]), "nome": art.get("name", f["nome"]), "cena": f["cena"], "mbid": art.get("id"),
            "wikidata": f["qid"], "tipo": art.get("type"), "pais": art.get("country") or (art.get("area") or {}).get("name"),
            "inicio": (vida.get("begin") or ano_da_claim(ent, "P571") or "")[:4] or None,
            "fim": (fim or "")[:4] or None,
            "ativa": None if not vida and not fim else not (vida.get("ended") or fim),
            "generos": generos,
            "foto": pt.get("foto") or en.get("foto"),
            "wikipedia": (f"https://pt.wikipedia.org/wiki/{quote(t['pt'].replace(' ', '_'))}" if "pt" in t else
                          f"https://en.wikipedia.org/wiki/{quote(t['en'].replace(' ', '_'))}" if "en" in t else None),
            "resumo_pt": pt.get("texto", "")[:1500], "resumo_en": en.get("texto", "")[:1500],
            "albuns": [],
        }
        for a in f["albuns"]:
            if not a["_faixas"]:  # sem lançamento oficial: pirata
                continue
            wd = albuns_wd.get(a["id"], {})
            notas = notas_da_critica(textos_album.get(wd.get("en", ""), ""))
            faixas = a["_faixas"]
            total = sum(x["ms"] or 0 for x in faixas)
            rating = a.get("rating", {}) or {}
            ficha["albuns"].append({
                "id": a["id"], "titulo": a["title"], "data": a["first-release-date"], "ano": a["first-release-date"][:4],
                "capa": a["_capa"],
                "faixas": [{"n": x["n"], "titulo": x["titulo"],
                            "duracao": f"{x['ms'] // 60000}:{x['ms'] // 1000 % 60:02d}" if x["ms"] else None}
                           for x in faixas],
                "duracao_min": round(total / 60000) if total else None,
                "critica": notas,
                "publico": round(rating["value"] * 2, 1) if rating.get("value") else None,
                "publico_votos": rating.get("votes-count", 0),
                "wikipedia": f"https://en.wikipedia.org/wiki/{quote(wd['en'].replace(' ', '_'))}" if "en" in wd else None,
                "resumo_en": res_album.get(wd.get("en", ""), {}).get("texto", "")[:1200],
                "spotify": wd.get("spotify"), "youtube": wd.get("youtube"),
            })
        completar(ficha, f["antigo"])
        (SAIDA / f"{ficha['id']}.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK: {len(fichas)} bandas gravadas em {SAIDA}", flush=True)


def incluir_pedidos(caminho: Path) -> None:
    """Acrescenta a bandas.txt as bandas pedidas no app (tabela pedidos do Supabase) que ainda não estão na lista."""
    sys.path.insert(0, str(RAIZ))
    from banco import CHAVE, URL  # noqa: E402  (a chave publicável, a mesma do app)
    try:
        r = requests.get(f"{URL}/pedidos", params={"select": "nome", "order": "criado_em"}, headers={"apikey": CHAVE},
                         timeout=30)
        r.raise_for_status()
        pedidos = [p["nome"].strip() for p in r.json()]
    except Exception as erro:  # noqa: BLE001
        print(f"Pedidos: não consegui ler ({erro})", flush=True)
        return
    existentes = {slug(b["nome"]) for b in ler_lista(caminho)}
    novos = list({slug(n): n for n in reversed(pedidos) if n and slug(n) not in existentes}.values())[::-1]
    if novos:
        texto = caminho.read_text(encoding="utf-8").rstrip("\n")
        bloco = "\n\n[Pedidos do app]\n" + "\n".join(novos) + "\n"
        caminho.write_text(texto + bloco, encoding="utf-8")
        print(f"Pedidos incluídos: {', '.join(novos)}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lista", default=str(RAIZ / "bandas.txt"))
    ap.add_argument("--so")
    ap.add_argument("--renovar", action="store_true", help="busca de novo as discografias (álbuns novos)")
    ap.add_argument("--pedidos", action="store_true", help="inclui antes as bandas pedidas no app")
    args = ap.parse_args()
    RENOVAR = args.renovar
    if args.pedidos:
        incluir_pedidos(Path(args.lista))
    lista = ler_lista(Path(args.lista))
    if args.so:
        lista = [b for b in lista if b["nome"].lower() == args.so.lower()]
    montar(lista)
    sys.exit(0)

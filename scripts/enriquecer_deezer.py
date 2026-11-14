"""Acrescenta dados do Deezer a cada banda do catálogo. API pública, sem chave (até 50 pedidos a cada 5 s).

- banda: id no Deezer, número de fãs, foto quadrada (reserva para quando a Wikipedia não tem foto);
- parecidas: artistas relacionados segundo o Deezer (alimentam "Parecidas" e o Descobrir);
- por álbum: id no Deezer (para o player embutido) e uma capa reserva, mais rápida que a do Cover Art Archive.

    python scripts/enriquecer_deezer.py            # todas as bandas de catalogo/
    python scripts/enriquecer_deezer.py --so nirvana

Saída: deezer/<banda>.json, mesclado pelo app (catalogo.py). As respostas ficam em .cache/.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_catalogo import CACHE, RAIZ, UA, slug  # noqa: E402

API = "https://api.deezer.com"
SAIDA = RAIZ / "deezer"
_ultimo = [0.0]


def dz(caminho: str, **params) -> dict:
    """GET no Deezer com cache em disco. Erros de cota (o Deezer responde 200 com {"error": ...}) não vão para o cache."""
    chave = hashlib.sha1((f"{API}/{caminho}" + json.dumps(params, sort_keys=True)).encode()).hexdigest()
    arquivo = CACHE / f"dz_{chave}.json"
    if arquivo.exists():
        return json.loads(arquivo.read_text(encoding="utf-8"))
    for n in range(6):
        espera = 0.12 - (time.time() - _ultimo[0])
        if espera > 0:
            time.sleep(espera)
        _ultimo[0] = time.time()
        try:
            r = requests.get(f"{API}/{caminho}", params=params, headers=UA, timeout=30)
            dados = r.json()
        except (requests.RequestException, ValueError):
            time.sleep(2 * (n + 1))
            continue
        if isinstance(dados, dict) and "error" in dados:
            if dados["error"].get("code") == 800:  # não existe
                dados = {}
                break
            time.sleep(3 * (n + 1))  # cota (código 4) ou instabilidade
            continue
        break
    else:
        return {}
    CACHE.mkdir(exist_ok=True)
    arquivo.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return dados


def imagem(url: str | None) -> str | None:
    """O Deezer devolve uma imagem genérica quando não tem foto ou capa: o caminho vem sem o código da imagem."""
    return url if url and "/artist//" not in url and "/cover//" not in url else None


def titulo_base(titulo: str) -> str:
    """'Nevermind (Deluxe Edition)' e 'Nevermind' viram 'nevermind'; '[Led Zeppelin IV]' vira 'led-zeppelin-iv'."""
    t = titulo.strip()
    while True:
        novo = re.sub(r"\s*[\(\[][^\)\]]*[\)\]]\s*$", "", t)
        if novo == t or not novo:
            break
        t = novo
    t = re.sub(r"\s+-\s+(\d{4}\s+)?(remaster|deluxe|expanded|anniversary|edition|version|mono|stereo).*$", "", t, flags=re.I)
    t = re.sub(r"['’‘`]", "", t).replace("&", " and ")
    return slug(t.strip("[]()")) or slug(titulo)


def albuns_do_artista(artista_id: int) -> list[dict]:
    albuns, indice = [], 0
    while indice < 500:
        pag = dz(f"artist/{artista_id}/albums", limit=100, index=indice)
        albuns += pag.get("data", [])
        if not pag.get("next"):
            break
        indice += 100
    return albuns


def limpo(texto: str) -> str:
    """Aspas e hífens tipográficos do MusicBrainz atrapalham a busca do Deezer."""
    return texto.replace("’", "'").replace("‘", "'").replace("‐", "-").replace("…", "...")


def achar_artista(banda: dict) -> tuple[dict | None, list[dict]]:
    """Fica o artista do Deezer com mais álbuns em comum com o catálogo.

    Candidatos: os homônimos da busca por artista (que ranqueia mal nomes curtos como Queen e Rush) e os donos dos
    álbuns mais conhecidos da banda na busca por álbum (que acha também "KoЯn" e "Jimi Hendrix" para The Jimi
    Hendrix Experience)."""
    nossos = {titulo_base(a["titulo"]) for a in banda["albuns"]}
    nome = limpo(banda["nome"])
    alvo = titulo_base(nome).removeprefix("the-")
    candidatos = {c["id"]: True for c in dz("search/artist", q=nome, limit=25).get("data", [])
                  if titulo_base(c["name"]).removeprefix("the-") == alvo}
    famosos = sorted(banda["albuns"], key=lambda a: -(a.get("publico_votos") or 0))[:3]

    def donos(consulta: str, titulo: str) -> None:
        for x in dz("search/album", q=consulta, limit=8).get("data", []):
            dono = (x.get("artist") or {}).get("id")
            if dono and titulo_base(x["title"]) == titulo_base(titulo):
                candidatos.setdefault(dono, False)  # False: nome diferente, precisa provar com álbuns

    def avaliar() -> tuple[int | None, int, list[dict]]:
        melhor = (None, 0, [])
        for cid, mesmo_nome in list(candidatos.items())[:8]:
            albuns = albuns_do_artista(cid)
            comuns = len(nossos & {titulo_base(a["title"]) for a in albuns})
            minimo = 1 if mesmo_nome or len(nossos) <= 2 else 2
            if comuns >= minimo and comuns > melhor[1]:
                melhor = (cid, comuns, albuns)
        return melhor

    for a in famosos:
        donos(f'artist:"{nome}" album:"{limpo(a["titulo"])}"', a["titulo"])
    melhor, _, albuns = avaliar()
    if melhor is None:  # grafias diferentes (KoЯn, Jimi Hendrix): busca livre pelo nome e pelo título
        for a in famosos:
            donos(f'{nome} {limpo(a["titulo"])}', a["titulo"])
        melhor, _, albuns = avaliar()
    if melhor is None:
        return None, []
    return dz(f"artist/{melhor}"), albuns


def enriquecer(banda: dict) -> dict:
    artista, albuns_dz = achar_artista(banda)
    if not artista:
        return {}
    por_titulo = {}
    for a in sorted(albuns_dz, key=lambda a: (a.get("record_type") != "album", a.get("release_date") or "9999")):
        por_titulo.setdefault(titulo_base(a["title"]), a)
    albuns = {}
    for a in banda["albuns"]:
        achado = por_titulo.get(titulo_base(a["titulo"]))
        if not achado:  # nem sempre o álbum aparece na lista do artista (participações, selos antigos)
            busca = dz("search/album", q=f'artist:"{limpo(banda["nome"])}" album:"{limpo(a["titulo"])}"',
                       limit=5).get("data", [])
            achado = next((x for x in busca if x.get("artist", {}).get("id") == artista["id"]
                           and titulo_base(x["title"]) == titulo_base(a["titulo"])), None)
        if achado:
            albuns[a["id"]] = {"id": achado["id"], "capa": imagem(achado.get("cover_medium"))}
    parecidas = [{"nome": p["name"], "deezer": p["id"], "fas": p.get("nb_fan", 0), "foto": imagem(p.get("picture_medium"))}
                 for p in dz(f"artist/{artista['id']}/related", limit=20).get("data", [])]
    return {"artista": {"id": artista["id"], "fas": artista.get("nb_fan", 0), "foto": imagem(artista.get("picture_big"))},
            "parecidas": parecidas, "albuns": albuns}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--so")
    args = ap.parse_args()
    SAIDA.mkdir(exist_ok=True)
    arquivos = sorted((RAIZ / "catalogo").glob("*.json"))
    if args.so:
        arquivos = [f for f in arquivos if f.stem == args.so]
    sem, total_alb, achados = [], 0, 0
    for i, f in enumerate(arquivos, 1):
        banda = json.loads(f.read_text(encoding="utf-8"))
        dados = enriquecer(banda)
        if not dados:
            sem.append(banda["nome"])
            (SAIDA / f.name).unlink(missing_ok=True)  # não deixa um casamento antigo e errado para trás
            continue
        total_alb += len(banda["albuns"])
        achados += len(dados["albuns"])
        (SAIDA / f.name).write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{i}/{len(arquivos)}] {banda['nome']}: {len(dados['albuns'])}/{len(banda['albuns'])} álbuns, "
              f"{len(dados['parecidas'])} parecidas", flush=True)
    print(f"OK: {len(arquivos) - len(sem)} bandas, {achados}/{total_alb} álbuns no Deezer. Sem artista: {sem}", flush=True)


if __name__ == "__main__":
    main()

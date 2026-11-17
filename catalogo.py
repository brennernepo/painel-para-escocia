"""Leitura do catálogo (catalogo/*.json, gerado por scripts/montar_catalogo.py), dos textos em português
(textos/*.json) e dos dados do Deezer (deezer/*.json, de scripts/enriquecer_deezer.py). Textos e Deezer são
opcionais: sem textos, a bio usa o resumo da Wikipedia; sem Deezer, não há player nem bandas parecidas."""

import hashlib
import json
import os
import re
import unicodedata
from datetime import date
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).parent
PAISES = {"US": "EUA", "GB": "Reino Unido", "BR": "Brasil", "CA": "Canadá", "AU": "Austrália", "DE": "Alemanha",
          "SE": "Suécia", "FR": "França", "IE": "Irlanda", "NL": "Holanda", "FI": "Finlândia", "NO": "Noruega",
          "DK": "Dinamarca", "IT": "Itália", "AR": "Argentina", "JP": "Japão", "BE": "Bélgica", "CH": "Suíça",
          "AT": "Áustria", "PL": "Polônia", "ES": "Espanha", "PT": "Portugal", "MX": "México", "NZ": "Nova Zelândia",
          "XE": "Europa", "XW": "Mundo"}


def primeiros_paragrafos(texto: str, limite: int = 700) -> str:
    """Corta o resumo da Wikipedia no fim de uma frase, perto do limite."""
    texto = re.sub(r"\s+", " ", texto or "").strip()
    if len(texto) <= limite:
        return texto
    corte = texto.rfind(". ", 0, limite)
    return texto[: corte + 1] if corte > 200 else texto[:limite].rsplit(" ", 1)[0] + "…"


def nota_critica(critica: dict) -> float | None:
    """Média das resenhas listadas na Wikipedia; sem ela, AllMusic; sem as duas, Metacritic."""
    if critica.get("media") is not None:
        return critica["media"]
    if critica.get("allmusic") is not None:
        return critica["allmusic"]
    if critica.get("metacritic") is not None:
        return round(critica["metacritic"] / 10, 1)
    return None


def versao_dos_dados() -> str:
    """Impressão digital dos arquivos de dados (nome, tamanho e data). Muda a cada publicação no GitHub, e com ela
    o cache do carregar() se renova na hora, sem esperar o app reiniciar."""
    partes = []
    for pasta in ("catalogo", "textos", "deezer"):
        if (RAIZ / pasta).exists():
            partes += [f"{pasta}/{e.name}:{e.stat().st_size}:{e.stat().st_mtime_ns}" for e in os.scandir(RAIZ / pasta)]
    for raiz, _, arquivos in os.walk(RAIZ / "historias"):
        for nome in arquivos:
            st_ = os.stat(os.path.join(raiz, nome))
            partes.append(f"h/{nome}:{st_.st_size}:{st_.st_mtime_ns}")
    extras = RAIZ / "extras.json"
    if extras.exists():
        partes.append(f"extras:{extras.stat().st_size}:{extras.stat().st_mtime_ns}")
    return hashlib.md5("|".join(sorted(partes)).encode()).hexdigest()


@st.cache_data(show_spinner="Abrindo a discoteca…", ttl="6h", max_entries=2)
def carregar(versao: str = "") -> dict:  # noqa: ARG001  (versao só serve de chave do cache)
    textos = {}
    for f in (RAIZ / "textos").glob("*.json"):
        textos[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    deezer = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in (RAIZ / "deezer").glob("*.json")}
    # história de cada disco e significado das faixas: historias/<banda>/<id do álbum>.json
    historias = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in (RAIZ / "historias").glob("*/*.json")}
    arq_extras = RAIZ / "extras.json"  # listas famosas e prêmios (scripts/listas_e_premios.py)
    extras = json.loads(arq_extras.read_text(encoding="utf-8")) if arq_extras.exists() else {}
    hoje = date.today().isoformat()
    bandas = {}
    for f in sorted((RAIZ / "catalogo").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        t = textos.get(b["id"], {})
        for campo in ("ativa", "fim"):  # correções de situação que o MusicBrainz ainda não registrou
            if campo in t:
                b[campo] = t[campo]
        b["bio"] = t.get("bio") or primeiros_paragrafos(b.get("resumo_pt")) or primeiros_paragrafos(b.get("resumo_en"))
        b["bio_em_ingles"] = not t.get("bio") and not b.get("resumo_pt")
        b["curiosidade"] = t.get("curiosidade")
        b["pais_nome"] = PAISES.get(b.get("pais") or "", b.get("pais") or "")
        dz = deezer.get(b["id"], {})
        artista = dz.get("artista") or {}
        b["deezer"], b["fas"], b["foto_deezer"] = artista.get("id"), artista.get("fas"), artista.get("foto")
        b["parecidas"] = dz.get("parecidas", [])
        b["premios"] = extras.get("bandas", {}).get(b["id"], {})
        dz_albuns = dz.get("albuns", {})
        curiosidades = t.get("albuns", {})
        for a in b["albuns"]:
            a["banda_id"] = b["id"]
            a["futuro"] = (a.get("data") or "") > hoje  # anunciado, ainda não lançado
            a["curiosidade"] = curiosidades.get(a["id"])
            a["deezer"] = (dz_albuns.get(a["id"]) or {}).get("id")
            a["capa_reserva"] = (dz_albuns.get(a["id"]) or {}).get("capa")
            a["listas"] = extras.get("albuns", {}).get(a["id"], [])
            h = historias.get(a["id"], {})
            a["historia"] = h.get("historia")
            significados = h.get("faixas", {})
            for faixa in a["faixas"]:
                faixa["significado"] = significados.get(str(faixa["n"]))
            a["nota_critica"] = nota_critica(a.get("critica") or {})
        notas = [a["nota_critica"] for a in b["albuns"] if a["nota_critica"] is not None]
        melhor = max([a for a in b["albuns"] if not a["futuro"]], key=lambda a: (a["nota_critica"] or a.get("publico") or 6)
                     + 0.25 * min(a.get("publico_votos") or 0, 12) + 0.6 * len(a["listas"]),
                     default=None)  # crítica + popularidade + listas famosas
        b["porta_de_entrada"] = melhor["id"] if melhor else None
        b["critica_media"] = round(sum(notas) / len(notas), 1) if notas else None
        bandas[b["id"]] = b
    return bandas


def slug(texto: str) -> str:
    """Mesmo id que scripts/montar_catalogo.py dá às bandas."""
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def albuns_por_id(bandas: dict) -> dict:
    return {a["id"]: a for b in bandas.values() for a in b["albuns"]}

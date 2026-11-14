"""Suas marcações e notas, guardadas no Supabase (projeto "Discoteca").

A chave publicável abaixo é feita para ficar visível: as regras do banco só deixam ler e gravar as tabelas
avaliacoes e bandas_usuario, e nunca apagar. Uma rotina do GitHub copia as duas tabelas para backup/ todo dia;
se o banco sair do ar, o app mostra essa cópia sem deixar editar.
"""

import json
from pathlib import Path

import requests
import streamlit as st

URL = "https://ljzhxubvksxwdzgiuzqt.supabase.co/rest/v1"
CHAVE = "sb_publishable_FS11DmFxOt9BTTxhcRVjTA_LCPxswey"
BACKUP = Path(__file__).parent / "backup"
CAMPOS_ALBUM = ("conheco", "escutei", "nota", "quero_ouvir", "favorito", "faixa_favorita", "comentario", "escutado_em")


def _cabecalho() -> dict:
    return {"apikey": CHAVE, "Content-Type": "application/json"}


def _ler_tabela(tabela: str) -> list[dict]:
    linhas, inicio = [], 0
    while True:
        r = requests.get(f"{URL}/{tabela}", params={"select": "*", "offset": inicio, "limit": 1000},
                         headers=_cabecalho(), timeout=15)
        r.raise_for_status()
        lote = r.json()
        linhas += lote
        if len(lote) < 1000:
            return linhas
        inicio += 1000


def iniciar() -> None:
    """Carrega o estado uma vez por sessão; as gravações atualizam o banco e a cópia em memória."""
    if "estado" in st.session_state:
        return
    try:
        albuns, bandas = _ler_tabela("avaliacoes"), _ler_tabela("bandas_usuario")
        st.session_state.somente_leitura = False
    except Exception:
        def copia(nome):
            arq = BACKUP / f"{nome}.json"
            return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else []
        albuns, bandas = copia("avaliacoes"), copia("bandas_usuario")
        st.session_state.somente_leitura = True
    st.session_state.estado = {"albuns": {a["album_id"]: a for a in albuns}, "bandas": {b["banda_id"]: b for b in bandas}}


def album(album_id: str) -> dict:
    return st.session_state.estado["albuns"].get(album_id, {})


def banda(banda_id: str) -> dict:
    return st.session_state.estado["bandas"].get(banda_id, {})


def _gravar(tabela: str, chave: str, linha: dict) -> bool:
    if st.session_state.get("somente_leitura"):
        st.toast("O banco está fora do ar agora; a marcação não foi salva.", icon="⚠️")
        return False
    try:
        r = requests.post(f"{URL}/{tabela}", json=linha, timeout=15,
                          headers={**_cabecalho(), "Prefer": "resolution=merge-duplicates,return=representation"})
        r.raise_for_status()
        salvo = r.json()[0]
    except Exception:
        st.toast("Não consegui salvar. Tente de novo em instantes.", icon="⚠️")
        return False
    st.session_state.estado["albuns" if tabela == "avaliacoes" else "bandas"][salvo[chave]] = salvo
    return True


def salvar_album(album_id: str, banda_id: str, **campos) -> bool:
    campos = {k: v for k, v in campos.items() if k in CAMPOS_ALBUM}
    if campos.get("escutei") or campos.get("nota") is not None:
        campos.setdefault("conheco", True)  # quem escutou ou deu nota, conhece
    return _gravar("avaliacoes", "album_id", {"album_id": album_id, "banda_id": banda_id, **campos})


def salvar_banda(banda_id: str, **campos) -> bool:
    campos = {k: v for k, v in campos.items() if k in ("conheco", "gosto")}
    return _gravar("bandas_usuario", "banda_id", {"banda_id": banda_id, **campos})

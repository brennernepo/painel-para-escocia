"""O que muda de um dia para o outro: os alertas de tempo do Met Office, ao vivo, e o atualizacao.json que uma
rotina diária revisa toda manhã (obras e greves nos trens, estradas, fechamentos, shows e jogos).

A rotina grava o JSON num ramo próprio do GitHub; o app lê esse ramo sem precisar ser reimplantado e, sem rede,
usa a cópia do repositório. Formato em verificar_atualizacao.py.
"""

import json
from datetime import date, datetime
from pathlib import Path
from xml.etree import ElementTree

import requests
import streamlit as st

from tempo import FUSO

RAMO = "claude/atualizacao-diaria"
URL_DIARIO = f"https://raw.githubusercontent.com/brennernepo/painel-para-escocia/refs/heads/{RAMO}/atualizacao.json"
LOCAL = Path(__file__).with_name("atualizacao.json")
VAZIO = {"atualizado_em": None, "avisos": [], "lugares": {}}

# Região de alertas do Met Office de cada hospedagem (Glencoe, Skye e a A9 ao norte caem em "he")
REGIAO_MET = {"edimburgo": "dg", "inverness": "he", "dalgety": "ta", "york": "yh"}


@st.cache_data(ttl=1800, show_spinner=False)
def atualizacao() -> dict:
    """A revisão mais recente da rotina diária. Cache de 30 minutos."""
    try:
        resposta = requests.get(URL_DIARIO, timeout=8)
        resposta.raise_for_status()
        dados = resposta.json()
    except Exception:  # sem rede ou ramo ainda inexistente
        try:
            dados = json.loads(LOCAL.read_text(encoding="utf-8"))
        except Exception:
            dados = {}
    return {**VAZIO, **dados}


@st.cache_data(ttl=1800, show_spinner=False)
def alertas_met() -> dict | None:
    """Alertas de tempo em vigor por hospedagem, do RSS do Met Office. Cache de 30 minutos."""
    saida = {}
    try:
        for base, regiao in REGIAO_MET.items():
            resposta = requests.get(
                f"https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{regiao}", timeout=8
            )
            resposta.raise_for_status()
            saida[base] = [
                {"titulo": i.findtext("title", ""), "texto": i.findtext("description", ""), "link": i.findtext("link", "")}
                for i in ElementTree.fromstring(resposta.content).iter("item")
            ]
    except Exception:
        return None
    return saida


def avisos_vigentes(dados: dict, hoje: date, cidade: str | None = None) -> list[dict]:
    """Avisos que ainda valem: sem dias marcados, ou com algum dia de hoje em diante. Com `cidade`, só os dela."""
    vigentes = []
    for a in dados.get("avisos", []):
        dias = [date.fromisoformat(d) for d in a.get("dias", [])]
        if dias and max(dias) < hoje:
            continue
        if cidade is not None and a.get("cidade") != cidade:
            continue
        vigentes.append(a)
    return sorted(vigentes, key=lambda a: {"vermelho": 0, "laranja": 1}.get(a.get("nivel"), 2))


def quando_revisado(dados: dict) -> str:
    """'hoje às 06h12', 'ontem às 06h10' ou 'em 03/11'; vazio se nunca rodou."""
    if not dados.get("atualizado_em"):
        return ""
    momento = datetime.fromisoformat(dados["atualizado_em"].replace("Z", "+00:00")).astimezone(FUSO)
    dias = (datetime.now(FUSO).date() - momento.date()).days
    if dias == 0:
        return f"hoje às {momento:%Hh%M}"
    if dias == 1:
        return f"ontem às {momento:%Hh%M}"
    return f"em {momento:%d/%m}"

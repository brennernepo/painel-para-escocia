"""Previsão do tempo (Open-Meteo), nascer/pôr do sol e médias históricas."""

import math
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests
import streamlit as st

FUSO = ZoneInfo("Europe/London")

# Código WMO → (descrição, emoji)
CODIGOS = {
    0: ("Céu limpo", "☀️"), 1: ("Quase limpo", "🌤"), 2: ("Parcialmente nublado", "⛅"), 3: ("Nublado", "☁️"),
    45: ("Neblina", "🌫"), 48: ("Neblina com geada", "🌫"),
    51: ("Garoa fraca", "🌦"), 53: ("Garoa", "🌦"), 55: ("Garoa forte", "🌧"),
    56: ("Garoa congelante", "🌧"), 57: ("Garoa congelante", "🌧"),
    61: ("Chuva fraca", "🌦"), 63: ("Chuva", "🌧"), 65: ("Chuva forte", "🌧"),
    66: ("Chuva congelante", "🌧"), 67: ("Chuva congelante", "🌧"),
    71: ("Neve fraca", "🌨"), 73: ("Neve", "🌨"), 75: ("Neve forte", "❄️"), 77: ("Grãos de neve", "🌨"),
    80: ("Pancadas fracas", "🌦"), 81: ("Pancadas de chuva", "🌧"), 82: ("Pancadas fortes", "⛈"),
    85: ("Pancadas de neve", "🌨"), 86: ("Pancadas de neve", "❄️"),
    95: ("Trovoada", "⛈"), 96: ("Trovoada com granizo", "⛈"), 99: ("Trovoada com granizo", "⛈"),
}


def descrever(codigo) -> tuple[str, str]:
    return CODIGOS.get(int(codigo) if codigo is not None else -1, ("Sem dado", "·"))


def hoje() -> date:
    return datetime.now(FUSO).date()


def sol(lat: float, lon: float, dia: date) -> tuple[datetime, datetime]:
    """Nascer e pôr do sol (algoritmo da NOAA, erro de cerca de 1 minuto), no horário local do Reino Unido."""
    n = dia.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1)
    eq = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                   - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dec = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
           + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    phi = math.radians(lat)
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(phi) * math.cos(dec))
                                - math.tan(phi) * math.tan(dec)))
    meia_noite = datetime(dia.year, dia.month, dia.day, tzinfo=timezone.utc)
    nascer = meia_noite + timedelta(minutes=720 - 4 * (lon + ha) - eq)
    por = meia_noite + timedelta(minutes=720 - 4 * (lon - ha) - eq)
    return nascer.astimezone(FUSO), por.astimezone(FUSO)


@st.cache_data(ttl=1800, show_spinner=False)
def previsao(locais: tuple[tuple[str, float, float], ...]) -> dict | None:
    """Previsão de 16 dias e condição atual para vários locais numa só chamada. Cache de 30 minutos."""
    try:
        resposta = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": ",".join(str(l[1]) for l in locais),
                "longitude": ",".join(str(l[2]) for l in locais),
                "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,wind_gusts_10m,precipitation",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,"
                         "precipitation_sum,snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,cloud_cover_mean",
                "timezone": "Europe/London",
                "forecast_days": 16,
            },
            timeout=15,
        )
        resposta.raise_for_status()
    except requests.RequestException:
        return None
    dados = resposta.json()
    if isinstance(dados, dict):
        dados = [dados]
    saida = {}
    for (chave, _, _), d in zip(locais, dados):
        diario = d["daily"]
        dias = {}
        for i, t in enumerate(diario["time"]):
            dias[date.fromisoformat(t)] = {
                "codigo": diario["weather_code"][i],
                "max": diario["temperature_2m_max"][i],
                "min": diario["temperature_2m_min"][i],
                "chuva_prob": diario["precipitation_probability_max"][i],
                "chuva_mm": diario["precipitation_sum"][i],
                "vento": diario["wind_speed_10m_max"][i],
                "rajada": diario["wind_gusts_10m_max"][i],
                "neve_cm": diario["snowfall_sum"][i],
                "nuvens": diario["cloud_cover_mean"][i],
            }
        saida[chave] = {"atual": d.get("current", {}), "dias": dias}
    saida["_hora"] = datetime.now(FUSO).strftime("%d/%m %H:%M")
    return saida


NEVE_OU_TROVOADA = {56, 57, 66, 67, 71, 73, 75, 77, 85, 86, 95, 96, 99}


def veredito(p: dict) -> tuple[str, str]:
    """Semáforo para passeio de estrada e paisagem: ('verde'|'atencao'|'evitar', motivo)."""
    motivos_vermelho, motivos_amarelo = [], []
    rajada, chuva_mm, prob = p.get("rajada") or 0, p.get("chuva_mm") or 0, p.get("chuva_prob") or 0
    if (p.get("codigo") or 0) in NEVE_OU_TROVOADA or (p.get("neve_cm") or 0) > 0:
        motivos_vermelho.append("neve, gelo ou trovoada previstos")
    if rajada >= 75:
        motivos_vermelho.append(f"rajadas de {rajada:.0f} km/h")
    if chuva_mm >= 15:
        motivos_vermelho.append(f"{chuva_mm:.0f} mm de chuva")
    if motivos_vermelho:
        return "evitar", "; ".join(motivos_vermelho)
    if rajada >= 55:
        motivos_amarelo.append(f"rajadas de {rajada:.0f} km/h")
    if chuva_mm >= 5 or prob >= 70:
        motivos_amarelo.append(f"{prob:.0f}% de chance de chuva, {chuva_mm:.0f} mm")
    if (p.get("nuvens") or 0) >= 90:
        motivos_amarelo.append("céu fechado: montanhas provavelmente encobertas")
    if motivos_amarelo:
        return "atencao", "; ".join(motivos_amarelo)
    return "verde", "sem chuva forte nem vento perigoso"

import hmac
import math
from datetime import date, timedelta
from html import escape
from urllib.parse import quote

import pydeck as pdk
import streamlit as st

import dados as D
import para_voce as PV
from coordenadas import COORD
from diario import alertas_met, atualizacao, avisos_vigentes, quando_revisado
from estilo import CSS, celular, html, libras, tags_html, url_maps
from tempo import descrever, hoje, previsao, sol, veredito

st.set_page_config(page_title="Painel para a Escócia", page_icon="🏴", layout="wide")
st.html(CSS)

SEMANA = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
COORD = {**COORD, **PV.COORD}
BASES = {b["id"]: b for b in D.BASES}


def ler_segredos() -> dict:
    """Senha, endereços e anfitriões vêm de st.secrets, nunca do repositório público."""
    try:
        return st.secrets.to_dict()
    except Exception:  # sem secrets.toml
        return {}


SEGREDOS = ler_segredos()
PRIVADO = {k: dict(v) for k, v in SEGREDOS.get("hospedagens", {}).items()}


def base_do_dia(dia: date) -> dict:
    """Onde vocês dormem na noite deste dia (no último dia, a última base)."""
    for b in D.BASES:
        if b["chegada"] <= dia < b["saida"]:
            return b
    return D.BASES[-1] if dia >= D.BASES[-1]["saida"] else D.BASES[0]


def fmt_data(dia: date) -> str:
    return f"{dia.day:02d}/{dia.month:02d}"


PREV = previsao(tuple((b["id"], b["lat"], b["lon"]) for b in D.BASES))


def dia_previsto(id_base: str, dia: date) -> dict | None:
    if not PREV or id_base not in PREV:
        return None
    return PREV[id_base]["dias"].get(dia)


def resumo_tempo(id_base: str, dia: date) -> tuple[str, str]:
    """Texto curto do tempo de um dia: previsão quando já existe, senão a média histórica."""
    p = dia_previsto(id_base, dia)
    if p and p["max"] is not None:
        nome, emoji = descrever(p["codigo"])
        chuva = f" · 💧{p['chuva_prob']}%" if p["chuva_prob"] is not None else ""
        return f"{emoji} {p['max']:.0f}° / {p['min']:.0f}°{chuva}", nome
    n = D.NORMAIS[id_base]
    return f"≈ {n['max_media']:.0f}° / {n['min_media']:.0f}°", "média histórica"


# ---------------------------------------------------------------------------
# Cabeçalho e faixa "agora"
# ---------------------------------------------------------------------------
html(
    '<div class="topo"><div class="marca-icone">🗺</div><div class="marca-nome">Brenner</div></div>'
    '<div class="titulo">Painel para a <span>Escócia</span></div>'
    f'<div class="descricao">{escape(D.SUBTITULO)}</div>'
)


def pedir_senha() -> None:
    """Sem a senha certa, nada abaixo do título aparece. Sem senha configurada, o painel fica fechado."""
    senha = str(SEGREDOS.get("senha", ""))
    if not senha:
        html('<div class="alerta laranja">Falta definir a senha nos Secrets do app (veja secrets.exemplo.toml).</div>')
        st.stop()
    if st.session_state.get("liberado"):
        return
    with st.form("senha", border=True):
        tentativa = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", type="primary")
    if entrar and hmac.compare_digest(tentativa.encode(), senha.encode()):
        st.session_state.liberado = True
        st.rerun()
    if entrar:
        st.error("Senha errada.")
    st.stop()


pedir_senha()

agora = hoje()
if agora < D.INICIO:
    faltam = (D.INICIO - agora).days
    primeira = D.BASES[0]
    p_atual = (PREV or {}).get(primeira["id"], {}).get("atual", {})
    tempo_agora = ""
    if p_atual:
        nome, emoji = descrever(p_atual.get("weather_code"))
        tempo_agora = f" Agora em {primeira['cidade']}: {emoji} {p_atual.get('temperature_2m', 0):.0f}°, {nome.lower()}."
    html(
        f'<div class="agora"><div class="agora-emoji">🧳</div><div><div class="agora-titulo">'
        f'Faltam {faltam} dias para a viagem</div><div class="agora-sub">Primeira parada: {primeira["cidade"]}, '
        f'check-in {escape(primeira["checkin"])} de {fmt_data(primeira["chegada"])}.{escape(tempo_agora)}</div></div></div>'
    )
elif agora <= D.FIM:
    b = base_do_dia(agora)
    nascer, por = sol(b["lat"], b["lon"], agora)
    texto, nome = resumo_tempo(b["id"], agora)
    html(
        f'<div class="agora"><div class="agora-emoji">{b["emoji"]}</div><div><div class="agora-titulo">'
        f'Hoje: {escape(b["cidade"])}</div><div class="agora-sub">{escape(texto)} ({escape(nome.lower())}) · '
        f'sol das {nascer:%H:%M} às {por:%H:%M}</div></div></div>'
    )

DIARIO = atualizacao()
MET = alertas_met()
NOME_BASE = {b["id"]: b["cidade"] for b in D.BASES} | {"geral": "Viagem"}


def link_seguro(url: str) -> str:
    return url if isinstance(url, str) and url.startswith("https://") else ""


def html_avisos(cidade: str | None = None) -> str:
    """Alertas do Met Office em vigor e avisos da revisão diária; com `cidade`, só os dela."""
    blocos = []
    for base, itens in (MET or {}).items():
        if cidade and base != cidade:
            continue
        for i in itens:
            nivel = "vermelho" if i["titulo"].lower().startswith("red") else "laranja"
            link = link_seguro(i["link"])
            mais = f' · <a class="link" href="{escape(link)}" target="_blank">detalhes</a>' if link else ""
            blocos.append(f'<div class="alerta {nivel}">🌧 <b>Met Office, {escape(NOME_BASE[base])}:</b> '
                          f'{escape(i["titulo"])}{mais}</div>')
    for a in avisos_vigentes(DIARIO, agora, cidade):
        dias = ", ".join(fmt_data(date.fromisoformat(d)) for d in a.get("dias", []))
        onde = "" if cidade else f'{escape(NOME_BASE.get(a.get("cidade"), "Viagem"))}'
        rotulo = " · ".join(x for x in (onde, dias) if x)
        link = link_seguro(a.get("fonte", ""))
        fonte = f' · <a class="link" href="{escape(link)}" target="_blank">fonte</a>' if link else ""
        nivel = a.get("nivel") if a.get("nivel") in ("vermelho", "laranja", "azul") else "azul"
        blocos.append(f'<div class="alerta {nivel}">{f"<b>{rotulo}:</b> " if rotulo else ""}'
                      f'{escape(a.get("texto", ""))}{fonte}</div>')
    return "".join(blocos)


revisado = quando_revisado(DIARIO)
avisos_topo = html_avisos()
if avisos_topo or revisado:
    rodape = (f"Revisado {revisado} (obras e greves, estradas, fechamentos, shows e jogos)" if revisado
              else "A revisão diária ainda não rodou")
    html(f'{avisos_topo}<div class="aviso">{escape(rodape)}. Alertas do Met Office ao vivo.</div>')

NOMES_ABAS = ["Roteiro", "Para você", "Tempo", "Edimburgo", "Highlands", "Glencoe e Skye", "Fife", "York", "Trechos",
              "Dicas e gastos"]
abas = dict(zip(NOMES_ABAS, st.tabs(NOMES_ABAS, key="aba", on_change="rerun")))


# ---------------------------------------------------------------------------
# Aba: roteiro
# ---------------------------------------------------------------------------
def casa(b: dict) -> tuple[float, float]:
    """Coordenadas da hospedagem (dos Secrets); sem elas, o bairro arredondado."""
    p = PRIVADO.get(b["id"], {})
    if "lat" in p and "lon" in p:
        return float(p["lat"]), float(p["lon"])
    return b["lat_mapa"], b["lon_mapa"]


def origem(b: dict) -> str:
    return PRIVADO.get(b["id"], {}).get("busca", b["busca_bairro"])


def km_entre(a: tuple[float, float], b: tuple[float, float]) -> float:
    (la1, lo1), (la2, lo2) = map(lambda p: (math.radians(p[0]), math.radians(p[1])), (a, b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def fmt_km(km: float) -> str:
    return f"{km:.1f} km".replace(".", ",") if km < 10 else f"{km:.0f} km"


SEM_CARRO = {"edimburgo", "york"}  # nessas cidades o plano é a pé, de ônibus ou de trem


def deslocamento(b: dict, destino: tuple[float, float]) -> tuple[str, str]:
    """Distância em linha reta e tempo estimado (ruas ≈ 1,3 × a reta), mais o modo da rota no Google Maps."""
    km = km_entre(casa(b), destino)
    real = km * 1.3
    longe = "walking" if real <= 3 else ("transit" if b["id"] in SEM_CARRO else "driving")
    if real <= 5:
        return f"{fmt_km(km)} da casa · ~{max(1, round(real / 4.8 * 60))} min a pé", longe
    if b["id"] in SEM_CARRO:
        return f"{fmt_km(km)} da casa · de ônibus ou trem (tempo na rota)", longe
    tempo = real / (30 if real < 15 else 65) * 60
    tempo_txt = f"~{round(tempo)} min" if tempo < 90 else f"~{tempo / 60:.1f} h".replace(".", ",")
    return f"{fmt_km(km)} da casa · {tempo_txt} de carro", longe


def url_rota(b: dict, busca: str, modo: str) -> str:
    return (f"https://www.google.com/maps/dir/?api=1&origin={quote(origem(b))}"
            f"&destination={quote(busca)}&travelmode={modo}")


def mapa_roteiro() -> pdk.Deck:
    # Edimburgo e Dalgety Bay ficam a 13 km: rótulos para lados opostos
    deslocamentos = {"edimburgo": [62, 12], "dalgety": [-66, -12], "inverness": [0, -18], "york": [0, -18]}
    pontos = [
        {"nome": f"{i}. {b['cidade']}", "lat": casa(b)[0], "lon": casa(b)[1],
         "deslocamento": deslocamentos.get(b["id"], [0, -18])}
        for i, b in enumerate(D.BASES, start=1)
    ]
    caminho = [{"path": [[lon, lat] for lat, lon in D.ROTA_MAPA]}]
    passeios = [{"nome": p["nome"], "lat": p["lat"], "lon": p["lon"]} for p in D.PONTOS_MAPA]
    return pdk.Deck(
        layers=[
            pdk.Layer("PathLayer", caminho, get_path="path", get_color=[232, 119, 46, 170], width_min_pixels=3,
                      get_width=4, joint_rounded=True, cap_rounded=True),
            pdk.Layer("ScatterplotLayer", passeios, get_position=["lon", "lat"], get_radius=1500,
                      radius_min_pixels=4, get_fill_color=[43, 30, 26, 150], stroked=True,
                      get_line_color=[255, 255, 255], line_width_min_pixels=1, pickable=True),
            pdk.Layer("ScatterplotLayer", pontos, get_position=["lon", "lat"], get_radius=4000, radius_min_pixels=8,
                      get_fill_color=[200, 49, 43, 230], stroked=True, get_line_color=[255, 255, 255],
                      line_width_min_pixels=2, pickable=True),
            pdk.Layer("TextLayer", pontos, get_position=["lon", "lat"], get_text="nome", get_size=13,
                      get_color=[43, 30, 26], font_family="'DM Sans, sans-serif'", font_weight=700,
                      get_pixel_offset="deslocamento", background=True, get_background_color=[255, 255, 255, 230],
                      background_padding=[6, 3]),
        ],
        initial_view_state=pdk.ViewState(latitude=55.82, longitude=-3.0, zoom=5.25 if celular() else 5.55),
        views=[pdk.View(type="MapView", controller={"scrollZoom": False, "dragRotate": False, "touchRotate": False})],
        map_provider="carto", map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={"html": "<b>{nome}</b>", "style": {"backgroundColor": "#fff", "color": "#2B1E1A",
                                                    "fontFamily": "DM Sans, sans-serif", "fontSize": "12px"}},
    )


with abas["Roteiro"]:
    html('<div class="rotulo">Onde vocês vão dormir</div>')
    casas = ""
    for i, b in enumerate(D.BASES, start=1):
        noites = (b["saida"] - b["chegada"]).days
        p = PRIVADO.get(b["id"], {})
        if p:
            onde = f'{escape(p.get("endereco", ""))}<br>Anfitrião: {escape(p.get("anfitriao", ""))}<br>'
            link = url_maps(p.get("busca", b["busca_bairro"]))
        else:
            onde = f"{escape(b['bairro'])}<br>"
            link = url_maps(b["busca_bairro"])
        casas += (
            f'<div class="casa"><div class="casa-cidade"><span class="casa-num">{i}</span>{escape(b["cidade"])}</div>'
            f'<div class="casa-datas">{fmt_data(b["chegada"])} → {fmt_data(b["saida"])} · {noites} noites</div>'
            f'<div class="casa-info">{onde}Check-in {escape(b["checkin"])} · check-out {escape(b["checkout"])}</div>'
            f'<div class="casa-info" style="color:var(--text3)">{escape(b["nota"])}</div>'
            f'<a class="maps" href="{link}" target="_blank">📍 Abrir no Google Maps</a></div>'
        )
    html(f'<div class="casas">{casas}</div>')
    if not PRIVADO:
        html('<div class="aviso">Endereços e anfitriões ficam fora do código público; veja secrets.exemplo.toml.</div>')

    html('<div class="rotulo">Dia a dia</div>')
    linhas = ""
    dia = D.INICIO
    while dia <= D.FIM:
        b = base_do_dia(dia)
        nascer, por = sol(b["lat"], b["lon"], dia)
        texto, nome = resumo_tempo(b["id"], dia)
        evento = D.EVENTOS_DIA.get(dia, "")
        classe = "dia hoje" if dia == agora else "dia"
        linhas += (
            f'<div class="{classe}"><div class="dia-data">{fmt_data(dia)}<small>{SEMANA[dia.weekday()]}</small></div>'
            f'<div><div class="dia-base">{b["emoji"]} {escape(b["cidade"])}</div>'
            f'<div class="dia-evento">{escape(evento)}</div>'
            f'<div class="dia-sol">☀ {nascer:%H:%M} – {por:%H:%M} ({(por - nascer).seconds / 3600:.1f} h de luz)</div></div>'
            f'<div class="dia-tempo">{escape(texto)}<small>{escape(nome)}</small></div></div>'
        )
        dia += timedelta(days=1)
    html(f'<div class="bloco">{linhas}</div>')
    html('<div class="aviso">A previsão substitui a média histórica sozinha quando o dia entra nos 16 dias da Open-Meteo.</div>')

    html('<div class="rotulo">O percurso</div>')
    with st.container(key="mapa_box"):
        st.pydeck_chart(mapa_roteiro(), height=420 if celular() else 480)
    html('<div class="aviso">Pontos vermelhos: hospedagens. Pontos escuros: passeios citados nas outras abas '
         '(passe o mouse ou toque para ver o nome). A linha segue a A9 e a ferrovia da costa leste.</div>')


# ---------------------------------------------------------------------------
# Aba: tempo
# ---------------------------------------------------------------------------
with abas["Tempo"]:
    atual = base_do_dia(agora) if D.INICIO <= agora <= D.FIM else D.BASES[0]
    escolha = st.segmented_control(
        "Cidade", [b["id"] for b in D.BASES], default=atual["id"], required=True, key="cidade_tempo",
        format_func=lambda i: f"{BASES[i]['emoji']} {BASES[i]['cidade']}", label_visibility="collapsed",
    )
    b = BASES[escolha]
    estadia = {b["chegada"] + timedelta(days=k) for k in range((b["saida"] - b["chegada"]).days + 1)}

    if PREV and escolha in PREV:
        a = PREV[escolha]["atual"]
        nome, emoji = descrever(a.get("weather_code"))
        html(
            f'<div class="rotulo">Agora em {escape(b["cidade"])} · atualizado {PREV["_hora"]}</div><div class="tiles">'
            f'<div class="tile forte"><div class="tile-valor">{emoji} {a.get("temperature_2m", 0):.0f}°</div>'
            f'<div class="tile-rot">{escape(nome)}</div></div>'
            f'<div class="tile"><div class="tile-valor">{a.get("apparent_temperature", 0):.0f}°</div><div class="tile-rot">sensação</div></div>'
            f'<div class="tile"><div class="tile-valor">{a.get("wind_speed_10m", 0):.0f}</div><div class="tile-rot">vento, km/h</div></div>'
            f'<div class="tile"><div class="tile-valor">{a.get("wind_gusts_10m", 0):.0f}</div><div class="tile-rot">rajadas, km/h</div></div></div>'
        )
        cartoes = ""
        for dia, p in PREV[escolha]["dias"].items():
            if p["max"] is None:
                continue
            nome, emoji = descrever(p["codigo"])
            classe = "cartao-dia estadia" if dia in estadia else "cartao-dia"
            cartoes += (
                f'<div class="{classe}" title="{escape(nome)}"><div class="cd-data">{SEMANA[dia.weekday()]} {fmt_data(dia)}</div>'
                f'<div class="cd-emoji">{emoji}</div><div class="cd-temp">{p["max"]:.0f}° <span>{p["min"]:.0f}°</span></div>'
                f'<div class="cd-extra">💧 {p["chuva_prob"] or 0}% · {p["chuva_mm"] or 0:.0f} mm<br>💨 {p["rajada"] or 0:.0f} km/h</div></div>'
            )
        cobre = any(d in estadia for d in PREV[escolha]["dias"])
        html(f'<div class="rotulo">Próximos 16 dias</div><div class="faixa-dias">{cartoes}</div>')
        if cobre:
            html('<div class="aviso">Bordas laranja: dias em que vocês estarão na cidade.</div>')
        else:
            primeiro = min(estadia)
            html(
                f'<div class="aviso">A previsão ainda não chega às datas de vocês em {escape(b["cidade"])}; '
                f'ela começa a aparecer por volta de {fmt_data(primeiro - timedelta(days=15))}.</div>'
            )
    else:
        html('<div class="alerta laranja">Não consegui buscar a previsão agora. Tente recarregar a página em alguns minutos.</div>')

    n = D.NORMAIS[escolha]
    html(
        f'<div class="rotulo">Como costuma ser de {fmt_data(b["chegada"])} a {fmt_data(b["saida"])} (2015–2025)</div>'
        '<div class="tiles">'
        f'<div class="tile"><div class="tile-valor">{n["max_media"]:.0f}° / {n["min_media"]:.0f}°</div><div class="tile-rot">máxima / mínima média</div></div>'
        f'<div class="tile"><div class="tile-valor">{n["dias_chuva_pct"]}%</div><div class="tile-rot">dos dias com chuva (≥1 mm)</div></div>'
        f'<div class="tile"><div class="tile-valor">{n["rajada_media_kmh"]}</div><div class="tile-rot">rajada típica, km/h</div></div>'
        f'<div class="tile"><div class="tile-valor">{n["min_recorde"]:.0f}° a {n["max_recorde"]:.0f}°</div><div class="tile-rot">extremos registrados</div></div>'
        "</div>"
        '<div class="aviso">Dados diários da reanálise ERA5 via Open-Meteo, mesmas datas de 2015 a 2025.</div>'
    )
    roupa = "".join(f'<div class="linha"><span class="linha-r">{escape(r)}</span><span class="linha-v">{escape(v)}</span></div>'
                    for r, v in D.O_QUE_LEVAR)
    links = " · ".join(f'<a class="link" href="{u}" target="_blank">{escape(t)}</a>' for t, u in D.LINKS_TEMPO)
    html(f'<div class="rotulo">O que levar</div><div class="bloco">{roupa}</div>'
         f'<div class="aviso" style="font-style:normal">Fontes oficiais: {links}</div>')


# ---------------------------------------------------------------------------
# Abas das cidades
# ---------------------------------------------------------------------------
def cartao_ponto(p: dict, base: dict | None = None) -> str:
    """Cartão de um lugar. Com `base`, mostra a distância da hospedagem e a rota saindo dela."""
    meta = f'<div class="ponto-meta">{p["meta"]}</div>' if p.get("meta") else ""
    busca = p.get("busca") or p["nome"]
    perto, rota = "", ""
    revisao = DIARIO["lugares"].get(p["nome"])
    if revisao and revisao.get("nota"):
        classe = "vermelho" if revisao.get("nivel") == "fechado" else "laranja" if revisao.get("nivel") == "atencao" else "azul"
        meta += f'<div class="ponto-aviso {classe}">📅 {escape(revisao["nota"])}</div>'
    if base and p["nome"] in COORD:
        texto, modo = deslocamento(base, COORD[p["nome"]])
        perto = f'<div class="ponto-casa">🏠 {escape(texto)}</div>'
        rota = f'<a class="maps" href="{url_rota(base, busca, modo)}" target="_blank">🧭 Rota a partir da casa</a>'
    return (
        f'<div class="ponto"><div class="ponto-topo"><span class="ponto-emoji">{p["emoji"]}</span>'
        f'<span class="ponto-nome">{escape(p["nome"])}</span></div>'
        f'<div class="ponto-texto">{escape(p["texto"])}</div>{meta}{perto}{tags_html(p.get("tags", []))}'
        f'<div class="ponto-links"><a class="maps" href="{url_maps(busca)}" target="_blank">📍 Abrir no Google Maps</a>{rota}</div></div>'
    )


def mapa_cidade(base: dict, pontos: list[dict]) -> pdk.Deck | None:
    """A hospedagem (vermelho) e os lugares da seção escolhida (escuro)."""
    lugares = [{"nome": p["nome"], "lat": COORD[p["nome"]][0], "lon": COORD[p["nome"]][1]}
               for p in pontos if p["nome"] in COORD]
    if not lugares:
        return None
    lat_c, lon_c = casa(base)
    lar = [{"nome": f"Casa em {base['cidade']}", "lat": lat_c, "lon": lon_c}]
    lats = [x["lat"] for x in lugares + lar]
    lons = [x["lon"] for x in lugares + lar]
    longe = max(km_entre((lat_c, lon_c), (x["lat"], x["lon"])) for x in lugares)
    zoom = min(15.0, max(6.0, 12.7 - math.log2(max(longe, 0.6)))) - (0.5 if celular() else 0)
    return pdk.Deck(
        layers=[
            pdk.Layer("ScatterplotLayer", lugares, get_position=["lon", "lat"], get_radius=60, radius_min_pixels=5,
                      radius_max_pixels=9, get_fill_color=[43, 30, 26, 190], stroked=True,
                      get_line_color=[255, 255, 255], line_width_min_pixels=1, pickable=True),
            pdk.Layer("ScatterplotLayer", lar, get_position=["lon", "lat"], get_radius=90, radius_min_pixels=9,
                      radius_max_pixels=12, get_fill_color=[200, 49, 43, 240], stroked=True,
                      get_line_color=[255, 255, 255], line_width_min_pixels=2, pickable=True),
        ],
        initial_view_state=pdk.ViewState(latitude=(min(lats) + max(lats)) / 2,
                                         longitude=(min(lons) + max(lons)) / 2, zoom=zoom),
        views=[pdk.View(type="MapView", controller={"scrollZoom": False, "dragRotate": False, "touchRotate": False})],
        map_provider="carto", map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={"html": "<b>{nome}</b>", "style": {"backgroundColor": "#fff", "color": "#2B1E1A",
                                                    "fontFamily": "DM Sans, sans-serif", "fontSize": "12px"}},
    )


BASE_DA_ABA = {"edimburgo": "edimburgo", "highlands": "inverness", "fife": "dalgety", "york": "york"}


def mostrar_cidade(cidade: dict, base: dict, chave: str) -> None:
    """Intro, avisos do dia, alerta, seções em pílulas, mapa da seção a partir da casa e cartões com distância."""
    if avisos := html_avisos(base["id"]):
        html(avisos)
    html(f'<div class="descricao" style="margin-top:4px">{escape(cidade["intro"])}</div>')
    if cidade.get("alerta"):
        html(f'<div class="alerta azul">{escape(cidade["alerta"])}</div>')
    secoes = cidade["secoes"]
    nomes = [s["nome"] for s in secoes]
    escolha = st.pills("Seção", nomes, default=nomes[0], key=f"secao_{chave}", label_visibility="collapsed")
    s = next((x for x in secoes if x["nome"] == escolha), secoes[0])
    html(
        f'<div class="regiao" style="margin-top:6px"><div class="faixa"></div><div class="regiao-corpo">'
        f'<div class="regiao-nome">{escape(s["nome"])}</div><div class="regiao-desc" style="margin-bottom:0">'
        f'{escape(s["descricao"])}</div></div></div>'
    )
    if s.get("pontos"):
        mapa = mapa_cidade(base, s["pontos"])
        if mapa:
            with st.container(key=f"mapa_{chave}"):
                st.pydeck_chart(mapa, height=300 if celular() else 360)
            html(f'<div class="aviso">Ponto vermelho: a casa em {escape(base["cidade"])}. Pontos escuros: os lugares desta '
                 'seção. Distâncias em linha reta; o tempo é estimado e a rota no Google Maps dá o valor real.</div>')
        html('<div class="pontos" style="margin-top:12px">' + "".join(cartao_ponto(p, base) for p in s["pontos"]) + "</div>")
    if s.get("dicas"):
        dicas = "".join(f'<div class="linha"><span class="linha-r">{escape(r)}</span><span class="linha-v">{escape(v)}</span></div>'
                        for r, v in s["dicas"])
        html(f'<div class="rotulo">Dicas</div><div class="bloco">{dicas}</div>')


for aba, chave in [("Edimburgo", "edimburgo"), ("Highlands", "highlands"), ("Fife", "fife"), ("York", "york")]:
    with abas[aba]:
        mostrar_cidade(D.CIDADES[chave], BASES[BASE_DA_ABA[chave]], chave)


# ---------------------------------------------------------------------------
# Aba: para você (sugestões pessoais por cidade: trabalho, história, música, bebida, comida)
# ---------------------------------------------------------------------------
with abas["Para você"]:
    html(f'<div class="descricao" style="margin-top:4px">{escape(PV.INTRO)}</div>')
    atual = base_do_dia(agora) if D.INICIO <= agora <= D.FIM else D.BASES[0]
    escolha = st.segmented_control(
        "Cidade", [b["id"] for b in D.BASES], default=atual["id"], required=True, key="cidade_voce",
        format_func=lambda i: f"{BASES[i]['emoji']} {BASES[i]['cidade']}", label_visibility="collapsed",
    )
    mostrar_cidade(PV.PARA_VOCE[escolha], BASES[escolha], f"voce_{escolha}")


# ---------------------------------------------------------------------------
# Aba: Glencoe e Skye
# ---------------------------------------------------------------------------
PREV_EXTRA = previsao(tuple((d["id"], d["lat"], d["lon"]) for d in D.DESTINOS_EXTRA))
NOMES_EXTRA = {d["id"]: d["nome"] for d in D.DESTINOS_EXTRA}
COORD_EXTRA = {d["id"]: (d["lat"], d["lon"]) for d in D.DESTINOS_EXTRA}
ROTULO_NIVEL = {"verde": "Bom para ir", "atencao": "Dá, com ressalvas", "evitar": "Melhor não", "info": "Sem previsão ainda"}
ORDEM_NIVEL = {"verde": 0, "info": 1, "atencao": 2, "evitar": 3}
COR_NIVEL = {"verde": "#157A55", "info": "#2C5C8A", "atencao": "#D97706", "evitar": "#B42318"}


def tempo_destino(local: str, dia: date) -> dict:
    p = (PREV_EXTRA or {}).get(local, {}).get("dias", {}).get(dia)
    if p and p["max"] is not None:
        nivel, motivo = veredito(p)
        nome, emoji = descrever(p["codigo"])
        texto = f"{emoji} {p['max']:.0f}° / {p['min']:.0f}° · 💧 {p['chuva_prob'] or 0}% · 💨 {p['rajada'] or 0:.0f} km/h"
        return {"nivel": nivel, "motivo": motivo, "texto": texto, "emoji": emoji, "p": p}
    n = D.NORMAIS_EXTRA[local]
    return {
        "nivel": "info", "emoji": "📅",
        "motivo": f"a previsão começa por volta de {fmt_data(dia - timedelta(days=15))}; "
                  f"nos últimos 11 anos, {n['dias_bons_pct']}% desses dias foram bons para o passeio",
        "texto": f"≈ {n['max_media']:.0f}° / {n['min_media']:.0f}° · chove em {n['dias_chuva_pct']}% dos dias",
        "p": None,
    }


with abas["Glencoe e Skye"]:
    html(f'<div class="descricao" style="margin-top:4px">{escape(D.GLENCOE_SKYE_INTRO)}</div>')

    # Tempo nos dias possíveis
    dias_possiveis = [date(2026, 11, 5), date(2026, 11, 6), date(2026, 11, 7)]
    for local in ("glencoe", "skye"):
        cartoes = ""
        for dia in dias_possiveis:
            t = tempo_destino(local, dia)
            nascer, por = sol(*COORD_EXTRA[local], dia)
            p = t["p"]
            if p:
                linha = (f'<div class="cd-temp">{p["max"]:.0f}° <span>{p["min"]:.0f}°</span></div>'
                         f'<div class="cd-extra">💧 {p["chuva_prob"] or 0}% · 💨 {p["rajada"] or 0:.0f}</div>')
            else:
                n = D.NORMAIS_EXTRA[local]
                linha = (f'<div class="cd-temp">≈{n["max_media"]:.0f}° <span>{n["min_media"]:.0f}°</span></div>'
                         '<div class="cd-extra">média histórica</div>')
            cartoes += (
                f'<div class="cartao-dia" style="flex-basis:150px;border-top:4px solid {COR_NIVEL[t["nivel"]]}">'
                f'<div class="cd-data">{SEMANA[dia.weekday()]} {fmt_data(dia)}</div><div class="cd-emoji">{t["emoji"]}</div>'
                f'{linha}<div class="cd-extra" style="color:{COR_NIVEL[t["nivel"]]};font-weight:600">{ROTULO_NIVEL[t["nivel"]]}</div>'
                f'<div class="cd-extra">☀ {nascer:%H:%M}–{por:%H:%M}</div></div>'
            )
        html(f'<div class="rotulo">{escape(NOMES_EXTRA[local])}</div><div class="faixa-dias">{cartoes}</div>')
    html('<div class="aviso">Verde: sem chuva forte nem vento perigoso. Laranja: rajadas acima de 55 km/h, chuva provável '
         'ou céu fechado. Vermelho: neve, trovoada, rajadas acima de 75 km/h ou mais de 15 mm de chuva.</div>')

    # Perguntas
    html('<div class="rotulo">Como vocês estão</div>')
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            carro = st.segmented_control("Vão ter carro?", ["Sim", "Não", "Ainda não sei"], default="Ainda não sei",
                                         required=True, key="gs_carro")
        with c2:
            limite = st.slider("Até quantas horas ao volante num dia?", 2.0, 8.0, 6.0, 0.5, key="gs_horas", format="%.1f h")

    # Cenários
    avaliados = []
    for c in D.CENARIOS:
        horas = c["minutos"] * 1.2 / 60
        tempos = [(l, d, tempo_destino(l, d)) for l, d in c.get("tempo", [(l, c["dia"]) for l in c["locais"]])]
        bloqueio = ""
        if c["carro"] and carro == "Não":
            bloqueio = "Precisa de carro"
        elif c["carro"] and horas > limite:
            bloqueio = f"~{horas:.1f} h ao volante passa do limite de {limite:g} h".replace(".", ",")
        if bloqueio:
            nivel = "evitar"
        elif tempos:
            nivel = max((t["nivel"] for _, _, t in tempos), key=lambda n: ORDEM_NIVEL[n])
        else:
            nivel = "verde"
        avaliados.append(((c.get("reserva", False), ORDEM_NIVEL[nivel]), c, horas, tempos, bloqueio, nivel))
    avaliados.sort(key=lambda x: x[0])  # o plano B fica sempre por último

    html('<div class="rotulo">Opções, das mais viáveis às menos</div>')
    for _, c, horas, tempos, bloqueio, nivel in avaliados:
        dia_txt = f'{SEMANA[c["dia"].weekday()]} {fmt_data(c["dia"])}'
        volante = f" · ~{horas:.1f} h ao volante com paradas curtas".replace(".", ",") if c["carro"] else ""
        motivo = f'<div class="opcao-resumo" style="color:{COR_NIVEL[nivel]}">{escape(bloqueio)}</div>' if bloqueio else ""
        linhas_tempo = "".join(
            f'<div class="linha"><span class="linha-r">{escape(NOMES_EXTRA[l])}, {fmt_data(d)}</span>'
            f'<span class="linha-v">{escape(t["texto"])}<br><span style="font-weight:400;color:var(--text3)">'
            f'{escape(t["motivo"])}</span></span></div>'
            for l, d, t in tempos
        )
        plano = "".join(
            f'<div class="linha"><span class="linha-r" style="flex:0 0 72px;font-weight:600">{escape(h)}</span>'
            f'<span class="linha-v" style="text-align:left;font-weight:400">{escape(o)}</span></div>'
            for h, o in c["plano"]
        )
        html(
            f'<div class="rota" style="margin-top:12px"><div class="faixa" style="background:{COR_NIVEL[nivel]}"></div>'
            f'<div class="regiao-corpo"><div class="regiao-nome" style="font-size:24px">{escape(c["titulo"])}</div>'
            f'<span class="chip">{dia_txt}</span> <span class="selo {nivel}">{ROTULO_NIVEL[nivel]}</span>{motivo}'
            f'<div class="regiao-desc" style="margin:10px 0 4px">{escape(c["comparacao"])}{volante}</div>'
            f'<div class="ponto-meta">{escape(c["rota"])}</div>'
            + (f'<div class="bloco" style="margin-top:10px">{linhas_tempo}</div>' if linhas_tempo else "")
            + (f'<div class="bloco" style="margin-top:10px">{plano}</div>' if plano else "")
            + f'<div class="alerta azul">{escape(c["observacao"])}</div></div></div>'
        )

    # O que ver
    html('<div class="rotulo">O que ver</div>')
    lugar = st.pills("Lugar", ["Glencoe", "Skye"], default="Glencoe", key="gs_lugar", label_visibility="collapsed")
    pontos = D.SKYE if lugar == "Skye" else D.GLENCOE
    html('<div class="pontos">' + "".join(cartao_ponto(p, BASES["inverness"]) for p in pontos) + "</div>")

    # Checklist
    itens = "".join(f'<div class="linha"><span class="linha-r">{escape(r)}</span><span class="linha-v">{escape(v)}</span></div>'
                    for r, v in D.CHECKLIST)
    links = " · ".join(f'<a class="link" href="{u}" target="_blank">{escape(t)}</a>' for t, u in D.LINKS_GLENCOE_SKYE)
    html(f'<div class="rotulo">Na véspera, antes de decidir</div><div class="bloco">{itens}</div>'
         f'<div class="aviso" style="font-style:normal">{links}</div>')


# ---------------------------------------------------------------------------
# Aba: trechos
# ---------------------------------------------------------------------------
with abas["Trechos"]:
    html(f'<div class="alerta azul" style="margin-top:4px">{escape(D.TRECHOS_INTRO)}</div>')
    for t in D.TRECHOS:
        opcoes = "".join(
            f'<div class="opcao"><div class="opcao-emoji">{o["emoji"]}</div><div><div class="opcao-nome">{escape(o["nome"])}</div>'
            f'<div class="opcao-resumo">{escape(o["resumo"])}</div><div class="opcao-texto">{escape(o["texto"])}</div></div></div>'
            for o in t["opcoes"]
        )
        data = f'<span class="chip">{escape(t["quando"])}</span>' if t.get("quando") else ""
        html(
            f'<div class="rota" style="margin-top:14px"><div class="faixa"></div><div class="regiao-corpo" style="padding-bottom:8px">'
            f'<div class="regiao-nome" style="font-size:26px">{escape(t["titulo"])}</div>{data}'
            f'<div class="regiao-desc" style="margin:8px 0 4px">{escape(t["descricao"])}</div>{opcoes}</div></div>'
        )
        if t.get("paradas"):
            html('<div class="rotulo">Paradas no caminho</div><div class="pontos">'
                 + "".join(cartao_ponto(p) for p in t["paradas"]) + "</div>")


# ---------------------------------------------------------------------------
# Aba: dicas e gastos
# ---------------------------------------------------------------------------
with abas["Dicas e gastos"]:
    for grupo in D.DICAS:
        linhas = "".join(f'<div class="linha"><span class="linha-r">{escape(r)}</span><span class="linha-v">{escape(v)}</span></div>'
                         for r, v in grupo["itens"])
        html(f'<div class="rotulo">{escape(grupo["titulo"])}</div><div class="bloco">{linhas}</div>')

    html('<div class="rotulo">Estimativa de gastos</div>')
    with st.container(border=True):
        c1, c2 = st.columns(2)
        perfil = c1.selectbox("Perfil de gasto", list(D.PERFIS), index=1)
        pessoas = c2.selectbox("Pessoas", [1, 2, 3, 4], index=1, format_func=lambda p: "1 pessoa" if p == 1 else f"{p} pessoas")
    dias = (D.FIM - D.INICIO).days
    gastos = D.PERFIS[perfil]
    dia_pessoa = sum(gastos.values())
    total = (dia_pessoa * dias + D.TRECHOS_POR_PESSOA) * pessoas
    html(
        '<div class="tiles" style="grid-template-columns:repeat(3,1fr)">'
        f'<div class="tile forte"><div class="tile-valor">{libras(total)}</div><div class="tile-rot">total estimado, {dias} dias</div></div>'
        f'<div class="tile"><div class="tile-valor">{libras(dia_pessoa)}</div><div class="tile-rot">por dia, por pessoa</div></div>'
        f'<div class="tile"><div class="tile-valor">{libras(D.TRECHOS_POR_PESSOA * pessoas)}</div><div class="tile-rot">trens entre as cidades</div></div>'
        "</div>"
        f'<div class="aviso">{escape(D.GASTOS_NOTA)}</div>'
    )
    maior = max(gastos.values())
    cats = "".join(
        f'<div class="cat"><div class="cat-topo"><div><div class="cat-nome">{escape(c)}</div>'
        f'<div class="cat-sub">{escape(D.CATEGORIAS[c])}</div></div><div class="cat-valor">{libras(v)}</div></div>'
        f'<div class="barra"><i style="width:{v / maior * 100:.0f}%"></i></div></div>'
        for c, v in gastos.items()
    )
    ref = "".join(f'<div class="linha"><span class="linha-r">{escape(i)}</span><span class="linha-v">{escape(p)}</span></div>'
                  for i, p in D.PRECOS)
    html(f'<div class="rotulo">Por categoria, por pessoa, por dia</div><div class="bloco">{cats}</div>'
         f'<div class="rotulo">Preços de referência</div><div class="bloco">{ref}</div>')

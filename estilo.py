"""Visual do painel (mesma identidade do Painel para Londres) e pequenos utilitários de HTML."""

import unicodedata
from html import escape
from urllib.parse import quote

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=DM+Sans:wght@400;500;600&display=swap');
:root {
  --bg: #FBF5EF; --card: #FFFFFF; --bg3: #F6E7DA;
  --border: rgba(160,52,28,0.13); --border2: rgba(160,52,28,0.26);
  --red: #C8312B; --orange: #E8772E; --tint: rgba(232,119,46,0.09);
  --text: #2B1E1A; --text2: rgba(43,30,26,0.74); --text3: rgba(43,30,26,0.50);
  --ok: #157A55; --ok-bg: #E3F3EB;
  --warn: #9A5306; --warn-bg: #FCEBD3;
  --bad: #B42318; --bad-bg: #FDE4E1;
  --info: #2C5C8A; --info-bg: #E5EEF7;
}
html, body, .stApp, .stMarkdown, button, input, textarea, label, p { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] { max-width: 960px; padding-top: 2rem; padding-bottom: 4rem; }

.topo { display: flex; align-items: center; gap: 10px; padding-bottom: 16px; border-bottom: 1px solid var(--border); margin-bottom: 26px; }
.marca-icone { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--red), var(--orange)); color: #fff; font-size: 17px; }
.marca-nome { font-family: 'Cormorant Garamond', serif; font-size: 24px; font-weight: 600; color: var(--text); }
.titulo { font-family: 'Cormorant Garamond', serif; font-size: 40px; font-weight: 500; line-height: 1.1; color: var(--text); margin: 0 0 8px; }
.titulo span { color: var(--red); }
.descricao { font-size: 14px; color: var(--text2); max-width: 620px; margin-bottom: 6px; }
.rotulo { font-size: 11px; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--text3); margin: 22px 0 10px; }
.aviso { font-size: 12px; color: var(--text3); font-style: italic; margin: 8px 0 0; }
a.link { color: var(--red) !important; font-weight: 600; text-decoration: none; }
a.link:hover { text-decoration: underline; }

/* abas e seletores */
[data-testid="stTabs"] [role="tab"] p { font-size: 14px; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p { color: var(--red); font-weight: 600; }
[data-testid="stButtonGroup"] button[aria-checked="true"] { background: linear-gradient(135deg, var(--red), var(--orange));
  border-color: transparent; color: #fff; }
[data-testid="stButtonGroup"] button[aria-checked="true"] p { color: #fff; }

/* faixa "agora" */
.agora { display: flex; gap: 14px; align-items: center; background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 14px 18px; margin: 4px 0 18px; }
.agora-emoji { font-size: 30px; }
.agora-titulo { font-weight: 600; font-size: 15px; color: var(--text); }
.agora-sub { font-size: 13px; color: var(--text2); }

/* cartões */
.regiao, .rota { background: var(--card); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
.faixa { height: 5px; background: linear-gradient(90deg, var(--red), var(--orange)); }
.regiao-corpo { padding: 18px 22px 20px; }
.regiao-nome { font-family: 'Cormorant Garamond', serif; font-size: 30px; font-weight: 600; color: var(--text); line-height: 1.15; }
.regiao-desc { font-size: 14px; color: var(--text2); margin: 6px 0 12px; max-width: 680px; }
.selo { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; padding: 3px 10px; border-radius: 99px; }
.selo::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.selo.verde { background: var(--ok-bg); color: var(--ok); }
.selo.atencao { background: var(--warn-bg); color: var(--warn); }
.selo.evitar { background: var(--bad-bg); color: var(--bad); }
.selo.info { background: var(--info-bg); color: var(--info); }

.pontos { display: grid; grid-template-columns: repeat(auto-fill, minmax(255px, 1fr)); gap: 10px; }
.ponto { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 14px 16px;
  display: flex; flex-direction: column; gap: 7px; }
.ponto-topo { display: flex; align-items: center; gap: 9px; }
.ponto-emoji { font-size: 20px; }
.ponto-nome { font-weight: 600; font-size: 15px; color: var(--text); line-height: 1.25; }
.ponto-texto { font-size: 13px; color: var(--text2); line-height: 1.5; }
.ponto-meta { font-size: 12px; color: var(--text3); line-height: 1.45; }
.ponto-meta b { color: var(--text2); font-weight: 600; }
.tags { display: flex; flex-wrap: wrap; gap: 5px; }
.tag { font-size: 11px; padding: 2px 9px; border-radius: 99px; background: var(--bg3); color: var(--text2); }
.tag.gratis { background: var(--ok-bg); color: var(--ok); }
.tag.pago { background: #FDE9DA; color: #A84616; }
.tag.fechado { background: var(--bad-bg); color: var(--bad); }
.tag.reserva { background: var(--info-bg); color: var(--info); }
.tag.trabalho { background: #EEE8F7; color: #5B3F8C; }
.tag.show { background: #FBE3E1; color: var(--red); font-weight: 600; }
a.maps { margin-top: auto; padding-top: 4px; font-size: 12px; font-weight: 600; color: var(--red) !important; text-decoration: none; }
a.maps:hover { text-decoration: underline; }
.ponto-casa { font-size: 12px; font-weight: 600; color: var(--text2); background: var(--bg3); border-radius: 8px;
  padding: 5px 9px; align-self: flex-start; }
.ponto-links { margin-top: auto; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.ponto-links a.maps { margin-top: 0; }

.duas-col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.bloco { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 6px 16px; }
.bloco .rotulo { margin: 10px 0 4px; }
.linha { display: flex; justify-content: space-between; align-items: center; gap: 14px; padding: 9px 0; border-bottom: 1px solid var(--border); }
.linha:last-child { border-bottom: none; }
.linha-r { flex: 1 1 45%; font-size: 13px; color: var(--text2); }
.linha-v { flex: 1 1 55%; font-size: 13px; font-weight: 500; color: var(--text); text-align: right; }
.chip { display: inline-block; font-size: 12px; padding: 3px 10px; border-radius: 99px; background: var(--tint); color: #A84616; font-weight: 500; }

/* hospedagens */
.casas { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
@media (max-width: 900px) { .casas { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px) { .casas { grid-template-columns: 1fr; } }
.casa { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 14px 16px; display: flex; flex-direction: column; gap: 4px; }
.casa-num { width: 24px; height: 24px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--red), var(--orange)); color: #fff; font-size: 12px; font-weight: 600; margin-right: 6px; }
.casa-cidade { font-family: 'Cormorant Garamond', serif; font-size: 24px; font-weight: 600; color: var(--text); display: flex; align-items: center; }
.casa-datas { font-size: 13px; font-weight: 600; color: #A84616; }
.casa-info { font-size: 12px; color: var(--text2); line-height: 1.5; }

/* dia a dia */
.dia { display: grid; grid-template-columns: 74px 1fr auto; gap: 12px; align-items: center; padding: 11px 0; border-bottom: 1px solid var(--border); }
.dia:last-child { border-bottom: none; }
.dia.hoje { background: var(--tint); margin: 0 -16px; padding-left: 16px; padding-right: 16px; }
.dia-data { font-weight: 600; font-size: 14px; color: var(--text); line-height: 1.2; }
.dia-data small { display: block; font-weight: 400; font-size: 11px; color: var(--text3); text-transform: uppercase; letter-spacing: .05em; }
.dia-base { font-size: 13px; font-weight: 600; color: var(--text); }
.dia-evento { font-size: 12px; color: var(--text2); line-height: 1.45; }
.dia-sol { font-size: 11px; color: var(--text3); }
.dia-tempo { text-align: right; font-size: 13px; color: var(--text); white-space: nowrap; }
.dia-tempo small { display: block; font-size: 11px; color: var(--text3); }

/* previsão */
.faixa-dias { display: flex; gap: 8px; overflow-x: auto; padding: 2px 2px 8px; scrollbar-width: thin; }
.cartao-dia { flex: 0 0 92px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 10px 8px; text-align: center; }
.cartao-dia.estadia { border: 1.5px solid var(--orange); background: #FFF8F2; }
.cd-data { font-size: 11px; color: var(--text3); text-transform: uppercase; letter-spacing: .04em; }
.cd-emoji { font-size: 24px; margin: 4px 0; }
.cd-temp { font-size: 14px; font-weight: 600; color: var(--text); font-variant-numeric: tabular-nums; }
.cd-temp span { color: var(--text3); font-weight: 400; }
.cd-extra { font-size: 11px; color: var(--text2); line-height: 1.35; margin-top: 3px; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.tile { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 14px; text-align: center; }
.tile.forte { background: linear-gradient(135deg, var(--red), var(--orange)); border-color: transparent; }
.tile-valor { font-size: 24px; font-weight: 600; color: var(--text); line-height: 1.2; font-variant-numeric: tabular-nums; }
.tile-rot { font-size: 12px; color: var(--text2); }
.tile.forte .tile-valor, .tile.forte .tile-rot { color: #fff; }

/* trechos */
.opcao { display: grid; grid-template-columns: 34px 1fr; gap: 10px; padding: 12px 0; border-top: 1px solid var(--border); }
.opcao-emoji { font-size: 22px; line-height: 1.2; }
.opcao-nome { font-weight: 600; font-size: 14px; color: var(--text); }
.opcao-resumo { font-size: 12px; font-weight: 600; color: #A84616; margin: 1px 0 3px; }
.opcao-texto { font-size: 13px; color: var(--text2); line-height: 1.5; }

/* gastos */
.cat { padding: 10px 0; border-bottom: 1px solid var(--border); }
.cat:last-child { border-bottom: none; }
.cat-topo { display: flex; justify-content: space-between; align-items: baseline; }
.cat-nome { font-size: 14px; color: var(--text); }
.cat-sub { font-size: 11px; color: var(--text3); }
.cat-valor { font-size: 15px; font-weight: 600; color: var(--text); font-variant-numeric: tabular-nums; }
.barra { height: 4px; border-radius: 4px; background: var(--bg3); margin-top: 7px; }
.barra i { display: block; height: 100%; border-radius: 4px; background: var(--orange); }

[class*="st-key-mapa_"] { border: 1px solid var(--border); border-radius: 16px; overflow: hidden; background: var(--card); }
.alerta { border-radius: 12px; padding: 10px 14px; font-size: 13px; margin-top: 10px; line-height: 1.5; }
.alerta.laranja { background: var(--warn-bg); color: var(--warn); }
.alerta.vermelho { background: var(--bad-bg); color: var(--bad); }
.alerta.azul { background: var(--info-bg); color: var(--info); }

@media (max-width: 640px) {
  .titulo { font-size: 32px; }
  .duas-col { grid-template-columns: 1fr; }
  .tiles { grid-template-columns: 1fr 1fr; }
  .regiao-corpo { padding: 16px; }
  .dia { grid-template-columns: 58px 1fr; row-gap: 4px; }
  .dia-tempo { grid-column: 2; text-align: left; }
  .dia-tempo small { display: inline; margin-left: 6px; }
}
</style>
"""


def html(trecho: str) -> None:
    st.markdown(trecho, unsafe_allow_html=True)


def normalizar(texto: str) -> str:
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


def url_maps(busca: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={quote(busca)}"


def libras(valor: float) -> str:
    return "£" + f"{valor:,.0f}".replace(",", ".")


def classe_tag(tag: str) -> str:
    t = normalizar(tag)
    if "fechad" in t or "esgotad" in t:
        return "tag fechado"
    if "gratis" in t:
        return "tag gratis"
    if "reserv" in t or "hora marcada" in t:
        return "tag reserva"
    if "wi-fi" in t or "tomada" in t or "chamada" in t:
        return "tag trabalho"
    if t == "show":
        return "tag show"
    if "pag" in t or "£" in tag:
        return "tag pago"
    return "tag"


def tags_html(tags: list[str]) -> str:
    return '<div class="tags">' + "".join(f'<span class="{classe_tag(t)}">{escape(t)}</span>' for t in tags) + "</div>"


def celular() -> bool:
    agente = st.context.headers.get("User-Agent", "")
    return "Mobi" in agente or "Android" in agente

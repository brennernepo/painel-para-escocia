"""Visual: loja de discos à noite. Fundo escuro, âmbar de válvula, capas em destaque."""

from html import escape
from urllib.parse import quote

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap');
:root { --bg:#141113; --card:#1E1A1D; --card2:#26211F; --linha:#3A322D; --txt:#EFE7DC; --txt2:#BDB2A5; --txt3:#8C8177;
        --ambar:#F2A541; --vermelho:#E5484D; --verde:#4CC38A; --azul:#6AA8F0; }
html, body, .stApp, .stMarkdown, p, label, input, textarea, button { font-family: 'DM Sans', sans-serif; }
[data-testid="stIconMaterial"], .material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }
.stApp { background: radial-gradient(1200px 500px at 10% -10%, #2A1F17 0%, var(--bg) 55%); }
.titulo { font-family:'Bebas Neue', sans-serif; font-size:52px; letter-spacing:1px; line-height:1; color:var(--txt); margin:4px 0 2px; }
.titulo span { color:var(--ambar); }
.sub { color:var(--txt2); font-size:15px; margin-bottom:14px; }
.rotulo { font-family:'Bebas Neue', sans-serif; font-size:24px; letter-spacing:.6px; color:var(--ambar); margin:18px 0 6px; }
.cartao-banda { background:var(--card); border:1px solid var(--linha); border-radius:16px; overflow:hidden; margin-bottom:6px; }
.cartao-banda .foto { width:100%; aspect-ratio:1/1; object-fit:cover; display:block; background:#2b2420; }
.cartao-banda .sem-foto { width:100%; aspect-ratio:1/1; display:flex; align-items:center; justify-content:center;
  font-family:'Bebas Neue'; font-size:64px; color:var(--ambar); background:linear-gradient(135deg,#2b2420,#3a2a1c); }
.cartao-banda .corpo { padding:10px 12px 12px; }
.cartao-banda .nome { font-weight:700; font-size:16px; color:var(--txt); line-height:1.2; }
.cartao-banda .meta { font-size:12px; color:var(--txt3); margin-top:2px; }
.barra { height:5px; background:#3a322d; border-radius:99px; margin-top:8px; overflow:hidden; }
.barra i { display:block; height:100%; background:var(--ambar); }
.chips { display:flex; flex-wrap:wrap; gap:5px; margin-top:6px; }
.chip { font-size:11px; padding:2px 9px; border-radius:99px; background:#2f2824; color:var(--txt2); white-space:nowrap; }
.chip.ambar { background:#3d2c15; color:var(--ambar); }
.chip.verde { background:#173326; color:var(--verde); }
.chip.vermelho { background:#3b1a1c; color:#FF8A8D; }
.chip.azul { background:#172a40; color:var(--azul); }
.cabeca { display:flex; gap:22px; align-items:flex-end; margin:6px 0 10px; flex-wrap:wrap; }
.cabeca img, .cabeca .sem-foto { width:190px; height:190px; border-radius:18px; object-fit:cover; box-shadow:0 10px 30px #0008; }
.cabeca .sem-foto { display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue'; font-size:80px;
  color:var(--ambar); background:linear-gradient(135deg,#2b2420,#3a2a1c); }
.cabeca .nome { font-family:'Bebas Neue'; font-size:64px; line-height:.95; color:var(--txt); }
.cabeca .meta { color:var(--txt2); font-size:15px; margin-top:6px; }
.bio { color:var(--txt); font-size:15px; line-height:1.65; max-width:820px; }
.bio-fonte { font-size:12px; color:var(--txt3); margin-top:4px; }
.curiosidade { background:#2a2116; border-left:3px solid var(--ambar); border-radius:10px; padding:10px 14px;
  color:#F5DEB8; font-size:14px; line-height:1.55; margin:10px 0; max-width:820px; }
.capa { width:100%; aspect-ratio:1/1; object-fit:cover; border-radius:10px; box-shadow:0 6px 18px #0009; display:block; }
.sem-capa { width:100%; aspect-ratio:1/1; border-radius:10px; display:flex; align-items:center; justify-content:center;
  background:repeating-radial-gradient(circle at 50% 50%, #1b1718 0 3px, #241f1f 3px 5px); color:var(--txt3); font-size:30px; }
.album-titulo { font-weight:700; font-size:18px; color:var(--txt); line-height:1.25; }
.album-meta { color:var(--txt3); font-size:13px; margin:2px 0 4px; }
.album-curio { color:var(--txt2); font-size:13.5px; line-height:1.5; margin-top:6px; }
.links { font-size:12.5px; margin-top:8px; }
.links a { color:var(--ambar) !important; text-decoration:none; margin-right:12px; }
.links a:hover { text-decoration:underline; }
.faixas { font-size:13px; color:var(--txt2); columns:2; column-gap:24px; }
.faixas div { break-inside:avoid; padding:1px 0; }
.faixas b { color:var(--txt3); font-weight:500; display:inline-block; width:24px; }
.faixas span { color:var(--txt3); }
.mini { display:flex; gap:10px; align-items:center; }
.mini img, .mini .sem-capa { width:64px; min-width:64px; height:64px; border-radius:8px; object-fit:cover; font-size:18px; }
.mini .t { font-weight:700; color:var(--txt); font-size:14px; line-height:1.2; }
.mini .s { color:var(--txt3); font-size:12px; }
.porque { color:var(--txt2); font-size:12.5px; margin-top:6px; line-height:1.45; }
.numero { background:var(--card); border:1px solid var(--linha); border-radius:14px; padding:12px 16px; }
.numero b { font-family:'Bebas Neue'; font-size:40px; color:var(--ambar); display:block; line-height:1; }
.numero span { color:var(--txt2); font-size:13px; }
.aviso { color:var(--txt3); font-size:12.5px; font-style:italic; margin-top:6px; }
.moldura { position:relative; overflow:hidden; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg,#2b2420,#3a2a1c); font-family:'Bebas Neue'; color:var(--ambar); }
.moldura.vinil { background:repeating-radial-gradient(circle at 50% 50%, #1b1718 0 3px, #241f1f 3px 5px); }
.moldura span { font-size:56px; }
.moldura img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; font-size:0; color:transparent; }
.moldura.foto { width:100%; aspect-ratio:1/1; }
.moldura.capa { width:100%; aspect-ratio:1/1; border-radius:10px; box-shadow:0 6px 18px #0009; }
.moldura.capa span { font-size:34px; }
.cabeca .moldura { width:190px; height:190px; border-radius:18px; box-shadow:0 10px 30px #0008; }
.cabeca .moldura span { font-size:80px; }
.mini .moldura { width:64px; min-width:64px; height:64px; border-radius:8px; }
.mini .moldura span { font-size:22px; }
</style>
"""


def html(trecho: str) -> None:
    st.html(trecho)


def iniciais(nome: str) -> str:
    partes = [p for p in nome.replace("The ", "").split() if p[:1].isalnum()]
    return "".join(p[0] for p in partes[:2]).upper() or "♪"


def foto_banda(b: dict, classe: str = "foto") -> str:
    """Foto sobre um fundo com as iniciais: se a imagem não carregar, fica o fundo."""
    img = f'<img src="{escape(b["foto"])}" loading="lazy" alt="">' if b.get("foto") else ""
    return f'<div class="moldura {classe}"><span>{escape(iniciais(b["nome"]))}</span>{img}</div>'


def capa(a: dict, classe: str = "capa") -> str:
    """Capa sobre um fundo de vinil: se a imagem não carregar, fica o vinil."""
    img = f'<img src="{escape(a["capa"])}" loading="lazy" alt="">' if a.get("capa") else ""
    return f'<div class="moldura vinil {classe}"><span>💿</span>{img}</div>'


def chips(itens: list[tuple[str, str]]) -> str:
    return '<div class="chips">' + "".join(f'<span class="chip {c}">{escape(t)}</span>' for t, c in itens if t) + "</div>"


def anos(b: dict) -> str:
    if b.get("inicio") and b.get("fim"):
        return f"{b['inicio']}–{b['fim']}"
    if b.get("inicio"):
        return f"desde {b['inicio']}"
    return ""


def situacao(b: dict) -> tuple[str, str]:
    if b.get("ativa") is True:
        return "na ativa", "verde"
    if b.get("ativa") is False:
        return "encerrada", "vermelho"
    return "", ""


def links_ouvir(banda: str, album: str, wikipedia: str | None) -> str:
    q = quote(f"{banda} {album}")
    partes = [f'<a href="https://open.spotify.com/search/{q}" target="_blank">Spotify</a>',
              f'<a href="https://music.youtube.com/search?q={q}" target="_blank">YouTube Music</a>',
              f'<a href="https://www.deezer.com/search/{q}" target="_blank">Deezer</a>']
    if wikipedia:
        partes.append(f'<a href="{escape(wikipedia)}" target="_blank">Wikipedia</a>')
    return '<div class="links">▶ Ouvir: ' + "".join(partes) + "</div>"


def data_br(data: str) -> str:
    """2026-11-20 → 20/11/2026; datas incompletas ficam como vieram (2027, 2027-03)."""
    partes = (data or "").split("-")
    return "/".join(reversed(partes)) if len(partes) == 3 else (data or "")


def nota_fmt(v: float | None) -> str:
    return "" if v is None else (f"{v:.1f}".replace(".", ",").replace(",0", ""))

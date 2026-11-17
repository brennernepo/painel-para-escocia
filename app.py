import hmac
import random
from collections import Counter, defaultdict
from datetime import date, timedelta
from html import escape

import pandas as pd
import streamlit as st
import streamlit.components.v1 as componentes

import banco
from catalogo import albuns_por_id, carregar, slug, versao_dos_dados
from estilo import (CSS, anos, capa, chips, data_br, enderecos, foto_banda, html, links_ouvir, lista_faixas, nota_fmt,
                    situacao)

st.set_page_config(page_title="Discoteca", page_icon="💿", layout="wide")
st.html(CSS)

LISTAS = {"Rolling Stone 500": "RS 500", "Rolling Stone 100 do metal": "RS Metal", "Rolling Stone 50 do grunge": "RS Grunge",
          "Rolling Stone 40 do punk": "RS Punk", "Apple Music 100": "Apple 100", "The Guardian 100": "Guardian 100"}
NOTAS = ["—"] + [nota_fmt(n / 2) for n in range(20, -1, -1)]
GOSTO = {-1: "🚫 Não curto", 0: "😐 Neutro", 1: "👍 Gosto", 2: "🔥 Favorita"}
POR_PAGINA = 24


def pedir_senha() -> None:
    """Só pede senha se houver uma nos Secrets do app."""
    try:
        senha = str(st.secrets.get("senha", ""))
    except Exception:
        senha = ""
    if not senha or st.session_state.get("liberado"):
        return
    with st.form("senha"):
        tentativa = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar", type="primary")
    if entrar and hmac.compare_digest(tentativa.encode(), senha.encode()):
        st.session_state.liberado = True
        st.rerun()
    if entrar:
        st.error("Senha errada.")
    st.stop()


pedir_senha()
banco.iniciar()
BANDAS = carregar(versao_dos_dados())
ALBUNS = albuns_por_id(BANDAS)
POR_DEEZER = {b["deezer"]: b["id"] for b in BANDAS.values() if b.get("deezer")}
if st.session_state.get("somente_leitura"):
    st.warning("O banco de notas está fora do ar: mostrando a cópia de segurança, sem edição.", icon="⚠️")


# ---------------------------------------------------------------------------
# Estado do usuário
# ---------------------------------------------------------------------------
def estado_banda(b: dict) -> dict:
    """Resumo do que você já fez com a banda: conhece, gosto, escutados e notas."""
    meu = banco.banda(b["id"])
    escutados = [a for a in b["albuns"] if banco.album(a["id"]).get("escutei")]
    notas = [banco.album(a["id"])["nota"] for a in b["albuns"] if banco.album(a["id"]).get("nota") is not None]
    conhece = meu.get("conheco") or bool(escutados) or any(banco.album(a["id"]).get("conheco") for a in b["albuns"])
    return {"conhece": conhece, "gosto": meu.get("gosto"), "escutados": len(escutados), "lista": bool(meu.get("quero_ouvir")),
            "media": round(sum(notas) / len(notas), 1) if notas else None}


def abrir_banda(banda_id: str) -> None:
    st.session_state.banda_id = banda_id
    st.switch_page(PAGINAS["banda"])


def abrir_album(album_id: str) -> None:
    st.session_state.album_id = album_id
    st.switch_page(PAGINAS["album"])


def album_sugerido(b: dict) -> dict | None:
    """Por onde começar a banda; se você já ouviu esse, o melhor que ainda falta."""
    porta = ALBUNS.get(b.get("porta_de_entrada") or "")
    if porta and not banco.album(porta["id"]).get("escutei"):
        return porta
    faltam = [a for a in b["albuns"] if not a["futuro"] and not banco.album(a["id"]).get("escutei")]
    return max(faltam, key=lambda a: (a["nota_critica"] or 0) + 0.7 * len(a.get("listas", [])), default=None)


def iniciar_chave(chave: str, valor) -> None:
    if chave not in st.session_state:
        st.session_state[chave] = valor


def ao_mudar_album(album_id: str, banda_id: str, campo: str, chave: str) -> None:
    valor = st.session_state[chave]
    if campo == "nota":
        valor = None if valor == "—" else float(valor.replace(",", "."))
    elif campo == "escutado_em":
        valor = valor.isoformat() if valor else None
    elif campo == "faixa_favorita":
        valor = None if valor == "—" else valor
    if banco.salvar_album(album_id, banda_id, **{campo: valor}) and campo in ("escutei", "nota") and valor:
        st.session_state[f"conheco_{album_id}"] = True


def ao_mudar_banda(banda_id: str, campo: str, chave: str) -> None:
    valor = st.session_state[chave]
    if campo == "gosto":
        valor = next((k for k, v in GOSTO.items() if v == valor), None)
    banco.salvar_banda(banda_id, **{campo: valor})


def ficha_md(a: dict) -> str:
    """O álbum com suas notas, pronto para colar no rascunho de um post."""
    b, e = BANDAS[a["banda_id"]], banco.album(a["id"])
    linhas = [f"# {a['titulo']}", f"**{b['nome']}** · {data_br(a['data'])}", ""]
    dados = [("Minha nota", nota_fmt(e.get("nota"))), ("Crítica", nota_fmt(a["nota_critica"])),
             ("Faixa favorita", e.get("faixa_favorita")), ("Escutei em", data_br(e.get("escutado_em") or "")),
             ("Duração", f"{a['duracao_min']} min" if a.get("duracao_min") else "")]
    linhas += [f"- {k}: {v}" for k, v in dados if v]
    if e.get("comentario"):
        linhas += ["", "## O que achei", "", e["comentario"]]
    if a.get("curiosidade"):
        linhas += ["", "## Curiosidade", "", a["curiosidade"]]
    if a.get("historia"):
        linhas += ["", "## A história do disco", "", a["historia"]]
    if a["faixas"]:
        linhas += ["", "## Faixas", ""]
        for f in a["faixas"]:
            linhas.append(f"{f['n']}. {f['titulo']}" + (f" ({f['duracao']})" if f["duracao"] else ""))
            if f.get("significado"):
                linhas.append(f"   {f['significado']}")
    return "\n".join(linhas) + "\n"


def controles_album(a: dict) -> None:
    e = banco.album(a["id"])
    args = lambda campo, chave: {"on_change": ao_mudar_album, "args": (a["id"], a["banda_id"], campo, chave)}
    c1, c2 = st.columns(2)
    for col, campo, rotulo in ((c1, "conheco", "Conheço"), (c2, "escutei", "Escutei inteiro"),
                               (c1, "quero_ouvir", "Quero ouvir"), (c2, "favorito", "Favorito ❤"),
                               (c1, "em_rotacao", "Em rotação 🔁")):
        chave = f"{campo}_{a['id']}"
        iniciar_chave(chave, bool(e.get(campo)))
        col.checkbox(rotulo, key=chave, **args(campo, chave))
    chave = f"nota_{a['id']}"
    iniciar_chave(chave, nota_fmt(e.get("nota")) if e.get("nota") is not None else "—")
    st.selectbox("Minha nota (0 a 10)", NOTAS, key=chave, **args("nota", chave))
    with st.expander("Mais: faixa favorita, data, comentário"):
        faixas = ["—"] + [f["titulo"] for f in a["faixas"]]
        chave = f"faixa_{a['id']}"
        iniciar_chave(chave, e.get("faixa_favorita") if e.get("faixa_favorita") in faixas else "—")
        st.selectbox("Faixa favorita", faixas, key=chave, **args("faixa_favorita", chave))
        chave = f"data_{a['id']}"
        iniciar_chave(chave, date.fromisoformat(e["escutado_em"]) if e.get("escutado_em") else None)
        st.date_input("Escutei em", key=chave, format="DD/MM/YYYY", **args("escutado_em", chave))
        chave = f"coment_{a['id']}"
        iniciar_chave(chave, e.get("comentario") or "")
        st.text_area("Comentário (vale como rascunho de post)", key=chave, max_chars=2000, **args("comentario", chave))
        st.download_button("⬇ Ficha em Markdown (para o blog)", ficha_md(a), file_name=f"{slug(a['titulo'])}.md",
                           mime="text/markdown", key=f"md_{a['id']}", on_click="ignore")


def chips_album(a: dict) -> str:
    c = a.get("critica") or {}
    meu = banco.album(a["id"])
    itens = [(f"Crítica {nota_fmt(a['nota_critica'])}" if a["nota_critica"] is not None else "", "ambar"),
             (f"AllMusic {nota_fmt(c['allmusic'])}" if c.get("allmusic") is not None else "", ""),
             (f"Metacritic {c['metacritic']}" if c.get("metacritic") else "", ""),
             (f"Público {nota_fmt(a['publico'])}" if a.get("publico") is not None and a.get("publico_votos", 0) >= 2 else "", ""),
             (f"Sua nota {nota_fmt(meu['nota'])}" if meu.get("nota") is not None else "", "azul"),
             ("✓ escutado" if meu.get("escutei") else "", "verde"),
             ("na fila" if meu.get("quero_ouvir") and not meu.get("escutei") else "", "vermelho"),
             (f"em breve · {data_br(a['data'])}" if a["futuro"] else "", "azul"),
             ("🔁 em rotação" if meu.get("em_rotacao") else "", "ambar")]
    itens += [(f"🏆 {LISTAS.get(l['lista'], l['lista'])}" + (f" · #{l['posicao']}" if l["posicao"] and l["lista"] != "1001 Discos"
               else ""), "verde") for l in a.get("listas", [])]
    return chips(itens)


SERVICOS = {"deezer": ("Deezer", "https://widget.deezer.com/widget/dark/album/{}", 300),
            "spotify": ("Spotify", "https://open.spotify.com/embed/album/{}?theme=0", 352),
            "youtube": ("YouTube", "https://www.youtube.com/embed/videoseries?list={}", 315)}


def tocar(album_id: str, servico: str) -> None:
    st.session_state.tocando = None if st.session_state.get("tocando") == (album_id, servico) else (album_id, servico)


def player(a: dict, onde) -> None:
    """Botões para tocar o álbum aqui mesmo. Só um player fica aberto por vez, para a página não pesar."""
    servicos = [s for s in SERVICOS if a.get(s)]
    if not servicos or a["futuro"]:
        return
    tocando = st.session_state.get("tocando")
    with onde.container(horizontal=True, gap="small"):
        for s in servicos:
            ativo = tocando == (a["id"], s)
            st.button(("⏹ Fechar " if ativo else "▶ Tocar no ") + SERVICOS[s][0], key=f"tocar_{s}_{a['id']}",
                      on_click=tocar, args=(a["id"], s), type="primary" if ativo else "secondary")
    if tocando and tocando[0] == a["id"] and tocando[1] in servicos:
        _, url, altura = SERVICOS[tocando[1]]
        with onde:
            componentes.iframe(url.format(a[tocando[1]]), height=altura)
        onde.caption("Toca completo se você estiver logado no serviço neste navegador (no Spotify, com Premium e no "
                     "computador); sem login, só prévias de 30 segundos.")


def bloco_album(a: dict, banda: dict, com_banda: bool = False) -> None:
    with st.container(border=True):
        c_capa, c_info, c_ctrl = st.columns([1.1, 3.1, 2.1], gap="medium")
        c_capa.html(capa(a, link=enderecos(banda["nome"], a)["Spotify"]))
        meta = " · ".join(x for x in (a.get("data", "")[:4], f"{len(a['faixas'])} faixas" if a["faixas"] else "",
                                       f"{a['duracao_min']} min" if a.get("duracao_min") else "") if x)
        nome_banda = f'<div class="album-meta" style="color:var(--ambar)">{escape(banda["nome"])}</div>' if com_banda else ""
        c_capa.button("Página do álbum", key=f"pag_{a['id']}", on_click=abrir_album, args=(a["id"],), width="stretch")
        curio = f'<div class="album-curio">💡 {escape(a["curiosidade"])}</div>' if a.get("curiosidade") else ""
        c_info.html(f'{nome_banda}<div class="album-titulo">{escape(a["titulo"])}</div>'
                    f'<div class="album-meta">{escape(meta)}</div>{chips_album(a)}{curio}'
                    f'{links_ouvir(banda["nome"], a)}')
        player(a, c_info)
        if a.get("historia"):
            with c_info.expander("A história do disco"):
                st.html(f'<div class="historia">{escape(a["historia"])}</div>')
        if a["faixas"]:
            com_sig = sum(1 for f in a["faixas"] if f.get("significado"))
            with c_info.expander(f"Faixas ({len(a['faixas'])})" + (" · com significados" if com_sig else "")):
                st.html(lista_faixas(banda["nome"], a, banco.album(a["id"]).get("faixa_favorita")))
        with c_ctrl:
            controles_album(a)


def marcar_banda(banda_id: str, gosto: int | None) -> None:
    banco.salvar_banda(banda_id, conheco=True, **({"gosto": gosto} if gosto is not None else {}))


def alternar_lista(banda_id: str) -> None:
    banco.salvar_banda(banda_id, quero_ouvir=not banco.banda(banda_id).get("quero_ouvir"))
    st.session_state.pop(f"blista_{banda_id}", None)  # o botão da página da banda relê o valor


def cartao_banda(b: dict, col, contexto: str, porque: str = "", acoes: bool = False) -> None:
    e = estado_banda(b)
    total = len(b["albuns"])
    sit, cor = situacao(b)
    meta = " · ".join(x for x in (b["pais_nome"], anos(b), f"{total} álbuns") if x)
    porque_html = f'<div class="porque">{escape(porque)}</div>' if porque else ""
    col.html(
        f'<div class="cartao-banda">{foto_banda(b)}<div class="corpo"><div class="nome">{escape(b["nome"])}</div>'
        f'<div class="meta">{escape(meta)}</div>'
        f'{chips([(g, "") for g in b["generos"][:2]] + [(sit, cor), (GOSTO.get(e["gosto"], "") if e["gosto"] else "", "ambar"), ("na sua lista" if e["lista"] else "", "azul")])}'
        f'<div class="barra"><i style="width:{(e["escutados"] / total * 100) if total else 0:.0f}%"></i></div>'
        f'<div class="meta">{e["escutados"]} de {total} escutados</div>{porque_html}</div></div>'
    )
    sugerido = album_sugerido(b)
    if sugerido:
        titulo = sugerido["titulo"] if len(sugerido["titulo"]) <= 26 else sugerido["titulo"][:25] + "…"
        col.button(f"💿 {titulo}", key=f"sug_{contexto}_{b['id']}", on_click=abrir_album, args=(sugerido["id"],),
                   width="stretch", help="Abrir o álbum sugerido para começar (ou o próximo que falta)")
    c1, c2 = col.columns(2)
    c1.button("Banda", key=f"abrir_{contexto}_{b['id']}", on_click=abrir_banda, args=(b["id"],), width="stretch")
    c2.button("✓ Na lista" if e["lista"] else "＋ Lista", key=f"lista_{contexto}_{b['id']}", on_click=alternar_lista,
              args=(b["id"],), width="stretch", help="Coloca a banda em Minhas bandas, para ouvir")
    if acoes:
        c1, c2 = col.columns(2)
        c1.button("Já conheço", key=f"conh_{contexto}_{b['id']}", on_click=marcar_banda, args=(b["id"], None),
                  width="stretch")
        c2.button("Não curto", key=f"nao_{contexto}_{b['id']}", on_click=marcar_banda, args=(b["id"], -1),
                  width="stretch")


def grade_bandas(lista: list[dict], contexto: str, porques: dict | None = None, acoes: bool = False) -> None:
    for i in range(0, len(lista), 4):
        cols = st.columns(4)
        for col, b in zip(cols, lista[i:i + 4]):
            cartao_banda(b, col, contexto, (porques or {}).get(b["id"], ""), acoes)


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------
def pagina_acervo() -> None:
    conhecidas = sum(1 for b in BANDAS.values() if estado_banda(b)["conhece"])
    escutados = sum(1 for a in ALBUNS.values() if banco.album(a["id"]).get("escutei"))
    html(f'<div class="titulo">O <span>acervo</span></div>'
         f'<div class="sub">{len(BANDAS)} bandas · {len(ALBUNS)} álbuns de estúdio · você conhece {conhecidas} bandas '
         f'e já escutou {escutados} álbuns. Use “＋ Lista” para levar uma banda para Minhas bandas.</div>')
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 1.6, 1.4])
    busca = c1.text_input("Buscar banda ou gênero", placeholder="Ex.: Soundgarden, thrash, Brasil…")
    cenas = sorted({b["cena"] for b in BANDAS.values()})
    escolhidas = c2.multiselect("Cena", cenas, placeholder="Todas")
    filtro = c3.selectbox("Mostrar", ["Todas", "Na minha lista", "Que conheço", "Que não conheço", "Favoritas", "Na ativa",
                                       "Encerradas"])
    ordem = c4.selectbox("Ordem", ["A–Z", "Mais escutadas", "Melhor crítica", "Mais antigas", "Mais novas"])
    termo = busca.lower().strip()
    lista = []
    for b in BANDAS.values():
        e = estado_banda(b)
        texto = " ".join([b["nome"], b["cena"], " ".join(b["generos"]), b.get("pais") or "",
                          "brasil" if b.get("pais") == "BR" else ""]).lower()
        if termo and termo not in texto:
            continue
        if escolhidas and b["cena"] not in escolhidas:
            continue
        if (filtro == "Na minha lista" and not e["lista"]) or (filtro == "Que conheço" and not e["conhece"]) or (filtro == "Que não conheço" and e["conhece"]) \
                or (filtro == "Favoritas" and e["gosto"] != 2) or (filtro == "Na ativa" and b.get("ativa") is not True) \
                or (filtro == "Encerradas" and b.get("ativa") is not False):
            continue
        lista.append(b)
    chaves = {"A–Z": lambda b: b["nome"].lower().removeprefix("the "),
              "Mais escutadas": lambda b: -estado_banda(b)["escutados"],
              "Melhor crítica": lambda b: -(b["critica_media"] or 0),
              "Mais antigas": lambda b: b.get("inicio") or "9999",
              "Mais novas": lambda b: -(int(b.get("inicio") or 0))}
    lista.sort(key=chaves[ordem])
    paginas = max(1, -(-len(lista) // POR_PAGINA))
    if st.session_state.get("pag_bandas", 1) > paginas:
        st.session_state.pag_bandas = 1
    pagina = st.session_state.get("pag_bandas", 1)
    grade_bandas(lista[(pagina - 1) * POR_PAGINA: pagina * POR_PAGINA], "lista")
    if paginas > 1:
        st.select_slider("Página", options=list(range(1, paginas + 1)), key="pag_bandas")
    if not lista:
        st.info("Nenhuma banda com esse filtro.")
    pedidos_abertos = sorted(p for p in banco.pedidos() if slug(p) not in BANDAS)
    with st.expander("Não achou uma banda? Peça para entrar no acervo"):
        with st.form("pedido", clear_on_submit=True, border=False):
            nome = st.text_input("Banda ou artista", placeholder="Ex.: Humble Pie, Nina Simone…")
            if st.form_submit_button("Pedir") and nome.strip():
                if banco.pedir_banda(nome.strip(), "acervo"):
                    st.success(f"Pedido anotado: {nome.strip()}. Entra no acervo na próxima atualização de segunda-feira.")
        if pedidos_abertos:
            st.caption("Na fila para entrar: " + ", ".join(pedidos_abertos))


def pagina_banda() -> None:
    nomes = {b["id"]: b["nome"] for b in sorted(BANDAS.values(), key=lambda b: b["nome"].lower())}
    atual = st.session_state.get("banda_id") or next(iter(nomes))
    escolha = st.selectbox("Banda", list(nomes), index=list(nomes).index(atual) if atual in nomes else 0,
                           format_func=nomes.get, label_visibility="collapsed")
    st.session_state.banda_id = escolha
    b = BANDAS[escolha]
    e = estado_banda(b)
    sit, cor = situacao(b)
    meta = " · ".join(x for x in (b["pais_nome"], anos(b), b["cena"]) if x)
    html(f'<div class="cabeca">{foto_banda(b, "")}<div><div class="nome">{escape(b["nome"])}</div>'
         f'<div class="meta">{escape(meta)}</div>'
         f'{chips([(g, "") for g in b["generos"]] + [(sit, cor)] + premios(b))}</div></div>')
    c1, c3, c2 = st.columns([1.2, 1.3, 3.5])
    chave = f"blista_{b['id']}"
    iniciar_chave(chave, e["lista"])
    c3.toggle("Na minha lista", key=chave, on_change=ao_mudar_banda, args=(b["id"], "quero_ouvir", chave),
              help="Minhas bandas: as que você quer ouvir")
    chave = f"bconheco_{b['id']}"
    iniciar_chave(chave, bool(banco.banda(b["id"]).get("conheco") or e["conhece"]))
    c1.toggle("Conheço a banda", key=chave, on_change=ao_mudar_banda, args=(b["id"], "conheco", chave))
    chave = f"bgosto_{b['id']}"
    iniciar_chave(chave, GOSTO.get(e["gosto"]))
    c2.segmented_control("O que acho", list(GOSTO.values()), key=chave, label_visibility="collapsed",
                         on_change=ao_mudar_banda, args=(b["id"], "gosto", chave))
    notas = f"sua média {nota_fmt(e['media'])} · " if e["media"] is not None else ""
    critica = f"crítica média {nota_fmt(b['critica_media'])}" if b["critica_media"] is not None else ""
    html(f'<div class="sub" style="margin:0 0 8px">{e["escutados"]} de {len(b["albuns"])} álbuns escutados · '
            f'{notas}{critica}</div>')
    if b["bio"]:
        fonte = "Resumo da Wikipedia em inglês" if b["bio_em_ingles"] else "Com base na Wikipedia"
        link = f' · <a href="{escape(b["wikipedia"])}" target="_blank" style="color:var(--ambar)">ler mais</a>' if b.get("wikipedia") else ""
        html(f'<div class="bio">{escape(b["bio"])}</div><div class="bio-fonte">{fonte}{link}</div>')
    if b.get("curiosidade"):
        html(f'<div class="curiosidade">💡 {escape(b["curiosidade"])}</div>')
    html('<div class="rotulo">Discografia de estúdio</div>')
    f1, f2 = st.columns([3, 1.4])
    filtro = f1.segmented_control("Álbuns", ["Todos", "Não escutados", "Escutados", "Na fila"], default="Todos",
                                  key=f"filtro_{b['id']}", label_visibility="collapsed")
    ordem = f2.selectbox("Ordem", ["Lançamento", "Melhor crítica", "Minha nota"], key=f"ordem_{b['id']}",
                         label_visibility="collapsed")
    porta = b.get("porta_de_entrada")
    if porta and not e["escutados"]:
        st.caption(f"Por onde começar: **{ALBUNS[porta]['titulo']}**, o que melhor junta crítica e popularidade.")
    albuns = [a for a in b["albuns"] if not (
        (filtro == "Não escutados" and banco.album(a["id"]).get("escutei"))
        or (filtro == "Escutados" and not banco.album(a["id"]).get("escutei"))
        or (filtro == "Na fila" and not banco.album(a["id"]).get("quero_ouvir")))]
    if ordem == "Melhor crítica":
        albuns.sort(key=lambda a: -(a["nota_critica"] if a["nota_critica"] is not None else -1))
    elif ordem == "Minha nota":
        albuns.sort(key=lambda a: -(banco.album(a["id"]).get("nota") if banco.album(a["id"]).get("nota") is not None else -1))
    limite = len(albuns) if st.session_state.get(f"todos_{b['id']}") else 20
    for a in albuns[:limite]:
        bloco_album(a, b)
    if len(albuns) > limite:
        st.button(f"Mostrar os outros {len(albuns) - limite} álbuns", key=f"btodos_{b['id']}",
                  on_click=lambda k=f"todos_{b['id']}": st.session_state.update({k: True}))
    if not b["albuns"]:
        st.info("Não achei álbuns de estúdio desta banda no MusicBrainz.")
    parecidas(b)


def premios(b: dict) -> list[tuple[str, str]]:
    p = b.get("premios") or {}
    hall = p.get("hall_da_fama")
    return [(f"🏛 Hall da Fama do Rock{f' · {hall}' if isinstance(hall, int) else ''}" if hall else "", "verde"),
            (f"🏆 {p['grammys']} Grammy{'s' if p['grammys'] > 1 else ''}" if p.get("grammys") else "", "verde")]


def no_acervo(p: dict) -> str | None:
    """Id no acervo de um artista do Deezer: pelo id do Deezer ou, na falta dele, pelo nome."""
    return POR_DEEZER.get(p["deezer"]) or (slug(p["nome"]) if slug(p["nome"]) in BANDAS else None)


def parecidas(b: dict) -> None:
    """Artistas que o Deezer relaciona a esta banda: os do acervo viram cartões; os de fora podem ser pedidos."""
    if not b.get("parecidas"):
        return
    dentro = [BANDAS[no_acervo(p)] for p in b["parecidas"] if no_acervo(p) not in (None, b["id"])][:8]
    fora = [p for p in b["parecidas"] if not no_acervo(p)][:10]
    html('<div class="rotulo">Parecidas</div>')
    if dentro:
        grade_bandas(dentro, f"par_{b['id']}")
    if fora:
        st.caption("Fora do acervo (segundo o Deezer). Clique para pedir que entrem na próxima atualização:")
        botoes_pedido(fora, f"par_{b['id']}", b["nome"])


def botoes_pedido(artistas: list[dict], contexto: str, origem: str) -> None:
    pedidos = banco.pedidos()
    with st.container(horizontal=True, gap="small"):
        for p in artistas:
            ja = p["nome"] in pedidos
            st.button(("✓ " if ja else "＋ ") + p["nome"], key=f"ped_{contexto}_{p['deezer']}", disabled=ja,
                      on_click=banco.pedir_banda, args=(p["nome"], f"parecida com {origem}"))


def pagina_minhas() -> None:
    html('<div class="titulo">Minhas <span>bandas</span></div>'
         '<div class="sub">Só o que você marcou: as bandas que quer ouvir e as que já curte.</div>')
    grupos = {"Para ouvir": [], "Favoritas": [], "Curto": []}
    for b in BANDAS.values():
        e = estado_banda(b)
        if e["lista"]:
            grupos["Para ouvir"].append(b)
        elif e["gosto"] == 2:
            grupos["Favoritas"].append(b)
        elif e["gosto"] == 1:
            grupos["Curto"].append(b)
    if not any(grupos.values()):
        st.info("Ainda vazio. Use “＋ Lista” nos cartões do Acervo e do Descobrir, ou o botão “Na minha lista” na página "
                "de uma banda, e ela aparece aqui. Bandas marcadas como “Gosto” ou “Favorita” também entram.")
        return
    for titulo, lista in grupos.items():
        if lista:
            html(f'<div class="rotulo">{titulo} · {len(lista)}</div>')
            grade_bandas(sorted(lista, key=lambda b: b["nome"].lower().removeprefix("the ")), f"minhas_{titulo}")


def pagina_album() -> None:
    aid = st.session_state.get("album_id") or st.query_params.get("id")
    if aid not in ALBUNS:
        opcoes = sorted(ALBUNS, key=lambda i: (BANDAS[ALBUNS[i]["banda_id"]]["nome"].lower(), ALBUNS[i]["data"]))
        aid = st.selectbox("Álbum", opcoes, index=None, placeholder="Busque um álbum pelo nome ou pela banda",
                           format_func=lambda i: f"{ALBUNS[i]['titulo']} · {BANDAS[ALBUNS[i]['banda_id']]['nome']} ({ALBUNS[i]['ano']})")
        if not aid:
            st.caption("Ou use o botão “Álbum” em qualquer sugestão.")
            return
    st.session_state.album_id = aid
    st.query_params["id"] = aid  # o endereço da página fica guardável
    a = ALBUNS[aid]
    b = BANDAS[a["banda_id"]]
    links = enderecos(b["nome"], a)
    c_capa, c_info = st.columns([1.15, 2.6], gap="large")
    c_capa.html(capa(a, link=links["Spotify"]))
    c_capa.button(f"🎸 {b['nome']}", key="alb_banda", on_click=abrir_banda, args=(b["id"],), width="stretch")
    meta = " · ".join(x for x in (data_br(a.get("data", "")), f"{len(a['faixas'])} faixas" if a["faixas"] else "",
                                   f"{a['duracao_min']} min" if a.get("duracao_min") else "") if x)
    curio = f'<div class="curiosidade">💡 {escape(a["curiosidade"])}</div>' if a.get("curiosidade") else ""
    c_info.html(f'<div class="album-meta" style="color:var(--ambar);font-size:15px">{escape(b["nome"])}</div>'
                f'<div class="cabeca" style="margin:0"><div class="nome" style="font-size:52px">{escape(a["titulo"])}</div></div>'
                f'<div class="album-meta">{escape(meta)}</div>{chips_album(a)}{curio}{links_ouvir(b["nome"], a)}')
    player(a, c_info)
    if a.get("historia"):
        html('<div class="rotulo">A história do disco</div>')
        html(f'<div class="historia">{escape(a["historia"])}</div>')
    elif a.get("resumo_en"):
        with c_info.expander("Sobre o disco (Wikipedia, em inglês)"):
            st.write(a["resumo_en"])
    c_faixas, c_meu = st.columns([2.2, 1.6], gap="large")
    with c_faixas:
        html('<div class="rotulo">Faixas</div>')
        if a["faixas"]:
            st.html(lista_faixas(b["nome"], a, banco.album(a["id"]).get("faixa_favorita")))
            st.caption("O link “letra” abre a música no letras.com, com a letra e, quando houver, a página de significado.")
        else:
            st.caption("Sem a lista de faixas no MusicBrainz.")
    with c_meu:
        html('<div class="rotulo">Para você</div>')
        controles_album(a)
    outros = [x for x in b["albuns"] if x["id"] != a["id"] and not x["futuro"]]
    if outros:
        html(f'<div class="rotulo">Mais de {escape(b["nome"])}</div>')
        outros.sort(key=lambda x: (bool(banco.album(x["id"]).get("escutei")),
                                   -((x["nota_critica"] or 0) + 0.7 * len(x.get("listas", [])))))
        grade_mini(outros[:6], "alb_mais")
    vizinhos = [BANDAS[i] for i in dict.fromkeys(no_acervo(p) for p in b["parecidas"]) if i and i != b["id"]]
    sugestoes = [x for x in (album_sugerido(v) for v in vizinhos) if x][:6]
    if sugestoes:
        html('<div class="rotulo">Se você curtir, experimente</div>')
        grade_mini(sugestoes, "alb_viz", {x["id"]: "de uma banda parecida" for x in sugestoes})


def gosto_por_banda() -> dict:
    """Quanto você gosta de cada banda: a marcação explícita, senão a média das suas notas."""
    saida = {}
    for b in BANDAS.values():
        e = estado_banda(b)
        if e["gosto"] is not None:
            saida[b["id"]] = e["gosto"]
        elif e["media"] is not None:
            saida[b["id"]] = 2 if e["media"] >= 8.5 else 1 if e["media"] >= 7 else 0 if e["media"] >= 5 else -1
    return saida


def mini_album(a: dict, col, contexto: str, extra: str = "") -> None:
    b = BANDAS[a["banda_id"]]
    critica = f"crítica {nota_fmt(a['nota_critica'])} · " if a["nota_critica"] is not None else ""
    ouvir = enderecos(b["nome"], a)["Spotify"]
    col.html(f'<div class="mini">{capa(a, "", ouvir)}<div><div class="t">{escape(a["titulo"])}</div>'
             f'<div class="s">{escape(b["nome"])} · {a["ano"]}</div><div class="s">{critica}{escape(extra)}</div>'
             f'{links_ouvir(b["nome"], a, compacto=True)}</div></div>')
    c0, c1, c2 = col.columns(3)
    c0.button("Álbum", key=f"alb_{contexto}_{a['id']}", on_click=abrir_album, args=(a["id"],), width="stretch",
              type="primary", help="Ver tudo sobre o álbum")
    chave = f"fila_{contexto}_{a['id']}"
    na_fila = bool(banco.album(a["id"]).get("quero_ouvir"))
    if c1.button("✓ Fila" if na_fila else "+ Fila", key=chave, width="stretch", disabled=na_fila):
        banco.salvar_album(a["id"], a["banda_id"], quero_ouvir=True)
        st.session_state[f"quero_ouvir_{a['id']}"] = True
        st.rerun()
    c2.button("Banda", key=f"ab_{contexto}_{a['id']}", on_click=abrir_banda, args=(b["id"],), width="stretch")


def grade_mini(albuns: list[dict], contexto: str, extras: dict | None = None) -> None:
    for i in range(0, len(albuns), 3):
        cols = st.columns(3)
        for col, a in zip(cols, albuns[i:i + 3]):
            with col.container(border=True):
                mini_album(a, st, contexto, (extras or {}).get(a["id"], ""))


def nao_escutado(a: dict) -> bool:
    return not banco.album(a["id"]).get("escutei")


def sugerivel(a: dict) -> bool:
    """Já lançado e ainda não escutado."""
    return not a["futuro"] and nao_escutado(a)


def pagina_ouvir() -> None:
    html('<div class="titulo">O que <span>ouvir</span></div>'
         '<div class="sub">Sugestões que se recalculam a cada nota e marcação que você faz.</div>')
    rotacao = [a for a in ALBUNS.values() if banco.album(a["id"]).get("em_rotacao")]
    if rotacao:
        html('<div class="rotulo">Em rotação</div>')
        grade_mini(rotacao, "rotacao")
    fila = [a for a in ALBUNS.values() if banco.album(a["id"]).get("quero_ouvir") and nao_escutado(a)]
    html('<div class="rotulo">Sua fila</div>')
    if fila:
        grade_mini(sorted(fila, key=lambda a: -(a["nota_critica"] or 0)), "fila")
    else:
        st.caption("Vazia. Use “+ Fila” nas sugestões abaixo ou marque “Quero ouvir” em qualquer álbum.")

    gostos = gosto_por_banda()
    na_lista = [b for b in BANDAS.values() if estado_banda(b)["lista"]]
    if na_lista:
        html('<div class="rotulo">Para começar as bandas da sua lista</div>')
        proximos, extras = [], {}
        for b in na_lista:
            faltam = [a for a in b["albuns"] if sugerivel(a)]
            porta = ALBUNS.get(b.get("porta_de_entrada") or "")
            a = porta if porta in faltam else max(faltam, key=lambda a: a["nota_critica"] or 0, default=None)
            if a:
                proximos.append(a)
                extras[a["id"]] = "por onde começar" if a is porta else "próximo da lista"
        grade_mini(proximos[:12], "lista", extras)

    seguidas = {b["id"] for b in na_lista} | {bid for bid, g in gostos.items() if g >= 1}
    corte = (date.today() - timedelta(days=200)).isoformat()
    novidades = [a for bid in seguidas for a in BANDAS[bid]["albuns"] if (a.get("data") or "") >= corte]
    if novidades:
        html('<div class="rotulo">Novidades das suas bandas</div>')
        novidades.sort(key=lambda a: a["data"], reverse=True)
        grade_mini(novidades[:9], "novos", {a["id"]: ("sai em " if a["futuro"] else "saiu em ") + data_br(a["data"])
                                            for a in novidades[:9]})

    hoje = date.today()
    perto = {(hoje + timedelta(days=d)).strftime("%m-%d"): d for d in range(-3, 4)}
    aniversarios = [a for a in ALBUNS.values() if len(a.get("data") or "") == 10 and a["data"][5:] in perto
                    and hoje.year - int(a["ano"]) >= 1 and gostos.get(a["banda_id"], 0) >= 0]
    if aniversarios:
        html('<div class="rotulo">Neste dia</div>')
        aniversarios.sort(key=lambda a: (abs(perto[a["data"][5:]]), -((hoje.year - int(a["ano"])) % 5 == 0),
                                         -(a["nota_critica"] or 0)))
        def quando(a):
            anos_ = hoje.year - int(a["ano"])
            d = perto[a["data"][5:]]
            dia = "hoje" if d == 0 else f"em {a['data'][8:]}/{a['data'][5:7]}"
            return f"faz {anos_} anos {dia}" if d <= 0 else f"completa {anos_} anos {dia}"
        grade_mini(aniversarios[:9], "aniver", {a["id"]: quando(a) for a in aniversarios[:9]})

    queridas = [bid for bid, g in gostos.items() if g >= 1]
    html('<div class="rotulo">Das bandas que você curte</div>')
    if queridas:
        cands = [a for bid in queridas for a in BANDAS[bid]["albuns"] if sugerivel(a)]
        cands.sort(key=lambda a: (-(gostos[a["banda_id"]]), -(a["nota_critica"] or 0)))
        grade_mini(cands[:9], "curte", {a["id"]: "falta você ouvir" for a in cands[:9]})
    else:
        st.caption("Marque “Gosto” ou “Favorita” em algumas bandas, ou dê notas a álbuns, e esta lista aparece.")

    html('<div class="rotulo">Clássicos que faltam</div>')
    st.caption("Os mais bem avaliados pela crítica e os que aparecem nas listas da Rolling Stone, no 1001 Discos e afins.")
    classicos = [a for a in ALBUNS.values() if sugerivel(a) and ((a["nota_critica"] or 0) >= 9 or a["listas"])
                 and gostos.get(a["banda_id"], 0) >= 0]
    classicos.sort(key=lambda a: -((a["nota_critica"] or 7) + 0.7 * len(a["listas"])))
    grade_mini(classicos[:12], "classicos", {a["id"]: " · ".join(LISTAS.get(l["lista"], l["lista"]) for l in a["listas"][:2])
                                             for a in classicos[:12]})

    html('<div class="rotulo">Sorteio</div>')
    pool = [a for a in ALBUNS.values() if sugerivel(a) and (a["nota_critica"] or 0) >= 8
            and gostos.get(a["banda_id"], 0) >= 0]
    if st.button("🎲 Sortear outro") or "sorteio" not in st.session_state:
        st.session_state.sorteio = random.sample(pool, min(3, len(pool)))
    grade_mini([a for a in st.session_state.sorteio if a["id"] in ALBUNS], "sorteio")


def pagina_descobrir() -> None:
    html('<div class="titulo">Desco<span>brir</span></div>'
         '<div class="sub">Bandas que você ainda não marcou como conhecidas, ordenadas pelo quanto combinam com o '
         'que você curte. Marque “Já conheço” para tirar da lista.</div>')
    gostos = gosto_por_banda()
    peso_genero, fonte_genero = defaultdict(float), defaultdict(list)
    for bid, g in gostos.items():
        for gen in BANDAS[bid]["generos"]:
            peso_genero[gen] += g
            if g >= 1:
                fonte_genero[gen].append(BANDAS[bid]["nome"])
    desconhecidas = [b for b in BANDAS.values() if not estado_banda(b)["conhece"] and b["albuns"]]
    referencias = {bid for bid, g in gostos.items() if g >= 1} | {b["id"] for b in BANDAS.values() if estado_banda(b)["lista"]}
    vizinhas, de_quem, fora = Counter(), defaultdict(list), {}
    for bid in referencias:
        for p in BANDAS[bid]["parecidas"]:
            alvo = no_acervo(p)
            if alvo and alvo not in referencias:
                vizinhas[alvo] += 1
                de_quem[alvo].append(BANDAS[bid]["nome"])
            elif not alvo:
                fora.setdefault(p["deezer"], {**p, "votos": 0})["votos"] += 1
    if not peso_genero:
        st.info("Ainda não sei do que você gosta. Por enquanto, as sugestões vão pela crítica: marque “Gosto” em "
                "algumas bandas que você conhece e esta página passa a seguir o seu gosto.")
    pontos, porques = {}, {}
    for b in desconhecidas:
        pontos[b["id"]] = (sum(peso_genero.get(g, 0) for g in b["generos"]) + 3 * vizinhas[b["id"]]
                           + (b["critica_media"] or 0) / 10)
        refs = Counter(n for g in b["generos"] for n in fonte_genero.get(g, []))
        porta = ALBUNS.get(b.get("porta_de_entrada") or "")
        partes = []
        if de_quem[b["id"]]:
            partes.append("Parecida com " + " e ".join(de_quem[b["id"]][:2]))
        elif refs:
            partes.append("Combina com " + " e ".join(n for n, _ in refs.most_common(2)))
        if porta:
            partes.append(f"comece por {porta['titulo']} ({porta['ano']})")
        porques[b["id"]] = "; ".join(partes) + "." if partes else ""
    melhores = sorted(desconhecidas, key=lambda b: -pontos[b["id"]])[:16]
    grade_bandas(melhores, "desc", porques, acoes=True)
    if fora:
        html('<div class="rotulo">Fora do acervo</div>')
        st.caption("Artistas que o Deezer liga às bandas que você curte e que ainda não estão aqui. Clique para pedir; "
                   "eles entram na próxima atualização de segunda-feira.")
        botoes_pedido(sorted(fora.values(), key=lambda p: (-p["votos"], -p["fas"]))[:16], "desc", "Descobrir")
    acervo = [b for b in desconhecidas if b["cena"] == "Descobertas do acervo"]
    if acervo:
        html('<div class="rotulo">Garimpo do acervo</div>')
        if st.button("🎲 Outras do acervo") or "garimpo" not in st.session_state:
            st.session_state.garimpo = [b["id"] for b in random.sample(acervo, min(8, len(acervo)))]
        grade_bandas([BANDAS[i] for i in st.session_state.garimpo if i in BANDAS and not estado_banda(BANDAS[i])["conhece"]],
                     "garimpo", porques, acoes=True)


def pagina_numeros() -> None:
    html('<div class="titulo">Seus <span>números</span></div>')
    meus = {aid: banco.album(aid) for aid in ALBUNS}
    escutados = [ALBUNS[aid] for aid, e in meus.items() if e.get("escutei")]
    com_nota = [(ALBUNS[aid], e["nota"]) for aid, e in meus.items() if e.get("nota") is not None]
    conhecidas = [b for b in BANDAS.values() if estado_banda(b)["conhece"]]
    media = round(sum(n for _, n in com_nota) / len(com_nota), 1) if com_nota else None
    pares = [(a, n) for a, n in com_nota if a["nota_critica"] is not None]
    crit = round(sum(a["nota_critica"] for a, _ in pares) / len(pares), 1) if pares else None
    cols = st.columns(5)
    for col, (v, rot) in zip(cols, [(len(conhecidas), "bandas que você conhece"), (len(escutados), "álbuns escutados"),
                                     (len(com_nota), "álbuns com nota"), (nota_fmt(media) or "—", "sua nota média"),
                                     (nota_fmt(crit) or "—", "crítica nos mesmos álbuns")]):
        col.html(f'<div class="numero"><b>{v}</b><span>{rot}</span></div>')
    if escutados:
        html('<div class="rotulo">Escutados por década</div>')
        st.bar_chart(pd.Series(Counter(f"{a['ano'][:3]}0s" for a in escutados)).sort_index(), color="#F2A541")
        html('<div class="rotulo">Escutados por cena</div>')
        st.bar_chart(pd.Series(Counter(BANDAS[a["banda_id"]]["cena"] for a in escutados)).sort_values(),
                     color="#E5484D", horizontal=True)
    if com_nota:
        html('<div class="rotulo">Seus dez mais</div>')
        top = sorted(com_nota, key=lambda x: -x[1])[:10]
        grade_mini([a for a, _ in top], "top", {a["id"]: f"sua nota {nota_fmt(n)}" for a, n in top})
    if pares:
        html('<div class="rotulo">Onde você discorda da crítica</div>')
        dif = sorted(pares, key=lambda x: -abs(x[1] - x[0]["nota_critica"]))[:6]
        grade_mini([a for a, _ in dif], "dif",
                   {a["id"]: f"você {nota_fmt(n)} × crítica {nota_fmt(a['nota_critica'])}" for a, n in dif})
    datados = [(ALBUNS[aid], e) for aid, e in meus.items() if e.get("escutado_em")]
    if datados:
        html('<div class="rotulo">Retrospectiva</div>')
        hoje = date.today()
        periodos = {"Este mês": hoje.strftime("%Y-%m"), "Este ano": str(hoje.year)}
        cols = st.columns(len(periodos))
        for col, (rotulo, prefixo) in zip(cols, periodos.items()):
            do_periodo = [(a, e) for a, e in datados if e["escutado_em"].startswith(prefixo)]
            notas_p = [e["nota"] for _, e in do_periodo if e.get("nota") is not None]
            idade = round(sum(int(a["ano"]) for a, _ in do_periodo) / len(do_periodo)) if do_periodo else None
            melhor = max(do_periodo, key=lambda x: x[1].get("nota") or 0)[0] if do_periodo else None
            col.html(f'<div class="numero"><b>{len(do_periodo)}</b><span>{rotulo}: álbuns escutados'
                     + (f" · média {nota_fmt(round(sum(notas_p) / len(notas_p), 1))}" if notas_p else "")
                     + (f" · idade musical: discos de {idade}" if idade else "")
                     + (f" · destaque: {escape(melhor['titulo'])}" if melhor else "") + "</span></div>")
    if com_nota:
        html('<div class="rotulo">Seu perfil de gosto</div>')
        por_genero, por_decada = defaultdict(list), defaultdict(list)
        for a, n in com_nota:
            por_decada[f"{a['ano'][:3]}0s"].append(n)
            for g in BANDAS[a["banda_id"]]["generos"][:3]:
                por_genero[g].append(n)
        c1, c2 = st.columns(2)
        tabela = lambda d: pd.DataFrame([(k, round(sum(v) / len(v), 1), len(v)) for k, v in d.items()],
                                        columns=["", "sua média", "álbuns"]).sort_values("sua média", ascending=False)
        c1.caption("Por gênero (gêneros com pelo menos 2 álbuns)")
        c1.dataframe(tabela({k: v for k, v in por_genero.items() if len(v) >= 2}), hide_index=True, width="stretch")
        c2.caption("Por década")
        c2.dataframe(tabela(por_decada), hide_index=True, width="stretch")
        if pares:
            dif = sum(n - a["nota_critica"] for a, n in pares) / len(pares)
            st.caption(("Você é mais generoso que a crítica" if dif > 0.3 else "Você é mais rigoroso que a crítica"
                        if dif < -0.3 else "Suas notas andam junto com as da crítica") + f" ({dif:+.1f} em média).")
    if not escutados and not com_nota:
        st.info("Os números aparecem conforme você marca álbuns como escutados e dá notas.")


PAGINAS = {
    "ouvir": st.Page(pagina_ouvir, title="O que ouvir", icon="🎧", url_path="ouvir", default=True),
    "minhas": st.Page(pagina_minhas, title="Minhas bandas", icon="⭐", url_path="minhas"),
    "acervo": st.Page(pagina_acervo, title="Acervo", icon="🗂️", url_path="acervo"),
    "descobrir": st.Page(pagina_descobrir, title="Descobrir", icon="🧭", url_path="descobrir"),
    "banda": st.Page(pagina_banda, title="Banda", icon="🎸", url_path="banda"),
    "album": st.Page(pagina_album, title="Álbum", icon="💿", url_path="album"),
    "numeros": st.Page(pagina_numeros, title="Números", icon="📊", url_path="numeros"),
}
st.navigation(list(PAGINAS.values()), position="top").run()

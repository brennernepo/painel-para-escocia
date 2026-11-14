import hmac
import random
from collections import Counter, defaultdict
from datetime import date
from html import escape

import pandas as pd
import streamlit as st

import banco
from catalogo import albuns_por_id, carregar
from estilo import CSS, anos, capa, chips, data_br, foto_banda, html, links_ouvir, nota_fmt, situacao

st.set_page_config(page_title="Discoteca", page_icon="💿", layout="wide")
st.html(CSS)

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
BANDAS = carregar()
ALBUNS = albuns_por_id(BANDAS)
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
    return {"conhece": conhece, "gosto": meu.get("gosto"), "escutados": len(escutados),
            "media": round(sum(notas) / len(notas), 1) if notas else None}


def abrir_banda(banda_id: str) -> None:
    st.session_state.banda_id = banda_id
    st.switch_page(PAGINAS["banda"])


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


def controles_album(a: dict) -> None:
    e = banco.album(a["id"])
    args = lambda campo, chave: {"on_change": ao_mudar_album, "args": (a["id"], a["banda_id"], campo, chave)}
    c1, c2 = st.columns(2)
    for col, campo, rotulo in ((c1, "conheco", "Conheço"), (c2, "escutei", "Escutei inteiro"),
                               (c1, "quero_ouvir", "Quero ouvir"), (c2, "favorito", "Favorito ❤")):
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
             (f"em breve · {data_br(a['data'])}" if a["futuro"] else "", "azul")]
    return chips(itens)


def bloco_album(a: dict, banda: dict, com_banda: bool = False) -> None:
    with st.container(border=True):
        c_capa, c_info, c_ctrl = st.columns([1.1, 3.1, 2.1], gap="medium")
        c_capa.html(capa(a))
        meta = " · ".join(x for x in (a.get("data", "")[:4], f"{len(a['faixas'])} faixas" if a["faixas"] else "",
                                       f"{a['duracao_min']} min" if a.get("duracao_min") else "") if x)
        nome_banda = f'<div class="album-meta" style="color:var(--ambar)">{escape(banda["nome"])}</div>' if com_banda else ""
        curio = f'<div class="album-curio">💡 {escape(a["curiosidade"])}</div>' if a.get("curiosidade") else ""
        c_info.html(f'{nome_banda}<div class="album-titulo">{escape(a["titulo"])}</div>'
                    f'<div class="album-meta">{escape(meta)}</div>{chips_album(a)}{curio}'
                    f'{links_ouvir(banda["nome"], a["titulo"], a.get("wikipedia"))}')
        if a["faixas"]:
            with c_info.expander(f"Faixas ({len(a['faixas'])})"):
                st.html('<div class="faixas">' + "".join(
                    f'<div><b>{f["n"]}</b>{escape(f["titulo"])} <span>{f["duracao"] or ""}</span></div>'
                    for f in a["faixas"]) + "</div>")
        with c_ctrl:
            controles_album(a)


def marcar_banda(banda_id: str, gosto: int | None) -> None:
    banco.salvar_banda(banda_id, conheco=True, **({"gosto": gosto} if gosto is not None else {}))


def cartao_banda(b: dict, col, contexto: str, porque: str = "", acoes: bool = False) -> None:
    e = estado_banda(b)
    total = len(b["albuns"])
    sit, cor = situacao(b)
    meta = " · ".join(x for x in (b["pais_nome"], anos(b), f"{total} álbuns") if x)
    porque_html = f'<div class="porque">{escape(porque)}</div>' if porque else ""
    col.html(
        f'<div class="cartao-banda">{foto_banda(b)}<div class="corpo"><div class="nome">{escape(b["nome"])}</div>'
        f'<div class="meta">{escape(meta)}</div>'
        f'{chips([(g, "") for g in b["generos"][:2]] + [(sit, cor), (GOSTO.get(e["gosto"], "") if e["gosto"] else "", "ambar")])}'
        f'<div class="barra"><i style="width:{(e["escutados"] / total * 100) if total else 0:.0f}%"></i></div>'
        f'<div class="meta">{e["escutados"]} de {total} escutados</div>{porque_html}</div></div>'
    )
    col.button("Abrir", key=f"abrir_{contexto}_{b['id']}", on_click=abrir_banda, args=(b["id"],), width="stretch")
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
def pagina_bandas() -> None:
    conhecidas = sum(1 for b in BANDAS.values() if estado_banda(b)["conhece"])
    escutados = sum(1 for a in ALBUNS.values() if banco.album(a["id"]).get("escutei"))
    html(f'<div class="titulo">Minha <span>discoteca</span></div>'
         f'<div class="sub">{len(BANDAS)} bandas · {len(ALBUNS)} álbuns de estúdio · você conhece {conhecidas} bandas '
         f'e já escutou {escutados} álbuns</div>')
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 1.6, 1.4])
    busca = c1.text_input("Buscar banda ou gênero", placeholder="Ex.: Soundgarden, thrash, Brasil…")
    cenas = sorted({b["cena"] for b in BANDAS.values()})
    escolhidas = c2.multiselect("Cena", cenas, placeholder="Todas")
    filtro = c3.selectbox("Mostrar", ["Todas", "Que conheço", "Que não conheço", "Favoritas", "Na ativa", "Encerradas"])
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
        if (filtro == "Que conheço" and not e["conhece"]) or (filtro == "Que não conheço" and e["conhece"]) \
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
         f'{chips([(g, "") for g in b["generos"]] + [(sit, cor)])}</div></div>')
    c1, c2 = st.columns([1.2, 4])
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
    filtro = st.segmented_control("Álbuns", ["Todos", "Não escutados", "Escutados", "Na fila"], default="Todos",
                                  key=f"filtro_{b['id']}", label_visibility="collapsed")
    porta = b.get("porta_de_entrada")
    if porta and not e["escutados"]:
        st.caption(f"Por onde começar: **{ALBUNS[porta]['titulo']}**, o que melhor junta crítica e popularidade.")
    for a in b["albuns"]:
        meu = banco.album(a["id"])
        if (filtro == "Não escutados" and meu.get("escutei")) or (filtro == "Escutados" and not meu.get("escutei")) \
                or (filtro == "Na fila" and not meu.get("quero_ouvir")):
            continue
        bloco_album(a, b)
    if not b["albuns"]:
        st.info("Não achei álbuns de estúdio desta banda no MusicBrainz.")


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
    col.html(f'<div class="mini">{capa(a, "")}<div><div class="t">{escape(a["titulo"])}</div>'
             f'<div class="s">{escape(b["nome"])} · {a["ano"]}</div><div class="s">{critica}{escape(extra)}</div></div></div>')
    c1, c2 = col.columns(2)
    chave = f"fila_{contexto}_{a['id']}"
    na_fila = bool(banco.album(a["id"]).get("quero_ouvir"))
    if c1.button("✓ Na fila" if na_fila else "+ Fila", key=chave, width="stretch", disabled=na_fila):
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
    fila = [a for a in ALBUNS.values() if banco.album(a["id"]).get("quero_ouvir") and nao_escutado(a)]
    html('<div class="rotulo">Sua fila</div>')
    if fila:
        grade_mini(sorted(fila, key=lambda a: -(a["nota_critica"] or 0)), "fila")
    else:
        st.caption("Vazia. Use “+ Fila” nas sugestões abaixo ou marque “Quero ouvir” em qualquer álbum.")

    gostos = gosto_por_banda()
    queridas = [bid for bid, g in gostos.items() if g >= 1]
    html('<div class="rotulo">Das bandas que você curte</div>')
    if queridas:
        cands = [a for bid in queridas for a in BANDAS[bid]["albuns"] if sugerivel(a)]
        cands.sort(key=lambda a: (-(gostos[a["banda_id"]]), -(a["nota_critica"] or 0)))
        grade_mini(cands[:9], "curte", {a["id"]: "falta você ouvir" for a in cands[:9]})
    else:
        st.caption("Marque “Gosto” ou “Favorita” em algumas bandas, ou dê notas a álbuns, e esta lista aparece.")

    html('<div class="rotulo">Clássicos que faltam</div>')
    classicos = [a for a in ALBUNS.values() if sugerivel(a) and (a["nota_critica"] or 0) >= 9
                 and gostos.get(a["banda_id"], 0) >= 0]
    classicos.sort(key=lambda a: -(a["nota_critica"] or 0))
    grade_mini(classicos[:9], "classicos")

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
    if not peso_genero:
        st.info("Ainda não sei do que você gosta. Por enquanto, as sugestões vão pela crítica: marque “Gosto” em "
                "algumas bandas que você conhece e esta página passa a seguir o seu gosto.")
    pontos, porques = {}, {}
    for b in desconhecidas:
        pontos[b["id"]] = sum(peso_genero.get(g, 0) for g in b["generos"]) + (b["critica_media"] or 0) / 10
        refs = Counter(n for g in b["generos"] for n in fonte_genero.get(g, []))
        porta = ALBUNS.get(b.get("porta_de_entrada") or "")
        partes = []
        if refs:
            partes.append("Combina com " + " e ".join(n for n, _ in refs.most_common(2)))
        if porta:
            partes.append(f"comece por {porta['titulo']} ({porta['ano']})")
        porques[b["id"]] = "; ".join(partes) + "." if partes else ""
    melhores = sorted(desconhecidas, key=lambda b: -pontos[b["id"]])[:16]
    grade_bandas(melhores, "desc", porques, acoes=True)
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
    if not escutados and not com_nota:
        st.info("Os números aparecem conforme você marca álbuns como escutados e dá notas.")


PAGINAS = {
    "bandas": st.Page(pagina_bandas, title="Minhas bandas", icon="🎸", url_path="bandas", default=True),
    "banda": st.Page(pagina_banda, title="Banda", icon="💿", url_path="banda"),
    "ouvir": st.Page(pagina_ouvir, title="O que ouvir", icon="🎧", url_path="ouvir"),
    "descobrir": st.Page(pagina_descobrir, title="Descobrir", icon="🧭", url_path="descobrir"),
    "numeros": st.Page(pagina_numeros, title="Números", icon="📊", url_path="numeros"),
}
st.navigation(list(PAGINAS.values()), position="top").run()

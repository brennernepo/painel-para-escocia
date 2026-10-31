"""Conteúdo do painel. O app lê tudo daqui; para corrigir ou incluir algo, edite este arquivo."""

from datetime import date

INICIO = date(2026, 11, 2)
FIM = date(2026, 11, 11)
SUBTITULO = "Edimburgo, Inverness, Fife e York, de 2 a 11 de novembro de 2026. A previsão do tempo se atualiza sozinha."

# ---------------------------------------------------------------------------
# Hospedagens, na ordem da viagem.
# lat/lon: centro da cidade (tempo e sol); lat_mapa/lon_mapa: o bairro, arredondado.
# Endereço e anfitrião ficam fora do repositório, em .streamlit/secrets.toml (veja secrets.exemplo.toml).
# ---------------------------------------------------------------------------
BASES = [
    {
        "id": "edimburgo", "cidade": "Edimburgo", "emoji": "🏰",
        "chegada": date(2026, 11, 2), "saida": date(2026, 11, 5),
        "bairro": "Shandon, oeste de Edimburgo", "busca_bairro": "Shandon, Edinburgh",
        "checkin": "a partir das 14h", "checkout": "até 10h",
        "lat": 55.9533, "lon": -3.1883, "lat_mapa": 55.93, "lon_mapa": -3.23,
        "nota": "Rua residencial calma. Ônibus 4, 44, 34 e 35 passam na Slateford Road, a 5 minutos, rumo a Haymarket, Princes Street e Royal Mile. Lidl a 6 minutos a pé.",
    },
    {
        "id": "inverness", "cidade": "Inverness", "emoji": "🏞",
        "chegada": date(2026, 11, 5), "saida": date(2026, 11, 7),
        "bairro": "Crown, centro de Inverness", "busca_bairro": "Crown, Inverness",
        "checkin": "a partir das 15h", "checkout": "até 10h",
        "lat": 57.4778, "lon": -4.2247, "lat_mapa": 57.48, "lon_mapa": -4.22,
        "nota": "No alto da escadaria Market Brae: 5 minutos a pé do centro e 7 a 10 da estação. Com mala, suba pela rampa da Stephen's Brae.",
    },
    {
        "id": "dalgety", "cidade": "Dalgety Bay", "emoji": "🌉",
        "chegada": date(2026, 11, 7), "saida": date(2026, 11, 9),
        "bairro": "Dalgety Bay, Fife", "busca_bairro": "Dalgety Bay",
        "checkin": "a confirmar", "checkout": "a confirmar",
        "lat": 56.0410, "lon": -3.3670, "lat_mapa": 56.03, "lon_mapa": -3.36,
        "nota": "Horários não aparecem na reserva: confirmem com a anfitriã. Estação de trem a ~30 min a pé (5 de táxi); Tesco a 19 min.",
    },
    {
        "id": "york", "cidade": "York", "emoji": "⛪",
        "chegada": date(2026, 11, 9), "saida": date(2026, 11, 11),
        "bairro": "Centro histórico de York", "busca_bairro": "York Minster",
        "checkin": "a partir das 15h", "checkout": "até 11h",
        "lat": 53.9600, "lon": -1.0873, "lat_mapa": 53.96, "lon_mapa": -1.08,
        "nota": "A 3 minutos da catedral e 15 da estação. Em volta, carro só entra antes das 10h30 ou depois das 17h.",
    },
]

# Médias das mesmas datas de 2015 a 2025 (reanálise ERA5 via Open-Meteo), calculadas em 10/10/2026
NORMAIS = {
    "edimburgo": {"max_media": 10.6, "min_media": 6.3, "max_recorde": 15.5, "min_recorde": 2.6,
                  "dias_chuva_pct": 43, "rajada_media_kmh": 43, "rajada_max_kmh": 84},
    "inverness": {"max_media": 10.5, "min_media": 5.1, "max_recorde": 15.7, "min_recorde": -0.4,
                  "dias_chuva_pct": 42, "rajada_media_kmh": 35, "rajada_max_kmh": 78},
    "dalgety": {"max_media": 10.5, "min_media": 5.1, "max_recorde": 14.8, "min_recorde": -0.9,
                "dias_chuva_pct": 55, "rajada_media_kmh": 42, "rajada_max_kmh": 92},
    "york": {"max_media": 11.4, "min_media": 6.0, "max_recorde": 17.1, "min_recorde": -1.7,
             "dias_chuva_pct": 42, "rajada_media_kmh": 41, "rajada_max_kmh": 69},
}

EVENTOS_DIA = {
    date(2026, 11, 2): "Chegada. Check-in a partir das 14h.",
    date(2026, 11, 3): "Edimburgo.",
    date(2026, 11, 4): "Edimburgo.",
    date(2026, 11, 5): "Check-out até 10h, trecho para Inverness (pela A9 ou por Glencoe), check-in a partir das 15h. "
                       "À noite, Bonfire Night em Inverness: fogueira às 18h e fogos às 19h no Bught Park, grátis.",
    date(2026, 11, 6): "Inverness, um bate-volta nas Highlands ou Skye.",
    date(2026, 11, 7): "Check-out até 10h e trecho para Dalgety Bay (pela A9 ou por Glencoe). Sem trem entre Inverness e Perth neste dia: obras, com ônibus substituto.",
    date(2026, 11, 8): "Fife ou Edimburgo. Remembrance Sunday: dois minutos de silêncio às 11h em todo o país.",
    date(2026, 11, 9): "Trecho para York, check-in a partir das 15h.",
    date(2026, 11, 10): "York.",
    date(2026, 11, 11): "Check-out até 11h. Às 11h, dois minutos de silêncio pelo Armistício.",
}

O_QUE_LEVAR = [
    ("Casaco", "Impermeável e com capuz. Com rajadas de 40 km/h, guarda-chuva vira do avesso"),
    ("Por baixo", "Camadas finas: segunda pele e fleece. Trens, pubs e museus são aquecidos"),
    ("Sapato", "Impermeável e com sola que agarre: a pedra molhada de Edimburgo e York escorrega"),
    ("Highlands", "Gorro, luvas e cachecol. Com vento, a sensação fica perto de zero"),
    ("Celular", "Bateria extra: escurece por volta das 16h20 e o mapa vira lanterna"),
    ("Tomada", "Tipo G, de três pinos retangulares. Leve adaptador"),
]

LINKS_TEMPO = [
    ("Alertas do Met Office", "https://weather.metoffice.gov.uk/warnings-and-advice/uk-warnings"),
    ("Traffic Scotland (estradas)", "https://www.traffic.gov.scot/"),
]

CIDADES = {}


def P(emoji, nome, texto, meta="", tags=(), busca=None):
    """Atalho para um cartão de lugar. `meta` aceita HTML simples (<b>)."""
    return {"emoji": emoji, "nome": nome, "texto": texto, "meta": meta, "tags": list(tags), "busca": busca}


# ---------------------------------------------------------------------------
# Inverness e Highlands (qui 05 a sáb 07/11). Pesquisa de 10/10/2026.
# ---------------------------------------------------------------------------
CIDADES["highlands"] = {
    "intro": (
        "Duas noites em Inverness, com um único dia inteiro livre: sexta, 06/11. Com menos de 9 horas de luz, "
        "esse dia comporta um passeio longo ou dois curtos, não mais. Escolham pela previsão do tempo."
    ),
    "alerta": (
        "Fechados nas datas de vocês: trem a vapor Jacobite (última viagem em 23/10), Cawdor Castle, Dunrobin Castle "
        "e o funicular de Cairngorm (manutenção de 2 a 9/11). Eilean Donan abre no dia 06 e fecha no dia 07."
    ),
    "secoes": [
        {
            "nome": "Bate-voltas",
            "descricao": (
                "Tempos de carro a partir de Inverness. Sem carro, há ônibus para os mais próximos e excursões "
                "para os distantes (veja a seção Excursões)."
            ),
            "pontos": [
                P("🏰", "Loch Ness e Urquhart Castle",
                  "Ruínas na beira do lago, o cartão-postal do Loch Ness. Comprem online: quando o online esgota, "
                  "não vendem na porta, e o estacionamento só é garantido com reserva.",
                  "🚗 30 min · 🚌 Citylink 919 para na porta · <b>9h30–16h30</b> (última entrada 15h30) · <b>£14</b> online · meio dia",
                  ["Pago", "Reserva"], "Urquhart Castle"),
                P("⛴", "Cruzeiro no Loch Ness",
                  "A Jacobite opera quase o ano todo. O mais completo leva ônibus, barco e entrada no Urquhart, "
                  "saindo da rodoviária de Inverness às 9h15 ou 14h15. No inverno o barco da tarde é mais curto.",
                  "50 min a partir de <b>£21</b> · 3h30 com Urquhart <b>£54</b> · confira o horário de novembro",
                  ["Pago"], "Clansman Harbour, Loch Ness"),
                P("⚔", "Culloden Battlefield",
                  "Campo da batalha de 1746, a última dos jacobitas. O campo é aberto; o centro de visitantes conta "
                  "a história em detalhe.",
                  "🚗 15 min · 🚌 Stagecoach 1B · centro <b>9h–16h</b> · ~<b>£16</b> · horário de 2026 a confirmar",
                  ["Pago"], "Culloden Battlefield"),
                P("🪨", "Clava Cairns",
                  "Túmulos de pedra de 4 mil anos num bosque silencioso, 2 km depois de Culloden. Quem viu Outlander "
                  "vai reconhecer o clima.",
                  "Sempre aberto", ["Grátis"], "Clava Cairns"),
                P("🛡", "Fort George",
                  "Fortaleza militar do século 18 ainda em uso pelo exército, sobre o estuário.",
                  "🚗 25 min · <b>10h–16h</b> (última entrada 15h) · <b>£10</b> online · 25% de desconto para quem chega sem carro",
                  ["Pago"], "Fort George"),
                P("🐬", "Black Isle e Chanonry Point",
                  "Ponta de areia onde golfinhos caçam no canal. Ficam ali o ano todo, mas em novembro aparecem menos. "
                  "Melhor hora: uma hora depois da maré baixa, com a maré subindo.",
                  "🚗 30 min · 🚌 Stagecoach 26 a cada ~2 h · meio dia", ["Grátis"], "Chanonry Point"),
                P("🔒", "Fort Augustus",
                  "Cinco eclusas do Canal da Caledônia na ponta sul do lago. Combina com Urquhart num dia inteiro; "
                  "a volta pela margem sul tem trechos de pista única.",
                  "🚗 55 min · 🚌 Citylink 919", ["Grátis"], "Fort Augustus Locks"),
                P("🌲", "Glen Affric e Plodda Falls",
                  "O vale mais bonito perto de Inverness, com floresta antiga. Estrada de pista única, sem sinal de "
                  "celular e sem café no caminho. Neve pode fechar a estrada.",
                  "🚗 1h–1h15 · estacionamento pago · meio dia a dia inteiro", [], "Plodda Falls"),
                P("🏔", "Aviemore e Cairngorms",
                  "Loch an Eilein tem uma trilha plana de uma hora em volta do lago, com um castelo numa ilha. "
                  "Fica no caminho do dia 07, de volta ao sul.",
                  "🚗 45 min pela A9 · também de trem · funicular fechado de 2 a 9/11", ["Grátis"], "Loch an Eilein"),
                P("🏯", "Eilean Donan",
                  "O castelo numa ilhota ligada por ponte de pedra. Só compensa no dia 06 e de carro ou excursão.",
                  "🚗 1h50 · 10h–16h · <b>£13</b>, só na bilheteria · <b>fechado em 07/11</b>",
                  ["Pago", "Só no dia 06"], "Eilean Donan Castle"),
                P("🌄", "Isle of Skye",
                  "São umas 2h40 de carro em cada sentido, mais de cinco horas ao volante para pouco mais de oito "
                  "de luz. Só faz sentido com excursão no dia 06, voltando por volta das 20h, já no escuro.",
                  "Excursão de ~12 h · ~£85–100", [], "Portree, Isle of Skye"),
            ],
            "dicas": [
                ("Dia 05 (chegada)", "Parada em Pitlochry ou Dalwhinnie na A9; à noite, beira-rio e castelo"),
                ("Dia 06 de carro", "Urquhart na abertura (9h30) e Fort Augustus, ou Eilean Donan"),
                ("Dia 06 sem carro", "Excursão da Rabbie's, ou o cruzeiro de 3h30 da Jacobite mais Culloden de ônibus"),
                ("Dia 07 (saída)", "Culloden e Clava cedo, depois a A9 para o sul com parada em Aviemore"),
                ("Regra de ouro", "Estar de volta à estrada principal antes de escurecer, por volta das 16h20"),
            ],
        },
        {
            "nome": "Inverness",
            "descricao": "Cidade pequena à beira do rio Ness. O centro, o castelo e o rio cabem num fim de tarde a pé.",
            "pontos": [
                P("🏰", "Inverness Castle",
                  "Reaberto em fevereiro de 2026 depois de uma reforma longa. O ingresso dá acesso às duas torres e "
                  "a um terraço no alto, com vista do rio e da cidade.",
                  "Todos os dias 10h–18h, última entrada 16h · <b>£20</b> online, £22 na porta · jardins grátis",
                  ["Pago"], "Inverness Castle"),
                P("🌉", "Rio Ness e Ness Islands",
                  "Caminhada plana do castelo até as ilhotas no meio do rio, ligadas por pontes de ferro. "
                  "Uns 25 minutos para cada lado.",
                  "Pode fechar em cheias", ["Grátis"], "Ness Islands, Inverness"),
                P("📚", "Leakey's Bookshop",
                  "Sebo enorme dentro de uma igreja antiga, com lareira acesa no inverno.",
                  "Ter–sáb 10h–17h30 · fechado dom e seg", ["Grátis"], "Leakey's Bookshop, Inverness"),
                P("🏛", "Inverness Museum and Art Gallery",
                  "História das Highlands, dos pictos aos jacobitas. Pequeno, bom para uma hora de chuva.",
                  "Ter–qui 12h–16h, sex–sáb 11h–16h · fechado dom–seg", ["Grátis"],
                  "Inverness Museum and Art Gallery"),
                P("🌿", "Botanic Gardens",
                  "Estufas tropicais aquecidas, com café. Boa saída para um dia frio.",
                  "Todos os dias 9h30–16h", ["Grátis"], "Inverness Botanic Gardens"),
                P("🛍", "Victorian Market",
                  "Galeria coberta do século 19 com praça de alimentação de doze barracas.",
                  "Cada barraca tem seu horário", ["Barato"], "Victorian Market, Inverness"),
                P("🎻", "Música ao vivo",
                  "Hootananny, na Church Street, tem música tradicional quase toda noite a partir das 21h. "
                  "O Gellions, de 1841, também toca todas as noites.",
                  "", [], "Hootananny, Inverness"),
            ],
            "dicas": [
                ("Da casa ao centro", "5 minutos descendo a escadaria Market Brae"),
                ("Da casa à estação", "7 a 10 minutos a pé, ladeira forte"),
                ("Com mala", "Subam pela rampa da Stephen's Brae em vez da escada, ou peguem um táxi"),
                ("Mercado", "Morrisons na Millburn Road, 7h–22h, a uns 8 minutos"),
            ],
        },
        {
            "nome": "Destilarias",
            "descricao": "As que recebem visitas no início de novembro. Quem dirige não bebe: o limite de álcool na Escócia é mais baixo que na Inglaterra.",
            "pontos": [
                P("🥃", "Singleton of Glen Ord",
                  "A destilaria mais perto de Inverness com visita guiada todos os dias.",
                  "🚗 25 min · 10h–17h · tour de 1h15 a partir de <b>£24</b>", ["Pago", "Reserva"],
                  "Glen Ord Distillery"),
                P("🥃", "Dalwhinnie",
                  "Uma das destilarias mais altas da Escócia, bem na A9. Parada natural na ida ou na volta.",
                  "🚗 1 h · 10h–16h · tour de 45 min a partir de <b>£21</b>", ["Pago", "Reserva"],
                  "Dalwhinnie Distillery"),
                P("🥃", "Tomatin",
                  "Perto de Inverness, mas no trecho da A9 em obras, com limite de 40 mph.",
                  "🚗 20 min · tour ~£20 · horário de novembro a confirmar", ["Pago"], "Tomatin Distillery"),
                P("🥃", "Glenfiddich (Speyside)",
                  "A mais conhecida de Speyside. Fica longe para um dia já curto.",
                  "🚗 1h20–1h30 · 9h30–16h30 · reserve", ["Pago", "Reserva"], "Glenfiddich Distillery"),
            ],
            "dicas": [("Mau tempo", "Glen Ord e Dalwhinnie avisam que podem fechar sem aviso em dia de tempestade")],
        },
        {
            "nome": "Excursões",
            "descricao": "Para quem não alugar carro. As agências abaixo têm saídas em novembro de 2026.",
            "pontos": [
                P("🚐", "Rabbie's",
                  "Saídas ao lado da Catedral, na Ardross Street: Skye (8h–20h), Loch Ness completo (9h30–17h15) e "
                  "Glen Affric com Culloden e Clava (9h–18h).",
                  "a partir de £40–58 por pessoa", ["Reserva"], "Inverness Cathedral, Ardross Street, Inverness"),
                P("🚐", "Highland Explorer Tours",
                  "Skye com Eilean Donan em 12 horas, saindo às 7h45 da Union Street. A entrada do castelo é paga à parte.",
                  "~£75–80 por pessoa · só no dia 06 · código WINTER dá 10% até 13/11", ["Reserva"], "15 Union Street, Inverness"),
                P("🚐", "Go Highlands",
                  "Grupo de até sete pessoas: Clava, Culloden e Loch Ness em 7 horas.",
                  "~£160 por pessoa", ["Reserva"], "Inverness"),
                P("⛴", "Jacobite Temptation",
                  "Ônibus, barco no Loch Ness e entrada no Urquhart em 3h30. Sobra meia tarde livre.",
                  "<b>£54</b> · sai às 9h15 ou 14h15 da rodoviária", ["Pago", "Reserva"], "Inverness Bus Station"),
            ],
            "dicas": [("Não funcionam em novembro", "Ônibus panorâmico da cidade e passeios de bicicleta")],
        },
        {
            "nome": "Onde comer",
            "descricao": "A casa fica no alto da Stephen's Brae, ao lado de dois bons restaurantes.",
            "pontos": [
                P("🍽", "Fig & Thistle",
                  "Bistrô escocês moderno de 38 lugares, a dois minutos da casa. Muito bem avaliado; reserve.",
                  "~£26–40 por pessoa", ["Reserva"], "Fig and Thistle, Inverness"),
                P("🍝", "Little Italy", "Italiano simples na Stephen's Street, colado à casa.", "££", [],
                  "Little Italy, Stephen's Street, Inverness"),
                P("⛪", "The Mustard Seed", "Cozinha escocesa numa igreja antiga à beira do rio.", "££", [],
                  "The Mustard Seed, Inverness"),
                P("🍕", "Black Isle Bar", "Cerveja orgânica da cervejaria Black Isle e pizza de forno a lenha.",
                  "££", [], "Black Isle Bar, Church Street, Inverness"),
                P("🥂", "Rocpool", "O jantar mais caprichado da cidade, na Ness Walk. Reserve.", "£££", ["Reserva"],
                  "Rocpool Restaurant, Inverness"),
            ],
        },
        {
            "nome": "Estrada no inverno",
            "descricao": "Para quem alugar carro. A A9 é a espinha dorsal entre Inverness e o sul.",
            "dicas": [
                ("Pista única", "Encoste no recuo (passing place) à sua esquerda, ou espere em frente ao da direita. Nunca estacione nele"),
                ("Cervos", "Risco maior ao amanhecer e ao anoitecer, que em novembro cai às 8h e às 16h30"),
                ("Neve e gelo", "Trechos altos da A9 (Slochd e Drumochter) e a A87 para Skye"),
                ("Obras na A9", "Tomatin–Moy com limite de 40 mph; Tay Crossing–Ballinluig também em obras"),
                ("Combustível", "Abasteça em Inverness, Aviemore ou Fort William; postos rurais fecham cedo e no domingo"),
                ("Antes de sair", "Câmeras e alertas em traffic.gov.scot e no Met Office"),
                ("Aluguel", "Enterprise na Seafield Road, Arnold Clark na Harbour Road, e as grandes no aeroporto (15 km)"),
                ("Devolver em Fife", "Cobram taxa por devolução em outra cidade"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# York (seg 09 a qua 11/11). Pesquisa de 10/10/2026; itens sem confirmação oficial dizem "confira".
# ---------------------------------------------------------------------------
CIDADES["york"] = {
    "intro": (
        "Segunda a quarta, com o apartamento a três minutos da catedral. Quase tudo se faz a pé, "
        "e a cidade cabe em um dia e meio sem correria."
    ),
    "alerta": (
        "O mercado de Natal abre em 12/11, um dia depois da saída de vocês. Em novembro as muralhas começam a "
        "fechar às 15h30, e o Yorkshire Museum só abre de quarta a domingo."
    ),
    "secoes": [
        {
            "nome": "Centro medieval",
            "descricao": "Catedral, muralhas e as ruas tortas em volta da Grape Lane. Tudo a menos de 10 minutos a pé.",
            "pontos": [
                P("⛪", "York Minster",
                  "A maior catedral gótica do norte da Europa. A subida à torre central tem 275 degraus e, no inverno, "
                  "só se compra no próprio dia, depois das 9h30, porque o vento cancela muitas subidas.",
                  "<b>Seg–sáb</b> 9h30–16h (última entrada) · dom 12h45–14h30 · <b>£20</b>, com a torre £26 · "
                  "o ingresso vale 12 meses",
                  ["Pago", "Torre no dia"]),
                P("🎶", "Evensong na catedral",
                  "Culto cantado pelo coro no fim da tarde, de graça e sem reserva. Entrada pela porta sul. "
                  "Terça (10/11) é o dia que encaixa.",
                  "<b>Ter–sáb às 17h30</b>",
                  ["Grátis"], "York Minster South Door"),
                P("🧱", "Muralhas da cidade",
                  "3,4 km de muralha medieval, umas duas horas a volta inteira. Se for fazer um trecho só, faça de "
                  "Bootham Bar a Monk Bar, com a catedral ao lado o caminho todo.",
                  "Abre às 8h · <b>em novembro começa a fechar às 15h30</b> · fecha o dia inteiro com gelo",
                  ["Grátis", "Fecha cedo"], "Bootham Bar, York"),
                P("🏚", "The Shambles",
                  "A rua medieval de casas tortas que quase se tocam no alto. Cedo, antes das 9h, dá para fotografar "
                  "sem multidão. O mercado coberto ao lado tem praça de alimentação.",
                  "Mercado das 9h às 16h no inverno",
                  ["Grátis", "Vá cedo"], "The Shambles, York"),
                P("🏰", "Clifford's Tower",
                  "Torre do castelo sobre um morro artificial, com terraço no telhado e vista da cidade.",
                  "Inverno 10h–16h · cerca de <b>£8,50</b> online (confira no English Heritage)",
                  ["Pago"]),
                P("🏛", "Barley Hall",
                  "Casa medieval restaurada no beco Coffee Yard. Também funciona como guarda-volumes da Stasher.",
                  "<b>£9,50</b> · inverno 10h–16h (última entrada 15h30)",
                  ["Pago", "Guarda-volumes"], "Barley Hall, Coffee Yard, York"),
                P("⚖", "Merchant Adventurers' Hall",
                  "Salão de comerciantes do século 14, com vigas de madeira enormes. Só aceita cartão.",
                  "<b>£7,50</b> · fim de semana com horário reduzido (confira)",
                  ["Pago"]),
            ],
            "dicas": [
                ("Ordem boa para o dia 10", "Muralhas de manhã, museus à tarde, Evensong às 17h30"),
                ("Ruas sem carro", "No centro, carro e táxi só entram antes das 10h30 ou depois das 17h"),
                ("Treasurer's House", "Fechada de 9 a 11/11: as visitas guiadas vão até outubro e o Natal começa só em 14/11"),
            ],
        },
        {
            "nome": "Museus",
            "descricao": "Bons para a tarde, quando escurece por volta das 16h15.",
            "pontos": [
                P("🚂", "National Railway Museum",
                  "Locomotivas reais, incluindo o Mallard e trens da realeza. Fica atrás da estação.",
                  "Todos os dias 10h–17h · <b>grátis</b>, reserva gratuita recomendada",
                  ["Grátis"]),
                P("🏚", "York Castle Museum",
                  "Tem uma rua vitoriana inteira reconstruída do lado de dentro, com lojas e iluminação a gás.",
                  "<b>Seg 11h–17h</b>, ter–dom 10h–17h · <b>£18</b>",
                  ["Pago"]),
                P("🛶", "JORVIK Viking Centre",
                  "Passeio em carrinho por uma York viking reconstruída sobre a escavação original.",
                  "<b>£17,50</b> antecipado · horário com hora marcada",
                  ["Pago", "Reserva"]),
                P("🌳", "Museum Gardens e St Mary's Abbey",
                  "Jardim com as ruínas de uma abadia beneditina. O Yorkshire Museum fica dentro dele.",
                  "Jardins grátis · Yorkshire Museum <b>£10</b>, qua–dom 10h–17h, <b>fechado seg e ter</b> (só dá na quarta, 11)",
                  ["Grátis"], "York Museum Gardens"),
                P("🖼", "York Art Gallery",
                  "Exposição atual: Turner, Wedgwood e outros. Só abre de quarta a domingo.",
                  "<b>£9</b> · só cabe na quarta, dia 11, antes de sair",
                  ["Pago"]),
                P("🍫", "York's Chocolate Story",
                  "York foi a cidade da KitKat e da Terry's. Visita guiada com degustação.",
                  "Todos os dias 10h–17h · cerca de <b>£21</b> · reserva obrigatória",
                  ["Pago", "Reserva"]),
            ],
        },
        {
            "nome": "À noite",
            "descricao": "York escurece cedo e tem tradição de passeios de fantasmas e pubs antigos.",
            "pontos": [
                P("👻", "The Original Ghost Walk",
                  "O passeio de fantasmas mais antigo da cidade, com chuva ou sem chuva.",
                  "<b>Toda noite às 20h</b>, saindo do pub King's Arms, na Ouse Bridge · £10 (na hora, só dinheiro)",
                  ["Pago"], "King's Arms, Ouse Bridge, York"),
                P("🕯", "Outros passeios de fantasmas",
                  "Ghost Hunt of York sai das Shambles às 19h30. Mad Alice só roda de quinta a sábado e não "
                  "encaixa nas datas de vocês.",
                  "", [], "The Shambles, York"),
                P("🍺", "Pubs históricos",
                  "Ye Olde Starre Inne e House of Trembling Madness na Stonegate; The Blue Bell, minúsculo e "
                  "eduardiano, na Fossgate; The Black Swan, de 1417.",
                  "", [], "Ye Olde Starre Inne, York"),
            ],
        },
        {
            "nome": "Onde comer",
            "descricao": "Perto de casa há bons restaurantes. Sunday roast não cai nas datas, que vão de segunda a quarta.",
            "pontos": [
                P("🫖", "Bettys",
                  "A casa de chá mais famosa do norte da Inglaterra. Não aceita reserva no salão: vá antes das "
                  "10h30 ou depois das 14h30. A Little Bettys fechou em 2021.",
                  "St Helen's Square · chá da tarde no Belmont Room, com reserva, ~£49,95",
                  ["Fila"], "Bettys, St Helen's Square, York"),
                P("🍲", "Shambles Food Court",
                  "Barracas com noodles, bagels e cozinha marroquina por uns £9.",
                  "9h–16h no inverno", ["Barato"], "Shambles Market, York"),
                P("🌶", "Na Grape Lane",
                  "Los Moros (norte-africano), Fish & Forest (no guia Michelin, só abre de quarta a sábado), Nineteen e Pig & Potato.",
                  "", [], "Grape Lane, York"),
                P("🥩", "The Whippet Inn",
                  "Carnes e pub food em North Street, do outro lado do rio.", "", [], "The Whippet Inn, York"),
                P("🍰", "Old York Tea Room",
                  "Alternativa à Bettys na Goodramgate, também com fila.", "", [], "Old York Tea Room, Goodramgate"),
            ],
        },
        {
            "nome": "Arredores",
            "descricao": "Para uma tarde fora, de trem. Em novembro várias casas de campo estão fechadas.",
            "pontos": [
                P("🌸", "Harrogate",
                  "Cidade de spa com a Bettys original e o jardim RHS Harlow Carr.",
                  "Trem Northern, ~35 min · a partir de ~£4", [], "Harrogate"),
                P("🏞", "Knaresborough",
                  "Viaduto sobre o rio Nidd e o castelo em ruínas. Pequena e fotogênica.",
                  "Trem, ~25 min", [], "Knaresborough"),
                P("🌊", "Scarborough",
                  "Praia vitoriana e castelo no penhasco.", "TransPennine, ~50 min", [], "Scarborough"),
                P("🏰", "Castle Howard",
                  "A casa fecha a temporada normal em 31/10 e reabre para o Natal em 12/11. Nas datas de vocês, "
                  "provavelmente fechada.",
                  "", ["Fechado nas datas"], "Castle Howard"),
            ],
        },
        {
            "nome": "Chegada e saída",
            "descricao": "Check-in às 15h e check-out às 11h. Da estação até o apartamento são uns 15 minutos a pé, com calçada de pedra.",
            "dicas": [
                ("Malas antes do check-in", "Stasher na Barley Hall ou nos Premier Inn da estação, a partir de ~£2 por mala"),
                ("Guarda-volumes na estação", "Left Luggage York, na Europcar da Queen Street, seg–sáb 8h–20h"),
                ("Mercado", "Sainsbury's Local na Davygate e Tesco Express na Goodramgate, a 5 minutos"),
                ("De carro", "Estacionamento Marygate, ~£23 o dia; o park & ride não permite pernoitar"),
                ("Saída para Londres", "LNER a cada 30 min, ~2h até King's Cross; antecipado a partir de ~£18"),
                ("Saída para Manchester Airport", "TransPennine direto, ~2h"),
                ("Saída para Edimburgo", "LNER direto, ~2h30"),
                ("11/11 às 11h", "Dois minutos de silêncio pelo Armistício; o sino da catedral toca 11 vezes"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# Edimburgo (seg 02 a qui 05/11; dá para voltar no domingo 08 a partir de Fife). Pesquisa de 10/10/2026.
# ---------------------------------------------------------------------------
CIDADES["edimburgo"] = {
    "intro": (
        "Três noites em Shandon, bairro residencial a oeste do centro. A Royal Mile fica a uns 40 minutos a pé "
        "ou 20 de ônibus. Com luz das 7h20 às 16h30, deixem os mirantes para a manhã e os museus para a tarde."
    ),
    "alerta": (
        "O Palácio de Holyroodhouse só abre de quinta a segunda em novembro: fechado em 03 e 04/11. A St Giles' "
        "cobra £12 de turistas desde 05/10/2026. O Natal de Edimburgo, com o mercado, começa só em 14/11. "
        "Dom 08/11, Remembrance Sunday: cerimônia às 11h na Royal Mile, que fica cheia de manhã."
    ),
    "secoes": [
        {
            "nome": "Old Town",
            "descricao": "A Royal Mile, do castelo ao palácio, e os becos (closes) que descem dela. Ladeiras e pedra o tempo todo.",
            "pontos": [
                P("🏰", "Edinburgh Castle",
                  "As joias da coroa escocesa, a capela de St Margaret, construção mais antiga da cidade, e a vista "
                  "de tudo. Ingresso com hora marcada; quando o online esgota, não vendem na porta.",
                  "Todos os dias 9h30–17h, última entrada 16h · <b>£23,50</b> online, £26 na porta · "
                  "flexível sem horário £38",
                  ["Pago", "Reserva"]),
                P("⛪", "St Giles' Cathedral",
                  "A catedral da Royal Mile, com a capela dos Cavaleiros do Cardo. Desde outubro de 2026 cobra "
                  "ingresso de quem não mora na Escócia.",
                  "Seg–qua e sex 10h–18h, qui 10h–17h, sáb 9h–17h, dom 13h–17h; última entrada 1 h antes · <b>£12</b>",
                  ["Pago"]),
                P("🕯", "The Real Mary King's Close",
                  "Visita guiada a ruas do século 17 que ficaram soterradas embaixo da prefeitura. Esgota.",
                  "Tour de 1 h · <b>£28,50</b>", ["Pago", "Reserva"]),
                P("🔭", "Camera Obscura",
                  "Câmera escura do século 19 no alto e cinco andares de ilusões de ótica. Abre até tarde, "
                  "bom para depois que escurece. Uns 100 degraus, sem elevador.",
                  "Seg–qui até 19h30, sex até 21h · <b>£24,95</b>", ["Pago", "Reserva"]),
                P("🥃", "Scotch Whisky Experience",
                  "Passeio pela produção de uísque com degustação e uma coleção de mais de 3 mil garrafas.",
                  "10h–20h · <b>£25</b> (50 min) ou £39,75 (75 min)", ["Pago"]),
                P("📜", "Writers' Museum",
                  "Casa do século 17 dedicada a Burns, Scott e Stevenson, escondida no Lady Stair's Close.",
                  "Todos os dias 10h–17h, última entrada 16h30 · <b>ter 03/11 fecha às 12h</b>", ["Grátis"]),
            ],
            "dicas": [
                ("Castelo", "Primeiro horário da manhã, antes dos grupos"),
                ("Ônibus de casa", "35 vai direto a Chambers Street e à Canongate; 4 e 44 vão à Princes Street"),
                ("Sem pressa", "A Royal Mile tem 1,8 km de ladeira; desçam do castelo para o palácio"),
            ],
        },
        {
            "nome": "Grassmarket e Harry Potter",
            "descricao": "A praça ao pé do castelo, a rua curva e colorida e o cemitério onde J.K. Rowling pegava nomes.",
            "pontos": [
                P("🌈", "Victoria Street",
                  "A rua curva de fachadas coloridas apontada como inspiração do Beco Diagonal. Tem o Oink, "
                  "sanduíche de porco assado, por £5–7.",
                  "", ["Grátis"], "Victoria Street, Edinburgh"),
                P("🪦", "Greyfriars Kirkyard",
                  "Cemitério do século 16 com o túmulo de Thomas Riddell, de onde teria saído o nome de Voldemort, "
                  "e a estátua do cachorro Greyfriars Bobby na entrada.",
                  "Aberto de dia", ["Grátis"], "Greyfriars Kirkyard"),
                P("☕", "The Elephant House",
                  "O café onde Rowling escreveu parte dos primeiros livros. Reabriu em dezembro de 2025, depois de "
                  "anos fechado por um incêndio.",
                  "Todos os dias 10h–18h", [], "The Elephant House, George IV Bridge"),
                P("🏛", "National Museum of Scotland",
                  "Do esqueleto de dinossauro à ovelha Dolly. Grátis e enorme; o terraço do último andar tem vista "
                  "do castelo.",
                  "Todos os dias 10h–17h", ["Grátis"]),
                P("🎻", "Sandy Bell's",
                  "Pub pequeno com música folk ao vivo toda noite.",
                  "Forrest Road", [], "Sandy Bell's, Edinburgh"),
                P("🥃", "The Bow Bar",
                  "Mais de 300 uísques de malte num bar antigo da West Bow.",
                  "", [], "The Bow Bar, Edinburgh"),
            ],
        },
        {
            "nome": "New Town e Calton Hill",
            "descricao": "Ruas georgianas planejadas no século 18, a Princes Street e o morro com a melhor vista do pôr do sol.",
            "pontos": [
                P("🌅", "Calton Hill",
                  "Morro de 15 minutos de subida a partir da Princes Street, com o monumento grego inacabado e vista "
                  "do castelo, do Arthur's Seat e do mar. O melhor lugar para o pôr do sol, perto das 16h20. "
                  "As trilhas não têm iluminação.",
                  "Sempre aberto · Nelson Monument 10h–15h30 (ter 03/11 só até 12h), £7,50", ["Grátis"], "Calton Hill"),
                P("🖼", "Scottish National Gallery",
                  "Rafael, Rembrandt, Monet e pintores escoceses, no meio dos jardins da Princes Street.",
                  "Todos os dias 10h–17h", ["Grátis"]),
                P("🗼", "Scott Monument",
                  "Torre gótica de 287 degraus estreitos. Fecha com vento forte, o que em novembro é comum.",
                  "Até ~15h30 no inverno · <b>£8</b> · ter 03/11 fecha às 12h", ["Pago"]),
                P("🥃", "Johnnie Walker Princes Street",
                  "Loja e experiência de oito andares com bar no terraço.",
                  "Tour de 90 min ~£30 (confira)", ["Pago"], "Johnnie Walker Princes Street"),
            ],
        },
        {
            "nome": "Holyrood e Arthur's Seat",
            "descricao": "O fim da Royal Mile: o palácio real, o parlamento e um vulcão extinto no meio da cidade.",
            "pontos": [
                P("👑", "Palace of Holyroodhouse",
                  "Residência oficial do rei na Escócia e o quarto de Mary, rainha dos escoceses. Em novembro só "
                  "abre de quinta a segunda: dá na segunda, 02/11, ou no domingo, 08/11, vindo de Fife.",
                  "Qui–seg 9h30–16h30, última entrada 15h15 · <b>£22</b> antecipado · "
                  "<b>fechado ter e qua</b>",
                  ["Pago", "Fechado ter-qua"]),
                P("⛰", "Arthur's Seat",
                  "Pico de 251 m. Uns 45 minutos de subida a partir do estacionamento de Holyrood, ida e volta "
                  "entre 1 e 2 horas. Pedra lisa quando chove; nunca desçam no escuro.",
                  "Faça de manhã", ["Grátis"], "Arthur's Seat"),
                P("🏛", "Parlamento escocês",
                  "Prédio contemporâneo premiado, aberto a visitas.",
                  "Seg, sex e sáb 10h–17h · ter–qui até 18h30 · fechado no domingo", ["Grátis"],
                  "Scottish Parliament"),
                P("🌍", "Dynamic Earth",
                  "Museu interativo sobre a formação da Terra. Bom para chuva.",
                  "~10h–17h30 · <b>£23</b> online (vale um ano) · pode fechar seg e ter no inverno: confira", ["Pago"]),
                P("🥃", "Holyrood Distillery",
                  "Destilaria nova de uísque e gin num galpão ferroviário.",
                  "Tour rápido <b>£15</b>", ["Pago"], "Holyrood Distillery"),
            ],
            "dicas": [("Ônibus de casa", "O 35 vai direto da Slateford Road até o Parlamento")],
        },
        {
            "nome": "Dean Village e Stockbridge",
            "descricao": "Um vilarejo de moinhos à beira do rio, a 15 minutos do West End, e o bairro de lojinhas ao lado.",
            "pontos": [
                P("🏘", "Dean Village",
                  "Casas antigas à beira do Water of Leith. A trilha do rio segue até Stockbridge.",
                  "", ["Grátis"], "Dean Village"),
                P("🌿", "Royal Botanic Garden",
                  "Jardim grátis com vista da cidade. As estufas vitorianas (Palm Houses) reabriram em outubro de 2026 "
                  "depois de restauração e pedem ingresso com hora marcada.",
                  "10h–16h de novembro a janeiro", ["Grátis", "Estufas com reserva"], "Royal Botanic Garden Edinburgh"),
                P("🛍", "Stockbridge",
                  "Raeburn Place tem lojas independentes e a Harkness Pies. O mercado de rua é só no domingo.",
                  "", [], "Raeburn Place, Edinburgh"),
            ],
        },
        {
            "nome": "Leith",
            "descricao": "O porto de Edimburgo, de bonde ou no ônibus 35 direto de casa.",
            "pontos": [
                P("🛳", "Royal Yacht Britannia",
                  "O iate da rainha Elizabeth II, aberto do convés à sala de jantar de Estado. Só aceita cartão.",
                  "Primeira entrada 10h, última 15h · <b>£23</b> online, £25 na porta", ["Pago"], "Royal Yacht Britannia"),
                P("🥃", "Port of Leith Distillery",
                  "Destilaria vertical, em um prédio de nove andares, com bar no alto.",
                  "Tour com degustação <b>£30</b>", ["Pago", "Reserva"]),
                P("🐟", "The Fishmarket",
                  "Fish and chips no píer de Newhaven, considerado dos melhores da cidade. Tem fila.",
                  "", [], "The Fishmarket, Newhaven, Edinburgh"),
            ],
        },
        {
            "nome": "Perto de casa",
            "descricao": "Shandon e Gorgie, para o café da manhã, o mercado e uma caminhada sem turista.",
            "pontos": [
                P("🛒", "Lidl Slateford Road", "O mercado mais perto, a uns 6 minutos.", "Todos os dias 8h–22h", [],
                  "Lidl, 155 Slateford Road, Edinburgh"),
                P("🚶", "Union Canal",
                  "O caminho do canal passa ao lado do Harrison Park e leva a Fountainbridge em uns 30 minutos.",
                  "", ["Grátis"], "Harrison Park, Edinburgh"),
                P("🍺", "Athletic Arms (The Diggers)",
                  "Pub clássico de bairro, com tortas e uísque, a 10 minutos.", "", [], "Athletic Arms, Edinburgh"),
                P("🥞", "Loudons", "Brunch em Fountainbridge, o mais perto de casa.", "", [], "Loudons, Fountainbridge"),
            ],
            "dicas": [
                ("Ônibus 38", "Para perto de casa, mas contorna o centro: serve para Morningside"),
                ("Tynecastle", "O estádio do Hearts fica a 700 m; em dia de jogo o bairro lota"),
                ("Murrayfield em 07/11", "Escócia × Nova Zelândia às 14h10, a 1,5 km da casa: Haymarket e trens para Fife lotados"),
            ],
        },
        {
            "nome": "Onde comer",
            "descricao": "Mistura de clássicos e opções baratas, segundo guias locais de 2026.",
            "pontos": [
                P("🍳", "Edinburgh Larder", "Café da manhã escocês completo, na Old Town.", "", [], "Edinburgh Larder"),
                P("🥪", "Oink", "Sanduíche de porco assado, barato e rápido.", "Victoria Street e Canongate", ["Barato"],
                  "Oink, Victoria Street, Edinburgh"),
                P("🍛", "Mosque Kitchen", "Curry farto a partir de ~£6.", "Southside", ["Barato"], "Mosque Kitchen, Edinburgh"),
                P("🥖", "Bánh Mì Brothers", "Almoço vietnamita barato.", "West Port", ["Barato"],
                  "Banh Mi Brothers, West Port, Edinburgh"),
                P("🍦", "Mary's Milk Bar", "Sorvete e chocolate quente na Grassmarket, com fila.", "", [],
                  "Mary's Milk Bar, Grassmarket"),
                P("🥘", "Arcade Haggis & Whisky House", "Haggis de várias formas e mais de cem uísques.", "Cockburn Street",
                  [], "Arcade Bar Haggis and Whisky House, Edinburgh"),
                P("🍻", "Bennets Bar", "Pub vitoriano com espelhos e madeira originais.", "Tollcross", [],
                  "Bennets Bar, Edinburgh"),
                P("🍲", "Teuchters", "Comida de pub escocesa no West End.", "", [], "Teuchters, William Street, Edinburgh"),
            ],
        },
        {
            "nome": "Chuva e noite",
            "descricao": "Escurece antes das 16h40. O que fazer quando chove ou já está escuro.",
            "dicas": [
                ("Cobertos e grátis", "National Museum, Scottish National Gallery, Writers' Museum, Parlamento"),
                ("Cobertos e pagos", "Camera Obscura, Mary King's Close, Scotch Whisky Experience, Dynamic Earth, Palm Houses"),
                ("Abertos à noite", "Camera Obscura (até 19h30 ou mais) e Scotch Whisky Experience (até 20h)"),
                ("Pôr do sol", "Calton Hill, esplanada do castelo, escada Vennel na Grassmarket, Blackford Hill"),
                ("Ventania", "Scott Monument e às vezes o castelo fecham com vento forte; ter 03/11 Scott, Nelson e Writers' Museum fecham às 12h"),
                ("Domingo", "St Giles' só abre às 13h; o Parlamento não abre"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# Fife (sáb 07 a seg 09/11; o domingo 08 é o dia livre). Pesquisa de 10/10/2026.
# ---------------------------------------------------------------------------
CIDADES["fife"] = {
    "intro": (
        "Duas noites em Dalgety Bay, na margem norte do Forth, com o domingo 08/11 inteiro livre. De carro, "
        "Fife rende muito. Sem carro, o trem chega a Edimburgo em meia hora; no domingo passa mais ou menos "
        "de hora em hora, sem trem entre 10h30 e 12h07."
    ),
    "alerta": (
        "Fechados em novembro: Culross Palace, Falkland Palace e Hopetoun House. A abadia de Dunfermline só abre "
        "de terça a sábado. As vilas de Culross e Falkland, cenários de Outlander, continuam abertas para passear."
    ),
    "secoes": [
        {
            "nome": "Perto de casa",
            "descricao": "Tudo a menos de 15 minutos de carro, ou a pé e de trem.",
            "pontos": [
                P("🚶", "Fife Coastal Path até Aberdour",
                  "Trilha costeira de uns 6 km, passando pelas ruínas da igreja de St Bridget. Dá para ir a pé "
                  "e voltar de trem da estação de Aberdour.",
                  "~2 h · St Bridget's Kirk a 3 km de casa", ["Grátis"], "St Bridget's Kirk, Dalgety Bay"),
                P("🏰", "Aberdour Castle",
                  "Um dos castelos mais antigos da Escócia, com jardim murado. Fica colado à estação de Aberdour.",
                  "10h–16h, pausa 12h30–13h30 · aberto sáb, dom e seg · <b>£7,50</b> online",
                  ["Pago"], "Aberdour Castle"),
                P("🏖", "Silver Sands",
                  "Praia de Aberdour com vista para Edimburgo do outro lado do estuário.",
                  "", ["Grátis"], "Silver Sands Beach, Aberdour"),
                P("🌉", "North Queensferry e as pontes",
                  "As três pontes do Forth vistas de baixo, incluindo a ferroviária vermelha de 1890, patrimônio "
                  "da Unesco. O aquário Deep Sea World fica ali.",
                  "🚗 11 min · trem até North Queensferry", ["Grátis"], "North Queensferry"),
                P("⛴", "South Queensferry",
                  "Do outro lado, a vila sob a ponte ferroviária, com a melhor foto dela a partir do Hawes Pier.",
                  "🚗 14 min · estacionamento ~£1,50/h", ["Grátis"], "Hawes Pier, South Queensferry"),
            ],
            "dicas": [
                ("Mercado", "Tesco na Regents Way, a 19 minutos a pé; Asda e Aldi a uns 2 km"),
                ("Até a estação", "~30 minutos a pé ou 5 de táxi"),
            ],
        },
        {
            "nome": "Bate-voltas",
            "descricao": "Para o domingo, 08/11. Distâncias de carro a partir de Dalgety Bay.",
            "pontos": [
                P("⛳", "St Andrews",
                  "Ruínas da catedral à beira-mar, castelo no penhasco e o campo de golfe mais antigo do mundo, "
                  "que no domingo fica aberto para caminhar. A praia West Sands é a da abertura de Carruagens de Fogo.",
                  "🚗 1 h · catedral seg, sex, sáb e dom 10h–16h · castelo <b>£10</b>",
                  ["Grátis", "Castelo pago"], "St Andrews Cathedral"),
                P("🐟", "East Neuk",
                  "Vilas de pescadores: Anstruther, com o Anstruther Fish Bar, Pittenweem e Crail. Combina com "
                  "St Andrews num dia só, de carro.",
                  "🚗 1 h · Fish Bar dom a qui 11h30–21h (para viagem até 21h30)", [], "Anstruther Fish Bar"),
                P("🎬", "Culross",
                  "Vila do século 17 quase intacta, a Cranesmuir de Outlander. O palácio está fechado, mas a vila "
                  "e o café Bessie's (qui–seg) funcionam.",
                  "🚗 24 min", ["Grátis", "Palácio fechado"], "Culross"),
                P("🎬", "Falkland",
                  "Vila que fez de Inverness dos anos 40 em Outlander. O palácio fecha no inverno; loja e jardim "
                  "abrem de quinta a segunda.",
                  "🚗 35 min", ["Grátis", "Palácio fechado"], "Falkland"),
                P("🐴", "The Kelpies e Falkirk Wheel",
                  "Duas cabeças de cavalo de aço de 30 m e o elevador giratório de barcos, a 15 minutos de carro um do outro.",
                  "🚗 35–40 min · Kelpies sempre abertas · barco na Wheel <b>£17,50</b>, até 15h30",
                  ["Grátis", "Barco pago"], "The Kelpies"),
                P("🏰", "Stirling Castle",
                  "Castelo real no alto de uma rocha, com vista para o Monumento a William Wallace. "
                  "O estacionamento do castelo está fechado: use o park & ride Castleview.",
                  "🚗 46 min · 9h30–17h · <b>£18,50</b> online", ["Pago"], "Stirling Castle"),
                P("👑", "Linlithgow Palace",
                  "Ruína do palácio onde nasceu Mary, rainha dos escoceses, à beira de um lago.",
                  "🚗 24 min · 10h–16h · <b>£10</b> online", ["Pago"], "Linlithgow Palace"),
                P("⚓", "Blackness Castle",
                  "Castelo em forma de navio sobre o Forth, outro cenário de Outlander.",
                  "🚗 21 min · 10h–16h · <b>£7,50</b> online", ["Pago"], "Blackness Castle"),
                P("⛪", "Dunfermline Abbey",
                  "Túmulo de Robert the Bruce. No inverno só abre de terça a sábado, então só no sábado, 07/11.",
                  "🚗 15 min · grátis", ["Grátis", "Só no sábado"], "Dunfermline Abbey"),
            ],
            "dicas": [
                ("Domingo de carro", "St Andrews de manhã, Anstruther no almoço, volta antes das 16h30"),
                ("Domingo sem carro", "Coastal Path até Aberdour e castelo, ou trem para Edimburgo"),
                ("Desconto", "Código GOOD25 dá 25% nos castelos da Historic Environment Scotland para quem chega de ônibus ou trem"),
            ],
        },
        {
            "nome": "Edimburgo a partir de Fife",
            "descricao": "O trem atravessa a Forth Bridge e chega a Haymarket e Waverley.",
            "dicas": [
                ("Tempo", "~31 minutos até Waverley, passando por Haymarket"),
                ("Preço", "Ida ~£7,40; ida e volta ~£12,80 (tarifa cheia; confira no app da ScotRail)"),
                ("Dias úteis", "~36 trens por dia em cada sentido"),
                ("Domingo", "~16 trens: o primeiro às 8h51, mais ou menos de hora em hora (sem trem entre 10h30 e 12h07)"),
                ("Bom para domingo", "Holyroodhouse abre no domingo; o Parlamento e a St Giles' de manhã, não"),
            ],
        },
    ],
}

# Traçado aproximado do percurso (A9 entre Perth e Inverness; linha da costa leste até York), (lat, lon)
ROTA_MAPA = [
    (55.93, -3.23), (55.9990, -3.4060), (56.3960, -3.4370), (56.7024, -3.7348), (56.9374, -4.2418),
    (57.1950, -3.8250), (57.4778, -4.2213),
    (57.1950, -3.8250), (56.9374, -4.2418), (56.7024, -3.7348), (56.3960, -3.4370), (56.03, -3.36),
    (55.9460, -3.1890), (55.7710, -2.0070), (54.9690, -1.6170), (54.7790, -1.5720), (53.96, -1.08),
]

# Destinos dos passeios, para o mapa do roteiro (coordenadas aproximadas)
PONTOS_MAPA = [
    {"nome": n, "lat": la, "lon": lo} for n, la, lo in [
        ("Urquhart Castle", 57.3242, -4.4419), ("Culloden", 57.4777, -4.0926), ("Fort George", 57.5830, -4.0690),
        ("Chanonry Point", 57.5741, -4.0937), ("Fort Augustus", 57.1448, -4.6806), ("Eilean Donan", 57.2739, -5.5161),
        ("Plodda Falls", 57.2729, -4.8585), ("Loch an Eilein", 57.1505, -3.8228), ("Dalwhinnie", 56.9374, -4.2418),
        ("Pitlochry", 56.7024, -3.7348), ("Dunkeld", 56.5651, -3.5858), ("Glen Ord", 57.5147, -4.4669),
        ("St Andrews", 56.3398, -2.7967), ("Anstruther", 56.2231, -2.6996), ("Culross", 56.0558, -3.6290),
        ("Falkland", 56.2534, -3.2073), ("Stirling Castle", 56.1238, -3.9481), ("The Kelpies", 56.0194, -3.7546),
        ("Linlithgow", 55.9790, -3.6010), ("Harrogate", 53.9921, -1.5418), ("Scarborough", 54.2826, -0.4005),
    ]
]

# ---------------------------------------------------------------------------
# Trechos
# ---------------------------------------------------------------------------
TRECHOS_INTRO = (
    "Recomendação: carro só de 05 a 09/11. Retirem no aeroporto de Edimburgo no dia 05 (fora da zona de "
    "baixa emissão do centro), usem nas Highlands e em Fife, e devolvam no mesmo aeroporto no dia 09, seguindo "
    "de trem para York. Em Edimburgo e em York, carro só atrapalha. Sem carro, tudo abaixo funciona de trem, "
    "com uma excursão no dia 06."
)

TRECHOS = [
    {
        "titulo": "Chegada em Edimburgo",
        "quando": "seg 02/11 · check-in a partir das 14h",
        "descricao": "Vindo de Londres de trem ou de avião, até a casa em Shandon.",
        "opcoes": [
            {"emoji": "🚆", "nome": "Trem de Londres (LNER)", "resumo": "~4h20 de King's Cross a Waverley",
             "texto": "Comprem antecipado no site da LNER. De Waverley, os ônibus 4 e 44 saem da Princes Street, ao lado, "
                      "até a Slateford Road; de táxi são uns 15 minutos."},
            {"emoji": "🚌", "nome": "Airlink 100", "resumo": "~30 min até o centro · £6, ida e volta £8,50",
             "texto": "Sai a cada 10 minutos, 24 horas. Desçam em Haymarket ou no centro e peguem o 4 ou o 44 até a Slateford Road."},
            {"emoji": "🚋", "nome": "Bonde", "resumo": "~35 min até Princes Street · £7,90",
             "texto": "A cada 7 a 10 minutos. Para em Haymarket, de onde a casa fica a uns 25 minutos a pé."},
            {"emoji": "🚕", "nome": "Táxi ou Uber", "resumo": "O mais simples com mala",
             "texto": "Shandon fica no caminho entre o aeroporto e o centro."},
        ],
    },
    {
        "titulo": "Edimburgo → Inverness",
        "quando": "qui 05/11 · check-out 10h, check-in 15h",
        "descricao": "O trecho mais bonito da viagem, subindo pela A9 e pela linha das Highlands.",
        "opcoes": [
            {"emoji": "🚆", "nome": "Trem ScotRail direto", "resumo": "~3h20–3h40 · a partir de ~£16–22 antecipado",
             "texto": "Uns 12 trens por dia saindo de Waverley. A tarifa antecipada é por trem e as baratas acabam primeiro: comprem já."},
            {"emoji": "🚗", "nome": "Carro pela A9", "resumo": "253 km · ~3h30 sem paradas, ~4h na prática",
             "texto": "Queensferry Crossing, M90, Perth e A9. Há um trecho em obras ao norte de Dunkeld com limite de 40 mph o dia inteiro e outro perto de Tomatin."},
            {"emoji": "🚌", "nome": "Ônibus Citylink/Megabus", "resumo": "~4 h · o mais barato",
             "texto": "Linha M90. Mais lento e sem as paradas no caminho."},
        ],
        "paradas": [
            P("⛪", "Dunkeld", "Catedral em ruínas à beira do rio Tay e a trilha The Hermitage, com cachoeira.",
              "Logo ao sair da M90", ["Grátis"], "Dunkeld Cathedral"),
            P("🥃", "Pitlochry", "Cidadezinha vitoriana com a destilaria Blair Athol e a represa. "
              "O mirante Queen's View fica a poucos minutos.",
              "Blair Athol abre todos os dias; reserve o tour", [], "Pitlochry"),
            P("🛍", "House of Bruar", "Loja de lã e mercado de comida escocesa, boa parada para almoço.",
              "Lojas 9h30–17h30", [], "House of Bruar"),
            P("🥃", "Dalwhinnie", "Destilaria no ponto mais alto da A9. Pode fechar com mau tempo.",
              "10h–16h · tour £21", ["Pago"], "Dalwhinnie Distillery"),
            P("🏰", "Blair Castle", "Fechado: a temporada de 2026 terminou em 30/10.", "", ["Fechado"], "Blair Castle"),
        ],
    },
    {
        "titulo": "Inverness → Dalgety Bay",
        "quando": "sáb 07/11 · check-out 10h",
        "descricao": "Mesmo caminho de volta para o sul. Neste sábado a linha Inverness–Perth está em obras (ônibus no lugar do trem); de carro não muda nada. Dia de jogo em Murrayfield: evitem Haymarket entre 13h e 18h.",
        "opcoes": [
            {"emoji": "🚆", "nome": "Trem", "resumo": "~4h30 ou mais · ônibus substituto até Perth",
             "texto": "Obras em Dalwhinnie: no sábado 07/11 não há trem entre Inverness e Perth. Ônibus da ScotRail fazem "
                      "esse trecho; em Perth, trem até Inverkeithing ou Edimburgo. Confiram os horários na véspera."},
            {"emoji": "🚗", "nome": "Carro", "resumo": "234 km · ~3 h sem paradas",
             "texto": "Culloden e Clava cedo, depois A9 com parada em Aviemore (Loch an Eilein) ou Dalwhinnie. Chegar antes de escurecer, perto das 16h20."},
        ],
    },
    {
        "titulo": "Dalgety Bay → York",
        "quando": "seg 09/11 · check-in 15h",
        "descricao": "Atravessa a fronteira. De trem é mais rápido e mais barato que de carro.",
        "opcoes": [
            {"emoji": "🚆", "nome": "Trem via Edimburgo", "resumo": "~2h15–3h · a partir de ~£19 antecipado",
             "texto": "LNER de Waverley a York. A LNER libera as tarifas 12 semanas antes; comprem direto no site dela, sem taxa."},
            {"emoji": "🚆", "nome": "Trem direto de Inverkeithing", "resumo": "~2h50–3h20 · a partir de ~£26",
             "texto": "Alguns LNER e CrossCountry saem de Inverkeithing, a uma estação de Dalgety Bay, direto para York."},
            {"emoji": "🚗", "nome": "Carro pela A1", "resumo": "361 km · 5 h ou mais",
             "texto": "Não compensa: taxa por devolver na Inglaterra e o centro de York não tem como estacionar perto do apartamento. "
                      "Melhor devolver no aeroporto de Edimburgo (25 min de Dalgety Bay) e seguir de trem."},
        ],
    },
    {
        "titulo": "Saída de York",
        "quando": "qua 11/11 · check-out 11h",
        "descricao": "A estação fica a 15 minutos a pé da Grape Lane.",
        "opcoes": [
            {"emoji": "🚆", "nome": "Londres King's Cross", "resumo": "~2 h · LNER a cada 30 min · a partir de ~£18",
             "texto": "Na hora pode passar de £80; com antecedência sai bem mais barato."},
            {"emoji": "✈️", "nome": "Manchester Airport", "resumo": "~2 h · TransPennine direto",
             "texto": "Trem de hora em hora, sem baldeação."},
        ],
    },
]

# ---------------------------------------------------------------------------
# Dicas
# ---------------------------------------------------------------------------
DICAS = [
    {"titulo": "Dinheiro e taxas", "itens": [
        ("Moeda", "Libra. Cartão por aproximação funciona em quase tudo, até em ônibus"),
        ("Notas escocesas", "Valem no Reino Unido inteiro, mas lojas na Inglaterra às vezes estranham: gastem antes de York"),
        ("Gorjeta", "10 a 12,5% no restaurante se a conta não trouxer service charge; no balcão do pub, não se dá"),
        ("Taxa de turismo de Edimburgo", "5% sobre as 3 noites, cobrada pelo anfitrião: perguntem ao anfitrião se já está no preço"),
        ("Highlands", "Sem taxa de turismo em 2026"),
        ("St Giles'", "£12 por pessoa desde outubro de 2026"),
    ]},
    {"titulo": "Trem", "itens": [
        ("ScotRail", "Desde setembro de 2025 não existe mais tarifa de horário de pico"),
        ("Two Together Railcard", "£35, digital, 1/3 de desconto para duas pessoas juntas; não vale antes das 9h30 em dias úteis"),
        ("LNER", "Tarifas saem 12 semanas antes; o dia 09/11 já está à venda"),
        ("Castelos com desconto", "Código GOOD25: 25% na Historic Environment Scotland chegando de ônibus ou trem"),
    ]},
    {"titulo": "Carro", "itens": [
        ("Mão", "Inglesa. Na rotatória, preferência para quem vem da direita"),
        ("Velocidade", "30 mph na cidade (muitas ruas de Edimburgo a 20), 60 em pista simples, 70 em pista dupla"),
        ("Álcool", "Limite escocês mais rígido que o inglês. Quem dirige, não bebe"),
        ("Zonas de baixa emissão", "Centros de Edimburgo, Glasgow, Dundee e Aberdeen; multa de £60. Carro alugado costuma estar liberado"),
        ("Estacionar em Edimburgo", "£6 a £9 por hora no centro"),
        ("Combustível", "Gasolina ~£1,75/litro, diesel ~£2,00/litro (outubro de 2026)"),
        ("CNH brasileira", "Confirmem com a locadora se pedem a Permissão Internacional para Dirigir"),
    ]},
    {"titulo": "Datas da viagem", "itens": [
        ("05/11, quinta", "Bonfire Night: em Inverness, fogueira (18h) e fogos (19h) oficiais e grátis no Bught Park; a Infirmary Bridge fecha"),
        ("07/11, sábado", "Escócia × Nova Zelândia em Murrayfield às 14h10"),
        ("08/11, domingo", "Remembrance Sunday: em 2025 o desfile saiu do castelo às 10h, com cerimônia às 11h na Royal Mile"),
        ("11/11, quarta", "Armistício: dois minutos de silêncio às 11h"),
        ("Natal", "Começa depois da viagem: Edimburgo em 14/11, York em 12/11"),
    ]},
    {"titulo": "Saúde e segurança", "itens": [
        ("Emergência", "999"),
        ("Sem urgência", "111 (NHS 24 na Escócia, NHS 111 na Inglaterra)"),
        ("Farmácia", "Boots e Superdrug em todos os centros"),
        ("Cidades", "As quatro são tranquilas; à noite, cuidado só com bebedeira na Cowgate e na Grassmarket"),
    ]},
    {"titulo": "Fuso e tomada", "itens": [
        ("Horário", "GMT, 3 horas à frente de Brasília"),
        ("Tomada", "Tipo G, 230 V"),
        ("Domingo", "Na Inglaterra, lojas grandes abrem só 6 horas; na Escócia não há essa regra"),
    ]},
]

# ---------------------------------------------------------------------------
# Gastos (libras por pessoa por dia, sem hospedagem, que já está paga)
# ---------------------------------------------------------------------------
PERFIS = {
    "Econômico": {"Alimentação": 35, "Transporte local": 8, "Atrações": 15, "Extras": 10},
    "Médio": {"Alimentação": 55, "Transporte local": 12, "Atrações": 30, "Extras": 20},
    "Premium": {"Alimentação": 100, "Transporte local": 25, "Atrações": 55, "Extras": 40},
}
CATEGORIAS = {
    "Alimentação": "café, almoço, jantar e lanches",
    "Transporte local": "ônibus, bonde, táxi",
    "Atrações": "castelos, museus, tours",
    "Extras": "lembranças, imprevistos, gorjetas",
}
TRECHOS_POR_PESSOA = 70  # três trechos de trem com tarifa antecipada
GASTOS_NOTA = (
    "Inclui os três trechos de trem com tarifa antecipada (~£70 por pessoa). Com carro de 05 a 09/11, troque isso "
    "pela diária da locadora mais ~£60–80 de combustível. A hospedagem fica de fora."
)
PRECOS = [
    ("Edinburgh Castle", "£23,50 online"),
    ("Palace of Holyroodhouse", "£22 antecipado"),
    ("St Giles' Cathedral", "£12"),
    ("Camera Obscura", "£24,95"),
    ("National Museum e National Gallery", "Grátis"),
    ("Urquhart Castle", "£14 online"),
    ("Inverness Castle", "£20 online"),
    ("Stirling Castle", "£18,50 online"),
    ("York Minster", "£20; com a torre £26"),
    ("Ônibus em Edimburgo", "£2,40; teto diário por aproximação £5,70"),
    ("Airlink 100 (aeroporto)", "£6; ida e volta £8,50"),
    ("Trem Edimburgo–Inverness", "a partir de ~£16–22 antecipado"),
    ("Trem Edimburgo–York", "a partir de ~£19 antecipado"),
]

# ---------------------------------------------------------------------------
# Glencoe e Skye: opções para decidir na hora, conforme o tempo e a disposição.
# Tempos de carro calculados com OSRM em 10/10/2026 (sem trânsito nem paradas); o app soma 20% como margem.
# ---------------------------------------------------------------------------
DESTINOS_EXTRA = [
    {"id": "glencoe", "nome": "Glencoe", "lat": 56.6826, "lon": -5.1023},
    {"id": "skye", "nome": "Skye (Portree)", "lat": 57.4125, "lon": -6.1960},
]

# Mesmas datas (05 a 07/11) de 2015 a 2025, ERA5 via Open-Meteo
NORMAIS_EXTRA = {
    "glencoe": {"max_media": 10.6, "min_media": 6.1, "dias_chuva_pct": 61, "rajada_media_kmh": 45, "dias_bons_pct": 61},
    "skye": {"max_media": 10.6, "min_media": 7.2, "dias_chuva_pct": 70, "rajada_media_kmh": 47, "dias_bons_pct": 58},
}

GLENCOE_SKYE_INTRO = (
    "Dois lugares que valem a viagem, mas que dependem de céu aberto e de disposição. Aqui ficam as formas "
    "de encaixar cada um, com o tempo previsto para o dia. Respondam as duas perguntas e o painel mostra o que "
    "cabe. A decisão boa se toma na véspera."
)

CENARIOS = [
    {
        "titulo": "Glencoe no caminho para Inverness",
        "dia": date(2026, 11, 5), "locais": ["glencoe"], "carro": True, "minutos": 286,
        "comparacao": "Em vez da A9 direta (3h26): Glencoe soma ~1h20 de volante.",
        "rota": "Edimburgo → Stirling → Crianlarich → Rannoch Moor → Glencoe → Fort William → Fort Augustus → Inverness",
        "plano": [
            ("8h00", "Saída de Edimburgo, com o carro retirado no aeroporto"),
            ("10h15", "Rannoch Moor e Buachaille Etive Mòr, a montanha da entrada do vale"),
            ("10h45", "Mirante das Three Sisters e Glencoe Visitor Centre; almoço"),
            ("12h45", "Fort William e o Commando Memorial, em Spean Bridge"),
            ("14h15", "Fort Augustus, nas eclusas do Loch Ness"),
            ("15h30", "Check-in em Inverness, antes do pôr do sol (16h23)"),
        ],
        "observacao": "A opção que mais rende: troca a A9 pela estrada mais bonita da Escócia sem gastar um dia a mais.",
    },
    {
        "titulo": "Skye de excursão",
        "dia": date(2026, 11, 6), "locais": ["skye"], "carro": False, "minutos": 0,
        "comparacao": "Ninguém dirige. Dia inteiro: das 8h às 20h.",
        "rota": "Inverness → Eilean Donan → Skye (Portree e Storr ou Quiraing, conforme o tempo) → volta pela Skye Bridge",
        "plano": [
            ("8h00", "Saída da parada ao lado da catedral, na Ardross Street (chegar 15 min antes)"),
            ("~10h", "Eilean Donan"),
            ("meio do dia", "Skye, com paradas escolhidas pelo guia conforme o tempo"),
            ("20h00", "Chegada em Inverness"),
        ],
        "observacao": "Rabbie's, a partir de ~£58 por pessoa, em van de 16 lugares. Cancelamento grátis até 24 h antes: "
                      "dá para reservar já e decidir na véspera.",
    },
    {
        "titulo": "Skye de carro",
        "dia": date(2026, 11, 6), "locais": ["skye"], "carro": True, "minutos": 330,
        "comparacao": "O dia mais puxado ao volante. A volta termina no escuro.",
        "rota": "Inverness → Eilean Donan → Skye Bridge → Sligachan → Portree → Old Man of Storr → volta pela mesma estrada",
        "plano": [
            ("7h30", "Saída, ainda escuro (o sol nasce às 7h40)"),
            ("9h10", "Eilean Donan por fora; a bilheteria abre às 10h"),
            ("10h15", "Ponte velha de Sligachan, com as montanhas Cuillin"),
            ("10h40", "Portree: porto colorido e almoço"),
            ("11h45", "Old Man of Storr: trilha de 1h30 a 2h, só com tempo seco"),
            ("14h00", "Início da volta"),
            ("~17h00", "Inverness, com a última hora no escuro"),
        ],
        "observacao": "Quiraing e Fairy Pools não cabem com luz. Abasteçam em Inverness; em Skye há posto em Broadford e Portree.",
    },
    {
        "titulo": "Glencoe no caminho para Fife",
        "dia": date(2026, 11, 7), "locais": ["glencoe"], "carro": True, "minutos": 270,
        "comparacao": "Em vez da A9 direta (3h01): Glencoe soma ~1h30 e evita Edimburgo no dia do jogo em Murrayfield.",
        "rota": "Inverness → Fort Augustus → Fort William → Glencoe → Rannoch Moor → Crianlarich → Stirling → Dalgety Bay",
        "plano": [
            ("8h00", "Saída de Inverness"),
            ("9h00", "Fort Augustus"),
            ("10h15", "Glencoe: Visitor Centre, Three Sisters e Glencoe Lochan"),
            ("12h15", "Rannoch Moor e saída para o sul"),
            ("15h00", "Dalgety Bay, com folga antes do pôr do sol (16h21)"),
        ],
        "observacao": "Se no dia 05 o tempo não deixar, esta é a segunda chance de ver Glencoe.",
    },
    {
        "titulo": "Skye no dia 06 e Glencoe no dia 07",
        "dia": date(2026, 11, 6), "locais": ["skye", "glencoe"], "carro": True, "minutos": 330,
        "tempo": [("skye", date(2026, 11, 6)), ("glencoe", date(2026, 11, 7))],
        "comparacao": "Umas 10 horas ao volante em dois dias seguidos.",
        "rota": "Dia 06: Skye de carro. Dia 07: Inverness → Glencoe → Dalgety Bay.",
        "plano": [],
        "observacao": "Só com dois motoristas, tempo bom nos dois lugares e disposição sobrando. "
                      "Alternativa mais leve: Skye de excursão no dia 06 e Glencoe de carro no dia 07.",
    },
    {
        "titulo": "Plano B: perto de Inverness",
        "dia": date(2026, 11, 6), "locais": [], "carro": False, "minutos": 60, "reserva": True,
        "comparacao": "Para dia de alerta, ventania ou cansaço.",
        "rota": "Culloden, Clava Cairns, Loch Ness até o Urquhart e uma destilaria, tudo a menos de 40 minutos",
        "plano": [],
        "observacao": "Funciona de carro ou de ônibus. Os detalhes estão na aba Highlands.",
    },
]

GLENCOE = [
    P("🏔", "Rannoch Moor e Buachaille Etive Mòr",
      "Planalto de turfa e lagos que a A82 atravessa antes de Glencoe. A montanha cônica na entrada do vale é a foto "
      "clássica, tirada perto do hotel Kingshouse.",
      "Mirantes à beira da estrada", ["Grátis"], "Buachaille Etive Mor viewpoint"),
    P("⛰", "Three Sisters",
      "Três montanhas lado a lado, vistas de um estacionamento na A82. Com nuvem baixa, somem por completo.",
      "Parada de 15 minutos", ["Grátis"], "Three Sisters viewpoint, Glencoe"),
    P("🏛", "Glencoe Visitor Centre",
      "Centro do National Trust sobre o massacre de 1692 e a geologia do vale, com café.",
      "Inverno 2026: todos os dias 9h30–16h · entrada grátis, estacionamento pago",
      ["Grátis"], "Glencoe Visitor Centre"),
    P("🌲", "Glencoe Lochan",
      "Trilha plana em volta de um lago com bosque, acima da vila. Boa até com chuva fraca.",
      "~40 min", ["Grátis"], "Glencoe Lochan"),
    P("🍺", "Clachaig Inn",
      "Pub de montanhistas com mais de 300 anos, lareira e comida farta.",
      "", [], "Clachaig Inn"),
    P("🌉", "Fort William e arredores",
      "A escada de oito eclusas Neptune's Staircase, em Banavie, e o Commando Memorial, com vista do Ben Nevis.",
      "🚗 Fort William a 27 min de Glencoe", ["Grátis"], "Neptune's Staircase"),
]

SKYE = [
    P("🏯", "Eilean Donan", "No caminho, antes da ponte. Aberto no dia 06, fechado no dia 07.",
      "10h–16h · <b>£13</b>, só na bilheteria", ["Pago"], "Eilean Donan Castle"),
    P("🌉", "Sligachan", "Ponte de pedra antiga com as montanhas Cuillin ao fundo. Parada rápida e de graça.",
      "", ["Grátis"], "Sligachan Old Bridge"),
    P("⚓", "Portree", "A capital da ilha, com o porto de casas coloridas. É onde há mais coisa aberta no inverno.",
      "", ["Grátis"], "Portree Harbour"),
    P("🗿", "Old Man of Storr",
      "Pináculo de rocha num paredão. Trilha íngreme e enlameada de uns 4 km ida e volta. Com chuva forte ou "
      "vento, não vale.",
      "1h30–2h · estacionamento ~£6 (a tarifa subiu em 2026; confira)", ["Estacionamento pago"], "Old Man of Storr"),
    P("🌊", "Kilt Rock", "Penhasco listrado com cachoeira caindo no mar, visto de um mirante à beira da estrada.",
      "20 min ao norte do Storr", ["Grátis"], "Kilt Rock"),
    P("💧", "Fairy Pools",
      "Piscinas de água azul no rio, ao pé das Cuillin. Estrada de pista única e trilha de 2,4 km: não cabem num "
      "bate-volta de novembro.", "", [], "Fairy Pools"),
    P("🥃", "Talisker",
      "A destilaria da ilha, em Carbost. A manutenção de 2026 foi de 11/10 a 1/11: está aberta no dia 06.",
      "Nov–fev: todos os dias 10h–16h30 · pode fechar com mau tempo", ["Pago"], "Talisker Distillery"),
    P("🏰", "Dunvegan Castle", "Fechado: a temporada vai de 1/4 a 15/10.", "", ["Fechado"], "Dunvegan Castle"),
]

CHECKLIST = [
    ("Alertas", "Met Office: aviso amarelo de vento ou neve nas Highlands derruba o plano"),
    ("Montanha", "MWIS (West Highlands) diz se as montanhas vão estar encobertas"),
    ("Estradas", "Traffic Scotland: A82 (Glencoe) e A87 (Skye)"),
    ("Luz", "Sair até 8h; o sol se põe por volta das 16h20"),
    ("Combustível", "Tanque cheio em Inverness ou Fort William"),
    ("Excursão", "Reservar já e cancelar até 24 h antes se o tempo virar"),
    ("Corpo", "Quem dirige dormiu bem? Cinco horas de pista estreita cansam mais do que parece"),
]

LINKS_GLENCOE_SKYE = [
    ("Alertas do Met Office", "https://weather.metoffice.gov.uk/warnings-and-advice/uk-warnings"),
    ("MWIS West Highlands", "https://www.mwis.org.uk/forecasts/scottish/west-highlands"),
    ("Traffic Scotland", "https://www.traffic.gov.scot/"),
]

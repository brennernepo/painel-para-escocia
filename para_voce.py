"""Aba "Para você": sugestões pessoais por cidade (trabalho com notebook, economia e história, música, bebida,
comida, hidratação e futebol). Mesmo formato de CIDADES em dados.py; as coordenadas ficam em COORD, no fim.
Pesquisa de 31/10/2026; o que não teve confirmação oficial diz "confira".
"""

from dados import P

INTRO = (
    "Escolhas para o seu jeito de viajar: onde abrir o notebook (e onde dá para fazer chamada; o Brasil está 3 horas "
    "atrás), Smith e Hume no ano dos 250 anos de A Riqueza das Nações, shows nas suas datas, pubs, comida boa e "
    "onde encher a garrafa d'água. Cada lugar mostra a distância da casa da cidade escolhida."
)

PARA_VOCE = {}

# ---------------------------------------------------------------------------
# Edimburgo (seg 02 a qui 05/11, e talvez dom 08/11 vindo de Dalgety Bay)
# ---------------------------------------------------------------------------
PARA_VOCE["edimburgo"] = {
    "intro": (
        "Edimburgo é a cidade de Adam Smith e David Hume, e em 2026 A Riqueza das Nações faz 250 anos. A casa fica "
        "a 10 minutos do Tynecastle e do canal: dá para alternar notebook, peregrinação iluminista e pint com trad "
        "music sem cruzar a cidade. Na quinta 05 você sai às 10h, então as noites são seg, ter e qua."
    ),
    "secoes": [
        {
            "nome": "Trabalhar",
            "descricao": "Bibliotecas grátis perto de casa e coworkings no centro para os dias de videochamada.",
            "pontos": [
                P("📚", "Fountainbridge Library",
                  "A biblioteca pública mais perto da casa, com mesas de estudo e tomadas. Boa para escrever posts e "
                  "preparar aulas; é silenciosa, então chamadas em outro lugar.",
                  "Seg 13h–20h · ter e qua 10h ou 13h até 17h ou 20h (confira) · <b>grátis</b>",
                  ["Grátis", "Tomadas", "Wi-fi"], "Fountainbridge Library 137 Dundee Street Edinburgh"),
                P("🏛", "Central Library",
                  "A biblioteca central, com wi-fi grátis e aberta até as 20h de segunda a quarta. Colada ao Museum "
                  "on the Mound e ao Sneaky Pete's: tarde de trabalho, depois museu ou show.",
                  "Seg–qua 10h–20h · qui 10h–17h · <b>grátis</b>",
                  ["Grátis", "Wi-fi"], "Edinburgh Central Library George IV Bridge"),
                P("📖", "National Library of Scotland",
                  "Cadastro de leitor grátis dá acesso ao acervo, com obras do Iluminismo escocês. Tem café no prédio: "
                  "trabalhe ali e peça uma primeira edição de Smith ou Hume na sala de leitura.",
                  "Seg–qui 10h–19h (confira) · <b>grátis</b> · em frente à Central Library",
                  ["Grátis", "Wi-fi"], "National Library of Scotland George IV Bridge"),
                P("💼", "The Melting Pot",
                  "Coworking ao lado da estação Waverley, com salas de reunião e cabines silenciosas. A melhor opção "
                  "do centro para chamada de vídeo com privacidade.",
                  "Seg–sex 8h30–17h30 · day pass <b>~£30 + VAT</b> (confira) · reserve antes",
                  ["Pago", "Reserva", "Wi-fi", "Chamada ok"], "The Melting Pot 15 Calton Road Edinburgh"),
                P("🏢", "Spaces Lochrin Square",
                  "Coworking da rede IWG na ponta de Fountainbridge, no caminho a pé entre a casa e o centro. Serve "
                  "para um dia inteiro de reuniões.",
                  "Seg–sex (confira horário) · day pass <b>a partir de ~£25</b> (confira)",
                  ["Pago", "Reserva", "Wi-fi", "Chamada ok"], "Spaces Lochrin Square 92 Fountainbridge Edinburgh"),
                P("☕", "Black Medicine Coffee",
                  "Café de madeira rústica que aceita longas sessões de notebook, com tomadas pelo salão. A dois passos "
                  "do Royal Oak e do Captain's Bar: trabalho de tarde, música à noite.",
                  "Todos os dias (confira horário) · café <b>£</b> · peça a senha do wi-fi",
                  ["Barato", "Wi-fi", "Tomadas"], "Black Medicine Coffee 2 Nicolson Street Edinburgh"),
            ],
        },
        {
            "nome": "Economia e história",
            "descricao": "Nos 250 anos de A Riqueza das Nações: Smith, Hume e a história bancária escocesa.",
            "pontos": [
                P("🪦", "Túmulo de Adam Smith",
                  "O túmulo restaurado fica no canto do Canongate Kirkyard, com tijolos de bronze no chão guiando até "
                  "ele. No ano dos 250 anos do livro, rende um vídeo para o LinkedIn ou o podcast.",
                  "Todos os dias, com luz (até ~16h30) · <b>grátis</b>",
                  ["Grátis"], "Canongate Kirkyard Adam Smith grave Edinburgh"),
                P("🏠", "Adam Smith's Panmure House",
                  "Smith morou aqui de 1778 até morrer, em 1790. Não abre ao público nas suas datas (o próximo evento é "
                  "em 10/11), mas a fachada e o pátio ficam a 100 m do túmulo.",
                  "Só por fora em 02–08/11 · <b>grátis</b> · 4 Lochend Close",
                  ["Grátis"], "Adam Smith's Panmure House 4 Lochend Close Edinburgh"),
                P("🏦", "Museum on the Mound",
                  "O museu do dinheiro, na sede histórica do Bank of Scotland (fundado em 1695). Cédulas, cofres, "
                  "falsificações e crises bancárias: material pronto para as suas aulas.",
                  "Ter–sáb 13h–17h, última entrada 16h45 · vá <b>ter 03 ou qua 04</b> · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Museum on the Mound Edinburgh"),
                P("🕯", "Mausoléu de David Hume",
                  "O mausoléu redondo de Hume, desenhado por Robert Adam, no Old Calton Burial Ground, ao pé do Calton "
                  "Hill. Feche o roteiro com as estátuas de Hume (High Street) e de Smith (Parliament Square).",
                  "Todos os dias, com luz (confira horário) · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Old Calton Burial Ground Waterloo Place Edinburgh"),
                P("💷", "Dundas House (RBS)",
                  "Mansão de 1774 que virou sede do Royal Bank of Scotland e segue como agência, com o salão de cúpula "
                  "estrelada. Entre num dia útil, de preferência depois do café no Dishoom, ao lado.",
                  "Seg–sex em horário bancário (confira) · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Royal Bank of Scotland Dundas House 36 St Andrew Square Edinburgh"),
                P("📚", "Topping & Company Booksellers",
                  "Livraria independente enorme, com escadas de madeira e ótima seção de história e filosofia. Lugar "
                  "para comprar uma edição comemorativa de Smith ou Hume.",
                  "Todos os dias 9h–21h",
                  ["Grátis"], "Topping & Company Booksellers 2 Blenheim Place Edinburgh"),
            ],
        },
        {
            "nome": "Música",
            "descricao": "Shows confirmados na agenda das casas para 02–04/11 e 08/11, trad ao vivo e vinil.",
            "pontos": [
                P("🎤", "Van Morrison no Usher Hall",
                  "Van the Man em turnê, a 30 minutos a pé da casa: pauta pronta para o Substack. Esgotado; só vale "
                  "tentar a revenda oficial da casa.",
                  "<b>Ter 03/11</b> · horário: confira · revenda oficial",
                  ["Show", "Esgotado"], "Usher Hall Lothian Road Edinburgh"),
                P("🎸", "Sneaky Pete's",
                  "Porão minúsculo e lendário da Cowgate, vitrine do indie local. Seg 02 Mae Stephens; ter 03 Gus Ives; "
                  "qua 04 cootie catcher, Flame e Floor Dwellers; dom 08 Dusky (DJ set).",
                  "Seg–qua <b>19h</b> · dom 08 <b>18h</b> · preço: confira",
                  ["Show", "Pago"], "Sneaky Pete's 73 Cowgate Edinburgh"),
                P("🎻", "The Queen's Hall",
                  "Igreja convertida em sala de concerto, com acústica ótima e longa história no folk escocês. Na "
                  "quarta toca a banda de rock turco mor ve ötesi: um ângulo inusitado para o blog.",
                  "<b>Qua 04/11 19h30</b> · preço: confira",
                  ["Show", "Pago", "Reserva"], "The Queen's Hall 85-89 Clerk Street Edinburgh"),
                P("🪕", "The Royal Oak",
                  "Pub minúsculo dedicado ao folk, com música ao vivo toda noite. Se voltar no domingo, às 20h tem o "
                  "Wee Folk Club no andar de baixo.",
                  "Todas as noites · dom 08: Wee Folk Club <b>20h, ~£9</b> (confira)",
                  ["Show", "Barato"], "The Royal Oak 1 Infirmary Street Edinburgh"),
                P("💿", "VoxBox Music",
                  "Loja de vinil independente em Stockbridge, com garimpo de indie, folk e rock escocês. Fecha segunda "
                  "e terça: vá na quarta.",
                  "<b>Qua 04/11 12h–17h</b> · dom 12h–16h · fecha seg e ter",
                  ["Grátis", "Fecha cedo"], "VoxBox Music 21 St Stephen Street Edinburgh"),
                P("🎼", "BBC Scottish Symphony no Usher Hall",
                  "Se voltar no domingo: a orquestra da BBC na Escócia toca a Quinta de Tchaikovsky na sala mais bonita "
                  "da cidade.",
                  "<b>Dom 08/11</b> · horário e preço: confira",
                  ["Show", "Pago", "Reserva"], "Usher Hall Lothian Road Edinburgh"),
            ],
        },
        {
            "nome": "Beber",
            "descricao": "Pubs de bairro perto de casa e, no caminho para o centro, real ale e whisky.",
            "pontos": [
                P("🍺", "The Athletic Arms",
                  "O pub da torcida do Hearts, colado ao Tynecastle, famoso pela cerveja bem tirada. O lugar para "
                  "falar de futebol com os locais.",
                  "Seg–qua 11h–0h · qui até 1h · pint <b>~£5</b> (confira)",
                  ["Barato"], "Athletic Arms 1 Angle Park Terrace Edinburgh"),
                P("🍻", "The Caley Sample Room",
                  "Gastropub espaçoso a 8 minutos de casa, com boa carta de cervejas e comida de pub. Bom para a "
                  "primeira noite, na segunda.",
                  "Seg–qua 16h–23h · qui 12h–0h (confira) · <b>£</b>",
                  ["Barato"], "Caley Sample Room 42-58 Angle Park Terrace Edinburgh"),
                P("⛪", "Cloisters Bar",
                  "Antiga casa paroquial em Tollcross virou bar de real ale, com muitas torneiras escocesas. Fica na "
                  "volta do centro para casa.",
                  "Seg 13h–23h · ter 12h–23h (confira) · <b>£</b>",
                  ["Barato"], "Cloisters Bar 26 Brougham Street Edinburgh"),
                P("🥃", "The Blue Blazer",
                  "Pub de esquina com dezenas de single malts e real ales, frequentado por locais. A 5 minutos do Usher "
                  "Hall: antes ou depois do show.",
                  "Seg–sáb 11h–1h · dom 12h30–1h · <b>££</b>",
                  ["Pago"], "Blue Blazer 2 Spittal Street Edinburgh"),
                P("🎶", "The Captain's Bar",
                  "Pub minúsculo com sessões de trad e folk quase toda noite. Peça um pint e ouça: vira texto para o "
                  "Substack.",
                  "Seg–sex 14h–1h · sessões à noite (confira) · <b>£</b>",
                  ["Show", "Barato"], "The Captains Bar 4 South College Street Edinburgh"),
            ],
        },
        {
            "nome": "Comer bem",
            "descricao": "Um italiano de bairro perto de casa, curry barato no centro e dois especiais.",
            "pontos": [
                P("🍝", "Locanda de Gusti",
                  "Italiano napolitano de bairro na Dalry Road, com massas e frutos do mar, querido pelos locais. Abre "
                  "segunda à noite: jantar do dia da chegada.",
                  "Seg 17h–22h · ter–sex almoço e jantar (confira) · <b>££</b>",
                  ["Pago", "Reserva"], "Locanda de Gusti 102 Dalry Road Edinburgh"),
                P("🍛", "Mother India's Cafe",
                  "Curry indiano em porções de tapas, ótimo custo-benefício, vizinho do Royal Oak. Jantar antes do folk.",
                  "Todos os dias a partir das 12h · <b>£–££</b>",
                  ["Barato", "Reserva"], "Mother India's Cafe 3-5 Infirmary Street Edinburgh"),
                P("🌯", "Kebab Mahal",
                  "Instituição barata e sem frescura desde 1979, aberta até tarde. O jantar rápido depois de um show "
                  "na Cowgate.",
                  "Todos os dias 12h–~0h · <b>£</b>",
                  ["Barato"], "Kebab Mahal 7 Nicolson Square Edinburgh"),
                P("🥓", "Dishoom Edinburgh",
                  "Café bombaiense famoso pelo bacon naan roll. Bom para começar cedo: 9h aqui são 6h no Brasil, antes "
                  "das chamadas. A Dundas House fica ao lado.",
                  "Café da manhã seg–sex a partir das 8h · <b>££</b> · fila no jantar",
                  ["Pago", "Reserva"], "Dishoom 3a St Andrew Square Edinburgh"),
                P("🦞", "The Scran & Scallie",
                  "Gastropub do chef Tom Kitchin, com cozinha escocesa clássica e porções fartas. Perto da VoxBox: "
                  "junte com o garimpo de quarta.",
                  "Todos os dias, almoço e jantar (confira) · <b>££–£££</b>",
                  ["Pago", "Reserva"], "The Scran & Scallie 1 Comely Bank Road Edinburgh"),
            ],
        },
        {
            "nome": "Hidratar e recarregar",
            "descricao": "Água grátis, piscina vitoriana perto de casa, banho turco e caminhada à beira d'água.",
            "pontos": [
                P("💧", "Top Up Tap da Rutland Place",
                  "Torneira pública de água potável da Scottish Water no seu caminho para o centro. Há outras na "
                  "Grassmarket, na Royal Mile, nos Meadows e no Parlamento; o app Refill mostra mais.",
                  "24 h · <b>grátis</b>",
                  ["Grátis"], "Rutland Place Edinburgh"),
                P("🏊", "Dalry Swim Centre",
                  "Piscina vitoriana de 1895, restaurada, com sauna, a 19 minutos de casa. Para recarregar entre uma "
                  "chamada e outra. Só aceita cartão.",
                  "Seg 7h–21h, sauna até 20h (confira) · <b>~£6–7</b> (confira)",
                  ["Pago", "Barato"], "Dalry Swim Centre 25 Caledonian Crescent Edinburgh"),
                P("♨", "Portobello Turkish Baths",
                  "Banho turco vitoriano à beira-mar: sala quente, sauna e piscina de imersão. Reserve com até 7 dias; "
                  "não há reembolso.",
                  "Sessões: confira · <b>£9,60</b> por 1h45 · ~35 min de ônibus",
                  ["Pago", "Reserva"], "Portobello Swim Centre 57 Promenade Edinburgh"),
                P("🌳", "Harrison Park e Union Canal",
                  "Parque e trilha do canal quase na porta de casa, planos e iluminados. Caminhada de 30 minutos antes "
                  "das 16h30, ou ida a pé a Fountainbridge pela beira d'água.",
                  "Todos os dias · <b>grátis</b>",
                  ["Grátis"], "Harrison Park Edinburgh"),
                P("🏞", "Water of Leith em Slateford",
                  "Trilha arborizada à beira do rio, passando sob o aqueduto do canal. A caminhada mais bonita perto "
                  "de casa.",
                  "Com luz, ~7h20–16h30 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Slateford Aqueduct Edinburgh"),
                P("🍵", "PekoeTea",
                  "Casa de chás escocesa com degustação em Leith Walk, para um fim de tarde mais leve que o café.",
                  "Qua–sáb 11h–17h · fecha dom a ter · <b>£</b>",
                  ["Barato", "Fecha cedo"], "PekoeTea 11 Leith Walk Edinburgh"),
            ],
        },
        {
            "nome": "Futebol",
            "descricao": "O Tynecastle fica a 11 minutos a pé da casa.",
            "pontos": [
                P("⚽", "Hearts x Falkirk",
                  "Jogo da primeira divisão num dos estádios mais barulhentos do Reino Unido, a 11 minutos da casa, se "
                  "você voltar no domingo. Ingressos vão primeiro para sócios; fuja de revendedor não oficial.",
                  "<b>Dom 08/11 15h</b> (confira: data e hora mudam por TV) · ingresso: confira",
                  ["Show", "Pago", "Reserva"], "Tynecastle Park Gorgie Road Edinburgh"),
                P("🏟", "Tour do Tynecastle e museu do Hearts",
                  "Cerca de 90 minutos pelo estádio, saindo do museu do clube. Pauta sobre torcida e identidade, com "
                  "paralelos com o Vila Nova.",
                  "Datas de novembro: confira · <b>~£12</b> (preço antigo)",
                  ["Pago", "Reserva"], "Heart of Midlothian Museum Wheatfield Street Edinburgh"),
                P("🕰", "Memorial do Hearts em Haymarket",
                  "Relógio em homenagem aos jogadores do Hearts que se alistaram juntos no McCrae's Battalion em 1914. "
                  "Futebol e guerra numa história que pouca gente conhece.",
                  "24 h · <b>grátis</b>",
                  ["Grátis"], "Heart of Midlothian War Memorial Haymarket Edinburgh"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# Inverness (qui 05 à tarde a sáb 07/11 de manhã; sexta 06 é o único dia inteiro)
# ---------------------------------------------------------------------------
PARA_VOCE["inverness"] = {
    "intro": (
        "Inverness é pequena e dá para fazer tudo a pé. Sexta, 06/11, é o único dia inteiro: trabalhe de manhã, use "
        "a luz até 16h20 para história e canal, e deixe a noite para música e whisky. Quinta à noite tem a Bonfire "
        "Night no Bught Park."
    ),
    "secoes": [
        {
            "nome": "Trabalhar",
            "descricao": "A poucos minutos da casa. Reunião às 9h de Brasília cai ao meio-dia aqui.",
            "pontos": [
                P("💻", "Inverness Creative Academy",
                  "Escola vitoriana que virou polo criativo, com hot desk e café no térreo. A melhor base para um dia "
                  "inteiro de trabalho na sexta, praticamente na sua rua.",
                  "Seg–sex 9h–17h: meia diária na qui 05 e diária na sex 06 · <b>£15</b> o dia, <b>£10</b> por 4 h · "
                  "reserva online",
                  ["Pago", "Reserva", "Wi-fi"], "Inverness Creative Academy Midmills Building Stephens Street Inverness"),
                P("📚", "Inverness Library",
                  "Biblioteca pública ao lado da rodoviária, com internet e computadores grátis, e a rede Ness WiFi "
                  "cobre o centro. Boa para escrever em silêncio; não serve para chamada.",
                  "Qui 05 9h–19h · sex 06 9h–18h30 · sáb 07 9h–17h · <b>grátis</b>",
                  ["Grátis", "Wi-fi"], "Inverness Library Farraline Park Inverness"),
                P("🎭", "Eden Court Café Bar",
                  "Café-bar espaçoso do centro cultural, à beira do rio, com wi-fi. Emende a tarde de trabalho com o "
                  "Confluence às 18h45, no mesmo prédio.",
                  "Seg–sáb 9h30–23h (confira) · consumo no café",
                  ["Wi-fi"], "Eden Court Café Bar Bishops Road Inverness"),
            ],
        },
        {
            "nome": "Economia e história",
            "descricao": "Um banco que quebrou, a grande obra pública de Telford e o arquivo das Highlands.",
            "pontos": [
                P("🏦", "The Caledonian (antigo Caledonian Bank)",
                  "Sede de 1847 do Caledonian Bank, banco emissor fundado em Inverness em 1838, abalado pela quebra do "
                  "City of Glasgow Bank em 1878 e absorvido pelo Bank of Scotland em 1907. Hoje é pub: uma cerveja "
                  "dentro de uma crise bancária, ótimo para o podcast.",
                  "Fachada a qualquer hora · pub (confira horário)",
                  ["Grátis"], "The Caledonian 9 High Street Inverness"),
                P("⚓", "Caledonian Canal: Muirtown e Clachnaharry",
                  "A grande obra pública de Thomas Telford, pensada para gerar emprego e segurar a emigração das "
                  "Highlands: um caso clássico de infraestrutura estatal com retorno discutível. Escadaria de eclusas "
                  "de Muirtown (1809) e eclusa do mar de Clachnaharry (1807).",
                  "Com luz, até ~16h20 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Clachnaharry Sea Lock Inverness"),
                P("🗄", "Highland Archive Centre",
                  "O arquivo oficial das Highlands, com papéis de propriedades, comércio e famílias. Peça material "
                  "sobre as Clearances e a economia local; avise antes para separarem os documentos (01463 256444).",
                  "<b>Sex 06</b> 10h–16h30 · fecha qua, sáb e dom · <b>grátis</b>",
                  ["Grátis", "Reserva", "Fecha cedo"], "Highland Archive Centre Bught Road Inverness"),
                P("🏛", "Inverness Town House",
                  "Prefeitura neogótica de 1882 que, em 1921, recebeu a primeira reunião do gabinete britânico fora de "
                  "Londres, com Lloyd George discutindo a questão irlandesa.",
                  "Por fora, a qualquer hora · <b>grátis</b>",
                  ["Grátis"], "Inverness Town House High Street"),
            ],
        },
        {
            "nome": "Música",
            "descricao": "O que está confirmado nas suas datas, e onde caçar sessões de trad e vinil.",
            "pontos": [
                P("🎻", "Confluence no Eden Court",
                  "Espetáculo dos 50 anos do Eden Court: você percorre o prédio, bastidores incluídos, com cinco cenas "
                  "ao vivo de música, dança, teatro e gaélico. Quinta coincide com a Bonfire Night: prefira sexta.",
                  "Qui 05 e <b>sex 06 18h45</b> · 1h35 sem intervalo · preço: confira (01463 234234)",
                  ["Show", "Pago", "Reserva"], "Eden Court Theatre Bishops Road Inverness"),
                P("🎬", "George Michael: The Faith Tour",
                  "Filme-concerto da turnê Faith, gravado em Paris em 1988, em tela grande no Eden Court. Pauta para o "
                  "blog sobre os discos de 1987 e 1988.",
                  "Em cartaz de 06 a 08/11 · horários: confira",
                  ["Show", "Pago"], "Eden Court Cinema Inverness"),
                P("🎶", "MacGregor's Bar",
                  "O bar de Bruce MacGregor, rabequista do Blazin' Fiddles, dedicado a sessões de fiddle e a whisky. "
                  "O lugar para ouvir trad de verdade em Inverness.",
                  "Sessões à noite: dias de novembro, confira",
                  ["Show"], "MacGregor's Bar 109 Academy Street Inverness"),
                P("🍀", "Johnny Foxes",
                  "Pub irlandês grande e animado, com música ao vivo quase toda noite. Plano para depois do jantar de "
                  "sexta.",
                  "Música à noite, por volta das 22h30 (confira) · entrada <b>grátis</b>",
                  ["Show", "Grátis"], "Johnny Foxes 26 Bank Street Inverness"),
                P("🎤", "The Market Bar",
                  "Bar minúsculo no andar de cima, famoso pelo \"menor palco do mundo\", com músicos locais. Clássico "
                  "de Inverness para o blog.",
                  "Música qui a sáb à noite (confira) · <b>grátis</b>",
                  ["Show", "Grátis"], "The Market Bar 32 Church Street Inverness"),
                P("💿", "Union Vinyl",
                  "A loja independente de vinil da cidade, nos degraus da Market Brae, colada à hospedagem. O dono pôs "
                  "o negócio à venda em 2025: confirme se ainda abre.",
                  "Horário: confira",
                  ["Pago"], "Union Vinyl Market Brae Steps Inverness"),
            ],
        },
        {
            "nome": "Beber",
            "descricao": "Whisky, cerveja da cidade e pubs com história, além dos que estão na aba Highlands.",
            "pontos": [
                P("🥃", "The Malt Room",
                  "Whisky bar pequeno e especializado na Church Street, com centenas de maltes. Peça um voo de single "
                  "malts das Highlands.",
                  "À noite (confira horário)",
                  ["Pago"], "The Malt Room 34 Church Street Inverness"),
                P("🍺", "Uile-bheist",
                  "A primeira destilaria de Inverness em décadas, que também é cervejaria, com taproom ao lado das "
                  "tinas, na beira do rio. Caso de empreendedorismo local para o LinkedIn.",
                  "Taproom 12h–23h · tour a partir de <b>£30</b> (confira)",
                  ["Pago", "Reserva"], "Uile-bheist Distillery Ness Bank Inverness"),
                P("🍻", "The Phoenix Ale House",
                  "Pub tradicional com balcão de 1894 e três cask ales rotativas, ao lado do MacGregor's.",
                  "Horário: confira",
                  ["Pago"], "Phoenix Ale House 108 Academy Street Inverness"),
                P("⛵", "Clachnaharry Inn",
                  "Pub antigo na margem do canal: fecha a caminhada até a eclusa do mar com uma pint e comida de pub.",
                  "Qui 05 12h–22h · sex 06 12h–23h (confira)",
                  ["Pago"], "Clachnaharry Inn Inverness"),
                P("🌾", "Black Isle Brewery",
                  "Cervejaria orgânica que abastece o Black Isle Bar, com loja e tour na fazenda, em Munlochy. Só vale "
                  "de carro ou táxi.",
                  "Loja e tours ~10h–17h, inverno: confira (01463 811871)",
                  ["Pago", "Fecha cedo"], "Black Isle Brewery Munlochy"),
            ],
        },
        {
            "nome": "Comer bem",
            "descricao": "Café da manhã escocês, frutos do mar e produto das Highlands, fora da lista da aba Highlands.",
            "pontos": [
                P("🍳", "Rendezvous Cafe",
                  "Um dos full Scottish breakfasts mais citados da cidade, com black pudding e tattie scone. "
                  "Abasteça antes do dia de trabalho na sexta.",
                  "Café da manhã (confira horário) · <b>£</b>",
                  ["Barato"], "Rendezvous Cafe 14a Church Street Inverness"),
                P("🦌", "Café One",
                  "Bistrô de produto das Highlands (cordeiro, caça e peixe do dia) e um dos melhores custo-benefício "
                  "da cidade, com menu early bird.",
                  "Almoço e jantar a partir de 17h30 (confira) · <b>£26–40</b>",
                  ["Pago", "Reserva"], "Cafe One 75 Castle Street Inverness"),
                P("🦞", "River House",
                  "O especial da viagem: frutos do mar escoceses ao pé da ponte suspensa da Greig Street, à beira do "
                  "Ness. Reserva quase obrigatória.",
                  "Ter–sáb a partir das 15h: jantar qui 05 ou sex 06 (confira) · <b>£££</b>",
                  ["Pago", "Reserva"], "River House 1 Greig Street Inverness"),
                P("🏰", "The Kitchen Brasserie",
                  "Três andares de vidro de frente para o rio e o castelo, com cozinha honesta e bom preço.",
                  "Qui e sex 12h–21h (confira) · <b>££</b>",
                  ["Pago"], "The Kitchen Brasserie 15 Huntly Street Inverness"),
            ],
        },
        {
            "nome": "Hidratar e recarregar",
            "descricao": "Água grátis, sauna e trilhas curtas para sair da tela.",
            "pontos": [
                P("💧", "Top Up Tap da Ness Walk",
                  "Bebedouro azul da Scottish Water na margem do rio, perto da catedral. Encha a garrafa a caminho do "
                  "Eden Court; há outro na High Street.",
                  "24 h · <b>grátis</b> · ponto exato: confira no mapa da Scottish Water",
                  ["Grátis"], "Scottish Water Top up Tap Ness Walk Inverness"),
                P("🥗", "Roots Cafe",
                  "Café vegetariano a 2 minutos da porta, da antiga equipe do Velocity. Participa do esquema de "
                  "recarga: enchem sua garrafa de graça.",
                  "Seg–qui 9h–15h30 · sex 9h–16h e 17h30–21h · sáb 9h–16h (confira) · <b>£</b>",
                  ["Barato"], "Roots Cafe 1 Crown Avenue Inverness"),
                P("🧖", "Inverness Leisure",
                  "Sauna, vapor e spa para descomprimir depois de um dia de chamadas, ou nado na piscina olímpica.",
                  "Piscina olímpica seg–sex 6h–22h · Health Suite <b>£12,20</b>, piscina <b>£9,10</b>",
                  ["Pago"], "Inverness Leisure Bught Lane Inverness"),
                P("🌲", "Craig Phadrig",
                  "Colina com floresta, forte da Idade do Ferro e vista para o Beauly Firth. Trilha de 1,9 km "
                  "(~45 min), com trechos íngremes e lama.",
                  "Com luz, até ~16h20 · <b>grátis</b> · ônibus da Church Street",
                  ["Grátis", "Fecha cedo"], "Craig Phadrig car park Leachkin Brae Inverness"),
                P("🚶", "Trilha do Caledonian Canal",
                  "Caminho plano na margem do canal, da ponte giratória de Tomnahurich até a eclusa do mar, com chance "
                  "de ver focas. Cerca de 2 horas ida e volta.",
                  "Com luz, até ~16h20 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Tomnahurich Swing Bridge Inverness"),
            ],
        },
        {
            "nome": "Futebol",
            "descricao": "O Inverness Caledonian Thistle não tem jogo listado entre 05 e 07/11.",
            "pontos": [
                P("⚽", "Caledonian Stadium",
                  "Casa do Inverness Caledonian Thistle, na beira do Moray Firth, sob a ponte de Kessock. O último jogo "
                  "em casa listado é 03/11, antes da sua chegada: vale a foto e a loja do clube para comparar com o "
                  "Vila Nova.",
                  "Sem jogo nas datas (confira em ictfc.com) · loja: confira",
                  ["Grátis"], "Caledonian Stadium Stadium Road Inverness"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# Dalgety Bay e Fife (sáb 07 à tarde a seg 09/11 de manhã; domingo 08 é Remembrance Sunday)
# ---------------------------------------------------------------------------
PARA_VOCE["dalgety"] = {
    "intro": (
        "Fife é a terra de Adam Smith e de Andrew Carnegie: em Kirkcaldy você pisa onde A Riqueza das Nações foi "
        "terminada, e em Dunfermline nasceu o maior filantropo industrial da história. Domingo 08 é Remembrance "
        "Sunday: cerimônias nos memoriais por volta das 10h30–11h, museus abrindo ao meio-dia."
    ),
    "alerta": (
        "Fechados ou sem programação: The Albert Hotel (North Queensferry) fechou em 2017, o Harbour Bar de "
        "Kirkcaldy só reabre em 2027, e nem o Raith Rovers nem o Dunfermline jogam em casa de 07 a 09/11 (o dérbi "
        "dos dois é na sexta 06)."
    ),
    "secoes": [
        {
            "nome": "Trabalhar",
            "descricao": "Para o domingo à tarde e a segunda de manhã, antes do trem para York. A biblioteca de "
                         "Dalgety Bay só abre de terça a sábado.",
            "pontos": [
                P("📚", "Dunfermline Carnegie Library & Galleries",
                  "A primeira biblioteca pública que Carnegie doou no mundo: você trabalha dentro da história da "
                  "filantropia. Chamadas no Granary Café, de frente para a abadia, de fone.",
                  "Dom 08 12h–16h · seg 09 10h–17h · <b>grátis</b> · trem com troca em Inverkeithing",
                  ["Grátis", "Wi-fi", "Fecha cedo"], "Dunfermline Carnegie Library & Galleries, Abbot Street"),
                P("🖼", "Kirkcaldy Galleries",
                  "Biblioteca, museu e café no mesmo prédio, a 2 minutos da estação de Kirkcaldy. Junta trabalho com "
                  "as salas sobre Adam Smith e o linóleo.",
                  "Dom 08 12h–16h · seg 09 10h–17h · <b>grátis</b> (confira) · ~20–25 min de trem",
                  ["Grátis", "Wi-fi", "Fecha cedo"], "Kirkcaldy Galleries, War Memorial Gardens"),
                P("🏢", "HQ Edinburgh (Coates Crescent)",
                  "Coworking com diária a 7 minutos a pé de Haymarket, no caminho entre Fife e Waverley. Segunda de "
                  "manhã com sala fechada para chamada, e depois o trem para York.",
                  "Seg–sex 8h30–17h30 · reserva online por dia · preço: confira",
                  ["Pago", "Reserva", "Wi-fi", "Chamada ok"], "HQ Coates Crescent Edinburgh"),
                P("☕", "Café Wynd",
                  "Café independente no Heritage Quarter de Dunfermline, com gente trabalhando de notebook. Combina "
                  "com a biblioteca e o museu Carnegie.",
                  "Dias e horários: confira · 10 Cross Wynd",
                  ["Barato", "Wi-fi"], "Café Wynd Cross Wynd Dunfermline"),
                P("🥐", "Simply Local Cafe",
                  "O café mais perto da casa, familiar, com pães da Stephens Bakery e wi-fi. Para uma hora de e-mails, "
                  "não para chamada longa.",
                  "Horário: confira · Moray Way North",
                  ["Barato", "Wi-fi"], "Simply Local Cafe Moray Way North Dalgety Bay"),
            ],
        },
        {
            "nome": "Economia e história",
            "descricao": "De Dalgety Bay a Kirkcaldy são 20–25 minutos de trem, e lá tudo cabe num raio de 1 km a pé.",
            "pontos": [
                P("📜", "Placa de Adam Smith na High Street",
                  "No 220 da High Street ficava a casa da mãe de Smith, onde ele morou de 1767 a 1776 e terminou A "
                  "Riqueza das Nações. Procure a placa de 1953 na coluna da entrada e as pedras gravadas no calçamento.",
                  "A qualquer hora, melhor com luz · <b>grátis</b> · 10 min a pé da estação de Kirkcaldy",
                  ["Grátis"], "220 High Street Kirkcaldy Adam Smith plaque"),
                P("🚶", "Adam Smith Close",
                  "A antiga Halkett's Close, colada ao terreno da casa, desce da High Street até a orla: o caminho "
                  "de Smith até o mar. Boa foto para o seu conteúdo.",
                  "A qualquer hora · <b>grátis</b>",
                  ["Grátis"], "Adam Smith Close Kirkcaldy"),
                P("⛪", "Kirkcaldy Old Kirk",
                  "A igreja onde Adam Smith foi batizado, em 5/6/1723. Por dentro só com agendamento; o cemitério e "
                  "a torre se veem por fora.",
                  "Dom 08 culto de manhã · interior com agendamento (01592 265499)",
                  ["Grátis"], "Old Kirk Kirkcaldy Kirk Wynd"),
                P("🏛", "Kirkcaldy Galleries: Moments in Time",
                  "Mostra que vai da Idade do Bronze à publicação de A Riqueza das Nações, com um andar dedicado ao "
                  "linóleo dos Nairn, a indústria da cidade desde 1847. O Adam Smith Theatre fica ao lado.",
                  "Dom 08 12h–16h · seg 09 10h–17h · <b>grátis</b> (confira)",
                  ["Grátis", "Fecha cedo"], "Kirkcaldy Galleries"),
                P("🏭", "Andrew Carnegie Birthplace Museum",
                  "O chalé de tecelão onde nasceu o dono da maior fortuna industrial do século 19, que depois doou "
                  "quase tudo. O par perfeito de Smith: mercado, capital e filantropia.",
                  "Todos os dias 11h–16h, última entrada 15h20 · <b>grátis</b> (doação)",
                  ["Grátis", "Fecha cedo"], "Andrew Carnegie Birthplace Museum Moodie Street Dunfermline"),
            ],
        },
        {
            "nome": "Música",
            "descricao": "Dois shows no fim de semana e a peregrinação a Big Country, Skids e Nazareth em Dunfermline.",
            "pontos": [
                P("🎤", "Alabama 3 acústico no PJ Molloys",
                  "A banda do tema de Os Sopranos num pub de 300 lugares em Dunfermline, domingo à noite: matéria "
                  "pronta para o Substack. Para voltar, táxi (~15 min): trem de domingo à noite é raro.",
                  "<b>Dom 08/11 19h</b> · a partir de <b>£27,50</b> (há listagem dizendo esgotado: confira)",
                  ["Show", "Pago", "Reserva"], "PJ Molloys Canmore Street Dunfermline"),
                P("🎸", "Ian Prowse & Amsterdam no Cabaret Voltaire",
                  "Rock com banda de seis músicos numa casa clássica da Cowgate, em Edimburgo, na noite da sua "
                  "chegada a Fife. São 30 minutos de trem; fique de olho no último trem de volta.",
                  "<b>Sáb 07/11 19h30</b> · a partir de <b>~£25</b> (confira)",
                  ["Show", "Pago", "Reserva"], "Cabaret Voltaire Blair Street Edinburgh"),
                P("🪑", "Banco de Stuart Adamson",
                  "Banco pago pelos fãs em 2011, com versos de In a Big Country, no Pittencrieff Park. Ele olha para "
                  "o Glen Pavilion, onde os Skids fizeram o segundo show e o Big Country estreou.",
                  "Parque aberto, com luz até ~16h20 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Glen Pavilion Pittencrieff Park Dunfermline"),
                P("🎭", "Alhambra Theatre",
                  "O palco de Dunfermline ligado ao Nazareth, formado na cidade em 1968, e às homenagens ao vocalista "
                  "Dan McCafferty. Vale a foto da fachada.",
                  "Fachada a qualquer hora · <b>grátis</b>",
                  ["Grátis"], "Alhambra Theatre Dunfermline"),
            ],
        },
        {
            "nome": "Beber",
            "descricao": "Um pub dentro de um banco, o uísque que nasceu num livro de impostos e uma estalagem antiga.",
            "pontos": [
                P("🏦", "The Robert Nairn",
                  "Wetherspoon num prédio do antigo Trustee Savings Bank, em terreno doado por Robert Nairn, o do "
                  "linóleo: banco e indústria num copo só. Barato, a 2 minutos do Old Kirk.",
                  "Todos os dias a partir das 8h, até ~meia-noite (confira dom) · <b>£</b>",
                  ["Barato"], "The Robert Nairn Kirk Wynd Kirkcaldy"),
                P("🥃", "Lindores Abbey Distillery",
                  "Num registro do Tesouro de 1494, a primeira menção escrita ao scotch: o frei John Cor, desta abadia, "
                  "recebe malte para fazer aqua vitae. Para um economista, a origem fiscal do uísque. Só de carro.",
                  "Nov–fev de quarta a domingo · dom 08 tours às 10h, 12h30 e 14h30 · preço: confira · ~50 min de carro",
                  ["Pago", "Reserva"], "Lindores Abbey Distillery Newburgh"),
                P("🍺", "Aberdour Hotel",
                  "Antiga estalagem de diligências com real ale no bar, a 2 minutos da estação de Aberdour, uma parada "
                  "depois de Dalgety Bay. Também serve Sunday lunch: plano B do assado de domingo.",
                  "Dom 11h–22h30 (confira cozinha)",
                  ["Pago"], "Aberdour Hotel High Street Aberdour"),
            ],
        },
        {
            "nome": "Comer bem",
            "descricao": "Assado de domingo perto de casa, fish and chips de verdade e um jantar especial no sábado.",
            "pontos": [
                P("🍖", "The Compass",
                  "O Sunday roast de 08/11 a uns 200 m da estação de Dalgety Bay: dá para voltar de Kirkcaldy direto "
                  "para a mesa. O imóvel apareceu para alugar em 2026: confirme que está aberto e reserve.",
                  "Dom 08 a partir das 12h (confira) · reserva pelo site da Belhaven",
                  ["Pago", "Reserva"], "The Compass Harbour Drive Dalgety Bay"),
                P("🍽", "The Wee Restaurant",
                  "Bistrô de 40 lugares com Michelin Plate, aos pés da Forth Bridge. O jantar de sábado: fecha domingo "
                  "e segunda.",
                  "<b>Sáb 07</b> jantar a partir das 17h45, últimos pedidos 20h30 · <b>£££</b> · reserve: 01383 616263",
                  ["Pago", "Reserva"], "The Wee Restaurant Main Street North Queensferry"),
                P("🐟", "Dalgety Fish Bar",
                  "A peixaria do bairro, bem avaliada e perto da casa: o fish and chips para levar no sábado à noite.",
                  "Horário: confira · 9 Moray Way North",
                  ["Barato"], "Dalgety Fish Bar Moray Way North Dalgety Bay"),
                P("🍟", "Valente's",
                  "Família italiana fritando peixe em Kirkcaldy desde 1921: um caso de pequena empresa centenária. "
                  "Peça para levar e coma de frente para o mar.",
                  "Horário de dom e seg: confira (01592 651991) · <b>£</b>",
                  ["Barato"], "Valente's Overton Road Kirkcaldy"),
            ],
        },
        {
            "nome": "Hidratar e recarregar",
            "descricao": "Sauna de domingo, água grátis em Dunfermline e uma caminhada saindo da porta de casa.",
            "pontos": [
                P("🧖", "Carnegie Leisure Centre",
                  "Sauna, vapor e laconium para o domingo frio; a Health Suite costuma incluir natação, conforme a "
                  "disponibilidade.",
                  "Dom 08 sauna 9h15–16h30, piscina 8h–17h (confira) · <b>~£5–7,50</b> (confira)",
                  ["Pago", "Fecha cedo"], "Carnegie Leisure Centre Dunfermline"),
                P("🚰", "Top Up Tap de Dunfermline",
                  "Torneira pública da Scottish Water na High Street, para encher a garrafa entre o museu Carnegie e "
                  "a biblioteca. Não há torneira dessas em Dalgety Bay.",
                  "24 h · <b>grátis</b> · ponto exato: confira no mapa da Scottish Water",
                  ["Grátis"], "Top Up Tap High Street Dunfermline"),
                P("🌊", "St Bridget's Kirk",
                  "Ruína medieval na beira do Forth, a uns 2 km da casa: caminhada de manhã cedo antes de trabalhar ou "
                  "da chamada com o Brasil.",
                  "Com luz, 7h30–16h20 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "St Bridget's Kirk Dalgety Bay"),
            ],
        },
        {
            "nome": "Futebol",
            "descricao": "Os clubes de Fife não jogam em casa nessas datas; o Hearts pode jogar no domingo em Edimburgo.",
            "pontos": [
                P("⚽", "Hearts x Falkirk",
                  "O único jogo grande por perto: domingo à tarde, 30 minutos de trem até Haymarket e uma caminhada "
                  "curta até Gorgie. A data vem de agregador: confirme na SPFL.",
                  "<b>Dom 08/11 15h</b> (confira) · ingresso: confira",
                  ["Show", "Pago", "Reserva"], "Tynecastle Park Edinburgh"),
                P("🏟", "Stark's Park (Raith Rovers)",
                  "O clube de Kirkcaldy, que tem Gordon Brown, ex-ministro das Finanças, como torcedor famoso, e "
                  "ganhou a Copa da Liga de 1994. Nas suas datas, só a foto de fora.",
                  "Sem jogo de 07 a 09/11 · <b>grátis</b>",
                  ["Grátis"], "Stark's Park Kirkcaldy"),
                P("🎨", "East End Park (Dunfermline Athletic)",
                  "O estádio do Dunfermline, onde foi pintado em 2009 um mural de Stuart Adamson, torcedor do clube: "
                  "futebol e rock numa foto só.",
                  "Sem jogo de 07 a 09/11 · <b>grátis</b> · confira se o mural ainda existe",
                  ["Grátis"], "East End Park Dunfermline"),
            ],
        },
    ],
}

# ---------------------------------------------------------------------------
# York (seg 09 à tarde a qua 11/11 de manhã; terça 10 é o único dia inteiro)
# ---------------------------------------------------------------------------
PARA_VOCE["york"] = {
    "intro": (
        "Em York: guildas, George Hudson e a filantropia quaker dos Rowntree, vinil, pubs de cerveja real e lugares "
        "com wi-fi a poucos minutos da Grape Lane. Lembre: 14h em York são 11h em Brasília."
    ),
    "alerta": (
        "Fechados nas suas datas: Mansion House (só de quarta a sábado, a partir das 10h30), Merchant Taylors' Hall "
        "e o Le Cochon Aveugle, que fechou. A Track Records e as livrarias Ken Spelman e Fossgate Books também "
        "fecharam."
    ),
    "secoes": [
        {
            "nome": "Trabalhar",
            "descricao": "A poucos minutos da Grape Lane, para abrir o notebook e, se precisar, fazer chamada.",
            "pontos": [
                P("📚", "York Explore Library",
                  "Biblioteca central com wi-fi grátis e área de estudo no 1º andar, com reserva de mesa. Para chamada, "
                  "desça para o Reading Café, no térreo (seg–qui 9h–16h), ou peça uma sala.",
                  "Seg 09 a qua 11: 9h–20h · <b>grátis</b>",
                  ["Grátis", "Wi-fi", "Tomadas"], "York Explore Library Museum Street York"),
                P("🏛", "The Guildhall (coworking)",
                  "Coworking dentro do Guildhall medieval, à beira do Ouse, com mesa avulsa e chá e café grátis. Para "
                  "uma tarde inteira de chamadas na terça.",
                  "Seg–sex · diária sob consulta (guildhall@york.ac.uk, 01904 435110)",
                  ["Pago", "Reserva", "Wi-fi", "Tomadas", "Chamada ok"], "The Guildhall York St Martins Courtyard Coney Street"),
                P("💻", "SPARK Studios",
                  "Coworking no complexo de contêineres Spark:York, na Piccadilly, com sala de reunião para chamada. A "
                  "diária mais barata que achamos.",
                  "Seg–sex 8h30–19h · <b>£10 + VAT</b> por dia (confira) · reserve por contato",
                  ["Pago", "Barato", "Reserva", "Wi-fi", "Chamada ok"], "Spark York 17-21 Piccadilly York"),
                P("🏰", "Gatehouse Coffee",
                  "Café de voluntários dentro do portão medieval de Walmgate Bar, com mesas, tomadas e wi-fi no salão "
                  "de cima. Trabalhar dentro da muralha rende boa foto.",
                  "Ter 10 ~10h–16h · seg pode fechar (confira) · <b>£</b>",
                  ["Barato", "Wi-fi", "Tomadas"], "Gatehouse Coffee Walmgate Bar York"),
            ],
        },
        {
            "nome": "Economia e história",
            "descricao": "Guildas, ferrovias e chocolate quaker, com livrarias de usados para fechar o dia.",
            "pontos": [
                P("⚖", "Merchant Adventurers' Hall",
                  "Salão de guilda do século 14, onde mercadores regulavam o comércio de lã e tecido: uma aula viva "
                  "de cartel, crédito e caridade corporativa. Rende post de história econômica.",
                  "Seg 09 e ter 10: 10h–16h · <b>£7,50</b>",
                  ["Pago"], "Merchant Adventurers' Hall Fossgate York"),
                P("🚂", "Trilha de George Hudson",
                  "O \"Railway King\" e a bolha ferroviária dos anos 1840 em 20 minutos: placa na 1 College Street, "
                  "onde ele foi aprendiz de tecelão, a Hudson House (44 Monkgate), onde morou, e a George Hudson "
                  "Street, a caminho da estação.",
                  "Com luz, até ~16h15 · <b>grátis</b>",
                  ["Grátis"], "1 College Street York George Hudson plaque"),
                P("🍫", "Onde nasceu Joseph Rowntree",
                  "Placa no lugar da mercearia quaker onde Joseph Rowntree nasceu, em 1836, no 10 Pavement. Ponto de "
                  "partida para falar de capitalismo quaker e filantropia.",
                  "A qualquer hora · <b>grátis</b>",
                  ["Grátis"], "10 Pavement York Rowntree plaque"),
                P("🏭", "York Cocoa Works",
                  "Fábrica artesanal de chocolate com tour e degustação. Bom contraste com a escala industrial da "
                  "Rowntree's e da Terry's para pensar a cadeia do cacau.",
                  "Todos os dias ~9h30–17h (confira) · tour a partir de <b>£12,50</b>",
                  ["Pago", "Reserva"], "York Cocoa Works 10 Castlegate York"),
                P("📖", "Lucius Books",
                  "Livraria antiquária de quatro andares, aberta em maio de 2026 num prédio do século 15 restaurado. "
                  "Procure primeiras edições de economia e história.",
                  "Horário: confira",
                  ["Grátis"], "Lucius Books 70 Micklegate York"),
                P("📚", "Minster Gate Bookshop",
                  "Sebo de vários andares em frente ao Minster, para garimpar história britânica, mapas e gravuras "
                  "antigas de York.",
                  "Seg–sáb 10h–17h30 (confira)",
                  ["Grátis"], "Minster Gate Bookshop 8 Minster Gates York"),
            ],
        },
        {
            "nome": "Música",
            "descricao": "Nenhum show confirmado nas casas grandes em 09 e 10/11 (o folk club só se reúne às "
                         "quintas): o roteiro é de vinil e microfone aberto.",
            "pontos": [
                P("💿", "Earworm Records",
                  "Loja independente de vinil novo e usado num pátio escondido da Goodramgate, desde 2013. Pauta para "
                  "o Substack.",
                  "Seg ~10h–18h (confira ter)",
                  ["Grátis"], "Earworm Records Powells Yard Goodramgate York"),
                P("🎛", "Record Plant York",
                  "Discos, CDs, fitas e memorabilia, aberta em novembro de 2025, com uma homenagem à cena de York nos "
                  "anos 70 e 80.",
                  "Todos os dias 10h–18h (confira)",
                  ["Grátis"], "Record Plant 26 Gillygate York"),
                P("🔁", "Rebound",
                  "Discos de segunda mão a duas portas da Record Plant: garimpe as duas na mesma ida.",
                  "Horário: confira",
                  ["Grátis"], "Rebound 5 Gillygate York"),
                P("🎧", "FortyFive Vinyl Café",
                  "Café com discos à venda e sala de audição em Micklegate: ouça um disco com café e fotografe para "
                  "o blog.",
                  "Todos os dias 10h–17h (confira) · <b>£</b>",
                  ["Barato"], "FortyFive Vinyl Cafe 29 Micklegate York"),
                P("🎸", "Open mic no Sotano",
                  "Bar de porão na Little Stonegate com microfone aberto às terças: a cena local na noite do dia 10, "
                  "a 2 minutos da casa.",
                  "<b>Ter 10</b> a partir das 21h (dado de ~2023: confira) · <b>grátis</b>",
                  ["Show", "Grátis"], "Sotano Little Stonegate York"),
            ],
        },
        {
            "nome": "Beber",
            "descricao": "Real ale e cervejarias locais, mais um bar de gin, sem repetir os pubs da aba York.",
            "pontos": [
                P("🚉", "York Tap",
                  "Pub dentro da estação, num salão de 1906, com umas 14 torneiras e bombas manuais. Um brinde a "
                  "George Hudson sem sair dos trilhos.",
                  "Seg–qui ~12h–22h (confira)",
                  ["Pago"], "York Tap York Railway Station"),
                P("🍺", "The Golden Ball",
                  "Pub comunitário de Bishophill, no Good Beer Guide, com real ales locais que mudam sempre. Às "
                  "segundas costumava ter microfone aberto de folk e cantautores.",
                  "Seg–qui 16h–23h · open mic seg ~20h30 (dado antigo: confira)",
                  ["Pago", "Show"], "The Golden Ball 2 Cromwell Road York"),
                P("🪓", "House of the Trembling Madness",
                  "Loja de cerveja no térreo e bar medieval em cima, com vigas e caveiras. Cerveja belga e britânica "
                  "a 1 minuto da casa.",
                  "~10h–0h (confira)",
                  ["Pago"], "House of the Trembling Madness 48 Stonegate York"),
                P("🏭", "Brew York",
                  "Cervejaria artesanal à beira do Foss, com dezenas de torneiras. Para a noite de terça: segunda "
                  "provavelmente fecha.",
                  "Ter 10 12h–23h (confira)",
                  ["Pago"], "Brew York Beer Hall Walmgate York"),
                P("🍸", "Evil Eye Lounge",
                  "Bar de coquetéis com loja de gin em Stonegate e centenas de rótulos: a parada do gin.",
                  "Horário: confira",
                  ["Pago"], "Evil Eye Lounge 42 Stonegate York"),
            ],
        },
        {
            "nome": "Comer bem",
            "descricao": "Um especial à beira do Ouse, bom custo-benefício e cafés para a quarta antes do check-out.",
            "pontos": [
                P("⭐", "The Star Inn the City",
                  "Do chef Andrew Pern, numa antiga casa de máquinas à beira do Ouse, com cozinha de Yorkshire. O "
                  "jantar especial que abre segunda e terça.",
                  "Seg–qui ~11h–23h (confira) · <b>£££</b>",
                  ["Pago", "Reserva"], "Star Inn the City Museum Street York"),
                P("🍝", "Il Paradiso del Cibo",
                  "Cantina sarda pequena e barulhenta na Walmgate, com massa farta e preço honesto: o custo-benefício "
                  "da viagem.",
                  "Seg e ter, jantar a partir das 18h (confira almoço) · <b>££</b>",
                  ["Barato", "Reserva"], "Il Paradiso del Cibo 40 Walmgate York"),
                P("🥐", "Partisan",
                  "Café e restaurante numa casa georgiana de Micklegate, com brunch caprichado. Almoço de segunda ou "
                  "terça.",
                  "Seg ~9h–15h (confira) · <b>££</b>",
                  ["Pago"], "Partisan 112 Micklegate York"),
                P("🍳", "Bruks",
                  "Café de bairro que abre cedo, com bubble and squeak. Perfeito para a quarta, antes do silêncio das "
                  "11h e do check-out.",
                  "Todos os dias a partir das 8h (confira) · <b>£</b>",
                  ["Barato"], "Bruks 1 Peter Lane York"),
                P("⛪", "Bar Convent Café",
                  "Café do convento em atividade mais antigo da Inglaterra (1686), aberto às 8h. Café da manhã "
                  "tranquilo na quarta, a caminho da estação.",
                  "Seg–sáb 8h–15h30 · <b>£</b>",
                  ["Barato", "Fecha cedo"], "Bar Convent Cafe Blossom Street York"),
            ],
        },
        {
            "nome": "Hidratar e recarregar",
            "descricao": "Água grátis, a piscina que os Rowntree deram aos operários e uma caminhada à beira do Ouse.",
            "pontos": [
                P("💧", "App Refill",
                  "A prefeitura de York indica o app Refill para achar cafés e lojas que enchem a garrafa de graça. "
                  "Baixe antes de sair.",
                  "Todos os dias · <b>grátis</b>",
                  ["Grátis"], "Refill water York city centre"),
                P("🏊", "Yearsley Swimming Pool",
                  "Piscina coberta de 1909, com 45,7 m, doada pela Rowntree aos operários: nadar nela é história "
                  "econômica na prática. Reserve pelo app Better.",
                  "Seg 09 7h10–17h20 · ter 10 7h–17h20 · <b>£5,50</b>",
                  ["Pago", "Reserva", "Fecha cedo"], "Yearsley Swimming Pool Haleys Terrace York"),
                P("🌳", "Rowntree Park",
                  "Parque à beira do Ouse doado pela Rowntree em 1921 em memória dos funcionários mortos na Primeira "
                  "Guerra. Faz sentido na véspera do Armistício.",
                  "Durante o dia, com luz até ~16h15 · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Rowntree Park Terry Avenue York"),
                P("🚶", "Caminhada pelo Ouse",
                  "Pela New Walk até a Millennium Bridge, volta pela outra margem passando pelo Rowntree Park. "
                  "Esticando até a torre do relógio da antiga fábrica da Terry's, uns 3 km de ida.",
                  "Até ~16h · <b>grátis</b>",
                  ["Grátis", "Fecha cedo"], "Millennium Bridge York"),
            ],
        },
        {
            "nome": "Futebol",
            "descricao": "O York City não joga em casa nesses dias; a aposta é um jogo de copa em Bradford.",
            "pontos": [
                P("⚽", "Bradford City x York City",
                  "Jogo do EFL Trophy no Valley Parade, a cerca de 1 hora de trem via Leeds: programa de torcedor de "
                  "verdade. Confira a volta: o último trem para York pode ser cedo.",
                  "<b>Ter 10/11 19h30</b> (data de agregador: confira) · ingresso: confira",
                  ["Show", "Pago", "Reserva"], "Valley Parade Bradford"),
            ],
        },
    ],
}

COORD = {
    # Edimburgo
    "Fountainbridge Library": (55.94012, -3.21836),
    "Central Library": (55.94830, -3.19253),
    "National Library of Scotland": (55.94866, -3.19207),
    "The Melting Pot": (55.95311, -3.18665),
    "Spaces Lochrin Square": (55.94383, -3.20781),
    "Black Medicine Coffee": (55.94714, -3.18579),
    "Túmulo de Adam Smith": (55.95216, -3.17980),
    "Adam Smith's Panmure House": (55.95222, -3.17840),
    "Museum on the Mound": (55.95019, -3.19325),
    "Mausoléu de David Hume": (55.95347, -3.18601),
    "Dundas House (RBS)": (55.95450, -3.19104),
    "Topping & Company Booksellers": (55.95765, -3.18428),
    "Van Morrison no Usher Hall": (55.94726, -3.20493),
    "Sneaky Pete's": (55.94817, -3.19148),
    "The Queen's Hall": (55.94120, -3.18184),
    "The Royal Oak": (55.94807, -3.18620),
    "VoxBox Music": (55.95769, -3.20723),
    "BBC Scottish Symphony no Usher Hall": (55.94726, -3.20493),
    "The Athletic Arms": (55.93895, -3.22384),
    "The Caley Sample Room": (55.93769, -3.22582),
    "Cloisters Bar": (55.94327, -3.20188),
    "The Blue Blazer": (55.94595, -3.20318),
    "The Captain's Bar": (55.94701, -3.18651),
    "Locanda de Gusti": (55.94367, -3.21963),
    "Mother India's Cafe": (55.94810, -3.18600),
    "Kebab Mahal": (55.94616, -3.18598),
    "Dishoom Edinburgh": (55.95354, -3.19251),
    "The Scran & Scallie": (55.95914, -3.21457),
    "Top Up Tap da Rutland Place": (55.94998, -3.20732),
    "Dalry Swim Centre": (55.94234, -3.21768),
    "Portobello Turkish Baths": (55.95303, -3.10688),
    "Harrison Park e Union Canal": (55.93682, -3.22572),
    "Water of Leith em Slateford": (55.92349, -3.24934),
    "PekoeTea": (55.97020, -3.17178),
    "Hearts x Falkirk": (55.93902, -3.23227),
    "Tour do Tynecastle e museu do Hearts": (55.93902, -3.23227),
    "Memorial do Hearts em Haymarket": (55.94628, -3.21650),
    # Inverness
    "Inverness Creative Academy": (57.47787, -4.21763),
    "Inverness Library": (57.48110, -4.22468),
    "Eden Court Café Bar": (57.47307, -4.23082),
    "The Caledonian (antigo Caledonian Bank)": (57.47773, -4.22504),
    "Caledonian Canal: Muirtown e Clachnaharry": (57.49050, -4.26261),  # eclusa do mar
    "Highland Archive Centre": (57.46207, -4.23770),
    "Inverness Town House": (57.47724, -4.22486),
    "Confluence no Eden Court": (57.47307, -4.23082),
    "George Michael: The Faith Tour": (57.47307, -4.23082),
    "MacGregor's Bar": (57.48065, -4.22824),
    "Johnny Foxes": (57.47735, -4.22675),
    "The Market Bar": (57.47892, -4.22629),
    "Union Vinyl": (57.47790, -4.22252),
    "The Malt Room": (57.47888, -4.22644),
    "Uile-bheist": (57.47395, -4.22634),
    "The Phoenix Ale House": (57.48070, -4.22763),
    "Clachnaharry Inn": (57.48860, -4.25835),
    "Black Isle Brewery": (57.53257, -4.30272),
    "Rendezvous Cafe": (57.47802, -4.22578),
    "Café One": (57.47609, -4.22446),
    "River House": (57.47878, -4.23085),
    "The Kitchen Brasserie": (57.47742, -4.22904),
    "Top Up Tap da Ness Walk": (57.47460, -4.22870),  # aproximado
    "Roots Cafe": (57.47801, -4.21920),
    "Inverness Leisure": (57.46409, -4.23995),
    "Craig Phadrig": (57.47730, -4.26971),
    "Trilha do Caledonian Canal": (57.46481, -4.24424),  # ponte de Tomnahurich
    "Caledonian Stadium": (57.49471, -4.21697),
    # Fife
    "Dunfermline Carnegie Library & Galleries": (56.07027, -3.46198),
    "Kirkcaldy Galleries": (56.11221, -3.16613),
    "HQ Edinburgh (Coates Crescent)": (55.94870, -3.21236),
    "Café Wynd": (56.07174, -3.46161),
    "Simply Local Cafe": (56.04127, -3.34322),  # mesma galeria da Dalgety Fish Bar
    "Placa de Adam Smith na High Street": (56.11166, -3.15730),
    "Adam Smith Close": (56.11172, -3.15715),
    "Kirkcaldy Old Kirk": (56.11265, -3.15826),
    "Kirkcaldy Galleries: Moments in Time": (56.11221, -3.16613),
    "Andrew Carnegie Birthplace Museum": (56.06794, -3.46123),
    "Alabama 3 acústico no PJ Molloys": (56.07034, -3.45962),  # Canmore Street
    "Ian Prowse & Amsterdam no Cabaret Voltaire": (55.94891, -3.18725),
    "Banco de Stuart Adamson": (56.06916, -3.47043),  # Glen Pavilion
    "Alhambra Theatre": (56.06990, -3.45790),
    "The Robert Nairn": (56.11195, -3.15794),
    "Lindores Abbey Distillery": (56.35174, -3.22557),
    "Aberdour Hotel": (56.05353, -3.30265),
    "The Compass": (56.04065, -3.36627),
    "The Wee Restaurant": (56.00918, -3.39428),
    "Dalgety Fish Bar": (56.04127, -3.34322),
    "Valente's": (56.12652, -3.14386),
    "Carnegie Leisure Centre": (56.07418, -3.46055),
    "Top Up Tap de Dunfermline": (56.07150, -3.46050),  # aproximado, High Street
    "St Bridget's Kirk": (56.03981, -3.33446),
    "Stark's Park (Raith Rovers)": (56.09978, -3.16843),
    "East End Park (Dunfermline Athletic)": (56.07565, -3.44199),
    # York ("App Refill" fica sem coordenada: não é um lugar)
    "York Explore Library": (53.96143, -1.08607),
    "The Guildhall (coworking)": (53.95966, -1.08560),
    "SPARK Studios": (53.95675, -1.07755),
    "Gatehouse Coffee": (53.95524, -1.07084),
    "Trilha de George Hudson": (53.96219, -1.08020),  # College Street
    "Onde nasceu Joseph Rowntree": (53.95857, -1.07982),
    "York Cocoa Works": (53.95721, -1.08136),
    "Lucius Books": (53.95727, -1.08850),
    "Minster Gate Bookshop": (53.96157, -1.08224),
    "Earworm Records": (53.96141, -1.07952),
    "Record Plant York": (53.96355, -1.08461),
    "Rebound": (53.96319, -1.08538),
    "FortyFive Vinyl Café": (53.95719, -1.08639),
    "Open mic no Sotano": (53.96100, -1.08360),  # aproximado, Little Stonegate
    "York Tap": (53.95845, -1.09263),
    "The Golden Ball": (53.95487, -1.08502),
    "House of the Trembling Madness": (53.96120, -1.08295),
    "Brew York": (53.95766, -1.07617),
    "Evil Eye Lounge": (53.96110, -1.08313),
    "The Star Inn the City": (53.96052, -1.08734),
    "Il Paradiso del Cibo": (53.95711, -1.07639),
    "Partisan": (53.95667, -1.08997),
    "Bruks": (53.95848, -1.08216),
    "Bar Convent Café": (53.95531, -1.09118),
    "Yearsley Swimming Pool": (53.97585, -1.07549),
    "Rowntree Park": (53.94819, -1.08158),
    "Caminhada pelo Ouse": (53.94496, -1.08225),  # Millennium Bridge
    "Bradford City x York City": (53.80434, -1.75936),
}

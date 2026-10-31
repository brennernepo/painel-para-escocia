"""Coordenadas (lat, lon) dos lugares citados em dados.py, pelo nome exato do cartão.

Servem para a distância até a casa, a rota e os mapas das abas de cidade. Lugar sem coordenada aparece sem essas três coisas.
Conferidas em 31/10/2026 (sites oficiais, Wikipedia e OpenStreetMap).
"""

COORD = {
    # Edimburgo
    "Edinburgh Castle": (55.94869, -3.20042),
    "St Giles' Cathedral": (55.94948, -3.19085),
    "The Real Mary King's Close": (55.95023, -3.19056),
    "Camera Obscura": (55.94903, -3.19560),
    "Scotch Whisky Experience": (55.94874, -3.19587),
    "Writers' Museum": (55.94969, -3.19374),
    "Victoria Street": (55.94865, -3.19377),
    "Greyfriars Kirkyard": (55.94683, -3.19289),
    "The Elephant House": (55.94757, -3.19179),
    "National Museum of Scotland": (55.94707, -3.18934),
    "Sandy Bell's": (55.94608, -3.19129),
    "The Bow Bar": (55.94842, -3.19414),
    "Calton Hill": (55.95525, -3.18280),
    "Scottish National Gallery": (55.95089, -3.19561),
    "Scott Monument": (55.95236, -3.19326),
    "Johnnie Walker Princes Street": (55.95047, -3.20759),
    "Palace of Holyroodhouse": (55.95269, -3.17161),
    "Arthur's Seat": (55.94407, -3.16160),
    "Parlamento escocês": (55.95247, -3.17566),
    "Dynamic Earth": (55.95053, -3.17442),
    "Holyrood Distillery": (55.94304, -3.17763),
    "Dean Village": (55.95226, -3.21822),
    "Royal Botanic Garden": (55.96529, -3.20886),
    "Stockbridge": (55.96056, -3.21608),  # Raeburn Place
    "Royal Yacht Britannia": (55.98215, -3.17731),
    "Port of Leith Distillery": (55.98270, -3.17548),
    "The Fishmarket": (55.98171, -3.19482),
    "Lidl Slateford Road": (55.93123, -3.23538),
    "Union Canal": (55.93682, -3.22572),  # Harrison Park
    "Athletic Arms (The Diggers)": (55.93895, -3.22384),
    "Loudons": (55.94358, -3.20822),
    "Edinburgh Larder": (55.95010, -3.18601),
    "Oink": (55.94859, -3.19425),
    "Mosque Kitchen": (55.94504, -3.18536),
    "Bánh Mì Brothers": (55.94611, -3.20142),
    "Mary's Milk Bar": (55.94684, -3.19739),
    "Arcade Haggis & Whisky House": (55.95041, -3.18881),
    "Bennets Bar": (55.94174, -3.20321),
    "Teuchters": (55.94931, -3.21231),
    # Inverness e Highlands
    "Loch Ness e Urquhart Castle": (57.32411, -4.44199),
    "Cruzeiro no Loch Ness": (57.36447, -4.39191),
    "Culloden Battlefield": (57.47654, -4.10012),
    "Clava Cairns": (57.47306, -4.07369),
    "Fort George": (57.58381, -4.07029),
    "Black Isle e Chanonry Point": (57.57414, -4.09179),
    "Fort Augustus": (57.14470, -4.68316),
    "Glen Affric e Plodda Falls": (57.27236, -4.85960),
    "Aviemore e Cairngorms": (57.14798, -3.81946),
    "Eilean Donan": (57.27410, -5.51592),
    "Isle of Skye": (57.41305, -6.19445),
    "Inverness Castle": (57.47643, -4.22564),
    "Rio Ness e Ness Islands": (57.46403, -4.23053),
    "Leakey's Bookshop": (57.48028, -4.22867),
    "Inverness Museum and Art Gallery": (57.47705, -4.22552),
    "Botanic Gardens": (57.46233, -4.24026),
    "Victorian Market": (57.47893, -4.22519),
    "Música ao vivo": (57.47906, -4.22730),
    "Singleton of Glen Ord": (57.52259, -4.47405),
    "Dalwhinnie": (56.94024, -4.23897),
    "Tomatin": (57.33899, -4.00928),
    "Glenfiddich (Speyside)": (57.45511, -3.12874),
    "Rabbie's": (57.47455, -4.22911),  # ponto de saída na Catedral
    "Highland Explorer Tours": (57.47876, -4.22501),  # Union Street
    "Go Highlands": (57.47780, -4.22470),  # centro de Inverness
    "Jacobite Temptation": (57.48067, -4.22487),  # rodoviária
    "Fig & Thistle": (57.47831, -4.22085),
    "Little Italy": (57.47833, -4.22067),
    "The Mustard Seed": (57.47886, -4.22813),
    "Black Isle Bar": (57.47949, -4.22724),
    "Rocpool": (57.47669, -4.22841),
    # Glencoe e Skye
    "Rannoch Moor e Buachaille Etive Mòr": (56.65149, -4.84129),  # Kingshouse
    "Three Sisters": (56.66775, -4.98677),  # estacionamento
    "Glencoe Visitor Centre": (56.67070, -5.07968),
    "Glencoe Lochan": (56.69069, -5.09584),
    "Clachaig Inn": (56.66446, -5.05657),
    "Fort William e arredores": (56.84640, -5.09370),  # Neptune's Staircase
    "Sligachan": (57.28981, -6.17327),
    "Portree": (57.41144, -6.18998),
    "Old Man of Storr": (57.50696, -6.17464),
    "Kilt Rock": (57.61087, -6.17201),
    "Fairy Pools": (57.24911, -6.24866),
    "Talisker": (57.30188, -6.35668),
    "Dunvegan Castle": (57.44843, -6.59008),
    # York
    "York Minster": (53.96236, -1.08208),
    "Evensong na catedral": (53.96236, -1.08208),
    "Muralhas da cidade": (53.96272, -1.08505),
    "The Shambles": (53.95930, -1.08003),
    "Clifford's Tower": (53.95583, -1.08018),
    "Barley Hall": (53.96091, -1.08260),
    "Merchant Adventurers' Hall": (53.95790, -1.07882),
    "National Railway Museum": (53.96050, -1.09611),
    "York Castle Museum": (53.95522, -1.07813),
    "JORVIK Viking Centre": (53.95739, -1.08029),
    "Museum Gardens e St Mary's Abbey": (53.96211, -1.08817),
    "York Art Gallery": (53.96301, -1.08636),
    "York's Chocolate Story": (53.96002, -1.08035),
    "The Original Ghost Walk": (53.95714, -1.08309),
    "Outros passeios de fantasmas": (53.95930, -1.08003),
    "Pubs históricos": (53.96123, -1.08353),
    "Bettys": (53.96012, -1.08422),
    "Shambles Food Court": (53.95931, -1.08061),
    "Na Grape Lane": (53.96092, -1.08196),
    "The Whippet Inn": (53.95818, -1.08567),
    "Old York Tea Room": (53.96079, -1.08008),
    "Harrogate": (53.99340, -1.53743),  # estação
    "Knaresborough": (54.00903, -1.47032),  # estação
    "Scarborough": (54.27977, -0.40527),  # estação
    "Castle Howard": (54.12156, -0.90665),
    # Fife
    "Fife Coastal Path até Aberdour": (56.03981, -3.33446),  # St Bridget's Kirk
    "Aberdour Castle": (56.05523, -3.29833),
    "Silver Sands": (56.05401, -3.28432),
    "North Queensferry e as pontes": (56.00984, -3.39463),
    "South Queensferry": (55.99180, -3.38608),  # Hawes Pier
    "St Andrews": (56.34007, -2.78783),  # catedral
    "East Neuk": (56.22223, -2.69797),  # Anstruther Fish Bar
    "Culross": (56.05566, -3.62837),
    "Falkland": (56.25310, -3.20798),
    "The Kelpies e Falkirk Wheel": (56.01914, -3.75550),  # Kelpies
    "Stirling Castle": (56.12403, -3.94801),
    "Linlithgow Palace": (55.97872, -3.60056),
    "Blackness Castle": (56.00606, -3.51583),
    "Dunfermline Abbey": (56.06980, -3.46290),
}

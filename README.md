# Painel para a Escócia

Painel em Streamlit para a viagem de 2 a 11 de novembro de 2026: Edimburgo, Inverness, Dalgety Bay (Fife) e York.

- **Roteiro**: as quatro hospedagens, o dia a dia com nascer e pôr do sol e o tempo de cada dia, e o mapa do percurso.
- **Tempo**: condição atual e previsão de 16 dias por cidade (Open-Meteo, atualizada a cada 30 minutos), com a média das mesmas datas de 2015 a 2025 enquanto a previsão não alcança a viagem.
- **Edimburgo, Highlands, Fife e York**: o que ver por região, com horário e preço de novembro, o que estará fechado, onde comer e dicas.
- **Glencoe e Skye**: as formas de encaixar cada um (no caminho, de excursão ou de carro), com o tempo previsto para o dia em cada lugar, um semáforo de "dá para ir" e um filtro por carro e horas ao volante.
- **Trechos**: trem, carro e ônibus entre as cidades, com paradas no caminho.
- **Dicas e gastos**: dinheiro, trem, carro, datas especiais e uma estimativa de gastos.

## Rodar no computador

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Onde mexer

O conteúdo está em `dados.py`. A previsão do tempo e o cálculo do sol ficam em `tempo.py`; o visual, em `estilo.py`. A pesquisa de horários e preços foi feita em 10/10/2026; os itens sem confirmação oficial estão marcados com "confira" no próprio texto.

## Endereços das hospedagens

Endereços e anfitriões não ficam no código, que é público. O app lê esses dados de `st.secrets`:

- no computador, do arquivo `.streamlit/secrets.toml`, que o `.gitignore` mantém fora do GitHub;
- no Streamlit Community Cloud, de **Settings → Secrets**: cole lá o conteúdo do `secrets.toml`.

O formato está em `secrets.exemplo.toml`. Sem esses dados, o painel mostra só o bairro de cada hospedagem.

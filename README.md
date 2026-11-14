# Discoteca

Controle pessoal de bandas e álbuns, com sugestões do que ouvir e um canto para descobrir bandas novas. Feito em
Streamlit. O painel da viagem à Escócia, que morava aqui antes, está guardado no ramo `escocia`.

## O que tem

- **O que ouvir** (página inicial): o que está em rotação, sua fila, por onde começar as bandas da sua lista,
  novidades das suas bandas (lançados nos últimos meses e anunciados), aniversários de discos "neste dia", os álbuns
  que faltam das bandas que você curte, os clássicos que faltam (crítica alta ou presença em listas como Rolling
  Stone 500 e 1001 Discos) e um sorteio.
- **Minhas bandas**: só o que você marcou. As bandas que quer ouvir ("＋ Lista"), as favoritas e as que curte.
- **Acervo**: todas as bandas, com filtros por cena, gênero e situação. Dá para pedir uma banda que não está aqui;
  ela entra sozinha na atualização de segunda-feira.
- **Descobrir**: bandas que você ainda não conhece, ordenadas pelo quanto combinam com o que você curte (gêneros e
  artistas parecidos segundo o Deezer), e artistas de fora do acervo para pedir.
- **Banda**: história, curiosidade, prêmios (Hall da Fama do Rock, Grammys), discografia de estúdio e bandas
  parecidas. Cada álbum tem capa, data, faixas, curiosidade, nota da crítica, nota do público, as listas famosas em
  que aparece, player embutido (Deezer, e Spotify e YouTube quando a Wikidata tem o id) e atalhos que abrem o álbum
  no app de cada serviço. Para cada álbum você marca: conheço, escutei inteiro, quero ouvir, favorito, em rotação,
  sua nota de 0 a 10, faixa favorita, data e um comentário, e baixa a ficha em Markdown para o blog.
- **Números**: escutados por década e cena, retrospectiva do mês e do ano, perfil de gosto por gênero e década,
  seus dez mais e onde você discorda da crítica.

O player toca as faixas inteiras quando você está logado no serviço no mesmo navegador (no Spotify, com Premium e
no computador). Sem login, toca prévias de 30 segundos.

## Onde ficam os dados

| O quê | Onde | Atualização |
|---|---|---|
| Catálogo (bandas, álbuns, faixas, capas, notas da crítica) | `catalogo/*.json` | toda segunda, pelo GitHub Actions (`catalogo.yml`), que acrescenta álbuns novos |
| Textos em português (história e curiosidades) | `textos/*.json` | quando bandas novas entram |
| Deezer: player, capas reserva, fotos, bandas parecidas | `deezer/*.json` | toda segunda (`catalogo.yml`) |
| Listas famosas e prêmios | `extras.json` | toda segunda (`catalogo.yml`) |
| Bandas pedidas no app | Supabase, tabela `pedidos` | entram em `bandas.txt` na segunda |
| Suas marcações e notas | Supabase, projeto "Discoteca" | na hora em que você clica |
| Cópia de segurança das suas notas | `backup/*.json` | todo dia, pelo GitHub Actions (`backup.yml`) |

O backup diário também mantém o projeto gratuito do Supabase acordado: sem nenhum acesso por uma semana, ele
pausaria. Se o banco cair, o app abre a cópia do `backup/` só para leitura.

A chave do Supabase em `banco.py` é a chave publicável, feita para ficar visível: as regras do banco só deixam ler e
gravar as duas tabelas de notas, incluir pedidos de bandas, e nunca apagar.

## Acrescentar bandas

O jeito mais fácil é pedir pelo app (Acervo ou Descobrir). Para incluir na mão, acrescente uma linha em `bandas.txt`
(com uma dica entre `|` se o nome for ambíguo) e rode:

```bash
python scripts/montar_catalogo.py
python scripts/enriquecer_deezer.py
python scripts/listas_e_premios.py
```

Fontes: MusicBrainz (discografia, faixas, datas), Cover Art Archive (capas), Wikidata e Wikipedia (fotos, resumos e
notas da crítica). Tudo aberto e sem chave; as respostas ficam em `.cache/`. Entram só os álbuns de estúdio com
lançamento oficial (piratas ficam de fora).

A rodada semanal usa `--renovar`: reaproveita as fichas já gravadas e só consulta as discografias e os álbuns novos.
Se alguma fonte não responder, a ficha anterior fica como estava.

## Senha (opcional)

Sem configuração, o app abre direto. Para pedir senha, crie `senha = "..."` nos Secrets do app no Streamlit Cloud.

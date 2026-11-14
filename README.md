# Discoteca

Controle pessoal de bandas e álbuns, com sugestões do que ouvir e um canto para descobrir bandas novas. Feito em
Streamlit. O painel da viagem à Escócia, que morava aqui antes, está guardado no ramo `escocia`.

## O que tem

- **Minhas bandas**: grade com foto, país, anos de atividade, gêneros e quanto da discografia você já ouviu. Filtros
  por cena, gênero, situação (na ativa ou encerrada) e pelo que você conhece.
- **Banda**: história, curiosidade, se ainda está na ativa e a discografia de estúdio. Cada álbum tem capa, data,
  faixas com duração, curiosidade, nota da crítica (média das resenhas listadas na Wikipedia, mais AllMusic e
  Metacritic), nota do público do MusicBrainz e links para ouvir no Spotify, YouTube Music e Deezer. Para cada álbum
  você marca: conheço, escutei inteiro, quero ouvir, favorito, sua nota de 0 a 10, faixa favorita, data e um
  comentário (que serve de rascunho de post).
- **O que ouvir**: sua fila, os álbuns que faltam das bandas que você curte, os clássicos que faltam e um sorteio.
- **Descobrir**: bandas que você ainda não conhece, ordenadas pelo quanto os gêneros delas combinam com o que você
  curte, cada uma com um álbum para começar. Inclui um garimpo de bandas tiradas de um acervo de blogs de rock.
- **Números**: o que você já ouviu por década e cena, seus dez mais e onde você discorda da crítica.

## Onde ficam os dados

| O quê | Onde | Atualização |
|---|---|---|
| Catálogo (bandas, álbuns, faixas, capas, notas da crítica) | `catalogo/*.json` | toda segunda, pelo GitHub Actions (`catalogo.yml`), que acrescenta álbuns novos |
| Textos em português (história e curiosidades) | `textos/*.json` | quando bandas novas entram |
| Suas marcações e notas | Supabase, projeto "Discoteca" | na hora em que você clica |
| Cópia de segurança das suas notas | `backup/*.json` | todo dia, pelo GitHub Actions (`backup.yml`) |

O backup diário também mantém o projeto gratuito do Supabase acordado: sem nenhum acesso por uma semana, ele
pausaria. Se o banco cair, o app abre a cópia do `backup/` só para leitura.

A chave do Supabase em `banco.py` é a chave publicável, feita para ficar visível: as regras do banco só deixam ler e
gravar as duas tabelas de notas, e nunca apagar.

## Acrescentar bandas

Inclua uma linha em `bandas.txt` (com uma dica entre `|` se o nome for ambíguo) e rode:

```bash
python scripts/montar_catalogo.py
```

Fontes: MusicBrainz (discografia, faixas, datas), Cover Art Archive (capas), Wikidata e Wikipedia (fotos, resumos e
notas da crítica). Tudo aberto e sem chave; as respostas ficam em `.cache/`. Entram só os álbuns de estúdio com
lançamento oficial (piratas ficam de fora).

A rodada semanal usa `--renovar`: reaproveita as fichas já gravadas e só consulta as discografias e os álbuns novos.
Se alguma fonte não responder, a ficha anterior fica como estava.

## Senha (opcional)

Sem configuração, o app abre direto. Para pedir senha, crie `senha = "..."` nos Secrets do app no Streamlit Cloud.

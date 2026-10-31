"""Confere o atualizacao.json antes de publicar: python verificar_atualizacao.py [caminho]

Formato:
{
  "atualizado_em": "2026-11-02T06:10:00Z",
  "avisos": [
    {"cidade": "geral" | "edimburgo" | "inverness" | "dalgety" | "york",
     "dias": ["2026-11-07"],                # opcional; some do painel depois do último dia
     "nivel": "vermelho" | "laranja" | "azul",
     "texto": "frase curta em português",
     "fonte": "https://..."}
  ],
  "lugares": {
    "Nome exato do cartão": {"nivel": "fechado" | "atencao" | "ok", "nota": "frase curta", "fonte": "https://..."}
  }
}
"""

import json
import sys
from datetime import date, datetime

import dados as D
import para_voce as PV

CIDADES = {"geral"} | {b["id"] for b in D.BASES}


def nomes_dos_cartoes() -> set[str]:
    nomes = set()
    for cidade in list(D.CIDADES.values()) + list(PV.PARA_VOCE.values()):
        for s in cidade["secoes"]:
            nomes |= {p["nome"] for p in s.get("pontos", [])}
    nomes |= {p["nome"] for p in D.GLENCOE + D.SKYE}
    nomes |= {p["nome"] for t in D.TRECHOS for p in t.get("paradas", [])}
    return nomes


def erros(dados: dict) -> list[str]:
    e = []
    try:
        datetime.fromisoformat(dados["atualizado_em"].replace("Z", "+00:00"))
    except Exception:
        e.append("atualizado_em ausente ou fora do formato ISO")
    for i, a in enumerate(dados.get("avisos", [])):
        if a.get("cidade") not in CIDADES:
            e.append(f"avisos[{i}]: cidade deve ser uma de {sorted(CIDADES)}")
        if a.get("nivel") not in ("vermelho", "laranja", "azul"):
            e.append(f"avisos[{i}]: nivel deve ser vermelho, laranja ou azul")
        if not isinstance(a.get("texto"), str) or not 0 < len(a["texto"]) <= 300:
            e.append(f"avisos[{i}]: texto vazio ou com mais de 300 caracteres")
        for d in a.get("dias", []):
            try:
                if not D.INICIO - (D.FIM - D.INICIO) <= date.fromisoformat(d) <= D.FIM:
                    e.append(f"avisos[{i}]: dia {d} fora da viagem")
            except ValueError:
                e.append(f"avisos[{i}]: dia {d} não é AAAA-MM-DD")
        if not str(a.get("fonte", "")).startswith("https://"):
            e.append(f"avisos[{i}]: fonte deve ser um link https")
    nomes = nomes_dos_cartoes()
    for nome, r in dados.get("lugares", {}).items():
        if nome not in nomes:
            e.append(f"lugares: '{nome}' não é o nome exato de nenhum cartão")
        if r.get("nivel") not in ("fechado", "atencao", "ok"):
            e.append(f"lugares['{nome}']: nivel deve ser fechado, atencao ou ok")
        if not isinstance(r.get("nota"), str) or not 0 < len(r["nota"]) <= 200:
            e.append(f"lugares['{nome}']: nota vazia ou com mais de 200 caracteres")
        if not str(r.get("fonte", "")).startswith("https://"):
            e.append(f"lugares['{nome}']: fonte deve ser um link https")
    return e


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "atualizacao.json"
    with open(caminho, encoding="utf-8") as f:
        problemas = erros(json.load(f))
    print("\n".join(problemas) or "OK")
    sys.exit(1 if problemas else 0)

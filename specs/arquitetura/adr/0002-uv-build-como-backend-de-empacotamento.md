---
numero: 0002
titulo: Usar uv_build como backend de empacotamento
status: aceito
data: 2026-08-10
substitui: —
substituido-por: —
modulos: []
---

# 0002 — Usar uv_build como backend de empacotamento

## Contexto

A mudança 001 trocou o Poetry pelo uv por decisão do mantenedor. Isso deixou uma escolha em
aberto que o pedido não cobria: o uv gerencia dependências e ambiente, mas **não impõe** um
backend de build. Sair de `poetry.core.masonry.api` obrigava a escolher o substituto.

Restrições no momento da decisão:

- O pacote tem layout **plano**: `kanbanize_sdk/` fica na raiz, não em `src/`.
- O artefato publicado é um wheel puro-Python, sem extensões compiladas.
- O projeto tinha uma única dependência de runtime, e reduzir fornecedores no toolchain era
  coerente com esse histórico.

Desconhecido no momento: se o `uv_build`, mais novo que as alternativas, teria alguma lacuna
no fluxo de publicação — que segue manual e não foi exercitado nesta mudança.

## Decisão

`[build-system]` passa a usar `uv_build`, com `[tool.uv.build-backend]` declarando
`module-root = ""` e `module-name = "kanbanize_sdk"` para acomodar o layout plano.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| `hatchling` | Maduro e muito usado, e teria funcionado. Mas traz um fornecedor a mais para um toolchain que acabou de ser unificado no uv, sem oferecer nada que este projeto precise — não há build customizado, hook de build nem extensão compilada |
| `setuptools` | Exigiria configuração de descoberta de pacote para o layout plano e é o mais verboso dos três, sem ganho |
| `poetry-core`, mantendo só o backend | Deixaria o Poetry como dependência de build depois de removê-lo como gerenciador. Meia-migração, com o custo de manter dois formatos de metadado na cabeça |

## Consequências

**Ganhamos:**
- Um fornecedor só para ambiente, dependências, lockfile e build
- `uv build` funciona sem configuração além das três linhas de `[tool.uv.build-backend]`
- Metadados em PEP 621, legíveis por qualquer ferramenta do ecossistema

**Pagamos:**
- `uv_build` é mais novo que `hatchling`; menos material de referência quando algo der errado
- O backend fica atrelado à faixa de versão do uv declarada em `[build-system].requires`

**Fica mais difícil depois:**
- Se o projeto um dia precisar de hook de build ou extensão compilada, `hatchling` volta a ser
  o candidato natural e a troca custa um ADR sucessor

## Como reverter

Barato. Trocar `[build-system]` e substituir `[tool.uv.build-backend]` pela configuração
equivalente do backend novo. Nada no código muda, e o wheel resultante é o mesmo. A reversão
não afeta consumidores.

## Sinais de que esta decisão envelheceu

- Necessidade de hook de build, extensão compilada ou artefato além do wheel puro
- Problema de publicação atribuível ao backend quando a release for automatizada (item 5 do
  `visao/ROADMAP.md`)
- O projeto adotar layout `src/`, o que tornaria a configuração de `module-root` desnecessária
  em qualquer backend e reabriria a comparação

# ADRs — Architecture Decision Records

Um arquivo por decisão. **ADR aceito é imutável.**

Mudou de ideia? Não edite: crie um ADR novo e marque o antigo como `substituído`.
O valor de um ADR está no registro do que você achava e por quê — editar destrói isso,
e destrói também a única evidência que justifica o custo da decisão nova.

## Numeração
`NNNN-slug-curto.md`, sequencial, nunca reaproveitada.

## Estados
| Estado | Significado |
|---|---|
| `proposto` | em discussão, não vale como regra |
| `aceito` | vigente e vinculante |
| `substituído` | superado — o campo `substituido-por` aponta o sucessor |
| `rejeitado` | avaliado e descartado; fica registrado para não ser reproposto |

## Quando escrever
Sempre que a decisão tiver **alternativa plausível descartada**. Se não havia alternativa,
não é ADR — é convenção, e vai para `governanca/02-convencoes.md`.

Gatilhos: escolha de biblioteca, padrão de persistência, estratégia de cache, formato de
contrato, modelo de autenticação, decisão de comprar vs construir, aceitação consciente de dívida.

## Índice

| # | Decisão | Estado | Data |
|---|---|---|---|
| [0001](0001-kanbanize-session-compoe-o-cliente-http.md) | Compor o cliente HTTP dentro de `KanbanizeSession` em vez de herdar dele | aceito | 2026-08-07 |
| [0002](0002-uv-build-como-backend-de-empacotamento.md) | Usar `uv_build` como backend de empacotamento | aceito | 2026-08-10 |
| [0003](0003-congelar-a-pilha-de-documentacao-com-pins-transitivos.md) | Congelar a pilha de documentação com pins transitivos em vez de modernizá-la | aceito | 2026-08-10 |
| [0004](0004-converter-o-corpo-para-json-no-endpoint.md) | Converter o corpo para JSON no endpoint, não no wrapper | aceito | 2026-08-11 |
| [0005](0005-introduzir-conftest-para-a-assercao-de-corpo.md) | Introduzir `tests/conftest.py` para a asserção de corpo, revogando a proibição anterior | aceito | 2026-08-11 |
| [0006](0006-documentacao-oficial-como-contrato-de-referencia.md) | Aceitar a documentação oficial da Kanbanize como contrato de referência, sem validação em execução real | aceito | 2026-08-12 |

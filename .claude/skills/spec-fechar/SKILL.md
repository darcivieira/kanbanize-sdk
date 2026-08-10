---
name: spec-fechar
description: Fecha uma mudança concluída — absorve o que foi implementado nos specs de estado (modulos, ui, dados), atualiza checklists, registra ADRs pendentes e limpa ACTIVE.md. Use sempre que o usuário disser que terminou a implementação, que a feature está pronta, que vai abrir o PR, ou pedir para atualizar/sincronizar as specs depois de codar. Use também ao detectar que todas as tarefas de tasks.md estão marcadas.
---

# spec-fechar

Sem este passo o sistema apodrece: specs de estado congelam e viram mentira.

## Passo 1 — Verificar de verdade

Não confie nas caixas marcadas em `tasks.md`. Compare o `spec.md` com o **código real**:

| Verificação | Como |
|---|---|
| Cada RF foi implementado? | Localize o código que o satisfaz. Cite arquivo e linha. |
| Cada critério de aceite tem teste? | Localize o teste. |
| O que foi feito além da spec? | Escopo extra é achado, não bônus — reporte. |
| O que ficou faltando? | Liste explicitamente. |

Divergência entre spec e código **não é erro de spec por padrão**. Pergunte qual dos dois
está certo antes de mexer.

## Passo 2 — Rodar o DoD

Percorra `specs/governanca/04-definition-of-done.md` item por item, marcando só o que você
verificou. Item não verificado fica desmarcado e é reportado — nunca marcado por otimismo.

## Passo 3 — Absorver no estado

| Mudou | Atualize |
|---|---|
| Endpoint, regra de negócio | `modulos/<mod>.md` — checklists e contratos |
| Entidade, campo, migration | `dados/entidades/<mod>.md` e `dados/INDICE.md` |
| Tela, rota, estado de UI | `ui/telas/<tela>.md` |
| Componente compartilhado | `ui/COMPONENTES.md` |
| Topologia, camada, fluxo | `arquitetura/VISAO_TECNICA.md` |
| Termo novo do domínio | `visao/GLOSSARIO.md` |
| Entrega de roadmap | `visao/ROADMAP.md` |

Respeite a propriedade de fatos de `governanca/02-convencoes.md`: um fato, um dono.
Se você está prestes a escrever a mesma informação em dois arquivos, pare — um deles deve referenciar.

## Passo 4 — ADRs

Para cada linha de `plan.md` marcada "vira ADR: sim", e para toda decisão tomada durante a
implementação que um revisor questionaria: use a skill `spec-adr`.

Decisão que revoga ADR anterior **não edita o anterior** — cria sucessor e marca o antigo
como `substituído`.

## Passo 5 — Encerrar

1. `spec.md` → `status: concluida`
2. `specs/ACTIVE.md` → `nenhuma`
3. Mantenha `mudancas/NNN-*/` no repositório. É o histórico do porquê.
4. Rode `python3 scripts/spec_status.py` e reporte.

## Saída

Resumo com: RFs entregues, o que ficou pendente e por quê, arquivos de spec atualizados,
ADRs criados, e itens de DoD que **não** puderam ser verificados.

Seja honesto sobre o pendente. Fechamento otimista é o modo mais rápido de a spec virar ficção.

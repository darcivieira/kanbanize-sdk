# Plano — NNN <título>

> Só existe depois que `spec.md` está aprovada. Aqui entra o **como**.

## Abordagem
<2 a 5 frases. O desenho em prosa antes do detalhe.>

## O que é reusado
| Existente | Caminho | Como entra |
|---|---|---|

Preencher esta tabela **antes** da próxima. Criar sem ter procurado é violação.

## O que é criado
| Novo | Caminho | Justificativa de não reusar |
|---|---|---|

## Alternativas consideradas
| Alternativa | Por que não | Vira ADR? |
|---|---|---|

## Contratos afetados
| Contrato | Mudança | Quebra compatibilidade? |
|---|---|---|

## Dados e migrations
| Passo | Reversível | Backfill | Risco |
|---|---|---|---|

## Backend ↔ frontend
<Ordem de entrega, como evitar quebra durante o deploy, feature flag se houver.>

## Estratégia de teste
| Nível | O que cobre | Cobre qual RF |
|---|---|---|

> Ao escrever os checkpoints, separe **o que se verifica na máquina** (testes, cobertura,
> build local) do **que só o remoto responde** (CI, Read the Docs, publicação). Misturar os
> dois trava o fechamento à toa — ver `governanca/04-definition-of-done.md`.

## Pontos de falha
| O que pode dar errado | Detectado por | Resposta |
|---|---|---|

## Fora do plano
<O que foi cogitado e deliberadamente adiado.>

---
**Aprovação humana:** ☐ pendente  
Não inicie a implementação sem esta caixa marcada.

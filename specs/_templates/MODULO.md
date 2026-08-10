# Módulo: <nome>

> Dono do fato: **comportamento** deste módulo. Schema fica em `dados/entidades/<nome>.md`.

## Responsabilidade
<uma frase. Se precisar de "e", o módulo provavelmente é dois.>

## Não faz
<limites explícitos — o que pertence a outro módulo.>

## Entidades usadas
| Entidade | Dono | Este módulo |
|---|---|---|
| | `dados/entidades/*.md` | lê / escreve / possui |

## Endpoints

### `MÉTODO /caminho`
- **Para quê:** 
- **Autorização:** 
- **Entrada:**

  | Campo | Tipo | Obrig. | Regra |
  |---|---|---|---|

- **Saída (200):**

  | Campo | Tipo | Descrição |
  |---|---|---|

- **Erros:**

  | Código | Quando | Corpo |
  |---|---|---|

- **Progresso:**
  - [ ] rota
  - [ ] validação
  - [ ] autorização
  - [ ] regra de negócio
  - [ ] testes

## Regras de negócio
| # | Regra | Onde vive |
|---|---|---|
| RN-1 | | |

## Dependências
| Depende de | Tipo | Se cair |
|---|---|---|

## Eventos publicados / consumidos
| Evento | Direção | Payload | Idempotente? |
|---|---|---|---|

## Testes esperados
- [ ] 

## Pendências conhecidas
| Item | Motivo | ADR |
|---|---|---|

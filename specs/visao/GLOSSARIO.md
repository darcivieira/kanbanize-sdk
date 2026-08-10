# Glossário

Termos de domínio. Dono único de cada definição — outros arquivos usam o termo, não o redefinem.

Regra: se um termo aparece em spec com dois sentidos, ele entra aqui e os dois sentidos ganham
nomes distintos.

O domínio é o da plataforma Kanbanize/Businessmap. O SDK não inventa conceito nenhum: cada
termo abaixo corresponde a um recurso ou campo da API v2.

## Domínio da plataforma

| Termo (PT) | Identificador no código (EN) | Definição |
|---|---|---|
| Espaço de trabalho | `workspace` | Agrupador de topo. Contém boards. Tem gerentes próprios (`managers`) e histórico de eventos. Recurso `/workspaces`. |
| Quadro | `board` | Unidade de trabalho dentro de um workspace. Concentra a maior parte da configuração do SDK: settings, estrutura, histórico, tags, stickers, campos customizados, tipos de cartão, motivos de bloqueio e descarte. Recurso `/boards`. |
| Fluxo de trabalho | `workflow` | Subdivisão de um quadro que agrupa colunas e raias. Um quadro tem N workflows. Pode ser copiado para outro quadro (`copy`). |
| Raia | `lane` | Faixa **horizontal** do quadro. Aninhável — `parent_lane_id` aponta para a raia mãe. |
| Coluna | `column` | Faixa **vertical** do quadro. Aninhável via `parent_column_id`. Pertence a uma `section` e a um `flow_type`. |
| Seção | `section` | Agrupamento de colunas dentro de um workflow, identificado por um inteiro. <<PREENCHER: o que cada valor de `section` significa na plataforma — o código só trafega o número, sem enumeração.>> |
| Célula | *(sem recurso próprio)* | A interseção de uma raia com uma coluna. Não é um recurso da API; só existe como alvo de limite. |
| Limite de célula | `cell limit` | Limite de WIP em uma célula específica. Trinca `lane_id` + `column_id` + `limit`. Recurso `/boards/{id}/cellLimits` — só `list` e `update` (PUT no conjunto inteiro). |
| Limite de seção de raia | `lane section limit` | Limite de WIP na interseção de uma raia com uma **seção** inteira (não com uma coluna). Trinca `lane_id` + `section` + `limit`. |
| Área mesclada | `merged area` | Conjunto de `lane_ids` × `column_ids` tratado como uma célula única, com uma `primary_column_id` e um `limit` próprio. |
| Adesivo | `sticker` | Marcador atribuível a cartões. O SDK gerencia apenas a **vinculação ao quadro** e seus limites (`limit_per_board`, `limit_per_card`), não a criação do adesivo em si. |
| Tipo de cartão | `card type` | Classificação de cartão vinculada ao quadro, com ícone (`icon_type`, `icon_id`), cor e `card_color_sync`. Tem `effectiveSettings` — a configuração resultante após herança. |
| Campo customizado | `custom field` | Campo definido pelo usuário e vinculado ao quadro. Recurso `/boards/{id}/customFields`. |
| Valor permitido | `allowed value` | Opção válida de um campo customizado de lista. Subrecurso do campo customizado, com `position` e `is_default`. |
| Contribuinte padrão | `default contributor` | Usuário pré-atribuído a um campo customizado. Subrecurso do campo customizado. |
| Motivo de descarte | `discard reason` | Razão registrada ao descartar um cartão. Pode ser obrigatória — ver `is_discard_reason_required` em `BoardSettingsUpdateBody`. |
| Motivo de bloqueio | `block reason` | Razão registrada ao bloquear um cartão. Recurso distinto do motivo de descarte. |
| Campo padrão visível | `visible standard field` | Campo nativo da plataforma que o quadro escolhe exibir. Identificado por **nome**, não por id. |
| Papel no quadro | `userRole` | Vínculo entre um usuário e um quadro, com um `role_id`. **Cuidado:** o SDK chama isso de `BoardAssignees`, mas o endpoint é `/boards/{id}/userRoles`. Dois nomes, um conceito. |
| Revisão de estrutura | `structure revision` | Versão numerada da estrutura de um quadro. `currentStructure` devolve a vigente; `structureRevisions` devolve o histórico. |
| Subdomínio | `subdomain` | Identificador da conta Kanbanize do cliente. Compõe a URL base: `https://{subdomain}.kanbanize.com/api/v2`. |
| Chave de API | `api_key` | Credencial da conta. Enviada no header HTTP `apikey` em toda requisição. |

## Termos do próprio SDK

| Termo (PT) | Identificador no código (EN) | Definição |
|---|---|---|
| Recurso | *classe em `endpoints/`* | Uma classe que agrupa os métodos de um recurso REST da API. Ex.: `Boards`, `Lanes`. |
| Fachada | `Kanbanize` | Ponto de entrada único. Cria a sessão e devolve instâncias de recurso por método-fábrica. |
| Sessão | `KanbanizeSession` | Classe que **compõe** um `httpx.Client` privado, monta a URL base, injeta o header `apikey` e trata a resposta. Não herda de cliente de terceiro — ver ADR 0001. |
| Corpo | `body` (`*InsertBody`, `*UpdateBody`) | Dataclass que representa o payload de escrita. Todo método aceita alternativamente um `dict` cru. |
| Parâmetros | `params` (`*ListParams`) | Dataclass que representa a query string de listagem. Também aceita `dict` cru. |
| Atributo desligado | `private` | Marcador de `utils.py` que desativa um método herdado, levantando `AttributeError` ao acesso. Ver termo ambíguo abaixo. |

## Os dois sentidos de "resposta"

Este par causou ambiguidade real e por isso ganha nomes distintos. Use sempre o nome
qualificado, nunca "resposta" sozinho:

| Nome a usar | O que é |
|---|---|
| **Resposta da API** | O JSON completo que a Kanbanize devolve, incluindo o envelope: `{"data": ..., "pagination": ...}`. |
| **Retorno do SDK** | O conteúdo já **desembrulhado**. Sem paginação, é apenas o valor de `data`. **Com** paginação, é o dict inteiro com as chaves de `pagination` promovidas ao topo — e `data` continua lá dentro. |

O desembrulho acontece em um único lugar: o middleware de resposta em `wrapper.py`. A tabela
completa de status → retorno está em `arquitetura/VISAO_TECNICA.md`, fluxo 4.

## Termos ambíguos a evitar

Proibidos em spec sem qualificação:

- **"cliente"** — pode significar o objeto `Kanbanize` (fachada), a `KanbanizeSession` (transporte
  HTTP), ou o cliente comercial dono do subdomínio. Diga qual.
- **"usuário"** — pode ser o `user` da plataforma Kanbanize (recurso `/users`) ou o dev que
  consome a biblioteca. Use **"usuário da plataforma"** vs **"dev consumidor"**.
- **"resposta"** — ver seção acima. Sempre "resposta da API" ou "retorno do SDK".
- **"privado"** — no SDK, `private` **não** significa visibilidade Python (`_nome`). Significa
  um método herdado que foi deliberadamente desativado e levanta `AttributeError`.
- **"inserir" / `insert`** — não implica `POST`. Em vários recursos do SDK, `insert` faz **`PUT`
  em um id que o chamador fornece** (`BoardStickers`, `BoardCustomFields`,
  `BoardCustomFieldAllowedValues`, `BoardCardTypes`). Sempre diga o verbo HTTP.
- **"atualizar" / `update`** — pode ser `PATCH` (atualização parcial) ou `PUT` (substituição do
  conjunto, como em `CellLimits` e `LaneSectionLimits`). Sempre diga o verbo HTTP.
- **"seção"** — a `section` de uma coluna e a seção de um `lane section limit` são o mesmo
  campo conceitual, mas aparecem em recursos diferentes. Qualifique com o recurso.
- **"limite"** — existem três: limite de coluna (`limit` em `ColumnsInsertBody`), limite de
  célula e limite de seção de raia. Nunca use sozinho.

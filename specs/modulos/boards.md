# Módulo: boards

> Dono do fato: **comportamento** do recurso `Boards`. Transporte e tratamento de erro são de
> `arquitetura/VISAO_TECNICA.md`.

Classe: `kanbanize_sdk/endpoints/boards.py` · `endpoint = '/boards'` · marker `@mark.boards`

É o recurso mais importante do SDK: **19 das 27 classes** dependem dele, por herança direta ou
por usarem `/boards/{board_id}/...` como base de path.

## Responsabilidade

Expor o CRUD de quadros da plataforma Kanbanize e servir de classe base para os subrecursos que
compartilham o path `/boards`.

## Não faz

Não trata de nada abaixo de `/boards/{id}/`. Cada subrecurso tem módulo próprio — settings,
estrutura, histórico, tags, stickers, campos customizados, tipos de cartão, motivos, workflows,
raias, colunas e limites. Ver `00-indice.md`.

## Métodos

### `list(params, **kwargs) → GET /boards`

- **Entrada:** `BoardsListParams | dict | None`

  | Campo | Tipo | Obrig. |
  |---|---|---|
  | `board_ids` | `List` | não |
  | `workspace_ids` | `List` | não |
  | `is_archived` | `Literal[0, 1]` | não |
  | `if_assigned` | `Literal[0, 1]` | não |
  | `fields` | `List` | não |
  | `expand` | `List` | não |

- **Saída:** `list`.
- 🔴 **A dataclass `BoardsListParams` não funciona.** Ver Pendências. Hoje o único jeito de
  filtrar é passar `dict` cru.
- **Progresso:** ☑ método ☐ dataclass utilizável ☑ export ☑ fábrica ☑ teste ☑ doc

### `insert(body) → POST /boards`

- **Entrada:** `BoardsInsertBody | dict` — os três campos são **obrigatórios**:
  `workspace_id: int`, `name: str`, `description: str`.
- **Saída:** `dict`.
- **Progresso:** ☑ método ☑ dataclass ☑ export ☑ fábrica ☑ teste ☑ doc

### `get(board_id) → GET /boards/{board_id}`

- **Saída:** `dict`.
- **Progresso:** ☑ método ☑ export ☑ fábrica ☑ teste ☑ doc

### `update(board_id, body) → PATCH /boards/{board_id}`

- **Entrada:** `board_id: int` + `BoardsUpdateBody | dict` — `name`, `description`,
  `is_archived`, todos opcionais.
- **Saída:** `dict`.
- **Progresso:** ☑ método ☑ dataclass ☑ export ☑ fábrica ☑ teste ☑ doc

### `delete(board_id) → DELETE /boards/{board_id}`

- **Saída:** `None`.
- **Progresso:** ☑ método ☑ export ☑ fábrica ☑ teste ☑ doc

## Herança — subrecursos que estendem esta classe

Reaproveitam `endpoint = '/boards'` e desligam com `utils.private` o que não se aplica:

| Classe | Herda | Mantém | Desliga |
|---|---|---|---|
| `BoardSettings` | `Boards` | `get`, `update` | `list`, `insert`, `delete` |
| `BoardStructure` | `Boards` | `get`, `get_revision` | os demais |
| `BoardStructureRevisions` | `Boards` | `get`, `get_revision` | os demais |
| `BoardHistory` | `Boards` | `list` | os demais |

Alterar a assinatura de qualquer método de `Boards` **propaga para as quatro**. Por isso
mexer aqui é sempre no mínimo 🟡 YELLOW.

## Erros

Sem tratamento local. Ver `arquitetura/VISAO_TECNICA.md`, fluxo 4.

## Testes existentes

`tests/test_boards.py`, marker `@mark.boards`, 5 testes de caminho feliz:

- [x] `test_list_boards`
- [x] `test_get_board`
- [x] `test_insert_board`
- [x] `test_update_board`
- [x] `test_delete_board`
- [ ] nenhum teste com `BoardsListParams` — é por isso que o defeito abaixo nunca apareceu
- [ ] nenhum teste de erro

## Pendências conhecidas

| Item | Motivo | Situação |
|---|---|---|
| 🔴 **`BoardsListParams` é inutilizável** | `dataclasses.py:124` está **sem o decorator `@dataclass`**. Sem ele não há `__init__` gerado: `BoardsListParams(board_ids=[1])` levanta `TypeError: BaseDataClasse.__init__() got an unexpected keyword argument 'board_ids'`. E `BoardsListParams().to_dict()` devolve `{}`, porque os atributos ficam na classe, não na instância — um filtro montado por atributo seria **silenciosamente descartado** | Defeito confirmado por execução em 2026-08-07. Correção é adicionar `@dataclass`. Nenhum teste cobre o caso |
| `insert`/`update` usam `data=payload` | O `httpx` urlencoda `dict` em `data=`, sob header `Content-Type: application/json` — mesmo comportamento de fio que o `requests` tinha. `Users.insert` usa `json=` e destoa | Preservado na mudança 001, por falta de verificação contra a API real. Ver `arquitetura/VISAO_TECNICA.md`, riscos |
| Campos sem descrição de regra | O significado de cada filtro está no OpenAPI da conta, que o agente não acessa | <<PREENCHER: colar o trecho da doc de `/boards` para completar a coluna de regra>> |

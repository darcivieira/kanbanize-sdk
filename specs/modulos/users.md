# Módulo: users

> Dono do fato: **comportamento** do recurso `Users`. Transporte e tratamento de erro são de
> `arquitetura/VISAO_TECNICA.md`.

Classe: `kanbanize_sdk/endpoints/users.py` · `endpoint = '/users'` · marker `@mark.users`

## Responsabilidade

Expor os endpoints de usuário da plataforma Kanbanize como métodos Python.

## Não faz

Não gerencia vínculo de usuário com quadro (isso é `board-assignees.md`, endpoint
`/userRoles`), nem com time (`teams.md`), nem lista os workspaces que ele gerencia
(`managed-workspaces.md`).

## Métodos

### `list(params) → GET /users`

- **Para quê:** listar usuários da plataforma.
- **Entrada:** `UsersListParams | dict | None`

  | Campo | Tipo | Obrig. | Observação |
  |---|---|---|---|
  | `user_ids` | `List` | não | `to_dict()` converte cada item para `str` |
  | `is_enabled` | `Literal[0, 1]` | não | |
  | `is_confirmed` | `Literal[0, 1]` | não | |
  | `if_assigned_where_i_am` | `Literal[0, 1]` | não | |
  | `fields` | `List` | não | |
  | `expand` | `List` | não | |

- **Saída:** `list` — o conteúdo de `data`.
- **Progresso:** ☑ método ☑ dataclass ☑ export ☑ fábrica ☑ teste ☑ doc

### `insert(body) → POST /users/invite`

- **Para quê:** convidar um usuário. **O path não é `/users`** — é `/users/invite`.
- **Entrada:** `UsersInsertBody | dict` — `email: str`, **obrigatório**. É a única dataclass do
  recurso sem campo opcional.
- **Saída:** `dict`.
- **Particularidade:** é o **único método de escrita de todo o SDK que usa `json=payload`**.
  Todos os demais usam `data=payload`. Ver Pendências.
- **Progresso:** ☑ método ☑ dataclass ☑ export ☑ fábrica ☑ teste ☑ doc

### `get(user_id) → GET /users/{user_id}`

- **Entrada:** `user_id: int`.
- **Saída:** `dict`.
- **Progresso:** ☑ método ☑ export ☑ fábrica ☑ teste ☑ doc

### `update(user_id, body) → PATCH /users/{user_id}`

- **Entrada:** `user_id: int` + `UsersUpdateBody | dict`

  | Campo | Tipo | Obrig. |
  |---|---|---|
  | `email` | `str` | não |
  | `username` | `str` | não |
  | `is_enabled` | `Literal[0, 1]` | não |
  | `is_tfa_enabled` | `Literal[0, 1]` | não |

- **Saída:** `dict`.
- **Progresso:** ☑ método ☑ dataclass ☑ export ☑ fábrica ☑ teste ☑ doc

### `delete(user_id) → DELETE /users/{user_id}`

- **Saída:** `None`. É o único método que **não** retorna o resultado de `self.service` —
  chama sem `return`. O efeito é o mesmo (`delete` devolve `None` em `204`), mas destoa do
  padrão de `Boards.delete`, que faz `return`.
- **Progresso:** ☑ método ☑ export ☑ fábrica ☑ teste ☑ doc

## Erros

Não há tratamento local. Todo status fora de `200`/`204` vira `ValueError` no middleware —
tabela completa em `arquitetura/VISAO_TECNICA.md`, fluxo 4.

## Testes existentes

`tests/test_users.py`, marker `@mark.users`, 5 testes — um por método, todos de caminho feliz:

- [x] `test_list_users`
- [x] `test_get_user`
- [x] `test_invite_user`
- [x] `test_update_user`
- [x] `test_delete_user`
- [ ] nenhum teste de erro (400/401/403/404/409/429/500/503)

## Pendências conhecidas

| Item | Motivo | Situação |
|---|---|---|
| `insert` usa `json=`, todos os outros recursos usam `data=` | Inconsistência histórica. `json=` é o correto para um corpo JSON; `data=` com `dict` urlencoda | Preservado na mudança 001. Padronizar depende de verificação do mantenedor contra a API real |
| `delete` não faz `return` | Destoa do padrão dos outros recursos | Cosmético |
| Docstrings das dataclasses são placeholder | Dívida aberta | Ver `governanca/01-constituicao.md` |
| Campos sem descrição de regra | O significado de cada filtro está no OpenAPI da conta, que o agente não acessa | <<PREENCHER: colar o trecho da doc de `/users` para completar a coluna de regra>> |

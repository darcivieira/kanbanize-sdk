# Tarefas — 002 Padronizar o corpo das escritas em JSON e automatizar a publicação no PyPI

Ordenadas por dependência. `[P]` = pode rodar em paralelo com a anterior.
Cada tarefa toca poucos arquivos e tem critério de pronto verificável.

Branch: `release_automation_and_json_body`

---

# FRENTE 1 — corpo JSON

## T-1 — Aceitar `json=` em `put` e `patch`
- **Arquivos:** `kanbanize_sdk/wrapper.py`
- **Depende de:** —
- **Cobre:** RF-1 (viabilizador)
- **Detalhe:** hoje só `post` tem o parâmetro `json`. `put(self, url, data=None, **kwargs)` e
  `patch(self, url, data=None, **kwargs)` ganham `json=None`, repassado ao cliente. Alteração
  **aditiva**: `data=` continua funcionando com o mesmo default. Não mexer no middleware nem
  nos headers.
- **Pronto quando:** `uv run python -c "import inspect;from kanbanize_sdk.wrapper import KanbanizeSession as K;print('json' in inspect.signature(K.put).parameters, 'json' in inspect.signature(K.patch).parameters)"` imprime `True True`.
- [x] feito

## T-2 — Criar a asserção de corpo, com teste negativo
- **Arquivos:** `tests/conftest.py` (criar), `tests/test_wrapper.py`
- **Depende de:** T-1
- **Cobre:** RF-4, RF-5
- **Detalhe:** um helper que recebe `httpx_mock` e o dict esperado, lê
  `httpx_mock.get_request().content` e afirma `json.loads(...) == esperado`. **Inclui um teste
  negativo** que prova que o helper falha quando o corpo é form-urlencoded — sem ele, a
  blindagem pode passar nos dois formatos e não provar nada. Acrescentar também teste de que
  `put` e `patch` transmitem `json=`.
- **Atenção:** criar `tests/conftest.py` contradiz a regra escrita em `testes/ESTRATEGIA.md`.
  Só execute se a aprovação do plano tiver confirmado essa escolha; caso contrário, a asserção
  é repetida em cada teste, sem `conftest.py`.
- **Pronto quando:** o teste negativo falha se o helper for aplicado a um corpo urlencodado, e
  passa quando aplicado a JSON.
- [x] feito

## T-3 — Trocar `data=` por `json=` nas 29 chamadas
- **Arquivos:** 16 arquivos em `kanbanize_sdk/endpoints/` — `boards.py`, `board_teams.py`,
  `columns.py`, `board_settings.py`, `board_custom_fields.py`, `lane_section_limits.py`,
  `board_card_types.py`, `cell_limits.py`, `merged_areas.py`, `teams.py`, `workspaces.py`,
  `board_stickers.py`, `users.py`, `workflows.py`, `lanes.py`,
  `board_custom_field_allowed_values.py`, `board_assignees.py`
- **Depende de:** T-1
- **Cobre:** RF-1, RF-2, RF-3, RF-6
- **Detalhe:** só o nome do argumento muda. **Três chamadas são multi-linha** e não aparecem em
  `grep` por linha — `board_custom_field_allowed_values.py` (duas) e `board_assignees.py`
  (uma). `users.py:44` (`Users.insert`) **já usa `json=` e não deve ser tocado**; a única linha
  a mudar naquele arquivo é a `:72` (`update`). Não tocar nas 7 escritas sem corpo.
- **Pronto quando:** a contagem por AST devolve `com data= : 0` e `com json= : 30`, e o diff
  não altera nenhuma assinatura.
- [x] feito

## T-4 — Aplicar a asserção de corpo nos testes de escrita
- **Arquivos:** os 24 arquivos de `tests/` com `add_response(method='POST'|'PUT'|'PATCH')`
- **Depende de:** T-2, T-3
- **Cobre:** RF-4, RNF-2, RNF-3
- **Detalhe:** 37 chamadas de escrita mockadas. Cada teste passa a afirmar o corpo, além da
  resposta. Cobrir os dois caminhos: teste com dataclass e teste com `dict` cru — hoje quase
  todos usam dataclass.
- **Pronto quando:** `uv run pytest -q` verde com **mais** de 124 testes, cobertura ≥ 99%.
- [x] feito

## T-5 [P] — Registrar o ADR do local da conversão
- **Arquivos:** `specs/arquitetura/adr/0004-*.md`, e `0005-*.md` se `conftest.py` for adotado
- **Depende de:** T-3
- **Cobre:** — (constituição, princípio 4)
- **Detalhe:** skill `spec-adr`. Decisão 1: converter no endpoint e não no wrapper — a
  alternativa de o wrapper reinterpretar `data=` é plausível e precisa constar. Decisão 2, se
  aplicável: introduzir `conftest.py` contra a regra de `testes/ESTRATEGIA.md`, e atualizar a
  regra lá.
- **Pronto quando:** ADR(s) com status `aceito` e indexados em `adr/README.md`.
- [x] feito

---

## Checkpoint 1

- `uv run pytest -q` verde, > 124 testes, cobertura ≥ 99%
- contagem por AST: `data=` zerado nas escritas de `endpoints/`
- diff vazio em `kanbanize_sdk/__init__.py` e `endpoints/__init__.py`
- `users.py:44` inalterado

---

# FRENTE 2 — publicação automatizada

## T-6 — Criar `.github/workflows/release.yml`
- **Arquivos:** `.github/workflows/release.yml` (criar)
- **Depende de:** —
- **Cobre:** RF-7, RF-8, RF-9, RF-10, RF-11, RF-12, RF-15, RF-16, RNF-4, RNF-5
- **Detalhe:** `on: release: types: [published]`. Um job, no environment `pypi`, com
  `permissions: id-token: write`. Ordem dos passos, e ela importa:
  1. checkout
  2. **encerrar sem publicar se a release for pre-release** (RF-16)
  3. instalar uv e Python 3.13, como no `pipeline.yml`
  4. **conferir que a tag `X.Y.Z` bate com a `version` do `pyproject.toml`**, sem prefixo `v` — falhar se não (RF-9)
  5. `uv sync --no-group doc` e `uv run pytest` (RF-11)
  6. `uv build`
  7. publicar por OIDC — **último passo** (RF-12)
  Nenhum secret. Não alterar `pipeline.yml`.
- **Pronto quando:** o arquivo existe, o CI segue verde, e o workflow **não** aparece nas
  execuções do push da branch (RNF-5).
- [x] feito

## T-7 — Passos manuais do mantenedor
- **Arquivos:** nenhum — configuração fora do repositório
- **Depende de:** T-6
- **Cobre:** RF-8, RF-15
- **Detalhe:** **tarefa do humano, o agente não executa.**
  1. No painel do PyPI, registrar o Trusted Publisher: repositório `darcivieira/kanbanize-sdk`,
     workflow `release.yml`, environment `pypi`.
  2. Nas configurações do repositório, criar o environment `pypi` **com regra de proteção
     ativa** — exigida na primeira release pela decisão D-4.
- **Pronto quando:** o mantenedor confirma os dois. Sem isso, T-9 falha na autenticação.
- [x] feito

## T-8 [P] — Atualizar specs e convenções
- **Arquivos:** `specs/governanca/02-convencoes.md`, `specs/visao/ROADMAP.md`,
  `specs/arquitetura/VISAO_TECNICA.md`, `specs/modulos/boards.md`, `specs/modulos/users.md`
- **Depende de:** T-6
- **Cobre:** RF-14
- **Detalhe:** `02-convencoes.md` — a linha "Publicar: manual hoje" com marcador de pendência
  vira a descrição do fluxo por release; some o marcador de pendência do comando de publicação. `ROADMAP.md` — item 5 marcado
  como entregue, e saem as linhas de bloqueio do `data=`/`json=` e da publicação manual.
  `VISAO_TECNICA.md` — fluxo 3 passa a dizer `json=`, e o risco correspondente sai. Os dois
  módulos perdem a pendência de `data=`/`json=`.
- **Pronto quando:** `grep -rn "data=" specs/` só retorna menções históricas em
  `mudancas/`, e `python3 scripts/spec_status.py` mostra um marcador de pendência a menos.
- [x] feito

---

## Checkpoint 2

- Workflow no repositório, CI verde, e ele **não** disparou em push nem em PR
- T-7 confirmada pelo mantenedor
- Specs sem a pendência de `data=`/`json=` nem a de comando de publicação

---

# RELEASE

## T-9 — Publicar a 0.3.0
- **Arquivos:** nenhum — ação no GitHub
- **Depende de:** merge da PR, Checkpoint 2, e T-7 confirmada
- **Cobre:** RF-13
- **Detalhe:** **tarefa do humano.** Criar a release no GitHub com tag `0.3.0` — **sem o `v`** —, **não**
  marcada como pre-release. Aprovar o environment quando o workflow pedir. É o **único passo
  irreversível do plano**: o PyPI não permite republicar uma versão.
- **Pronto quando:** em ambiente limpo, `pip install kanbanize-sdk==0.3.0` instala e
  `python -c "import kanbanize_sdk"` funciona em Python 3.13.
- [x] feito

## Cobertura dos requisitos

| RF | Tarefa |
|---|---|
| RF-1 | T-1, T-3 |
| RF-2, RF-3, RF-6 | T-3 |
| RF-4 | T-2, T-4 |
| RF-5 | T-2 |
| RF-7 a RF-12, RF-15, RF-16 | T-6 |
| RF-8, RF-15 (execução real) | T-7 |
| RF-13 | T-9 |
| RF-14 | T-8 |

Todos os 16 RFs cobertos.

## Ao concluir todas

Ordem de encerramento de `governanca/04-definition-of-done.md`:
**push → CI verde → `spec-fechar` → abrir a PR → merge → T-9.**

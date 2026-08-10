# Tarefas — 001 Migração de runtime, gerenciador de pacotes e cliente HTTP

Ordenadas por dependência. `[P]` = pode rodar em paralelo com a anterior.
Cada tarefa toca poucos arquivos e tem critério de pronto verificável.

Branch: `migration_runtime_toolchain_httpx`

---

# ENTREGA A — Python 3.13 + uv

Nenhuma tarefa desta entrega altera `kanbanize_sdk/` ou `tests/`.

## T-1 — Traduzir `pyproject.toml` de Poetry para PEP 621 + uv
- **Arquivos:** `pyproject.toml`
- **Depende de:** —
- **Cobre:** RF-1, RF-2, RF-3, RF-17
- **Detalhe:** `[tool.poetry]` → `[project]`; `requires-python = ">=3.13"`; `version = "0.3.0"`;
  classificador `Programming Language :: Python :: 3.10` → `3.13`; `[build-system]` deixa de ser
  `poetry.core.masonry.api`; grupos `dev` e `doc` migram para o formato de grupos do uv,
  preservando os mesmos pacotes e faixas de versão. `requests` continua como dependência de
  runtime nesta entrega — a troca é da Entrega B.
- **Pronto quando:** `uv sync` completa sem erro e `python -c "import kanbanize_sdk"` funciona
  no ambiente do uv.
- [x] feito

## T-2 — Transcrever os 29 markers de pytest
- **Arquivos:** `pyproject.toml`
- **Depende de:** T-1
- **Cobre:** RF-3
- **Detalhe:** os markers de `[tool.pytest.ini_options]` (hoje linhas 38–69) precisam sobreviver
  intactos. Marker perdido não quebra a suíte — o teste só some do filtro `-m`, silenciosamente.
- **Pronto quando:** `uv run pytest --markers | grep -c "^@pytest.mark"` lista os 29 markers do
  projeto, e a contagem confere com o arquivo original.
- [x] feito

## T-3 — Gerar `uv.lock` e comparar as versões resolvidas
- **Arquivos:** `uv.lock` (criar)
- **Depende de:** T-1
- **Cobre:** RF-4
- **Detalhe:** comparar as versões resolvidas com as travadas em `poetry.lock` — `requests`
  2.32.3, `pytest` 7.4.4, `pytest-cov` 4.1.0, `requests-mock` 1.12.1, `isort` 5.13.2. Divergência
  precisa ser consciente, não acidental.
- **Pronto quando:** `uv.lock` existe, versionado, e as divergências em relação a `poetry.lock`
  estão listadas no corpo do commit.
- [x] feito

## T-4 — Remover `poetry.lock`
- **Arquivos:** `poetry.lock` (remover)
- **Depende de:** T-3
- **Cobre:** RF-4
- **Pronto quando:** o arquivo não existe e `uv sync` continua funcionando a partir do zero
  (`rm -rf .venv && uv sync`).
- [x] feito

## T-5 — Atualizar o CI para 3.13 + uv
- **Arquivos:** `.github/workflows/pipeline.yml`
- **Depende de:** T-3
- **Cobre:** RF-11
- **Detalhe:** `python-version: '3.10'` → `'3.13'`; `pip install poetry` → instalação do uv;
  `poetry install --without doc` → equivalente em uv; `poetry run pytest ...` → `uv run pytest ...`
  preservando as mesmas flags (`-s -x --cov=kanbanize_sdk -vv --cov-report=xml`). O passo do
  Codecov não muda.
- **Pronto quando:** o workflow roda verde na PR, com 109 testes.
- [x] feito

## T-6 [P] — Atualizar o Read the Docs
- **Arquivos:** `.readthedocs.yaml`
- **Depende de:** T-3
- **Cobre:** RF-12
- **Detalhe:** `tools.python: "3.10"` → `"3.13"`; os jobs `post_create_environment` e
  `post_install` hoje chamam `pip install poetry`, `poetry config virtualenvs.create false` e
  `poetry install --only doc` — precisam virar o equivalente em uv. `mkdocs.yml` não muda.
- **Pronto quando:** o build do RTD na PR fica verde e a página de uma classe de recurso
  renderiza (o mkdocstrings precisa continuar enxergando `kanbanize_sdk`).
- [x] feito

---

## Checkpoint A

Após T-6, tudo abaixo verdadeiro ao mesmo tempo:

- `uv run pytest --cov=kanbanize_sdk --cov-report=term-missing -q` → **109 passed**, cobertura ≥ 99%
- `git diff --stat main -- kanbanize_sdk/ tests/` → **vazio**. Se houver qualquer linha aqui, a
  Entrega A saiu do escopo
- CI verde em Python 3.13
- Build do RTD verde
- `poetry.lock` não existe; `uv.lock` versionado

**Não avance para a Entrega B com o Checkpoint A vermelho.** O ponto do fatiamento é saber, ao
entrar em B, que nada do que quebrar veio do toolchain.

---

# ENTREGA B — requests → httpx

## T-7 — Trocar as dependências de HTTP e de mock
- **Arquivos:** `pyproject.toml`, `uv.lock`
- **Depende de:** Checkpoint A
- **Cobre:** RF-16, RNF-5
- **Detalhe:** sai `requests`, entra `httpx` como **única** dependência de runtime; sai
  `requests-mock`, entra `pytest-httpx` em dev.
- **Pronto quando:** `uv sync` completa e `uv run python -c "import requests"` falha com
  `ModuleNotFoundError` no ambiente do projeto.
- [x] feito

## T-8 — Reescrever `KanbanizeSession` com composição
- **Arquivos:** `kanbanize_sdk/wrapper.py`
- **Depende de:** T-7
- **Cobre:** RF-5, RF-6, RF-7, RF-15
- **Detalhe:** a classe deixa de herdar e passa a guardar um `httpx.Client` privado, construído
  com a URL base e os headers fixos (`Content-Type: application/json`, `apikey`). Expõe
  `get`, `post`, `put`, `patch`, `delete` com as mesmas assinaturas de hoje, e mantém
  `DefaultOptions` e as properties `uri` e `api_key`. Os imports não usados
  (`RequestException`, `CaseInsensitiveDict`, hoje em `wrapper.py:5-6`) somem. **Não** chamar
  `raise_for_status()` — o middleware é quem decide o que é erro.
- **Pronto quando:** `grep -rn "requests" kanbanize_sdk/` não retorna nada, e
  `httpx.Client not in KanbanizeSession.__mro__` é verdadeiro.
- [x] feito

## T-9 — Portar o middleware de resposta
- **Arquivos:** `kanbanize_sdk/wrapper.py`
- **Depende de:** T-8
- **Cobre:** RF-8, RF-9
- **Detalhe:** a tabela de status → retorno é portada sem alteração de comportamento: 200 sem
  `pagination` devolve `data`; 200 com `pagination` promove as chaves ao topo e preserva `data`
  dentro; 204 devolve `None`; 400/401/403/404/409/429 levantam `ValueError` com o `error` do
  corpo; 500/503 levantam `ValueError` com a mensagem fixa; qualquer outro status levanta com a
  mensagem genérica.
- **Pronto quando:** T-10 verde.
- [x] feito

## T-10 — Criar `tests/test_wrapper.py`
- **Arquivos:** `tests/test_wrapper.py` (criar)
- **Depende de:** T-9
- **Cobre:** RF-6, RF-7, RF-8, RF-9, RF-15
- **Detalhe:** um teste por faixa de status da tabela, mais um de headers, mais um de
  construtor/properties, mais um que afirma que `httpx.Client` não está no `__mro__`. Marker
  novo `wrapper`, declarado em `pyproject.toml`. É o primeiro teste do caminho de erro que o
  projeto tem.
- **Pronto quando:** `uv run pytest -m wrapper -vv` passa, e
  `--cov-report=term-missing` mostra `wrapper.py` sem linhas faltando no bloco de erro.
- [x] feito

## T-11 — Resolver o portão de D-4 (`data=` vs `json=`)
- **Arquivos:** `kanbanize_sdk/endpoints/*.py` (só se o portão abrir)
- **Depende de:** T-10
- **Cobre:** RF-14
- **Detalhe:** **tarefa bloqueada por verificação humana.** Perguntar ao mantenedor se ele
  verificou contra a API real qual codificação de corpo a Kanbanize aceita.
  - Verificou e confirmou JSON → padronizar todos os métodos de escrita em `json=`, com teste
    que inspecione o corpo enviado.
  - Não verificou, ou a API espera form-urlencoded → **marcar esta tarefa como fora de escopo**,
    preservar `data=`/`json=` exatamente como estão, e registrar a pendência.
  O executor **não decide isto sozinho** e **não faz chamada real** para descobrir.
- **Pronto quando:** a decisão está registrada no corpo do commit, com o caminho escolhido e o
  porquê.
- **RESULTADO: fora de escopo.** O mantenedor não verificou contra a API real qual codificação
  de corpo a Kanbanize aceita, e o agente não pode verificar. Pela regra do portão em
  `spec.md`, RF-14 sai do escopo: `data=` e `json=` foram preservados exatamente como estavam.
  Nenhum arquivo de `endpoints/` foi tocado.
- [x] feito (como fora de escopo)

## T-12 — Converter os 29 arquivos de teste para `pytest-httpx`
- **Arquivos:** `tests/test_*.py`
- **Depende de:** T-10
- **Cobre:** RF-10, RNF-3, RNF-4
- **Detalhe:** trocar a fixture `requests_mock` por `httpx_mock`, preservando URL absoluta,
  JSON esperado, marker e credenciais fictícias. **Converter por grupo**, com a suíte verde
  entre grupos: (1) users, teams, workspaces e derivados; (2) boards e núcleo; (3) configuração
  de board; (4) estrutura de board. Não converter os 29 de uma vez.
- **Pronto quando:** `uv run pytest -q` → **≥ 109 passed** e cobertura ≥ 99%.
- [x] feito

## T-13 — Registrar o ADR de composição sobre herança
- **Arquivos:** `specs/arquitetura/adr/0001-*.md`
- **Depende de:** T-8
- **Cobre:** — (exigência de `governanca/01-constituicao.md`, princípio 4)
- **Detalhe:** rodar a skill `spec-adr`. A decisão é D-2: `KanbanizeSession` compõe em vez de
  herdar. A alternativa descartada — herdar `httpx.Client` — é plausível e precisa constar.
- **Pronto quando:** o ADR existe com status `aceito` e está linkado em
  `arquitetura/VISAO_TECNICA.md`.
- [x] feito

## T-14 [P] — Atualizar docs e specs que citam `poetry` e `requests`
- **Arquivos:** `README.md`, `specs/governanca/02-convencoes.md`, `specs/testes/ESTRATEGIA.md`,
  `specs/arquitetura/VISAO_TECNICA.md`, `CLAUDE.md`
- **Depende de:** T-12
- **Cobre:** RF-13
- **Detalhe:** todos listam comandos `poetry run ...` que deixam de existir, e a visão técnica
  afirma que `wrapper.py` é "a única fronteira com `requests`". Corrigir também a exigência de
  Python no README.
- **Pronto quando:** `grep -rn "poetry" README.md CLAUDE.md specs/` só retorna menções
  históricas explicitamente marcadas como tal.
- [x] feito

---

## Checkpoint B

Após T-14:

- `uv run pytest --cov=kanbanize_sdk --cov-report=term-missing -q` → ≥ 109 passed, cobertura ≥ 99%
- `grep -rn "requests" kanbanize_sdk/` → vazio
- Diff de `kanbanize_sdk/__init__.py` e `endpoints/__init__.py` → vazio (RNF-1)
- Diff de `kanbanize_sdk/endpoints/*.py` → vazio, **exceto** se o portão de D-4 abriu (T-11)
- Diff de `kanbanize_sdk/client.py`, `dataclasses.py`, `utils.py` → vazio
- CI verde, RTD verde

## Cobertura dos requisitos

| RF | Tarefa |
|---|---|
| RF-1, RF-2, RF-3 | T-1, T-2 |
| RF-4 | T-3, T-4 |
| RF-5 | T-8 |
| RF-6, RF-7 | T-8, T-10 |
| RF-8, RF-9 | T-9, T-10 |
| RF-10 | T-12 |
| RF-11 | T-5 |
| RF-12 | T-6 |
| RF-13 | T-14 |
| RF-14 | T-11 (condicional) |
| RF-15 | T-8, T-10 |
| RF-16 | T-7 |
| RF-17 | T-1 |

Todos os 17 RFs cobertos.

## Ao concluir todas

Rode a skill `spec-fechar`. Não marque a mudança como concluída manualmente.

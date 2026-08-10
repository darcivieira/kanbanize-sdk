# Definition of Done — 001, verificado em 2026-08-10

Percorrido item a item de `specs/governanca/04-definition-of-done.md` contra o código
mergeado em `main` (PR #6, merge `62e0bd1`). O checklist de origem é reutilizável e fica
desmarcado; este arquivo é o registro desta mudança.

Legenda: ☑ verificado · ☐ **não** verificado · ➖ não se aplica

## Sempre

- ☑ Comportamento bate com `spec.md` — 16 dos 17 RFs verificados por execução; ver tabela no
  fechamento
- ☑ Nenhum requisito sem implementação ou sem justificativa — RF-14 saiu por regra do portão
  de D-4, registrado em `spec.md` e em `tasks.md`
- ☑ Spec de estado atualizada — `arquitetura/VISAO_TECNICA.md`, `visao/PRODUTO.md`,
  `visao/GLOSSARIO.md`, `visao/ROADMAP.md`, `governanca/01·02·03·04·05`,
  `testes/ESTRATEGIA.md`, `modulos/boards.md`, `modulos/users.md`
- ➖ Lint e type-check — **não existem neste projeto**. Não foram rodados e não foram fingidos
- ☑ Testes passam — 124 passed; `tests/test_wrapper.py` cobre os critérios de aceite de RF-6
  a RF-9 e RF-15
- ☑ Sem `TODO`, código morto ou comentado — o `send()` comentado em `wrapper.py` foi removido;
  varredura por `TODO|FIXME|XXX` não retorna nada
- ☑ Sem segredo ou dado real — só `teste`/`teste_key` e `test`/`token`; nenhum subdomínio real
- ☑ Erros tratados com contexto — nenhum `except:` nem `except ...: pass` no pacote. O
  middleware propaga `ValueError`, incluindo o defeito preservado de `500`/`503`
- ☑ Decisão não-óbvia registrada como ADR — 0001, 0002 e 0003

## Biblioteca cliente HTTP

- ➖ Path, verbo e nomes de campo contra a documentação — **nenhum contrato de API foi tocado**.
  Os ~130 métodos e seus paths estão byte a byte iguais
- ➖ Método novo com type hints e docstring — nenhum método público de recurso foi criado. Os
  seis métodos verbais de `KanbanizeSession` mantêm os type hints e seguem **sem docstring**,
  como já era antes desta mudança
- ➖ Payload aceita dataclass ou `dict` — nenhum método de escrita foi alterado
- ➖ Método herdado desligado com `utils.private` — nenhum recurso novo
- ☑ Nenhuma importação de `httpx` fora de `wrapper.py` — verificado por varredura
- ☑ Nenhum símbolo público renomeado ou removido **sem ADR** — a remoção dos métodos herdados
  de `requests.Session` está coberta pelo ADR 0001 e por RNF-6. Diff vazio em
  `kanbanize_sdk/__init__.py` e `endpoints/__init__.py`
- ➖ Recurso novo exportado / fabricado — nenhum recurso novo
- ➖ Dataclass nova exportada — nenhuma dataclass nova
- ➖ `docs/api/<recurso>.md` — nenhum recurso novo
- ☑ Teste com `pytest-httpx` e marker declarado — 124 testes na fixture nova; marker `wrapper`
  acrescentado a `pyproject.toml`, totalizando 30
- ☑ Nenhum subdomínio ou api_key real

## Gates de qualidade

- ☑ `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` passa com **124 testes** —
  local e no CI (run `31389978560`, Python 3.13.15)
- ☑ Cobertura **99%**, acima da meta de 95%
- ☑ Nenhum teste acessa a rede real — toda a suíte usa `httpx_mock`

## Itens que ficaram por verificar

- ☐ **Build do Read the Docs.** A configuração está correta e o `mkdocs build` local é verde,
  mas o job do RTD com uv nunca foi executado — não é coberto pelo `pipeline.yml`. Este é o
  único item do DoD que o fechamento **não** consegue afirmar.

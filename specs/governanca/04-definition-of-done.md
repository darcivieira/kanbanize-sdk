# Definition of Done

Uma tarefa só está pronta quando **todos** os itens aplicáveis estão marcados.
Declarar concluído com item pendente é violação — sinalize o que falta.

## Sempre

- [ ] Comportamento bate com o que está em `mudancas/NNN/spec.md`
- [ ] Nenhum requisito da spec ficou sem implementação nem sem justificativa registrada
- [ ] Spec de estado atualizada (`modulos/`, `ui/`, `dados/`) — checklists marcados
- [ ] Lint e type-check passam
- [ ] Testes passam; testes novos cobrem os critérios de aceite da spec
- [ ] Sem `TODO`, código morto ou comentado deixado para trás
- [ ] Sem segredo, credencial ou dado real em código, teste ou log
- [ ] Erros tratados com contexto; nada de falha silenciosa
- [ ] Decisão não-óbvia registrada como ADR

## Biblioteca cliente HTTP (quando aplicável)

Este projeto não tem backend nem frontend — é uma lib. Os gates abaixo substituem os
tradicionais de servidor e de UI.

- [ ] Path, verbo HTTP e nomes de campo conferidos contra o trecho de documentação **fornecido
      pelo humano** — nunca inferidos por analogia, convenção REST ou memória. O agente não
      acessa o OpenAPI da conta (ver `03-limites-agente.md`)
- [ ] Método novo tem type hints completos e docstring no padrão `Parameters:` / `Returns:`
- [ ] Payload aceita tanto a dataclass quanto `dict` cru, no padrão
      `body.to_dict() if isinstance(body, X) else body`
- [ ] Método herdado que não se aplica foi desligado com `utils.private`, não sobrescrito vazio
- [ ] Nenhuma importação de `httpx` fora de `wrapper.py`
- [ ] Nenhum símbolo público renomeado ou removido sem ADR — o pacote está no PyPI
- [ ] Recurso novo exportado em `endpoints/__init__.py`, `kanbanize_sdk/__init__.py`
      **e** fabricado em `client.py`
- [ ] Dataclass nova exportada em `kanbanize_sdk/__init__.py`
- [ ] `docs/api/<recurso>.md` criado com a diretiva `::: endpoints.<recurso>`
- [ ] Teste com `pytest-httpx` cobrindo cada método novo, com o marker `@mark.<recurso>`
      declarado em `pyproject.toml`
- [ ] Nenhum subdomínio ou api_key real em código, teste, docstring ou fixture

## Gates de qualidade

- [ ] `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` passa, com **124
      testes ou mais** — a suíte nunca encolhe
- [ ] Cobertura ≥ **95%**. Ver `testes/ESTRATEGIA.md` para o que a métrica esconde
- [ ] Nenhum teste novo acessa a rede real

Gates que **não existem** hoje e que o agente não deve fingir ter rodado: lint, type-check,
budget de tamanho, verificação de segurança automatizada. Adotá-los é 🔴 RED — ver o
`[PRECISA DECISÃO]` em `02-convencoes.md`.

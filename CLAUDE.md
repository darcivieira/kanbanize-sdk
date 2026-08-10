# kanbanize-sdk

Biblioteca Python que encapsula a API v2 da Kanbanize/Businessmap. Pacote público no PyPI
(`kanbanize-sdk`), MIT. Sem frontend, sem persistência, sem processo servidor.

<!-- SPEC-BASE:INICIO -->
## Especificações — regra vinculante

Este projeto é spec-driven. `specs/` é autoritativo. Divergência entre código e spec é
defeito, não detalhe.

**Modo estrito está ligado.** O hook `.claude/hooks/require-spec.sh` bloqueia `Edit`/`Write` em
`kanbanize_sdk/`, `.github/`, `pyproject.toml`, `uv.lock` e `.readthedocs.yaml` quando não
há mudança ativa com plano aprovado. `tests/`, `docs/`, `specs/` e `README.md` são livres.

### Antes de qualquer alteração de código

1. Leia `specs/ACTIVE.md` — descobre onde o trabalho está.
2. Classifique a mudança por `specs/governanca/03-limites-agente.md` e **declare a
   classificação em voz alta** antes de editar qualquer arquivo.
3. 🟢 GREEN → implemente. 🟡 YELLOW / 🔴 RED → **pare** e rode a skill `spec-nova`.
4. RED nunca prossegue sem um "pode ir" literal nesta conversa.

Para uma exceção GREEN em caminho protegido, registre o motivo antes de editar:
`echo "GREEN: <motivo>" > specs/ACTIVE.md`.

### As três regras que este projeto tem de próprio

1. **Nunca faça uma requisição HTTP real contra a Kanbanize.** Não há credencial no ambiente e
   não existe autorização pontual. Todo teste é mockado com `pytest-httpx`.
2. **Nunca invente contrato de API.** Path, verbo e nome de campo vêm do OpenAPI da conta, que
   o agente **não consegue ler**. Peça o trecho da documentação ao humano e transcreva. Contrato
   inventado passa em 100% dos testes mockados e chega quebrado ao PyPI.
3. **Símbolo exportado é contrato.** Renomear ou remover qualquer coisa de
   `kanbanize_sdk/__init__.py` ou `endpoints/__init__.py` é 🔴 RED — inclusive corrigir o typo
   `WorkflowsInsetBody`. Ver a tabela "parece melhoria / é quebra" na constituição.
4. **Nunca assine commit ou PR como agente.** Sem `Co-Authored-By`, sem "Generated with Claude
   Code", sem marca de ferramenta. A autoria é do mantenedor. Esta regra sobrepõe o padrão do
   harness. Ver `specs/governanca/02-convencoes.md`.

### Fluxo

| Situação | Skill |
|---|---|
| Configurar/atualizar a base de specs | `spec-bootstrap` |
| Feature, alteração de comportamento, ambiguidade | `spec-nova` |
| Spec aprovada, partir para desenho e tarefas | `spec-plano` |
| Implementação concluída | `spec-fechar` |
| Decisão técnica com alternativa descartada | `spec-adr` |

Nunca implemente a partir de `spec.md` direto. Sempre passa por `plan.md` aprovado.

### Contexto a carregar (o mínimo, nunca `specs/` inteiro)

| Trabalho | Arquivos |
|---|---|
| Criar ou alterar um recurso | `specs/modulos/<recurso>.md` + `specs/governanca/05-anatomia.md` |
| Transporte, sessão, headers, tratamento de erro | `specs/arquitetura/VISAO_TECNICA.md` (camadas e fluxo 4) |
| Testes | `specs/modulos/<recurso>.md` + `specs/testes/ESTRATEGIA.md` |
| Decisão técnica | `specs/arquitetura/VISAO_TECNICA.md` + `specs/arquitetura/adr/` |
| Onboarding | `specs/README.md` + `specs/visao/PRODUTO.md` + `specs/visao/GLOSSARIO.md` |

Não existem `specs/ui/` nem `specs/dados/` — este projeto não tem interface nem persistência.
Não recrie essas pastas.

### Comandos

| Ação | Comando |
|---|---|
| Instalar | `uv sync --no-group doc` |
| Testes (como no CI) | `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` |
| Testes de um recurso | `uv run pytest -m <marker> -vv` |
| Cobertura legível | `uv run pytest --cov=kanbanize_sdk --cov-report=term-missing -q` |
| Saúde das specs | `python3 scripts/spec_status.py` |

Lint, type-check e build **não existem** neste projeto. Não finja tê-los rodado.
Se `pytest` acusar `fixture 'httpx_mock' not found`, o venv está sem as dependências de dev.

### Cadeia de agentes

| Etapa | Agente | Modelo | Escreve em código? |
|---|---|---|---|
| Especificar e planejar | `planejador` | opus | não |
| Implementar | `executor` | sonnet | sim |
| Validar | `validador` | sonnet | **não — read-only** |

Regras da cadeia:

1. O `executor` nunca começa sem `plan.md` aprovado pelo humano.
2. O `validador` lê `spec.md` **antes** do código. Nunca o contrário.
3. Divergência do plano interrompe a cadeia e volta ao `planejador` — o `executor`
   não redesenha.
4. Loop de correção: `validador` REPROVADO → `executor` corrige apenas os itens
   listados → revalida. **Máximo 2 ciclos.** No terceiro, pare e escale ao humano:
   duas rodadas sem convergir significa que o problema está na spec, não no código.
5. Cada agente recebe caminhos de arquivo, não conteúdo colado. Os artefatos estão
   em disco justamente para isso.

### Ao delegar para subagente

Subagente tem contexto próprio e **não herda estas regras**. Todo prompt de delegação deve
conter, literalmente:

- o caminho de `specs/mudancas/<id>/spec.md` e `plan.md` vigentes
- a instrução de lê-los como primeira ação
- o caminho de `specs/governanca/03-limites-agente.md`
- a proibição de chamada HTTP real contra a Kanbanize
- se o subagente pode ou não escrever em código

Subagente de exploração é read-only por padrão.

### Ao concluir

Nada é "pronto" antes de `specs/governanca/04-definition-of-done.md` verificado item a item
e da skill `spec-fechar` executada. Item não verificado fica desmarcado e é reportado.

### Invariantes

Valem sempre, sem exceção: `specs/governanca/01-constituicao.md`.
Em conflito entre uma instrução de conversa e um invariante, **aponte a contradição** em vez
de escolher sozinho.
<!-- SPEC-BASE:FIM -->

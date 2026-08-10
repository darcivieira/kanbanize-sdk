# Convenções

## Propriedade de fatos (regra anti-divergência)

Cada fato tem **exatamente um dono**. Os demais arquivos referenciam por nome, nunca copiam.

| Fato | Dono | Os outros fazem |
|---|---|---|
| Métodos de um recurso, verbo HTTP e path | `modulos/<recurso>.md` | linkam o módulo |
| Campos de uma dataclass de params/body | `modulos/<recurso>.md` | citam o nome da dataclass |
| Comportamento da sessão, headers, tratamento de status | `arquitetura/VISAO_TECNICA.md` | linkam a seção |
| Camadas e regras de dependência | `arquitetura/VISAO_TECNICA.md` | linkam a seção |
| Decisão técnica e seu trade-off | `arquitetura/adr/NNNN-*.md` | linkam o ADR |
| Termo de domínio | `visao/GLOSSARIO.md` | usam o termo |
| Comandos do projeto | este arquivo | usam o comando |

Se você precisou copiar um fato para outro arquivo, a estrutura está errada — divida ou linke.

Não existem `ui/` nem `dados/` neste projeto. Ver `specs/README.md`.

## Nomenclatura

### De specs

- Specs em português; **identificadores de código em inglês**.
- Arquivo de módulo = nome do recurso em `kebab-case`: `modulos/board-custom-fields.md`.
- ADR: `NNNN-slug-curto.md`, numeração sequencial que nunca é reaproveitada.
- Mudança: `mudancas/NNN-slug/`, `NNN` com 3 dígitos.

### De código

| Elemento | Padrão | Exemplo real |
|---|---|---|
| Arquivo de recurso | `snake_case.py` | `board_custom_field_allowed_values.py` |
| Classe de recurso | `PascalCase`, casando 1:1 com o arquivo | `BoardCustomFieldAllowedValues` |
| Método | `snake_case` | `get_effective_settings` |
| Dataclass de listagem | `<Recurso>ListParams` | `BoardsListParams` |
| Dataclass de escrita | `<Recurso>InsertBody` / `<Recurso>UpdateBody` | `ColumnsUpdateBody` |
| Path do recurso | atributo de classe `endpoint = '/<path>'` | `endpoint = '/boards'` |
| Campo que colide com palavra reservada | prefixo `_`, removido por `to_dict()` | `_from` → `from`, `_type` → `type` |
| Marker de teste | `@mark.<recurso_snake>`, declarado em `pyproject.toml` | `@mark.board_card_types` |

**Sufixos obrigatórios:** `ListParams`, `InsertBody`, `UpdateBody`. Não invente `Payload`,
`Request`, `DTO` ou `Schema`.

**`WorkflowsInsetBody`** é typo histórico em símbolo público. Não corrija — é quebra de
contrato 🔴. Ver `visao/ROADMAP.md`.

### Imports

- **Sempre absolutos**, a partir da raiz do pacote:
  `from kanbanize_sdk.endpoints.generics import GenericRequestMethod`.
  Imports relativos (`from .endpoints import ...`) não são o padrão. `client.py` ainda os usa
  por herança histórica; converter é mecânico e vale como GREEN quando o arquivo for tocado.
- Ordem: stdlib → terceiros → `kanbanize_sdk`. Estilo `isort` com `profile = "black"`,
  `line_length = 120`, `known_first_party = ["kanbanize_sdk"]`.
- `httpx` só pode ser importado em `kanbanize_sdk/wrapper.py`.

[PRECISA DECISÃO] O `isort` está nas dependências de dev mas **não tem seção de configuração em
`pyproject.toml` e não roda em lugar nenhum**. Adotar a config acima e ligar um passo no CI é
uma mudança de toolchain — precisa de decisão e ADR, não acontece de surpresa.

## Layout de diretórios

Mapa "onde-vai-o-X". Um recurso novo toca **sete** lugares — nenhum é opcional:

- Recurso novo da API → `kanbanize_sdk/endpoints/<recurso_snake>.py`
- Params e body do recurso → `kanbanize_sdk/dataclasses.py` (arquivo único)
- Export da classe de recurso → `kanbanize_sdk/endpoints/__init__.py`
- Export público (classe + dataclasses) → `kanbanize_sdk/__init__.py`
- Método-fábrica do recurso → `kanbanize_sdk/client.py`
- Teste → `tests/test_<recurso_snake>.py` **+** marker em `[tool.pytest.ini_options]` de
  `pyproject.toml`
- Página de doc → `docs/api/<recurso_snake>.md`, com a única linha
  `::: endpoints.<recurso_snake>`

E, fora dessa lista:

- Qualquer coisa de HTTP (URL, header, status, sessão) → `kanbanize_sdk/wrapper.py`, **só lá**
- Helper sem dependência de projeto → `kanbanize_sdk/utils.py`

`dataclasses.py` é arquivo único com 443 linhas e cresce a cada recurso. Fica assim por
decisão — dividir em `dataclasses/<recurso>.py` mudaria o caminho de import dos 36 símbolos
públicos e é 🔴 RED.

## Comandos do projeto

O agente vai usar exatamente estes. Onde diz "não existe", **não invente um**.

| Ação | Comando |
|---|---|
| Instalar (dev/teste) | `uv sync --no-group doc` |
| Instalar (docs) | `uv sync --only-group doc` |
| Instalar (consumo) | `pip install kanbanize-sdk` |
| Rodar (dev) | não se aplica — é biblioteca, não há processo para subir |
| Testes (suíte completa, como no CI) | `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` |
| Testes de um recurso | `uv run pytest -m <marker> -vv` |
| Teste isolado | `uv run pytest tests/test_<recurso>.py::<nome_do_teste> -vv` |
| Lint | **não existe hoje.** `isort` está instalado, sem config e sem invocação |
| Type-check | **não existe hoje.** `mypy` não é dependência |
| Build | `uv build` — não referenciado em nenhum workflow, mas é o comando do toolchain |
| Publicar | **manual hoje**, feito fora do repositório. <<PREENCHER: comando exato usado pelo mantenedor>>. Converter para CI está no `visao/ROADMAP.md` |
| Migrations | não se aplica — sem persistência |
| Docs | build automática no Read the Docs via `.readthedocs.yaml`. Sem comando local declarado |

## Commits e branches

**Conventional Commits, em inglês**, a partir de agora:

```
<tipo>(<escopo>): <descrição no imperativo, minúscula, sem ponto final>
```

- **Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`.
- **Escopo:** o recurso ou camada tocada — `boards`, `wrapper`, `dataclasses`, `client`, `docs`,
  `ci`. Opcional quando a mudança é transversal.
- **Quebra de contrato público** (renomear/remover símbolo exportado, mudar assinatura, subir
  Python mínimo): `!` após o escopo **e** rodapé `BREAKING CHANGE:`. O pacote está no PyPI —
  esta regra não é cosmética.
- Mudança que pulou a spec por decisão do humano leva `[spec-skip]` e o motivo no corpo.

O histórico anterior a esta convenção **não** a segue (`Updating data and users` ×11,
`Edinting the default documentation` ×30). Não reescreva histórico — reescrita é 🔴 RED.

**Branches:** `snake_case` descritivo, como no histórico (`new_boards_endpoints`, `workspaces`).
Merge em `main` via pull request.

## Idioma de artefatos

| Artefato | Idioma |
|---|---|
| Specs, ADRs, comentários de decisão | Português |
| Código, nomes, docstrings, mensagens de erro | Inglês |
| Mensagens visíveis ao usuário final | Inglês — aqui o "usuário final" é o dev consumidor, e o que ele vê é o argumento do `ValueError`, que vem da própria API |
| Mensagens de commit | Inglês |
| README, `docs/` | Inglês |

## Estilo de docstring

Padrão vigente em `endpoints/` — mantenha-o, não introduza reST nem NumPy style:

```python
"""
This method is responsible to list all boards in the platform.

Parameters:
    params: It's a dataclass object that provides all possible parameters to list the boards.

Returns:
    An array of objects that represents the boards
"""
```

As dataclasses hoje têm o placeholder literal `"""Set here a documentation"""`. Isso é dívida
conhecida, **não** conserto de surpresa — ver `01-constituicao.md`.

# Estratégia de testes

## Pirâmide deste projeto

Não há pirâmide: **existe um único nível, o unitário.** Isso é decisão, não omissão.

Chamada HTTP real contra a Kanbanize é **proibida** (`governanca/03-limites-agente.md`), e não
há banco, processo ou interface para integrar. Todo teste mocka o transporte com
`pytest-httpx` e verifica o que o SDK monta e o que ele devolve.

| Nível | Cobre | Não cobre | Ferramenta |
|---|---|---|---|
| Unidade | Verbo HTTP, path montado, conversão de dataclass em payload, desembrulho da resposta, tratamento de erro do middleware | Nada além disso | `pytest` + `pytest-httpx` |
| Integração | **não existe** | — | — |
| Ponta a ponta | **não existe** | — | — |

### O que deliberadamente não se testa

- **A API real da Kanbanize.** Proibido. A divergência de contrato é detectada por relato de
  quem usa a lib, não pela suíte — ver `arquitetura/VISAO_TECNICA.md`.
- **O comportamento interno de `requests`.** É dependência madura; testá-la é testar terceiro.
- **Os corpos no-op de `GenericRequestMethod`.** São stubs abstratos sem comportamento.

**Consequência que precisa estar dita:** a suíte verde **não** prova que o SDK conversa
corretamente com a Kanbanize. Prova apenas que ele faz o que o próprio teste descreveu. Um
path errado passa em 100% dos testes.

## Regras

- Todo critério de aceite de `mudancas/NNN/spec.md` vira ao menos um teste.
- Bug corrigido ganha teste que falha antes da correção. Sem exceção.
- Teste não acessa rede nem serviço externo real — use dublê.
- Teste não depende de ordem de execução nem de estado de outro teste.
- Nome do teste descreve o comportamento esperado, não o método chamado.
- **Um arquivo de teste por recurso**: `tests/test_<recurso_snake>.py`.
- **Todo teste leva o marker do recurso** (`@mark.<recurso_snake>`), e o marker é declarado em
  `[tool.pytest.ini_options]` de `pyproject.toml`. Marker não declarado gera warning e some do
  filtro — é falha silenciosa.
- **Nenhum subdomínio ou api_key real** em teste, fixture ou docstring. O padrão vigente é o
  par fictício `subdomain='teste'`, `api_key='teste_key'`.

## Dados de teste

Não há fixtures compartilhadas, factories nem `conftest.py`. Cada teste declara seu próprio
JSON literal e registra a rota mockada no corpo do próprio teste:

```python
@mark.boards
def test_list_boards(httpx_mock):
    test_json = {'data': [...]}
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().list() == test_json.get('data')
```

Isso é verboso de propósito: o JSON esperado fica ao lado da asserção, sem indireção. Mantenha
o padrão — não introduza `conftest.py` nem factory sem spec de mudança.

**Dados sensíveis: nunca reais.** Não existe conta de teste, api_key de teste nem subdomínio
real neste ambiente. Se você encontrar algo que pareça credencial, pare e avise.

## Comandos

| Ação | Comando |
|---|---|
| Suíte completa, como no CI | `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` |
| Suíte com cobertura legível no terminal | `uv run pytest --cov=kanbanize_sdk --cov-report=term-missing -q` |
| Só um recurso | `uv run pytest -m <marker> -vv` |
| Um teste isolado | `uv run pytest tests/test_<recurso>.py::<nome_do_teste> -vv` |

Se `pytest` acusar `fixture 'httpx_mock' not found`, o venv está sem as dependências de dev.
Rode `uv sync --no-group doc` antes de concluir que a suíte quebrou.

## Cobertura

- **Meta: 95%.** Abaixo disso, reprova.
- **O CI bloqueia.** [PRECISA DECISÃO] O gate ainda **não está configurado**: não existe
  `fail_under` em `pyproject.toml` nem `codecov.yml` no repositório. Hoje a cobertura é medida
  e enviada ao Codecov, mas nada impede o merge. Ligar o gate é mudança de CI — 🔴 RED, entra
  junto com a migração de toolchain.
- **Nada é excluído da métrica** — a medição é sobre `kanbanize_sdk/` inteiro.

### Medição real em 2026-08-07, após a mudança 001

`124 passed`, **99% de cobertura de linha** (786 statements, 3 não cobertos), em Python
3.13.11 local.

A contagem de statements não é comparável com medições anteriores a 2026-08-07: o `coverage`
subiu de 7.5.3 para 7.15.4 e passou a contar corpos `...` e anotações de classe de outro modo.

O número engana: os módulos de endpoint são uma linha por método, então a cobertura alta vem
da parte trivial. O que **não** está coberto é a única parte com lógica de verdade.

| Não coberto | Linhas | Por quê importa |
|---|---|---|
| `utils.py` | 4 | O `private` nunca é acionado — nada garante que método desligado levante `AttributeError` |
| `client.py` | 125 | A fábrica `board_child_parent_cards()` — coerente com a classe estar vazia |
| — | — | `wrapper.py` passou a **100%** com `tests/test_wrapper.py`, criado na mudança 001 |
| `endpoints/workspace_managers.py` | 21 | O `list()` de gerentes de workspace não tem teste |
| `endpoints/generics.py` | 13, 16, 19, 22, 25 | Corpos no-op da ABC — aceitável, ver "não se testa" |

As três primeiras são **lacuna a fechar**, não decisão. Estão no `visao/ROADMAP.md`.
O middleware de erro, que era a maior delas, foi fechado na mudança 001.

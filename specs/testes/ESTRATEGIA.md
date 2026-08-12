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
- **O comportamento interno de `httpx`.** É dependência madura; testá-la é testar terceiro.
- **Os corpos no-op de `GenericRequestMethod`.** São stubs abstratos sem comportamento.

**Consequência que precisa estar dita:** a suíte verde **não** prova que o SDK conversa
corretamente com a Kanbanize. Prova apenas que ele faz o que o próprio teste descreveu. Um
path errado passa em 100% dos testes.

Isso é **decisão, não lacuna** — ver ADR 0006. A documentação oficial é o contrato de
referência, e um método transcrito fielmente dela está correto por definição. O que a suíte
não cobre, e nenhuma suíte cobrirá enquanto chamada real for proibida, é se a **transcrição**
foi fiel. O controle disso é registrar o trecho de documentação de cada recurso em
`specs/modulos/<recurso>.md`. Recurso sem esse registro é recurso sem contrato auditável.

## Regras

- Todo critério de aceite de `mudancas/NNN/spec.md` vira ao menos um teste.
- Bug corrigido ganha teste que falha antes da correção. Sem exceção.
- Teste não acessa rede nem serviço externo real — use dublê.
- Teste não depende de ordem de execução nem de estado de outro teste.
- Nome do teste descreve o comportamento esperado, não o método chamado.
- **Um arquivo de teste por recurso**: `tests/test_<recurso_snake>.py`.
- **Todo teste leva o marker do recurso** (`@mark.<recurso_snake>`), e o marker é declarado em
  `[tool.pytest.ini_options]` de `pyproject.toml`. São 30 markers: 29 de recurso mais
  `wrapper`, que cobre a camada de transporte. Marker não declarado gera warning e some do
  filtro — é falha silenciosa.
- **Nenhum subdomínio ou api_key real** em teste, fixture ou docstring. O padrão vigente é o
  par fictício `subdomain='teste'`, `api_key='teste_key'`.

## Dados de teste

Cada teste declara seu próprio JSON literal e registra a rota mockada no corpo do próprio
teste. Não há factories nem fixtures de dado:

```python
@mark.boards
def test_list_boards(httpx_mock):
    test_json = {'data': [...]}
    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)
    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})
    assert service.boards().list() == test_json.get('data')
```

Isso é verboso de propósito: o JSON esperado fica ao lado da asserção, sem indireção.

**`tests/conftest.py` existe, com um limite escrito** (ver ADR 0005): ele abriga **apenas**
asserções sobre a requisição enviada, que não cabem inline. Hoje contém uma única fixture,
`assert_json_body`. Continua proibido usar `conftest.py` para fixture de dado, factory ou
construção de payload — o valor esperado fica no corpo do teste.

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

### Medição real em 2026-08-11

`200 passed`, **99% de cobertura de linha** (787 statements, **1** não coberto), em Python
3.13.11.

A contagem de statements não é comparável com medições anteriores a 2026-08-07: o `coverage`
subiu de 7.5.3 para 7.15.4 e passou a contar corpos `...` e anotações de classe de outro modo.

| Não coberto | Linha | Por quê importa |
|---|---|---|
| `client.py` | 125 | A fábrica `board_child_parent_cards()` — coerente com a classe estar vazia. É a **única** lacuna que sobra, e só fecha quando o recurso for implementado |

Todas as demais lacunas foram fechadas: o caminho de erro do `wrapper.py` na mudança 001, e
`utils.private` mais `WorkspaceManagers.list` na onda de correções GREEN de 2026-08-11.

Dois defeitos de teste apareceram nessa onda e valem como alerta de padrão:

- `test_workspace_managers.py` tinha **duas funções com o mesmo nome**; a segunda sombreava a
  primeira, que nunca rodava — e a morta era justamente o teste do `list`. Nome duplicado não
  gera erro em Python: o teste some em silêncio.
- Onze testes carregavam nome copiado do arquivo de origem (`test_get_merged_area` dentro de
  `test_board_block_reasons.py`). Nome errado manda quem lê a falha para o recurso errado.

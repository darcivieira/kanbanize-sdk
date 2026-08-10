# Anatomia — skeletons copiáveis

Estruturas canônicas deste projeto. Copie e adapte; não invente layout novo.
Se um skeleton não serve para o caso, isso é um sinal de mudança **YELLOW** — especifique antes.

Todos os trechos abaixo são **código real deste repositório**, não exemplo genérico.

## Estrutura do pacote

```
kanbanize_sdk/
├── __init__.py       # superfície pública: Kanbanize + as 36 dataclasses
├── client.py         # fachada: instancia a sessão, fabrica recursos. Sem regra, sem HTTP
├── wrapper.py        # ÚNICO ponto que fala httpx: URL base, headers, tratamento de status
├── dataclasses.py    # params e bodies, todos herdando BaseDataClasse
├── utils.py          # `private` — desliga método herdado
└── endpoints/
    ├── __init__.py   # export das 27 classes de recurso
    ├── generics.py   # GenericRequestMethod (ABC): endpoint = '' + stubs no-op
    └── <recurso>.py  # uma classe por recurso da API
```

Dependências: `endpoints/*` → `wrapper` → `httpx`. `dataclasses.py` e `utils.py` são folhas.
`client.py` importa `endpoints/*` e `wrapper`. Ver `arquitetura/VISAO_TECNICA.md`.

## Recurso

Um recurso herda de `GenericRequestMethod`, declara `endpoint` e implementa só o que a API
oferece. Extraído de `endpoints/boards.py`:

```python
from kanbanize_sdk.endpoints.generics import GenericRequestMethod
from kanbanize_sdk.dataclasses import BoardsListParams, BoardsInsertBody, BoardsUpdateBody


class Boards(GenericRequestMethod):
    """
    Class responsible to make calls to Kanbanize boards endpoints
    """
    endpoint = '/boards'

    def list(self, params: BoardsListParams | dict | None = None, **kwargs) -> list:
        """
        This method is responsible to list all board in the platform.

        Parameters:
            params: It's a dataclass object that provide all possible parameters to be used to list the boards.

        Returns:
            An array of objects that represents the boards
        """
        params = params.to_dict() if isinstance(params, BoardsListParams) else params
        return self.service.get(self.endpoint, params=params)

    def insert(self, body: BoardsInsertBody | dict) -> dict:
        payload = body.to_dict() if isinstance(body, BoardsInsertBody) else body
        return self.service.post(self.endpoint, data=payload)

    def get(self, board_id: int) -> dict:
        return self.service.get(self.endpoint + f'/{board_id}')
```

O que **não** pode variar:

- path sempre relativo, construído a partir de `self.endpoint` — nunca URL absoluta;
- toda chamada passa por `self.service`, nunca por `httpx` direto;
- todo método de escrita aceita dataclass **ou** `dict`, no padrão
  `body.to_dict() if isinstance(body, X) else body`;
- type hints completos, incluindo o retorno;
- docstring no padrão `Parameters:` / `Returns:`.

### Subrecurso por herança

Quando um recurso é filho de outro e reaproveita a base do path, herde e **desligue** o que não
existe. De `endpoints/board_settings.py`:

```python
from kanbanize_sdk.endpoints.boards import Boards
from kanbanize_sdk.utils import private


class BoardSettings(Boards):
    list = private
    insert = private
    delete = private

    def get(self, board_id: int) -> dict:
        return self.service.get(self.endpoint + f'/{board_id}/settings')
```

Desligar é `= private`. Nunca `pass`, nunca `raise NotImplementedError`, nunca corpo vazio.

## Dataclass de params / body

Em `dataclasses.py`, arquivo único. Todo campo é opcional com default `None` — `to_dict()`
remove os nulos, e prefixo `_` some no dicionário (é assim que `_from` vira `from`):

```python
@dataclass
class BoardHistoryListParams(BaseDataClasse):
    """Set here a documentation"""
    board_ids: list[int] | None = None
    user_ids: list[int] | None = None
    event_types: list[str] | None = None
    _from: str | None = None
    to: str | None = None
    page: int | None = None
    per_page: int | None = None
```

Nomes seguem `<Recurso>ListParams`, `<Recurso>InsertBody`, `<Recurso>UpdateBody`. Sem exceção.

> A docstring placeholder acima é dívida conhecida e **aberta** — ao criar dataclass nova,
> escreva uma docstring de verdade. Ver `01-constituicao.md`.

## Registro de um recurso novo — os sete pontos

Nenhum é opcional. Recurso pela metade é superfície pública quebrada.

1. `kanbanize_sdk/endpoints/<recurso_snake>.py` — a classe
2. `kanbanize_sdk/dataclasses.py` — params e bodies
3. `kanbanize_sdk/endpoints/__init__.py` — `from .<recurso_snake> import <Recurso>`
4. `kanbanize_sdk/__init__.py` — export da classe e das dataclasses
5. `kanbanize_sdk/client.py` — o método-fábrica:
   ```python
   def board_tags(self):
       return BoardTags(self.service)
   ```
6. `pyproject.toml` — o marker em `[tool.pytest.ini_options]`, **e** `tests/test_<recurso>.py`
7. `docs/api/<recurso_snake>.md` — uma linha: `::: endpoints.<recurso_snake>`

## Teste

Único nível existente. Padrão real, de `tests/test_boards.py`:

```python
from pytest import mark
from kanbanize_sdk import Kanbanize


@mark.boards
def test_list_boards(httpx_mock):
    test_json = {'data': [{'board_id': 1, 'name': 'Board One'}]}

    httpx_mock.add_response(method='GET', url='https://teste.kanbanize.com/api/v2/boards', json=test_json)

    service = Kanbanize({'subdomain': 'teste', 'api_key': 'teste_key'})

    assert service.boards().list() == test_json.get('data')
```

Regras do padrão:

- credenciais fictícias fixas: `subdomain='teste'`, `api_key='teste_key'`;
- URL do mock é a **absoluta**, com a base — é o que prova que o path foi montado certo;
- o JSON esperado fica no corpo do teste, sem `conftest.py` nem factory;
- marker do recurso sempre presente e declarado em `pyproject.toml`;
- um teste por método público.

Não há teste de integração e não haverá — chamada real é proibida. Ver `testes/ESTRATEGIA.md`.

## Não se aplica a este projeto

Sem frontend e sem persistência: não existem skeletons de tela, componente, hook de dados,
repositório, entidade ou migration. Se um pedido exigir um deles, **pare** — é mudança 🔴 RED
de escopo do produto, não tarefa de implementação.

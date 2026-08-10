# Visão técnica

Dono do fato: topologia, camadas e fluxo de execução. Decisões e seus porquês ficam em `adr/`.

Este projeto é uma **biblioteca**, não uma aplicação. Não há servidor, banco, fila nem
interface. Ler as seções abaixo com essa lente: "processo" é o processo do dev consumidor que
importa a lib.

## Stack

| Camada | Tecnologia | Versão | Observação |
|---|---|---|---|
| Runtime | Python | `>=3.13` — `.python-version` fixa 3.13 no dev, CI e Read the Docs em 3.13 | |
| Transporte HTTP | `httpx` | `>=0.27,<1.0` (lock 0.27.2) | **Única** dependência de runtime |
| Modelagem de payload | `dataclasses` da stdlib | — | Sem Pydantic, por escolha |
| Empacotamento | uv + `uv_build` | uv 0.9.x | `pyproject.toml` em PEP 621, lockfile `uv.lock` |
| Testes | `pytest`, `pytest-cov`, `pytest-httpx` | 7.4.x / 4.1.x / 0.30.x | |
| Docs | MkDocs Material + mkdocstrings | 9.4.x / 0.23.x | Build no Read the Docs |
| CI | GitHub Actions (`.github/workflows/pipeline.yml`) | — | Só testes + Codecov |
| Banco / Fila / Deploy | **não se aplica** | — | Sem persistência e sem processo servidor |

## Topologia

Um único processo: o do dev consumidor.

```
[ processo do dev consumidor ]
        │
        │ Kanbanize({'subdomain': ..., 'api_key': ...})
        ▼
   client.Kanbanize ──cria──▶ wrapper.KanbanizeSession  (compõe httpx.Client — ver ADR 0001)
        │                              │
        │ .boards() → Boards(service)  │
        ▼                              │
   endpoints.Boards ──chama──────────▶ │ HTTPS síncrono
                                       ▼
                    https://{subdomain}.kanbanize.com/api/v2
```

Tudo é **síncrono e bloqueante**. Não há thread, worker, fila, cron nem entrypoint executável
(não existe `[project.scripts]`). Uma instância de `Kanbanize` cria uma única
`KanbanizeSession`, compartilhada por todos os recursos que ela fabrica.

## Camadas e regras de dependência

Quatro camadas. A seta indica "pode importar".

```
endpoints/*.py  ──▶  wrapper.py  ──▶  httpx
      │                  ▲
      └──▶ dataclasses.py│
      └──▶ utils.py      │
                         │
client.py ──▶ endpoints/*.py ──┘ (e wrapper.py, para instanciar a sessão)
```

Regras verificáveis:

- **`wrapper.py` é a única fronteira com `httpx`.** Nenhum arquivo em `endpoints/` importa
  `httpx`, monta URL absoluta ou lê `Response`. Endpoint fala com `self.service`.
- **`KanbanizeSession` não herda de cliente de terceiro** — compõe um `httpx.Client` privado.
  Ver `adr/0001-kanbanize-session-compoe-o-cliente-http.md`.
- **`dataclasses.py` não importa nada do projeto.** É folha: só `dataclasses` e `typing`.
  Não conhece endpoint, sessão nem HTTP.
- **`utils.py` é folha.** Não importa nada.
- **Recurso não importa recurso**, exceto por **herança declarada** — `BoardSettings`,
  `BoardStructure`, `BoardStructureRevisions` e `BoardHistory` herdam de `Boards`;
  `WorkspaceManagers` e `WorkspaceHistory` herdam de `Workspaces`; `ColumnsListParams` herda de
  `LanesListParams`. Fora dessa herança, um endpoint não conhece outro.
- **Todo recurso herda de `GenericRequestMethod`** (`endpoints/generics.py`) e declara
  `endpoint = '/<recurso>'` como atributo de classe.
- **`client.py` só monta.** É fachada: instancia a sessão e fabrica recursos. Não contém regra
  nem chamada HTTP.
- **Método herdado que não se aplica é desligado com `utils.private`**, nunca sobrescrito com
  `pass`, `raise NotImplementedError` ou implementação vazia.

## Fronteira com a API da Kanbanize

O "contrato" deste projeto não é interno — é a **API v2 da Kanbanize**, externa e fora do
controle do mantenedor.

**Fonte da verdade:** o OpenAPI publicado pela própria plataforma, em
`https://{subdomain}.kanbanize.com/openapi`.

**Mecanismo de sincronia: manual, e reativo.**

- Ao construir um recurso novo, o mantenedor **lê o OpenAPI da conta** e transcreve à mão o
  path, o verbo e os campos para uma classe em `endpoints/` e dataclasses em `dataclasses.py`.
- Não há download do spec, não há codegen, não há schema versionado no repositório.
- Depois de publicado, a divergência é descoberta **por relato de não funcionamento** de quem
  consome a lib. Só então o mantenedor investiga se a API mudou.

**Consequência a assumir, não a esconder:** os 30 arquivos de teste mockam a camada HTTP com
`pytest-httpx` e afirmam que o SDK devolve o `data` do JSON que o próprio teste escreveu.
Nenhum teste toca a API real. **Se a Kanbanize alterar um endpoint, a suíte continua verde.**
A detecção de quebra de contrato é externa ao repositório.

Isto está registrado como risco aceito, não como pendência a corrigir de surpresa.

## Fluxos críticos

### 1. Autenticação

Não há fluxo de autenticação: não há login, token, refresh nem expiração.

1. O dev instancia `Kanbanize({'subdomain': ..., 'api_key': ...})`.
2. `KanbanizeSession.__init__` guarda ambos em atributos privados e monta
   `https://{subdomain}.kanbanize.com/api/v2`.
3. `KanbanizeSession.request` injeta, **em toda** requisição, os headers
   `Content-Type: application/json` e `apikey: <api_key>`.

A credencial é responsabilidade do dev consumidor. O SDK não a lê de ambiente, não a persiste
e não a registra em log.

### 2. Leitura (`list` / `get`)

1. O dev chama `service.boards().list(params)`.
2. O recurso converte a dataclass em `dict` — `params.to_dict() if isinstance(...) else params`.
   `BaseDataClasse.to_dict()` remove chaves com valor `None` e tira o `_` inicial dos nomes
   (é como `_from` e `_type` viram `from` e `type` na query).
3. O recurso chama `self.service.get(self.endpoint, params=...)` com path **relativo**.
4. `KanbanizeSession.request` prefixa a URL base e injeta headers.
5. O middleware de resposta trata o resultado (fluxo 4).

### 3. Escrita (`insert` / `update` / `delete`)

Igual ao fluxo de leitura, com duas diferenças:

- O payload vai em `data=payload`.
- O verbo varia por recurso e **não segue convenção uniforme** — `insert` é `POST` em
  `Boards`/`Teams`/`Workflows`/`Lanes`/`Columns`/`MergedAreas`, mas é **`PUT` em um id fornecido
  pelo chamador** em `BoardStickers`, `BoardCustomFields`, `BoardCustomFieldAllowedValues` e
  `BoardCardTypes`. `update` é `PATCH` na maioria, mas `PUT` em `CellLimits`,
  `LaneSectionLimits`, `BoardAssignees`, `BoardTeams`, `BoardTags` e outros. O verbo real de
  cada método é o fato registrado em `specs/modulos/`.

### 4. Tratamento de resposta — `KanbanizeSession.__middleware_response`

Ponto único de decisão. Todo retorno e todo erro do SDK passam por aqui.

| Situação | Comportamento |
|---|---|
| `204` | devolve `None` |
| `200` sem corpo útil | devolve `None` |
| `200` **com** `pagination` | funde as chaves de `pagination` no nível de topo e devolve o dict inteiro — **inclusive a chave `data`** |
| `200` sem `pagination` | devolve **só** o valor de `data` |
| `400, 401, 403, 404, 409, 429` | lê `error` do corpo e levanta `ValueError(error)` |
| `500, 503` | levanta **`ValueError(None)`** — a entrada de `status_message` não tem chave `error`, então `response.get('error')` devolve `None` e a mensagem nunca chega ao chamador. **Defeito preservado**, ver `visao/ROADMAP.md` |
| qualquer outro status | levanta `ValueError` com a mensagem genérica `status_message[0]` |

Não há hierarquia de exceção: **`ValueError` é o único tipo levantado pelo código de produção.**
Quem consome não consegue distinguir "não encontrado" de "rate limit" pelo tipo — só pelo
conteúdo do argumento.

## Ambientes

Não existem dev/homologação/produção de aplicação. Os contextos de execução reais são:

| Contexto | Como se instala | O que roda | HTTP real? |
|---|---|---|---|
| Local | `uv sync --no-group doc` | `pytest` com `pytest-httpx` | Não |
| CI — GitHub Actions | idem | `uv run pytest -s -x --cov=kanbanize_sdk -vv --cov-report=xml` + upload ao Codecov | Não |
| Read the Docs | `uv sync --only-group doc` | MkDocs Material + mkdocstrings sobre `kanbanize_sdk/` | Não |
| Consumo (PyPI) | `pip install kanbanize-sdk` | código do dev, contra um subdomínio Kanbanize real | **Sim** |

**Nenhum ambiente do repositório bate contra a API real.** O único tráfego HTTP real acontece
na máquina de quem consome a lib.

<<PREENCHER: existe um subdomínio e uma api_key de conta de teste usados manualmente pelo
mantenedor antes de publicar? Se sim, onde ficam e qual é a política de uso. Não respondido.>>

## Riscos técnicos conhecidos

Dívidas assumidas conscientemente. Nenhuma deve ser "consertada de surpresa" — ver
`governanca/01-constituicao.md`.

| Risco | Evidência | Situação |
|---|---|---|
| Suíte verde não prova compatibilidade com a API | 124/124 testes usam `pytest-httpx` | Aceito. Detecção é reativa, por relato de usuário |
| `ValueError` como exceção única | `wrapper.py:77` | Aceito. Trocar por hierarquia própria é quebra de contrato 🔴 |
| Verbo HTTP inconsistente entre `insert`/`update` de recursos diferentes | ver Fluxo 3 | Aceito. Uniformizar quebraria contrato público |
| Escrita usa `data=payload` com um `dict`, sob header `Content-Type: application/json` — **exceto `Users.insert`, que usa `json=`** | `wrapper.py:29`, `boards.py:37`, `users.py:44` | **Não avaliado.** `requests` codifica `dict` em `data=` como form-urlencoded, não como JSON; com `json=` codifica JSON de verdade. Os dois convivem no mesmo pacote. Os testes não detectam a diferença porque mockam o transporte. <<PREENCHER: o mantenedor precisa confirmar contra a API real qual das duas formas ela aceita, antes de isso ser tratado como defeito.>> |
| Sem lint, sem type-check, sem meta de cobertura no CI | `pipeline.yml` | Aceito hoje |
| `BoardsListParams` sem `@dataclass` — dataclass inutilizável | `dataclasses.py:124` | **Defeito confirmado.** Ver `modulos/boards.md` |
| `WorkflowsInsetBody` com typo em símbolo público | `dataclasses.py`, `__init__.py` | Corrigir é 🔴 quebra de contrato |
| `BoardChildParentCards` exportada e vazia | `endpoints/board_child_parent_cards.py` | Ver `visao/ROADMAP.md` |
| Exemplo do README usa `UserListParams` inexistente | `README.md:28`, `docs/index.md:23` | Ver `visao/ROADMAP.md` |

Nenhum ADR foi escrito ainda — `arquitetura/adr/` está vazio. As decisões acima estão
descritas aqui, mas seus **porquês** não foram registrados. Ver os 3 próximos passos ao fim do
bootstrap.

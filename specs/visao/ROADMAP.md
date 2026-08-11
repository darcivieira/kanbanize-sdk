# Roadmap

Fatias de entrega, não lista de features. Cada fase deve ser utilizável sozinha.

## Fase atual: cobertura de endpoints da API v2

Ampliar a superfície coberta pelo SDK, mantendo o contrato público estável.

| Entrega | Módulo | Estado |
|---|---|---|
| Users | `endpoints/users.py` | ☑ |
| Teams | `endpoints/teams.py` | ☑ |
| Workspaces (+ managers, history, managed) | `endpoints/workspace*.py` | ☑ |
| Boards (+ settings, structure, revisions, history) | `endpoints/board*.py` | ☑ |
| Configuração de board (tags, stickers, custom fields, card types, motivos) | `endpoints/board_*.py` | ☑ |
| Estrutura de board (workflows, lanes, columns, limites, merged areas) | `endpoints/{workflows,lanes,columns,cell_limits,merged_areas,lane_section_limits}.py` | ☑ |
| Child/parent cards | `endpoints/board_child_parent_cards.py` | ☐ classe existe vazia, sem métodos e sem teste |
| Recursos de **cards** da API v2 | — | ☐ não iniciado |

## Próxima fase: modernização de runtime e toolchain

Ordem declarada pelo mantenedor. Cada item é uma mudança 🔴 RED (troca de dependência,
de runtime ou de contrato) e exige spec + ADR antes de qualquer código.

| # | Entrega | Estado | Impacto no contrato público |
|---|---|---|---|
| 1 | Migrar runtime para **Python 3.13** | ☑ mudança 001 | Deixou de suportar 3.10–3.12 para quem instala do PyPI |
| 2 | Migrar gerenciador de pacote de **Poetry para uv** | ☑ mudança 001 | Interno — mudou CI, `.readthedocs.yaml` e os comandos de `governanca/02-convencoes.md` |
| 3 | Migrar dependência de runtime de **`requests` para `httpx`** | ☑ mudança 001 | `KanbanizeSession` deixou de herdar cliente de terceiro — ver ADR 0001 |
| 4 | Criar **modo async** | ☐ | Aditivo se convivendo com a API síncrona; ver ADR quando decidido |
| 5 | Converter a **publicação no PyPI de manual para CI** | ☑ mudança 002 | Interno — `release.yml` com Trusted Publishing, sem segredo no repositório |

O item 4 foi destravado pelo item 3: `httpx` é o que viabiliza o async sem uma segunda
dependência de runtime.

## Depois / talvez nunca

Parking lot. Registrado aqui para **não** voltar como escopo acidental:

- Retry, backoff e tratamento de rate limit (`429`) — hoje é não-objetivo declarado em
  `PRODUTO.md`. Só sai do parking lot por decisão explícita.
- Cache de resposta — conflita com o não-objetivo "não armazena dados".
- Validação local de payload — a validação é da API remota, por decisão.
- CLI ou serviço em cima da lib — o produto é biblioteca.

<<PREENCHER: outras ideias que o mantenedor queira congelar aqui.>>

## Bloqueios conhecidos

| Bloqueio | Impacto | Contorno atual |
|---|---|---|
| `WorkflowsInsetBody` — typo de "Insert" em símbolo público exportado | Corrigir o nome é quebra de contrato para quem já importa | Nenhum; usar o nome com typo |
| `LaneSectionLimits.update` aceita qualquer objeto como corpo | O `isinstance` contra a dataclass certa falha em silêncio e o objeto cru vira corpo. Um teste chegou a passar `CellLimitsUpdateBody` por engano e ficou verde com `requests` | Corrigido no teste; o endpoint continua permissivo |
| `BoardChildParentCards` é classe vazia (`...`), exportada e sem teste | Recurso anunciado na superfície pública mas inoperante. É a **única** linha sem cobertura no pacote (`client.py:125`) | Nenhum |
| `private` comentado em dois recursos | `workspace_managers.py:9` e `workspace_history.py:10-13` têm `# post= private`, `# insert = private`, `# get = private`, `# update = private`. Alguém pretendeu desligar esses métodos e nunca ativou: hoje eles estão herdados e chamáveis. Os arquivos nem importam `private` | Apagar os comentários é 🟢 GREEN; **desligar de fato os métodos muda o que consumidores podem chamar** e é mudança de contrato |
| 🔴 `500` e `503` levantam `ValueError(None)` | `wrapper.py` monta `{'code': 500, 'message': ...}` e depois lê `.get('error')` desse dict, que não tem essa chave. A mensagem nunca chega a quem consome. Confirmado por execução em 2026-08-07 e coberto por teste em `tests/test_wrapper.py`, que fixa o comportamento atual | Nenhum. Corrigir muda o que o consumidor observa — precisa de spec própria |
| `Kanbanize` sem `api_key` agora falha na construção | Com `requests`, header de valor `None` era omitido e a requisição saía sem `apikey`. O `httpx` levanta `AttributeError`. Falha cedo em vez de tarde, mas é comportamento observável diferente | Passar `api_key` — que sempre foi obrigatório na prática |
| O `pipeline.yml` não cobre o build do Read the Docs | Quebra na documentação só aparece depois do merge, olhando o site publicado. Foi assim que se verificou a mudança 001 | Conferir a página publicada após mudanças que toquem `.readthedocs.yaml`, `mkdocs.yml` ou o grupo `doc` |
| Sem lint, sem type-check e sem gate de cobertura no CI | Regressão de estilo e de tipo não é detectada; a meta de 95% de `testes/ESTRATEGIA.md` não é aplicada por ninguém | Revisão manual |
| A escrita em JSON nunca foi confirmada contra a API real | Desde a mudança 002 todas as escritas mandam JSON, e 30 testes afirmam isso. Mas os testes mockam o transporte: eles provam o que o SDK **envia**, não o que a Kanbanize **aceita** | Nenhum. Uma chamada real de escrita do mantenedor encerraria a dúvida; o agente está proibido de fazê-la |

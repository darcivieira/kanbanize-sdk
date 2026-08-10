---
id: 001-migracao-runtime-toolchain-http
titulo: Migração de runtime, gerenciador de pacotes e cliente HTTP
classificacao: 🔴 RED
status: concluida
criada: 2026-08-07
modulos: [boards, users, "+ os 25 recursos restantes, indiretamente"]
telas: []
---

# 001 — Migração de runtime, gerenciador de pacotes e cliente HTTP

Três frentes simultâneas, por decisão do mantenedor:

1. Runtime: Python 3.10 → 3.13
2. Gerenciador de pacotes: Poetry → uv
3. Cliente HTTP: `requests` → `httpx`

## Problema

O projeto está preso a um toolchain e a um runtime que o mantenedor já não usa, e a um cliente
HTTP que fecha a porta para o próximo item do roadmap.

Evidência:

- `pyproject.toml:22` declara `python = "^3.10"`; `.github/workflows/pipeline.yml` e
  `.readthedocs.yaml` fixam `3.10`. O venv local do mantenedor **já roda 3.13.11**, e os 109
  testes passam nele — o repositório descreve um ambiente que ninguém mais usa.
- O empacotamento é Poetry (`poetry.core.masonry.api`), e o mantenedor decidiu padronizar em
  uv (`visao/ROADMAP.md`, itens 1 e 2, prioridade imediata declarada).
- `requests` é síncrono e não tem contrapartida assíncrona. O modo async é o item 4 do roadmap
  e **não é alcançável** enquanto o transporte for `requests`. Trocar depois significaria
  reescrever `wrapper.py` duas vezes.

## Resultado esperado

Do ponto de vista de quem consome a lib: **nada muda na forma de chamar**. `Kanbanize(...)`,
os ~130 métodos, as 36 dataclasses e o formato de retorno continuam idênticos. O que muda é o
Python mínimo suportado.

Do ponto de vista de quem mantém: `uv sync` instala, `uv run pytest` testa, o CI roda em 3.13,
e `wrapper.py` passa a usar `httpx` — abrindo caminho para o modo async sem nova reescrita.

## Fora de escopo

Explícito, para não "aproveitar a viagem":

- **Não implementar o modo async.** Esta mudança só remove o impedimento. O async é mudança
  própria, com spec e ADR próprios.
- **Não adicionar retry, backoff nem tratamento de rate limit** — o `httpx` oferece transporte
  com retry embutido, e isso continua sendo não-objetivo (`visao/PRODUTO.md`).
- **Não trocar `ValueError` por exceções próprias**, mesmo que o `httpx` levante exceções
  diferentes de `requests`. O tipo que o SDK levanta continua `ValueError`.
- **Não mudar path, verbo HTTP ou assinatura** de nenhum dos ~130 métodos.
- **Não corrigir** `WorkflowsInsetBody`, `BoardsListParams` nem `BoardChildParentCards`.
- **Não adotar lint nem type-check** — apesar de o `isort` estar nas dependências. É decisão à
  parte — ver a decisão pendente registrada em `governanca/02-convencoes.md`.
- **Não adicionar teste do caminho de erro** além do necessário para provar equivalência de
  comportamento. Fechar aquela lacuna é trabalho próprio.
- **Não publicar no PyPI.** A publicação segue manual e fora desta mudança.

## Requisitos funcionais

| # | Requisito | Verificável por |
|---|---|---|
| RF-1 | `pyproject.toml` declara o Python mínimo como 3.13 e o classificador correspondente | leitura do arquivo |
| RF-2 | O build backend deixa de ser `poetry.core.masonry.api` e passa a ser o adotado pelo uv | leitura do `[build-system]` |
| RF-3 | As dependências de runtime, dev e doc são declaradas no formato do uv, preservando os mesmos pacotes (exceto os substituídos) | `uv sync` completa sem erro |
| RF-4 | Existe um lockfile do uv versionado, e `poetry.lock` é removido | `ls uv.lock`, ausência de `poetry.lock` |
| RF-5 | `kanbanize_sdk/wrapper.py` não importa `requests` em nenhuma linha | `grep -r requests kanbanize_sdk/` sem resultado |
| RF-6 | `KanbanizeSession` mantém o nome, o construtor `DefaultOptions` e as propriedades `uri` e `api_key` | teste que instancia e lê ambas |
| RF-7 | Toda requisição continua enviando os headers `Content-Type: application/json` e `apikey` | teste que inspeciona os headers da requisição mockada |
| RF-8 | O middleware de resposta mantém exatamente a tabela de status → retorno de `arquitetura/VISAO_TECNICA.md` (fluxo 4), incluindo o desembrulho de `data` e a promoção de `pagination` | testes de equivalência por faixa de status |
| RF-9 | Erro continua sendo `ValueError`, com o mesmo argumento | teste por faixa de status |
| RF-10 | Os 29 arquivos de teste passam a usar a ferramenta de mock compatível com `httpx`, mantendo um teste por método e o marker por recurso | suíte verde, contagem ≥ 109 |
| RF-11 | O CI roda em Python 3.13 e usa uv no lugar do Poetry | `pipeline.yml` + execução verde |
| RF-12 | O Read the Docs constrói a documentação com uv em 3.13 | build verde no RTD |
| RF-13 | O `README.md` reflete a nova exigência de Python | leitura |
| RF-14 | **Condicional a D-4.** Todos os métodos de escrita usam `json=payload`, eliminando a divergência de `Users.insert` | teste que inspeciona o corpo enviado, por método de escrita |
| RF-15 | `KanbanizeSession` **não herda** de nenhuma classe de biblioteca de terceiro; compõe um `httpx.Client` privado | `KanbanizeSession.__mro__` não contém `httpx.Client` |
| RF-16 | `requests` e `requests-mock` saem das dependências; entram `httpx` e `pytest-httpx` | leitura do `pyproject.toml` |
| RF-17 | A versão publicada passa a ser `0.3.0` | leitura do `pyproject.toml` |

## Requisitos não-funcionais

| # | Requisito | Limite |
|---|---|---|
| RNF-1 | Nenhum símbolo público removido ou renomeado | diff de `kanbanize_sdk/__init__.py` e `endpoints/__init__.py` vazio |
| RNF-2 | Nenhuma assinatura de método público alterada | diff sem mudança de assinatura |
| RNF-3 | Cobertura não cai | ≥ 99% (valor medido em 2026-08-07) |
| RNF-4 | Contagem de testes não cai | ≥ 109 |
| RNF-5 | Dependências de runtime | continua **uma só** — `httpx` substitui `requests`, não soma |
| RNF-6 | Redução de superfície aceita (D-2) | os métodos e atributos herdados de `requests.Session` que o SDK nunca prometeu — `head`, `options`, `mount`, `cookies`, `auth`, `send` — deixam de existir em `KanbanizeSession`. Aceito como parte da quebra de `0.3.0` |

## Critérios de aceite

```
Dado um ambiente limpo com Python 3.13
Quando eu rodar `uv sync` e o comando de teste do novo toolchain
Então os 109 testes passam e a cobertura é ≥ 99%
```

```
Dado que a API responde 200 com corpo {"data": [...]} e sem "pagination"
Quando eu chamar qualquer método de listagem
Então o retorno é exatamente o conteúdo de "data", como antes da migração
```

```
Dado que a API responde 200 com corpo contendo "pagination"
Quando eu chamar o método
Então o retorno é o dict com as chaves de pagination promovidas ao topo e "data" preservada dentro
```

```
Dado que a API responde 404 com corpo {"error": {...}}
Quando eu chamar qualquer método
Então é levantado ValueError com o conteúdo de "error" como argumento
```

```
Dado que a API responde 500
Quando eu chamar qualquer método
Então é levantado ValueError com {'code': 500, 'message': 'The request failed due to an internal server error.'}
```

```
Dado que a API responde 204
Quando eu chamar um método de delete
Então o retorno é None
```

```
Dado um consumidor que já usa a lib
Quando ele atualizar de 0.2.12 para 0.3.0 em Python 3.13
Então nenhuma chamada existente precisa ser alterada
```

```
Dado um ambiente com Python 3.12
Quando alguém tentar `pip install kanbanize-sdk==0.3.0`
Então o pip recusa a instalação por requires-python, em vez de instalar e quebrar em runtime
```

```
Dado que o mantenedor NÃO verificou contra a API real qual codificação de corpo ela aceita
Quando a implementação for revisada
Então RF-14 está fora de escopo e os métodos de escrita preservam `data=`/`json=` como estão hoje
```

```
Dado que o mantenedor verificou e confirmou que a API aceita corpo JSON
Quando eu chamar qualquer método de escrita
Então o corpo enviado é JSON e não form-urlencoded, em todos os métodos, inclusive os que hoje usam `data=`
```

## Impacto no que já existe

| Arquivo / módulo | Tipo | Risco |
|---|---|---|
| `pyproject.toml` | alterar | 🔴 Python mínimo, build backend, formato de dependências, `[tool.pytest.ini_options]` com os 28 markers precisa sobreviver |
| `poetry.lock` | remover | 🔴 arquivo intocável por regra; a remoção é o ponto da mudança |
| `uv.lock` | criar | — |
| `kanbanize_sdk/wrapper.py` | alterar | 🔴 **o arquivo de maior alcance do projeto.** Único ponto de transporte; atinge os ~130 métodos de uma vez. `httpx.Client` não é substituto drop-in de `requests.Session`: a assinatura de `request()` difere, `data=` com `dict` tem semântica diferente, e as exceções são outras |
| `kanbanize_sdk/wrapper.py:5-6` | alterar | `RequestException` e `CaseInsensitiveDict` são importados e **não usados** — somem com a migração |
| `tests/*.py` (29 arquivos) | alterar | 🔴 `requests-mock` não funciona com `httpx`. Todos os 109 testes precisam trocar de ferramenta de mock |
| `.github/workflows/pipeline.yml` | alterar | 🔴 `setup-python` para 3.13, `pip install poetry` → instalação do uv, comandos de install e test |
| `.readthedocs.yaml` | alterar | 🔴 `tools.python: "3.10"` → `"3.13"`, e os jobs `post_create_environment` / `post_install` que hoje chamam poetry |
| `README.md` | alterar | menção à versão de Python |
| `kanbanize_sdk/endpoints/*.py` (27) | **não alterar** | usam `self.service`, não `requests`. Se algum precisar mudar, o desenho da migração está errado |
| `kanbanize_sdk/dataclasses.py` | **não alterar** | é folha, sem dependência de HTTP |
| `specs/governanca/02-convencoes.md`, `specs/testes/ESTRATEGIA.md`, `CLAUDE.md` | alterar | todos listam comandos `poetry run ...` que deixam de existir |
| `specs/arquitetura/VISAO_TECNICA.md` | alterar | tabela de stack, camadas e o texto que diz "única fronteira com `requests`" |

## Decisões tomadas

Todas resolvidas com o mantenedor em 2026-08-07. Nenhuma pendente.

| # | Pergunta | Decisão | Porquê |
|---|---|---|---|
| D-1 | O Python mínimo do pacote cai para 3.13? | **Sim — `requires-python = ">=3.13"`**, abandonando 3.10–3.12 | Meia-migração deixa o compromisso de compatibilidade sem o benefício. O `pip` passa a recusar a instalação em runtime antigo, em vez de quebrar depois |
| D-2 | `KanbanizeSession` continua herdando um cliente de terceiro? | **Não — passa a compor** um `httpx.Client` interno | A herança de `requests.Session` faz o transporte vazar para a superfície pública. Compondo, a superfície fica no que a spec promete, e a próxima troca de cliente fica barata. **É redução consciente de superfície** — ver Impacto |
| D-3 | O que substitui `requests-mock`? | **`pytest-httpx`** | Fixture no mesmo formato do padrão atual; a conversão dos 109 testes fica mecânica, que é o que se quer num lote desse tamanho. `respx` e `MockTransport` puro exigiriam reescrever o estilo de cada teste |
| D-4 | `data=` vs `json=` nos métodos de escrita | **Padronizar em `json=`, com portão de verificação** — ver RF-14 e o critério de aceite correspondente | O header já anuncia `application/json`; `data=` com `dict` urlencoda e no httpx ainda emite `DeprecationWarning`. Mas nenhum teste prova o que a API aceita, então a padronização não pode ser aplicada às cegas |
| D-5 | Versão publicada | **`0.3.0`** | Em `0.x`, incremento de minor já sinaliza quebra por convenção. `1.0.0` declararia estabilidade da API pública, o que é prematuro com `BoardChildParentCards` vazia e `BoardsListParams` defeituosa |

### Sobre D-4 — o portão

O mantenedor **ainda não verificou** contra a API real qual codificação de corpo a Kanbanize
aceita. O agente não pode verificar: chamada HTTP real é proibida
(`governanca/03-limites-agente.md`).

Regra desta mudança, sem exceção:

- Se a verificação manual **confirmar** que a API aceita corpo JSON de verdade →
  padroniza em `json=` (RF-14).
- Se a verificação **não acontecer**, ou indicar que a API espera form-urlencoded →
  **RF-14 sai do escopo** e a migração preserva o comportamento atual campo a campo,
  divergência de `Users.insert` inclusa. A padronização vira mudança própria.

O risco de aplicar `json=` sem verificar é quebrar a escrita dos 129 métodos em produção, com
a suíte verde e sem ninguém perceber até um usuário reclamar.

## Riscos

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Mudança silenciosa no corpo enviado ao trocar `requests` por `httpx` | **alta** | RF-7 e RF-8 exigem teste que inspecione a requisição, não só a resposta. Hoje nenhum teste faz isso |
| Aplicar `json=` (RF-14) sem verificação real quebrar a escrita dos 129 métodos em produção | **alta se o portão for ignorado** | O portão de D-4 é bloqueante: sem verificação do mantenedor, RF-14 sai do escopo. Não há atalho — o agente não pode verificar sozinho |
| Alguém depender de método herdado de `requests.Session` que some com D-2 | baixa | Nenhum método do SDK usa a herança; a redução está declarada em RNF-6 e a versão `0.3.0` sinaliza a quebra |
| A suíte verde não prova compatibilidade com a API real (todos os testes são mockados) | **certa** | Limitação estrutural, já registrada em `testes/ESTRATEGIA.md`. Depois do merge, uma verificação manual do mantenedor contra a conta real é o único caminho |
| Reescrever 29 arquivos de teste em lote introduzir regressão por copiar-colar | média | RNF-4 (contagem ≥ 109) e RNF-3 (cobertura ≥ 99%) |
| RTD quebrar com uv e não ser detectado no CI | média | O build do RTD é externo ao `pipeline.yml`; verificar o build da PR antes do merge |
| Consumidor em 3.10 receber a atualização sem aviso | depende de D-1 | `requires-python` correto faz o `pip` recusar a instalação em vez de quebrar em tempo de execução |

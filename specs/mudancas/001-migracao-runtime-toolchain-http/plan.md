# Plano — 001 Migração de runtime, gerenciador de pacotes e cliente HTTP

> Só existe depois que `spec.md` está aprovada. Aqui entra o **como**.

Branch: `migration_runtime_toolchain_httpx`

## Abordagem

Duas entregas sequenciais na mesma branch, com um checkpoint verde entre elas. **Entrega A**
(Python 3.13 + uv) não toca uma única linha de `kanbanize_sdk/` nem de `tests/`: é reescrita de
`pyproject.toml`, geração de `uv.lock`, e ajuste de CI e Read the Docs. Se a suíte continuar
verde no fim de A, está provado que o runtime e o empacotador não são a causa de nada que
quebre depois. **Entrega B** (requests → httpx) reescreve `wrapper.py` e converte os 29
arquivos de teste — com a rede de segurança de A já estável.

O desenho de B é conservador de propósito: `httpx.Client` passa a ser um atributo privado de
`KanbanizeSession`, e a classe expõe exatamente os seis pontos que os endpoints já usam
(`get`, `post`, `put`, `patch`, `delete`, mais as properties `uri` e `api_key`). Os 27 arquivos
de `endpoints/` e o `client.py` **não mudam** — se o executor precisar tocá-los, o desenho está
errado e a cadeia volta ao planejador.

O middleware de resposta é portado com a tabela de status intacta. A única tradução real é de
exceção: `requests` não levantava nada em erro HTTP (o middleware lia `status_code`), e o httpx
mantém o mesmo padrão desde que **não** se chame `raise_for_status()`.

## O que é reusado

| Existente | Caminho | Como entra |
|---|---|---|
| Tabela de status → retorno do middleware | `kanbanize_sdk/wrapper.py:56-79` | Portada linha a linha, sem alteração de comportamento. É o contrato do RF-8 |
| `DefaultOptions` (TypedDict) | `kanbanize_sdk/wrapper.py:9-12` | Mantido como está. O construtor não muda (RF-6) |
| Properties `uri` e `api_key` | `kanbanize_sdk/wrapper.py:20-26` | Mantidas com a mesma assinatura (RF-6) |
| Os 6 métodos verbais da sessão | `kanbanize_sdk/wrapper.py:32-50` | Mesmos nomes e mesmos retornos; muda só quem executa a chamada por baixo |
| `GenericRequestMethod` e os 27 recursos | `kanbanize_sdk/endpoints/` | **Intocados.** Falam com `self.service`, não com o transporte |
| `client.py`, `dataclasses.py`, `utils.py` | `kanbanize_sdk/` | **Intocados** |
| Os 28 markers de teste | `pyproject.toml:38-69` | Transcritos para o `[tool.pytest.ini_options]` do novo formato. Marker perdido = teste que some do filtro |
| Estrutura dos 29 arquivos de teste | `tests/` | Preservada: um arquivo por recurso, um teste por método, marker por recurso, credenciais fictícias `teste`/`teste_key`. Muda só a fixture de mock |
| Metadados do pacote | `pyproject.toml:1-19` | Nome, descrição, autor, licença, URLs, `packages` — transcritos para o formato PEP 621 |

## O que é criado

| Novo | Caminho | Justificativa de não reusar |
|---|---|---|
| `uv.lock` | raiz | Substitui `poetry.lock`. Não há como reusar — é outro formato |
| Bloco `[project]` (PEP 621) | `pyproject.toml` | O uv não lê `[tool.poetry]`. A tradução é obrigatória |
| `httpx.Client` privado dentro de `KanbanizeSession` | `kanbanize_sdk/wrapper.py` | Não há cliente a reusar: o atual é a própria herança de `requests.Session`, que sai por decisão D-2 |
| Testes de equivalência do middleware | `tests/test_wrapper.py` (novo) | Não existe teste do caminho de erro hoje (`wrapper.py:74-77` tem cobertura zero). Sem ele, RF-8 e RF-9 são inverificáveis — não dá para provar que o comportamento foi preservado se ninguém nunca o testou |

O `tests/test_wrapper.py` é a única adição de escopo em relação ao "só migrar", e é
deliberada: a spec exige provar equivalência (RF-8, RF-9), e não se prova equivalência sem
teste. Cobre apenas as faixas de status e o desembrulho — **não** é o fechamento da lacuna de
cobertura registrada em `testes/ESTRATEGIA.md`, que segue como trabalho próprio.

## Alternativas consideradas

| Alternativa | Por que não | Vira ADR? |
|---|---|---|
| Uma entrega só, as três frentes juntas | Se a suíte quebrar, não se sabe se a causa é o runtime, o empacotador ou o cliente HTTP. O fatiamento isola a variável ao custo de um commit a mais | não |
| `KanbanizeSession` herdando `httpx.Client` | Decidido em D-2: mantém o transporte vazando para a superfície pública e repete o acoplamento que se está pagando para remover | **sim** — é a decisão de desenho com alternativa plausível desta mudança |
| Manter `requests` e adicionar `httpx` só para o modo async | Duas dependências de runtime e dois caminhos de código para manter em paralelo. Viola RNF-5 | não |
| `respx` ou `httpx.MockTransport` no lugar de `pytest-httpx` | Decidido em D-3: ambos exigiriam reescrever o estilo de cada um dos 109 testes, não só a fixture | não |
| Converter os 29 arquivos de teste de uma vez, num commit | Um erro de copiar-colar no lote fica invisível. Converter por grupo de recurso, com a suíte verde entre grupos, custa pouco e detecta cedo | não |
| Fazer B antes de A | httpx moderno exige Python recente; migrar o cliente HTTP num runtime que já vai ser trocado é retrabalho garantido | não |

**Vira ADR:** sim, um — a decisão de composição sobre herança em `KanbanizeSession`. Registrar
com a skill `spec-adr` durante a Entrega B, não no fim.

## Contratos afetados

| Contrato | Mudança | Quebra compatibilidade? |
|---|---|---|
| `requires-python` | `>=3.10` → `>=3.13` | **Sim.** Intencional (D-1). O `pip` recusa a instalação em runtime antigo |
| Versão do pacote | `0.2.12` → `0.3.0` | Sinaliza a quebra (D-5) |
| `Kanbanize` e os ~130 métodos de recurso | nenhuma | Não |
| 36 dataclasses | nenhuma | Não |
| Formato de retorno e tipo de exceção (`ValueError`) | nenhuma | Não |
| Métodos herdados de `requests.Session` em `KanbanizeSession` (`head`, `options`, `mount`, `cookies`, `auth`, `send`) | somem | **Sim.** Aceito em RNF-6 |
| Corpo enviado nos métodos de escrita | `data=` → `json=` | **Condicional ao portão de D-4.** Sem verificação manual, não muda |

## Dados e migrations

Não se aplica — o projeto não tem persistência. O único artefato equivalente é o lockfile:

| Passo | Reversível | Backfill | Risco |
|---|---|---|---|
| `poetry.lock` → `uv.lock` | Sim, por `git revert` | — | Resolução de versões diferente da travada hoje; mitigado por comparar as versões resolvidas antes de seguir |

## Ordem de entrega

Não há backend/frontend. A ordem que importa é entre as duas entregas:

**Entrega A — Python 3.13 + uv** (T-1 a T-6)
Só toca metadados, lockfile e automação. Ao fim, a suíte roda com `uv run pytest`, ainda em
cima de `requests`. Nenhum arquivo de `kanbanize_sdk/` ou `tests/` foi alterado.

**Checkpoint A:** 109 testes verdes, cobertura ≥ 99%, CI verde em 3.13, build do RTD verde.
Se algo aqui falhar, a causa é toolchain — não HTTP. **Não avance para B com A vermelho.**

**Entrega B — requests → httpx** (T-7 a T-13)
Depende inteiramente de A. Reescreve o transporte, depois os testes por grupo.

Como não quebrar durante o processo: A e B são commits separados na mesma branch, e nenhuma
publicação acontece nesta mudança (fora de escopo). O consumidor só é afetado no release, que
é posterior e manual.

## Estratégia de teste

| Nível | O que cobre | Cobre qual RF |
|---|---|---|
| Suíte existente (109 testes) rodando sem alteração após A | Prova que runtime 3.13 e uv não mudaram comportamento | RF-1, RF-2, RF-3, RF-4, RF-11 |
| Suíte existente convertida para `pytest-httpx` | Prova que os ~130 métodos mantêm verbo, path e retorno | RF-5, RF-10, RNF-3, RNF-4 |
| `tests/test_wrapper.py` — faixas de status | 200 sem paginação, 200 com paginação, 204, 400/401/403/404/409/429, 500, 503, status fora da tabela | RF-8, RF-9 |
| `tests/test_wrapper.py` — headers | `Content-Type: application/json` e `apikey` presentes em toda requisição | RF-7 |
| `tests/test_wrapper.py` — construtor e properties | `uri` montada corretamente, `api_key` acessível, `httpx.Client` fora do `__mro__` | RF-6, RF-15 |
| Inspeção do corpo enviado, por método de escrita | Só se o portão de D-4 abrir | RF-14 |
| Leitura de arquivo (não automatizável) | `pyproject.toml`, `README.md`, workflow, `.readthedocs.yaml` | RF-12, RF-13, RF-16, RF-17 |

RF sem teste: **RF-12** (build do RTD) só é verificável pelo build externo da PR — está em
Pontos de falha, não em teste automatizado.

## Pontos de falha

| O que pode dar errado | Detectado por | Resposta |
|---|---|---|
| Marker de teste perdido na tradução do `pyproject.toml` | contagem de testes < 109 no checkpoint A | Reconferir os 28 markers um a um contra `pyproject.toml:38-69` |
| `uv` resolver versões diferentes das travadas em `poetry.lock` | comparação explícita em T-3 | Fixar a versão divergente antes de seguir |
| Junção de URL do httpx diferir da concatenação manual atual | `tests/test_wrapper.py` e os testes de recurso, que registram a URL absoluta | O mock não casa e o teste falha — é o comportamento desejado |
| `data=` com `dict` emitir `DeprecationWarning` no httpx e mudar o corpo | inspeção de corpo em T-11 | É exatamente o que o portão de D-4 decide. Sem verificação do mantenedor, preservar o comportamento atual |
| Conversão em lote dos 29 arquivos introduzir regressão por copiar-colar | conversão por grupo, com suíte verde entre grupos (T-12) | Reverter o grupo, não a entrega |
| Build do Read the Docs quebrar com uv | build da PR no RTD — externo ao CI | Corrigir antes do merge; o `pipeline.yml` não cobre isso |
| Executor "aproveitar a viagem" e corrigir `BoardsListParams` ou o typo | revisão do diff | Fora de escopo declarado na spec. Volta ao planejador |

## Fora do plano

Cogitado e deliberadamente adiado:

- Fechar a lacuna de cobertura do caminho de erro além do necessário para provar equivalência
- Adotar `ruff`/`mypy` aproveitando que o `pyproject.toml` está sendo reescrito
- Ligar o gate de cobertura no CI aproveitando que o workflow está sendo reescrito
- Automatizar a publicação no PyPI aproveitando que o CI está sendo mexido
- Implementar o modo async
- Corrigir `BoardsListParams`, `WorkflowsInsetBody` ou `BoardChildParentCards`

Os três primeiros são tentadores porque o arquivo já está aberto. São mudanças próprias, cada
uma com sua decisão em aberto. Fazê-las aqui esconde o risco real da migração dentro de um
diff maior.

---
**Aprovação humana:** ☑ aprovado — "Aprovado", mantenedor, 2026-08-07  
Não inicie a implementação sem esta caixa marcada.

# Plano — 002 Padronizar o corpo das escritas em JSON e automatizar a publicação no PyPI

> Só existe depois que `spec.md` está aprovada. Aqui entra o **como**.

Branch: `release_automation_and_json_body`

## Abordagem

Duas frentes independentes no código, com uma dependência de **ordem de release**: a Frente 1
precisa estar mergeada antes de a Frente 2 ser usada, porque a primeira release deve publicar
um pacote com o corpo já correto. A Frente 1 é uma troca mecânica de `data=` por `json=` em 29
linhas, blindada por um teste de corpo por método alterado — teste que hoje não existe em lugar
nenhum, porque a suíte inteira só afirma sobre a resposta. A Frente 2 é um workflow novo,
isolado do `pipeline.yml`, que só roda no evento `release`.

O desenho da Frente 1 se apoia numa assimetria: `json=` e `data=` produzem corpos diferentes,
e o teste que distingue os dois é `json.loads(request.content)` — falha com
`JSONDecodeError` quando o corpo é form-urlencoded. Um único helper de asserção serve aos 29
casos, então a blindagem não custa 29 invenções.

A Frente 2 não inventa nada: `uv build` já é o comando de build registrado em
`02-convencoes.md`, e o `pipeline.yml` já é o modelo de job em uv que o repositório usa.

## O que é reusado

| Existente | Caminho | Como entra |
|---|---|---|
| Padrão `payload = body.to_dict() if isinstance(...) else body` | as 29 chamadas em `endpoints/` | **Inalterado.** Só o argumento de destino muda, de `data=` para `json=` |
| `KanbanizeSession.post/put/patch` já aceitam `json=` | `wrapper.py:44` (`post`) | O `post` já tem o parâmetro. `put` e `patch` **não têm** — ver "O que é criado" |
| Header `Content-Type: application/json` | `wrapper.py`, headers do cliente | **Inalterado.** Já era enviado; passa a corresponder ao corpo |
| `Users.insert` com `json=` | `users.py:44` | **Inalterado.** É o único caso já correto, e vira a referência do padrão |
| Fixture `httpx_mock` e `httpx_mock.get_request()` | 30 arquivos em `tests/` | A asserção de corpo lê `get_request().content`. Nenhuma ferramenta nova |
| Estrutura dos testes de escrita | 24 arquivos, 37 chamadas `add_response(method='POST'\|'PUT'\|'PATCH')` | Cada um ganha a asserção de corpo. A estrutura não muda |
| Job em uv do CI | `.github/workflows/pipeline.yml` | Modelo copiado para o workflow de release: `setup-uv`, `uv python install 3.13`, `uv sync`, `uv run pytest` |
| `uv build` | já registrado em `02-convencoes.md` | É o passo de construção do workflow |
| `version` em `pyproject.toml` | `pyproject.toml` | Fonte da verdade da versão. O workflow **lê** e compara com a tag; não escreve |

## O que é criado

| Novo | Caminho | Justificativa de não reusar |
|---|---|---|
| Parâmetro `json=` em `KanbanizeSession.put` e `.patch` | `kanbanize_sdk/wrapper.py` | **Não há o que reusar: eles não aceitam `json`.** Hoje só `post` tem o parâmetro. Sem isso, 14 das 29 chamadas não têm como mandar JSON. É a única alteração no wrapper, e é aditiva |
| Helper de asserção de corpo | `tests/conftest.py` (novo) ou função em cada teste | Não existe nada equivalente. Ver decisão de desenho abaixo |
| Workflow de publicação | `.github/workflows/release.yml` | Não há job de publicação. Não pode entrar no `pipeline.yml`: aquele roda em push e PR, e este só pode rodar em `release` (RNF-5) |

### Decisão de desenho — onde mora o helper de asserção

`testes/ESTRATEGIA.md` diz, hoje: *"Não há fixtures compartilhadas, factories nem
`conftest.py` (…) Mantenha o padrão — não introduza `conftest.py` nem factory sem spec de
mudança."*

Criar `tests/conftest.py` **contraria uma regra escrita**. O plano propõe fazê-lo mesmo assim,
e a alternativa está avaliada abaixo. Se o humano preferir manter a regra, a saída é repetir
`json.loads(httpx_mock.get_request().content) == esperado` em cada teste — três linhas por
teste, 37 vezes. Esta é uma escolha do humano na aprovação do plano, não do executor.

## Alternativas consideradas

| Alternativa | Por que não | Vira ADR? |
|---|---|---|
| Fazer o wrapper converter `data=<dict>` em JSON, sem tocar nos endpoints | Resolveria as 29 linhas em um lugar só. Mas esconde a intenção: o endpoint continuaria dizendo `data=` e mandando JSON, o oposto do problema atual. E quebraria quem passasse `data=<str>` de propósito | **sim** |
| Repetir a asserção de corpo em cada teste, sem `conftest.py` | Respeita a regra vigente de `ESTRATEGIA.md`, mas são 37 repetições de três linhas, e a mudança de contrato futura teria 37 pontos de edição | **sim** — a decisão sobre `conftest.py` altera uma regra escrita |
| Publicar com `pypa/gh-action-pypi-publish` em vez de `uv publish` | É a action oficial e integra bem com Trusted Publishing. Mas o repositório acabou de padronizar em uv, e `uv publish` também suporta OIDC. Manter um fornecedor a menos | não |
| Guardar `PYPI_API_TOKEN` em secrets | Decidido em D-1/RF-8: Trusted Publishing não deixa credencial de longa duração no repositório | não |
| Publicar antes de rodar os testes, para reduzir tempo | Publicação é irreversível; teste é barato. Ordem invertida trocaria segundos por risco permanente | não |
| Fazer as duas frentes em PRs separadas | Defensável, mas a Frente 2 sem a Frente 1 publicaria a 0.3.0 com o corpo errado — que é exatamente o que a mudança quer evitar | não |

**Vira ADR:** dois. O local da conversão para JSON (endpoint × wrapper), e a introdução de
`conftest.py` contra a regra vigente. Ambos com a skill `spec-adr`, durante a implementação.

## Contratos afetados

| Contrato | Mudança | Quebra compatibilidade? |
|---|---|---|
| Corpo HTTP das 29 escritas | form-urlencoded → JSON | **Sim, no fio.** É o ponto da mudança. Nenhuma assinatura Python muda |
| `KanbanizeSession.put/patch` | ganham parâmetro `json=None` | Não — aditivo, com default |
| Assinaturas públicas dos ~130 métodos | nenhuma | Não |
| Versão publicada | 0.2.12 → 0.3.0 no PyPI | A 0.3.0 já carrega as quebras da mudança 001 |

## Dados e migrations

Não se aplica — sem persistência.

## Ordem de entrega

**Frente 1 — corpo JSON** (T-1 a T-5). Wrapper primeiro, endpoints depois, testes junto.

**Checkpoint 1:** suíte verde, `grep` de `data=` em `endpoints/` vazio, e cada método de
escrita com asserção de corpo.

**Frente 2 — workflow** (T-6 a T-8). Não depende do código da Frente 1 para ser escrita, mas
**não pode ser usada** antes dela.

**Checkpoint 2:** workflow no repositório, CI verde, e os dois passos manuais do mantenedor
concluídos.

**Release** (T-9). Só depois do merge. É o único passo irreversível do plano.

Como não quebrar durante o processo: o workflow novo só dispara em `release`, então existir na
branch não publica nada. A publicação real só acontece quando o humano criar a release.

## Estratégia de teste

| Nível | O que cobre | Cobre qual RF |
|---|---|---|
| Unidade — asserção de corpo em cada teste de escrita | O corpo enviado é JSON e não form-urlencoded, para dataclass e para `dict` | RF-1, RF-4 |
| Unidade — `tests/test_wrapper.py` existente | Header `Content-Type: application/json` continua presente | RF-5 |
| Unidade — teste novo em `test_wrapper.py` | `put` e `patch` aceitam e transmitem `json=` | RF-1 (viabilizador) |
| Diff / `grep` | Nenhum `data=` restante; `users.py` intocado; 7 escritas sem corpo intocadas | RF-1, RF-2, RF-3, RF-6, RNF-1 |
| Execução do workflow em release de teste | Conferência de tag, pre-release ignorada, ordem dos passos | RF-9, RF-12, RF-16 |
| Leitura do workflow | Gatilho, OIDC sem secret, `uv build`, environment | RF-7, RF-8, RF-10, RF-11, RF-15, RNF-4, RNF-5 |
| Manual, pós-release | `pip install kanbanize-sdk==0.3.0` em ambiente limpo | RF-13 |
| Leitura | `02-convencoes.md` descreve o fluxo novo | RF-14 |

**RF sem teste automatizado:** RF-13 depende de o pacote estar publicado; RF-15 e RF-8 são
verificáveis por leitura mais a execução real da primeira release.

## Pontos de falha

| O que pode dar errado | Detectado por | Resposta |
|---|---|---|
| Escapar uma das 29 linhas na troca | `grep` de RF-1 no Checkpoint 1 | Corrigir a linha faltante |
| `put`/`patch` não aceitarem `json` e o executor tentar passar mesmo assim | `TypeError` no primeiro teste | É por isso que o wrapper vem primeiro (T-1) |
| Asserção de corpo escrita de forma que passa com os dois formatos | Revisão do helper; um teste negativo que prove que ele falha com form-urlencoded | T-2 inclui esse teste negativo |
| Trusted Publishing não registrado no PyPI antes da release | Falha de autenticação no workflow | Falha antes de publicar. T-7 é a tarefa manual, e é pré-requisito de T-9 |
| Tag divergindo da versão | RF-9, antes do build | O PyPI não permite republicar; esta é a rede principal |
| Environment `pypi` inexistente | O job fica pendente ou falha | T-7 cria |
| A API rejeitar JSON em algum recurso | **Nenhum teste pega.** Só uso real | Registrado em riscos da spec. Reversão pontual no recurso afetado |
| Executor "aproveitar a viagem" e corrigir `BoardsListParams` ou o typo | Revisão do diff | Fora de escopo declarado. Volta ao planejador |

## Fora do plano

- Corrigir `BoardsListParams`, `WorkflowsInsetBody`, `BoardChildParentCards`
- Corrigir o defeito de `ValueError(None)` em 500/503
- Lint, type-check, gate de cobertura, atualização das actions em Node 20
- Cobrir o build do Read the Docs no CI
- Bump automático de versão e changelog

Os três primeiros são tentadores porque o executor vai passar por `endpoints/`, por
`pyproject.toml` e por `.github/`. São mudanças próprias.

---
**Aprovação humana:** ☑ aprovado — "Sim", mantenedor, 2026-08-11  
Escolha do helper: **`tests/conftest.py`**, conforme a recomendação do plano. O mantenedor
aprovou sem selecionar entre as duas opções; a alternativa (repetir a asserção nos 37 testes)
fica descartada e a mudança da regra de `testes/ESTRATEGIA.md` vira ADR.

Não inicie a implementação sem esta caixa marcada.

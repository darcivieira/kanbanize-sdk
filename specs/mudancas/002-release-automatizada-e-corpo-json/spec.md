---
id: 002-release-automatizada-e-corpo-json
titulo: Padronizar o corpo das escritas em JSON e automatizar a publicação no PyPI
classificacao: 🔴 RED
status: em-implementacao
criada: 2026-08-10
modulos: [boards, users, "+ 14 arquivos de endpoints com chamada de escrita"]
telas: []
---

# 002 — Padronizar o corpo das escritas em JSON e automatizar a publicação no PyPI

Duas frentes, unidas por um tema: **tornar a 0.3.0 publicável e publicá-la sozinha.**
Não faz sentido automatizar a entrega de um pacote cujo caminho de escrita pode estar
quebrado, então a correção do corpo vem junto.

## Problema

### Frente 1 — o corpo das escritas

29 chamadas de escrita em 16 arquivos de `kanbanize_sdk/endpoints/` passam o payload em
`data=<dict>`. Tanto o `requests` quanto o `httpx` codificam isso como
**`application/x-www-form-urlencoded`** — mas o header enviado em toda requisição é
`Content-Type: application/json` (`wrapper.py`). O SDK anuncia JSON e manda formulário.

Uma única chamada destoa: `Users.insert` (`users.py:44`) usa `json=payload` e manda JSON de
verdade. Não há registro de por que só ela.

Nenhum teste detecta a diferença: a suíte inteira mocka o transporte e afirma sobre a
**resposta**, nunca sobre o corpo enviado.

O mantenedor relata que a API v2 da Kanbanize aceita corpo JSON, com base em uso próprio em
outro projeto. Isso deixa dois cenários, e **os dois apontam para a mesma correção**:

| Cenário | Consequência hoje | Efeito da mudança |
|---|---|---|
| A API aceita JSON **e** form-urlencoded | escritas funcionam | padronização, risco baixo |
| A API aceita **só** JSON | **todas as escritas do SDK estão quebradas em produção** e ninguém percebeu | correção de defeito grave |

O cenário "aceita só form-urlencoded" está praticamente excluído: se fosse o caso, o uso do
mantenedor com JSON em outro projeto não teria funcionado.

### Frente 2 — a publicação

Não há nenhum job de publicação em `.github/workflows/`. A release é manual, feita fora do
repositório, e o comando exato nunca foi registrado. Isso significa passo manual sujeito a
erro exatamente no momento em que um erro é irreversível: **o PyPI não permite republicar uma
versão**.

A versão `0.3.0` já está em `pyproject.toml` desde a mudança 001 e **nunca foi publicada** —
o PyPI ainda serve a `0.2.12`.

## Resultado esperado

Para quem consome: `pip install kanbanize-sdk==0.3.0` passa a funcionar, e os métodos de
escrita mandam JSON de verdade — coerente com o header que o SDK sempre anunciou.

Para quem mantém: publicar deixa de ser um comando decorado. Publicar uma release no GitHub,
com tag `0.3.0`, dispara o workflow que constrói e envia o pacote ao PyPI sem nenhum segredo
guardado no repositório.

## Fora de escopo

- **Não publicar no TestPyPI.** Decidido: vai direto ao PyPI.
- **Não mudar path, verbo HTTP nem assinatura** de nenhum método.
- **Não mexer em `wrapper.py`.** O header já é `application/json`; o que muda é o argumento
  usado pelos endpoints.
- **Não alterar as 7 chamadas de escrita que não mandam corpo** — não têm payload a codificar.
- **Não trocar `ValueError` por exceções próprias**, nem corrigir o defeito de `500`/`503`.
- **Não adotar lint, type-check nem gate de cobertura** — continua sendo decisão à parte.
- **Não corrigir** `BoardsListParams`, `WorkflowsInsetBody` nem `BoardChildParentCards`.
- **Não automatizar bump de versão nem geração de changelog.** A versão continua editada à mão
  em `pyproject.toml`; o workflow apenas **confere** que ela bate com a tag.

## Requisitos funcionais

### Frente 1 — corpo JSON

| # | Requisito | Verificável por |
|---|---|---|
| RF-1 | As 29 chamadas de escrita que hoje usam `data=<payload>` passam a usar `json=<payload>` | `grep -rn "self.service.\(post\|put\|patch\)(.*data=" kanbanize_sdk/endpoints/` sem resultado |
| RF-2 | `Users.insert` continua com `json=` — nenhuma alteração | diff vazio em `users.py` |
| RF-3 | As 7 chamadas de escrita sem corpo permanecem inalteradas | diff limitado às 29 linhas de escrita com payload |
| RF-4 | Cada método de escrita alterado ganha teste que **inspeciona o corpo enviado** e afirma que é JSON, não form-urlencoded | teste que lê `request.content` e faz `json.loads` com sucesso |
| RF-5 | O header `Content-Type: application/json` continua sendo enviado | teste existente em `tests/test_wrapper.py` |
| RF-6 | Nenhuma assinatura pública muda; payload continua aceitando dataclass ou `dict` | diff sem mudança de assinatura |

### Frente 2 — publicação automatizada

| # | Requisito | Verificável por |
|---|---|---|
| RF-7 | Existe workflow em `.github/workflows/` disparado por `on: release: types: [published]` | leitura do arquivo |
| RF-8 | A autenticação é **Trusted Publishing** (OIDC). Nenhum token do PyPI é guardado em secrets | ausência de `PYPI_API_TOKEN`; presença de `permissions: id-token: write` |
| RF-9 | O workflow **falha** se a tag da release não corresponder à `version` do `pyproject.toml`. A tag é `X.Y.Z`, **sem prefixo `v`**, e a comparação é literal | execução com tag divergente falha antes de publicar |
| RF-10 | O workflow constrói com `uv build` e publica os artefatos gerados | leitura + execução |
| RF-11 | O workflow roda a suíte de testes **antes** de publicar, e não publica se ela falhar | leitura + execução |
| RF-12 | Publicar é o **último** passo; nenhum passo posterior pode falhar depois de o pacote estar no PyPI | leitura da ordem dos steps |
| RF-13 | Após a release, `pip install kanbanize-sdk==0.3.0` instala do PyPI e `import kanbanize_sdk` funciona em Python 3.13 | execução em ambiente limpo |
| RF-14 | `governanca/02-convencoes.md` deixa de dizer que a publicação é manual e passa a descrever o fluxo por release | leitura |
| RF-15 | O job que publica roda em um **GitHub Environment chamado `pypi`** | leitura do `environment:` no job |
| RF-16 | Release marcada como **pre-release** não publica: o workflow encerra sem enviar nada ao PyPI | execução com uma pre-release |

## Requisitos não-funcionais

| # | Requisito | Limite |
|---|---|---|
| RNF-1 | Nenhum símbolo público renomeado ou removido | diff vazio em `__init__.py` e `endpoints/__init__.py` |
| RNF-2 | Cobertura não cai | ≥ 99% |
| RNF-3 | Contagem de testes não cai | ≥ 124, e sobe com os testes de RF-4 |
| RNF-4 | Nenhum segredo de longa duração no repositório | zero secrets novos |
| RNF-5 | O workflow de publicação não roda em push nem em pull request | só no evento `release` |

## Critérios de aceite

```
Dado um método de escrita que recebe uma dataclass
Quando ele for chamado
Então o corpo da requisição é JSON válido, e não uma string form-urlencoded
```

```
Dado um método de escrita que recebe um dict cru
Quando ele for chamado
Então o corpo da requisição é JSON válido com o mesmo conteúdo
```

```
Dado que a suíte de testes falha
Quando uma release for publicada no GitHub
Então o workflow falha e nada é enviado ao PyPI
```

```
Dado que pyproject.toml declara version = "0.3.0"
Quando uma release for publicada com a tag 0.9.9
Então o workflow falha na conferência de versão, antes de construir ou publicar
```

```
Dado que pyproject.toml declara version = "0.3.0"
Quando uma release for publicada com a tag 0.3.0
Então o pacote é construído, publicado no PyPI por Trusted Publishing, e `pip install kanbanize-sdk==0.3.0` funciona
```

```
Dado um push na main ou a abertura de uma pull request
Quando o CI rodar
Então o workflow de publicação NÃO é acionado
```

```
Dado que uma release é publicada e marcada como pre-release no GitHub
Quando o workflow rodar
Então ele encerra sem publicar, e o PyPI não recebe nada
```

```
Dado que a regra de proteção do environment pypi está ativa
Quando o workflow chegar ao passo de publicação
Então ele aguarda aprovação manual antes de enviar o pacote
```

## Impacto no que já existe

| Arquivo / módulo | Tipo | Risco |
|---|---|---|
| 16 arquivos em `kanbanize_sdk/endpoints/` — 29 linhas | alterar | 🔴 **muda o corpo enviado ao servidor.** É o ponto de maior risco da mudança, e nenhum teste atual o cobre |
| `kanbanize_sdk/endpoints/users.py` | **não alterar** | já usa `json=` |
| `kanbanize_sdk/wrapper.py` | **não alterar** | o header já é `application/json`; a codificação é escolhida pelo argumento no endpoint |
| `tests/test_*.py` | alterar | acrescentar asserção de corpo nos testes de escrita (RF-4) |
| `.github/workflows/<novo>.yml` | criar | 🔴 publica em registro público, ação irreversível |
| `.github/workflows/pipeline.yml` | **não alterar** | o CI de testes segue como está |
| `pyproject.toml` | **não alterar** | `version = "0.3.0"` já está correta |
| `specs/governanca/02-convencoes.md` | alterar | remove o marcador de pendência do comando de publicação (RF-14) |
| `specs/visao/ROADMAP.md` | alterar | item 5 da próxima fase e duas linhas de bloqueios conhecidos saem |
| `specs/modulos/boards.md`, `specs/modulos/users.md` | alterar | a pendência de `data=`/`json=` deixa de existir |
| `specs/arquitetura/VISAO_TECNICA.md` | alterar | fluxo 3 e o risco correspondente |
| Configuração no painel do PyPI | externo | 🔴 **passo manual do mantenedor**, fora do repositório — sem ele o workflow falha na autenticação |
| Environment `pypi` nas configurações do repositório | externo | 🔴 **passo manual do mantenedor** — criar o environment e ativar a regra de proteção antes da primeira release |

## Decisões tomadas

Todas resolvidas com o mantenedor em 2026-08-10. Nenhuma pendente.

| # | Pergunta | Decisão | Porquê |
|---|---|---|---|
| D-1 | GitHub Environment dedicado para o job de publicação? | **Sim — environment `pypi`** | Publicar é irreversível: o PyPI não permite republicar uma versão. O environment dá um ponto de aprovação manual entre a release e o envio, e é onde o Trusted Publishing é amarrado com mais precisão. Custo zero quando a proteção não for usada |
| D-2 | O workflow de publicação roda a suíte de novo? | **Sim** | Custa poucos segundos e fecha uma janela real: a release pode ser criada de uma tag antiga ou de um commit cujo CI nunca rodou. Confiar no CI do commit assume uma correspondência que o GitHub não garante |
| D-3 | Pré-releases publicam? | **Não** — o workflow encerra sem publicar quando a release está marcada como *pre-release* | Evita mandar um `rc` ao PyPI por clique errado. Contrapartida assumida: soltar um `rc` de propósito exigirá alterar o workflow |
| D-4 | A release da 0.3.0 espera a verificação real do corpo JSON? | **Não espera** — mas a **primeira** release passa pela aprovação manual do environment do D-1 | Não há cenário plausível em que mudar para `json=` piore as coisas: ou a API aceita as duas formas, ou só JSON, e nesse caso as escritas já estão quebradas. Ainda assim, a primeira release do fluxo novo é o pior momento para descobrir um erro, porque a 0.3.0 não pode ser republicada |

### D-5 — formato da tag, revisado em 2026-08-11

O formato acordado antes de a spec ser escrita era `vX.Y.Z`. O mantenedor reviu durante a
implementação: a tag é **`X.Y.Z`, sem o prefixo `v`**, igual à `version` do `pyproject.toml`.
A comparação de RF-9 passa a ser literal, sem tirar prefixo — o que também elimina a única
transformação de string do passo, e portanto a única forma de ele errar sozinho.

Consequência: uma tag `v0.3.0` agora **falha** na conferência, em vez de passar.

### Consequência operacional do D-4

A regra de proteção do environment `pypi` deve estar **ativa na primeira release**. Depois que
o fluxo se provar, relaxá-la é decisão do mantenedor e não exige nova spec.

## Riscos

| Risco | Probabilidade | Mitigação |
|---|---|---|
| A API rejeitar corpo JSON em algum recurso específico | baixa | Nenhum teste local pega isso. Depende de verificação real do mantenedor. Se acontecer, é reversão pontual no recurso afetado |
| Trusted Publishing não configurado no painel do PyPI antes da primeira release | **alta se esquecido** | O workflow falha na autenticação, antes de publicar. Falha barata, mas confunde — deixar explícito nas tarefas |
| Tag divergente da versão publicar o número errado | média | RF-9: o workflow falha antes de construir. O PyPI não permite republicar, então esta checagem é a rede de proteção principal |
| Publicar uma 0.3.0 com escritas quebradas | baixa | RF-11 exige a suíte verde, mas a suíte **não prova** compatibilidade com a API real — limitação estrutural registrada em `testes/ESTRATEGIA.md` |
| Alterar 29 linhas em 16 arquivos em lote e escapar uma | média | RF-1 é verificável por `grep`; RF-4 obriga teste por método alterado |

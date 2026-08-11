# Constituição

Invariantes deste projeto. São descritivos do que já é verdade, não aspiracionais —
se uma linha aqui não descreve o código real, ela está errada e deve ser corrigida.

## Princípios

1. **Pragmatismo sobre dogma.** Arquitetura é meio, não fim. Aplique a estrutura completa
   onde a complexidade paga por ela; resolva direto onde não paga. Justifique o excesso,
   não a simplicidade.
2. **Reuso antes de criação.** Antes de criar módulo, helper, componente ou camada nova,
   procure o existente. Criar sem justificar duplicação é violação.
3. **Nada de gold-plating.** Não implemente o que não foi pedido. Abstração especulativa
   ("vai que um dia precisamos de outro provider") é violação, salvo quando a spec pedir.
4. **Todo "porquê" não-óbvio vira ADR.** Se você tomou uma decisão que um dev competente
   questionaria em code review, registre em `arquitetura/adr/`.
5. **Falha explícita.** Nada de `except: pass`, `catch {}` silencioso ou fallback mudo.
   Erro se propaga com contexto ou é tratado com registro.
6. **Spec e código andam juntos.** Mudou o comportamento, atualizou a spec no mesmo commit.

## Invariantes técnicos

1. **`httpx` só é importado em `kanbanize_sdk/wrapper.py`.** Nenhum arquivo em `endpoints/`
   monta URL absoluta, define header ou lê um objeto `Response`. Endpoint fala com
   `self.service` e passa path relativo. `KanbanizeSession` **compõe** o cliente, não herda
   dele — ver `arquitetura/adr/0001-*.md`.
2. **`dataclasses.py` e `utils.py` são folhas.** Não importam nada do próprio pacote. Se um
   deles precisou importar um endpoint ou o wrapper, o desenho está errado.
3. **Todo recurso herda de `GenericRequestMethod`** (`endpoints/generics.py`) **e declara
   `endpoint = '/<path>'`** como atributo de classe.
4. **Recurso só conhece outro recurso por herança declarada.** As únicas heranças legítimas
   hoje: `BoardSettings`, `BoardStructure`, `BoardStructureRevisions` e `BoardHistory` sobre
   `Boards`; `WorkspaceManagers` e `WorkspaceHistory` sobre `Workspaces`; `ColumnsListParams`
   sobre `LanesListParams`. Fora disso, um endpoint não importa outro.
5. **`client.py` só monta.** Instancia a `KanbanizeSession` e fabrica recursos. Zero regra de
   negócio, zero chamada HTTP, zero condicional.
6. **Método herdado que não se aplica é desligado com `utils.private`** — nunca com `pass`,
   `raise NotImplementedError` nem corpo vazio.
7. **Todo método de escrita aceita dataclass ou `dict`**, no padrão exato
   `payload = body.to_dict() if isinstance(body, XBody) else body`. Aceitar só a dataclass é
   violação; aceitar só `dict` também.
8. **Recurso ou dataclass novos só entram completos.** Os sete pontos de
   `02-convencoes.md` — classe, dataclasses, export em `endpoints/__init__.py`, export em
   `kanbanize_sdk/__init__.py`, fábrica em `client.py`, teste com marker registrado em
   `pyproject.toml`, e página em `docs/api/`. Recurso pela metade não é entrega parcial: é
   superfície pública quebrada. `BoardChildParentCards` é o contraexemplo vivo disto.

## Reprovação automática em code review

Duas condições reprovam sozinhas, sem discussão de mérito:

1. **Teste unitário falhando.** Qualquer teste vermelho na suíte. Não existe "falha conhecida,
   pode seguir".
2. **Não cumprimento do contrato com a API da Kanbanize.** Path, verbo HTTP, nome de campo ou
   formato divergente do OpenAPI da conta
   (`https://{subdomain}.kanbanize.com/openapi`). O contrato é externo e não negociável: o SDK
   se adapta a ele, nunca o contrário.

O segundo item é o mais perigoso para um agente, porque **os testes não o detectam** — a suíte
inteira mocka o transporte HTTP. Um path errado passa verde.

E o agente **não consegue conferir sozinho**: o OpenAPI está atrás do subdomínio do mantenedor
e chamada HTTP real é proibida (`03-limites-agente.md`). Portanto, ao criar ou alterar um
recurso, o agente **pede o trecho da documentação ao humano e transcreve**. Inferir path, verbo
ou nome de campo por analogia com outro recurso é violação deste invariante, não atalho.
Ver `arquitetura/VISAO_TECNICA.md`, seção "Fronteira com a API da Kanbanize".

## Armadilhas — o que parece melhoria e é quebra

Este projeto é um pacote público no PyPI em `0.3.x`, consumido por gente que o mantenedor não
conhece. Cinco coisas parecem limpeza óbvia e **quebram consumidores**. Nenhuma pode ser feita
sem ADR e "pode ir" literal:

| Parece | É |
|---|---|
| Corrigir o typo `WorkflowsInsetBody` → `WorkflowsInsertBody` | Remoção de símbolo público exportado. Quebra todo `from kanbanize_sdk import WorkflowsInsetBody` |
| Trocar `ValueError` por uma hierarquia de exceções própria | Quebra todo `except ValueError` de quem consome |
| Uniformizar `insert` para sempre `POST` | Muda o comportamento HTTP de `BoardStickers`, `BoardCustomFields`, `BoardCustomFieldAllowedValues` e `BoardCardTypes`, que hoje fazem `PUT` em id fornecido |
| Substituir a assinatura `body: X \| dict` por só a dataclass | Quebra quem passa `dict` cru — que é hoje a única saída em `Boards.list` |
| Substituir `utils.private` por algo "mais pythônico" | Muda o tipo e a mensagem do erro que consumidores veem ao chamar método desligado |

Regra geral: **símbolo exportado é contrato.** Se está em `kanbanize_sdk/__init__.py`, mexer é
🔴 RED.

## Dívida conhecida — status: aberta

O mantenedor declarou toda a dívida abaixo **aberta**: pode ser corrigida quando o agente já
estiver no arquivo por outro motivo. Não precisa de permissão caso a caso.

| Dívida | Onde |
|---|---|
| `BoardChildParentCards` exportada e vazia | `endpoints/board_child_parent_cards.py` |
| Ausência de lint e type-check | `pyproject.toml`, `pipeline.yml` |
| `dataclasses.py` monolítico, 443 linhas | `dataclasses.py` |

**"Aberta" não rebaixa a classificação de risco.** Continua valendo `03-limites-agente.md`:

- Apagar o `private` comentado em `workspace_managers.py` e `workspace_history.py` → 🟢 GREEN:
  é código comentado, e o DoD proíbe deixá-lo para trás. **Mas desligar de fato aqueles
  métodos é outra coisa** — muda o que o consumidor pode chamar, e é mudança de contrato.
- Implementar `BoardChildParentCards` → 🟡 YELLOW: é recurso novo, precisa de spec.
- Adotar lint/type-check → mudança de toolchain e de CI, 🔴 RED com ADR.
- Dividir `dataclasses.py` → muda o caminho de import de 36 símbolos públicos, 🔴 RED.

O que "aberta" significa na prática: o agente **não precisa perguntar se pode mexer**. Ainda
precisa seguir o fluxo correspondente ao risco.

## Limites de escopo

Os não-objetivos do produto são donos de `visao/PRODUTO.md`. Resumo operacional para o agente:
este SDK **não armazena e não manipula dados**. Não adicione cache, retry, backoff, validação
local de payload, persistência, CLI ou camada de serviço — nada disso é "melhoria esquecida",
tudo isso foi recusado de propósito. Ver o parking lot em `visao/ROADMAP.md`.

## Governança

- Alterar este arquivo é uma mudança **RED** (ver `03-limites-agente.md`).
- Um invariante só cai por ADR que o revogue explicitamente.

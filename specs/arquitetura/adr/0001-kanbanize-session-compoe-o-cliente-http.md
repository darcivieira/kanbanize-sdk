---
numero: 0001
titulo: Compor o cliente HTTP dentro de KanbanizeSession em vez de herdar dele
status: aceito
data: 2026-08-07
substitui: —
substituido-por: —
modulos: []
---

# 0001 — Compor o cliente HTTP dentro de KanbanizeSession em vez de herdar dele

## Contexto

Desde a origem do SDK, `KanbanizeSession` **herda `requests.Session`** e sobrescreve
`request()`, `get()`, `post()`, `put()`, `patch()` e `delete()` para prefixar a URL base,
injetar os headers e passar a resposta por um middleware.

A mudança 001 troca `requests` por `httpx`, o que obriga a decidir o que a classe passa a ser.
A escolha não é neutra: `KanbanizeSession` é instanciada dentro de `Kanbanize` e fica acessível
como `service`, então tudo o que a classe base expõe é, na prática, superfície pública de um
pacote publicado no PyPI.

Restrições no momento da decisão:

- O pacote está em `0.2.12` no PyPI, com consumidores desconhecidos.
- Nenhum código do SDK usa a herança: os 27 recursos chamam apenas os seis métodos verbais.
- Nenhum teste exercitava métodos herdados.
- O modo async está no roadmap, e `httpx` foi escolhido justamente para viabilizá-lo.

Desconhecido no momento: se algum consumidor usa `session.head()`, `session.mount()`,
`session.cookies` ou `session.auth`. Não há telemetria nem issue que indique isso — a decisão
foi tomada sem essa evidência.

## Decisão

`KanbanizeSession` **não herda** de nenhuma classe de biblioteca de terceiro. Ela guarda um
`httpx.Client` em atributo privado e expõe apenas o que o SDK promete: os seis métodos verbais,
`request()`, e as propriedades `uri` e `api_key`.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| Herdar `httpx.Client`, espelhando o desenho atual | Mantém o transporte vazando para a superfície pública, que é exatamente o acoplamento que se está pagando para remover. E amarra a superfície do SDK à evolução do httpx: qualquer método novo ou renomeado na classe base vira, sem revisão, parte da API pública do pacote |
| Manter `requests` e adicionar `httpx` só para o futuro modo async | Duas dependências de runtime e dois caminhos de transporte para manter em paralelo, com o risco de divergirem no tratamento de erro. Viola a restrição de dependência única |
| Criar uma camada de abstração de transporte, com implementações plugáveis | Abstração especulativa para um único cliente HTTP. Violaria o princípio 3 da constituição (nada de gold-plating) |

## Consequências

**Ganhamos:**
- A superfície pública passa a ser exatamente a documentada, e não "tudo o que a biblioteca de
  terceiro oferece"
- A próxima troca de cliente HTTP fica contida em um arquivo, sem quebra de contrato
- O modo async pode ser adicionado como uma segunda implementação interna sem duplicar a
  hierarquia de classes

**Pagamos:**
- Quebra para quem usava métodos herdados (`head`, `options`, `mount`, `cookies`, `auth`,
  `send`). Sinalizada pela versão `0.3.0`
- Qualquer capacidade nova do httpx que o SDK queira expor precisa ser escrita à mão, em vez de
  vir de graça pela herança

**Fica mais difícil depois:**
- Passar o objeto `service` para código de terceiro que espere um cliente HTTP compatível com
  a interface do httpx
- Reintroduzir a herança seria uma segunda quebra de contrato

## Como reverter

Barato em código: reintroduzir a herança é um `class KanbanizeSession(httpx.Client)` e a
remoção da delegação. Caro em contrato: seria a segunda mudança consecutiva na superfície
pública, e exigiria novo bump de versão. O caminho de saída existe, mas o custo é de
credibilidade, não de implementação.

## Sinais de que esta decisão envelheceu

- Issues pedindo acesso a recursos do httpx que o SDK não expõe (timeouts por chamada, proxies,
  retries de transporte, streaming)
- A lista de métodos delegados crescer a ponto de reimplementar a interface do `httpx.Client`
  por inteiro — nesse ponto, a herança volta a ser o desenho honesto
- O modo async exigir duplicar toda a delegação, em vez de reaproveitá-la

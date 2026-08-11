---
numero: 0004
titulo: Converter o corpo para JSON no endpoint, não no wrapper
status: aceito
data: 2026-08-11
substitui: —
substituido-por: —
modulos: []
---

# 0004 — Converter o corpo para JSON no endpoint, não no wrapper

## Contexto

Até a mudança 002, 29 chamadas de escrita em 16 arquivos de `endpoints/` passavam o payload em
`data=<dict>`. Tanto o `requests` quanto o `httpx` codificam isso como
`application/x-www-form-urlencoded`, enquanto `wrapper.py` sempre enviou
`Content-Type: application/json`. O SDK anunciava JSON e mandava formulário. Uma única
chamada, `Users.insert`, usava `json=` e mandava JSON de verdade.

Nenhum teste detectava a diferença: a suíte inteira afirma sobre a **resposta**, nunca sobre o
corpo enviado.

Corrigir isso admitia dois lugares: o endpoint, que escolhe o argumento, ou o wrapper, que é o
ponto único de transporte e poderia reinterpretar `data=<dict>` como JSON.

Desconhecido no momento: se a API da Kanbanize aceita as duas codificações ou só JSON. O
mantenedor relata que JSON funciona, com base em uso próprio em outro projeto; não houve
verificação contra a API dentro desta mudança.

## Decisão

A conversão acontece **no endpoint**: as 29 chamadas passam a usar `json=payload`. O wrapper
ganha apenas o parâmetro `json` em `put` e `patch` — que só `post` tinha —, de forma aditiva e
com o mesmo default.

O wrapper **não** reinterpreta `data=`. Quem chama declara o que quer enviar.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| O wrapper converter `data=<dict>` em JSON | Resolveria 29 linhas em um lugar só, mas deixaria o endpoint dizendo `data=` e mandando JSON — exatamente o tipo de divergência entre o que o código diz e o que ele faz que originou este defeito. Também quebraria qualquer chamada que quisesse mesmo enviar form-urlencoded |
| Manter `data=` e mudar o header para `application/x-www-form-urlencoded` | Alinharia header e corpo, mas na direção errada: a API é JSON, e `Users.insert` já provava que JSON funciona |
| Deixar como estava até haver verificação contra a API real | Os dois cenários possíveis apontam para a mesma correção. Se a API aceita as duas formas, é limpeza; se aceita só JSON, as escritas estavam quebradas. Não havia cenário em que manter fosse melhor |

## Consequências

**Ganhamos:**
- O corpo enviado passa a corresponder ao header que o SDK sempre anunciou
- A intenção fica no lugar onde é lida: o endpoint declara `json=`
- 30 testes passam a afirmar o corpo enviado, não só a resposta — capacidade que a suíte não
  tinha

**Pagamos:**
- Mudança de comportamento **no fio** para 29 chamadas, sem verificação prévia contra a API
- `put` e `patch` agora aceitam `data` e `json` ao mesmo tempo; passar os dois é erro do
  chamador, e nada impede

**Fica mais difícil depois:**
- Um recurso que precise mesmo de form-urlencoded terá de passar `data=` explicitamente,
  contrariando o padrão — e isso vai parecer engano para quem ler

## Como reverter

Trocar `json=payload` de volta para `data=payload` no recurso afetado. É reversão pontual: um
recurso por vez, sem tocar no wrapper. As asserções de corpo apontam exatamente onde.

## Sinais de que esta decisão envelheceu

- Relato de que algum endpoint da Kanbanize rejeita corpo JSON
- Necessidade de enviar `multipart/form-data`, para upload, em algum recurso futuro
- O parâmetro `data` dos métodos do wrapper ficar sem nenhum uso — nesse ponto, removê-lo
  simplifica, mas é quebra de contrato

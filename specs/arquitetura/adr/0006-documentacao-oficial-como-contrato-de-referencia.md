---
numero: 0006
titulo: Aceitar a documentação oficial da Kanbanize como contrato de referência, sem validação em execução real
status: aceito
data: 2026-08-12
substitui: —
substituido-por: —
modulos: []
---

# 0006 — Aceitar a documentação oficial da Kanbanize como contrato de referência, sem validação em execução real

## Contexto

A suíte deste projeto é 100% mockada. Os 34 pontos de asserção de corpo provam o que o SDK
**envia**; nenhum teste prova o que a API da Kanbanize **aceita**. Chamada HTTP real é
proibida (`governanca/03-limites-agente.md`), não há conta de teste no ambiente, e o agente
não consegue ler o OpenAPI da conta.

Isso vinha sendo registrado como dívida em aberto desde o bootstrap, com a implicação de que
faltava fazer algo a respeito. Na prática, nada estava sendo feito e nada estava planejado —
uma dívida que ninguém pretende pagar não é dívida, é uma decisão não assumida.

O mantenedor decidiu assumi-la: **a documentação oficial da plataforma é tratada como
correta**, mesmo sem validação em tempo de execução.

## Decisão

A documentação oficial da Kanbanize — o OpenAPI publicado em
`https://{subdomain}.kanbanize.com/openapi` — é o **contrato de referência** do SDK.

Consequências diretas:

- Um método transcrito fielmente da documentação está **correto por definição**, mesmo sem
  nunca ter sido exercitado contra a API.
- Se a plataforma se comportar de forma diferente do que documenta, isso é **defeito da
  plataforma**, não do SDK. A detecção continua sendo relato de quem usa a lib, e a correção
  passa a ser adaptação a um fato novo — não conserto de um erro nosso.
- A pergunta do corpo `data=` vs `json=`, aberta desde a mudança 001, fica **encerrada**: o SDK
  manda JSON desde a mudança 002, coerente com o header e com o que a documentação descreve.

## O que esta decisão desloca, e não elimina

O risco não some, muda de lugar. Sai de *"a API pode se comportar diferente do documentado"* e
entra em *"nossa transcrição da documentação pode estar errada"*.

E a segunda é hoje a mais perigosa, porque **a documentação não está no repositório**. Se o
contrato de referência é um documento que nenhum arquivo daqui registra, então:

- ninguém consegue revisar se a transcrição está fiel — nem o mantenedor daqui a seis meses,
  nem um contribuidor, nem um agente;
- a suíte verde continua sem significar nada sobre corretude de contrato;
- a regra de "peça o trecho da documentação ao humano e transcreva"
  (`01-constituicao.md`) vira o único controle, e ele depende de disciplina em cada mudança.

**Mitigação obrigatória desta decisão:** registrar no repositório o trecho de documentação de
cada recurso, em `specs/modulos/<recurso>.md`. Isso deixa de ser preenchimento de spec e passa
a ser o registro do contrato assumido como verdadeiro. Sem isso, a decisão não tem controle
nenhum — só confiança.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| Teste de contrato contra uma conta real | É o único que prova de verdade. Esbarra na proibição de chamada real e na inexistência de conta de teste. Também tornaria a suíte dependente de rede e de estado remoto, num projeto cujo teste hoje roda em 1 segundo |
| Gravar respostas reais uma vez e testar contra elas (VCR/cassettes) | Meio-termo tentador: prova a transcrição num instante do tempo. Mas exige ao menos uma chamada real, e cassettes envelhecem **em silêncio** — passam a garantir compatibilidade com uma API que já mudou, o que é pior que não garantir nada |
| Continuar tratando como dívida em aberto | Era o estado anterior. Dívida que ninguém pretende pagar polui a lista e esconde as que importam |

## Consequências

**Ganhamos:**
- Uma fonte da verdade nomeada, em vez de uma incerteza permanente na lista de dívidas
- Critério claro de culpa quando algo quebra: se a transcrição bate com a doc, o defeito é da
  plataforma
- A pergunta do `data=`/`json=` sai da lista

**Pagamos:**
- Aceitamos que a documentação pode estar errada ou desatualizada, e que descobriremos isso
  por reclamação de usuário
- A fidelidade da transcrição vira o ponto único de falha, sem nenhuma verificação automática

**Fica mais difícil depois:**
- Justificar a ausência de teste de contrato quando o SDK ganhar consumidores exigentes
- Auditar uma transcrição antiga cujo trecho de documentação nunca foi registrado

## Como reverter

Reverter é adotar teste de contrato real, o que exige três coisas que hoje não existem: uma
conta de teste, permissão para chamada real, e disposição para a suíte depender de rede.
Nenhuma é impossível; todas são decisão do mantenedor. A reversão não mexe em uma linha de
código de produção.

## Sinais de que esta decisão envelheceu

- Um segundo relato de comportamento divergente do documentado — o primeiro é anedota, o
  segundo é padrão
- Um recurso cuja documentação seja ambígua a ponto de duas transcrições fiéis serem possíveis
- Consumidores relevantes o bastante para que "descobrimos por reclamação" deixe de ser
  aceitável
- Passar a existir conta de teste no ambiente, o que removeria o principal impedimento

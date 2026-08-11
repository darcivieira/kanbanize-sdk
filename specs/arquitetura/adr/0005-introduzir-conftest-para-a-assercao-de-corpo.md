---
numero: 0005
titulo: Introduzir tests/conftest.py para a asserção de corpo, revogando a proibição anterior
status: aceito
data: 2026-08-11
substitui: —
substituido-por: —
modulos: []
---

# 0005 — Introduzir tests/conftest.py para a asserção de corpo, revogando a proibição anterior

## Contexto

`testes/ESTRATEGIA.md` dizia, desde o bootstrap: *"Não há fixtures compartilhadas, factories
nem `conftest.py` (…) Mantenha o padrão — não introduza `conftest.py` nem factory sem spec de
mudança."*

A regra tinha um propósito real: os testes deste projeto são deliberadamente verbosos, com o
JSON esperado ao lado da asserção, sem indireção. Quem lê um teste vê tudo.

A mudança 002 exigiu afirmar o **corpo enviado** em 30 testes de escrita — capacidade que a
suíte não tinha. A asserção não é uma linha: precisa ler `httpx_mock.get_request().content`,
tentar `json.loads`, e falhar com mensagem útil quando o corpo vier form-urlencoded. Sem
mensagem útil, o erro aparece como `JSONDecodeError` cru e ninguém entende o que aconteceu.

Repetir isso 30 vezes seriam ~120 linhas duplicadas, com 30 pontos de edição no dia em que a
asserção precisar mudar.

A regra citada foi escrita pelo próprio bootstrap, descrevendo o estado do projeto na época —
não era decisão examinada. Este ADR a substitui por uma versão com limite explícito.

## Decisão

`tests/conftest.py` passa a existir, contendo **uma** fixture: `assert_json_body`.

A regra de `testes/ESTRATEGIA.md` é revista: `conftest.py` fica reservado a **asserções sobre
a requisição enviada**, que não cabem inline. Continua proibido usar `conftest.py` para
fixtures de dados, factories ou construção de payload — o JSON esperado permanece no corpo de
cada teste, e é isso que a regra original protegia.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| Repetir a asserção nos 30 testes, sem `conftest.py` | Respeita a regra ao pé da letra, mas troca uma indireção de três linhas por 120 linhas duplicadas e 30 pontos de edição. O que a regra protege — o dado esperado visível ao lado da asserção — continua protegido, porque só a *mecânica* sai do teste, não o valor |
| Um módulo `tests/helpers.py` importado explicitamente | Evita a "mágica" da fixture e seria defensável. Mas o helper precisa de `httpx_mock`, que é fixture: importar exigiria passá-lo à mão em toda chamada, ficando mais verboso que a fixture sem ganho de clareza |
| Não verificar o corpo, confiando na revisão de código | É exatamente o que permitiu a divergência sobreviver desde a origem do SDK. Descartada sem hesitação |

## Consequências

**Ganhamos:**
- Uma asserção com mensagem de erro que nomeia o defeito, em vez de `JSONDecodeError`
- Um ponto único de edição quando a verificação de corpo mudar
- A capacidade de afirmar o que o SDK **envia**, e não só o que ele devolve

**Pagamos:**
- Uma indireção: quem lê um teste de escrita precisa abrir `conftest.py` para saber o que
  `assert_json_body` faz
- Um precedente. `conftest.py` existir convida a colocar mais coisa lá, que é justamente o que
  a regra original evitava — por isso o limite ficou escrito

**Fica mais difícil depois:**
- Recusar a próxima fixture compartilhada exigirá apontar o limite deste ADR, não mais a
  ausência do arquivo

## Como reverter

Inlinear a fixture nos 30 testes e apagar `conftest.py`. Mecânico, e o teste negativo em
`test_wrapper.py` continua valendo como prova de que a asserção distingue os formatos.

## Sinais de que esta decisão envelheceu

- `conftest.py` passar de uma fixture, especialmente se ganhar factory ou dado de teste
- Alguém precisar ler `conftest.py` para entender o que um teste espera — sinal de que valor
  vazou para dentro do helper
- A suíte adotar teste de contrato de verdade, contra a API real, tornando a asserção de corpo
  redundante

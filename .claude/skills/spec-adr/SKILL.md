---
name: spec-adr
description: Cria um Architecture Decision Record em specs/arquitetura/adr/ ou marca um ADR existente como substituído. Use sempre que uma decisão técnica com alternativa plausível for tomada — escolha de biblioteca, padrão de persistência, estratégia de cache, modelo de autenticação, comprar vs construir, ou aceitação consciente de dívida técnica. Use também quando o usuário disser que mudou de ideia sobre uma decisão já registrada, ou pedir para documentar o porquê de algo.
---

# spec-adr

## Antes de tudo: isto é mesmo um ADR?

| Situação | Onde vai |
|---|---|
| Havia alternativa plausível e ela foi descartada | **ADR** |
| Só uma forma razoável de fazer | `governanca/02-convencoes.md` |
| Regra que nunca pode ser violada | `governanca/01-constituicao.md` |
| Como o sistema é montado hoje | `arquitetura/VISAO_TECNICA.md` |

Se a tabela "Alternativas descartadas" ficaria vazia, não é ADR. Não crie.

## Criar

1. Próximo número livre em `specs/arquitetura/adr/`, 4 dígitos, **nunca reaproveitado**.
2. Arquivo `NNNN-slug-curto.md` a partir de `specs/_templates/ADR.md`.
3. Preencha:
   - **Contexto:** restrições reais no momento, incluindo o que era desconhecido.
     Isto é o que dá valor ao ADR daqui a um ano.
   - **Alternativas descartadas:** com o motivo real, não o motivo elegante.
   - **Consequências:** ganhos, custos, e o que fica mais difícil depois.
   - **Como reverter:** custo e caminho. Se for irreversível, diga.
   - **Sinais de envelhecimento:** o que observar que indicaria hora de um sucessor.
4. Status `aceito` só quando o humano confirmar. Antes disso, `proposto`.
5. Atualize o índice em `specs/arquitetura/adr/README.md`.

## Substituir

**Nunca edite um ADR aceito.** O registro do que se pensava é o produto.

1. Crie o sucessor com `substitui: NNNN` e explique no contexto **o que mudou desde então**.
2. No antigo, altere **apenas** `status: substituído` e `substituido-por: MMMM`.
3. Atualize o índice.

## Regra de escrita

Contexto e alternativas em **fatos e restrições**, não em justificativa retrospectiva.
"Escolhemos X porque é melhor" não é ADR. "Escolhemos X porque Y exigia Z que não tínhamos
até <data>, ao custo de W" é.

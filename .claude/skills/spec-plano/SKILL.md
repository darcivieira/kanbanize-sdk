---
name: spec-plano
description: Gera plan.md e tasks.md a partir de uma spec de mudança já aprovada em specs/mudancas/NNN-*/. Use depois da skill spec-nova, quando o usuário pedir o plano técnico, o desenho da solução, ou a quebra em tarefas de uma mudança já especificada. Use também quando o usuário disser que aprovou a spec e quer partir para o desenho.
---

# spec-plano

Converte requisito em desenho técnico e tarefas ordenadas. Aqui entra o **como**.

## Pré-condições

- `specs/mudancas/NNN-*/spec.md` existe, com `status: aprovada`
- Nenhum `[PRECISA DECISÃO]` pendente

Se qualquer uma falhar, pare e diga qual.

## Passo 1 — Reconhecimento antes do desenho

Antes de propor qualquer estrutura nova, leia o código real dos módulos e telas listados
em "Impacto no que já existe". Delegue para subagente se for extenso.

Preencha a tabela **"O que é reusado" antes** da tabela "O que é criado".
Essa ordem não é estilística: criar sem ter procurado é violação da constituição, e a
ordem das tabelas é o que força a busca.

## Passo 2 — plan.md

Use `specs/_templates/MUDANCA-plan.md`. Regras:

- Toda criação nova precisa de justificativa de **por que não reusar**
- Alternativa considerada e descartada com peso real → marque "vira ADR: sim"
- Migration: declare reversibilidade e backfill explicitamente
- Backend + frontend: declare a ordem de entrega e como não quebrar durante o deploy
- Amarre cada nível de teste aos RFs que ele cobre — RF sem teste é buraco

Se o desenho exigir camada, padrão ou biblioteca nova, isso é 🔴 **RED**: pare e sinalize.

## Passo 3 — tasks.md

Use `specs/_templates/MUDANCA-tasks.md`. Regras:

- Ordem por dependência real, não por conveniência
- Cada tarefa toca poucos arquivos e cita os caminhos
- "Pronto quando" verificável — não "implementado corretamente"
- Cada RF da spec aparece em pelo menos uma tarefa; conferir cobertura ao final
- `[P]` só onde não há conflito de arquivo
- Checkpoints onde algo passa a funcionar ponta a ponta

## Passo 4 — Parar para aprovação

Apresente: abordagem em 3 frases, o que é reusado, o que é criado, os riscos, e a contagem
de tarefas. Peça aprovação explícita.

**Não implemente.** A caixa de aprovação em `plan.md` só é marcada pelo humano.

---
name: spec-nova
description: Cria a especificação de uma mudança em specs/mudancas/NNN-slug/spec.md antes de qualquer código ser escrito. Use sempre que o usuário pedir uma feature nova, uma alteração de comportamento, um endpoint, uma tela, ou qualquer mudança classificada como YELLOW ou RED em specs/governanca/03-limites-agente.md — mesmo que ele peça "só implementa rápido". Use também quando o pedido tiver ambiguidade de requisito ou tocar três ou mais arquivos.
---

# spec-nova

Transforma um pedido em requisito verificável **antes** de existir código.

## Passo 1 — Classificar

Leia `specs/governanca/03-limites-agente.md` e declare no formato:

```
CLASSIFICAÇÃO: 🟡 YELLOW
MOTIVO: <uma frase>
```

Se for 🟢 GREEN, **não crie spec**. Diga que é GREEN e implemente direto —
burocracia em mudança trivial destrói a adesão ao processo.

## Passo 2 — Contexto

Carregue o mínimo: `governanca/01-constituicao.md`, `visao/GLOSSARIO.md`, e os
`modulos/` ou `ui/telas/` que o pedido toca. Não carregue `specs/` inteiro.

Verifique `specs/ACTIVE.md`. Se já houver mudança em curso, pergunte antes de abrir outra —
duas frentes simultâneas é como o processo apodrece.

## Passo 3 — Interrogar

Escreva o rascunho e marque **cada suposição** com `[PRECISA DECISÃO]`. Depois pergunte
apenas sobre elas — no máximo 5 por vez, com opções concretas, não perguntas abertas.

Perguntas que sempre valem a pena:
- O que acontece no caminho infeliz? (dado ausente, permissão negada, serviço fora)
- Isso muda algo que já está em produção?
- Qual o comportamento com volume grande / lista vazia?
- Quem pode fazer isso?

## Passo 4 — Escrever

Numere o diretório: próximo `NNN` livre em `specs/mudancas/`, 3 dígitos.
Use `specs/_templates/MUDANCA-spec.md`. Preencha tudo, especialmente:

- **Fora de escopo** — o que impede expansão silenciosa
- **RF numerados e testáveis** — se não dá para escrever o teste, o RF está vago
- **Critérios de aceite** em Dado/Quando/Então
- **Impacto no existente** com caminhos reais, obtidos por leitura do código

Atualize `specs/ACTIVE.md` com o id da mudança.

## Passo 5 — Parar

Nenhum `[PRECISA DECISÃO]` pode sobreviver. Resolva todos com o humano.

Depois: apresente um resumo curto e **pare**. Não gere plano, não escreva código.
O próximo passo é a skill `spec-plano`, e ele é do humano.

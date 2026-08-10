---
numero: 0003
titulo: Congelar a pilha de documentação com pins transitivos em vez de modernizá-la
status: aceito
data: 2026-08-10
substitui: —
substituido-por: —
modulos: []
---

# 0003 — Congelar a pilha de documentação com pins transitivos em vez de modernizá-la

## Contexto

O `poetry.lock` removido pela mudança 001 travava a pilha de documentação em versões de 2024.
Ao gerar o `uv.lock` do zero, com as **mesmas faixas declaradas**, o build da documentação
quebrou em três pontos encadeados:

| Pacote | Versão antiga | Resolução nova | Sintoma |
|---|---|---|---|
| `mkdocs-autorefs` | 1.0.1 | 1.4.4 | `AttributeError: 'dict' object has no attribute 'link_titles'` |
| `griffe` | 0.45.3 | 2.1.0 | `ModuleNotFoundError: No module named 'griffe.collections'` |
| `pygments` | 2.18.0 | 2.20.0 | `AttributeError: 'NoneType' object has no attribute 'replace'` no realce de código |

A raiz é comum: `mkdocstrings` está declarado em `^0.23.0`, versão de outubro de 2023, e
prende toda a cadeia a uma geração de APIs que os pacotes transitivos já abandonaram. O
lockfile antigo escondia isso — nunca foi uma pilha compatível, foi uma pilha congelada.

A descoberta aconteceu **no meio de uma migração de runtime, empacotador e cliente HTTP**.
Modernizar a documentação ali dentro somaria uma quarta frente ao diff e misturaria o risco.

## Decisão

Manter `mkdocstrings` em `^0.23.0` e **fixar os três transitivos** no grupo `doc`, com
comentário no `pyproject.toml` explicando o sintoma de cada um e a condição de remoção:

```
mkdocs-autorefs>=1.0.1,<1.1.0
griffe>=0.45.3,<1.0.0
pygments>=2.18.0,<2.19.0
```

É aceitação consciente de dívida: a pilha de documentação fica congelada até uma mudança
própria subir o `mkdocstrings`.

## Alternativas descartadas

| Alternativa | Por que não |
|---|---|
| Subir `mkdocstrings` para 0.30.x e `mkdocstrings-python` para 1.19.x agora | É a correção certa, mas é upgrade de versão maior — 🔴 RED por `03-limites-agente.md` — dentro de uma mudança que já trocava runtime, empacotador e cliente HTTP. Se o build de documentação quebrasse depois, não haveria como saber qual das quatro frentes causou |
| Não fixar nada e aceitar a documentação quebrada | O Read the Docs é a documentação pública do pacote. Entregar a migração com a doc quebrada transfere o problema para quem consome |
| Reproduzir o `poetry.lock` inteiro fixando todas as versões antigas | Congelaria também o que não tem problema, e transformaria o `pyproject.toml` num lockfile escrito à mão |

## Consequências

**Ganhamos:**
- O build da documentação volta a funcionar, com a migração isolada em três frentes
- Cada pin carrega no próprio arquivo o motivo e a condição de saída — não vira mistério

**Pagamos:**
- Três pins que não descrevem uma necessidade do projeto, e sim uma incompatibilidade de
  terceiros
- A pilha de documentação fica presa a uma geração antiga, sem correções nem recursos novos
- Qualquer pacote novo no grupo `doc` pode colidir com esses limites

**Fica mais difícil depois:**
- Quanto mais tempo passar, maior o salto do `mkdocstrings` quando ele finalmente subir
- Um quarto sintoma pode aparecer em outro transitivo ainda não fixado, com a mesma raiz

## Como reverter

A reversão **é** a modernização: subir `mkdocstrings` e `mkdocstrings-python` para versões que
falem com `griffe` 2.x, remover os três pins e conferir o build no Read the Docs. Barato em
código, e o único risco é a renderização mudar de aparência. Merece mudança própria, não um
"aproveitar a viagem".

## Sinais de que esta decisão envelheceu

- Um quarto pin transitivo se tornar necessário para manter o build de pé
- Algum pin entrar em conflito com uma dependência de documentação que se queira adicionar
- `pygments` ou `griffe` na faixa fixada receberem aviso de segurança
- O tema `mkdocs-material` exigir uma versão de `pymdown-extensions` incompatível com o pin de
  `pygments`

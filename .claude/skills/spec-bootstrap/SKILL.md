---
name: spec-bootstrap
description: Entrevista o desenvolvedor e preenche a base de specs (specs/) de um projeto novo ou já existente, depois conecta tudo ao CLAUDE.md. Use sempre que o usuário pedir para inicializar, configurar, adotar ou "ligar" o sistema de specs, quando mencionar preencher a governança/constituição do projeto, quando houver marcadores <<PREENCHER>> em specs/, ou quando pedir para o Claude Code passar a seguir as specs do projeto. Use também quando o usuário acabar de descompactar ou copiar a pasta specs/ para um repositório.
---

# spec-bootstrap

Preenche a base de specs por **entrevista**, nunca por suposição.

## Princípio inegociável

Você **não inventa** conteúdo de spec. Cada fato preenchido vem de (a) resposta do humano,
ou (b) leitura direta do código, apresentada ao humano e **confirmada** por ele.

Se você não tem o fato, deixa `<<PREENCHER: ...>>` e diz explicitamente o que ficou pendente.
Spec inventada é pior que spec vazia: o agente futuro vai confiar nela.

## Fase 0 — Reconhecimento

1. Verifique se `specs/` existe. Se não existir, avise que a base precisa ser copiada antes.
2. Determine o tipo de projeto:
   - **Existente:** há código-fonte além de config.
   - **Novo:** repositório vazio ou só scaffolding.
3. Se **existente**, delegue a varredura para um subagente de exploração (read-only) e peça:
   - linguagens, frameworks e versões (a partir de arquivos de manifesto)
   - layout de diretórios de topo e o padrão que ele sugere
   - módulos / bounded contexts aparentes
   - rotas de API e rotas de frontend existentes
   - entidades / modelos de dados
   - biblioteca de componentes e origem dos tokens visuais
   - comandos reais (scripts de package manager, Makefile, CI)
   - o que já existe de doc (README, ADRs, comentários de arquitetura)

   Subagente evita que a varredura consuma o contexto principal.

4. Apresente o resultado como **proposta**, em tabela, e peça confirmação:
   > "Detectei isto. Confirma, corrige ou completa?"

   Nunca escreva em `specs/` antes desta confirmação.

## Fase 1 — Entrevista

Regras da entrevista:
- **Um bloco por vez.** Espere a resposta antes do próximo.
- Ofereça o que você detectou como resposta padrão — o humano só corrige.
- Aceite "não sei" e "depois": vira `<<PREENCHER>>`, não vira invenção.
- No máximo 5 perguntas por bloco.
- **Escreva os arquivos de cada bloco antes de passar ao próximo.** Se a conversa for
  interrompida, o que já foi respondido está salvo.

### Bloco A — Produto → `visao/PRODUTO.md`, `visao/GLOSSARIO.md`
1. O que o sistema faz, em uma frase?
2. Que problema resolve, para quem, e qual é a alternativa que as pessoas usam hoje?
3. O que ele explicitamente **não** faz? (não-objetivos)
4. Quais termos de domínio um dev novo entenderia errado?
5. Alguma restrição dura — prazo, regulatório, integração obrigatória, legado intocável?

### Bloco B — Escopo técnico → `arquitetura/VISAO_TECNICA.md`
1. O projeto tem backend, frontend, ambos, mobile? Monorepo ou repos separados?
2. Stack e versões por camada (confirme o detectado).
3. Como backend e frontend mantêm o contrato em sincronia — codegen, tipos compartilhados, manual?
4. Quais processos existem além do servidor web (workers, cron, filas)?
5. Quais ambientes existem e o que difere entre eles?

Se **não houver frontend**, remova `specs/ui/` e as linhas de UI do DoD. Não deixe seção
vazia — seção vazia vira ruído de contexto.
Se **não houver backend**, remova `dados/` e as linhas de backend do DoD.

### Bloco C — Convenções → `governanca/02-convencoes.md`
1. Onde vai cada tipo de coisa? (peça 5 a 8 linhas de "onde-vai-o-X" com caminhos reais)
2. Convenções de nomeação e sufixos obrigatórios.
3. Comandos exatos: instalar, rodar, testar, lint, type-check, build, migration.
4. Padrão de commit e de branch.
5. Idioma de mensagem ao usuário final e de commit.

### Bloco D — Constituição → `governanca/01-constituicao.md`
1. Quais regras de dependência entre camadas nunca podem ser violadas?
2. O que um code review reprovaria automaticamente neste projeto?
3. Que padrão o projeto segue hoje que um agente provavelmente quebraria por não saber?
4. Que dívida existe hoje que **não** deve ser "consertada de surpresa"?

Pergunta 4 é a mais importante e a mais esquecida: agente que "melhora" código legado
sem pedir causa mais dano que ausência de spec.

### Bloco E — Limites → `governanca/03-limites-agente.md`
1. O que o agente **nunca** pode fazer sem seu "pode ir" literal? (além da lista padrão RED)
2. Quais diretórios ou arquivos são intocáveis?
3. Existe dado real, produção ou integração com terceiro no ambiente local?

### Bloco F — Qualidade → `governanca/04-definition-of-done.md`, `testes/ESTRATEGIA.md`
1. O que se testa e o que deliberadamente não se testa?
2. Ferramentas de teste por nível e comandos.
3. Meta de cobertura e se o CI bloqueia.
4. Gates extras: bundle, performance, verificação visual, segurança.

### Bloco G — Frontend → `ui/DESIGN_SYSTEM.md`, `ui/COMPONENTES.md`
*(pule inteiro se não houver frontend)*
1. Design system próprio, biblioteca de terceiros, ou híbrido? Qual e versão?
2. Como os tokens são definidos e consumidos hoje?
3. Meta de acessibilidade (nível, contraste, suporte a leitor de tela)?
4. Breakpoints e comportamento em cada um.
5. Quais componentes compartilhados já existem? (confirme o detectado)

### Bloco H — Dados → `dados/INDICE.md`
*(pule se não houver persistência)*
1. Banco, ORM, ferramenta de migration.
2. Multi-tenancy? Qual estratégia?
3. Convenções universais: chave primária, timestamps, soft delete, auditoria.
4. Confirme a lista de entidades detectada e a que contexto cada uma pertence.

### Bloco I — Rigor → hook e `CLAUDE.md`
Pergunte, com o trade-off explícito:

> Quer o modo **estrito** ou **consultivo**?
> - **Estrito:** um hook bloqueia edições em código quando não há mudança especificada e
>   aprovada. Garantia real, atrito real. Bom para repositório de time ou contexto regulado.
> - **Consultivo:** as skills orientam, nada bloqueia. Sem atrito, e depende de disciplina —
>   em sessão longa a regra pode ser despriorizada.

Se escolher estrito: instale `.claude/hooks/require-spec.sh`, registre em
`.claude/settings.json` e **ajuste os caminhos protegidos** aos diretórios reais do projeto.
Se consultivo: não instale o hook e diga que ele pode ser ligado depois.

## Fase 2 — Estado atual (só projeto existente)

Para cada módulo e tela detectados, crie o arquivo a partir do template com os checklists
**marcados conforme o código real**. Não invente requisito: descreva o que existe.

Ordem: comece pelos 2 ou 3 módulos mais movimentados. Os demais ficam com stub e
`<<PREENCHER>>`. Cobertura parcial honesta vale mais que cobertura total fabricada.

Se encontrar decisão arquitetural evidente e não registrada, proponha um ADR retroativo com
status `aceito` e data estimada — mas **só escreva depois de o humano confirmar o "porquê"**.
O porquê não está no código.

## Fase 3 — Conectar ao CLAUDE.md

1. Se `CLAUDE.md` não existe, crie.
2. Insira o bloco de `.claude/CLAUDE.md.bloco` entre os marcadores
   `<!-- SPEC-BASE:INICIO -->` e `<!-- SPEC-BASE:FIM -->`.
3. Se os marcadores já existem, **substitua só o conteúdo entre eles**. Nunca sobrescreva
   o resto do arquivo.
4. Preencha os placeholders do bloco com os caminhos reais deste projeto.

## Fase 4 — Fechamento

Rode `python3 scripts/spec_status.py` e apresente:

- tabela do que foi preenchido, por arquivo
- lista dos `<<PREENCHER>>` restantes, ordenada por impacto
- modo escolhido (estrito/consultivo) e o que isso significa na prática
- **os 3 próximos passos**, concretos

Termine com uma pergunta única: qual pendência atacar primeiro.

## Erros a evitar

| Erro | Em vez disso |
|---|---|
| Fazer todas as perguntas de uma vez | Um bloco por vez, escrevendo entre eles |
| Preencher com genérico plausível | Deixar `<<PREENCHER>>` e nomear a lacuna |
| Escrever antes de confirmar a detecção | Propor em tabela, esperar o "confirma" |
| Manter seções que não se aplicam | Remover `ui/` ou `dados/` se não houver |
| Escrever ADR retroativo pelo código | Perguntar o porquê ao humano primeiro |
| Sobrescrever o CLAUDE.md existente | Editar só entre os marcadores |

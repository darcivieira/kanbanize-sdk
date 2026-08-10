# Limites do agente — GREEN / YELLOW / RED

**Classifique toda mudança antes de tocar em qualquer arquivo.** Em caso de dúvida entre
dois níveis, assuma o mais alto. Declare a classificação em voz alta antes de agir.

---

## 🟢 GREEN — pode executar direto

Sem spec, sem aprovação. Reversível e de escopo local.

- Correção de typo, comentário, texto de log
- Formatação, lint, organização de imports
- Teste novo que não altera comportamento de produção
- Refactor local que **não muda assinatura pública nem comportamento observável**
- Correção de bug com causa evidente, em um arquivo, com teste que a comprova
- Preencher um marcador de pendência em spec a partir de informação que o humano acabou de dar

**Regra de corte:** se você não consegue descrever a mudança em uma frase sem "e",
não é GREEN.

---

## 🟡 YELLOW — exige spec de mudança antes de codar

Fluxo obrigatório: `spec-nova` → `spec-plano` → aprovação humana → implementar.

- Endpoint, rota, tela ou componente compartilhado novo
- Mudança de comportamento visível ao usuário
- Alteração aditiva de schema (coluna nova nullable, campo opcional)
- Mudança que toca **3 ou mais módulos/arquivos**
- Qualquer requisito com ambiguidade real (você precisaria supor algo para prosseguir)
- Alteração em regra de negócio existente
- Mudança de estado/fluxo de dados no frontend que afeta mais de uma tela

---

## 🔴 RED — exige spec + ADR + aprovação humana explícita

Nunca execute sem um "pode ir" literal do humano nesta conversa.

- Migration destrutiva ou de perda de dados (drop, rename, mudança de tipo, backfill)
- Quebra de contrato público (API, evento, formato de arquivo, props de componente exportado)
- Dependência nova, remoção de dependência, ou upgrade de versão maior
- Autenticação, autorização, criptografia, gestão de segredos, multi-tenancy
- Alteração em `specs/governanca/01-constituicao.md`
- Exclusão de arquivos, `git reset`, `git push --force`, reescrita de histórico
- Mudança em CI/CD, infraestrutura, ou qualquer coisa que toque produção
- Introduzir camada, padrão arquitetural ou biblioteca de estado novos
- Manipular dados reais de usuário

### RED específicos deste projeto

O pacote é público no PyPI em `0.3.x` e consumido por gente desconhecida. Tudo abaixo é
quebra de contrato ou mudança de infraestrutura:

- **Renomear ou remover qualquer símbolo** exportado em `kanbanize_sdk/__init__.py` ou
  `kanbanize_sdk/endpoints/__init__.py`
- **Mudar a assinatura** de um método público de recurso — nome, ordem ou obrigatoriedade de
  parâmetro
- **Mudar o verbo HTTP ou o path** de um método já existente
- **Mexer em `kanbanize_sdk/wrapper.py`** — é o ponto único de transporte, de headers e de
  tratamento de erro; qualquer alteração ali atinge os ~130 métodos de uma vez
- **Subir a versão** em `pyproject.toml` ou **publicar no PyPI**
- **Alterar `.github/workflows/pipeline.yml` ou `.readthedocs.yaml`**
- **Qualquer um dos itens de migração** do `visao/ROADMAP.md` ainda abertos: modo async e
  publicação via CI
- **Fazer uma requisição HTTP real** contra a Kanbanize — ver seção abaixo, é proibição
  absoluta, não RED negociável

---

## Arquivos intocáveis

| Arquivo / diretório | Regra |
|---|---|
| `uv.lock` | Nunca editar à mão. Só muda como efeito de um comando `uv`, e a mudança de dependência que o gerou já é 🔴 RED |
| `LICENSE` | Só o preenchimento dos placeholders `[year]` / `[fullname]`, que é dívida aberta. Trocar a licença é 🔴 RED |
| `.github/` | Qualquer arquivo. CI é 🔴 RED |
| `.readthedocs.yaml` | 🔴 RED |
| `.idea/` | Config de IDE do mantenedor. Não é do agente |

---

## Proibição absoluta: nenhuma chamada HTTP real

**O agente nunca faz uma requisição contra a API da Kanbanize.** Não para conferir um
contrato, não para "só testar", não com subdomínio de exemplo. Não existe autorização
pontual para isso.

Não há api_key nem subdomínio real em nenhum lugar do ambiente — nem em arquivo, nem em
variável de ambiente. Se o agente encontrar algo que pareça uma credencial real, **pare e
avise**; não use.

Todo teste é mockado com `pytest-httpx`, seguindo estritamente a documentação fornecida.

**Consequência prática, e é importante:** o OpenAPI da conta
(`https://{subdomain}.kanbanize.com/openapi`) é a fonte da verdade do contrato, mas está atrás
do subdomínio do mantenedor — **o agente não consegue lê-lo**. Então, ao criar ou alterar um
recurso, o agente **não deve inferir path, verbo ou nome de campo** por analogia com outro
recurso, por convenção REST ou por memória. Deve **pedir ao humano** o trecho da documentação
e transcrevê-lo. Contrato inventado passa em todos os testes e chega ao PyPI quebrado.

---

## Protocolo de bloqueio

Ao identificar YELLOW ou RED, **pare antes de editar** e responda no formato:

```
CLASSIFICAÇÃO: 🟡 YELLOW
MOTIVO: cria endpoint novo e toca 4 arquivos
PRÓXIMO PASSO: rodar a skill `spec-nova` para especificar antes de implementar
```

Se o humano pedir para pular a spec, isso é permitido — mas registre no commit
`[spec-skip]` e o motivo. Nunca pule silenciosamente.

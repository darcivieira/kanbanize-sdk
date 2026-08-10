# Produto

## O que é

Biblioteca Python que encapsula a API v2 da plataforma Kanbanize/Businessmap, expondo cada
recurso REST como método tipado e cada payload como dataclass.

Distribuída publicamente como pacote `kanbanize-sdk` no PyPI, sob licença MIT.

## Problema

Quem precisa integrar com a Kanbanize hoje escreve o próprio adapter: monta as chamadas
`requests` na mão, descobre o formato de cada payload por tentativa contra a documentação da
plataforma, e repete em todo projeto o mesmo desembrulho do envelope `data`/`pagination` que a
API devolve.

Esse adapter é reescrito do zero a cada integração, por cada pessoa, sem ganho acumulado.

## Para quem

| Perfil | O que precisa fazer |
|---|---|
| Dev que constrói uma integração com a Kanbanize | Chamar um endpoint e receber dados estruturados corretos, sem construir adapter próprio |
| Mantenedor do SDK | Acrescentar cobertura de endpoint sem quebrar quem já consome |

O projeto é **aberto**: o consumidor não é conhecido nem controlado. Qualquer pessoa pode
instalar do PyPI e construir sua integração em cima.

## Proposta de valor

Um único adapter, mantido em um lugar, que referencia **todos** os endpoints da API e entrega
os dados já estruturados — para que N projetos diferentes integrem sem cada um recriar a
mesma camada de transporte.

## Não-objetivos

O SDK **não armazena e não manipula dados**. Ele é um adapter de requisição: recebe
parâmetros, chama a API, devolve o que a API respondeu (sem o envelope). Tudo abaixo é
deliberadamente fora de escopo:

- **Não persiste nada** — sem banco, sem ORM, sem migration, sem cache em disco ou memória.
- **Não transforma o dado de negócio** — a única transformação é remover o envelope `data`
  da resposta da API.
- **Não valida payload localmente** — a validação é responsabilidade da API remota.
- **Não faz retry, backoff nem controle de rate limit** — HTTP `429` é propagado como erro.
- **Não oferece cliente assíncrono** hoje (ver `ROADMAP.md` — está previsto).
- **Não cobre os recursos de cards** da API v2. A cobertura atual é: users, teams, workspaces,
  boards e a estrutura de board (workflows, lanes, columns, limites, áreas mescladas).
- **Não é CLI nem serviço.** É biblioteca importável — não há entrypoint executável.

## Métricas de sucesso

<<PREENCHER: como se sabe que está funcionando. Candidatos possíveis, ainda não escolhidos:
downloads no PyPI, número de endpoints da API v2 cobertos vs total, issues abertas por
contrato incorreto, cobertura de testes. Nenhuma foi confirmada pelo mantenedor.>>

## Restrições

| Restrição | Natureza |
|---|---|
| Pacote público no PyPI em `0.3.x` — renomear ou remover símbolo exportado quebra consumidores desconhecidos | Contrato público |
| Python 3.13 como mínimo suportado, fixado no CI e no Read the Docs | Ambiente |
| `httpx` é a única dependência de runtime — manter assim é decisão, não acaso | Arquitetura |
| A API v2 da Kanbanize é externa e não versionada pelo mantenedor — mudança lá quebra aqui, sem aviso | Dependência externa |

Sem prazo, sem restrição regulatória e sem consumidor nomeado que não possa quebrar —
o compromisso é com o público anônimo do PyPI, não com um cliente específico.

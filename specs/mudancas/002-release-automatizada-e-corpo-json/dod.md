# Definition of Done — 002, verificado em 2026-08-11

Percorrido item a item de `specs/governanca/04-definition-of-done.md` contra o código da
branch `release_automation_and_json_body`, commit `c66346d`, com o CI verde.

Legenda: ☑ verificado · ☐ **não** verificado · ➖ não se aplica

## Sempre

- ☑ Comportamento bate com `spec.md` — 15 dos 16 RFs verificados por execução; RF-13 depende
  da release
- ☑ Nenhum requisito sem implementação ou sem justificativa — RF-13 é a T-9, do mantenedor
- ☑ Spec de estado atualizada — `02-convencoes.md`, `ROADMAP.md`, `VISAO_TECNICA.md`,
  `ESTRATEGIA.md`, `modulos/boards.md`, `modulos/users.md`
- ➖ Lint e type-check — **não existem neste projeto**. Não rodados, não fingidos
- ☑ Testes passam — 128, e os 30 testes de escrita passaram a afirmar o corpo enviado
- ☑ Sem `TODO`, código morto ou comentado
- ☑ Sem segredo ou dado real — o workflow não guarda token; testes seguem com credencial
  fictícia
- ☑ Erros tratados com contexto — `assert_json_body` falha nomeando o defeito e mostrando o
  content-type e o corpo, em vez de um `JSONDecodeError` cru
- ☑ Decisão não-óbvia registrada como ADR — 0004 e 0005

## Biblioteca cliente HTTP

- ➖ Path, verbo e nomes de campo contra a documentação — nenhum contrato de API foi tocado;
  path e verbo das 29 chamadas estão idênticos
- ➖ Método novo com type hints e docstring — nenhum método público de recurso foi criado
- ☑ Payload aceita dataclass ou `dict` — preservado, e agora **coberto por teste** nos dois
  caminhos (`test_insert_board` e `test_insert_board_with_a_raw_dict_body`)
- ➖ Método herdado desligado com `utils.private` — nenhum recurso novo
- ☑ Nenhuma importação de `httpx` fora de `wrapper.py`
- ☑ Nenhum símbolo público renomeado ou removido — diff vazio em `kanbanize_sdk/__init__.py` e
  `endpoints/__init__.py`
- ➖ Recurso novo exportado / fabricado — nenhum
- ➖ Dataclass nova exportada — nenhuma
- ➖ `docs/api/<recurso>.md` — nenhum recurso novo
- ☑ Teste com `pytest-httpx` e marker declarado — 128 testes; nenhum marker novo foi
  necessário
- ☑ Nenhum subdomínio ou api_key real

## Gates de qualidade

- ☑ Suíte verde com **128 testes** — local e no CI (run `31482918222`)
- ☑ Cobertura **99%**, acima da meta de 95%
- ☑ Nenhum teste acessa a rede real

## Verificações próprias desta mudança

- ☑ **A asserção de corpo tem dentes.** Reverter `Boards.insert` para `data=` faz o teste
  falhar com `body is not JSON. content-type='application/json'
  content=b'workspace_id=0&name=Teste&description=Description+test'` — que é exatamente o
  defeito que a mudança corrige
- ☑ **A conferência de tag funciona nos quatro casos** testados localmente: `v0.3.0` passa;
  `v0.9.9`, `0.3.0` (sem `v`) e `v0.3.0-rc1` falham
- ☑ **O `release.yml` não dispara em push** — o push do commit `c66346d` acionou apenas o
  workflow `Kanbanize-sdk` (RNF-5)

## Itens que ficaram por verificar

- ☐ **RF-13** — `pip install kanbanize-sdk==0.3.0` só é verificável depois da release (T-9).
- ☐ **RF-8 e RF-15 em execução real** — o Trusted Publishing e o environment `pypi` estão
  declarados no workflow, mas só a primeira release prova que a autenticação OIDC funciona.
  Depende da T-7, que é do mantenedor.
- ☐ **A API aceitar corpo JSON.** Os 34 pontos de asserção provam o que o SDK **envia**;
  nenhum teste prova o que a Kanbanize **aceita**. Registrado como dívida permanente em
  `visao/ROADMAP.md`.

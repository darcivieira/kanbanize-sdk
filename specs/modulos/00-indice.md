# Índice de recursos

Um arquivo de spec por recurso, criado sob demanda. Marcado = tem spec de estado escrita.
Desmarcado = o recurso existe no código, mas ainda não foi especificado.

Cobertura parcial honesta vale mais que cobertura total fabricada: não crie um arquivo aqui
sem transcrever o contrato real a partir da documentação da API.

## Users e Teams

- [x] `users.md` — `Users`
- [ ] `teams.md` — `Teams`

## Workspaces

- [ ] `workspaces.md` — `Workspaces`
- [ ] `workspace-managers.md` — `WorkspaceManagers`
- [ ] `workspace-history.md` — `WorkspaceHistory`
- [ ] `managed-workspaces.md` — `ManagedWorkspaces`

## Boards — núcleo

- [x] `boards.md` — `Boards`
- [ ] `board-settings.md` — `BoardSettings`
- [ ] `board-structure.md` — `BoardStructure`
- [ ] `board-structure-revisions.md` — `BoardStructureRevisions`
- [ ] `board-history.md` — `BoardHistory`

## Boards — configuração

- [ ] `board-assignees.md` — `BoardAssignees` (endpoint real: `/userRoles`)
- [ ] `board-teams.md` — `BoardTeams`
- [ ] `board-tags.md` — `BoardTags`
- [ ] `board-visible-standard-fields.md` — `BoardVisibleStandardFields`
- [ ] `board-stickers.md` — `BoardStickers`
- [ ] `board-custom-fields.md` — `BoardCustomFields`
- [ ] `board-custom-field-allowed-values.md` — `BoardCustomFieldAllowedValues`
- [ ] `board-custom-field-default-contributors.md` — `BoardCustomFieldDefaultContributors`
- [ ] `board-discard-reasons.md` — `BoardDiscardReasons`
- [ ] `board-block-reasons.md` — `BoardBlockReasons`
- [ ] `board-card-types.md` — `BoardCardTypes`
- [ ] `board-card-templates.md` — `BoardCardTemplates`
- [ ] `board-child-parent-cards.md` — `BoardChildParentCards` — **classe vazia, sem métodos e
      sem teste.** Especificar exige a documentação da API; ver `visao/ROADMAP.md`

## Estrutura de board

- [ ] `workflows.md` — `Workflows`
- [ ] `lanes.md` — `Lanes`
- [ ] `columns.md` — `Columns`
- [ ] `cell-limits.md` — `CellLimits`
- [ ] `merged-areas.md` — `MergedAreas`
- [ ] `lane-section-limits.md` — `LaneSectionLimits`

## Camadas transversais

Não têm arquivo próprio — o comportamento é dono de `arquitetura/VISAO_TECNICA.md`:

| Componente | Onde está especificado |
|---|---|
| `Kanbanize` (fachada) | Topologia |
| `KanbanizeSession` (transporte, headers, status) | Camadas + Fluxo 4 |
| `GenericRequestMethod` | Camadas |
| `utils.private` | `governanca/05-anatomia.md` |
| Dataclasses de params e body | o recurso que as usa |

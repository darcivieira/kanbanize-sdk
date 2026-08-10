# Tela: <nome>

> Dono do fato: rota, estados e dados desta tela.

## Rota
`/caminho` — <pública | autenticada | papel exigido>

## Objetivo do usuário
<o que a pessoa vem fazer aqui. Uma frase, na voz do usuário.>

## Dados consumidos
| Origem | Endpoint / query | Quando | Cache |
|---|---|---|---|

## Estados (todos obrigatórios)

| Estado | O que aparece | Ação disponível |
|---|---|---|
| Carregando | | |
| Vazio | | |
| Erro | | |
| Sucesso | | |
| Sem permissão | | |

Estado vazio e estado de erro **não são opcionais**. Tela que só trata o caminho feliz
não passa no DoD.

## Composição
| Componente | Origem | Props principais |
|---|---|---|

## Interações
| Gatilho | Efeito | Feedback ao usuário | Reversível? |
|---|---|---|---|

## Validação de formulário
| Campo | Regra | Mensagem | Quando valida |
|---|---|---|---|

## Acessibilidade
- [ ] Navegável só por teclado, ordem de foco correta
- [ ] Foco visível em todo controle
- [ ] Rótulo acessível em cada campo e botão de ícone
- [ ] Erro de formulário anunciado e associado ao campo
- [ ] Contraste conforme meta do design system
- [ ] Título de página único e descritivo

## Responsividade
| Breakpoint | Layout |
|---|---|

## Progresso
- [ ] rota e navegação
- [ ] estado de sucesso
- [ ] estados de carregando / vazio / erro
- [ ] acessibilidade
- [ ] responsividade
- [ ] testes

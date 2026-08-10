#!/usr/bin/env bash
# Bloqueia edições em código de produção quando não há mudança especificada e aprovada.
# Registrar em .claude/settings.json sob hooks.PreToolUse, matcher "Edit|Write".
# Exit 0 = permite | Exit 2 = nega e devolve a mensagem ao agente.

set -uo pipefail
input=$(cat)

# --- AJUSTE AQUI: caminhos de código protegidos ------------------------------
# kanbanize-sdk: o código de produção é o pacote. Somam-se os arquivos de
# empacotamento e CI, classificados como RED em specs/governanca/03-limites-agente.md.
# Livres: tests/, docs/, specs/, README.md, .idea/
PROTEGIDOS_REGEX='^(kanbanize_sdk/|\.github/|pyproject\.toml$|uv\.lock$|\.readthedocs\.yaml$|\.python-version$)'
# -----------------------------------------------------------------------------

path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)
[ -z "$path" ] && exit 0

rel="${path#"$CLAUDE_PROJECT_DIR"/}"

# Fora do código protegido: libera (specs, docs, config, testes)
printf '%s' "$rel" | grep -Eq "$PROTEGIDOS_REGEX" || exit 0

# Testes e specs são sempre liberados
printf '%s' "$rel" | grep -Eq '(^|/)(tests?|__tests__|specs)/|\.(test|spec)\.[jt]sx?$|_test\.py$' && exit 0

SPECS="${CLAUDE_PROJECT_DIR:-.}/specs"
ACTIVE="$SPECS/ACTIVE.md"

if [ ! -f "$ACTIVE" ]; then
  echo "BLOQUEADO: specs/ACTIVE.md não existe. Rode a skill spec-bootstrap." >&2
  exit 2
fi

id=$(head -n1 "$ACTIVE" | tr -d '\r\n[:space:]')

if [ -z "$id" ] || [ "$id" = "nenhuma" ]; then
  cat >&2 <<MSG
BLOQUEADO: não há mudança ativa em specs/ACTIVE.md.
Arquivo alvo: $rel

Classifique a mudança em specs/governanca/03-limites-agente.md.
  - GREEN  -> registre a exceção: echo "GREEN: <motivo>" > specs/ACTIVE.md
  - YELLOW/RED -> rode a skill spec-nova antes de editar código.
MSG
  exit 2
fi

# Exceção GREEN declarada explicitamente
case "$id" in GREEN:*) exit 0 ;; esac

dir="$SPECS/mudancas/$id"
if [ ! -d "$dir" ]; then
  echo "BLOQUEADO: ACTIVE.md aponta para '$id', mas specs/mudancas/$id não existe." >&2
  exit 2
fi

if [ ! -f "$dir/plan.md" ]; then
  echo "BLOQUEADO: a mudança '$id' não tem plan.md. Rode a skill spec-plano." >&2
  exit 2
fi

if ! grep -q '^\*\*Aprovação humana:\*\* ☑' "$dir/plan.md"; then
  cat >&2 <<MSG
BLOQUEADO: o plano de '$id' ainda não foi aprovado.
Apresente o plano ao humano. Após o "pode ir", ele marca a caixa em:
  $dir/plan.md   ->   **Aprovação humana:** ☑ aprovado
MSG
  exit 2
fi

exit 0

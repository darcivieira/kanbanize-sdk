#!/usr/bin/env python3
"""Relatório de saúde da base de specs. Sem dependências externas.

Uso:
    python3 scripts/spec_status.py            # relatório completo
    python3 scripts/spec_status.py --pendentes # só os <<PREENCHER>>
    python3 scripts/spec_status.py --ci        # exit 1 se houver spec de estado vazia
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SPECS = RAIZ / "specs"

RE_PREENCHER = re.compile(r"<<PREENCHER:?([^>]*)>>", re.S)
RE_CHECK = re.compile(r"^\s*[-*]\s*\[( |x|X)\]\s+(.*)$", re.M)
RE_DECISAO = re.compile(r"\[PRECISA DECISÃO\]")


def arquivos_md() -> list[Path]:
    if not SPECS.exists():
        sys.exit(f"erro: {SPECS} não encontrado. Rode a partir da raiz do projeto.")
    return sorted(p for p in SPECS.rglob("*.md") if "_templates" not in p.parts)


def rel(p: Path) -> str:
    return str(p.relative_to(RAIZ))


def main() -> int:
    args = set(sys.argv[1:])
    so_pendentes = "--pendentes" in args
    modo_ci = "--ci" in args

    pendentes: list[tuple[str, str]] = []
    checks: dict[str, tuple[int, int]] = {}
    decisoes: list[str] = []

    for p in arquivos_md():
        texto = p.read_text(encoding="utf-8", errors="replace")
        for m in RE_PREENCHER.finditer(texto):
            desc = " ".join(m.group(1).split())[:90] or "(sem descrição)"
            pendentes.append((rel(p), desc))
        marcados = RE_CHECK.findall(texto)
        if marcados:
            feitos = sum(1 for estado, _ in marcados if estado.lower() == "x")
            checks[rel(p)] = (feitos, len(marcados))
        if RE_DECISAO.search(texto):
            decisoes.append(rel(p))

    if not so_pendentes:
        ativa = (SPECS / "ACTIVE.md")
        atual = ativa.read_text(encoding="utf-8").strip().splitlines()[0] if ativa.exists() else "—"
        print("=" * 66)
        print(f"MUDANÇA ATIVA: {atual}")
        print("=" * 66)

        if checks:
            print("\nPROGRESSO POR SPEC")
            for arq, (feitos, total) in sorted(checks.items()):
                pct = round(100 * feitos / total)
                barra = "█" * (pct // 10) + "·" * (10 - pct // 10)
                print(f"  {barra} {pct:3d}%  {feitos:3d}/{total:<3d}  {arq}")

    if pendentes:
        print(f"\nCAMPOS NÃO PREENCHIDOS ({len(pendentes)})")
        atual = None
        for arq, desc in pendentes:
            if arq != atual:
                print(f"\n  {arq}")
                atual = arq
            print(f"    · {desc}")
    else:
        print("\nNenhum <<PREENCHER>> restante.")

    if decisoes:
        print(f"\n⚠ [PRECISA DECISÃO] em aberto ({len(decisoes)})")
        for arq in decisoes:
            print(f"    · {arq}")

    if modo_ci:
        criticos = [a for a, _ in pendentes if "/governanca/" in a]
        if criticos:
            print(f"\nCI: {len(set(criticos))} arquivo(s) de governança incompletos.")
            return 1
        if decisoes:
            print("\nCI: há [PRECISA DECISÃO] em aberto.")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

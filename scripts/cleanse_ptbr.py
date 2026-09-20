#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Purificação com Modelo Rival (Deslop PT-BR Cleanse)
Executa a limpeza de textos gerados por IA utilizando uma família de modelos DIFERENTE
daquela que redigiu o rascunho.

A regra fundamental: um modelo é péssimo para ouvir o próprio sotaque.
Um modelo rival ouve os vícios instantaneamente.

Roteamento automático:
- Se escrito por Claude (ou no Claude Code): chama 'codex exec' (OpenAI / GPT-5/4o)
- Se escrito por GPT (ou no Codex): chama 'claude -p' (Anthropic)
- Se no Gemini CLI: chama o CLI rival disponível
- Se nenhum CLI estiver instalado: exibe o prompt formatado para colar no chat da outra IA

O texto limpo é emitido no STDOUT (para permitir redirecionamento direto: cleanse_ptbr.py draft.md > limpo.md).
As notas de edição são emitidas no STDERR (para visualização no console).
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path

# Suporte UTF-8 no Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SENTINELA_NOTAS = "<<<DESLOP-PTBR-NOTAS>>>"


def carregar_prompt_mestre() -> str:
    """Carrega o prompt mestre de cleanse do diretório prompts/."""
    caminho_base = Path(__file__).resolve().parent.parent
    caminho_prompt = caminho_base / "prompts" / "cleanse_ptbr.txt"
    if not caminho_prompt.is_file():
        sys.stderr.write(f"deslop-cleanse: erro — arquivo de prompt não encontrado em '{caminho_prompt}'.\n")
        sys.exit(2)
    return caminho_prompt.read_text(encoding="utf-8", errors="replace")


def separar_corpo_e_notas(resposta: str):
    """Separa o texto limpo (acima do sentinela) das notas da edição (abaixo do sentinela)."""
    if SENTINELA_NOTAS in resposta:
        partes = resposta.split(SENTINELA_NOTAS, 1)
        corpo = partes[0].rstrip()
        notas = partes[1].strip()
        return corpo, notas
    else:
        # Se o modelo esqueceu o sentinela, emite tudo como corpo e avisa no stderr
        aviso = (
            "deslop-cleanse: AVISO — marcador de sentinela não encontrado na resposta do modelo.\n"
            "Emitindo todo o conteúdo como texto. Verifique o final do arquivo antes de publicar.\n"
        )
        sys.stderr.write(aviso)
        return resposta.rstrip(), ""


def executar_comando_com_timeout(cmd_lista, timeout_segundos: int):
    """Executa o comando da CLI com timeout seguro."""
    try:
        resultado = subprocess.run(
            cmd_lista,
            capture_output=True,
            text=True,
            timeout=timeout_segundos,
            encoding="utf-8",
            errors="replace"
        )
        return resultado.returncode, resultado.stdout, resultado.stderr
    except subprocess.TimeoutExpired:
        sys.stderr.write(f"deslop-cleanse: erro — timeout excedido ({timeout_segundos}s).\n")
        sys.exit(124)
    except FileNotFoundError:
        return 127, "", f"Comando '{cmd_lista[0]}' não encontrado no sistema."
    except Exception as e:
        return 1, "", str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Purificador com Modelo Rival em Português do Brasil (Deslop PT-BR Cleanse)"
    )
    parser.add_argument("arquivo", nargs="?", help="Arquivo Markdown ou texto para purificar (opcional se usar stdin)")
    parser.add_argument("--escritor", choices=["claude", "gpt", "gemini"], default=None,
                        help="Família do modelo que escreveu o rascunho original (default: detecta por variável de ambiente ou claude)")
    parser.add_argument("--timeout", type=int, default=180, help="Tempo limite em segundos para a chamada do modelo (default: 180s)")
    parser.add_argument("--apenas-prompt", action="store_true", help="Apenas exibe o prompt formatado sem chamar nenhum CLI")

    args = parser.parse_args()

    # Leitura do rascunho
    if args.arquivo:
        caminho = Path(args.arquivo)
        if not caminho.is_file():
            sys.stderr.write(f"deslop-cleanse: erro — arquivo '{args.arquivo}' não encontrado.\n")
            sys.exit(66)
        rascunho = caminho.read_text(encoding="utf-8", errors="replace")
    else:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        rascunho = sys.stdin.read()

    if not rascunho.strip():
        sys.stderr.write("deslop-cleanse: erro — rascunho vazio. Nada para purificar.\n")
        sys.exit(66)

    prompt_mestre = carregar_prompt_mestre()
    texto_completo = f"{prompt_mestre}\n\n{rascunho}"

    if args.apenas_prompt:
        print(texto_completo)
        sys.exit(0)

    # Identifica o autor do rascunho
    escritor = args.escritor or os.environ.get("DESLOP_ESCRITOR", "claude").lower()

    # Procura executáveis nos PATHs
    codex_bin = shutil.which("codex")
    claude_bin = shutil.which("claude")

    # Roteamento entre modelos rivais
    if codex_bin and escritor != "gpt":
        # Draft feito por Claude ou Gemini -> Purificado pelo GPT-5 / Codex
        sys.stderr.write("deslop-cleanse: roteando rascunho para limpeza via Codex / GPT...\n")
        cmd = [codex_bin, "exec", "--skip-git-repo-check", "--sandbox", "read-only", texto_completo]
        code, stdout, stderr = executar_comando_com_timeout(cmd, args.timeout)
        if code != 0:
            sys.stderr.write(f"deslop-cleanse: falha na execução do codex: {stderr}\n")
            sys.exit(code)
        
        # Extração limpa se o codex adicionar banners
        corpo, notas = separar_corpo_e_notas(stdout)
        print(corpo)
        if notas:
            sys.stderr.write("\n--- O QUE MUDOU (NOTAS DE EDIÇÃO) ---\n")
            sys.stderr.write(notas + "\n")
            sys.stderr.write("-------------------------------------\n")
        sys.exit(0)

    elif claude_bin and escritor == "gpt":
        # Draft feito por GPT -> Purificado pelo Claude CLI
        sys.stderr.write("deslop-cleanse: roteando rascunho para limpeza via Claude CLI...\n")
        cmd = [claude_bin, "-p", texto_completo]
        code, stdout, stderr = executar_comando_com_timeout(cmd, args.timeout)
        if code != 0:
            sys.stderr.write(f"deslop-cleanse: falha na execução do claude: {stderr}\n")
            sys.exit(code)

        corpo, notas = separar_corpo_e_notas(stdout)
        print(corpo)
        if notas:
            sys.stderr.write("\n--- O QUE MUDOU (NOTAS DE EDIÇÃO) ---\n")
            sys.stderr.write(notas + "\n")
            sys.stderr.write("-------------------------------------\n")
        sys.exit(0)

    else:
        # Nenhum CLI rival instalado ou CLI disponível é da mesma família do autor original
        sys.stderr.write(
            "deslop-cleanse: nenhum CLI de modelo rival encontrado.\n"
            "(Um rascunho escrito por Claude precisa do 'codex'; um rascunho de GPT precisa do 'claude').\n"
            "Copie o bloco abaixo e cole no chat da outra família de IA:\n\n"
        )
        print(texto_completo)
        sys.exit(127)


if __name__ == "__main__":
    main()

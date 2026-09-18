#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Vícios de Escrita de IA em Português do Brasil (Deslop PT-BR)
Analisa arquivos Markdown ou texto comum via CLI ou Stdin, calcula pontuação de IA (0 a 100)
e aponta os sinais de alerta (W1 a W36) com linha, citação e sugestão de correção.

Zero dependências externas (apenas biblioteca padrão do Python).
"""

import sys
import re
import argparse
import json
from pathlib import Path

# Configura suporte a UTF-8 no console do Windows sem estourar UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Definição dos Padrões e Regras de Detecção
RULES = [
    {
        "id": "W1",
        "nome": "Gerundismo Corporativo / SAC",
        "severidade": "Alta",
        "regex": r"\b(vou estar|vamos estar|estaremos|iremos estar|vai estar)\s+([a-zá-ú]+ndo)\b",
        "sugestao": "Substitua por verbo direto no presente ou futuro simples (ex: 'vou enviar', 'faremos')."
    },
    {
        "id": "W2",
        "nome": "Gerúndio Conclusivo de Falsa Análise",
        "severidade": "Alta",
        "regex": r",\s+(destacando|demonstrando|reforçando|evidenciando|consolidando|sublinhando|mostrando)\s+(a importância|o papel|o compromisso|a relevância|a necessidade|sua posição|que)\b",
        "sugestao": "Corte a oração de gerúndio redundante ou transforme-a em oração coordenada com fatos reais."
    },
    {
        "id": "W3",
        "nome": "Conectivos Arcaicos de Oficialês",
        "severidade": "Alta",
        "regex": r"\b(ademais|outrossim|destarte|doravante|não obstante|nesse diapasão|no bojo de|mister se faz|cumpre salientar|faz-se imperioso)\b",
        "sugestao": "Use conectivos diretos ('além disso', 'por isso', 'mas') ou corte e una as frases."
    },
    {
        "id": "W4",
        "nome": "Abertura Genérica (Throat-Clearing)",
        "severidade": "Alta",
        "regex": r"\b(no cenário atual|em um mundo cada vez mais|na era digital em que vivemos|vale ressaltar que|é importante notar que|é imperioso ressaltar)\b",
        "sugestao": "Delete a introdução e comece diretamente pelo sujeito e ação concreta."
    },
    {
        "id": "W5",
        "nome": "Contraste Binário Vazio",
        "severidade": "Alta",
        "regex": r"\b(não é sobre|não se trata de|não é apenas um[a]?|mais do que um[a]?)\b.*?\b(mas|é sobre|é um[a]?|uma verdadeira)\b",
        "sugestao": "Corte a negação e afirme a ideia positiva diretamente."
    },
    {
        "id": "W7",
        "nome": "Revelação Teatral com Dois-Pontos",
        "severidade": "Alta",
        "regex": r"\b(o detalhe crucial|o grande segredo|a melhor parte|o resultado|a questão é):",
        "sugestao": "Reescreva como frase declarativa direta comum."
    },
    {
        "id": "W8",
        "nome": "Adjetivo Inflado de Vendas / Falsa Grandiosidade",
        "severidade": "Alta",
        "regex": r"\b(revolucionário|revolucionária|divisor de águas|game-changer|sem atritos|seamless|meticulosamente|impecável|transformador[a]?)\b",
        "sugestao": "Troque por especificações técnicas, números ou métricas concretas."
    },
    {
        "id": "W9",
        "nome": "Falso Amigo de Tradução de IA",
        "severidade": "Alta",
        "regex": r"\b(mergulhar em|nos aprofundarmos|rica tapeçaria|orquestrando|orquestrar|alavancar|aninhad[oa] no coração)\b",
        "sugestao": "Use verbos naturais do português: 'analisar', 'examinar', 'conjunto', 'usar', 'fica em'."
    },
    {
        "id": "W10",
        "nome": "Abertura Falsa Celebração (Excited to Announce)",
        "severidade": "Alta",
        "regex": r"\b(temos o prazer de anunciar|estamos muito felizes em compartilhar|é com grande entusiasmo que)\b",
        "sugestao": "Diga imediatamente o que foi lançado e o benefício concreto."
    },
    {
        "id": "W11",
        "nome": "Falsa Inclusividade (Seja X ou Y)",
        "severidade": "Alta",
        "regex": r"\b(seja você um[a]?|quer você seja|não importa se você é)\b.*?\b(ou um[a]?)\b",
        "sugestao": "Especifique diretamente o público-alvo real a quem o texto se destina."
    },
    {
        "id": "W12",
        "nome": "Pivô de Falsa Conversação",
        "severidade": "Alta",
        "regex": r"\b(a verdade é que|a realidade é uma só|para ser bem sincero|olha só:?)(?=\s|$)",
        "sugestao": "Corte a introdução e vá direto ao fato."
    },
    {
        "id": "W13",
        "nome": "Fechamento Falso-Profundo (Fake-Profound Kicker)",
        "severidade": "Alta",
        "regex": r"\b(o futuro não está chegando|o futuro já começou|o futuro é agora|a única constante é a mudança|o futuro parece promissor|apenas o tempo dirá)\b",
        "sugestao": "Elimine a frase de efeito; encerre no ponto factual ou na próxima ação concreta."
    },
    {
        "id": "W14",
        "nome": "Resumo Repetitivo em Texto Curto",
        "severidade": "Média",
        "regex": r"\b(em suma|em conclusão|em resumo|concluindo, podemos dizer)\b",
        "sugestao": "Se o texto é curto, corte o resumo final; o leitor acabou de ler os pontos."
    },
    {
        "id": "W16",
        "nome": "Voz Passiva Impessoal Burocrática",
        "severidade": "Média",
        "regex": r"\b(foi observado que|foi determinado que|pôde-se constatar que|tem sido verificado que)\b",
        "sugestao": "Adote a voz ativa direta: quem fez a ação + verbo + complemento."
    },
    {
        "id": "W17",
        "nome": "Pergunta Retórica como Transição Preguiçosa",
        "severidade": "Média",
        "regex": r"\b(mas como garantir|mas como isso funciona|você já se perguntou por que|qual é a solução para)\b.*?\?",
        "sugestao": "Transforme a pergunta em afirmação de causa ou objetivo."
    },
    {
        "id": "W18",
        "nome": "Hedging Compulsivo / Incerteza Vazia",
        "severidade": "Média",
        "regex": r"\b(seria potencialmente|pode ser potencialmente|sob certas perspectivas|em certa medida parece)\b",
        "sugestao": "Seja direto sobre o cenário real e o risco comprovado."
    },
    {
        "id": "W19",
        "nome": "Substantivação em Cadeia",
        "severidade": "Média",
        "regex": r"\b(realização da|proceder à|efetuar a|implementação da)\s+([a-zá-ú]+ção)\b",
        "sugestao": "Troque a locução substantivada por um verbo de ação direta (ex: 'analisar' em vez de 'proceder à análise')."
    },
    {
        "id": "W20",
        "nome": "Atribuição Vaga (Falsa Autoridade)",
        "severidade": "Média",
        "regex": r"\b(estudos comprovam que|especialistas afirmam que|pesquisas recentes indicam que|muitos defendem que)\b",
        "sugestao": "Cite o nome e ano da fonte ou apresente o ponto como argumento direto."
    },
    {
        "id": "W22",
        "nome": "Bloco de Hashtags Genéricas",
        "severidade": "Média",
        "regex": r"(#[A-Za-z0-9_Á-ú]+\s*){3,}",
        "sugestao": "Remova o bloco de hashtags; adote busca semântica natural."
    },
    {
        "id": "W25",
        "nome": "Jargão Corporativo Oco (Buzzword)",
        "severidade": "Média",
        "regex": r"\b(mudança de paradigma|mindset|visão holística|gerar sinergia|pensar fora da caixa|elevar o patamar)\b",
        "sugestao": "Substitua a buzzword por uma descrição da ação prática."
    },
    {
        "id": "W37",
        "nome": "Objeções Imaginárias / Espantalho (Shadowboxing)",
        "severidade": "Alta",
        "regex": r"\b(você pode estar pensando que|você poderia pensar que|alguém poderia argumentar que|uma abordagem tentadora seria|não estamos dizendo que)\b",
        "sugestao": "Remova a falsa objeção e afirme a decisão e justificativa real diretamente."
    },
    {
        "id": "W38",
        "nome": "Resíduo de Chatbot (Chatbot Residue)",
        "severidade": "Alta",
        "regex": r"\b(com certeza!|certamente!|ótima pergunta!|espero que isso ajude|espero ter ajudado|fique à vontade para perguntar)\b",
        "sugestao": "Corte saudações ou despedidas robóticas remanescentes da conversa."
    }
]


def strip_code_blocks(text: str) -> str:
    """Remove blocos de código markdown (```...``` e `...`) para evitar falsos positivos em código."""
    # Preserva quebras de linha para manter a contagem de linhas correta
    def replace_with_newlines(match):
        return "\n" * match.group(0).count("\n")

    text = re.sub(r"```[\s\S]*?```", replace_with_newlines, text)
    text = re.sub(r"`[^`\n]+`", " ", text)
    return text


def analyze_text(text: str, ignore_rules=None):
    """Analisa o texto e retorna lista de violações e score de slop.
    ignore_rules: conjunto ou lista de IDs de regras a ignorar (ex: {'W12', 'W17', 'W15'})
    """
    if ignore_rules is None:
        ignore_rules = set()
    elif isinstance(ignore_rules, str):
        ignore_rules = {r.strip().upper() for r in ignore_rules.split(",") if r.strip()}
    else:
        ignore_rules = {str(r).strip().upper() for r in ignore_rules}

    lines = text.splitlines()
    clean_text = strip_code_blocks(text)
    clean_lines = clean_text.splitlines()

    violations = []
    
    # Contadores de severidade
    weights = {"Alta": 15, "Média": 7, "Baixa": 3}
    score_points = 0

    for idx, line in enumerate(clean_lines, start=1):
        # Ignora cabeçalhos ou linhas vazias para certas regras
        for rule in RULES:
            if rule["id"] in ignore_rules:
                continue
            matches = list(re.finditer(rule["regex"], line, re.IGNORECASE))
            for m in matches:
                trecho = m.group(0).strip()
                # Salva o trecho real da linha original
                violations.append({
                    "linha": idx,
                    "regra_id": rule["id"],
                    "regra_nome": rule["nome"],
                    "severidade": rule["severidade"],
                    "trecho": trecho,
                    "sugestao": rule["sugestao"]
                })
                score_points += weights.get(rule["severidade"], 5)

    # Verificação de em-dashes em excesso (W15)
    if "W15" not in ignore_rules:
        em_dash_count = len(re.findall(r"—", clean_text))
        if em_dash_count > 3:
            violations.append({
                "linha": 1,
                "regra_id": "W15",
                "regra_nome": "Travessões em Excesso (Em-dash abuse)",
                "severidade": "Média",
                "trecho": f"{em_dash_count} travessões (—) encontrados no texto",
                "sugestao": "Reduza os travessões para no máximo 1-2 em textos longos. Prefira vírgulas ou orações curtas."
            })
            score_points += 10

    # Verificação de Emojis em excesso (W21)
    if "W21" not in ignore_rules:
        emojis = re.findall(r"[🚀💡🎯🔥✨👉👏]", clean_text)
        if len(emojis) >= 3:
            violations.append({
                "linha": 1,
                "regra_id": "W21",
                "regra_nome": "Emojis Decorativos em Excesso",
                "severidade": "Média",
                "trecho": f"{len(emojis)} emojis de ênfase encontrados: {' '.join(set(emojis))}",
                "sugestao": "Corte os emojis decorativos. Deixe a força do texto carregar a mensagem."
            })
            score_points += 10

    # Cálculo da pontuação final (0 a 100)
    # Considera também a extensão do texto para normalizar
    total_words = max(len(re.findall(r"\w+", clean_text)), 1)
    normalized_ratio = (score_points / (total_words / 30.0 + 1)) * 10
    final_score = min(int(normalized_ratio), 100)

    # Nível de risco
    if final_score >= 60:
        nivel = "CRÍTICO (Texto com fortíssima textura de IA)"
    elif final_score >= 30:
        nivel = "MODERADO (Vários vícios mecânicos detectados)"
    elif final_score > 0:
        nivel = "LEVE (Pequenos ajustes de polimento recomendados)"
    else:
        nivel = "LIMPO (Texto natural, sem sinais detectáveis de IA)"

    return {
        "score": final_score,
        "nivel": nivel,
        "total_palavras": total_words,
        "total_violacoes": len(violations),
        "violacoes": violations
    }


def main():
    parser = argparse.ArgumentParser(
        description="Detector de Vícios de IA em Português do Brasil (deslop-ptbr)"
    )
    parser.add_argument("arquivo", nargs="?", help="Caminho do arquivo Markdown ou texto para auditar (opcional se usar stdin)")
    parser.add_argument("--json", action="store_true", help="Retorna saída estruturada em JSON (ideal para CI/CD)")
    parser.add_argument("--max-score", type=int, default=100, help="Falha com código 1 se o score for maior que este valor")
    parser.add_argument("--ignore", type=str, default="", help="IDs de regras a ignorar separados por vírgula (ex: --ignore W12,W17,W15)")

    args = parser.parse_args()

    if args.arquivo:
        caminho = Path(args.arquivo)
        if not caminho.is_file():
            sys.stderr.write(f"Erro: Arquivo '{args.arquivo}' não encontrado.\n")
            sys.exit(2)
        conteudo = caminho.read_text(encoding="utf-8", errors="replace")
    else:
        # Lê do stdin
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        conteudo = sys.stdin.read()

    resultado = analyze_text(conteudo, ignore_rules=args.ignore)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        # Saída amigável no terminal
        print("\n" + "=" * 65)
        print("  🔍 RELATÓRIO DE AUDITORIA DESLOP PT-BR")
        print("=" * 65)
        print(f"📊 Pontuação de IA: {resultado['score']}/100  -->  {resultado['nivel']}")
        print(f"📝 Total de palavras: {resultado['total_palavras']} | Violações encontradas: {resultado['total_violacoes']}\n")

        if not resultado["violacoes"]:
            print("✨ Parabéns! O texto está limpo e sem vícios mecânicos de IA.")
        else:
            print("-" * 65)
            for v in resultado["violacoes"]:
                tag = f"[{v['severidade'].upper()}]"
                print(f"• Linha {v['linha']} {tag} {v['regra_id']} - {v['regra_nome']}")
                print(f"   Trecho:  \"{v['trecho']}\"")
                print(f"   Sugestão: {v['sugestao']}\n")
            print("-" * 65)

    if resultado["score"] > args.max_score:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Vícios de Escrita de IA em Português do Brasil (Deslop PT-BR)
Analisa arquivos Markdown, páginas HTML ou texto comum via CLI ou Stdin.
Calcula a pontuação de IA (0 a 100), aponta os sinais de alerta (W1 a W38, W6, PROOF)
com linha/trecho e sugestão de correção, e atua como build gate em CI/CD.

Zero dependências externas (apenas biblioteca padrão do Python).
"""

import sys
import re
import argparse
import json
import html
from pathlib import Path

# Configura suporte a UTF-8 no console do Windows sem estourar UnicodeEncodeError
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


def normalise_typography(t: str) -> str:
    """Normaliza variantes tipográficas para caracteres planos esperados pelas regexes.
    
    Substitui hífens não-quebráveis, espaços duros e aspas curvas simples e duplas.
    Isso impede que regras de sintaxe fiquem cegas em textos formatados para web/print.
    """
    t = t.replace('\u2011', '-').replace('\u2013', '-')
    t = t.replace('\xa0', ' ')
    t = t.replace('’', "'").replace('‘', "'")
    t = t.replace('“', '"').replace('”', '"')
    return t


def visible_text(html_content: str) -> str:
    """Extrai apenas o texto visível que um leitor humano lê na página.
    Remove <script>, <style>, comentários e tags, e decodifica entidades HTML.
    """
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.DOTALL)
    t = re.sub(r'<[^>]+>', ' ', t)
    # Decodifica entidades numéricas e nomeadas (&amp;, &#x27;, &quot;, etc.)
    t = html.unescape(t)
    return normalise_typography(t)


def markdown_prose(md: str) -> str:
    """Extrai a prosa de um arquivo Markdown, protegendo código e isolando elementos sintáticos.
    
    Substitui inline code e texto riscado por placeholders neutros ('isto') para evitar
    fusão acidental de palavras antes e depois do bloco.
    Converte quebras de tabela (|), títulos (#) e marcadores de lista em divisores
    sintáticos ('.') para que linhas independentes não sejam lidas como uma oração contínua.
    """
    # Preserva quebras de linha em blocos de código cercados
    def replace_with_newlines(match):
        return "\n" * match.group(0).count("\n")

    md = re.sub(r'```[\s\S]*?```', replace_with_newlines, md)
    # Imagens markdown: ![alt](url) -> ponto isolado (alt não é copy do corpo)
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' . ', md)
    # Links markdown: [texto](url) -> mantém apenas o texto do link
    md = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', md)
    # Inline code e texto riscado (strikethrough) substituídos por placeholder neutro
    md = re.sub(r'`[^`\n]*`', ' isto ', md)
    md = re.sub(r'~~[\s\S]*?~~', ' isto ', md)
    # Cabeçalhos Markdown (# até ######) viram sentenças isoladas
    md = re.sub(r'^\s{0,3}#{1,6}\s*(.*)$', r' . \1 . ', md, flags=re.MULTILINE)
    # Colunas de tabela (|) viram separadores para não fundir células
    md = re.sub(r'\|', ' . ', md)
    # Marcadores de listas (- , * , + , 1.) viram separadores de sentença
    md = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+', ' . ', md, flags=re.MULTILINE)
    # Citações (>)
    md = re.sub(r'^\s*>\s?', ' . ', md, flags=re.MULTILINE)
    # Remove negrito e itálico remanescentes (* e _)
    md = re.sub(r'[*_]', ' ', md)
    return normalise_typography(md)


def strip_code_blocks(text: str) -> str:
    """Remove blocos de código markdown (```...``` e `...`) para evitar falsos positivos em código."""
    def replace_with_newlines(match):
        return "\n" * match.group(0).count("\n")

    text = re.sub(r"```[\s\S]*?```", replace_with_newlines, text)
    text = re.sub(r"`[^`\n]+`", " isto ", text)
    return normalise_typography(text)


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
        "id": "W6",
        "nome": "Tríades Ornamentais Simétricas (Tricolon)",
        "severidade": "Alta",
        "regex": r"\b(inovação|agilidade|eficiência|robustez|segurança|confiabilidade|flexibilidade|excelência|produtividade|qualidade|escalabilidade|rapidez|resiliência|inteligência|modernidade|estabilidade),\s+(inovação|agilidade|eficiência|robustez|segurança|confiabilidade|flexibilidade|excelência|produtividade|qualidade|escalabilidade|rapidez|resiliência|inteligência|modernidade|estabilidade)\s+e\s+(inovação|agilidade|eficiência|robustez|segurança|confiabilidade|flexibilidade|excelência|produtividade|qualidade|escalabilidade|rapidez|resiliência|inteligência|modernidade|estabilidade)\b",
        "sugestao": "Corte o trio de buzzwords simétricas. Diga concretamente o que o produto faz ou apresente métricas reais."
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

# Padrões de Prova Social Fabricada (Invented Social Proof)
PROOF_PATTERNS = [
    (
        r"\b(?:mais\s+de\s+|amado\s+por\s+|confiado\s+por\s+|usado\s+por\s+)?(\d[\d.]*(?:,\d+)?)\s*\+?\s*(?:de\s+)?(clientes?|usuários?|empresas?|alunos?|times?|equipes?|leitores?|profissionais|assinantes?)\s+(satisfeitos?|ativos?|felizes?|verificados?|certificados?|engajados?|parceiras?)\b",
        "Prova social com adjetivo de validação inflada ('X clientes satisfeitos/ativos')"
    ),
    (
        r"\b(?:amado|utilizado|confiado|adotado)\s+por\s+(?:mais\s+de\s+)?(\d[\d.]*(?:,\d+)?)\s*\+?\s*(clientes?|usuários?|empresas?|times?|equipes?)\b",
        "Fórmula corporativa de prova social ('confiado por X clientes')"
    ),
    (
        r"\b(\d[\d.]*(?:,\d+)?)\s*\+?\s*(?:milhões?|mil)?\s+(?:de\s+)?(clientes?|usuários?|empresas?)\s+satisfeit[oa]s?\b",
        "Número massivo com 'satisfeitos' sem fonte ou auditoria explícita"
    )
]

# Tríades com fecho retórico
RHETORICAL_TRICOLON = [
    (
        r"\b([A-Za-zÀ-ÿ]{4,}),\s+([A-Za-zÀ-ÿ]{4,})\s+e\s+(feito para durar|pronto para o futuro|com foco no cliente|pensad[oa] para você|construído para durar)\b",
        "Tríade com fecho retórico ornamental"
    ),
    (
        r"\b(rápido|seguro|inteligente|fácil|moderno|eficiente|confiável|robusto|inovador|intuitivo|ágil),\s+(rápido|seguro|inteligente|fácil|moderno|eficiente|confiável|robusto|inovador|intuitivo|ágil)\s+e\s+(rápido|seguro|inteligente|fácil|moderno|eficiente|confiável|robusto|inovador|intuitivo|ágil)\b",
        "Tríade de adjetivos promocionais simétricos"
    )
]


def analyze_text(text: str, ignore_rules=None, allow_proof=False, is_markdown=False, is_html=False):
    """Analisa o texto e retorna lista de violações e score de slop (0 a 100).
    
    ignore_rules: conjunto ou lista de IDs de regras a ignorar (ex: {'W12', 'W17', 'W15'})
    allow_proof: se True, ignora penalidade da regra PROOF (para números reais e comprovados)
    is_markdown: força limpeza via markdown_prose
    is_html: força limpeza via visible_text
    """
    if ignore_rules is None:
        ignore_rules = set()
    elif isinstance(ignore_rules, str):
        ignore_rules = {r.strip().upper() for r in ignore_rules.split(",") if r.strip()}
    else:
        ignore_rules = {str(r).strip().upper() for r in ignore_rules}

    if is_html:
        clean_text = visible_text(text)
    elif is_markdown:
        clean_text = markdown_prose(text)
    else:
        clean_text = strip_code_blocks(text)

    clean_lines = clean_text.splitlines()
    violations = []
    
    # Pesos de severidade
    weights = {"Alta": 15, "Média": 7, "Baixa": 3}
    score_points = 0

    # 1. Varredura das regras de linha por linha
    for idx, line in enumerate(clean_lines, start=1):
        for rule in RULES:
            if rule["id"] in ignore_rules:
                continue
            matches = list(re.finditer(rule["regex"], line, re.IGNORECASE))
            for m in matches:
                trecho = m.group(0).strip()
                violations.append({
                    "linha": idx,
                    "regra_id": rule["id"],
                    "regra_nome": rule["nome"],
                    "severidade": rule["severidade"],
                    "trecho": trecho,
                    "sugestao": rule["sugestao"]
                })
                score_points += weights.get(rule["severidade"], 5)

    # 2. Verificação algorítmica de Tríades Retóricas (W6)
    if "W6" not in ignore_rules:
        for pat, desc in RHETORICAL_TRICOLON:
            for m in re.finditer(pat, clean_text, re.IGNORECASE):
                trecho = m.group(0).strip()
                violations.append({
                    "linha": 1,
                    "regra_id": "W6",
                    "regra_nome": f"Tríade Ornamental ({desc})",
                    "severidade": "Alta",
                    "trecho": trecho,
                    "sugestao": "Substitua a tríade retórica por dados ou características concretas do serviço."
                })
                score_points += weights["Alta"]

    # 3. Verificação de Prova Social Fabricada (PROOF)
    if "PROOF" not in ignore_rules:
        for pat, desc in PROOF_PATTERNS:
            for m in re.finditer(pat, clean_text, re.IGNORECASE):
                trecho = m.group(0).strip()
                if allow_proof:
                    # Avisa, mas não penaliza se foi autorizado
                    violations.append({
                        "linha": 1,
                        "regra_id": "PROOF",
                        "regra_nome": f"Prova Social Auditada ({desc})",
                        "severidade": "Baixa",
                        "trecho": trecho,
                        "sugestao": "Métrica liberada via flag --allow-proof."
                    })
                else:
                    violations.append({
                        "linha": 1,
                        "regra_id": "PROOF",
                        "regra_nome": f"Falsa Prova Social Fabricada ({desc})",
                        "severidade": "Alta",
                        "trecho": trecho,
                        "sugestao": "Se o número for real e comprovável, utilize a flag --allow-proof. Caso contrário, remova ou substitua por especificação concreta."
                    })
                    score_points += weights["Alta"]

    # 4. Verificação de Travessões por Janela de Sentença (W15)
    if "W15" not in ignore_rules:
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        for s in sentences:
            for i in range(0, max(1, len(s)), 220):
                window = s[i:i + 220]
                if window.count('—') >= 2:
                    trecho_curto = window.strip()[:70] + ("..." if len(window.strip()) > 70 else "")
                    violations.append({
                        "linha": 1,
                        "regra_id": "W15",
                        "regra_nome": "Travessões em Excesso na Mesma Sentença (Em-dash abuse)",
                        "severidade": "Média",
                        "trecho": trecho_curto,
                        "sugestao": "Dois ou mais travessões na mesma oração denunciam cadência de máquina. Quebre em frases ou use vírgulas."
                    })
                    score_points += weights["Média"]
                    break

    # 5. Verificação de Emojis em excesso (W21)
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
            score_points += weights["Média"]

    # Cálculo da pontuação final (0 a 100)
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
        description="Detector de Vícios de IA em Português do Brasil (Deslop PT-BR)"
    )
    parser.add_argument("arquivo", nargs="?", help="Caminho do arquivo Markdown, HTML ou texto para auditar (opcional se usar stdin ou --text)")
    parser.add_argument("--text", type=str, help="Texto direto passado via linha de comando para análise rápida")
    parser.add_argument("--json", action="store_true", help="Retorna saída estruturada em JSON (ideal para CI/CD)")
    parser.add_argument("--max-score", type=int, default=100, help="Falha com código 1 se o score for maior que este valor (use 0 para zero-tolerance em CI)")
    parser.add_argument("--fail-if-slop", action="store_true", help="Atua como build gate estrito: falha com código 1 se qualquer vício for detectado (score > 0)")
    parser.add_argument("--ignore", type=str, default="", help="IDs de regras a ignorar separados por vírgula (ex: --ignore W12,W17,W15)")
    parser.add_argument("--allow-proof", action="store_true", help="Permite métricas e números de prova social sem penalizar o score de build")
    parser.add_argument("--markdown", action="store_true", help="Força o modo de pré-processamento de Markdown (protege código, isola tabelas/listas)")
    parser.add_argument("--view", type=str, help="Para arquivos HTML, restringe a análise à seção identificada por id=\"<view>\"")

    args = parser.parse_args()

    is_html = False
    is_markdown = args.markdown

    if args.text is not None:
        conteudo = args.text
    elif args.arquivo:
        caminho = Path(args.arquivo)
        if not caminho.is_file():
            sys.stderr.write(f"Erro: Arquivo '{args.arquivo}' não encontrado.\n")
            sys.exit(2)
        try:
            conteudo = caminho.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            sys.stderr.write(f"Erro ao ler arquivo '{args.arquivo}': {e}\n")
            sys.exit(2)
        
        if caminho.suffix.lower() in [".html", ".htm"]:
            is_html = True
            if args.view:
                # Recorta o bloco correspondente ao id informado
                start_tag = f'id="{args.view}"'
                pos = conteudo.find(start_tag)
                if pos >= 0:
                    next_tag = conteudo.find('id="view-', pos + len(start_tag))
                    conteudo = conteudo[pos:next_tag if next_tag > 0 else len(conteudo)]
                else:
                    sys.stderr.write(f"Aviso: elemento id=\"{args.view}\" não encontrado no HTML. Analisando arquivo completo.\n")
        elif caminho.suffix.lower() in [".md", ".markdown"]:
            is_markdown = True
    else:
        # Lê do stdin
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        conteudo = sys.stdin.read()

    # Rejeição de entrada vazia: um build não pode aprovar arquivo vazio gerado por falha
    if not conteudo.strip():
        sys.stderr.write("deslop-ptbr: erro — entrada vazia fornecida para auditoria.\n")
        sys.exit(1)

    resultado = analyze_text(
        conteudo,
        ignore_rules=args.ignore,
        allow_proof=args.allow_proof,
        is_markdown=is_markdown,
        is_html=is_html
    )

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print("\n" + "=" * 65)
        print("  🇧🇷 RELATÓRIO DE AUDITORIA DESLOP PT-BR")
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

    limite_score = 0 if args.fail_if_slop else args.max_score
    if resultado["score"] > limite_score:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

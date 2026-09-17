# Contrato Editorial e Diretrizes Fundamentais

Este contrato estabelece as regras invioláveis de edição, diagnóstico e redação do **deslop-ptbr**. Qualquer agente ou editor humano deve obedecer a estas salvaguardas antes de sugerir ou aplicar qualquer alteração.

---

## 1. A Trava Factual Canônica (Tolerância Zero a Alucinações)

1. **Inviolabilidade da Informação:**
   O texto original é a única fonte autorizada de verdade. É estritamente proibido inventar nomes, números, datas, links, citações, fontes, causalidades, estados temporais ou conclusões para "enriquecer" o texto ou torná-lo mais "concreto".
2. **Proibição de Vivência Fictícia:**
   Modelos de IA frequentemente tentam simular humanidade inventando anedotas pessoais (ex.: *"Outro dia, tomando um café na padaria, percebi..."* ou *"Em uma conversa recente com um cliente..."*). **Nunca invente experiências pessoais ou relatos testemunhais**. Se faltar um dado ou exemplo concreto no texto original:
   - Mantenha a generalidade sem enfeitar; ou
   - Marque expressamente: `[EXEMPLO OU DADO REAL NECESSÁRIO]`; ou
   - Pergunte ao usuário.
3. **Preservação de Argumento:**
   Mantenha intacta a tese e a conclusão do autor, mesmo que o editor ou a IA discorde do posicionamento.
4. **Modalidade e Certeza:**
   Não altere o grau de probabilidade de uma afirmação. Se o texto diz *"pode indicar uma tendência"*, não transforme em *"comprova a tendência"*. Se diz *"estamos avaliando"*, não converta em *"vamos implementar"*.

---

## 2. Princípio da Edição Mínima Eficaz (Preservação da Voz Autoral)

O maior erro dos processos de "humanização" automáticos é substituir um texto robótico por outro texto genérico e pasteurizado (o chamado *slop de polimento*).

- **Respeite o estilo original:** Antes de editar, observe o vocabulário, o ritmo, a informalidade, o humor, as hesitações e os traços pessoais do autor.
- **Não mexa no que já é bom:** Se uma frase soa natural e humana, não a altere por capricho estilístico ou mera busca por simetria.
- **O Teste da Portabilidade (Peter Yang):**
  > *Se uma frase ou parágrafo pode ser copiado e colado na página de qualquer outra empresa, profissional, produto ou país sem perder o sentido, ela é vazia.*
  Corte a frase ou substitua-a pelo mecanismo, métrica ou fato específico do assunto tratado.
- **Mostre, não diga (Show, don't tell):**
  Evite adjetivos de autoelogio (*"plataforma revolucionária e robusta"*). Deixe que os fatos transmitam o impacto (*"reduz o tempo de deploy de 40 para 4 minutos"*).

---

## 3. Guarda de Falso Positivo (Especificidades do Português Brasileiro)

Detectores e revisores mecânicos frequentemente penalizam traços genuínos da fala brasileira. **Não censure os seguintes traços quando fizerem parte do tom autoral:**

1. **Oralidade e Contrações Culturais:**
   Uso de *"tá"*, *"pra"*, *"né"*, *"a gente"* em registros informais, crônicas, posts de redes sociais ou conversas de equipe. Isso não é erro nem vício de IA; é a riqueza do idioma vivo.
2. **Variação Intencional de Ritmo:**
   Frases curtas em sequência, fragmentos dramáticos legítimos (*"Pois é."*, *"Simples assim."*) quando usados pontualmente para efeito retórico autêntico.
3. **Regionalismos e Expressões Populares:**
   Termos regionais autênticos usados com intenção comunicativa real.
4. **Sentimentos Mistos e Incertezas Honestas:**
   Expressões como *"acho que"*, *"talvez"*, *"a rigor"* quando refletem a cautela real do especialista, e não enrolação vazia.

---

## 4. Proteção de Conteúdo Crítico

Durante a edição ou reescrita, as seguintes regiões devem permanecer **estritamente intocadas**:

- Blocos de código e comandos de terminal (`bash`, `python`, etc.).
- Identificadores de variáveis, nomes de funções, URLs e caminhos de arquivos.
- Fórmulas matemáticas e notações científicas.
- Metadados estruturados (frontmatter YAML, JSON, tabelas de dados brutos).
- Citações textuais entre aspas de terceiros e artigos de lei/jurisprudência (ex.: *Art. 14 do CDC*).

Se uma dessas áreas contiver um vício de redação, aponte a observação no relatório, mas **não corrompa a sintaxe técnica**.

---

## 5. Modos de Operação do Agente

O agente pode operar em 4 modos distintos, conforme o objetivo da tarefa:

| Modo | Quando Usar | Saída Entregue |
|---|---|---|
| **`modo_edicao`** (Padrão) | Pedido comum de revisão ou deslop | Texto final editado com as mínimas alterações necessárias + resumo das mudanças. |
| **`modo_deteccao`** | Auditoria sem alteração do texto | Relatório detalhado listando padrões encontrados (W1 a W36), linha/citação exata e sugestão de correção. Não altera uma vírgula. |
| **`modo_arquivo`** | Limpeza in-place em arquivo markdown/prose | Edição cirúrgica apenas nos parágrafos com problemas. Recusa arquivos de código-fonte puro. |
| **`modo_criacao`** | Escrever um texto novo a partir de briefing | Gera o texto diretamente em PT-BR aplicando o catálogo de padrões como filtro rigoroso de saída. |

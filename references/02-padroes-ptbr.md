# Catálogo Completo de Padrões e Sinais de Alerta em PT-BR (W1 a W36)

Este catálogo reúne a síntese exaustiva dos vícios de escrita mais recorrentes gerados por Grandes Modelos de Linguagem (ChatGPT, Claude, Gemini, Llama) ao produzirem ou traduzirem textos em Português do Brasil.

Os sinais estão organizados por nível de severidade e contêm diagnóstico claro, gatilhos linguísticos, exemplos reais de **Antes (IA)** e **Depois (Humano)** e a regra de correção recomendada.

---

## 🔴 SEVERIDADE ALTA: Bandeiras Vermelhas Imediatas de IA

Estes padrões gritam autoria mecânica instantaneamente para qualquer leitor atento. Devem ser corrigidos com prioridade máxima.

---

### W1 · Gerundismo Corporativo e de Telemarketing

- **Gatilhos:** *"vou estar enviando"*, *"estaremos realizando"*, *"vai estar recebendo"*, *"iremos estar providenciando"*, *"vamos estar disponibilizando"*.
- **O Problema:** Padrão herdado de scripts de call center e e-mails corporativos burocráticos. Em textos comuns, destrói qualquer fluidez.
- **Antes (IA):**
  > *"Vou estar enviando os arquivos em anexo e estaremos realizando a análise assim que possível."*
- **Depois (Humano):**
  > *"Vou enviar os arquivos em anexo e faremos a análise assim que possível."*
- **Regra:** Converta para o presente, futuro simples ou pretérito direto. Nunca empilhe verbo auxiliar + estar + gerúndio.

---

### W2 · Gerúndio Conclusivo de Falsa Análise de Impacto

- **Gatilhos:** *"..., destacando a importância de..."*, *"..., contribuindo para o fortalecimento de..."*, *"..., demonstrando que..."*, *"..., reforçando a necessidade de..."*, *"..., consolidando sua posição..."*.
- **O Problema:** A IA encerra quase todo parágrafo com uma oração reduzida de gerúndio que finge deduzir uma grande lição moral ou de mercado, mas apenas repete o que já foi dito.
- **Antes (IA):**
  > *"A fintech atingiu 20 milhões de usuários ativos em 2025, demonstrando o compromisso com a experiência do cliente e reforçando a relevância da transformação digital no setor."*
- **Depois (Humano):**
  > *"A fintech atingiu 20 milhões de usuários ativos em 2025 e se tornou uma das três maiores do país."*
- **Regra:** Corte a oração de gerúndio redundante. Se a consequência for factual e importante, transforme-a em uma oração coordenada ou frase independente com dados reais.

---

### W3 · Conectivos Arcaicos de Oficialês em Contextos Comuns

- **Gatilhos:** *"ademais"*, *"outrossim"*, *"destarte"*, *"doravante"*, *"não obstante"*, *"nesse diapasão"*, *"no bojo de"*, *"mister se faz"*, *"cumpre salientar que"*, *"faz-se imperioso"*.
- **O Problema:** São expressões do jargão jurídico de fóruns e acórdãos do século passado. A IA as insere em posts de LinkedIn, e-mails internos e artigos de blog onde nenhum brasileiro usaria tais termos.
- **Antes (IA):**
  > *"O novo recurso aumentou a velocidade de consulta. Ademais, reduziu custos operacionais. Destarte, a equipe decidiu adotar a biblioteca."*
- **Depois (Humano):**
  > *"O novo recurso aumentou a velocidade de consulta e reduziu custos operacionais. Por isso, a equipe decidiu adotar a biblioteca."*
- **Regra:** Substitua por conectivos naturais (*"além disso"*, *"por isso"*, *"com isso"*, *"mas"*) ou simplesmente corte e una as ideias.

---

### W4 · Aberturas Genéricas e Enroladas (Throat-Clearing)

- **Gatilhos:** *"No cenário atual..."*, *"Em um mundo cada vez mais conectado..."*, *"Na era digital em que vivemos..."*, *"Vale ressaltar que..."*, *"É importante ter em mente que..."*, *"No ecossistema dinâmico de hoje..."*.
- **O Problema:** Frases pré-fabricadas que atrasam a entrega do conteúdo real e servem apenas para a IA "limpar a garganta" antes de falar algo relevante.
- **Antes (IA):**
  > *"No cenário atual, caracterizado por rápidas transformações tecnológicas, é imperioso ressaltar que a automação de testes desempenha um papel fundamental."*
- **Depois (Humano):**
  > *"A automação de testes evita que bugs simples cheguem à produção e reduz o tempo de deploy."*
- **Regra:** Delete a introdução inteira e comece imediatamente pelo sujeito e pela ação concreta.

---

### W5 · Contraste Binário Vazio ("Não é sobre X, é sobre Y")

- **Gatilhos:** *"Não se trata de X, mas sim de Y"*, *"A questão não é X, é Y"*, *"Não é apenas uma ferramenta, é uma revolução"*, *"Mais do que um produto, uma experiência"*.
- **O Problema:** Muleta retórica que cria um falso dilema dramático. Na prática, 95% das vezes o que importa é apenas a segunda parte (Y).
- **Antes (IA):**
  > *"A inteligência artificial não é sobre substituir desenvolvedores. É sobre dar superpoderes à criatividade humana."*
- **Depois (Humano):**
  > *"A inteligência artificial automatiza tarefas repetitivas e libera os desenvolvedores para problemas mais complexos."*
- **Regra:** Corte a negação inicial. Afirme a ideia positiva diretamente de forma clara e fundamentada.

---

### W6 · Tríades Ornamentais Simétricas (A Regra dos Três)

- **Gatilhos:** Listas compulsivas de três substantivos ou adjetivos abstratos (*"inovação, agilidade e excelência"*, *"simples, rápido e intuitivo"*, *"segurança, transparência e confiabilidade"*).
- **O Problema:** A IA é viciada no ritmo triádico. O resultado soa ensaiado, publicitário e desprovido de substância.
- **Antes (IA):**
  > *"Nossa solução foi desenhada para entregar eficiência, escalabilidade e robustez ao seu fluxo de trabalho."*
- **Depois (Humano):**
  > *"O sistema processa 5.000 requisições por segundo sem degradação de latência."*
- **Regra:** Escolha o benefício real específico ou substitua a lista abstrata por um fato mensurável.

---

### W7 · Revelação Teatral com Dois-Pontos

- **Gatilhos:** Sintagma nominal curto seguido de dois-pontos e uma frase com falsa dramaticidade (*"O detalhe crucial: ele funciona offline."*, *"A melhor parte: é de graça."*, *"O resultado: economia imediata."*).
- **O Problema:** Tique típico do LinkedIn americano copiado sem critério. Soa piegas e manipulativo.
- **Antes (IA):**
  > *"O segredo que ninguém te conta: o gargalo quase nunca é o banco de dados."*
- **Depois (Humano):**
  > *"Na maioria dos casos, a lentidão está na camada de serialização, e não no banco de dados."*
- **Regra:** Reescreva em uma frase declarativa direta normal. Use dois-pontos apenas para introduzir listas técnicas, definições ou citações literais.

---

### W8 · Adjetivos Superlativos de Vendas / Falsa Grandiosidade

- **Gatilhos:** *"revolucionário"*, *"game-changer"*, *"divisor de águas"*, *"robusto"*, *"sem atritos" (seamless)*, *"de ponta"*, *"inovador"*, *"impecável"*, *"transformador"*.
- **O Problema:** Adjetivos que tentam forçar o leitor a admirar o produto sem apresentar nenhuma prova empírica.
- **Antes (IA):**
  > *"Nossa plataforma de ponta oferece uma experiência revolucionária e perfeita para desenvolvedores."*
- **Depois (Humano):**
  > *"O editor tem autocompletion inteligente, suporte nativo a TypeScript e abre em menos de um segundo."*
- **Regra:** Substitua qualquer elogio vazio por especificações técnicas, números ou funcionalidades concretas.

---

### W9 · Falsos Amigos e Traduções Mecânicas do Inglês

- **Gatilhos:**
  - *"mergulhar em / nos aprofundarmos"* (tradução crua de *delve into*).
  - *"fazer sentido"* usado de forma onipresente (tradução literal de *makes sense*).
  - *"tapeçaria"* usada como metáfora de complexidade (*tapestry*).
  - *"orquestrar"* em todo contexto organizacional (*orchestrate*).
  - *"alavancar"* como único sinônimo de usar/impulsionar (*leverage*).
  - *"aninhado"* para falar de localização física (*nestled*).
- **O Problema:** Expressões em inglês que têm sentidos idiomáticos específicos viram aberrações estilísticas quando vertidas mecanicamente para o português.
- **Antes (IA):**
  > *"Vamos mergulhar na rica tapeçaria de desafios enfrentados pelo time ao alavancar essa tecnologia."*
- **Depois (Humano):**
  > *"Vamos examinar as principais dificuldades que a equipe encontrou ao adotar essa tecnologia."*
- **Regra:** Empregue verbos e substantivos cotidianos do português: *analisar*, *conjunto*, *usar*, *adotar*, *aproveitar*.

---

### W10 · Aberturas do Tipo "Excited to Announce" / Celebração Falsa

- **Gatilhos:** *"Temos o prazer de anunciar..."*, *"Estamos muito felizes em compartilhar..."*, *"É com grande entusiasmo que apresentamos..."*.
- **O Problema:** Linguagem corporativa engomada que foca nos sentimentos da empresa em vez de focar no valor para quem lê.
- **Antes (IA):**
  > *"Estamos empolgadíssimos em anunciar que a versão 2.0 do nosso software finalmente chegou!"*
- **Depois (Humano):**
  > *"Lançamos hoje a versão 2.0. A principal mudança é a exportação automática em PDF e o suporte a múltiplos workspaces."*
- **Regra:** Diga o que aconteceu e o que mudou na primeira oração.

---

### W11 · Falsa Inclusividade Condicional ("Seja você um X ou um Y")

- **Gatilhos:** *"Seja você um iniciante curioso ou um especialista veterano..."*, *"Quer você esteja começando agora ou liderando uma grande equipe..."*.
- **O Problema:** A IA tenta abraçar o universo inteiro em uma única frase e acaba não dialogando com ninguém.
- **Antes (IA):**
  > *"Seja você um estudante de programação ou um arquiteto de software renomado, este guia vai te ensinar algo novo."*
- **Depois (Humano):**
  > *"Este guia foi escrito para quem já domina Python e quer aprender a estruturar microsserviços com FastAPI."*
- **Regra:** Defina claramente o público-alvo real e fale com ele com precisão.

---

### W12 · Pivôs de Falsa Conversação

- **Gatilhos:** *"A verdade é uma só:"*, *"Aqui está a grande questão:"*, *"Para ser bem sincero,"*, *"A realidade nua e crua:"*, *"Olha só:"*.
- **O Problema:** Cria uma intimidade artificial, fazendo a IA posar como sábia iluminada que vai revelar um segredo cósmico.
- **Antes (IA):**
  > *"A verdade é que a maioria das startups falha por falta de foco comercial."*
- **Depois (Humano):**
  > *"A maioria das startups encerra as operações porque não valida clientes pagantes antes de construir o produto."*
- **Regra:** Corte a introdução e faça a afirmação de forma direta e circunstanciada.

---

### W13 · Fechamentos com Falsa Profundidade (Fake-Profound Kickers)

- **Gatilhos:** Frases de efeito no final do texto tentando criar um momento épico: *"O futuro não está chegando: ele já está aqui."*, *"Afinal, a única constante é a mudança."*, *"E no final das contas, é isso que nos torna verdadeiramente humanos."*.
- **O Problema:** Tenta fechar o texto com filosofia barata de parachoque de caminhão.
- **Antes (IA):**
  > *"Adotar boas práticas de código exige disciplina. Afinal, programar não é apenas escrever linhas de instrução, mas tecer o amanhã com a ponta dos dedos."*
- **Depois (Humano):**
  > *"Adotar boas práticas de código exige disciplina e reduz o débito técnico a longo prazo."*
- **Regra:** Elimine a metáfora forçada. Encerre com a conclusão lógica, o próximo passo ou um ponto factual.

---

### W14 · Resumo e Recapitulação Desnecessária

- **Gatilhos:** *"Em suma,"*, *"Em conclusão,"*, *"Em resumo,"*, *"Para finalizar, vimos que..."*.
- **O Problema:** Em textos curtos (posts, e-mails, artigos breves), a IA insiste em reescrever um parágrafo que apenas repete tudo que o leitor acabou de ler dois segundos atrás.
- **Antes (IA):**
  > *"Em conclusão, discutimos a importância do Docker, os benefícios dos containers e as etapas de configuração do ambiente."*
- **Depois (Humano):**
  > *(Corte total do parágrafo ou substituição pelo comando final: "Para rodar o container, execute `docker compose up -d`.")*
- **Regra:** Se o texto tem menos de 1.500 palavras, corte o resumo final. Encerre no último argumento ou numa instrução de ação concreta.

---

## 🟡 SEVERIDADE MÉDIA: Enfraquecem o Texto e Revelam IA

Estes sinais enfraquecem o dinamismo do texto, criam burocracia desnecessária e entregam a falta de convicção autoral.

---

### W15 · Travessões em Excesso (Em-dash abuse)

- **O Problema:** No inglês de IA, o travessão longo (—) é usado a cada duas frases para encaixar orações explicativas. Quando trazido ao português, quebra o ritmo natural da leitura.
- **Antes (IA):**
  > *"O framework — que foi criado por engenheiros experientes — oferece alto rendimento — sem exigir configurações complexas."*
- **Depois (Humano):**
  > *"O framework foi criado por engenheiros experientes e entrega alto desempenho sem exigir configurações complexas."*
- **Regra:** Limite o travessão a no máximo 1 ou 2 por artigo longo, apenas quando realmente superior à vírgula ou ao parêntese.

---

### W16 · Voz Passiva Sistemática e Impessoal

- **Gatilhos:** *"Foi verificado pelos pesquisadores que..."*, *"Pôde-se constatar que os dados..."*, *"Tem sido observado pelo mercado que..."*.
- **O Problema:** Oculta o sujeito responsável pela ação e deixa a frase pesada.
- **Antes (IA):**
  > *"Foi observado pela equipe de suporte que erros críticos vinham sendo causados pela atualização."*
- **Depois (Humano):**
  > *"A equipe de suporte descobriu que a atualização causava erros críticos."*
- **Regra:** Coloque quem fez a ação no início da frase (Sujeito + Verbo + Objeto).

---

### W17 · Perguntas Retóricas como Transição Preguiçosa

- **Gatilhos:** *"Mas como garantir que isso funcione?"*, *"Você já se perguntou por que isso acontece?"*, *"Qual é a solução para esse dilema?"*.
- **O Problema:** A IA usa perguntas para fugir da responsabilidade de criar uma transição argumentativa fluida.
- **Antes (IA):**
  > *"O tráfego aumentou 300%. Mas como a infraestrutura lidou com essa demanda? A resposta é simples: usamos Kubernetes."*
- **Depois (Humano):**
  > *"O tráfego aumentou 300%. Para suportar essa carga, a infraestrutura foi migrada para Kubernetes."*
- **Regra:** Transforme o par pergunta-resposta em uma afirmação causal ou de propósito (*"Para resolver X, adotamos Y"*).

---

### W18 · Ressalvas Excessivas e Falta de Posição (Hedging Compulsivo)

- **Gatilhos:** *"Pode ser potencialmente possível que..."*, *"Em certa medida, parece indicar..."*, *"Não se pode descartar a hipótese de..."*.
- **O Problema:** Medo robótico de emitir uma opinião ou assumir uma posição técnica clara.
- **Antes (IA):**
  > *"É plausível considerar que a escolha do Rust poderia, sob certas perspectivas, ser potencialmente vantajosa para microsserviços de baixa latência."*
- **Depois (Humano):**
  > *"Rust é a melhor escolha quando o microsserviço exige latência abaixo de 5 milissegundos e consumo previsível de memória."*
- **Regra:** Se há evidência ou recomendação técnica, seja firme e especifique o cenário real.

---

### W19 · Falsa Erudição e Substantivação em Cadeia

- **Gatilhos:** Empilhar substantivos terminados em *-ção* no lugar de verbos de ação simples (*"a realização da implementação da otimização"*).
- **Antes (IA):**
  > *"Procedemos à realização da migração do banco para a obtenção de uma redução nos custos."*
- **Depois (Humano):**
  > *"Migramos o banco de dados para reduzir custos."*
- **Regra:** Transforme substantivos abstratos em verbos de ação direta.

---

### W20 · Atribuição Vaga e Falaciosa ("Especialistas afirmam")

- **Gatilhos:** *"Estudos comprovam que..."*, *"Especialistas afirmam que..."*, *"É amplamente reconhecido que..."*, *"Muitos defendem que..."*.
- **O Problema:** Cita autoridades invisíveis para dar falso peso a uma frase comum.
- **Antes (IA):**
  > *"Pesquisas recentes indicam que desenvolvedores felizes produzem código melhor."*
- **Depois (Humano):**
  > *"Diga qual pesquisa (ex.: 'Segundo o relatório DORA 2024...') ou corte a falsa autoridade e trate como argumento direto."*
- **Regra:** Cite a fonte nominal com dados ou remova a muleta de autoridade.

---

### W21 · Emojis Decorativos como Muleta de Atenção

- **Gatilhos:** Títulos e listas lotados de foguetes (🚀), lâmpadas (💡), alvos (🎯), chamas (🔥) e dedos apontando (👉).
- **O Problema:** Tentativa visual forçada de disfarçar texto fraco ou superficial.
- **Regra:** Em textos técnicos, institucionais ou autorais, corte emojis decorativos. Mantenha apenas símbolos funcionais de status (✅ feito, 🟡 em andamento, 🔴 bloqueado).

---

### W22 · Blocos de Hashtags Genéricas

- **Gatilhos:** Três a dez hashtags aglomeradas no rodapé de posts (*#Inovação #Tech #IA #Liderança #FuturoDoTrabalho*).
- **Regra:** Remova os blocos de hashtags genéricas. Plataformas modernas utilizam busca semântica por texto; hashtags vazias apenas aumentam a poluição visual.

---

### W23 · Aspas de Distanciamento / Ironia Gratuita (Scare Quotes)

- **O Problema:** Colocar palavras comuns entre aspas para parecer elegante ou irônico (*"O time precisa 'vestir a camisa'"*, *"A ferramenta 'mágica' do mercado"*).
- **Regra:** Se a palavra é a correta, use-a sem aspas. Se é inadequada, escolha um termo melhor.

---

### W24 · Metadiscurso Interpretativo

- **Gatilhos:** Frases que saem do assunto para dizer ao leitor como ele deve reagir: *"Preste muita atenção nisso:"*, *"O ponto-chave aqui é:"*, *"Como você pôde ver,"*, *"Essa distinção é de suma importância:"*.
- **Regra:** Se o argumento foi bem construído, o leitor entenderá a importância sozinho. Corte o comentário externo e mantenha o foco no conteúdo.

---

### W25 · Jargões Corporativos Ocos (Buzzwords)

- **Gatilhos:** *"mudança de paradigma"*, *"mindset de crescimento"*, *"visão holística"*, *"gerar sinergia"*, *"pensar fora da caixa"*, *"elevar o patamar"*.
- **Regra:** Descreva a ação prática correspondente em português claro e objetivo.

---

### W26 · Repetição de Sinônimos em Ciclo (Synonym Cycling)

- **O Problema:** A IA evita repetir a palavra exata e cria um carrossel confuso de termos: *"O agente processa o texto. O assistente analisa o parágrafo. A ferramenta entrega a resposta."*
- **Regra:** No português técnico e informativo, a precisão supera a variação ornamental. Se a palavra exata é *servidor*, repita *servidor*.

---

## 🟢 SEVERIDADE BAIXA: Ritmo, Estatística e Cadência

Padrões sutis que não chegam a ser um erro isolado, mas que no conjunto dão ao texto aquela sensação esquisita de "foi uma máquina que escreveu".

---

### W27 · Ritmo Metronômico (Simetria Mecânica de Frases)

- **O Problema:** 4 ou mais frases consecutivas com extensão idêntica (geralmente entre 16 e 22 palavras). A leitura fica monótona e anestesiante.
- **Correção:** Quebre a cadência. Misture frases longas e explicativas com frases curtas de 3 a 5 palavras. O ritmo humano é variado e imprevisível.

---

### W28 · O Advérbio "Muito" e Intensificadores Fracos

- **Gatilhos:** *"muito rápido"*, *"extremamente importante"*, *"altamente escalável"*, *"verdadeiramente eficaz"*.
- **Correção:** Troque a dupla fraca por um adjetivo forte ou dado concreto (*"muito rápido"* ➔ *"processa em 12ms"*).

---

### W29 · Repetição Cíclica da Tese (Re-derivação)

- **O Problema:** A cada nova seção, a IA volta ao início e redefine sua premissa principal com palavras ligeiramente diferentes, em vez de fazer o argumento avançar.
- **Correção:** Declare a premissa uma única vez no momento mais adequado e use os parágrafos seguintes para aprofundar, contra-argumentar ou exemplificar.

---

### W30 · Negrito Pulverizado sem Hierarquia

- **O Problema:** Destacar em **negrito** uma palavra a cada duas linhas no meio de frases normais, sem qualquer critério hierárquico.
- **Correção:** Reserve o negrito para termos técnicos novos na primeira menção, dados numéricos críticos ou decisões de ação. Negrito é navegação visual, não enfeite.

---

### W31 · Listas de Bullets em Vez de Raciocínio Fluido

- **O Problema:** Preguiça de estruturar argumentos contínuos, transformando tudo em listas numeradas ou bullet points desnecessários.
- **Correção:** Se duas ou três frases explicam um processo com clareza, prefira texto corrido em prosa elegante. Use listas apenas para dados paralelos, requisitos técnicos ou opções de escolha.

---

### W32 · Aspas Tipográficas Inglesas (Curly Quotes)

- **O Problema:** Aspas curvas estilizadas (`“ ”` e `‘ ’`) injetadas por modelos sem formatação limpa de código.
- **Correção:** Em código, arquivos de configuração e comandos, garanta o uso estrito de aspas retas (`"` e `'`).

---

### W33 · Conectivos Mecânicos de Transição

- **Gatilhos:** Abrir todos os parágrafos com conectores padrão em sequência: *"Primeiramente..."*, *"Em segundo lugar..."*, *"Por outro lado..."*, *"Em contrapartida..."*.
- **Correção:** Crie conexões semânticas entre as ideias, retomando o sujeito ou a consequência da frase anterior em vez de usar muletas fixas.

---

### W34 · Clichês da Internet Vintage Reaquecidos por IA

- **Gatilhos:** *"uma vez visto, não dá para desver"*, *"bateu diferente"*, *"morando de aluguel na minha cabeça"*, *"disse tudo e mais um pouco"*, *"deixe essa ficha cair"*.
- **Correção:** Se a expressão não faz parte do seu estilo natural de conversa, substitua pelo sentimento ou observação literal.

---

### W35 · Falsa Profundidade com Termos da Física e Biologia

- **Gatilhos:** *"DNA da empresa"*, *"salto quântico"*, *"gravidade da situação"*, *"campo de atração magnético de clientes"*.
- **Correção:** Fale sobre estratégia, produto e cultura em termos reais de negócios e engenharia.

---

### W36 · Dramatização Desnecessária de Erros

- **Gatilhos:** *"Ops!"*, *"Infelizmente, algo deu errado."*, *"Pedimos desculpas pelo transtorno."* (em logs, terminais e respostas a desenvolvedores).
- **Correção:** Respostas técnicas não precisam de drama ou afeto artificial. Aponte o erro técnico, a causa raiz e o comando de solução.

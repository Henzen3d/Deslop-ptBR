---
name: deslop-ptbr
description: Skill de edição e deslop para o agente Hermes em Português do Brasil.
triggers:
  - "deslop"
  - "humanizar"
  - "tirar cara de ia"
  - "remover vicios de ia"
---

# Hermes Agent Skill: Deslop PT-BR

Quando este comando ou gatilho for acionado:

1. Leia `references/01-contrato-editorial.md` e `references/02-padroes-ptbr.md`.
2. Garanta a **Trava Factual Canônica**: preserve fatos, dados, códigos e nomes. Jamais alucine relatos pessoais.
3. Elimine gerundismos (*"vou estar enviando"*), orações conclusivas em gerúndio (*"..., demonstrando..."*), arcaísmos (*"ademais"*, *"outrossim"*), aberturas genéricas (*"No cenário atual..."*) e falsos amigos de tradução (*"mergulhar em"*, *"tapeçaria"*).
4. Em modo de edição, devolva apenas o texto final corrigido e um resumo breve das alterações.
5. Em modo de detecção, aponte os códigos W1 a W36 com a citação exata.

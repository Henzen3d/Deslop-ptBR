#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes unitários para o script de purificação scripts/cleanse_ptbr.py
Valida a separação entre texto limpo (STDOUT) e notas de edição (STDERR),
e o carregamento do prompt mestre.
"""

import unittest
import sys
from pathlib import Path

# Adiciona scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cleanse_ptbr import separar_corpo_e_notas, carregar_prompt_mestre, SENTINELA_NOTAS


class TestCleansePTBR(unittest.TestCase):

    def test_prompt_mestre_loads_successfully(self):
        prompt = carregar_prompt_mestre()
        self.assertIn("Você é um editor sênior humano", prompt)
        self.assertIn("<<<DESLOP-PTBR-NOTAS>>>", prompt)
        self.assertIn("ETAPA 1 — Vocabulário", prompt)

    def test_sentinel_splitting_standard(self):
        resposta_modelo = (
            "Lançamos o novo painel de controle direto no navegador.\n"
            "Ele cruza os dados das faturas em dez segundos.\n"
            f"{SENTINELA_NOTAS}\n"
            "• Cortada a abertura genérica 'No cenário atual'.\n"
            "• Removido o gerundismo 'estaremos enviando'.\n"
        )
        corpo, notas = separar_corpo_e_notas(resposta_modelo)
        self.assertIn("Lançamos o novo painel", corpo)
        self.assertNotIn("Cortada a abertura", corpo)
        self.assertNotIn(SENTINELA_NOTAS, corpo)

        self.assertIn("Cortada a abertura genérica", notas)
        self.assertIn("Removido o gerundismo", notas)

    def test_sentinel_missing_fallback(self):
        resposta_sem_sentinela = (
            "Aqui está o texto perfeitamente reescrito sem nenhum sentinela incluído."
        )
        corpo, notas = separar_corpo_e_notas(resposta_sem_sentinela)
        self.assertEqual(corpo, resposta_sem_sentinela)
        self.assertEqual(notas, "")


if __name__ == "__main__":
    unittest.main()

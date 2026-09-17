#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes unitários para scripts/detector_ptbr.py
"""

import unittest
import sys
from pathlib import Path

# Adiciona scripts ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from detector_ptbr import analyze_text, strip_code_blocks


class TestDetectorPTBR(unittest.TestCase):

    def test_gerundismo_detection(self):
        texto = "Prezados, vou estar enviando a planilha e estaremos realizando a checagem amanhã."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W1", rule_ids)
        self.assertGreater(res["score"], 0)

    def test_conclusivo_gerundio(self):
        texto = "O sistema atingiu 99% de uptime, demonstrando o compromisso com a qualidade."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W2", rule_ids)

    def test_arcaismos_oficiales(self):
        texto = "O projeto foi aprovado. Ademais, destarte cumpre salientar que os custos foram baixos."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W3", rule_ids)

    def test_abertura_generica(self):
        texto = "No cenário atual, a tecnologia desempenha um papel central."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W4", rule_ids)

    def test_falsos_amigos_traducao(self):
        texto = "Vamos mergulhar em uma rica tapeçaria de dados ao alavancar essa ferramenta."
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W9", rule_ids)

    def test_clean_human_text_passes(self):
        texto = (
            "Lançamos hoje o novo painel de controle. Ele resolve um problema antigo: "
            "cruzar os dados da fatura levava quatro horas em planilhas manuais. "
            "Agora o relatório sai em dez segundos direto no navegador."
        )
        res = analyze_text(texto)
        self.assertEqual(res["total_violacoes"], 0)
        self.assertEqual(res["score"], 0)

    def test_shadowboxing_and_chatbot_residue(self):
        texto = "Você poderia pensar que a IA substitui o autor. Certamente! Espero que isso ajude!"
        res = analyze_text(texto)
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertIn("W37", rule_ids)
        self.assertIn("W38", rule_ids)

    def test_code_blocks_are_protected(self):
        texto = """
Aqui está o código:
```python
# Não deve acusar falso positivo em código
def enviar():
    # ademais destarte outrossim
    return "vou estar enviando"
```
O código acima roda no servidor.
"""
        res = analyze_text(texto)
        # Nenhuma regra de W1 ou W3 deve disparar porque está dentro do bloco de código
        rule_ids = [v["regra_id"] for v in res["violacoes"]]
        self.assertNotIn("W1", rule_ids)
        self.assertNotIn("W3", rule_ids)


if __name__ == "__main__":
    unittest.main()
